# 33 — Formal Energy Contract Checker

**Domain:** Verification  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no proof checker, no measured contract joules, no verification certificate)  
**Operator role:** Optional host gate that refuses a scheduled step when the named energy contract is missing, inconsistent with the rail floor, or marked `to-be-measured` without a hold. Not a production model checker and not a plant-safety certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *check_bounds*, *accept_contract*, *defer*, or *unknown*. A full formal stack (SMT or temporal checker over joule traces, certified energy invariant, listed plant SIL) is out of scope until a named contract table and measurement hold exist on the intended node.

This card specifies the host-facing interface. There is **no proof engine, no public invariant suite, and no measured joule-per-check** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A contract decision is a *policy event*, not proof a physical rail obeyed an invariant on hardware.
- Host evaluation of a fixture contract table on a laptop is not a verification certificate.
- Do not claim certified energy contracts, IEC/ISO functional-safety ratings, or “formally verified AI plant” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card checks whether a *named contract table* is consistent with that floor.
- Distinct from Model 19: Model 19 estimates energy-neutral probability. This card does not claim a survival curve.
- Distinct from Model 17: Model 17 validates air-gap config shape. This card does not compile schemas.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `contract_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `ctr_id` | input | Ancestry id (`33` or `33-custom-<slug>`). Not a SIL lot |
| `max_rows` | input | Design cap. Wider tables are out of this card |
| `ctr_action` | output | `hold` / `check_bounds` / `accept_contract` / `defer` / `unknown` |
| `rows_checked` | output | Planned row count after the action |
| `ctr_ok` | output | Boolean: the next scheduled step may run under the named table |
| `refuse_reason` | output | `energy` / `missing_contract` / `unmeasured` / `no_hold` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `ctr_step(energy_state, contract_table, hold_token) -> ctr_action`
- `ctr_ok(energy_state, contract_table, hold_token) -> bool`
- `gate_task(task_id, ctr_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture contract table on the laptop CI runner; that is still not a proof checker.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse accept_contract unless a host JSON path exists.
4. Model 33 `ctr_ok()` — refuse unless every in-scope row is `agreed` or has a named hold.
5. Only then `gate_task(allow)` for the scheduled step.

Missing contract-table fields must refuse with `missing_contract`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.001–0.05 J | Cheap table compares, not SMT traces |
| Skip (`ctr_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 33 |
| On-device check_bounds + accept | unknown | Do not schedule until measured |
| Listed formal proof path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule accept_contract when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `accept_contract` as proof the *physical rail* satisfied an invariant — only that the named table is internally consistent with the hold policy.
- Do not invent SIL levels, SMT solver times, or certified joule invariants in host logs.

## Key Traits
- Formal-contract lite is a refuse/allow gate, not a certified verification runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any field step that depends on agreed energy rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_contract`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, or `coh`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check proprietary proof scripts or fake SIL certificates into this public card.

## Next measurements (not done)
- Time and current for check_bounds vs accept_contract vs hold on the intended runtime.
- Decide whether contract tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a verification certificate.
- Optional host stub: `ctr_ok()` on a fixture contract table in CI — still not a proof checker.
