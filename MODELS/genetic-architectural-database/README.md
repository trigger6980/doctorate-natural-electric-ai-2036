# Genetic / Architectural Model Database

**50 Architectural Models for Natural Electric × Future AI Systems (2036 Horizon)**

This catalog documents 50 distinct model architectures relevant to energy-aware edge intelligence, agentic systems, neuromorphic computing, TinyML under harvested power, and sovereign/off-grid AI.

Each entry includes:
- Short description
- Primary use domain
- Energy / resource profile (qualitative)
- Key architectural traits
- Status in this repository (catalog entry / skeleton / planned)

The database is designed so independent researchers and enterprise users can reference, reproduce, or request identical/custom variants under contract.

See also:
- [Enterprise Order & Contract](../../ENTERPRISE/order-and-contract.md)
- [Scope assumptions for a quote](../../ENTERPRISE/scope-assumptions.md)
- [Operator AI Machinery](../../AGENTS/operator-ai-machinery.md)

Cards **01–09** now share the same interface + energy-budget + next-measurements pattern. Cards **10+** remain short catalog stubs until the same pattern is applied. Model 05 has a host helper (`joules_from_voltage`) that is **analytic and uncalibrated**.

---

## Catalog Index (1–50)

| # | Model Name | Domain | Energy Profile | Status |
|---|------------|--------|----------------|--------|
| 01 | Threshold Energy Scheduler | Natural Electric | Ultra-low | Skeleton code exists |
| 02 | Quantized LSTM Irradiance Forecaster | TinyML + Harvest | Low | Interface specified |
| 03 | RL Duty-Cycle Controller | Energy-aware Agents | Low–Medium | Interface specified |
| 04 | Hybrid PV-RF Energy State Estimator | Harvest Sensing | Ultra-low | Interface specified |
| 05 | Supercap Voltage Proxy Model | Power Management | Ultra-low | Interface + uncalibrated host helper |
| 06 | Early-Exit Tiny Classifier | Edge Vision / Sensing | Low | Interface specified |
| 07 | Binary Neural Net Sensor Gate | Ultra-constrained | Ultra-low | Interface specified |
| 08 | Event-Driven Spiking Encoder | Neuromorphic | Ultra-low | Interface specified |
| 09 | Local RAG Retriever (Quantized) | Offline Knowledge | Medium | Interface specified |
| 10 | Offline LLM Runtime Adapter | Off-grid AI Box | Medium–High | Catalog |
| 11 | Multi-Agent Energy Broker | Agentic Mesh | Low | Catalog |
| 12 | Intermittent Compute Checkpoint Model | Batteryless | Ultra-low | Catalog |
| 13 | Magnetic Field Harvest Predictor | Ambient Magnetic | Ultra-low | Catalog |
| 14 | Vibration / TENG Feature Extractor | Mechanical Harvest | Ultra-low | Catalog |
| 15 | Indoor Lux Adaptive Scheduler | Indoor PV | Ultra-low | Catalog |
| 16 | Secure Integrity Auditor | Security | Low | Catalog |
| 17 | Air-Gap Config Validator | Security / Networking | Low | Catalog |
| 18 | Local Mesh Routing Policy | Sovereign Networking | Low | Catalog |
| 19 | Energy-Neutral Probability Estimator | Formal / Probabilistic | Low | Catalog |
| 20 | Tiny Decision Tree Disaggregator | NILM / Sensing | Ultra-low | Catalog |
| 21 | Quantized Random Forest Policy | Control | Low | Catalog |
| 22 | Hierarchical Early-Exit Cascade | Multi-stage Inference | Low–Medium | Catalog |
| 23 | Memory-Efficient KV Cache Adapter | LLM Edge | Medium | Catalog |
| 24 | Speculative Decode Lite | LLM Acceleration | Medium | Catalog |
| 25 | On-Device Continual Learner (Constrained) | Adaptive Edge | Medium | Catalog |
| 26 | Federated Aggregate (Offline-Capable) | Distributed | Medium | Catalog |
| 27 | Differential Privacy Noise Injector (Edge) | Privacy | Low | Catalog |
| 28 | Physical AI Low-Level Controller | Robotics / Physical | Medium | Catalog |
| 29 | World-Model Lite (Video Dynamics) | Spatial Intelligence | High | Catalog |
| 30 | Neuromorphic Reservoir Computer | Physical Reservoir | Ultra-low–Low | Catalog |
| 31 | Ionic Synapse Conductance Model | Neuromorphic Materials | Research | Catalog |
| 32 | Energy-Information Co-Harvest Encoder | Dual Harvest | Ultra-low | Catalog |
| 33 | Formal Energy Contract Checker | Verification | Low | Catalog |
| 34 | Multi-Source Power Path Optimizer | Power Electronics + AI | Low | Catalog |
| 35 | Hand-Crank + Solar Duty Planner | Portable Off-grid | Low | Catalog |
| 36 | BLE / Mesh Energy-Aware MAC | Networking | Ultra-low | Catalog |
| 37 | Secure Boot + Model Attestation Lite | Security | Low | Catalog |
| 38 | Quantized Multimodal Sensor Fusion | Sensing | Low–Medium | Catalog |
| 39 | Anomaly Detector (Energy Signature) | Monitoring | Low | Catalog |
| 40 | Self-Healing Agent Restart Policy | Resilience | Low | Catalog |
| 41 | Token-Budget Aware Agent Planner | Agentic | Medium | Catalog |
| 42 | Tool-Use Guardrail Model | Safe Agents | Low | Catalog |
| 43 | Local Preference Alignment (Tiny) | Alignment | Medium | Catalog |
| 44 | Distilled Reasoning Trace Model | Reasoning | Medium | Catalog |
| 45 | Edge Graph Neural Net (Sparse) | Structured Data | Medium | Catalog |
| 46 | Temporal Graph Energy Forecaster | Time-series | Medium | Catalog |
| 47 | Hierarchical Multi-Agent Orchestrator | Operator AI | Medium–High | Catalog |
| 48 | Sovereign Compute Resource Allocator | Systems | Medium | Catalog |
| 49 | Genetic Architecture Search Lite | Meta / AutoML | Medium | Catalog |
| 50 | Enterprise Identical Model Template | Commercial / Contract | Configurable | Order Page |

---

## How to Use This Database

- Researchers: reference the architecture descriptions and extend the skeletons.
- Enterprise: see the Order & Contract page to request identical or customized instances under formal agreement. Attach the scope-assumptions table so energy claims stay labeled.
- Contributors: open issues or PRs to deepen any entry with code, measurements, or citations.

All models are intended to remain compatible with the Natural Electric principle: energy state is a first-class runtime signal.
