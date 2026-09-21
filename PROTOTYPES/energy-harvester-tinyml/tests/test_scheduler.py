"""Basic tests for the energy-aware scheduler. Run with: python -m pytest tests/"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from energy_aware_scheduler import (
    EnergyState,
    PolicyConfig,
    Action,
    simple_threshold_policy,
    run_simulation,
)


def test_sleep_when_low_voltage():
    cfg = PolicyConfig(v_min_safe=3.3)
    state = EnergyState(voltage_v=3.0, estimated_joules=0.1)
    assert simple_threshold_policy(state, cfg) == Action.SLEEP


def test_prefer_transmit_when_high_energy():
    cfg = PolicyConfig(v_high=4.5, tx_cost_j=0.05)
    state = EnergyState(voltage_v=4.8, estimated_joules=1.0)
    assert simple_threshold_policy(state, cfg) == Action.TRANSMIT


def test_simulation_runs_without_crash():
    log = run_simulation(steps=20)
    assert len(log) == 20
    assert all(isinstance(row[1], str) for row in log)


if __name__ == "__main__":
    test_sleep_when_low_voltage()
    test_prefer_transmit_when_high_energy()
    test_simulation_runs_without_crash()
    print("All basic tests passed.")
