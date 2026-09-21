# 03 — RL Duty-Cycle Controller

**Domain:** Energy-aware Agents / Control  
**Energy Profile:** Low–Medium  
**Status:** Catalog + interface specification (no trained policy in-tree)  
**Operator role:** Drop-in replacement for Model 01 `simple_threshold_policy`

## Description
Reinforcement-learning policy (or distilled imitation of one) that selects sensing / inference / transmission / sleep actions to maximize long-term information value while keeping the energy store within safe bounds. Trained offline on simulated or measured harvest traces; deployed quantized.

Until a trained artifact exists, Model 01 remains the only executable policy. This card defines the contract a learned policy must satisfy so the Operator AI executor can swap it without changing task graphs.

## Interface (planned, same Action space as Model 01)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState.voltage_v` | input | Same struct as Model 01 |
| `EnergyState.estimated_joules` | input | Same struct as Model 01 |
| `EnergyState.lux` | optional input | Forecast from Model 02 may be written here |
| `forecast_lux[]` | optional input | Short-horizon hint from Model 02 |
| `Action` | output | Must be one of `SLEEP`, `SENSE`, `INFER`, `TRANSMIT` |

Required callable signature:

```text
learned_policy(state: EnergyState, cfg: PolicyConfig) -> Action
```

The policy-gated executor (`AGENTS/policy_gated_executor.py`) already accepts any callable with that shape. A future RL policy plugs in by passing `policy_fn=...`.

## Energy budget (example, not measured hardware)
Training cost is **offline and not part of the node budget**. On-node cost is the inference of the distilled policy.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Policy inference (tiny net / table) | 0.0005–0.002 J | Must stay cheaper than SENSE |
| Hard safety override | 0 J | If `voltage_v < v_min_safe`, force SLEEP even if the net says otherwise |

## Key Traits
- Explicitly optimizes for energy-neutral probability (training objective, not a field claim)
- Can incorporate uncertainty estimates from the irradiance forecaster
- Designed to replace or augment the simple threshold scheduler
- Must remain auditable: Action enum only, no hidden side effects

## Implementation Notes
No weights in-tree. Integration path is the `policy_fn` argument on `decide_and_run`.

## Next measurements (not done)
- Define a reward that penalizes brown-out and rewards useful SENSE/INFER/TX.
- Train offline against the host simulator in `energy_aware_scheduler.py`.
- Distill to a lookup table or int8 net and A/B against Model 01 on the same traces.
