"""Tests for the Operator AI task-graph executor skeleton.

Run from repo root:
    python -m pytest AGENTS/test_task_graph_executor.py -q
or:
    python AGENTS/test_task_graph_executor.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from task_graph_executor import Task, TaskGraphExecutor


def _inc(ctx):
    return {"n": ctx.get("n", 0) + 1}


def _double(ctx):
    return {"n": ctx.get("n", 0) * 2}


def test_runs_in_dependency_order():
    graph = TaskGraphExecutor(
        [
            Task("inc", _inc, min_joules=0.001),
            Task("double", _double, min_joules=0.001, depends_on=["inc"]),
        ]
    )
    cp = graph.run(estimated_joules=1.0, context={"n": 1})
    assert cp.completed == ["inc", "double"]
    assert cp.context["n"] == 4
    assert cp.aborted_reason is None


def test_energy_gate_stops_expensive_task():
    graph = TaskGraphExecutor(
        [
            Task("cheap", _inc, min_joules=0.001),
            Task("expensive", _double, min_joules=1.0, depends_on=["cheap"]),
        ]
    )
    cp = graph.run(estimated_joules=0.01, context={"n": 0})
    assert cp.completed == ["cheap"]
    assert cp.aborted_reason is not None
    assert cp.aborted_reason.startswith("energy_gate:expensive")


def test_resume_from_checkpoint():
    graph = TaskGraphExecutor(
        [
            Task("inc", _inc, min_joules=0.001),
            Task("double", _double, min_joules=0.001, depends_on=["inc"]),
        ]
    )
    first = graph.run(estimated_joules=0.0015, context={"n": 1})
    assert first.completed == ["inc"]
    second = graph.run(estimated_joules=1.0, checkpoint=first)
    assert second.completed == ["inc", "double"]
    assert second.context["n"] == 4


def test_unknown_dependency_raises():
    try:
        TaskGraphExecutor([Task("a", _inc, depends_on=["missing"])])
    except ValueError as exc:
        assert "missing" in str(exc)
    else:
        raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_runs_in_dependency_order()
    test_energy_gate_stops_expensive_task()
    test_resume_from_checkpoint()
    test_unknown_dependency_raises()
    print("All task-graph executor tests passed.")
