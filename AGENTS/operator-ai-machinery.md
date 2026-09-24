# Operator AI Machinery

Foundational description of the operator-level AI machinery used and extended in this portfolio.

## Purpose
Provide a reliable, energy-aware, multi-agent orchestration layer that can:
- Observe energy state and environmental signals
- Plan and dispatch tasks across specialized agents / models
- Maintain progress under intermittent power and connectivity
- Enforce safety, integrity, and resource contracts
- Support both research experimentation and enterprise deployment

## Core Components (Current + Planned)
1. **Energy State Observer** — continuous or sampled reading of voltage / estimated joules / harvest rate. Model 04 specifies the planned fusion interface; Model 05 specifies voltage→joules.
2. **Policy / Scheduler** — decides which models or agents may run (starts with threshold policy, evolves to learned and hierarchical).
3. **Agent Registry** — catalog of available specialized agents (research, security, sensing, planning, etc.).
4. **Task Graph Executor** — runs ordered or conditional workflows with checkpointing for intermittent compute. **Skeleton now in** `AGENTS/task_graph_executor.py` with tests in `AGENTS/test_task_graph_executor.py`.
5. **Policy gate** — `AGENTS/policy_gated_executor.py` runs Model 01 (or a compatible `policy_fn`) *before* the graph. SLEEP refuses the graph; SENSE/INFER/TRANSMIT filter tasks by tag. Optional `gas_search` preflight records Model 49 refuse tokens as `gas_<reason>` skips. That is a research gate, not a NAS certificate.
6. **Energy broker (Model 11)** — `AGENTS/energy_broker.py` partitions one local pool. `AGENTS/brokered_executor.py` grants before run; refuse maps to skip.
7. **Integrity & Contract Layer** — verifies model hashes, energy contracts, and safe failure modes.
8. **Enterprise Interface** — configuration and licensing surface for identical or customized deployments.
9. **Host sandbox** — `SANDBOX/run_prototypes.py` runs the public stubs as specialized agents on a host. Not hardware.

## Task-graph executor (current behavior)
- Sequential dispatch with dependency checks.
- Per-task `min_joules` energy gate; abort reason recorded instead of silent skip.
- Checkpoint object stores completed task names and a shared context dict so a brown-out can resume (Model 12 host stand-in).
- **Host-file persistence:** `Checkpoint.save(path)` / `Checkpoint.load(path)` write JSON. This is a stand-in for flash, not a hardware driver.
- Unknown dependencies fail at construction time.
- Policy gate maps Action → allowed task tags (`sense` / `infer` / `transmit`).
- Optional Model 49 preflight maps `refuse_reason` onto `aborted_reason='gas_<reason>'` before the energy policy runs.
- Brokered path maps Model 11 grants onto the same graph.

Not yet implemented: parallel workers, hardware energy observer hook, cryptographic integrity, on-device flash mapping, radio mesh.

## Relationship to the 50-Model Database
Many of the architectural models in the Genetic / Architectural Model Database are intended to plug into this operator machinery as interchangeable or composable components. Model 01 (threshold energy scheduler) is the first policy sitting in front of the executor. Model 03 is specified to use the same `policy_fn` slot. Model 02 is specified as an INFER-tagged task that the gate may skip. Models 04 and 05 specify the observer / joule-proxy that should eventually fill `estimated_joules`. Model 11 allocates the pool among local agents. Model 12 is the checkpoint contract. Model 49 may preflight the same graph with a fixture candidate table; a pass is not an architecture certificate.

## Status
Foundational document plus a host-side executor skeleton, policy gate, JSON checkpoint files, energy broker, brokered executor, Model 49 gas preflight, and host sandbox. Hardware integration and configuration schemas will be added incrementally under `AGENTS/` and linked from the model catalog.
