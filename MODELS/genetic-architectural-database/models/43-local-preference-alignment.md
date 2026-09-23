# 43 — Local Preference Alignment (Tiny)

**Domain:** Alignment  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no preference trainer, no reward model, no alignment certificate)  
**Operator role:** Optional host gate that refuses a preference-update or ranked-choice step when the named preference table is missing, a preference row is `to-be-measured` without a hold, or the update class is unknown. Not a production RLHF / DPO trainer and not a certified alignment runtime.

## Description
Harvested-power agents can spend more joules *and more irreversible policy drift* on a preference update than on the inference step that requested it. A cheap policy can decide whether the *next* local preference step may run against a named table, shrink to a read-only rank, or stay deferred so the rail and the alignment boundary can recover. A full preference trainer + measured joules-per-update is out of scope until named preference rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no preference trainer, no reward-model weights, no calibrated update-to-joule library, and no measured joule-per-preference-step** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A preference decision is a *policy event*, not proof that a human preference was learned.
- Host evaluation of a fixture preference table on a laptop is not an alignment certificate.
- Do not claim RLHF, DPO, constitutional AI, or “certified local alignment” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named preference update* may consume that rail.
- Distinct from Model 11: Model 11 allocates energy across agents. This card allocates *permission for one preference table inside one wake*.
- Distinct from Model 25: Model 25 is constrained continual learning. This card is *preference ranking / refuse*, not generic plasticity.
- Distinct from Model 41: Model 41 bounds *plan tokens*. This card bounds *preference updates a plan may request*.
- Distinct from Model 42: Model 42 gates *tool names*. This card gates *preference rows after tools and plans*.
- Distinct from Model 44: Model 44 (still a stub) is distilled reasoning traces. This card is local preference ranking.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `pref_table` | input | Named preference rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_pref` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `aln_id` | input | Ancestry id (`43` or `43-custom-<slug>`). Not a silicon lot |
| `max_pref_updates` | input | Design cap on named preference updates in one wake window |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not update preferences |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not write preferences |
| `att_ok` | input | Optional Model 37 result; an unattested model should not write preferences |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `write_pref` |
| `aln_action` | output | `hold` / `rank_readonly` / `write_pref` / `defer` / `unknown` |
| `prefs_checked` | output | Planned preference-row count after the action |
| `aln_ok` | output | Boolean: the next scheduled preference step may run under the named table |
| `refuse_reason` | output | `energy` / `missing_preftable` / `unmeasured` / `no_hold` / `plan` / `tool` / `attest` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured trainer energy) |

Planned entry points:
- `aln_step(energy_state, pref_table, hold_pref) -> aln_action`
- `aln_ok(energy_state, pref_table, hold_pref) -> bool`
- `gate_task(task_id, aln_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture preference table on the laptop CI runner; that is still not a trainer.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 41 `tok_ok()` when the update is plan-driven — otherwise omit.
5. Model 42 `grd_ok()` when the update is tool-driven — otherwise omit.
6. Model 43 `aln_ok()` — refuse unless every in-scope preference row is `agreed` or has a named hold.
7. Only then `gate_task(allow)` for the scheduled preference step.

Missing preference-table fields must refuse with `missing_preftable`. Rows marked `to-be-measured` without `hold_pref` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `tok_ok`, `grd_ok`, `att_ok`, or `energy_grant_ok` false must still refuse `write_pref`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU trainer traces |
| Skip (`aln_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 41 / 42 / 43 |
| On-device rank_readonly / write_pref | unknown | Do not schedule until measured |
| Full preference trainer + reward model + calibrated update-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `write_pref` or `rank_readonly` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `aln_ok` as proof that *a human preference was learned* — only that the named table is internally consistent with the hold policy.
- Do not invent win-rates, reward scores, or certified alignment joules in host logs.
- Do not treat this card as an RLHF stack, DPO trainer, or alignment certificate.

## Key Traits
- Local preference alignment lite is a refuse/allow gate, not a trainer
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / token / tool gates) and *before* any field preference write that depends on agreed table rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_preftable`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, or `grd`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary preference traces or fake alignment marks into this public card.

## Next measurements (not done)
- Time and current for rank_readonly vs write_pref vs hold on the intended MCU + rail.
- Decide whether preference tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an alignment certificate.
- Optional host stub: `aln_ok()` on a fixture preference table in CI — still not a trainer.
