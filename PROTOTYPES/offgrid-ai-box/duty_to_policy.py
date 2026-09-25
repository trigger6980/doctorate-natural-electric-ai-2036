"""Map Off-Grid AI Box energy_duty decisions onto the Operator AI policy Action.

Host path only. Does not read an ADC. Does not claim measured joules.
Compatible with AGENTS/policy_gated_executor.Action and decide_and_run(policy_fn=...).

Optional via_host_reader path exercises the same host_voltage_reader feed
contract already used by first_boot / compose_first_boot_demo: pack_volts
pass through read_pack_volts + as_feed before decide. Sources remain
host_placeholder | hardware_pending only; is_field_measurement stays False.
"""

from __future__ import annotations

from typing import Callable, Optional

from energy_duty import FLOOR_VOLTS, decide
from host_voltage_reader import as_feed, read_pack_volts

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
    via_host_reader: bool = False,
    reader_source: str = "host_placeholder",
) -> list[dict]:
    """Controlled host voltage → duty → policy-action log. Not a field certificate.

    When via_host_reader is True, each voltage is wrapped through
    host_voltage_reader.read_pack_volts + as_feed so the documented feed
    contract is exercised before energy_duty.decide. Reader meta tags are
    recorded on each row; is_field_measurement remains False.
    """
    rows = []
    for v in voltages:
        feed_volts = float(v)
        reader_meta = None
        if via_host_reader:
            reading = read_pack_volts(feed_volts, source=reader_source)
            feed_volts = as_feed(reading)
            reader_meta = {
                "reader_source": reading["source"],
                "reader_is_field_measurement": reading["is_field_measurement"],
                "reader_is_firmware": reading["is_firmware"],
            }
        duty = decide(
            feed_volts, infer_requested=infer_requested, floor_volts=floor_volts
        )
        policy = duty_string_to_policy_action(duty)
        row = {
            "pack_volts": feed_volts,
            "infer_requested": bool(infer_requested),
            "duty": duty,
            "policy_action": policy,
            "via_host_reader": bool(via_host_reader),
            "source": "host_fixture",
            "is_field_measurement": False,
            "is_firmware": False,
        }
        if reader_meta is not None:
            row.update(reader_meta)
        rows.append(row)
    return rows
