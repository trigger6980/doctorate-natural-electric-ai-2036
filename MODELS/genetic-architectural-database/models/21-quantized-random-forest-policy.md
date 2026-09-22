# 21 — Quantized Random Forest Policy

**Domain:** Control  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no trained forest, no measured vote joules, no control certificate)  
**Operator role:** Optional host gate that refuses an expensive controller or radio hop when a small quantized forest already votes *hold* or *defer*. Not a certified plant controller and not a trained weight file.

## Description
Some off-grid control loops only need a coarse vote: *hold*, *nudge*, *defer*, or *unknown*. A full random-forest stack (trained ensemble, calibrated vote probabilities, plant-floor traces) is out of scope until labeled windows exist on the intended node.

This card specifies the host-facing interface. There is **no trained forest, no public weight file, and no measured joule-per-vote** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A forest vote is a *policy event*, not proof the plant state is correct.
- Host evaluation of a fixture feature vector on a laptop is not a field control certificate.
- Do not claim IEC, SIL, or “certified control” status from this card.
- Distinct from Model 03: Model 03 is an RL duty-cycle *controller interface*. This card is a quantized ensemble *vote* used as a gate.
- Distinct from Model 06: Model 06 is an early-exit tiny classifier. This card is an ensemble of shallow trees over named features.
- Distinct from Model 20: Model 20 is a *single* shallow tree for NILM-style window labels. This card is an ensemble policy for control votes.
- Distinct from Model 22: Model 22 is a later hierarchical early-exit cascade. This card is one forest, not a staged cascade.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `window_features` | input | Named placeholders reused from Model 20 where possible. Uncalibrated |
| `forest_id` | input | Ancestry id (`21` or `21-custom-<slug>`). Not a weight hash |
| `n_trees` | input | Design cap (e.g. 8). Larger ensembles are out of this card |
| `max_depth` | input | Per-tree cap (e.g. 4) |
| `vote` | output | `hold` / `nudge` / `defer` / `unknown` |
| `vote_share` | output | Host placeholder in [0, 1]. Not a calibrated probability |
| `rf_ok` | output | Boolean: vote is usable for a downstream gate |
| `refuse_reason` | output | `energy` / `missing_features` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of this vote (not the downstream actuator) |

Planned entry points:
- `vote_policy(energy_state, window_features) -> vote`
- `rf_ok(energy_state, window_features) -> bool`
- `gate_task(task_id, rf_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture feature vector on the laptop CI runner; that is still not a trained forest.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 20 `disagg_ok()` when a cheap load class is useful — otherwise omit.
4. Model 21 `rf_ok()` — ensemble vote before Models 03, 10, 18, or 28.
5. Only then `gate_task(allow)` for the expensive path.

Missing features must refuse with `missing_features`. An `unknown` vote must skip the expensive path unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host vote of 8 depth-4 trees | 0.0004–0.004 J | Cheap compares, not actuators |
| Skip (`rf_ok` false) | 0 J extra | Gate via Model 01 / 20 / 21 |
| Feature extract on device | unknown | Do not schedule until measured |
| Trained forest inference on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a downstream controller when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `vote` as proof the *actuator command* is safe — only that the named features produced that majority leaf.
- Do not invent plant set-points or confusion-matrix scores in host logs.

## Key Traits
- Quantized forest is a refuse/allow gate, not a certified controller
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* Model 20 when a load class exists, *before* expensive control or radio work
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_features` or `unknown` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, or `disagg`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check trained weights into this public card.

## Next measurements (not done)
- Time and current for an 8-tree vote vs a Model 20 single-tree walk on the intended MCU.
- Decide whether `window_features` stay buyer-supplied or are later filled by Models 13–15 observers.
- Wire a skip reason through `policy_gated_executor` without claiming a control certificate.
- Optional host stub: `rf_ok()` on a fixture feature vector in CI — still not a trained forest.
