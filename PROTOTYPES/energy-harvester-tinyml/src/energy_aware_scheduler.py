"""
Energy-aware scheduler skeleton for Natural Electric TinyML nodes.
Target: MicroPython on ESP32 or host-side simulation.
Treats supercapacitor / battery voltage as the primary energy-state signal.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from supercap_voltage_proxy import voltage_from_joules


class Action(Enum):
    SLEEP = auto()
    SENSE = auto()
    INFER = auto()
    TRANSMIT = auto()


@dataclass
class EnergyState:
    voltage_v: float          # measured or estimated
    estimated_joules: float   # optional model of remaining energy
    lux: Optional[float] = None


@dataclass
class PolicyConfig:
    v_min_safe: float = 3.3
    v_high: float = 4.5
    infer_cost_j: float = 0.009   # example 9 mJ for tiny NN
    tx_cost_j: float = 0.05
    sense_cost_j: float = 0.002


def simple_threshold_policy(state: EnergyState, cfg: PolicyConfig) -> Action:
    """Minimal energy-aware policy. Replace with quantized RL later."""
    if state.voltage_v < cfg.v_min_safe:
        return Action.SLEEP
    if state.voltage_v >= cfg.v_high and state.estimated_joules > cfg.tx_cost_j:
        return Action.TRANSMIT
    if state.estimated_joules > cfg.infer_cost_j:
        return Action.INFER
    if state.estimated_joules > cfg.sense_cost_j:
        return Action.SENSE
    return Action.SLEEP


def simulate_step(
    state: EnergyState,
    action: Action,
    cfg: PolicyConfig,
    C_farads: Optional[float] = None,
) -> EnergyState:
    """Host-side energy accounting for tests. Hardware will replace this.

    Default keeps the original linear voltage drop so existing tests stay
    comparable. Pass C_farads explicitly to map remaining joules through
    the Model 05 analytic capacitor equation. C is still uncalibrated.
    """
    cost = {
        Action.SLEEP: 0.0001,
        Action.SENSE: cfg.sense_cost_j,
        Action.INFER: cfg.infer_cost_j,
        Action.TRANSMIT: cfg.tx_cost_j,
    }[action]
    new_j = max(0.0, state.estimated_joules - cost)
    if C_farads is None:
        new_v = max(cfg.v_min_safe - 0.1, state.voltage_v - (cost * 0.1))
    else:
        new_v = voltage_from_joules(new_j, C_farads, v_min_useful=cfg.v_min_safe)
    return EnergyState(voltage_v=new_v, estimated_joules=new_j, lux=state.lux)


def run_simulation(steps: int = 100, initial_v: float = 4.2, initial_j: float = 1.0):
    cfg = PolicyConfig()
    state = EnergyState(voltage_v=initial_v, estimated_joules=initial_j, lux=500.0)
    log = []
    for i in range(steps):
        action = simple_threshold_policy(state, cfg)
        state = simulate_step(state, action, cfg)
        log.append((i, action.name, state.voltage_v, state.estimated_joules))
        # simulated harvest (indoor 500 lx example)
        state.estimated_joules += 0.0015
        state.voltage_v = min(5.0, state.voltage_v + 0.002)
    return log


if __name__ == "__main__":
    results = run_simulation()
    for row in results[::10]:
        print(row)
