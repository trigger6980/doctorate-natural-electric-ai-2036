# 27 — Differential Privacy Noise Injector (Edge)

**Domain:** Privacy  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no noise sampler firmware, no privacy certificate, no measured noise joules)  
**Operator role:** Optional host gate that refuses a share-or-publish step when the rail cannot pay the sample-plus-add pair, or when the named privacy budget is missing. Not a production DP runtime and not an (ε,δ) certificate.

## Description
Some off-grid clusters only need a staged refuse: *hold*, *sample*, *add*, *release*, or *unknown*. A full DP stack (calibrated Gaussian/Laplace firmware, accountant, measured noise joules) is out of scope until a named mechanism and a privacy budget exist on the intended node.

This card specifies the host-facing interface. There is **no sampler binary, no public ε schedule, and no measured joule-per-sample** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A DP-injector decision is a *policy event*, not proof the released vector is private.
- Host evaluation of a fixture noise width on a laptop is not a field privacy certificate.
- Do not claim (ε,δ)-DP, RDP, zCDP, or “certified edge privacy” status from this card.
- Distinct from Model 26: Model 26 gates whether a *share* may be encoded or merged. This card gates whether *noise* may be added before a release.
- Distinct from Model 28 (catalog stub): physical control is a later card. This card must still refuse if the privacy budget is missing even when no actuator exists.
- Distinct from Model 16: Model 16 checks integrity of a named blob. This card does not hash firmware.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `vector_len` | input | Named placeholder length. Uncalibrated |
| `eps_budget` | input | Named placeholder ε. Uncalibrated; not a live accountant |
| `mech_id` | input | Ancestry id (`27` or `27-custom-<slug>`). Not a sampler hash |
| `max_vector_len` | input | Design cap. Larger vectors are out of this card |
| `dp_action` | output | `hold` / `sample` / `add` / `release` / `unknown` |
| `samples_added` | output | Planned count after the action |
| `dp_ok` | output | Boolean: the next sample-plus-add pair may run |
| `refuse_reason` | output | `energy` / `missing_budget` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `dp_step(energy_state, vector_len, eps_budget) -> dp_action`
- `dp_ok(energy_state, vector_len, eps_budget) -> bool`
- `gate_task(task_id, dp_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture vector length on the laptop CI runner; that is still not a DP accountant.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse release unless a host JSON path exists.
4. Model 26 `agg_ok()` when a share precedes the release — otherwise omit.
5. Model 27 `dp_ok()` — refuse sample/add unless the named sizes fit.
6. Only then `gate_task(allow)` for the inject step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip the sample-add pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or NPU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-sample | 0.001–0.05 J | Cheap compares, not RNG or NPU traces |
| Skip (`dp_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 26 / 27 |
| On-device sample + add | unknown | Do not schedule until measured |
| Certified (ε,δ) accountant | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a sample or add when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `release` as proof the *vector* is private or accurate — only that the named sizes fit the budget.
- Do not invent ε or joules-per-sample numbers in host logs.

## Key Traits
- Edge DP is a refuse/allow gate, not a certified privacy runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* aggregate/checkpoint gates and *before* any public write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, or `agg`. Keep joule costs labeled uncalibrated until an MCU/NPU measurement exists. Do not check sampler firmware or ε schedules into this public card.

## Next measurements (not done)
- Time and current for sample vs add vs hold on the intended runtime.
- Decide whether vector length is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a privacy certificate.
- Optional host stub: `dp_ok()` on a fixture vector length in CI — still not a DP accountant.
