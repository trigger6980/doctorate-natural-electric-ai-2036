# 47 — Hierarchical Multi-Agent Orchestrator

**Domain:** Operator AI  
**Energy Profile:** Medium–High (uncalibrated)  
**Status:** Catalog + interface specification (no production orchestrator, no agent-runtime mesh, no orchestration certificate)  
**Operator role:** Optional host gate that refuses a hierarchical dispatch when the named role table is missing, a child-agent budget is `to-be-measured` without a hold, or the wake class is unknown. Not a production multi-agent runtime and not a certified Operator AI mesh.

## Description
A single task-graph walk (existing Operator AI host sketches) cannot decide which *named child agents* may wake under a shared rail. A cheap policy can decide whether the *next* hierarchical step may dispatch one child, fan-out a bounded cohort, or stay deferred so the rail can recover. A full agent mesh + measured joules-per-dispatch is out of scope until named role rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no production orchestrator, no agent-runtime mesh, no calibrated dispatch-to-joule library, and no measured joule-per-wake** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- An orchestrate decision is a *policy event*, not proof that child agents ran.
- Host evaluation of a fixture role table on a laptop is not an orchestration certificate.
- Do not claim AutoGen, CrewAI, LangGraph, Swarm, or “certified multi-agent mesh” from this card.
- Distinct from Model 11: Model 11 grants energy to one requester. This card orders *named child roles* after a grant exists.
- Distinct from Model 40: Model 40 is a self-heal / restart policy. This card dispatches *live hierarchy*, not crash recovery.
- Distinct from Model 41: Model 41 plans tokens for one agent. This card sequences *multiple named roles*.
- Distinct from Model 42: Model 42 guards a tool path. This card guards *who may call whom*.
- Distinct from Model 46: Model 46 forecasts energy on a named temporal graph. This card chooses *agent order*, not snapshot rolls.
- Distinct from Model 48: Model 48 allocates sovereign compute slots. This card orchestrates agents, not machine slots.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `role_table` | input | Named child-agent rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_hmo` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `hmo_id` | input | Ancestry id (`47` or `47-custom-<slug>`). Not a silicon lot |
| `max_children` | input | Design cap on named children in one wake |
| `max_depth` | input | Design cap on hierarchy depth in one wake |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `fan_out` |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not schedule children |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not emit child calls |
| `rst_ok` | input | Optional Model 40 result; an unhealthy host should not fan out |
| `att_ok` | input | Optional Model 37 result; an unattested model should not dispatch |
| `tgf_ok` | input | Optional Model 46 result; a refused forecast should not schedule a high-cost cohort |
| `hmo_action` | output | `hold` / `one_child` / `fan_out` / `defer` / `unknown` |
| `children_checked` | output | Planned role-row count after the action |
| `hmo_ok` | output | Boolean: the next scheduled hierarchical dispatch may run under the named table |
| `refuse_reason` | output | `energy` / `missing_roles` / `unmeasured` / `no_hold` / `grant` / `plan` / `tool` / `restart` / `attest` / `forecast` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured orchestrator energy) |

Planned entry points:
- `hmo_step(energy_state, role_table, hold_hmo) -> hmo_action`
- `hmo_ok(energy_state, role_table, hold_hmo) -> bool`
- `gate_task(task_id, hmo_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture role table on the laptop CI runner; that is still not a production orchestrator.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 40 `rst_ok()` when host health is in scope — otherwise omit.
5. Model 41 `tok_ok()` when the dispatch is plan-driven — otherwise omit.
6. Model 42 `grd_ok()` when the dispatch is tool-driven — otherwise omit.
7. Model 46 `tgf_ok()` when a forecast must precede a high-cost cohort — otherwise omit.
8. Model 47 `hmo_ok()` — refuse unless every in-scope role row is `agreed` or has a named hold.
9. Only then `gate_task(allow)` for the scheduled hierarchical dispatch.

Missing role-table fields must refuse with `missing_roles`. Rows marked `to-be-measured` without `hold_hmo` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `energy_grant_ok`, `tok_ok`, `grd_ok`, `rst_ok`, `att_ok`, or `tgf_ok` false must still refuse `fan_out`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU agent mesh |
| Skip (`hmo_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 40 / 41 / 42 / 46 / 47 |
| On-device one_child / fan_out | unknown | Do not schedule until measured |
| Full production orchestrator + calibrated wake-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `fan_out` or `one_child` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `hmo_ok` as proof that *child agents ran* — only that the named table is internally consistent with the hold policy.
- Do not invent latency SLAs, cohort counts as certificates, or certified dispatch joules in host logs.
- Do not treat this card as an AutoGen / CrewAI / LangGraph / Swarm runtime or multi-agent certificate.

## Key Traits
- Hierarchical multi-agent orchestration lite is a refuse/allow gate, not a runtime mesh
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / restart / token / tool / forecast gates) and *before* any field duty change that depends on agreed role rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_roles`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, `grd`, `aln`, `rsn`, `gnn`, or `tgf`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary orchestrator weights or fake dispatch marks into this public card.

## Next measurements (not done)
- Time and current for one_child vs fan_out vs hold on the intended MCU + rail.
- Decide whether role tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an orchestration certificate.
- Optional host stub: `hmo_ok()` on a fixture role table in CI — still not a production orchestrator.
