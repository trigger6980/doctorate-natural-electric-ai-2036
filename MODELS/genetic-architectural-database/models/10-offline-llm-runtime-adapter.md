# 10 — Offline LLM Runtime Adapter

**Domain:** Off-grid AI Box  
**Energy Profile:** Medium–High  
**Status:** Catalog + interface specification (no runtime binary, GGUF weights, or measured token joules in this repository)  
**Operator role:** Optional GENERATE body on the off-grid AI box; Model 01 must grant a medium–high budget; Model 09 retrieve should succeed first when RAG is in the graph

## Description
Thin adapter around an *already local* LLM runtime (llama.cpp, MLC-LLM, or equivalent) that exposes energy-state awareness: throttle context length, batch size, or decode frequency according to remaining joules, and refuse generation when the budget cannot cover a minimum prompt pass.

This card specifies the host-facing interface so Operator AI can budget energy per generation. **No weights, no compiled runtime, and no measured token joules exist here yet.** Simulator costs below are placeholders and are larger than Model 09 retrieve on purpose.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `prompt_text` | input | Operator or retrieved-context prompt |
| `max_new_tokens` | parameter | Hard cap; adapter may lower it |
| `energy_budget_j` | input | From Model 05 / Model 01; skip if below prefill cost |
| `runtime_id` | parameter | Which local runtime + weight file; must already be on disk |
| `completion_text` | output | Empty string on skip |
| `tokens_out` | output | 0 on skip |
| `joules_used_est` | output | Sum of placeholder costs, not hardware |
| `throttled` | output | True if context or tokens were reduced to fit budget |

Planned entry points:
- `generate(prompt_text, max_new_tokens, energy_budget_j) -> completion`
- `estimate_generate_cost_j(n_in, n_out) -> float` (table lookup until measured)
- `throttle_to_budget(n_in, n_out_wanted, energy_budget_j) -> (n_in_used, n_out_used)`

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended off-grid box before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Prefill / prompt pass | 0.40 J × f(n_in) | One local forward over the prompt |
| Decode token | 0.02 J × n_out | Local decode only |
| KV cache grow | included in decode | No cloud offload |
| Skip generate | 0 J extra | Policy chose SLEEP or budget too low |

Safety rules:
- If `energy_budget_j` is below prefill cost, do not start the runtime; return empty completion.
- Generation must never open a WAN socket to a hosted model API.
- Missing weight file or missing runtime binary is a hard fail-soft: empty completion, not a silent cloud fallback.

## Key Traits
- Offline-first: the weight file is a deliverable, not a URL
- Medium–high energy: belongs on the off-grid AI box, not on the harvesting MCU of Models 01–08
- Fail-soft: missing runtime means empty text, not invented answers
- Consumes Model 09 hits only when retrieve returned non-empty results *and* budget remains
- Throttle is first-class: shorter context is preferred over a brownout

## Implementation Notes
No source file yet. When added, live under `PROTOTYPES/offgrid-ai-box/` and consume an explicit energy budget argument. Do not vendor a hosted OpenAI-compatible endpoint as the default backend.

## Next measurements (not done)
- Choose one public small GGUF (or equivalent) and record on-disk size on the intended SBC.
- Measure joules per prefill and per decode token (current × time × rail voltage).
- Record tokens/s vs remaining supercap voltage; do not claim field latency until then.
