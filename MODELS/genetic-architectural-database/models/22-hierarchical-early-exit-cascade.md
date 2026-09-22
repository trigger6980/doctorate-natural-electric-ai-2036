# 22 — Hierarchical Early-Exit Cascade

**Domain:** Multi-stage Inference  
**Energy Profile:** Low–Medium  
**Status:** Catalog + interface specification (no trained cascade, no measured stage joules, no inference certificate)  
**Operator role:** Optional host gate that refuses a later, more expensive stage when an earlier cheap stage already exits *accept* or *defer*. Not a certified classifier stack and not a trained weight file.

## Description
Some off-grid inference paths only need a staged refuse: *exit-accept*, *exit-reject*, *continue*, or *unknown*. A full hierarchical cascade (trained stage models, calibrated exit thresholds, on-device traces) is out of scope until labeled windows exist on the intended node.

This card specifies the host-facing interface. There is **no trained cascade, no public weight file, and no measured joule-per-stage** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A cascade exit is a *policy event*, not proof the world label is correct.
- Host evaluation of a fixture feature vector on a laptop is not a field inference certificate.
- Do not claim ImageNet, MLPerf, or “certified detection” status from this card.
- Distinct from Model 06: Model 06 is a *single* early-exit tiny classifier. This card is a *sequence of stages* with an explicit continue/exit policy.
- Distinct from Model 21: Model 21 is one quantized forest vote. This card is staged models that may include that vote as stage-0 only.
- Distinct from Model 10: Model 10 is an offline LLM runtime adapter. This card must refuse to call Model 10 unless a late stage is explicitly allowed.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `window_features` | input | Named placeholders. Uncalibrated |
| `cascade_id` | input | Ancestry id (`22` or `22-custom-<slug>`). Not a weight hash |
| `n_stages` | input | Design cap (e.g. 3). Deeper stacks are out of this card |
| `stage_k` | input | Current stage index in `[0, n_stages)` |
| `exit` | output | `exit-accept` / `exit-reject` / `continue` / `unknown` |
| `stage_used` | output | Last stage that produced a usable exit |
| `cascade_ok` | output | Boolean: an exit is usable for a downstream gate |
| `refuse_reason` | output | `energy` / `missing_features` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of stages actually walked |

Planned entry points:
- `cascade_step(energy_state, window_features, stage_k) -> exit`
- `cascade_ok(energy_state, window_features) -> bool`
- `gate_task(task_id, cascade_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture feature vector on the laptop CI runner; that is still not a trained cascade.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 20 `disagg_ok()` or Model 21 `rf_ok()` as cheap stage-0 — otherwise omit.
4. Model 22 `cascade_ok()` — refuse later stages (Models 09, 10, 24, 29) unless `continue` is allowed.
5. Only then `gate_task(allow)` for the expensive path.

Missing features must refuse with `missing_features`. An `unknown` exit must skip later stages unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of 3 shallow stages | 0.0005–0.008 J | Cheap compares, not cameras |
| Skip (`cascade_ok` false) | 0 J extra | Gate via Model 01 / 20 / 21 / 22 |
| Stage-2 on device | unknown | Do not schedule until measured |
| Trained cascade inference on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a later stage when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `exit-accept` as proof the *world label* is safe — only that the named features produced that stage exit.
- Do not invent accuracy scores or confusion-matrix numbers in host logs.

## Key Traits
- Hierarchical cascade is a refuse/allow gate, not a certified detector
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* cheap gates (20/21) and *before* expensive retrieval or LLM work
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_features` or `unknown` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, or `rf`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check trained weights into this public card.

## Next measurements (not done)
- Time and current for a 3-stage walk vs a Model 06 single early-exit on the intended MCU.
- Decide whether stage-0 reuses Model 20/21 outputs or takes raw features.
- Wire a skip reason through `policy_gated_executor` without claiming an inference certificate.
- Optional host stub: `cascade_ok()` on a fixture feature vector in CI — still not a trained cascade.
