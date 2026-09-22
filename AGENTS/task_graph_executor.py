"""Minimal Operator AI task-graph executor.

Designed for intermittent, energy-aware nodes. Tasks are pure functions or
callables registered by name. Execution is sequential with optional energy
gates and checkpointing so a run can resume after a brown-out.

This is a host-side skeleton. Hardware integration and parallel dispatch
are explicit next steps, not implied as complete.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass
class Task:
    name: str
    fn: Callable[[Dict[str, Any]], Dict[str, Any]]
    min_joules: float = 0.0
    depends_on: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class Checkpoint:
    completed: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    aborted_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "completed": list(self.completed),
            "context": dict(self.context),
            "aborted_reason": self.aborted_reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Checkpoint":
        return cls(
            completed=list(data.get("completed") or []),
            context=dict(data.get("context") or {}),
            aborted_reason=data.get("aborted_reason"),
        )

    def save(self, path: Union[str, Path]) -> Path:
        """Host-side stand-in for flash. Writes JSON. Not a hardware driver."""
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return dest

    @classmethod
    def load(cls, path: Union[str, Path]) -> "Checkpoint":
        dest = Path(path)
        data = json.loads(dest.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("checkpoint file must contain a JSON object")
        return cls.from_dict(data)


class TaskGraphExecutor:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.name: t for t in tasks}
        self._validate_deps()

    def _validate_deps(self) -> None:
        for task in self.tasks.values():
            for dep in task.depends_on:
                if dep not in self.tasks:
                    raise ValueError(f"Unknown dependency {dep!r} for task {task.name!r}")

    def run(
        self,
        estimated_joules: float,
        context: Optional[Dict[str, Any]] = None,
        checkpoint: Optional[Checkpoint] = None,
    ) -> Checkpoint:
        cp = checkpoint or Checkpoint()
        if context:
            cp.context.update(context)
        remaining_j = float(estimated_joules)

        pending = [t for t in self.tasks.values() if t.name not in cp.completed]
        safety = 0
        while pending and safety < 256:
            safety += 1
            progressed = False
            still: List[Task] = []
            for task in pending:
                if not all(d in cp.completed for d in task.depends_on):
                    still.append(task)
                    continue
                # Equality must be allowed; float subtraction can land a hair under.
                if remaining_j + 1e-12 < task.min_joules:
                    cp.aborted_reason = (
                        f"energy_gate:{task.name}:need={task.min_joules}:have={remaining_j:.6f}"
                    )
                    still.append(task)
                    continue
                result = task.fn(cp.context)
                if result:
                    cp.context.update(result)
                remaining_j = max(0.0, remaining_j - task.min_joules)
                cp.completed.append(task.name)
                progressed = True
            pending = still
            if not progressed:
                if cp.aborted_reason is None and pending:
                    cp.aborted_reason = "blocked_on_dependencies_or_energy"
                break
        cp.context["_remaining_joules"] = remaining_j
        return cp
