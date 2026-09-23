# 44 — Distilled Reasoning Trace Model

**Domain:** Reasoning  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no teacher model, no chain-of-thought store, no reasoning certificate)  
**Operator role:** Optional host gate that refuses a distilled-trace or self-check step when the named trace table is missing, a trace row is `to-be-measured` without a hold, or the decode class is unknown. Not a production teacher–student distiller and not a certified chain-of-thought runtime.

## Description
Harvested-power agents can spend more joules on a long reasoning trace than on the answer token that used it. A cheap policy can decide whether the *next* distilled-trace step may run against a named table, shrink to a short-answer decode, or stay deferred so the rail and the token budget can recover. A full teacher model + measured joules-per-trace is out of scope until named trace rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no teacher checkpoint, no student weights, no calibrated trace-to-joule library, and no measured joule-per-reasoning-step** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A trace decision is a *policy event*, not proof that multi-step reasoning occurred.
- Host evaluation of a fixture trace table on a laptop is not a chain-of-thought certificate.
- Do not claim teacher distillation, process-reward models, or “certified local reasoning” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named reasoning trace* may consume that rail.
- Distinct from Model 11: Model 11 allocates energy across agents. This card allocates *permission for one trace table inside one wake*.
- Distinct from Model 24: Model 24 is speculative decode lite. This card is *trace length / refuse*, not draft-token accept rate.
- Distinct from Model 41: Model 41 bounds *plan tokens*. This card bounds *reasoning tokens a plan may emit*.
- Distinct from Model 42: Model 42 gates *tool names*. This card gates *trace rows after tools and plans*.
- Distinct from Model 43: Model 43 gates *preference rows*. This card gates *reasoning traces after preferences*.
- Distinct from Model 45: Model 45 (still a stub) is a sparse edge GNN. This card is distilled traces.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `trace_table` | input | Named trace rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_rsn` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `rsn_id` | input | Ancestry id (`44` or `44-custom-<slug>`). Not a silicon lot |
| `max_trace_tokens` | input | Design cap on named reasoning tokens in one wake window |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not emit traces |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not write traces |
| `aln_ok` | input | Optional Model 43 result; a refused preference path should not write traces |
| `att_ok` | input | Optional Model 37 result; an unattested model should not write traces |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `write_trace` |
| `rsn_action` | output | `hold` / `short_answer` / `write_trace` / `defer` / `unknown` |
| `traces_checked` | output | Planned trace-row count after the action |
| `rsn_ok` | output | Boolean: the next scheduled reasoning-trace step may run under the named table |
| `refuse_reason` | output | `energy` / `missing_tracetable` / `unmeasured` / `no_hold` / `plan` / `tool` / `pref` / `attest` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured teacher energy) |

Planned entry points:
- `rsn_step(energy_state, trace_table, hold_rsn) -> rsn_action`
- `rsn_ok(energy_state, trace_table, hold_rsn) -> bool`
- `gate_task(task_id, rsn_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture trace table on the laptop CI runner; that is still not a teacher or student.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 41 `tok_ok()` when the trace is plan-driven — otherwise omit.
5. Model 42 `grd_ok()` when the trace is tool-driven — otherwise omit.
6. Model 43 `aln_ok()` when the trace would write preferences — otherwise omit.
7. Model 44 `rsn_ok()` — refuse unless every in-scope trace row is `agreed` or has a named hold.
8. Only then `gate_task(allow)` for the scheduled reasoning-trace step.

Missing trace-table fields must refuse with `missing_tracetable`. Rows marked `to-be-measured` without `hold_rsn` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `tok_ok`, `grd_ok`, `aln_ok`, `att_ok`, or `energy_grant_ok` false must still refuse `write_trace`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU teacher traces |
| Skip (`rsn_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 41 / 42 / 43 / 44 |
| On-device short_answer / write_trace | unknown | Do not schedule until measured |
| Full teacher + student + calibrated trace-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `write_trace` or `short_answer` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `rsn_ok` as proof that *multi-step reasoning occurred* — only that the named table is internally consistent with the hold policy.
- Do not invent accept-rates, process-reward scores, or certified reasoning joules in host logs.
- Do not treat this card as a teacher-student distiller, process-reward model, or chain-of-thought certificate.

## Key Traits
- Distilled reasoning lite is a refuse/allow gate, not a teacher
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / token / tool / preference gates) and *before* any field trace write that depends on agreed table rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_tracetable`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, `grd`, or `aln`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary teacher traces or fake reasoning marks into this public card.

## Next measurements (not done)
- Time and current for short_answer vs write_trace vs hold on the intended MCU + rail.
- Decide whether trace tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a reasoning certificate.
- Optional host stub: `rsn_ok()` on a fixture trace table in CI — still not a teacher.
