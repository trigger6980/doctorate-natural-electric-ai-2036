"""Host tests for first_boot refuse sketch. Not a hardware certificate."""

from first_boot import PRIMARY_WORKLOAD, first_boot


def test_below_floor_refuses_inference():
    rec = first_boot(3.2, infer_requested=True)
    assert rec["duty"] == "REFUSE"
    assert rec["policy_action"] == "SLEEP"
    assert rec["inference_allowed"] is False
    assert rec["workload"] is None
    assert rec["is_field_measurement"] is False


def test_above_floor_allows_tinyml_primary():
    rec = first_boot(3.8, infer_requested=True, allow_secondary_llm=False)
    assert rec["duty"] == "INFER"
    assert rec["inference_allowed"] is True
    assert rec["workload"] == PRIMARY_WORKLOAD


def test_listen_only_does_not_claim_workload():
    rec = first_boot(3.8, infer_requested=False)
    assert rec["duty"] == "IDLE_LISTEN"
    assert rec["workload"] is None
