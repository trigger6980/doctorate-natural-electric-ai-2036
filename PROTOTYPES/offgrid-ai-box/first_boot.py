"""Host first-boot refuse sketch for the Off-Grid AI Box.

Not firmware. Not an ADC driver. Reads a caller-supplied pack voltage
(the same interface as energy_duty.decide) and returns a boot record
that either allows the primary TinyML path or refuses inference.

STATUS next-priority #4: first-boot script that refuses inference
below the documented floor — still host / documentation until hardware exists.
"""

from __future__ import annotations

from energy_duty import FLOOR_VOLTS, decide
from duty_to_policy import duty_string_to_policy_action

PRIMARY_WORKLOAD = "tinyml_policy"
SECONDARY_WORKLOAD = "offline_llm"


def first_boot(
    pack_volts: float,
    *,
    infer_requested: bool = True,
    allow_secondary_llm: bool = False,
    floor_volts: float = FLOOR_VOLTS,
) -> dict:
    """Return a host boot record. Never claims field measurement."""
    duty = decide(
        float(pack_volts),
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
    return {
        "pack_volts": float(pack_volts),
        "floor_volts": float(floor_volts),
        "infer_requested": bool(infer_requested),
        "duty": duty,
        "policy_action": policy,
        "inference_allowed": not refuse,
        "workload": workload,
        "source": "host_first_boot",
        "is_field_measurement": False,
        "is_firmware": False,
    }


if __name__ == "__main__":
    import json
    import sys

    volts = float(sys.argv[1]) if len(sys.argv) > 1 else 3.2
    print(json.dumps(first_boot(volts), indent=2))
