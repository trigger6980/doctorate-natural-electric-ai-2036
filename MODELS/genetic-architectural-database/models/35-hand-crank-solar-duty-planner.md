# 35 — Hand-Crank + Solar Duty Planner

**Domain:** Portable Off-grid  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no crank dynamo firmware, no measured crank joules, no portable-duty certificate)  
**Operator role:** Optional host gate that refuses a scheduled step when the named crank-or-solar mix is missing, inconsistent with the rail floor, or marked `to-be-measured` without a hold. Not a production portable-power planner and not a human-effort certificate.

## Description
Some portable nodes pair a small PV pane with a hand crank (or pedal dynamo) and only need a staged refuse: *hold*, *solar_only*, *crank_assist*, *defer*, or *unknown*. A full portable-power stack (crank firmware, measured human-watt input, listed duty SIL) is out of scope until a named duty table and measurement hold exist on the intended node.

This card specifies the host-facing interface. There is **no dynamo driver, no public human-watt suite, and no measured joule-per-crank-cycle** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A duty decision is a *policy event*, not proof a physical crank or pane delivered the planned mix on hardware.
- Host evaluation of a fixture duty table on a laptop is not a portable-duty certificate.
- Do not claim certified human-watt input, MPPT lock, or “AI-optimized crank-solar plant” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses which *named portable sources* may feed that rail.
- Distinct from Model 03: Model 03 is a general RL duty-cycle controller. This card is a named crank+solar mix only.
- Distinct from Model 15: Model 15 is indoor-lux adaptive scheduling. This card does not claim a lux-to-joule fit.
- Distinct from Model 34: Model 34 chooses among generic multi-source paths. This card is the portable crank+solar specialization, not a general MPPT optimizer.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `duty_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `hcd_id` | input | Ancestry id (`35` or `35-custom-<slug>`). Not a dynamo lot |
| `max_slots` | input | Design cap on named duty slots. Wider tables are out of this card |
| `hcd_action` | output | `hold` / `solar_only` / `crank_assist` / `defer` / `unknown` |
| `slots_checked` | output | Planned row count after the action |
| `hcd_ok` | output | Boolean: the next scheduled step may run under the named mix |
| `refuse_reason` | output | `energy` / `missing_duty` / `unmeasured` / `no_hold` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `hcd_step(energy_state, duty_table, hold_token) -> hcd_action`
- `hcd_ok(energy_state, duty_table, hold_token) -> bool`
- `gate_task(task_id, hcd_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture duty table on the laptop CI runner; that is still not crank firmware.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse crank_assist unless a host JSON path exists.
4. Model 34 `ppo_ok()` when a generic multi-source table is also in scope — otherwise omit.
5. Model 35 `hcd_ok()` — refuse unless every in-scope duty slot is `agreed` or has a named hold.
6. Only then `gate_task(allow)` for the scheduled step.

Missing duty-table fields must refuse with `missing_duty`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.001–0.05 J | Cheap table compares, not crank traces |
| Skip (`hcd_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 34 / 35 |
| On-device solar_only + crank_assist | unknown | Do not schedule until measured |
| Listed dynamo / pane path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule crank_assist when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `crank_assist` as proof a *human* delivered watts — only that the named table is internally consistent with the hold policy.
- Do not invent human-watt ratings, crank cadence, or certified portable joules in host logs.
- Do not treat this card as an occupational-safety or medical-effort rating.

## Key Traits
- Portable duty lite is a refuse/allow gate, not a certified dynamo runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* generic power-path / contract / checkpoint gates and *before* any field step that depends on agreed crank+solar rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_duty`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, or `ppo`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not check proprietary dynamo firmware or fake human-watt certificates into this public card.

## Next measurements (not done)
- Time and current for solar_only vs crank_assist vs hold on the intended runtime.
- Decide whether duty tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a portable-duty certificate.
- Optional host stub: `hcd_ok()` on a fixture duty table in CI — still not crank firmware.
