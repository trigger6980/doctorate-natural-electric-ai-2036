# 11 — Multi-Agent Energy Broker

**Domain:** Agentic Mesh  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (host allocator stub exists; no radio mesh and no measured allocation joules)  
**Operator role:** Sits above Model 01. Several Operator AI task graphs may request joules in the same tick; the broker decides who receives a budget and who must SLEEP.

## Description
A deterministic allocator that treats remaining energy as a scarce shared resource among local agents. It does **not** discover peers on a network and does **not** move joules between physical nodes. It only partitions a single reported budget so concurrent tasks cannot each assume they own the whole capacitor.

This card specifies the host-facing interface so Operator AI can request, grant, and refuse energy. **No mesh protocol, no consensus layer, and no measured allocation joules exist here yet.** Simulator costs below are placeholders and are smaller than Model 09 retrieve on purpose — brokering should be cheap relative to inference.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `pool_j` | input | Remaining joules from Model 05 / Model 01 |
| `requests` | input | List of `{agent_id, want_j, priority}` |
| `reserve_j` | parameter | Floor left unallocated so the node can SLEEP |
| `grants` | output | List of `{agent_id, granted_j}` — 0 means refused |
| `pool_remaining_j` | output | `pool_j` minus sum(grants) minus unused reserve |
| `joules_used_est` | output | Broker overhead only (placeholder) |

Planned entry points:
- `allocate(pool_j, requests, reserve_j) -> grants`
- `estimate_broker_cost_j(n_requests) -> float` (table lookup until measured)

Host stub: `AGENTS/energy_broker.py` implements `allocate` only. It does not talk to hardware.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended node before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Rank + grant N requests | 0.0002 J × N | Host or MCU sort/scan |
| Refuse all (pool below reserve) | 0 J extra | Policy chose SLEEP |
| Radio mesh gossip | not modeled | Out of scope for this card |

Safety rules:
- Never grant more than `max(0, pool_j - reserve_j)` in total.
- Never grant more than `want_j` to a single agent.
- Higher `priority` is served first; equal priority keeps request order (stable).
- A grant of 0 is a valid, expected outcome — not an error.
- The broker must not open a WAN socket or invent a remote energy source.

## Key Traits
- Local-only: one energy pool, many claimants
- Low energy: intended to run every scheduler tick without dominating the budget
- Fail-soft: empty request list or empty pool returns empty grants
- Complements Model 01 (threshold policy) and Operator AI task-graph execution
- Does not replace Model 47 (hierarchical orchestrator); this card only allocates joules

## Implementation Notes
`AGENTS/energy_broker.py` is the host allocator. It is not a mesh stack. When a radio path exists, it should live under `PROTOTYPES/` and consume an explicit energy budget argument of its own.

## Next measurements (not done)
- Time `allocate` on the intended MCU or SBC for N = 2, 8, 32 claimants.
- Measure joules per allocation tick (current × time × rail voltage).
- Decide whether `priority` is an integer or an energy-weighted score after field use.
