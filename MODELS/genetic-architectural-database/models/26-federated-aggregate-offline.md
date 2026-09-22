# 26 — Federated Aggregate (Offline-Capable)

**Domain:** Distributed  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no federated trainer, no privacy certificate, no measured aggregate joules)  
**Operator role:** Optional host gate that refuses a local share-or-merge step when the rail cannot pay the encode-plus-merge pair, or when the named share budget is missing. Not a production federated-learning runtime and not a multi-site weight file.

## Description
Some off-grid clusters only need a staged refuse: *hold*, *encode*, *merge*, *commit*, or *unknown*. A full federated stack (secure aggregation, measured share joules, multi-site coordinator) is out of scope until a named aggregator and a share budget exist on the intended nodes.

This card specifies the host-facing interface. There is **no trainer weight file, no public client roster, and no measured joule-per-share** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A federated-aggregate decision is a *policy event*, not proof the merged weights are better or private.
- Host evaluation of a fixture share size on a laptop is not a field federation certificate.
- Do not claim FedAvg, secure aggregation, differential privacy, or “certified offline federation” status from this card.
- Distinct from Model 25: Model 25 gates a *local* update-plus-verify pair. This card gates whether a *share* may be encoded or merged.
- Distinct from Model 27 (catalog stub): noise injection is a later card. This card must still refuse if the share size is missing even when no noise model exists.
- Distinct from Model 11: Model 11 partitions one local energy pool. This card does not allocate watts across sites.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `share_bytes` | input | Named placeholder size. Uncalibrated |
| `peer_count` | input | Named placeholder count. Uncalibrated; not a live roster |
| `agg_id` | input | Ancestry id (`26` or `26-custom-<slug>`). Not a trainer hash |
| `max_share_bytes` | input | Design cap. Larger shares are out of this card |
| `agg_action` | output | `hold` / `encode` / `merge` / `commit` / `unknown` |
| `bytes_shared` | output | Planned count after the action |
| `agg_ok` | output | Boolean: the next encode-plus-merge pair may run |
| `refuse_reason` | output | `energy` / `missing_budget` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `agg_step(energy_state, share_bytes, peer_count) -> agg_action`
- `agg_ok(energy_state, share_bytes, peer_count) -> bool`
- `gate_task(task_id, agg_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture share size on the laptop CI runner; that is still not a federated trainer.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse commit unless a host JSON path exists.
4. Model 25 `learn_ok()` when a local update precedes the share — otherwise omit.
5. Model 26 `agg_ok()` — refuse encode/merge unless the named sizes fit.
6. Only then `gate_task(allow)` for the aggregate step.

Missing budget fields must refuse with `missing_budget`. An `unknown` action must skip the encode-merge pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or NPU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-encode | 0.001–0.05 J | Cheap compares, not radio or NPU traces |
| Skip (`agg_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 25 / 26 |
| On-device encode + merge | unknown | Do not schedule until measured |
| Multi-site federated trainer | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an encode or merge when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `commit` as proof the *merged weights* are private or accurate — only that the named sizes fit the budget.
- Do not invent client-count or joules-per-round numbers in host logs.

## Key Traits
- Offline federation is a refuse/allow gate, not a certified multi-site runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* local learn/checkpoint gates and *before* any share write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_budget` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, or `learn`. Keep joule costs labeled uncalibrated until an MCU/NPU measurement exists. Do not check federated weights or client rosters into this public card.

## Next measurements (not done)
- Time and current for encode vs merge vs hold on the intended runtime.
- Decide whether share size is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a federation certificate.
- Optional host stub: `agg_ok()` on a fixture share size in CI — still not a federated trainer.
