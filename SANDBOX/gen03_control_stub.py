"""Host stub for Generator 03 refuse/run names.

Uses plant_observe_ok from the energy-aware scheduler. Does not invent
joules, COP, or firmware wiring to a heat stage.
"""

from __future__ import annotations

import sys
from enum import Enum, auto
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "energy-harvester-tinyml" / "src"))

from energy_aware_scheduler import EnergyState, PolicyConfig, plant_observe_ok  # noqa: E402


class Gen03State(Enum):
    IDLE = auto()
    CHARGE = auto()
    HEAT_PUMP_RUN = auto()
    PELTIER_ASSIST = auto()
    REFUSE = auto()
    TEG_TRICKLE = auto()


def decide_gen03(
    state: EnergyState,
    cfg: PolicyConfig,
    *,
    storage_above_floor: bool,
    pv_present: bool,
    heat_pump_ok: bool = False,
    peltier_ok: bool = False,
    teg_delta_present: bool = False,
) -> Gen03State:
    """Name a control state. Refuse beats run. Missing tank T is refuse."""
    if not plant_observe_ok(state, cfg):
        return Gen03State.REFUSE
    if not storage_above_floor:
        return Gen03State.CHARGE if pv_present else Gen03State.IDLE
    if heat_pump_ok:
        return Gen03State.HEAT_PUMP_RUN
    if peltier_ok:
        return Gen03State.PELTIER_ASSIST
    if teg_delta_present:
        return Gen03State.TEG_TRICKLE
    return Gen03State.CHARGE if pv_present else Gen03State.IDLE


def named_host_scenarios() -> list[dict[str, Any]]:
    """Labeled host scenarios for the sandbox log. Flags are inputs, not measurements."""
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    rows = [
        {
            "id": "missing_tank_t",
            "state": EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=None),
            "storage_above_floor": True,
            "pv_present": True,
            "heat_pump_ok": True,
        },
        {
            "id": "tank_at_target",
            "state": EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=55.0),
            "storage_above_floor": True,
            "pv_present": True,
            "heat_pump_ok": True,
        },
        {
            "id": "heat_pump_below_target",
            "state": EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=40.0),
            "storage_above_floor": True,
            "pv_present": True,
            "heat_pump_ok": True,
        },
        {
            "id": "below_floor_with_pv",
            "state": EnergyState(voltage_v=3.4, estimated_joules=0.02, tank_t_c=40.0),
            "storage_above_floor": False,
            "pv_present": True,
        },
        {
            "id": "teg_trickle_only",
            "state": EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=40.0),
            "storage_above_floor": True,
            "pv_present": False,
            "heat_pump_ok": False,
            "peltier_ok": False,
            "teg_delta_present": True,
        },
    ]
    out: list[dict[str, Any]] = []
    for row in rows:
        state = row["state"]
        kwargs = {k: v for k, v in row.items() if k not in ("id", "state")}
        decision = decide_gen03(state, cfg, **kwargs)
        out.append(
            {
                "id": row["id"],
                "decision": decision.name,
                "tank_t_c": state.tank_t_c,
                "flags": kwargs,
                "note": "Host names only. Flags are scenario inputs, not field sensors.",
            }
        )
    return out
