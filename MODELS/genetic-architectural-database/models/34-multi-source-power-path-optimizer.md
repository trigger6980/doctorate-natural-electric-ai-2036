# 34 — Multi-Source Power Path Optimizer

**Domain:** Power Electronics + AI  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no MPPT firmware, no measured path joules, no power-path certificate)  
**Operator role:** Optional host gate that refuses a scheduled step when the named source mix is missing, inconsistent with the rail floor, or marked `to-be-measured` without a hold. Not a production power-path controller and not a converter-efficiency certificate.

## Description
Some off-grid nodes have more than one harvest or storage path (PV, thermoelectric, crank, supercap, small pack) and only need a staged refuse: *hold*, *prefer_primary*, *blend*, *defer*, or *unknown*. A full power-electronics stack (MPPT firmware, measured converter efficiency, listed path SIL) is out of scope until a named source table and measurement hold exist on the intended node.

This card specifies the host-facing interface. There is **no MPPT engine, no public efficiency suite, and no measured joule-per-switch** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A path decision is a *policy event*, not proof a physical converter delivered the planned mix on hardware.
- Host evaluation of a fixture source table on a laptop is not a power-path certificate.
- Do not claim certified converter efficiency, MPPT lock, or “AI-optimized multi-source plant” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses which *named sources* may feed that rail.
- Distinct from Model 04: Model 04 estimates PV-RF energy state. This card does not claim an RF or PV estimator.
- Distinct from Model 11: Model 11 allocates joules among agents. This card allocates among *power paths*, not tasks.
- Distinct from Model 33: Model 33 checks a named energy contract table. This card does not issue a verification certificate.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `source_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `ppo_id` | input | Ancestry id (`34` or `34-custom-<slug>`). Not a converter lot |
| `max_sources` | input | Design cap. Wider tables are out of this card |
| `ppo_action` | output | `hold` / `prefer_primary` / `blend` / `defer` / `unknown` |
| `sources_checked` | output | Planned row count after the action |
| `ppo_ok` | output | Boolean: the next scheduled step may run under the named mix |
| `refuse_reason` | output | `energy` / `missing_source` / `unmeasured` / `no_hold` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `ppo_step(energy_state, source_table, hold_token) -> ppo_action`
- `ppo_ok(energy_state, source_table, hold_token) -> bool`
- `gate_task(task_id, ppo_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture source table on the laptop CI runner; that is still not MPPT firmware.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse blend unless a host JSON path exists.
4. Model 33 `ctr_ok()` when a named energy contract is in scope — otherwise omit.
5. Model 34 `ppo_ok()` — refuse unless every in-scope source is `agreed` or has a named hold.
6. Only then `gate_task(allow)` for the scheduled step.

Missing source-table fields must refuse with `missing_source`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.001–0.05 J | Cheap table compares, not MPPT traces |
| Skip (`ppo_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 33 / 34 |
| On-device prefer_primary + blend | unknown | Do not schedule until measured |
| Listed converter / MPPT path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule blend when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `blend` as proof the *physical converters* delivered the planned mix — only that the named table is internally consistent with the hold policy.
- Do not invent MPPT lock times, converter efficiency, or certified path joules in host logs.

## Key Traits
- Power-path lite is a refuse/allow gate, not a certified converter runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* contract/checkpoint gates and *before* any field step that depends on agreed source rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_source`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, or `ctr`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check proprietary MPPT firmware or fake efficiency certificates into this public card.

## Next measurements (not done)
- Time and current for prefer_primary vs blend vs hold on the intended runtime.
- Decide whether source tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a power-path certificate.
- Optional host stub: `ppo_ok()` on a fixture source table in CI — still not MPPT firmware.
