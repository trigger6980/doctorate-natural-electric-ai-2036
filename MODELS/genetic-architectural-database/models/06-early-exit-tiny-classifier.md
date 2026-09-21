# 06 — Early-Exit Tiny Classifier

**Domain:** Edge Vision / Sensing  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no trained weights in this repository)  
**Operator role:** Optional INFER body with a cheap first exit; later exits only when Model 01 grants enough joules

## Description
Classification network with intermediate exit points. Easy examples terminate early, saving energy; hard examples continue to deeper layers. Particularly valuable when average-case energy matters more than worst-case latency.

This card specifies the host-facing interface so Operator AI can budget energy per exit. **No dataset, trained weights, or measured millijoule costs exist here yet.** Simulator costs below are placeholders inherited from Model 01's INFER budget.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `features` | input | Small feature vector (not raw high-res frames on first cut) |
| `max_exit` | parameter | Hard cap on depth for this invocation |
| `energy_budget_j` | input | From Model 05 / Model 01; stop before the next exit if remaining joules are insufficient |
| `confidence_threshold` | parameter | Exit early when the head is confident |
| `exit_id` | output | Which exit fired (0 = earliest) |
| `label` / `score` | output | Tentative class; later exits may revise |
| `joules_used_est` | output | Sum of placeholder exit costs, not hardware |

Planned entry points:
- `infer_with_exits(features, energy_budget_j, max_exit) -> result`
- `estimate_exit_cost_j(exit_id) -> float` (table lookup until measured)

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the target board before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Exit 0 (shallow head) | 0.002 J | Cheap gate; similar order to Model 01 SENSE |
| Exit 1 | 0.005 J | Mid-depth features |
| Exit 2 (full net) | 0.009 J | Same placeholder as Model 01 INFER |
| No-op / skip infer | 0 J extra | Policy chose SLEEP |

Safety rule: if `energy_budget_j` is below Exit 0 cost, do not run the network; return a skip to the scheduler.

## Key Traits
- Average-case energy can be far below worst-case if most samples exit early
- Compatible with Model 01 actions: early-exit is a refinement of INFER, not a new radio path
- Fail-soft: missing weights means the host must skip inference rather than invent labels
- Pairs with Model 07 as a still-cheaper binary gate in front of Exit 0

## Implementation Notes
No source file yet. When added, live next to `energy_aware_scheduler.py` and consume `EnergyState.estimated_joules`.

## Next measurements (not done)
- Train or distill a tiny multi-exit net on a public tiny-image or sensor dataset.
- Measure joules per exit on the intended MCU (current + time × rail voltage).
- Record exit-rate vs confidence threshold on that dataset; do not claim field accuracy until then.
