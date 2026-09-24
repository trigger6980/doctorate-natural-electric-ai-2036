"""Host tests for Model 50 inquiry completeness. Not a sales test."""

from inquiry_completeness import (
    inquiry_ok,
    items_present,
    outline_ready,
    quote_action,
    refuse_reason,
    stamp,
)

COMPLETE = {
    "model_ids": ["01"],
    "license_shape": "identical",
    "deploy_context": "lab replica of public scheduler",
    "energy_honesty": "to-be-measured",
    "scope_table": {"joules": "to-be-measured"},
    "deliverable_shape": "research_replica",
}


def test_complete_packet_may_draft():
    assert items_present(COMPLETE) == 6
    assert refuse_reason(COMPLETE) == "ok"
    assert inquiry_ok(COMPLETE) is True
    assert quote_action(COMPLETE) == "draft"


def test_missing_model_asks():
    packet = dict(COMPLETE)
    packet["model_ids"] = []
    assert inquiry_ok(packet) is False
    assert refuse_reason(packet) == "missing_model"
    assert quote_action(packet) == "ask"


def test_wellbeing_fail_declines():
    packet = dict(COMPLETE)
    packet["wellbeing_ok"] = False
    assert inquiry_ok(packet) is False
    assert refuse_reason(packet) == "wellbeing"
    assert quote_action(packet) == "decline"


def test_bad_shape_is_incomplete():
    packet = dict(COMPLETE)
    packet["license_shape"] = "enterprise-sku"
    assert inquiry_ok(packet) is False
    assert refuse_reason(packet) == "missing_shape"


def test_observer_json_is_not_evidence():
    packet = dict(COMPLETE)
    packet["energy_evidence"] = "energy_observer.json"
    assert inquiry_ok(packet) is False
    assert refuse_reason(packet) == "observer_not_evidence"
    assert quote_action(packet) == "ask"


def test_intended_use_quote_evidence_asks():
    packet = dict(COMPLETE)
    packet["intended_use"] = "quote_evidence"
    assert inquiry_ok(packet) is False
    assert refuse_reason(packet) == "observer_not_evidence"
    assert quote_action(packet) == "ask"


def test_intended_use_discuss_may_draft():
    packet = dict(COMPLETE)
    packet["intended_use"] = "discuss"
    assert inquiry_ok(packet) is True
    assert quote_action(packet) == "draft"


def test_hardware_pending_token_is_not_evidence():
    packet = dict(COMPLETE)
    packet["energy_evidence"] = "hardware_pending"
    assert refuse_reason(packet) == "observer_not_evidence"
    assert quote_action(packet) == "ask"


def test_stamp_complete_discuss():
    packet = dict(COMPLETE)
    packet["intended_use"] = "discuss"
    labeled = stamp(packet)
    assert labeled["items_present"] == 6
    assert labeled["refuse_reason"] == "ok"
    assert labeled["quote_action"] == "draft"
    assert labeled["intended_use"] == "discuss"
    assert labeled["inquiry_ok"] is True
    assert labeled["energy_evidence"] is None
    assert labeled["outline_ready"] is True
    assert labeled["price_allowed"] is False
    assert "commercial_figure_off_repo" in labeled["outline_sections"]


def test_stamp_refuses_observer_evidence():
    packet = dict(COMPLETE)
    packet["energy_evidence"] = "claim_scan"
    packet["intended_use"] = "quote_evidence"
    labeled = stamp(packet)
    assert labeled["refuse_reason"] == "observer_not_evidence"
    assert labeled["quote_action"] == "ask"
    assert labeled["inquiry_ok"] is False
    assert labeled["energy_evidence"] == "claim_scan"
    assert labeled["outline_ready"] is False
    assert labeled["price_allowed"] is False


def test_outline_ready_never_allows_price():
    ready = outline_ready(COMPLETE)
    assert ready["outline_ready"] is True
    assert ready["price_allowed"] is False
    assert ready["quote_action"] == "draft"
    assert len(ready["sections"]) == 10
    blocked = outline_ready({"model_ids": []})
    assert blocked["outline_ready"] is False
    assert blocked["price_allowed"] is False


if __name__ == "__main__":
    test_complete_packet_may_draft()
    test_missing_model_asks()
    test_wellbeing_fail_declines()
    test_bad_shape_is_incomplete()
    test_observer_json_is_not_evidence()
    test_intended_use_quote_evidence_asks()
    test_intended_use_discuss_may_draft()
    test_hardware_pending_token_is_not_evidence()
    test_stamp_complete_discuss()
    test_stamp_refuses_observer_evidence()
    test_outline_ready_never_allows_price()
    print("inquiry_completeness tests passed")
