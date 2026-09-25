"""Host composition: energy-harvester voltage proxy + offgrid first_boot.

STATUS next-priority (host path). Caller-supplied pack volts only, or
pack volts obtained through host_voltage_reader.feed_via_reader.
Optional joules estimate when C_farads is explicit (Model 05 host helper).
Never claims ADC, firmware, or field measurement.
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
from host_voltage_reader import feed_via_reader  # noqa: E402
from supercap_voltage_proxy import joules_from_voltage  # noqa: E402


def compose_first_boot(
    pack_volts: float,
    *,
    infer_requested: bool = True,
    allow_secondary_llm: bool = False,
    C_farads: Optional[float] = None,
    v_min_useful: float = 3.3,
    via_host_reader: bool = False,
    reader_source: str = "host_placeholder",
) -> dict:
    """Compose host voltage proxy (optional) with first_boot refuse path.

    When via_host_reader is True, pack_volts is first wrapped through
    host_voltage_reader.feed_via_reader so the documented feed contract
    is exercised. C_farads must be explicit to attach estimated_joules.
    Unknown C is not a license to guess. Output is always host-sourced;
    is_field_measurement stays False.
    """
    feed_volts = float(pack_volts)
    reader_meta = None
    if via_host_reader:
        feed_volts, reader_meta = feed_via_reader(
            feed_volts, source=reader_source
        )
    boot = first_boot(
        feed_volts,
        infer_requested=infer_requested,
        allow_secondary_llm=allow_secondary_llm,
    )
    estimated_joules = None
    joules_note = "C_farads not supplied; joules left unset (honest)"
    if C_farads is not None:
        if float(C_farads) <= 0.0:
            raise ValueError("C_farads must be positive when supplied")
        estimated_joules = joules_from_voltage(
            feed_volts,
            float(C_farads),
            v_min_useful=float(v_min_useful),
        )
        joules_note = (
            "analytic E=0.5*C*(V^2-Vmin^2); C is caller-supplied, not calibrated"
        )
    out = {
        **boot,
        "estimated_joules": estimated_joules,
        "C_farads_used": float(C_farads) if C_farads is not None else None,
        "joules_note": joules_note,
        "composition": "energy_harvester_proxy + offgrid_first_boot",
        "via_host_reader": bool(via_host_reader),
        "source": "host_compose_first_boot",
        "is_field_measurement": False,
        "is_firmware": False,
    }
    if reader_meta is not None:
        out.update(reader_meta)
    return out


def demo_rows() -> list[dict]:
    """Controlled host rows: below floor, above floor, with/without C, reader-fed."""
    return [
        compose_first_boot(3.2, infer_requested=True),
        compose_first_boot(3.8, infer_requested=True, C_farads=1.0),
        compose_first_boot(3.8, infer_requested=False),
        compose_first_boot(4.0, infer_requested=True, allow_secondary_llm=True, C_farads=2.0),
        compose_first_boot(
            3.2,
            infer_requested=True,
            via_host_reader=True,
            reader_source="host_placeholder",
        ),
        compose_first_boot(
            3.8,
            infer_requested=True,
            C_farads=1.0,
            via_host_reader=True,
            reader_source="hardware_pending",
        ),
    ]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        v = float(sys.argv[1])
        c = float(sys.argv[2]) if len(sys.argv) > 2 else None
        print(json.dumps(compose_first_boot(v, C_farads=c), indent=2))
    else:
        print(json.dumps(demo_rows(), indent=2))
