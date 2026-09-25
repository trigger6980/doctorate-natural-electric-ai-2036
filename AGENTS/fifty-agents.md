# Fifty Agents — Complete Registry

**Status:** Complete as a named-role registry. These are Operator AI *roles* mapped 1:1 to the Genetic / Architectural Model Database (cards 01–50). They are **not** 50 independent production runtimes and **not** a claim that fifty trained models exist on disk.

Honesty rule: an agent listed here may *wake*, *hold*, or *refuse*. Wake does not mean the underlying model is trained, measured, or certified.

See also:
- `MODELS/genetic-architectural-database/`
- `AGENTS/operator-ai-machinery.md`
- `AGENTS/agent_registry.py`

---

## How the two agents of the hourly automation use this list

- **Agent 1 (Code Structure)** may deepen one card or one host helper per cycle.
- **Agent 2 (Enterprise)** may only reference agents whose commercial status is `catalog` or `template` — never invent SKUs.

---

## Registry (01–50)

| ID | Agent name | Role (one line) | Wakes when | Default action if unmeasured |
|----|------------|-----------------|------------|------------------------------|
| 01 | Rail Floor Agent | Maps voltage / joules to SLEEP / SENSE / INFER / TRANSMIT | Always first | SLEEP below `v_min_safe` |
| 02 | Irradiance Forecast Agent | Short-horizon lux / solar forecast for duty planning | After 01, if lux history exists | HOLD / skip forecast |
| 03 | Duty-Cycle RL Agent | Learned or distilled action policy over harvest traces | After 01 + optional 02 | Fall back to 01 thresholds |
| 04 | Hybrid Harvest Agent | Fuses PV + RF energy-state estimates | When both sources are in scope | Use single-source voltage |
| 05 | Capacitance Proxy Agent | Voltage ↔ joules conversion | When `C_farads` is named | Refuse numeric joules |
| 06 | Early-Exit Vision Agent | Cheap-then-deep classifier | Sensing task + energy grant | Exit early or skip |
| 07 | Binary Gate Agent | Ultra-cheap yes/no sensor gate | Before any expensive sensor | Gate closed |
| 08 | Spiking Encode Agent | Event / spike encoding of streams | Event sensors present | Hold analog samples |
| 09 | Offline RAG Agent | On-device retrieve-then-generate | Knowledge base loaded | Skip retrieve |
| 10 | Offline LLM Adapter Agent | Energy-aware local LLM runtime adapter | Model file present + rail high | Do not start decode |
| 11 | Energy Broker Agent | Grants joules to one requester | Multi-agent contention | Refuse grant |
| 12 | Checkpoint Agent | Intermittent-compute host JSON checkpoint | Before commit / after burst | Refuse commit |
| 13 | Magnetic Harvest Agent | Predicts magnetic-field harvest | Coil / field sensor in scope | Skip tesla fit |
| 14 | Vibration / TENG Agent | Mechanical harvest features | Vibration sensor in scope | Skip cycle fit |
| 15 | Indoor Lux Agent | Indoor-PV adaptive scheduler | Indoor lux stream present | Hold outdoor policy |
| 16 | Integrity Auditor Agent | Hash / integrity audit of files and models | Before trust of a payload | Refuse trust |
| 17 | Air-Gap Config Agent | Validates offline config without network | Config change requested | Refuse parse |
| 18 | Mesh Route Agent | Local mesh / hop policy | Radio path in scope | Hold last route |
| 19 | Neutral-Probability Agent | Energy-neutral survival estimate | Burst cost named | Omit certificate |
| 20 | NILM Tree Agent | Tiny decision-tree disaggregation | Mains / load stream | Skip disagg |
| 21 | Forest Policy Agent | Quantized random-forest control vote | Control task + grant | Frozen / skip vote |
| 22 | Cascade Exit Agent | Multi-stage early-exit inference | Inference task | Stop at first exit |
| 23 | KV-Cache Adapter Agent | Memory-efficient context packing | LLM context growth | Truncate / refuse |
| 24 | Speculative Decode Agent | Draft-then-verify decode gate | LLM decode + surplus energy | Full decode or skip |
| 25 | Continual-Learn Gate Agent | Allow or refuse local weight updates | Update budget named | HOLD update |
| 26 | Federated Aggregate Agent | Offline-capable federated merge | Peer updates present | Skip aggregate |
| 27 | DP Noise Agent | Edge differential-privacy injector | Privacy scope on | Refuse export |
| 28 | Physical Control Agent | Low-level actuator / motion gate | Actuator in scope | Hold actuators |
| 29 | World-Model Lite Agent | Cheap spatial / video dynamics | Camera + surplus | Skip dynamics |
| 30 | Reservoir Agent | Neuromorphic / physical reservoir | Analog node in scope | Digital fallback |
| 31 | Ionic Synapse Agent | Materials / conductance research gate | Lab cell named | Out of scope |
| 32 | Co-Harvest Encode Agent | Simultaneous energy + information harvest | Dual transducer named | Single harvest only |
| 33 | Energy Contract Agent | Formal energy-contract checker | Contract row present | Refuse proof |
| 34 | Power-Path Agent | Multi-source MPPT / path optimizer | Two+ sources | Hold last path |
| 35 | Hand-Crank Planner Agent | Portable solar + crank duty planner | Portable box mode | Solar-only plan |
| 36 | Energy-Aware MAC Agent | BLE / mesh MAC duty | Radio on | Sleep radio |
| 37 | Attestation Agent | Secure-boot / model attestation lite | Before dispatch of a model | Refuse dispatch |
| 38 | Multimodal Fusion Agent | Quantized sensor fusion | 2+ modalities | Use single modality |
| 39 | Energy-Anomaly Agent | Detects abnormal energy signatures | Monitor task | Log only |
| 40 | Self-Heal Restart Agent | Restart / watchdog policy | Host unhealthy | Restart hold |
| 41 | Token-Budget Planner Agent | Plans tokens vs remaining joules | Agent text task | Truncate plan |
| 42 | Tool-Guardrail Agent | Allows or blocks a tool path | Tool call requested | Block tool |
| 43 | Preference Align Agent | Tiny on-device preference gate | Preference table present | Skip align |
| 44 | Reasoning Trace Agent | Distilled reasoning-trace gate | Hard reasoning task | Short answer only |
| 45 | Sparse GNN Agent | Edge graph inference | Graph payload present | Skip graph |
| 46 | Temporal Forecast Agent | Temporal-graph energy forecast | History window named | Hold last forecast |
| 47 | Hierarchy Orchestrator Agent | Orders named child agents | Multi-role table present | One child or defer |
| 48 | Sovereign Allocator Agent | Allocates compute slots off-cloud | Slot table present | Refuse extra slots |
| 49 | Architecture-Search Gate Agent | Lite NAS / genetic search preflight | Search budget named | Skip search |
| 50 | Enterprise Template Agent | Commercial completeness checklist | Enterprise inquiry | Incomplete until 6 items present |

---

## Wake order (default Operator stack)

1. **Always:** 01 (rail floor)
2. **Safety / trust:** 16, 17, 33, 37, 40, 42
3. **Energy picture:** 02, 04, 05, 13, 14, 15, 19, 34, 35, 46
4. **Sense / infer:** 06, 07, 08, 20, 21, 22, 38, 39
5. **Language / knowledge:** 09, 10, 23, 24, 41, 43, 44
6. **Learn / share:** 12, 25, 26, 27
7. **Physical / materials:** 28, 29, 30, 31, 32
8. **Network / radio:** 18, 36
9. **Multi-agent systems:** 11, 47, 48, 49
10. **Commercial:** 50

Any agent whose card status is interface-only **must refuse or hold** rather than invent measurements.

## Completion definition used here

The 50 agents are **finished as a registry** when:
- Every ID 01–50 has a name, role, wake condition, and default unmeasured action.
- Every ID maps to an existing model card.
- `agent_registry.py` can list and look up all 50 without raising.

They are **not** finished as trained weights, field measurements, or production firmwares. That remains per-card `Next measurements` work.
