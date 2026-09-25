"""Named 50-agent registry mapped to model cards 01-50.

This is a host catalog, not a runtime mesh and not a claim that
fifty trained models exist. Lookup and listing only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class AgentRole:
    id: int
    name: str
    domain: str
    default_if_unmeasured: str
    card: str


AGENTS: List[AgentRole] = [
    AgentRole(1, "Rail Floor Agent", "Natural Electric", "SLEEP", "01-threshold-energy-scheduler.md"),
    AgentRole(2, "Irradiance Forecast Agent", "TinyML + Harvest", "HOLD", "02-quantized-lstm-irradiance-forecaster.md"),
    AgentRole(3, "Duty-Cycle RL Agent", "Energy-aware Agents", "FALLBACK_01", "03-rl-duty-cycle-controller.md"),
    AgentRole(4, "Hybrid Harvest Agent", "Harvest Sensing", "SINGLE_SOURCE", "04-hybrid-pv-rf-energy-state-estimator.md"),
    AgentRole(5, "Capacitance Proxy Agent", "Power Management", "REFUSE_JOULES", "05-supercap-voltage-proxy.md"),
    AgentRole(6, "Early-Exit Vision Agent", "Edge Vision", "SKIP_OR_EARLY", "06-early-exit-tiny-classifier.md"),
    AgentRole(7, "Binary Gate Agent", "Ultra-constrained", "GATE_CLOSED", "07-binary-neural-net-sensor-gate.md"),
    AgentRole(8, "Spiking Encode Agent", "Neuromorphic", "HOLD_SAMPLES", "08-event-driven-spiking-encoder.md"),
    AgentRole(9, "Offline RAG Agent", "Offline Knowledge", "SKIP_RETRIEVE", "09-local-rag-retriever-quantized.md"),
    AgentRole(10, "Offline LLM Adapter Agent", "Off-grid AI Box", "NO_DECODE", "10-offline-llm-runtime-adapter.md"),
    AgentRole(11, "Energy Broker Agent", "Agentic Mesh", "REFUSE_GRANT", "11-multi-agent-energy-broker.md"),
    AgentRole(12, "Checkpoint Agent", "Batteryless", "REFUSE_COMMIT", "12-intermittent-compute-checkpoint.md"),
    AgentRole(13, "Magnetic Harvest Agent", "Ambient Magnetic", "SKIP_FIT", "13-magnetic-field-harvest-predictor.md"),
    AgentRole(14, "Vibration TENG Agent", "Mechanical Harvest", "SKIP_FIT", "14-vibration-teng-feature-extractor.md"),
    AgentRole(15, "Indoor Lux Agent", "Indoor PV", "HOLD_POLICY", "15-indoor-lux-adaptive-scheduler.md"),
    AgentRole(16, "Integrity Auditor Agent", "Security", "REFUSE_TRUST", "16-secure-integrity-auditor.md"),
    AgentRole(17, "Air-Gap Config Agent", "Security / Networking", "REFUSE_PARSE", "17-air-gap-config-validator.md"),
    AgentRole(18, "Mesh Route Agent", "Sovereign Networking", "HOLD_ROUTE", "18-local-mesh-routing-policy.md"),
    AgentRole(19, "Neutral-Probability Agent", "Formal / Probabilistic", "OMIT_CERT", "19-energy-neutral-probability-estimator.md"),
    AgentRole(20, "NILM Tree Agent", "NILM / Sensing", "SKIP_DISAGG", "20-tiny-decision-tree-disaggregator.md"),
    AgentRole(21, "Forest Policy Agent", "Control", "SKIP_VOTE", "21-quantized-random-forest-policy.md"),
    AgentRole(22, "Cascade Exit Agent", "Multi-stage Inference", "FIRST_EXIT", "22-hierarchical-early-exit-cascade.md"),
    AgentRole(23, "KV-Cache Adapter Agent", "LLM Edge", "TRUNCATE", "23-memory-efficient-kv-cache-adapter.md"),
    AgentRole(24, "Speculative Decode Agent", "LLM Acceleration", "SKIP_OR_FULL", "24-speculative-decode-lite.md"),
    AgentRole(25, "Continual-Learn Gate Agent", "Adaptive Edge", "HOLD_UPDATE", "25-on-device-continual-learner.md"),
    AgentRole(26, "Federated Aggregate Agent", "Distributed", "SKIP_AGG", "26-federated-aggregate-offline.md"),
    AgentRole(27, "DP Noise Agent", "Privacy", "REFUSE_EXPORT", "27-differential-privacy-noise-injector.md"),
    AgentRole(28, "Physical Control Agent", "Robotics / Physical", "HOLD_ACTUATOR", "28-physical-ai-low-level-controller.md"),
    AgentRole(29, "World-Model Lite Agent", "Spatial Intelligence", "SKIP_DYNAMICS", "29-world-model-lite.md"),
    AgentRole(30, "Reservoir Agent", "Physical Reservoir", "DIGITAL_FALLBACK", "30-neuromorphic-reservoir.md"),
    AgentRole(31, "Ionic Synapse Agent", "Neuromorphic Materials", "OUT_OF_SCOPE", "31-ionic-synapse-conductance.md"),
    AgentRole(32, "Co-Harvest Encode Agent", "Dual Harvest", "SINGLE_HARVEST", "32-energy-information-co-harvest-encoder.md"),
    AgentRole(33, "Energy Contract Agent", "Verification", "REFUSE_PROOF", "33-formal-energy-contract-checker.md"),
    AgentRole(34, "Power-Path Agent", "Power Electronics + AI", "HOLD_PATH", "34-multi-source-power-path-optimizer.md"),
    AgentRole(35, "Hand-Crank Planner Agent", "Portable Off-grid", "SOLAR_ONLY", "35-hand-crank-solar-duty-planner.md"),
    AgentRole(36, "Energy-Aware MAC Agent", "Networking", "SLEEP_RADIO", "36-ble-mesh-energy-aware-mac.md"),
    AgentRole(37, "Attestation Agent", "Security", "REFUSE_DISPATCH", "37-secure-boot-model-attestation-lite.md"),
    AgentRole(38, "Multimodal Fusion Agent", "Sensing", "SINGLE_MODALITY", "38-quantized-multimodal-sensor-fusion.md"),
    AgentRole(39, "Energy-Anomaly Agent", "Monitoring", "LOG_ONLY", "39-anomaly-detector-energy-signature.md"),
    AgentRole(40, "Self-Heal Restart Agent", "Resilience", "RESTART_HOLD", "40-self-healing-agent-restart-policy.md"),
    AgentRole(41, "Token-Budget Planner Agent", "Agentic", "TRUNCATE_PLAN", "41-token-budget-aware-agent-planner.md"),
    AgentRole(42, "Tool-Guardrail Agent", "Safe Agents", "BLOCK_TOOL", "42-tool-use-guardrail.md"),
    AgentRole(43, "Preference Align Agent", "Alignment", "SKIP_ALIGN", "43-local-preference-alignment.md"),
    AgentRole(44, "Reasoning Trace Agent", "Reasoning", "SHORT_ANSWER", "44-distilled-reasoning-trace.md"),
    AgentRole(45, "Sparse GNN Agent", "Structured Data", "SKIP_GRAPH", "45-edge-sparse-gnn.md"),
    AgentRole(46, "Temporal Forecast Agent", "Time-series", "HOLD_FORECAST", "46-temporal-graph-energy-forecaster.md"),
    AgentRole(47, "Hierarchy Orchestrator Agent", "Operator AI", "DEFER", "47-hierarchical-multi-agent-orchestrator.md"),
    AgentRole(48, "Sovereign Allocator Agent", "Systems", "REFUSE_SLOT", "48-sovereign-compute-resource-allocator.md"),
    AgentRole(49, "Architecture-Search Gate Agent", "Meta / AutoML", "SKIP_SEARCH", "49-genetic-architecture-search-lite.md"),
    AgentRole(50, "Enterprise Template Agent", "Commercial / Contract", "INCOMPLETE", "50-enterprise-identical-model-template.md"),
]


def by_id(agent_id: int) -> Optional[AgentRole]:
    for agent in AGENTS:
        if agent.id == agent_id:
            return agent
    return None


def all_ids() -> List[int]:
    return [a.id for a in AGENTS]


def completeness() -> Dict[str, int]:
    ids = set(all_ids())
    return {
        "count": len(AGENTS),
        "expected": 50,
        "missing": len(set(range(1, 51)) - ids),
        "complete": int(ids == set(range(1, 51))),
    }


if __name__ == "__main__":
    c = completeness()
    print(c)
    if not c["complete"]:
        raise SystemExit("registry is incomplete")
    print("50 agents registered")
