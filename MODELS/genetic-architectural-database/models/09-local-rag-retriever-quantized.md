# 09 — Local RAG Retriever (Quantized)

**Domain:** Offline Knowledge  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no embedding weights or on-device index in this repository)  
**Operator role:** Optional INFER/RETRIEVE body on the off-grid AI box; Model 01 must grant a medium energy budget before a query runs

## Description
Quantized embedding + retrieval pipeline that is intended to run entirely on-device or on the off-grid AI box. After a knowledge base is loaded, retrieval-augmented generation should not require an external network call.

This card specifies the host-facing interface so Operator AI can budget energy per query. **No corpus, no quantized embedder, and no measured query joules exist here yet.** Simulator costs below are placeholders and are larger than TinyML SENSE/INFER on purpose.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `query_text` | input | Short operator or agent query |
| `k` | parameter | Number of chunks to return |
| `energy_budget_j` | input | From Model 05 / Model 01; skip if below embed cost |
| `index_id` | parameter | Which local index; must already be on disk |
| `hits` | output | List of `{chunk_id, score}` — empty on skip |
| `joules_used_est` | output | Sum of placeholder costs, not hardware |

Planned entry points:
- `retrieve(query_text, k, energy_budget_j) -> hits`
- `estimate_retrieve_cost_j(k) -> float` (table lookup until measured)

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended off-grid box before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Embed query (quantized) | 0.05 J | One forward of a tiny embedder |
| Scan / ANN lookup | 0.02 J × f(index size) | Local index only |
| Return k chunks | included above | No network |
| Skip retrieve | 0 J extra | Policy chose SLEEP or budget too low |

Safety rule: if `energy_budget_j` is below embed cost, do not run the embedder; return empty hits. Retrieval must never open a WAN socket.

## Key Traits
- Offline-first: the index is a deliverable, not a cloud call
- Medium energy: belongs on the off-grid AI box, not on the harvesting MCU of Models 01–08
- Fail-soft: missing weights or missing index means empty hits, not invented passages
- Pairs with Model 10 (runtime adapter) only after retrieve succeeds and budget remains

## Implementation Notes
No source file yet. When added, live under `PROTOTYPES/offgrid-ai-box/` and consume an explicit energy budget argument. Do not silently fall back to a hosted embedding API.

## Next measurements (not done)
- Choose a public tiny embedder and a public domain corpus; record index size on disk.
- Measure joules per query on the intended SBC (current × time × rail voltage).
- Record recall@k on that corpus; do not claim field retrieval quality until then.
