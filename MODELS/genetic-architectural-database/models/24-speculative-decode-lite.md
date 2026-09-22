# 24 — Speculative Decode Lite

**Domain:** LLM Acceleration  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no draft model, no accepted-token certificate, no measured draft joules)  
**Operator role:** Optional host gate that refuses a speculative draft step when the rail cannot pay the draft-plus-verify pair, or when the named draft length is missing. Not a production spec-decode runtime and not a draft-model weight file.

## Description
Some off-grid LLM paths only need a staged refuse: *draft*, *verify*, *accept*, *reject*, or *unknown*. A full speculative-decode stack (draft model, tree attention, measured accept-rate joules) is out of scope until a named draft model and a verify budget exist on the intended node.

This card specifies the host-facing interface. There is **no draft weight file, no public accept-rate table, and no measured joule-per-draft** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A spec-decode decision is a *policy event*, not proof the generated tokens are correct.
- Host evaluation of a fixture draft length on a laptop is not a field accept-rate certificate.
- Do not claim Medusa, EAGLE, Lookahead, or “certified speculative decode” status from this card.
- Distinct from Model 10: Model 10 is the offline LLM runtime adapter. This card only gates *whether a draft-then-verify pair may run*.
- Distinct from Model 23: Model 23 gates KV growth. This card must still refuse a draft if `kv_ok` is false.
- Distinct from Model 22: Model 22 is a multi-stage classifier cascade. This card is draft/verify policy for decode, not label exit.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `draft_tokens` | input | Named placeholder count. Uncalibrated |
| `verify_tokens` | input | Named placeholder count. Uncalibrated |
| `spec_id` | input | Ancestry id (`24` or `24-custom-<slug>`). Not a draft-model hash |
| `max_draft` | input | Design cap. Longer drafts are out of this card |
| `spec_action` | output | `draft` / `verify` / `accept` / `reject` / `unknown` |
| `tokens_accepted` | output | Planned count after the action |
| `spec_ok` | output | Boolean: the next draft-plus-verify pair may run |
| `refuse_reason` | output | `energy` / `missing_budget` / `kv_full` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `spec_step(energy_state, draft_tokens, verify_tokens) -> spec_action`
- `spec_ok(energy_state, draft_tokens, verify_tokens) -> bool`
- `gate_task(task_id, spec_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture draft length on the laptop CI runner; that is still not a draft model.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 23 `kv_ok()` — refuse draft growth unless cache append is allowed.
4. Model 24 `spec_ok()` — refuse Model 10 draft-plus-verify unless `draft` then `verify` is allowed.
5. Only then `gate_task(allow)` for the speculative step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip the draft pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or NPU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of draft-or-reject | 0.001–0.02 J | Cheap compares, not NPU traces |
| Skip (`spec_ok` false) | 0 J extra | Gate via Model 01 / 19 / 23 / 24 |
| On-device draft + verify | unknown | Do not schedule until measured |
| Trained draft model on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a draft when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `accept` as proof the *generated text* is safe — only that the named counts fit the budget.
- Do not invent accept-rate or tokens-per-joule numbers in host logs.

## Key Traits
- Speculative decode is a refuse/allow gate, not a certified acceleration runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* Model 23 cache policy and *before* Model 10 draft growth
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget` or `kv_full` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, or `full`. Keep joule costs labeled uncalibrated until an MCU/NPU measurement exists. Do not check draft-model weights into this public card.

## Next measurements (not done)
- Time and current for draft vs verify vs reject on the intended runtime.
- Decide whether draft length is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an accept-rate certificate.
- Optional host stub: `spec_ok()` on a fixture draft length in CI — still not a draft model.
