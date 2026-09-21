# 01 — Threshold Energy Scheduler

**Domain:** Natural Electric / Power Management  
**Energy Profile:** Ultra-low  
**Status:** Skeleton code already present in `PROTOTYPES/energy-harvester-tinyml/`

## Description
Simple but effective policy that maps observed supercapacitor / battery voltage (and optional estimated joules) to discrete actions: SLEEP, SENSE, INFER, TRANSMIT. Thresholds are configurable. Serves as the baseline energy-aware controller for all higher models.

## Key Traits
- Deterministic and fully auditable
- Extremely low compute cost
- Directly couples physical energy state to software behavior
- Easy to replace with learned policies (RL, decision tree, etc.) later

## Implementation Notes
See `PROTOTYPES/energy-harvester-tinyml/src/energy_aware_scheduler.py` and accompanying tests.
