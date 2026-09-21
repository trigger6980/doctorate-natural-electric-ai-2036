# 07 — Binary Neural Net Sensor Gate

**Domain:** Ultra-constrained Sensing  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no BNN weights in this repository)  
**Operator role:** Pre-SENSE / pre-INFER gate so Model 01 does not pay for a sensor or classifier when the binary gate says idle

## Description
Binary (or ternary) neural network used as a cheap gate that decides whether a more expensive sensor or model should be activated. Extreme quantization for microcontrollers with very limited RAM and flash.

This card specifies only the control interface. **No trained BNN, no XNOR-popcount kernel, and no measured gate energy exist in the tree.**

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `cheap_features` | input | Already-on sensors (voltage, lux, last ADC) — not a new high-cost modality |
| `threshold` | parameter | Score above which the expensive path is allowed |
| `energy_budget_j` | input | Must cover gate cost + the proposed next action |
| `allow_expensive` | output | Boolean: wake SENSE / Model 06 or stay idle |
| `score` | output | Uncalibrated binary-net score |

Planned entry points:
- `gate_should_wake(cheap_features, threshold) -> bool`
- `gate_cost_j() -> float` (placeholder until measured)

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Binary gate forward | 0.0004 J | Packed-bit MAC / popcount on MCU |
| Wake expensive SENSE | + Model 01 SENSE (0.002 J placeholder) | Only if gate allows |
| Wake Model 06 Exit 0 | + 0.002 J placeholder | Only if gate allows |

Safety rule: if voltage is below Model 01 `v_min_safe`, the gate is not consulted — SLEEP wins.

## Key Traits
- Extreme quantization for RAM/flash-limited parts
- Intended to sit *in front of* Model 06, not replace it
- Deterministic given weights; weights are not published yet
- Energy-first: a false-negative (stay idle) is preferred over a false-positive radio burst when joules are scarce

## Implementation Notes
Not implemented. A host stub may later wrap a lookup table so tests can exercise the scheduler without claiming a real BNN.

## Next measurements (not done)
- Choose a public binary-net baseline and a tiny feature set that does not require a camera.
- Measure gate latency and current on the target MCU.
- Report false-wake rate against a logged field trace; do not invent that rate.
