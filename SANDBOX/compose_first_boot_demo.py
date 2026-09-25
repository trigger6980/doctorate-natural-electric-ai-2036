"""Host composition: energy-harvester voltage proxy + offgrid first_boot.

STATUS next-priority #2 (optional thin host demo). Caller-supplied pack
volts only. Optional joules estimate when C_farads is explicit (Model 05
host helper). Never claims ADC, firmware, or field measurement.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "energy-harvester-tinyml" / "src"))
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "offgrid-ai-box"))

from first_boot import first_boot  # noqa: E402
from supercap_voltage_proxy import joules_from_voltage  # noqa: E402


def compose_first_boot(
    pack_volts: float,
    *,
    infer_requested: bool = True,
    allow_secondary_llm: bool = False,
    C_farads: Optional[float] = None,
    v_min_useful: float = 3.3,
) -> dict:
    """Compose host voltage proxy (optional) with first_boot refuse path.

    C_farads must be explicit to attach estimated_joules. Unknown C is not
    a license to guess. Output is always host-sourced.
    """
    boot = first_boot(
        float(pack_volts),
        infer_requested=infer_requested,
        allow_secondary_llm=allow_secondary_llm,
    )
    estimated_joules = None
    joules_note = "C_farads not supplied; joules left unset (honest)"
    if C_farads is not None:
        if float(C_farads) <= 0.0:
            raise ValueError("C_farads must be positive when supplied")
        estimated_joules = joules_from_voltage(
            float(pack_volts),
            float(C_farads),
            v_min_useful=float(v_min_useful),
        )
        joules_note = (
            "analytic E=0.5*C*(V^2-Vmin^2); C is caller-supplied, not calibrated"
        )
    return {
        **boot,
        "estimated_joules": estimated_joules,
        "C_farads_used": float(C_farads) if C_farads is not None else None,
        "joules_note": joules_note,
        "composition": "energy_harvester_proxy + offgrid_first_boot",
        "source": "host_compose_first_boot",
        "is_field_measurement": False,
        "is_firmware": False,
    }


def demo_rows() -> list[dict]:
    """Controlled host rows: below floor, above floor, with/without C."""
    return [
        compose_first_boot(3.2, infer_requested=True),
        compose_first_boot(3.8, infer_requested=True, C_farads=1.0),
        compose_first_boot(3.8, infer_requested=False),
        compose_first_boot(4.0, infer_requested=True, allow_secondary_llm=True, C_farads=2.0),
    ]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        v = float(sys.argv[1])
        c = float(sys.argv[2]) if len(sys.argv) > 2 else None
        print(json.dumps(compose_first_boot(v, C_farads=c), indent=2))
    else:
        print(json.dumps(demo_rows(), indent=2))
