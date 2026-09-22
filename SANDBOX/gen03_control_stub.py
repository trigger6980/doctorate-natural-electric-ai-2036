"""Host stub for Generator 03 refuse/run names.

Uses plant_observe_ok from the energy-aware scheduler. Does not invent
joules, COP, or firmware wiring to a heat stage.
"""

from __future__ import annotations

import sys
from enum import Enum, auto
from pathlib import Path

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
