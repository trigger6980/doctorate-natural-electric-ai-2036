"""Map Off-Grid AI Box energy_duty decisions onto the Operator AI policy Action.

Host path only. Does not read an ADC. Does not claim measured joules.
Compatible with AGENTS/policy_gated_executor.Action and decide_and_run(policy_fn=...).
"""

from __future__ import annotations

from typing import Callable, Optional

from energy_duty import FLOOR_VOLTS, decide

# Local string constants so this module stays importable without AGENTS on path
# when only the prototype tree is on sys.path. The policy_fn returned still
# yields the same names as policy_gated_executor.Action.
ACTION_SLEEP = "SLEEP"
ACTION_SENSE = "SENSE"
ACTION_INFER = "INFER"
ACTION_TRANSMIT = "TRANSMIT"

DUTY_TO_POLICY = {
    "SLEEP": ACTION_SLEEP,
    "REFUSE": ACTION_SLEEP,  # low pack → refuse graph (same as policy_sleep)
    "IDLE_LISTEN": ACTION_SENSE,  # listen maps to sense-class allowance
    "INFER": ACTION_INFER,
}


def duty_string_to_policy_action(duty: str) -> str:
    """Map a energy_duty.decide() string to a policy action name."""
    key = (duty or "").strip().upper()
    if key not in DUTY_TO_POLICY:
        raise ValueError(f"unknown duty action: {duty!r}")
    return DUTY_TO_POLICY[key]


def make_duty_policy_fn(
    *,
    infer_requested: bool = True,
    floor_volts: float = FLOOR_VOLTS,
) -> Callable:
    """Return a policy_fn(EnergyState, PolicyConfig) -> Action for decide_and_run.

    Uses pack voltage from EnergyState.voltage_v. Ignores estimated_joules for
    the duty decision (joules remain a separate gate inside the task graph).
    Returns Action enum members when policy_gated_executor is importable;
    otherwise returns the string names (tests may assert either).
    """

    def policy_fn(state, cfg):
        volts = float(getattr(state, "voltage_v", 0.0))
        duty = decide(volts, infer_requested=infer_requested, floor_volts=floor_volts)
        name = duty_string_to_policy_action(duty)
        try:
            from policy_gated_executor import Action  # type: ignore

            return Action[name]
        except Exception:
            return name

    return policy_fn


def fixture_log(
    voltages: list[float],
    *,
    infer_requested: bool = True,
    floor_volts: float = FLOOR_VOLTS,
) -> list[dict]:
    """Controlled host voltage → duty → policy-action log. Not a field certificate."""
    rows = []
    for v in voltages:
        duty = decide(float(v), infer_requested=infer_requested, floor_volts=floor_volts)
        policy = duty_string_to_policy_action(duty)
        rows.append(
            {
                "pack_volts": float(v),
                "infer_requested": bool(infer_requested),
                "duty": duty,
                "policy_action": policy,
                "source": "host_fixture",
                "is_field_measurement": False,
            }
        )
    return rows
