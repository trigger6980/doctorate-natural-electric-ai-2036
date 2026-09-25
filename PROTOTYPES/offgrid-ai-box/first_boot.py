"""Host first-boot refuse sketch for the Off-Grid AI Box.

Not firmware. Not an ADC driver. Reads a caller-supplied pack voltage
(the same interface as energy_duty.decide) and returns a boot record
that either allows the primary TinyML path or refuses inference.

Optional via_host_reader path exercises the same host_voltage_reader
feed contract already used by duty_to_policy.fixture_log and
compose_first_boot_demo: pack_volts pass through feed_via_reader before
decide. Sources remain host_placeholder | hardware_pending only;
is_field_measurement stays False.

STATUS: first-boot refuse sketch that refuses inference below the
documented floor — still host / documentation until hardware exists.
"""

from __future__ import annotations

from energy_duty import FLOOR_VOLTS, decide
from duty_to_policy import duty_string_to_policy_action
from host_voltage_reader import feed_via_reader

PRIMARY_WORKLOAD = "tinyml_policy"
SECONDARY_WORKLOAD = "offline_llm"


def first_boot(
    pack_volts: float,
    *,
    infer_requested: bool = True,
    allow_secondary_llm: bool = False,
    floor_volts: float = FLOOR_VOLTS,
    via_host_reader: bool = False,
    reader_source: str = "host_placeholder",
) -> dict:
    """Return a host boot record. Never claims field measurement.

    When via_host_reader is True, pack_volts is wrapped through
    host_voltage_reader.feed_via_reader so the documented feed contract
    is exercised before energy_duty.decide. Reader meta tags are
    recorded on the boot record; is_field_measurement remains False.
    """
    feed_volts = float(pack_volts)
    reader_meta = None
    if via_host_reader:
        feed_volts, reader_meta = feed_via_reader(
            feed_volts, source=reader_source
        )
    duty = decide(
        feed_volts,
        infer_requested=infer_requested,
        floor_volts=floor_volts,
    )
    policy = duty_string_to_policy_action(duty)
    refuse = duty in ("REFUSE", "SLEEP") or policy == "SLEEP"
    workload = None
    if not refuse and infer_requested:
        workload = (
            SECONDARY_WORKLOAD if allow_secondary_llm else PRIMARY_WORKLOAD
        )
    out = {
        "pack_volts": feed_volts,
        "floor_volts": float(floor_volts),
        "infer_requested": bool(infer_requested),
        "duty": duty,
        "policy_action": policy,
        "inference_allowed": not refuse,
        "workload": workload,
        "via_host_reader": bool(via_host_reader),
        "source": "host_first_boot",
        "is_field_measurement": False,
        "is_firmware": False,
    }
    if reader_meta is not None:
        out.update(reader_meta)
    return out


if __name__ == "__main__":
    import json
    import sys

    volts = float(sys.argv[1]) if len(sys.argv) > 1 else 3.2
    print(json.dumps(first_boot(volts), indent=2))
