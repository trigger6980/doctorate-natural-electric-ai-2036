# 12 — Intermittent Compute Checkpoint Model

**Domain:** Batteryless / intermittent compute  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (host JSON checkpoint exists; no on-device flash mapping or measured write joules)  
**Operator role:** Persist completed task names and shared context so a brown-out can resume. Used by `TaskGraphExecutor` and the Model 11 brokered path.

## Description
A tiny persistence contract for harvested-power nodes: write the smallest state that lets work continue after voltage collapse, and refuse a write when the remaining budget cannot cover it.

This card specifies the host-facing interface. **`Checkpoint.save` / `Checkpoint.load` in `AGENTS/task_graph_executor.py` are a host JSON stand-in, not a flash driver.** Simulator write costs below are placeholders.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `completed` | state | Task names already finished |
| `context` | state | Small JSON-safe dict; no weights |
| `aborted_reason` | state | Energy / broker / policy skip |
| `energy_budget_j` | input | Skip persist if below write cost |
| `path` | parameter | Host file today; flash slot later |
| `joules_used_est` | output | Placeholder write cost |

Planned entry points:
- `save_checkpoint(state, path, energy_budget_j) -> ok`
- `load_checkpoint(path) -> state`
- `estimate_persist_cost_j(nbytes) -> float` (table lookup until measured)

Host stand-in already present: `Checkpoint.save` / `Checkpoint.load` (no energy argument yet).

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator cost | Intended physical meaning |
| --- | --- | --- |
| Serialize + write small JSON | 0.001 J | One flash page program |
| Read checkpoint | 0.0003 J | One flash page read |
| Skip persist (budget too low) | 0 J extra | Keep RAM copy only |

Safety rules:
- Never claim wear-leveling or power-fail atomicity from the host JSON helper.
- Do not persist model weights or raw sensor buffers in this object.
- A missing file is a hard fail-soft: start from an empty checkpoint, do not invent completed work.

## Key Traits
- Ultra-low energy: persist must be cheaper than the work it protects
- Idempotent resume: re-running a completed name is a no-op
- Pairs with Model 11: broker skips are recorded in `aborted_reason` and context
- Does not replace Model 40 (self-healing restart policy)

## Implementation Notes
Host JSON lives in `AGENTS/task_graph_executor.py`. The sandbox writes `SANDBOX/out/checkpoint.json` as a demo only. On-device flash mapping remains future work.

## Next measurements (not done)
- Measure joules per page program/erase on the intended MCU.
- Record wear vs checkpoint frequency; do not claim lifetime.
- Decide a maximum context byte budget after measuring flash page size.
