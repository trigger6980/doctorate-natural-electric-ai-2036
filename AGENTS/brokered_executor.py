"""Connect Model 11 energy broker to the Operator AI task graph.

Design contract (Model 11):
- Grant before run.
- Grant of 0 (or grant < min_joules) maps to skip, not an exception.
- Never over-allocate the pool.
- Local pool only; no radio mesh.

This module does not replace TaskGraphExecutor.run. It asks the broker
once per tick for every still-pending ready task, then runs only those
that received a full min_joules grant.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from energy_broker import EnergyRequest, allocate, estimate_broker_cost_j
from task_graph_executor import Checkpoint, Task, TaskGraphExecutor


def _priority_for(task: Task) -> int:
    if "priority" in task.tags:
        # tags may contain "priority:3"
        for tag in task.tags:
            if tag.startswith("priority:"):
                try:
                    return int(tag.split(":", 1)[1])
                except ValueError:
                    return 0
    if "transmit" in task.tags:
        return 3
    if "infer" in task.tags:
        return 2
    if "sense" in task.tags:
        return 1
    return 0


def brokered_run(
    executor: TaskGraphExecutor,
    estimated_joules: float,
    reserve_j: float = 0.0,
    context: Optional[Dict[str, Any]] = None,
    checkpoint: Optional[Checkpoint] = None,
) -> Checkpoint:
    """Allocate once, then run granted tasks in dependency order.

    Broker overhead is subtracted from the pool first (placeholder cost).
    Tasks that are not granted are left pending; aborted_reason records skips.
    """
    cp = checkpoint or Checkpoint()
    if context:
        cp.context.update(context)

    pending: List[Task] = [t for t in executor.tasks.values() if t.name not in cp.completed]
    overhead = estimate_broker_cost_j(len(pending))
    pool = max(0.0, float(estimated_joules) - overhead)

    requests = [
        EnergyRequest(agent_id=t.name, want_j=t.min_joules, priority=_priority_for(t))
        for t in pending
    ]
    grants = allocate(pool_j=pool, requests=requests, reserve_j=reserve_j)
    granted_map = {g.agent_id: g.granted_j for g in grants}
    cp.context["_broker_grants"] = granted_map
    cp.context["_broker_overhead_j"] = overhead
    cp.context["_broker_reserve_j"] = reserve_j

    runnable = []
    skipped = []
    for task in pending:
        got = granted_map.get(task.name, 0.0)
        if got + 1e-15 >= task.min_joules and task.min_joules > 0.0:
            runnable.append(task)
        elif task.min_joules == 0.0:
            runnable.append(task)
        else:
            skipped.append(task.name)

    if not runnable:
        cp.aborted_reason = "broker_refused_all" if pending else None
        cp.context["_remaining_joules"] = pool
        cp.context["_broker_skipped"] = skipped
        return cp

    gated = TaskGraphExecutor(runnable)
    # Give the subgraph the sum of its grants so energy_gate still applies.
    budget = sum(granted_map.get(t.name, 0.0) for t in runnable)
    out = gated.run(estimated_joules=budget, checkpoint=cp)
    out.context["_broker_skipped"] = skipped
    if skipped and out.aborted_reason is None:
        out.aborted_reason = "broker_partial:" + ",".join(skipped)
    return out
