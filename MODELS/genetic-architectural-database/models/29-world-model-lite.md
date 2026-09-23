# 29 — World-Model Lite (Video Dynamics)

**Domain:** Spatial Intelligence  
**Energy Profile:** High  
**Status:** Catalog + interface specification (no video encoder, no dynamics certificate, no measured rollout joules)  
**Operator role:** Optional host gate that refuses a world-model rollout when the rail cannot pay the next encode-plus-step pair, or when the named frame budget is missing. Not a production video world model and not a spatial-intelligence certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *encode*, *roll*, *compare*, or *unknown*. A full world-model stack (video encoder, latent dynamics, measured rollout joules, listed spatial certificate) is out of scope until a named frame budget and plant bounds exist on the intended node.

This card specifies the host-facing interface. There is **no video encoder, no public latent file, and no measured joule-per-rollout** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A world-model decision is a *policy event*, not proof the plant was predicted safely.
- Host evaluation of a fixture frame count on a laptop is not a field dynamics certificate.
- Do not claim SOTA video world models, occupancy maps, or “certified spatial AI” status from this card.
- Distinct from Model 28: Model 28 gates whether a *physical command* may leave the host. This card gates whether a *rollout step* may consume frames.
- Distinct from Model 24: Model 24 is a speculative-decode draft gate. This card does not draft tokens.
- Distinct from Model 22: Model 22 is a staged classifier cascade. This card does not train stages.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `frame_budget` | input | Named placeholder frame count. Uncalibrated |
| `latent_bounds` | input | Named placeholder limits. Uncalibrated; not a live latent |
| `wm_id` | input | Ancestry id (`29` or `29-custom-<slug>`). Not a weight hash |
| `max_frames` | input | Design cap. Longer rollouts are out of this card |
| `wm_action` | output | `hold` / `encode` / `roll` / `compare` / `unknown` |
| `frames_issued` | output | Planned count after the action |
| `wm_ok` | output | Boolean: the next encode-plus-roll pair may run |
| `refuse_reason` | output | `energy` / `missing_budget` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `wm_step(energy_state, frame_budget, latent_bounds) -> wm_action`
- `wm_ok(energy_state, frame_budget, latent_bounds) -> bool`
- `gate_task(task_id, wm_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture frame budget on the laptop CI runner; that is still not a video encoder.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse roll unless a host JSON path exists.
4. Model 28 `phys_ok()` when a physical command follows the rollout — otherwise omit.
5. Model 29 `wm_ok()` — refuse encode/roll unless the named sizes fit.
6. Only then `gate_task(allow)` for the rollout step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip the encode-roll pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or accelerator before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-compare | 0.001–0.05 J | Cheap compares, not camera or GPU traces |
| Skip (`wm_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 28 / 29 |
| On-device encode + roll | unknown | Do not schedule until measured |
| Listed spatial-certificate path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an encode or roll when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `roll` as proof the *plant* was predicted or is safe — only that the named sizes fit the budget.
- Do not invent FPS, latent dim, or joules-per-frame numbers in host logs.

## Key Traits
- World-model lite is a refuse/allow gate, not a certified video runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any camera or GPU write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, or `phys`. Keep joule costs labeled uncalibrated until an MCU/accelerator measurement exists. Do not check video weights or latents into this public card.

## Next measurements (not done)
- Time and current for encode vs roll vs hold on the intended runtime.
- Decide whether frame budget is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a dynamics certificate.
- Optional host stub: `wm_ok()` on a fixture frame budget in CI — still not a video encoder.
