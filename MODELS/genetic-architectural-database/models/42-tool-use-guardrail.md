# 42 — Tool-Use Guardrail Model

**Domain:** Safe Agents  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no tool runtime, no allow-list firmware, no safety certificate)  
**Operator role:** Optional host gate that refuses a tool call when the named allow-list is missing, a tool row is `to-be-measured` without a hold, or the tool class is unknown. Not a production tool executor and not a certified agent-safety runtime.

## Description
Harvested-power agents can spend more joules *and more blast radius* on a tool call than on the reasoning step that requested it. A cheap policy can decide whether the *next* tool invocation may run against a named allow-list, shrink to a read-only probe, or stay deferred so the rail and the safety boundary can recover. A full tool runtime + measured joules-per-call is out of scope until named allow-list rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no tool dispatcher, no sandbox hypervisor, no calibrated call-to-joule library, and no measured joule-per-tool-call** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A guardrail decision is a *policy event*, not proof that a tool executed.
- Host evaluation of a fixture allow-list on a laptop is not a safety certificate.
- Do not claim OpenAI function-calling, LangChain tools, MCP production runtime, or “certified tool-use safety” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named tool call* may consume that rail.
- Distinct from Model 11: Model 11 allocates energy across agents. This card allocates *permission for one tool name inside one wake*.
- Distinct from Model 16 / 17 / 37: those gate integrity, config, and attestation. This card gates *whether a tool name is allowed after those gates*.
- Distinct from Model 33: Model 33 checks an energy *contract*. This card checks a tool *allow-list*.
- Distinct from Model 41: Model 41 bounds *plan tokens*. This card bounds *tool invocations that a plan may request*.
- Distinct from Model 47: Model 47 (still a stub) is multi-agent orchestration. This card is one agent’s tool floor.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `tool_allow_table` | input | Named tool rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_tool` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `grd_id` | input | Ancestry id (`42` or `42-custom-<slug>`). Not a silicon lot |
| `max_tool_calls` | input | Design cap on named tool calls in one wake window |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not call tools |
| `att_ok` | input | Optional Model 37 result; an unattested model should not call tools |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `invoke_tool` |
| `grd_action` | output | `hold` / `probe_readonly` / `invoke_tool` / `defer` / `unknown` |
| `tools_checked` | output | Planned tool-call count after the action |
| `grd_ok` | output | Boolean: the next scheduled tool call may run under the named table |
| `refuse_reason` | output | `energy` / `missing_allowlist` / `unmeasured` / `no_hold` / `plan` / `attest` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured tool energy) |

Planned entry points:
- `grd_step(energy_state, tool_allow_table, hold_tool) -> grd_action`
- `grd_ok(energy_state, tool_allow_table, hold_tool) -> bool`
- `gate_task(task_id, grd_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture allow-list on the laptop CI runner; that is still not a tool runtime.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 41 `tok_ok()` when the call is plan-driven — otherwise omit.
5. Model 42 `grd_ok()` — refuse unless every in-scope tool row is `agreed` or has a named hold.
6. Only then `gate_task(allow)` for the scheduled tool invocation.

Missing allow-list fields must refuse with `missing_allowlist`. Rows marked `to-be-measured` without `hold_tool` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `tok_ok`, `att_ok`, or `energy_grant_ok` false must still refuse `invoke_tool`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU tool traces |
| Skip (`grd_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 41 / 42 |
| On-device probe_readonly / invoke_tool | unknown | Do not schedule until measured |
| Full tool dispatcher + sandbox + calibrated call-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `invoke_tool` or `probe_readonly` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `grd_ok` as proof that *a physical tool ran* — only that the named allow-list is internally consistent with the hold policy.
- Do not invent tools-per-second, API cost, or certified tool-call joules in host logs.
- Do not treat this card as an MCP production server, LangChain toolkit, or agent-safety certificate.

## Key Traits
- Tool-use guardrail lite is a refuse/allow gate, not a tool runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / token gates) and *before* any field tool call that depends on agreed allow-list rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_allowlist`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, or `tok`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary tool traces or fake safety marks into this public card.

## Next measurements (not done)
- Time and current for probe_readonly vs invoke_tool vs hold on the intended MCU + rail.
- Decide whether tool allow-lists are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a safety certificate.
- Optional host stub: `grd_ok()` on a fixture allow-list in CI — still not a tool runtime.
