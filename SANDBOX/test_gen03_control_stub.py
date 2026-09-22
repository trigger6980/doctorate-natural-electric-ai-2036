"""Host tests for Generator 03 control names. No invented watts."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "SANDBOX"))
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "energy-harvester-tinyml" / "src"))

from energy_aware_scheduler import EnergyState, PolicyConfig
from gen03_control_stub import Gen03State, decide_gen03, named_host_scenarios


def test_missing_tank_is_refuse():
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    state = EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=None)
    assert decide_gen03(state, cfg, storage_above_floor=True, pv_present=True, heat_pump_ok=True) == Gen03State.REFUSE


def test_tank_at_target_is_refuse():
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    state = EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=55.0)
    assert decide_gen03(state, cfg, storage_above_floor=True, pv_present=True, heat_pump_ok=True) == Gen03State.REFUSE


def test_heat_pump_when_below_target_and_surplus():
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    state = EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=40.0)
    assert (
        decide_gen03(state, cfg, storage_above_floor=True, pv_present=True, heat_pump_ok=True)
        == Gen03State.HEAT_PUMP_RUN
    )


def test_below_floor_charges_when_pv():
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    state = EnergyState(voltage_v=3.4, estimated_joules=0.02, tank_t_c=40.0)
    assert decide_gen03(state, cfg, storage_above_floor=False, pv_present=True) == Gen03State.CHARGE


def test_teg_trickle_does_not_start_heat():
    cfg = PolicyConfig(require_tank_t_for_heat=True, tank_target_c=50.0)
    state = EnergyState(voltage_v=4.8, estimated_joules=1.0, tank_t_c=40.0)
    assert (
        decide_gen03(
            state,
            cfg,
            storage_above_floor=True,
            pv_present=False,
            heat_pump_ok=False,
            peltier_ok=False,
            teg_delta_present=True,
        )
        == Gen03State.TEG_TRICKLE
    )


def test_named_host_scenarios_cover_refuse_and_run():
    rows = named_host_scenarios()
    by_id = {r["id"]: r["decision"] for r in rows}
    assert by_id["missing_tank_t"] == "REFUSE"
    assert by_id["tank_at_target"] == "REFUSE"
    assert by_id["heat_pump_below_target"] == "HEAT_PUMP_RUN"
    assert by_id["below_floor_with_pv"] == "CHARGE"
    assert by_id["teg_trickle_only"] == "TEG_TRICKLE"
    # JSON-serializable so the sandbox can write the log.
    json.dumps(rows)


if __name__ == "__main__":
    test_missing_tank_is_refuse()
    test_tank_at_target_is_refuse()
    test_heat_pump_when_below_target_and_surplus()
    test_below_floor_charges_when_pv()
    test_teg_trickle_does_not_start_heat()
    test_named_host_scenarios_cover_refuse_and_run()
    print("gen03 control stub tests passed.")
