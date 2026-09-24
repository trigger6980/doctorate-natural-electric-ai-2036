"""Tests for policy-gated task-graph execution."""

from task_graph_executor import Task, TaskGraphExecutor
from policy_gated_executor import (
    Action,
    EnergyState,
    PolicyConfig,
    decide_and_run,
    simple_threshold_policy,
)


def _graph():
    def sense(ctx):
        return {"sensed": True}

    def infer(ctx):
        return {"inferred": True}

    def tx(ctx):
        return {"sent": True}

    tasks = [
        Task("sense", sense, min_joules=0.002),
        Task("infer", infer, min_joules=0.009, depends_on=["sense"]),
        Task("tx", tx, min_joules=0.05, depends_on=["infer"]),
    ]
    tags = {"sense": "sense", "infer": "infer", "tx": "transmit"}
    return TaskGraphExecutor(tasks), tags


def test_sleep_refuses_graph():
    ex, tags = _graph()
    state = EnergyState(voltage_v=3.0, estimated_joules=1.0)
    cp = decide_and_run(ex, state, task_tags=tags)
    assert cp.aborted_reason == "policy_sleep"
    assert cp.completed == []


def test_sense_only_runs_sense():
    ex, tags = _graph()
    state = EnergyState(voltage_v=3.5, estimated_joules=0.003)
    cp = decide_and_run(ex, state, task_tags=tags)
    assert cp.context["_policy_action"] == "SENSE"
    assert "sense" in cp.completed
    assert "infer" not in cp.completed


def test_high_energy_can_transmit():
    ex, tags = _graph()
    state = EnergyState(voltage_v=4.6, estimated_joules=1.0)
    cp = decide_and_run(ex, state, task_tags=tags)
    assert cp.context["_policy_action"] == "TRANSMIT"
    assert set(cp.completed) == {"sense", "infer", "tx"}


def test_custom_policy_callable():
    def always_sleep(state, cfg):
        return Action.SLEEP

    ex, tags = _graph()
    state = EnergyState(voltage_v=5.0, estimated_joules=10.0)
    cp = decide_and_run(ex, state, policy_fn=always_sleep, task_tags=tags)
    assert cp.aborted_reason == "policy_sleep"


def test_default_policy_matches_thresholds():
    cfg = PolicyConfig()
    assert simple_threshold_policy(EnergyState(3.0, 1.0), cfg) is Action.SLEEP
    assert simple_threshold_policy(EnergyState(3.5, 0.003), cfg) is Action.SENSE


def test_gas_preflight_missing_table_skips_before_policy():
    ex, tags = _graph()
    state = EnergyState(voltage_v=4.6, estimated_joules=1.0)
    cp = decide_and_run(
        ex,
        state,
        task_tags=tags,
        gas_search={"search_table": []},
    )
    assert cp.aborted_reason == "gas_missing_table"
    assert cp.context["_gas_reason"] == "missing_table"
    assert cp.completed == []
    assert "_policy_action" not in cp.context


def test_gas_preflight_ok_does_not_block_policy():
    ex, tags = _graph()
    state = EnergyState(voltage_v=4.6, estimated_joules=1.0)
    table = [{"id": "parent-a", "status": "agreed"}]
    cp = decide_and_run(
        ex,
        state,
        task_tags=tags,
        gas_search={"search_table": table, "wake_class": "keep_parent"},
    )
    assert cp.aborted_reason is None or not str(cp.aborted_reason).startswith("gas_")
    assert cp.context.get("_gas_reason") == "ok"
    assert set(cp.completed) == {"sense", "infer", "tx"}


def test_gas_unmeasured_hold_mismatch():
    ex, tags = _graph()
    state = EnergyState(voltage_v=4.6, estimated_joules=1.0)
    table = [{"id": "child-b", "status": "to-be-measured", "hold_id": "hold-gas-1"}]
    cp = decide_and_run(
        ex,
        state,
        task_tags=tags,
        gas_search={"search_table": table, "hold_gas": "hold-other"},
    )
    assert cp.aborted_reason == "gas_unmeasured"
    assert cp.context["_gas_action"] == "hold"


if __name__ == "__main__":
    test_sleep_refuses_graph()
    test_sense_only_runs_sense()
    test_high_energy_can_transmit()
    test_custom_policy_callable()
    test_default_policy_matches_thresholds()
    test_gas_preflight_missing_table_skips_before_policy()
    test_gas_preflight_ok_does_not_block_policy()
    test_gas_unmeasured_hold_mismatch()
    print("policy_gated_executor tests passed")
