# 03 — RL Duty-Cycle Controller

**Domain:** Energy-aware Agents / Control  
**Energy Profile:** Low–Medium  
**Status:** Catalog

## Description
Reinforcement-learning policy (or distilled imitation of one) that selects sensing / inference / transmission / sleep actions to maximize long-term information value while keeping the energy store within safe bounds. Trained offline on simulated or measured harvest traces; deployed quantized.

## Key Traits
- Explicitly optimizes for energy-neutral probability
- Can incorporate uncertainty estimates from the irradiance forecaster
- Designed to replace or augment the simple threshold scheduler
