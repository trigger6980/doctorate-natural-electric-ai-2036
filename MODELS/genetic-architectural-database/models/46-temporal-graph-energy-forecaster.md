# 46 — Temporal Graph Energy Forecaster

**Domain:** Time-series  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no trained temporal GNN, no snapshot store, no forecast certificate)  
**Operator role:** Optional host gate that refuses a temporal-graph forecast step when the named snapshot table is missing, a horizon row is `to-be-measured` without a hold, or the window class is unknown. Not a production T-GNN trainer and not a certified energy-forecast runtime.

## Description
A sparse GNN on one static snapshot (Model 45) cannot say whether the *next* harvest window will stay above the Model 01 floor. A cheap policy can decide whether the *next* temporal-graph step may roll a named snapshot table forward, shrink to a 1-window lookahead, or stay deferred so the rail can recover. A full trained temporal GNN + measured joules-per-roll is out of scope until named snapshot rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no trained weight file, no snapshot / edge-time store, no calibrated roll-to-joule library, and no measured joule-per-horizon** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A forecast decision is a *policy event*, not proof that a temporal roll occurred.
- Host evaluation of a fixture snapshot table on a laptop is not a forecast certificate.
- Do not claim T-GCN, EvolveGCN, STGCN production status, or “certified harvest forecast” from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named snapshot table* may consume that rail.
- Distinct from Model 02: Model 02 is a quantized LSTM irradiance forecaster. This card rolls *named graph snapshots*, not a univariate irradiance sequence.
- Distinct from Model 04: Model 04 estimates current energy state from PV + RF features. This card forecasts *future graph energy* from named windows.
- Distinct from Model 19: Model 19 estimates energy-neutral probability. This card forecasts *named horizon energy*, not a survival certificate.
- Distinct from Model 45: Model 45 is one static sparse pass. This card is *time-indexed snapshot rolls* on the same graph family.
- Distinct from Model 47: Model 47 (still a stub) is multi-agent orchestration. This card forecasts energy on a named temporal graph, not agent order.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `snapshot_table` | input | Named time-indexed graph rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_tgf` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `tgf_id` | input | Ancestry id (`46` or `46-custom-<slug>`). Not a silicon lot |
| `max_windows` | input | Design cap on named snapshot windows in one wake |
| `max_horizon` | input | Design cap on forecast steps in one wake |
| `gnn_ok` | input | Optional Model 45 result; a refused static graph should not roll time |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not schedule forecasts |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not write forecast tensors |
| `att_ok` | input | Optional Model 37 result; an unattested model should not roll snapshots |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `roll_horizon` |
| `tgf_action` | output | `hold` / `one_window` / `roll_horizon` / `defer` / `unknown` |
| `windows_checked` | output | Planned snapshot-row count after the action |
| `tgf_ok` | output | Boolean: the next scheduled temporal-graph forecast step may run under the named table |
| `refuse_reason` | output | `energy` / `missing_snapshots` / `unmeasured` / `no_hold` / `graph` / `plan` / `tool` / `attest` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured T-GNN energy) |

Planned entry points:
- `tgf_step(energy_state, snapshot_table, hold_tgf) -> tgf_action`
- `tgf_ok(energy_state, snapshot_table, hold_tgf) -> bool`
- `gate_task(task_id, tgf_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture snapshot table on the laptop CI runner; that is still not a trained temporal GNN.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 41 `tok_ok()` when the forecast is plan-driven — otherwise omit.
5. Model 42 `grd_ok()` when the forecast is tool-driven — otherwise omit.
6. Model 45 `gnn_ok()` when the static graph must be valid before time is rolled — otherwise omit.
7. Model 46 `tgf_ok()` — refuse unless every in-scope snapshot row is `agreed` or has a named hold.
8. Only then `gate_task(allow)` for the scheduled temporal-graph forecast step.

Missing snapshot-table fields must refuse with `missing_snapshots`. Rows marked `to-be-measured` without `hold_tgf` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `gnn_ok`, `tok_ok`, `grd_ok`, `att_ok`, or `energy_grant_ok` false must still refuse `roll_horizon`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU T-GNN layers |
| Skip (`tgf_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 41 / 42 / 45 / 46 |
| On-device one_window / roll_horizon | unknown | Do not schedule until measured |
| Full trained T-GNN + calibrated horizon-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `roll_horizon` or `one_window` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `tgf_ok` as proof that *a forecast roll occurred* — only that the named table is internally consistent with the hold policy.
- Do not invent MAE, horizon counts as certificates, or certified forecast joules in host logs.
- Do not treat this card as a T-GCN / EvolveGCN / STGCN trainer or harvest-forecast certificate.

## Key Traits
- Temporal graph energy forecast lite is a refuse/allow gate, not a trainer
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / token / tool / static-graph gates) and *before* any field duty change that depends on agreed snapshot rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_snapshots`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, `grd`, `aln`, `rsn`, or `gnn`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary temporal-graph weights or fake forecast marks into this public card.

## Next measurements (not done)
- Time and current for one_window vs roll_horizon vs hold on the intended MCU + rail.
- Decide whether snapshot tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a forecast certificate.
- Optional host stub: `tgf_ok()` on a fixture snapshot table in CI — still not a trained temporal GNN.
