# 01 — Threshold Energy Scheduler

**Domain:** Natural Electric / Power Management  
**Energy Profile:** Ultra-low  
**Status:** Skeleton code present in `PROTOTYPES/energy-harvester-tinyml/`  
**Operator role:** Policy / Scheduler plug-in for Operator AI Machinery

## Description
Simple but effective policy that maps observed supercapacitor / battery voltage (and optional estimated joules) to discrete actions: SLEEP, SENSE, INFER, TRANSMIT. Thresholds are configurable. Serves as the baseline energy-aware controller for all higher models.

## Interface (current skeleton)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState.voltage_v` | input | Measured or estimated rail voltage |
| `EnergyState.estimated_joules` | input | Host-side remaining-energy estimate |
| `EnergyState.lux` | optional input | Harvest proxy; not yet used by the threshold policy |
| `PolicyConfig.v_min_safe` | parameter | Default 3.3 V — below this, SLEEP |
| `PolicyConfig.v_high` | parameter | Default 4.5 V — high-energy transmit window |
| `PolicyConfig.infer_cost_j` | parameter | Default 0.009 J |
| `PolicyConfig.tx_cost_j` | parameter | Default 0.05 J |
| `PolicyConfig.sense_cost_j` | parameter | Default 0.002 J |
| `Action` | output | `SLEEP`, `SENSE`, `INFER`, `TRANSMIT` |

Python entry points:
- `simple_threshold_policy(state, cfg) -> Action`
- `simulate_step(state, action, cfg) -> EnergyState`
- `run_simulation(steps, initial_v, initial_j) -> list`

## Energy budget (example, not measured hardware)
These numbers are **placeholders used by the host simulator**. They must be replaced with bench measurements on the target board before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| SLEEP | 0.0001 J / step | Leakage + RTC wake |
| SENSE | 0.002 J | ADC / sensor sample |
| INFER | 0.009 J | Tiny quantized forward pass |
| TRANSMIT | 0.050 J | Short radio burst |
| Indoor harvest (sim) | +0.0015 J / step | 500 lx indoor PV example |

Safety rule in the current policy: if `voltage_v < v_min_safe`, always SLEEP regardless of estimated joules.

## Key Traits
- Deterministic and fully auditable
- Extremely low compute cost
- Directly couples physical energy state to software behavior
- Easy to replace with learned policies (RL, decision tree, etc.) later
- Compatible with the Operator AI task-graph energy gate (`min_joules`)

## Implementation Notes
See `PROTOTYPES/energy-harvester-tinyml/src/energy_aware_scheduler.py` and accompanying tests.

## Next measurements (not done)
- Capture real ESP32 + supercap discharge curves.
- Replace the linear `cost * 0.1` voltage model with `E = 0.5 * C * V^2`.
- Log policy decisions against harvested lux on hardware.
