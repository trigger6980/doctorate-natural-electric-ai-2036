# 25 — On-Device Continual Learner (Constrained)

**Domain:** Adaptive Edge  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no on-device trainer, no plasticity certificate, no measured update joules)  
**Operator role:** Optional host gate that refuses a local weight update when the rail cannot pay the update-plus-verify pair, or when the named update budget is missing. Not a production continual-learning runtime and not a replay-buffer weight file.

## Description
Some off-grid nodes only need a staged refuse: *hold*, *update*, *verify*, *commit*, or *unknown*. A full continual-learning stack (replay buffer, EWC/LwF regularizer, measured update joules) is out of scope until a named trainer and an update budget exist on the intended node.

This card specifies the host-facing interface. There is **no trainer weight file, no public forgetting table, and no measured joule-per-update** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A continual-learn decision is a *policy event*, not proof the updated weights are better.
- Host evaluation of a fixture update size on a laptop is not a field plasticity certificate.
- Do not claim EWC, LwF, PackNet, or “certified on-device learning” status from this card.
- Distinct from Model 21: Model 21 is a frozen ensemble vote. This card only gates *whether a local update may run*.
- Distinct from Model 12: Model 12 checkpoints host JSON. This card must still refuse an update if the checkpoint path is missing.
- Distinct from Model 24: Model 24 gates draft-then-verify decode. This card gates learn-then-verify weight writes.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `update_bytes` | input | Named placeholder size. Uncalibrated |
| `verify_samples` | input | Named placeholder count. Uncalibrated |
| `learn_id` | input | Ancestry id (`25` or `25-custom-<slug>`). Not a trainer hash |
| `max_update_bytes` | input | Design cap. Larger updates are out of this card |
| `learn_action` | output | `hold` / `update` / `verify` / `commit` / `unknown` |
| `bytes_written` | output | Planned count after the action |
| `learn_ok` | output | Boolean: the next update-plus-verify pair may run |
| `refuse_reason` | output | `energy` / `missing_budget` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `learn_step(energy_state, update_bytes, verify_samples) -> learn_action`
- `learn_ok(energy_state, update_bytes, verify_samples) -> bool`
- `gate_task(task_id, learn_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture update size on the laptop CI runner; that is still not a trainer.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse commit unless a host JSON path exists.
4. Model 25 `learn_ok()` — refuse a local update unless `update` then `verify` is allowed.
5. Only then `gate_task(allow)` for the learn step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip the update pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or NPU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-update | 0.001–0.05 J | Cheap compares, not NPU traces |
| Skip (`learn_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 25 |
| On-device update + verify | unknown | Do not schedule until measured |
| Trained continual learner on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an update when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `commit` as proof the *new weights* are safe — only that the named sizes fit the budget.
- Do not invent forgetting-rate or joules-per-epoch numbers in host logs.

## Key Traits
- Continual learning is a refuse/allow gate, not a certified plasticity runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* Model 12 checkpoint presence and *before* any on-device write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, or `spec`. Keep joule costs labeled uncalibrated until an MCU/NPU measurement exists. Do not check trainer weights into this public card.

## Next measurements (not done)
- Time and current for update vs verify vs hold on the intended runtime.
- Decide whether update size is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a plasticity certificate.
- Optional host stub: `learn_ok()` on a fixture update size in CI — still not a trainer.
