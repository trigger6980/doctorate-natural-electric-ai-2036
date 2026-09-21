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
5. **Integrity & Contract Layer** — verifies model hashes, energy contracts, and safe failure modes.
6. **Enterprise Interface** — configuration and licensing surface for identical or customized deployments.

## Task-graph executor (current behavior)
- Sequential dispatch with dependency checks.
- Per-task `min_joules` energy gate; abort reason recorded instead of silent skip.
- Checkpoint object stores completed task names and a shared context dict so a brown-out can resume.
- Unknown dependencies fail at construction time.

Not yet implemented: parallel workers, hardware energy observer hook, cryptographic integrity, persistence to flash.

## Relationship to the 50-Model Database
Many of the architectural models in the Genetic / Architectural Model Database are intended to plug into this operator machinery as interchangeable or composable components. Model 01 (threshold energy scheduler) is the first policy intended to sit in front of the executor.

## Status
Foundational document plus a host-side executor skeleton. Hardware integration and configuration schemas will be added incrementally under `AGENTS/` and linked from the model catalog.
