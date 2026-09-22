# 23 — Memory-Efficient KV Cache Adapter

**Domain:** LLM Edge  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no packed KV layout, no measured cache joules, no context-window certificate)  
**Operator role:** Optional host gate that refuses a later decode step when the named cache budget is already full or the rail cannot pay the next append. Not a production LLM runtime and not a packed weight file.

## Description
Some off-grid LLM paths only need a staged refuse: *append*, *evict*, *refuse*, or *unknown*. A full memory-efficient KV adapter (paged layouts, quantized keys/values, measured DRAM/SRAM joules) is out of scope until a local runtime and a named context budget exist on the intended node.

This card specifies the host-facing interface. There is **no packed KV layout, no public cache dump, and no measured joule-per-append** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A cache decision is a *policy event*, not proof the generated tokens are correct.
- Host evaluation of a fixture token count on a laptop is not a field context-window certificate.
- Do not claim Hugging Face, vLLM, llama.cpp, or “certified long-context” status from this card.
- Distinct from Model 10: Model 10 is the offline LLM runtime adapter. This card only gates *how much cache* that runtime may grow.
- Distinct from Model 22: Model 22 is a multi-stage classifier cascade. This card is cache-budget policy for decode, not label exit.
- Distinct from Model 09: Model 09 retrieves local chunks. This card must refuse to keep retrieved tokens in KV unless `append` is allowed.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `tokens_in_cache` | input | Named placeholder count. Uncalibrated |
| `tokens_to_append` | input | Named placeholder count. Uncalibrated |
| `cache_id` | input | Ancestry id (`23` or `23-custom-<slug>`). Not a layout hash |
| `max_tokens` | input | Design cap. Larger windows are out of this card |
| `kv_action` | output | `append` / `evict` / `refuse` / `unknown` |
| `tokens_after` | output | Planned count after the action |
| `kv_ok` | output | Boolean: the next decode step may grow or reuse cache |
| `refuse_reason` | output | `energy` / `full` / `missing_budget` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `kv_step(energy_state, tokens_in_cache, tokens_to_append) -> kv_action`
- `kv_ok(energy_state, tokens_in_cache, tokens_to_append) -> bool`
- `gate_task(task_id, kv_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture token count on the laptop CI runner; that is still not a packed KV layout.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 22 `cascade_ok()` if a cheap classifier must pass before LLM work — otherwise omit.
4. Model 23 `kv_ok()` — refuse Model 10 decode growth unless `append` or planned `evict` is allowed.
5. Only then `gate_task(allow)` for the decode step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip decode growth unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or NPU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of append-or-evict | 0.001–0.02 J | Cheap compares, not DRAM traces |
| Skip (`kv_ok` false) | 0 J extra | Gate via Model 01 / 19 / 22 / 23 |
| On-device KV append | unknown | Do not schedule until measured |
| Packed / quantized KV on device | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an append when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `append` as proof the *generated text* is safe — only that the named counts fit the budget.
- Do not invent tokens-per-joule or perplexity numbers in host logs.

## Key Traits
- KV adapter is a refuse/allow gate, not a certified long-context runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* cheap gates (19/22) and *before* Model 10 decode growth
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `full` or `missing_budget` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, or `cascade`. Keep joule costs labeled uncalibrated until an MCU/NPU measurement exists. Do not check packed KV dumps into this public card.

## Next measurements (not done)
- Time and current for append vs evict vs refuse on the intended runtime.
- Decide whether eviction is FIFO, score-based, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a context-window certificate.
- Optional host stub: `kv_ok()` on a fixture token count in CI — still not a packed KV layout.
