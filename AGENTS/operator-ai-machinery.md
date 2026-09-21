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
1. **Energy State Observer** — continuous or sampled reading of voltage / estimated joules / harvest rate.
2. **Policy / Scheduler** — decides which models or agents may run (starts with threshold policy, evolves to learned and hierarchical).
3. **Agent Registry** — catalog of available specialized agents (research, security, sensing, planning, etc.).
4. **Task Graph Executor** — runs ordered or conditional workflows with checkpointing for intermittent compute. **Skeleton now in** `AGENTS/task_graph_executor.py` with tests in `AGENTS/test_task_graph_executor.py`.
5. **Policy gate** — `AGENTS/policy_gated_executor.py` runs Model 01 (or a compatible `policy_fn`) *before* the graph. SLEEP refuses the graph; SENSE/INFER/TRANSMIT filter tasks by tag.
6. **Integrity & Contract Layer** — verifies model hashes, energy contracts, and safe failure modes.
7. **Enterprise Interface** — configuration and licensing surface for identical or customized deployments.

## Task-graph executor (current behavior)
- Sequential dispatch with dependency checks.
- Per-task `min_joules` energy gate; abort reason recorded instead of silent skip.
- Checkpoint object stores completed task names and a shared context dict so a brown-out can resume.
- Unknown dependencies fail at construction time.
- Policy gate maps Action → allowed task tags (`sense` / `infer` / `transmit`).

Not yet implemented: parallel workers, hardware energy observer hook, cryptographic integrity, persistence to flash.

## Relationship to the 50-Model Database
Many of the architectural models in the Genetic / Architectural Model Database are intended to plug into this operator machinery as interchangeable or composable components. Model 01 (threshold energy scheduler) is the first policy sitting in front of the executor. Model 03 is specified to use the same `policy_fn` slot. Model 02 is specified as an INFER-tagged task that the gate may skip.

## Status
Foundational document plus a host-side executor skeleton and a policy gate. Hardware integration and configuration schemas will be added incrementally under `AGENTS/` and linked from the model catalog.
