# 19 — Energy-Neutral Probability Estimator

**Domain:** Formal / Probabilistic  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no measured survival curves, no certified energy-neutral proof)  
**Operator role:** Optional host gate that refuses a scheduled burst when the estimated probability of remaining above `v_min_safe` through the burst is below a named threshold. Not a formal verification product and not a measured harvest model.

## Description
Harvested-power nodes need a cheap answer to “will this next burst leave the rail below the Model 01 floor?” A full energy-neutral proof (measured harvest process, certified discharge curve, PAC-Bayes or martingale bound on remaining energy) is out of scope until harvest and load joules are measured on the intended node.

This card specifies the host-facing interface. There is **no fitted harvest process, no certified survival curve, and no measured energy-neutral proof** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A low probability is a *policy event*, not proof the harvest source failed.
- Host simulation of a Bernoulli or piecewise-constant harvest rate on a laptop is not the same as a field energy-neutral certificate.
- Do not claim IEC, IEEE, or “energy-neutral certified” status from this card.
- Distinct from Model 01: Model 01 answers “is voltage now above a threshold?” This card answers “is the *estimated chance* of staying above that threshold through a named burst acceptable?”
- Distinct from Model 05: Model 05 maps voltage ↔ joules when C is supplied. This card consumes that map as an input; it does not invent C.
- Distinct from Model 11: Model 11 partitions a *known* local pool. This card estimates whether the pool will still exist after a burst under an *uncertain* harvest increment.
- Distinct from Model 33: Model 33 is the later formal-contract checker. This card is a cheap numeric estimate, not a proof checker.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `burst_joules_est` | input | Placeholder cost of the candidate task; labeled uncalibrated |
| `harvest_joules_est` | input | Optional expected harvest during the burst window; 0 if unknown |
| `harvest_var` | input | Optional variance placeholder; host may omit |
| `p_min_survive` | input | Named threshold (e.g. 0.8). Not a certified reliability target |
| `p_survive` | output | Estimated P(energy after burst ≥ Model 01 floor). Host formula only |
| `neutral_ok` | output | Boolean: `p_survive >= p_min_survive` |
| `refuse_reason` | output | `energy` / `uncertain` / `missing_C` / `ok` |
| `joules_used_est` | output | Placeholder cost of this estimate itself (not the burst) |

Planned entry points:
- `p_survive(energy_state, burst_joules_est, harvest_joules_est=0) -> float`
- `neutral_ok(energy_state, burst_joules_est, p_min_survive) -> bool`
- `gate_task(task_id, neutral_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may evaluate a fixture `(V, C, burst)` triple on the laptop CI runner; that is still not a field certificate.

Typical composition:
1. Model 05 `joules_from_voltage` when `C_farads` is explicit — otherwise refuse with `missing_C`.
2. Model 01 floor `v_min_safe` converted the same way.
3. Model 19 `neutral_ok()` — estimated remainder after burst + optional harvest.
4. Only then `gate_task(allow)` for the burst.

A charged rail with missing C must still refuse. A high `p_survive` with Model 01 already in SLEEP must still refuse.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host estimate from V, C, burst | 0.0002–0.002 J | Cheap arithmetic |
| Skip (`neutral_ok` false) | 0 J extra | Gate via Model 01 / 19 |
| Actual burst on device | unknown | Do not schedule until measured |
| Harvest increment during burst | unknown | Do not treat host `harvest_joules_est` as measured |

Safety rules:
- Never schedule a burst when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `neutral_ok` as proof the *task output* is good — only that the estimated remainder is acceptable under the named inputs.
- Do not invent Weibull, battery-cycle, or MTBF numbers in host logs.

## Key Traits
- Survival chance is a refuse/allow gate, not a certification product
- Reuses Model 01 floor and Model 05 joule map so C stays explicit
- Intended to run *before* expensive inference or radio work (Models 09, 10, 18)
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `uncertain` or `missing_C` as well as `energy`, `policy`, `integrity`, `config`, or `route`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not fit harvest curves from live telemetry in this card.

## Next measurements (not done)
- Time and current for the host arithmetic vs a real burst on the intended MCU.
- Decide whether `harvest_joules_est` stays buyer-supplied or is later filled by Models 13–15 observers.
- Wire a skip reason through `policy_gated_executor` without claiming a formal energy-neutral proof.
- Optional host stub: `neutral_ok()` on a fixture `(V, C, burst)` in CI — still not a field certificate.
