# 41 — Token-Budget Aware Agent Planner

**Domain:** Agentic  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no planner runtime, no token meter, no planning certificate)  
**Operator role:** Optional host gate that refuses a plan expansion when the named token budget is missing, a budget row is `to-be-measured` without a hold, or the plan class is unknown. Not a production agent planner and not a certified token-accounting runtime.

## Description
Harvested-power agents can spend more joules on *thinking tokens* than on the physical step they were meant to take. A cheap policy can decide whether the *next* plan expansion may consume a named token budget, shrink to a cheaper outline, or stay deferred so the rail can recover. A full planner runtime + measured joules-per-token is out of scope until named budget rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no planner runtime, no tokenizer, no calibrated token-to-joule library, and no measured joule-per-token** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A planning decision is a *policy event*, not proof that an LLM generated a plan.
- Host evaluation of a fixture budget table on a laptop is not a planning certificate.
- Do not claim LangChain, AutoGPT, swarm-planner, or “AI-certified reasoning” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named plan expansion* may consume that rail.
- Distinct from Model 09 / 10: those are retrieval and offline-LLM *runtimes*. This card only gates whether a plan *budget* may grow.
- Distinct from Model 11: Model 11 allocates energy across agents. This card allocates *token slots inside one planner wake*.
- Distinct from Model 23 / 24: those bound KV cache and speculative decode. This card bounds *plan tokens before decode*.
- Distinct from Model 40: Model 40 decides whether a failed agent may *restart*. This card decides whether a live agent may *expand a plan*.
- Distinct from Model 47: Model 47 (still a stub) is multi-agent orchestration. This card is one planner’s token floor.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `token_budget_table` | input | Named remaining-token rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `tok_id` | input | Ancestry id (`41` or `41-custom-<slug>`). Not a silicon lot |
| `max_plan_tokens` | input | Design cap on named tokens in one wake window |
| `rst_ok` | input | Optional Model 40 result; a refused restart should not expand a plan |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `expand_plan` |
| `tok_action` | output | `hold` / `outline_cheap` / `expand_plan` / `defer` / `unknown` |
| `tokens_checked` | output | Planned token count after the action |
| `tok_ok` | output | Boolean: the next scheduled plan expansion may run under the named table |
| `refuse_reason` | output | `energy` / `missing_budget` / `unmeasured` / `no_hold` / `restart` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured planner energy) |

Planned entry points:
- `tok_step(energy_state, token_budget_table, hold_token) -> tok_action`
- `tok_ok(energy_state, token_budget_table, hold_token) -> bool`
- `gate_task(task_id, tok_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture budget table on the laptop CI runner; that is still not a planner runtime.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 40 `rst_ok()` when the planner itself just failed — otherwise omit.
4. Model 41 `tok_ok()` — refuse unless every in-scope budget row is `agreed` or has a named hold.
5. Only then `gate_task(allow)` for the scheduled plan expansion.

Missing budget-table fields must refuse with `missing_budget`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `rst_ok` or `energy_grant_ok` false must still refuse `expand_plan`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU planner traces |
| Skip (`tok_ok` false) | 0 J extra | Gate via Model 01 / 11 / 40 / 41 |
| On-device outline_cheap / expand_plan | unknown | Do not schedule until measured |
| Full planner + tokenizer + calibrated token-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `expand_plan` or `outline_cheap` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `tok_ok` as proof that *a physical planner ran* — only that the named budget table is internally consistent with the hold policy.
- Do not invent tokens-per-second, LLM cost, or certified planner joules in host logs.
- Do not treat this card as an agent framework, AutoGPT clone, or reasoning certificate.

## Key Traits
- Token-budget lite is a refuse/allow gate, not a planner runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker/restart gates) and *before* any field plan expansion that depends on agreed budget rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, or `rst`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary planner traces or fake reasoning marks into this public card.

## Next measurements (not done)
- Time and current for outline_cheap vs expand_plan vs hold on the intended MCU + rail.
- Decide whether token-budget tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a planning certificate.
- Optional host stub: `tok_ok()` on a fixture budget table in CI — still not a planner runtime.
