"""Host tests for Model 50 inquiry completeness. Not a sales test."""

from inquiry_completeness import inquiry_ok, items_present, quote_action, refuse_reason

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


if __name__ == "__main__":
    test_complete_packet_may_draft()
    test_missing_model_asks()
    test_wellbeing_fail_declines()
    test_bad_shape_is_incomplete()
    test_observer_json_is_not_evidence()
    test_intended_use_quote_evidence_asks()
    test_intended_use_discuss_may_draft()
    test_hardware_pending_token_is_not_evidence()
    print("inquiry_completeness tests passed")
