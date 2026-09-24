"""Gate a task graph behind Model 01's threshold policy (or a compatible policy).

Host-side only. Does not talk to hardware. The default policy mirrors
`simple_threshold_policy` so this module can be tested without importing
across prototype paths.

Optional Model 49 preflight (`gas_search`) records a research skip token.
That token is not an architecture certificate and is not an enterprise
inquiry decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, Mapping, Optional

from task_graph_executor import Checkpoint, TaskGraphExecutor


class Action(Enum):
    SLEEP = auto()
    SENSE = auto()
    INFER = auto()
    TRANSMIT = auto()


@dataclass
class EnergyState:
    voltage_v: float
    estimated_joules: float
    lux: Optional[float] = None


@dataclass
class PolicyConfig:
    v_min_safe: float = 3.3
    v_high: float = 4.5
    infer_cost_j: float = 0.009
    tx_cost_j: float = 0.05
    sense_cost_j: float = 0.002


def simple_threshold_policy(state: EnergyState, cfg: PolicyConfig) -> Action:
    if state.voltage_v < cfg.v_min_safe:
        return Action.SLEEP
    if state.voltage_v >= cfg.v_high and state.estimated_joules > cfg.tx_cost_j:
        return Action.TRANSMIT
    if state.estimated_joules > cfg.infer_cost_j:
        return Action.INFER
    if state.estimated_joules > cfg.sense_cost_j:
        return Action.SENSE
    return Action.SLEEP


ALLOWED_WHEN_SLEEP: frozenset = frozenset()
ALLOWED_WHEN_SENSE = frozenset({"sense"})
ALLOWED_WHEN_INFER = frozenset({"sense", "infer"})
ALLOWED_WHEN_TRANSMIT = frozenset({"sense", "infer", "transmit"})


def allowed_task_tags(action: Action) -> frozenset:
    return {
        Action.SLEEP: ALLOWED_WHEN_SLEEP,
        Action.SENSE: ALLOWED_WHEN_SENSE,
        Action.INFER: ALLOWED_WHEN_INFER,
        Action.TRANSMIT: ALLOWED_WHEN_TRANSMIT,
    }[action]


def _energy_mapping(state: EnergyState) -> Dict[str, float]:
    return {"voltage_v": state.voltage_v, "rail_voltage_v": state.voltage_v}


def apply_gas_preflight(
    checkpoint: Optional[Checkpoint],
    state: EnergyState,
    gas_search: Optional[Mapping[str, Any]],
) -> Optional[Checkpoint]:
    """If gas_search is provided and refuse_reason is not ok, abort early.

    gas_search keys used: search_table, hold_gas, plus any kwargs accepted
    by gas_search_gate.refuse_reason except energy_state / v_min_safe
    (those come from EnergyState / PolicyConfig when decide_and_run calls).
    """
    if not gas_search:
        return None
    from gas_search_gate import gas_action, refuse_reason

    table = gas_search.get("search_table")
    hold = gas_search.get("hold_gas")
    extra = {
        k: v
        for k, v in gas_search.items()
        if k not in {"search_table", "hold_gas", "energy_state", "v_min_safe"}
    }
    reason = refuse_reason(_energy_mapping(state), table, hold, **extra)
    action = gas_action(_energy_mapping(state), table, hold, **extra)
    if reason == "ok":
        cp = checkpoint or Checkpoint()
        cp.context["_gas_reason"] = "ok"
        cp.context["_gas_action"] = action
        return None

    cp = checkpoint or Checkpoint()
    cp.aborted_reason = f"gas_{reason}"
    cp.context["_gas_reason"] = reason
    cp.context["_gas_action"] = action
    cp.context["_remaining_joules"] = state.estimated_joules
    return cp


def decide_and_run(
    executor: TaskGraphExecutor,
    state: EnergyState,
    cfg: Optional[PolicyConfig] = None,
    policy_fn: Optional[Callable[[EnergyState, PolicyConfig], Action]] = None,
    context: Optional[Dict[str, Any]] = None,
    checkpoint: Optional[Checkpoint] = None,
    task_tags: Optional[Dict[str, str]] = None,
    gas_search: Optional[Mapping[str, Any]] = None,
) -> Checkpoint:
    """Run the graph only for tasks whose tag is allowed by the policy action.

    task_tags maps task name -> one of sense|infer|transmit.
    Untagged tasks are treated as infer (must have at least INFER energy).

    gas_search, when provided, is a research preflight (Model 49). A refuse
    token becomes aborted_reason='gas_<reason>'. Passing preflight does not
    certify an architecture search.
    """
    cfg = cfg or PolicyConfig()
    gas_abort = apply_gas_preflight(checkpoint, state, gas_search)
    if gas_abort is not None:
        return gas_abort

    policy = policy_fn or simple_threshold_policy
    action = policy(state, cfg)
    allowed = allowed_task_tags(action)

    if action is Action.SLEEP:
        cp = checkpoint or Checkpoint()
        cp.aborted_reason = "policy_sleep"
        cp.context["_policy_action"] = action.name
        cp.context["_remaining_joules"] = state.estimated_joules
        return cp

    tags = task_tags or {}
    allowed_tasks = []
    for name, task in executor.tasks.items():
        tag = tags.get(name, "infer")
        if tag in allowed:
            allowed_tasks.append(task)

    if not allowed_tasks:
        cp = checkpoint or Checkpoint()
        cp.aborted_reason = f"policy_{action.name.lower()}_no_matching_tasks"
        cp.context["_policy_action"] = action.name
        cp.context["_remaining_joules"] = state.estimated_joules
        return cp

    gated = TaskGraphExecutor(allowed_tasks)
    cp = gated.run(
        estimated_joules=state.estimated_joules,
        context=context,
        checkpoint=checkpoint,
    )
    cp.context["_policy_action"] = action.name
    if gas_search:
        cp.context.setdefault("_gas_reason", "ok")
    return cp
