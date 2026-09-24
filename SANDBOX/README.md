# Host sandbox (not hardware)

This folder is a **host-side** runner so specialized agents can execute the public Python prototypes against the Model 11 design contract.

It is not a VM, not an MCU, and not a licensed runtime pack.

## What it runs
1. Model 01 scheduler simulation (`energy_aware_scheduler.run_simulation`).
2. Model 11 `allocate` across four named local agents (sense, infer, retrieve, generate).
3. Model 11 ↔ task-graph `brokered_run` (grant before run; refuse maps to skip).
4. Model 12 host checkpoint write to `SANDBOX/out/checkpoint.json`.
5. Generator 03 control-name log (`SANDBOX/out/gen03_decisions.json`) from labeled host scenarios. Names only; no watts.
6. Model 49 gas preflight demo (`SANDBOX/out/gas_preflight.json`) via `policy_gated_executor.decide_and_run`. Surfaces `_gas_reason` for an agreed-row table and a missing-table refuse. Research labels only.
7. Host energy observer demo (`SANDBOX/out/energy_observer.json`) via `AGENTS/energy_observer.py`. Sources are `host_placeholder` or `hardware_pending`. `is_field_measurement` is always false.

## How to run
From the repository root:

```bash
python SANDBOX/run_prototypes.py
```

Optional knobs (environment):
- `SANDBOX_POOL_J` — joules in the local pool (default `0.12`)
- `SANDBOX_RESERVE_J` — unallocated floor (default `0.01`)

## Specialized agent roles in the demo graph
| Agent id | Role | Tag | Placeholder want_j |
| --- | --- | --- | --- |
| sense | TinyML sense body | sense | 0.002 |
| infer | Tiny classifier | infer | 0.009 |
| retrieve | Model 09 stand-in | infer | 0.05 |
| generate | Model 10 stand-in | transmit | 0.40 |

With the default 0.12 J pool and 0.01 J reserve, generate is expected to be **skipped**. That is the contract working, not a failure.

## Model 49 labels in this folder
`summary.json` may include `_gas_reason_ok` and `_gas_reason_missing_table`. Those strings are the same research tokens used by `AGENTS/gas_search_gate.py`. They are not NAS results, not measured generation joules, not decline codes, and not `inquiry_ok`.

## Energy observer labels in this folder
`summary.json` may include `observer_source_placeholder` and `observer_is_field_measurement`. Those fields come from the host stub. They are not ADC readings, not a quote attachment, and not proof of harvest.

## What this sandbox does not do
- Calibrate `C_farads`
- Load GGUF weights or an embedding index
- Open a network socket
- Measure real joules
- Drive a heat pump, Peltier stage, or TEG
- Run a neural architecture search farm
