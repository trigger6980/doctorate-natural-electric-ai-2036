"""Tests for Model 11 ↔ task-graph wiring."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from brokered_executor import brokered_run
from task_graph_executor import Task, TaskGraphExecutor


def _mark(name):
    def fn(ctx):
        ctx.setdefault("ran", []).append(name)
        return {"ran": ctx["ran"]}

    return fn


def test_grant_before_run_skips_ungranted():
    graph = TaskGraphExecutor(
        [
            Task("sense", _mark("sense"), min_joules=0.01, tags=["sense"]),
            Task("infer", _mark("infer"), min_joules=0.20, tags=["infer"]),
        ]
    )
    cp = brokered_run(graph, estimated_joules=0.05, reserve_j=0.0)
    assert "sense" in cp.completed
    assert "infer" not in cp.completed
    assert cp.context["_broker_grants"]["infer"] == 0.0
    assert "infer" in cp.context["_broker_skipped"]


def test_reserve_can_refuse_everyone():
    graph = TaskGraphExecutor(
        [Task("infer", _mark("infer"), min_joules=0.05, tags=["infer"])]
    )
    cp = brokered_run(graph, estimated_joules=0.05, reserve_j=0.05)
    assert cp.completed == []
    assert cp.aborted_reason == "broker_refused_all"


def test_priority_prefers_transmit():
    graph = TaskGraphExecutor(
        [
            Task("infer", _mark("infer"), min_joules=0.08, tags=["infer"]),
            Task("tx", _mark("tx"), min_joules=0.08, tags=["transmit"]),
        ]
    )
    cp = brokered_run(graph, estimated_joules=0.08, reserve_j=0.0)
    assert cp.completed == ["tx"]
    assert "infer" in cp.context["_broker_skipped"]


if __name__ == "__main__":
    test_grant_before_run_skips_ungranted()
    test_reserve_can_refuse_everyone()
    test_priority_prefers_transmit()
    print("brokered executor tests passed.")
