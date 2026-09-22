# 20 — Tiny Decision Tree Disaggregator

**Domain:** NILM / Sensing  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no trained tree, no measured cycle joules, no appliance-label certificate)  
**Operator role:** Optional host gate that refuses a high-cost classifier or radio hop when a cheap tree already labels the current window as idle or out of scope. Not a certified NILM product and not a trained weight file.

## Description
Off-grid nodes sometimes only need a coarse answer: is this window likely *idle*, *single known load*, or *unknown / defer*. A full NILM stack (high-rate ADC, trained forest or CNN, appliance ground truth) is out of scope until current and voltage traces exist on the intended node.

This card specifies the host-facing interface. There is **no trained decision tree, no public weight file, and no measured joule-per-inference** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A tree label is a *policy event*, not proof an appliance is present.
- Host evaluation of a fixture feature vector on a laptop is not the same as a field NILM certificate.
- Do not claim IEC, NIST, or “certified disaggregation” status from this card.
- Distinct from Model 06: Model 06 is an early-exit tiny classifier for generic sensing. This card is a shallow tree over *named energy-window features*.
- Distinct from Model 07: Model 07 is a binary sensor gate. This card may emit more than two labels.
- Distinct from Model 19: Model 19 estimates chance the rail survives a burst. This card estimates what the *load class* of the current window is.
- Distinct from Model 21: Model 21 is the later quantized random-forest policy. This card is a single shallow tree, not an ensemble.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `window_features` | input | Named placeholders: mean, peak, duty, optional harmonic bin. Uncalibrated |
| `tree_id` | input | Ancestry id (`20` or `20-custom-<slug>`). Not a weight hash |
| `max_depth` | input | Design cap (e.g. 4). Deeper trees are out of this card |
| `label` | output | `idle` / `known_load` / `unknown` / `defer` |
| `confidence` | output | Host placeholder in [0, 1]. Not a calibrated probability |
| `disagg_ok` | output | Boolean: label is usable for a downstream gate |
| `refuse_reason` | output | `energy` / `missing_features` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of this tree walk (not the downstream task) |

Planned entry points:
- `disaggregate(energy_state, window_features) -> label`
- `disagg_ok(energy_state, window_features) -> bool`
- `gate_task(task_id, disagg_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture feature vector on the laptop CI runner; that is still not a trained NILM model.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 20 `disagg_ok()` — cheap label before Models 06, 09, 10, or 18.
4. Only then `gate_task(allow)` for the expensive path.

Missing features must refuse with `missing_features`. An `unknown` label must skip the expensive path unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of a depth-4 tree | 0.00005–0.0005 J | Cheap compares |
| Skip (`disagg_ok` false) | 0 J extra | Gate via Model 01 / 20 |
| Feature extract on device | unknown | Do not schedule until measured |
| Trained tree inference on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a downstream classifier when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `label` as proof the *appliance identity* is correct — only that the named features produced that leaf.
- Do not invent appliance watt ratings or confusion-matrix scores in host logs.

## Key Traits
- Shallow tree is a refuse/allow gate, not a certified NILM product
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *before* expensive inference or radio work (Models 06, 09, 10, 18)
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_features` or `unknown` as well as `energy`, `policy`, `integrity`, `config`, `route`, or `uncertain`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check trained weights into this public card.

## Next measurements (not done)
- Time and current for a depth-4 walk vs a Model 06 classifier on the intended MCU.
- Decide whether `window_features` stay buyer-supplied or are later filled by Models 13–15 observers.
- Wire a skip reason through `policy_gated_executor` without claiming a NILM certificate.
- Optional host stub: `disagg_ok()` on a fixture feature vector in CI — still not a trained tree.
