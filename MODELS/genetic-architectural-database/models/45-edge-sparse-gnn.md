# 45 — Edge Graph Neural Net (Sparse)

**Domain:** Structured Data  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no trained GNN, no adjacency store, no graph certificate)  
**Operator role:** Optional host gate that refuses a sparse-graph step when the named graph table is missing, a layer row is `to-be-measured` without a hold, or the hop class is unknown. Not a production GNN trainer and not a certified graph-inference runtime.

## Description
Harvested-power agents can spend more joules walking a dense adjacency than reading the few edges that matter. A cheap policy can decide whether the *next* sparse-GNN step may run against a named graph table, shrink to a 1-hop neighborhood, or stay deferred so the rail can recover. A full trained GNN + measured joules-per-message-pass is out of scope until named graph rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no trained weight file, no CSR/CSC adjacency store, no calibrated message-pass-to-joule library, and no measured joule-per-layer** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A graph decision is a *policy event*, not proof that message passing occurred.
- Host evaluation of a fixture graph table on a laptop is not a GNN certificate.
- Do not claim GraphSAGE, GAT, GCN production status, or “certified sparse inference” from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named graph table* may consume that rail.
- Distinct from Model 11: Model 11 allocates energy across agents. This card allocates *permission for one graph table inside one wake*.
- Distinct from Model 18: Model 18 is mesh routing policy. This card is *feature aggregation on a named graph*, not hop forwarding.
- Distinct from Model 38: Model 38 fuses multimodal sensors. This card aggregates *named graph neighborhoods*.
- Distinct from Model 44: Model 44 gates reasoning traces. This card gates *sparse message-pass layers*.
- Distinct from Model 46: Model 46 (still a stub) is a temporal graph energy forecaster. This card is one static sparse pass.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `graph_table` | input | Named graph rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_gnn` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `gnn_id` | input | Ancestry id (`45` or `45-custom-<slug>`). Not a silicon lot |
| `max_hops` | input | Design cap on named message-pass hops in one wake window |
| `max_edges` | input | Design cap on edges visited in one wake |
| `tok_ok` | input | Optional Model 41 result; a refused plan should not walk graphs |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not write embeddings |
| `rsn_ok` | input | Optional Model 44 result; a refused trace should not seed graph features |
| `att_ok` | input | Optional Model 37 result; an unattested model should not walk graphs |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `message_pass` |
| `gnn_action` | output | `hold` / `one_hop` / `message_pass` / `defer` / `unknown` |
| `edges_checked` | output | Planned edge-row count after the action |
| `gnn_ok` | output | Boolean: the next scheduled sparse-GNN step may run under the named table |
| `refuse_reason` | output | `energy` / `missing_graphtable` / `unmeasured` / `no_hold` / `plan` / `tool` / `trace` / `attest` / `grant` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured GNN energy) |

Planned entry points:
- `gnn_step(energy_state, graph_table, hold_gnn) -> gnn_action`
- `gnn_ok(energy_state, graph_table, hold_gnn) -> bool`
- `gate_task(task_id, gnn_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture graph table on the laptop CI runner; that is still not a trained GNN.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-agent energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when attestation is in scope — otherwise omit.
4. Model 41 `tok_ok()` when the graph walk is plan-driven — otherwise omit.
5. Model 42 `grd_ok()` when the graph walk is tool-driven — otherwise omit.
6. Model 44 `rsn_ok()` when the graph features come from a reasoning trace — otherwise omit.
7. Model 45 `gnn_ok()` — refuse unless every in-scope graph row is `agreed` or has a named hold.
8. Only then `gate_task(allow)` for the scheduled sparse-GNN step.

Missing graph-table fields must refuse with `missing_graphtable`. Rows marked `to-be-measured` without `hold_gnn` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `tok_ok`, `grd_ok`, `rsn_ok`, `att_ok`, or `energy_grant_ok` false must still refuse `message_pass`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU GNN layers |
| Skip (`gnn_ok` false) | 0 J extra | Gate via Model 01 / 11 / 37 / 41 / 42 / 44 / 45 |
| On-device one_hop / message_pass | unknown | Do not schedule until measured |
| Full trained GNN + calibrated layer-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `message_pass` or `one_hop` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `gnn_ok` as proof that *message passing occurred* — only that the named table is internally consistent with the hold policy.
- Do not invent mAP, layer counts as certificates, or certified graph joules in host logs.
- Do not treat this card as a GraphSAGE / GAT / GCN trainer or graph certificate.

## Key Traits
- Sparse edge GNN lite is a refuse/allow gate, not a trainer
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / attestation / token / tool / trace gates) and *before* any field embedding write that depends on agreed table rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_graphtable`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, `grd`, `aln`, or `rsn`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary graph weights or fake GNN marks into this public card.

## Next measurements (not done)
- Time and current for one_hop vs message_pass vs hold on the intended MCU + rail.
- Decide whether graph tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a graph certificate.
- Optional host stub: `gnn_ok()` on a fixture graph table in CI — still not a trained GNN.
