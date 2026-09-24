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
- [First-page routing](../../ENTERPRISE/first-page-routing.md)
- [Scope assumptions for a quote](../../ENTERPRISE/scope-assumptions.md)
- [Placeholder engagement tiers](../../ENTERPRISE/placeholder-engagement-tiers.md)
- [Allowed cover-letter claims](../../ENTERPRISE/allowed-cover-claims.md)
- [Operator AI Machinery](../../AGENTS/operator-ai-machinery.md)
- [Host sandbox](../../SANDBOX/README.md)
- [Model 50 commercial template](models/50-enterprise-identical-model-template.md)

Cards **01–50** now share an honesty pattern. Cards 01–49 use interface + energy-budget + next-measurements. Card **50** uses the same refuse/allow pattern as a *commercial template* that points at the order page — not a product sheet and not a SKU list. Model 05 has a host helper (`joules_from_voltage` / `voltage_from_joules`) that is **analytic and uncalibrated**. Model 11 has a host allocator stub (`AGENTS/energy_broker.py`) plus a brokered task-graph path (`AGENTS/brokered_executor.py`). Model 12 documents the existing host JSON checkpoint as an interface, not flash. Models 13–48 remain interface-only as previously recorded. Model 49 has a host fixture stub (`AGENTS/gas_search_gate.py`) plus an optional policy-executor preflight (`gas_search` → `gas_<reason>`): no NAS controller and no architecture-search certificate. Model 50 has a host checklist (`ENTERPRISE/inquiry_completeness.py`) that only counts the six public completeness items.

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
| 10 | Offline LLM Runtime Adapter | Off-grid AI Box | Medium–High | Interface specified |
| 11 | Multi-Agent Energy Broker | Agentic Mesh | Low | Interface + host allocator + brokered executor |
| 12 | Intermittent Compute Checkpoint Model | Batteryless | Ultra-low | Interface specified (host JSON only) |
| 13 | Magnetic Field Harvest Predictor | Ambient Magnetic | Ultra-low | Interface specified (no coil / no tesla fit) |
| 14 | Vibration / TENG Feature Extractor | Mechanical Harvest | Ultra-low | Interface specified (no piezo-TENG / no cycle fit) |
| 15 | Indoor Lux Adaptive Scheduler | Indoor PV | Ultra-low | Interface specified (no photodiode / no lux-joule fit) |
| 16 | Secure Integrity Auditor | Security | Low | Interface specified (no TPM / no measured hash J) |
| 17 | Air-Gap Config Validator | Security / Networking | Low | Interface specified (no schema compiler / no measured parse J) |
| 18 | Local Mesh Routing Policy | Sovereign Networking | Low | Interface specified (no radio / no measured hop J) |
| 19 | Energy-Neutral Probability Estimator | Formal / Probabilistic | Low | Interface specified (no survival curve / no certificate) |
| 20 | Tiny Decision Tree Disaggregator | NILM / Sensing | Ultra-low | Interface specified (no trained tree / no NILM certificate) |
| 21 | Quantized Random Forest Policy | Control | Low | Interface specified (no trained forest / no control certificate) |
| 22 | Hierarchical Early-Exit Cascade | Multi-stage Inference | Low–Medium | Interface specified (no trained cascade / no inference certificate) |
| 23 | Memory-Efficient KV Cache Adapter | LLM Edge | Medium | Interface specified (no packed KV / no context-window certificate) |
| 24 | Speculative Decode Lite | LLM Acceleration | Medium | Interface specified (no draft model / no accept-rate certificate) |
| 25 | On-Device Continual Learner (Constrained) | Adaptive Edge | Medium | Interface specified (no trainer / no plasticity certificate) |
| 26 | Federated Aggregate (Offline-Capable) | Distributed | Medium | Interface specified (no federated trainer / no privacy certificate) |
| 27 | Differential Privacy Noise Injector (Edge) | Privacy | Low | Interface specified (no sampler firmware / no DP certificate) |
| 28 | Physical AI Low-Level Controller | Robotics / Physical | Medium | Interface specified (no actuator driver / no motion certificate) |
| 29 | World-Model Lite (Video Dynamics) | Spatial Intelligence | High | Interface specified (no video encoder / no dynamics certificate) |
| 30 | Neuromorphic Reservoir Computer | Physical Reservoir | Ultra-low–Low | Interface specified (no analog node / no reservoir certificate) |
| 31 | Ionic Synapse Conductance Model | Neuromorphic Materials | Research | Interface specified (no wet-lab cell / no materials certificate) |
| 32 | Energy-Information Co-Harvest Encoder | Dual Harvest | Ultra-low | Interface specified (no co-harvest transducer / no dual-harvest certificate) |
| 33 | Formal Energy Contract Checker | Verification | Low | Interface specified (no proof checker / no verification certificate) |
| 34 | Multi-Source Power Path Optimizer | Power Electronics + AI | Low | Interface specified (no MPPT firmware / no power-path certificate) |
| 35 | Hand-Crank + Solar Duty Planner | Portable Off-grid | Low | Interface specified (no crank firmware / no portable-duty certificate) |
| 36 | BLE / Mesh Energy-Aware MAC | Networking | Ultra-low | Interface specified (no radio firmware / no MAC certificate) |
| 37 | Secure Boot + Model Attestation Lite | Security | Low | Interface specified (no boot firmware / no attestation certificate) |
| 38 | Quantized Multimodal Sensor Fusion | Sensing | Low–Medium | Interface specified (no fusion graph / no fusion certificate) |
| 39 | Anomaly Detector (Energy Signature) | Monitoring | Low | Interface specified (no trained detector / no anomaly certificate) |
| 40 | Self-Healing Agent Restart Policy | Resilience | Low | Interface specified (no watchdog firmware / no restart certificate) |
| 41 | Token-Budget Aware Agent Planner | Agentic | Medium | Interface specified (no planner runtime / no planning certificate) |
| 42 | Tool-Use Guardrail Model | Safe Agents | Low | Interface specified (no tool runtime / no safety certificate) |
| 43 | Local Preference Alignment (Tiny) | Alignment | Medium | Interface specified (no preference trainer / no alignment certificate) |
| 44 | Distilled Reasoning Trace Model | Reasoning | Medium | Interface specified (no teacher / no reasoning certificate) |
| 45 | Edge Graph Neural Net (Sparse) | Structured Data | Medium | Interface specified (no trained GNN / no graph certificate) |
| 46 | Temporal Graph Energy Forecaster | Time-series | Medium | Interface specified (no trained T-GNN / no forecast certificate) |
| 47 | Hierarchical Multi-Agent Orchestrator | Operator AI | Medium–High | Interface specified (no production orchestrator / no orchestration certificate) |
| 48 | Sovereign Compute Resource Allocator | Systems | Medium | Interface specified (no cluster scheduler / no allocation certificate) |
| 49 | Genetic Architecture Search Lite | Meta / AutoML | Medium | Interface + host fixture stub + policy preflight (no NAS controller / no architecture certificate) |
| 50 | Enterprise Identical Model Template | Commercial / Contract | Configurable | Interface + host completeness checklist (not a product sheet) |

---

## How to Use This Database

- Researchers: reference the architecture descriptions and extend the skeletons.
- Enterprise: start at [first-page routing](../../ENTERPRISE/first-page-routing.md), then the [Model 50 card](models/50-enterprise-identical-model-template.md) and the Order & Contract page to request identical or customized instances under formal agreement. Attach the scope-assumptions table so energy claims stay labeled. Use placeholder engagement tiers to name the *shape* of work — not a price. Use allowed cover-letter claims so quotes stay inside what the public tree can support.
- Contributors: open issues or PRs to deepen any entry with code, measurements, or citations.

All models are intended to remain compatible with the Natural Electric principle: energy state is a first-class runtime signal.
