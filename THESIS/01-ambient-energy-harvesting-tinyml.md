# Research Axis 01 — Ambient Energy Harvesting + TinyML

## Problem
Battery maintenance and grid dependency remain the primary barriers to dense, long-lived intelligent sensing and edge AI. Natural Electric approaches treat the environment itself as the power source.

## Approach
- Hybrid harvesting (PV indoor/outdoor, magnetic field around conductors, vibration/TENG, ambient RF).
- Supercapacitor or hybrid storage with observable voltage as energy-state proxy.
- Quantized TinyML models (Decision Tree / Random Forest / tiny NN / LSTM) whose inference cost is known in mJ.
- Reinforcement-learning or rule-based policies that throttle sensing, inference, and radio according to energy state and predicted harvest.

## Key References (2024–2026)
- MIT magnetic-field energy harvesting self-powered sensors.
- Indoor PV + EdgeML demonstrations (Epishine, DSSC, OPV, perovskite under lux-level lighting).
- Hybrid PV+RF + RL-scheduled TinyML for energy-neutral IoT.
- Solar-powered Raspberry Pi Zero / ESP32 LLM and sensor nodes.

## Prototype in this Repository
See `PROTOTYPES/energy-harvester-tinyml/`.

## Open Questions for 2036
- Co-design of harvester physics + neuromorphic compute so that energy and information are harvested simultaneously.
- Formal guarantees of energy-neutral operation under adversarial or highly variable environments.
- Scaling from single nodes to self-organizing energy-aware agent meshes.
