"""Tests for Model 11 host energy broker. Run with: python -m pytest AGENTS/"""

from energy_broker import (
    EnergyRequest,
    allocate,
    allocate_all_or_nothing,
    estimate_broker_cost_j,
)


def test_refuses_when_pool_is_only_reserve():
    grants = allocate(
        pool_j=0.05,
        requests=[EnergyRequest("a", want_j=0.04, priority=1)],
        reserve_j=0.05,
    )
    assert grants[0].granted_j == 0.0


def test_never_over_allocates():
    grants = allocate(
        pool_j=0.10,
        requests=[
            EnergyRequest("a", want_j=0.08, priority=2),
            EnergyRequest("b", want_j=0.08, priority=1),
        ],
        reserve_j=0.02,
    )
    total = sum(g.granted_j for g in grants)
    assert total <= 0.08 + 1e-12
    assert grants[0].granted_j == 0.08
    assert grants[1].granted_j == 0.0


def test_equal_priority_keeps_request_order():
    grants = allocate(
        pool_j=0.05,
        requests=[
            EnergyRequest("first", want_j=0.05, priority=0),
            EnergyRequest("second", want_j=0.05, priority=0),
        ],
        reserve_j=0.0,
    )
    assert grants[0].granted_j == 0.05
    assert grants[1].granted_j == 0.0


def test_all_or_nothing_does_not_starve_cheap_agent():
    grants = allocate_all_or_nothing(
        pool_j=0.05,
        requests=[
            EnergyRequest("expensive", want_j=0.20, priority=2),
            EnergyRequest("cheap", want_j=0.01, priority=1),
        ],
        reserve_j=0.0,
    )
    by_id = {g.agent_id: g.granted_j for g in grants}
    assert by_id["expensive"] == 0.0
    assert by_id["cheap"] == 0.01


def test_estimate_cost_scales_with_n():
    assert estimate_broker_cost_j(0) == 0.0
    assert estimate_broker_cost_j(4) == 0.0008


if __name__ == "__main__":
    test_refuses_when_pool_is_only_reserve()
    test_never_over_allocates()
    test_equal_priority_keeps_request_order()
    test_all_or_nothing_does_not_starve_cheap_agent()
    test_estimate_cost_scales_with_n()
    print("energy broker tests passed.")
