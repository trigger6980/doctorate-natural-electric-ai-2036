#!/usr/bin/env python3
"""Host sandbox: run public prototypes under the Model 11 design contract."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "AGENTS"))
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "energy-harvester-tinyml" / "src"))
sys.path.insert(0, str(ROOT / "SANDBOX"))

from brokered_executor import brokered_run  # noqa: E402
from energy_aware_scheduler import run_simulation  # noqa: E402
from energy_broker import EnergyRequest, allocate_all_or_nothing  # noqa: E402
from gen03_control_stub import named_host_scenarios  # noqa: E402
from policy_gated_executor import EnergyState, decide_and_run  # noqa: E402
from task_graph_executor import Task, TaskGraphExecutor  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"


def _agent(name: str):
    def fn(ctx):
        ran = list(ctx.get("ran", []))
        ran.append(name)
        return {"ran": ran, "last_agent": name}

    return fn


def _gas_demo_graph():
    tasks = [
        Task("sense", _agent("sense"), min_joules=0.002, tags=["sense"]),
        Task("infer", _agent("infer"), min_joules=0.009, tags=["infer"], depends_on=["sense"]),
    ]
    tags = {"sense": "sense", "infer": "infer"}
    return TaskGraphExecutor(tasks), tags


def run_gas_preflight_demos():
    """Host-only Model 49 labels. Not a search farm and not a quote status."""
    state = EnergyState(voltage_v=4.6, estimated_joules=0.05)
    graph, tags = _gas_demo_graph()
    ok_cp = decide_and_run(
        graph,
        state,
        task_tags=tags,
        context={"ran": []},
        gas_search={
            "search_table": [{"id": "parent-a", "status": "agreed"}],
            "wake_class": "keep_parent",
        },
    )
    graph_miss, tags_miss = _gas_demo_graph()
    miss_cp = decide_and_run(
        graph_miss,
        state,
        task_tags=tags_miss,
        context={"ran": []},
        gas_search={"search_table": []},
    )
    return {
        "ok_gas_reason": ok_cp.context.get("_gas_reason"),
        "ok_aborted_reason": ok_cp.aborted_reason,
        "missing_table_gas_reason": miss_cp.context.get("_gas_reason"),
        "missing_table_aborted_reason": miss_cp.aborted_reason,
        "note": (
            "Host fixture only. _gas_reason is a research skip label. "
            "It is not a NAS result, not measured joules, and not inquiry_ok."
        ),
    }


def main() -> int:
    pool_j = float(os.environ.get("SANDBOX_POOL_J", "0.12"))
    reserve_j = float(os.environ.get("SANDBOX_RESERVE_J", "0.01"))
    OUT.mkdir(parents=True, exist_ok=True)

    sched_log = run_simulation(steps=8)
    (OUT / "scheduler_tail.json").write_text(
        json.dumps(sched_log[-3:], indent=2),
        encoding="utf-8",
    )

    requests = [
        EnergyRequest("sense", want_j=0.002, priority=1),
        EnergyRequest("infer", want_j=0.009, priority=2),
        EnergyRequest("retrieve", want_j=0.05, priority=2),
        EnergyRequest("generate", want_j=0.40, priority=3),
    ]
    grants = allocate_all_or_nothing(pool_j=pool_j, requests=requests, reserve_j=reserve_j)
    grant_doc = {g.agent_id: g.granted_j for g in grants}
    (OUT / "broker_grants.json").write_text(json.dumps(grant_doc, indent=2), encoding="utf-8")

    graph = TaskGraphExecutor(
        [
            Task("sense", _agent("sense"), min_joules=0.002, tags=["sense"]),
            Task("infer", _agent("infer"), min_joules=0.009, tags=["infer"], depends_on=["sense"]),
            Task("retrieve", _agent("retrieve"), min_joules=0.05, tags=["infer"], depends_on=["infer"]),
            Task("generate", _agent("generate"), min_joules=0.40, tags=["transmit"], depends_on=["retrieve"]),
        ]
    )
    cp = brokered_run(graph, estimated_joules=pool_j, reserve_j=reserve_j, context={"ran": []})
    path = cp.save(OUT / "checkpoint.json")

    gen03_log = named_host_scenarios()
    (OUT / "gen03_decisions.json").write_text(
        json.dumps(gen03_log, indent=2),
        encoding="utf-8",
    )

    gas_demo = run_gas_preflight_demos()
    (OUT / "gas_preflight.json").write_text(json.dumps(gas_demo, indent=2), encoding="utf-8")

    summary = {
        "pool_j": pool_j,
        "reserve_j": reserve_j,
        "completed": cp.completed,
        "skipped": cp.context.get("_broker_skipped"),
        "aborted_reason": cp.aborted_reason,
        "grants_all_or_nothing": grant_doc,
        "brokered_grants": cp.context.get("_broker_grants"),
        "checkpoint": str(path),
        "gen03_decisions": [row["id"] + ":" + row["decision"] for row in gen03_log],
        "_gas_reason_ok": gas_demo["ok_gas_reason"],
        "_gas_reason_missing_table": gas_demo["missing_table_gas_reason"],
        "gas_preflight": gas_demo,
        "note": (
            "Host sandbox only. Placeholder joules. Generate skip under default pool "
            "is expected. Gen03 names are scenario flags, not measured watts. "
            "_gas_reason is a Model 49 research label, not a search farm and not a quote."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
