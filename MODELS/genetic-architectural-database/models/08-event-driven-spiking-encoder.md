# 08 — Event-Driven Spiking Encoder

**Domain:** Neuromorphic  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no spike kernel or measured event energy in this repository)  
**Operator role:** Optional SENSE front-end that emits sparse events so Model 01 / 07 only wake on activity, not on a fixed sample clock

## Description
Spiking or event-based encoder that converts a continuous sensor stream into sparse spike events. Computation is intended to occur on events rather than on a periodic ADC cadence, which matches intermittent and energy-harvesting regimes.

This card specifies only the host-facing interface. **No neuromorphic chip model, no trained SNN weights, and no measured picojoule-per-spike figures exist in the tree.**

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `sample` | input | Latest analog or cheap digital sample already paid for |
| `threshold` | parameter | Change magnitude that emits a spike |
| `refractory_s` | parameter | Minimum time between spikes from this channel |
| `energy_budget_j` | input | Must cover encode cost; encoder must not schedule radio |
| `spike` | output | Boolean or `{channel, t}` event |
| `events_this_window` | output | Count for the scheduler window |

Planned entry points:
- `encode_event(sample, threshold, refractory_s) -> Optional[Spike]`
- `encode_cost_j() -> float` (placeholder until measured)

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Threshold compare + no spike | 0.00005 J | Cheap residual check |
| Emit one spike event | 0.0002 J | Encode + buffer write |
| Hand off to Model 07 gate | + Model 07 gate cost | Only if a spike fired |

Safety rule: if voltage is below Model 01 `v_min_safe`, the encoder is not run — SLEEP wins. A silent window is a valid outcome.

## Key Traits
- Event sparsity is the energy strategy; dense streaming is out of scope for this card
- Intended to sit *in front of* Model 07, not replace the scheduler
- Deterministic given threshold and refractory; no learned weights required for the first stub
- Energy-first: dropping events under budget is preferred to inventing a wake

## Implementation Notes
Not implemented. A host stub may later wrap a simple delta-threshold so tests can emit synthetic spikes without claiming a neuromorphic runtime.

## Next measurements (not done)
- Log a real sensor trace and count events vs a fixed sample clock.
- Measure compare-and-buffer current on the target MCU.
- Do not publish a picojoule-per-spike number until that measurement exists.
