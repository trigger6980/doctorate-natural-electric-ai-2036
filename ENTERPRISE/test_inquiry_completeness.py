"""Host tests for Model 50 inquiry completeness. Not a sales test."""

from inquiry_completeness import (
    OUTLINE_SECTIONS,
    copy_headings,
    inquiry_ok,
    items_present,
    off_repo_keys,
    outline_ready,
    partition_keys,
    public_fill_keys,
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
    assert labeled["headings_copyable"] is True
    assert labeled["headings"] == labeled["outline_sections"]
    assert labeled["fill_on_repo"]["commercial_figure_off_repo"] is False
    assert labeled["fill_on_repo"]["who_measures_joules"] is True
    assert "commercial_figure_off_repo" not in labeled["public_fill_keys"]
    assert "who_measures_joules" in labeled["public_fill_keys"]
    assert len(labeled["public_fill_keys"]) == 9
    assert labeled["off_repo_keys"] == ["commercial_figure_off_repo"]
    assert labeled["partition_disjoint"] is True
    assert labeled["partition_covers_outline"] is True


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
    assert labeled["headings_copyable"] is False
    assert labeled["headings"] == []
    assert labeled["fill_on_repo"]["who_measures_joules"] is False
    assert labeled["fill_on_repo"]["commercial_figure_off_repo"] is False
    assert labeled["public_fill_keys"] == []
    assert labeled["off_repo_keys"] == []
    assert labeled["partition_disjoint"] is True
    assert labeled["partition_covers_outline"] is False


def test_outline_ready_never_allows_price():
    ready = outline_ready(COMPLETE)
    assert ready["outline_ready"] is True
    assert ready["price_allowed"] is False
    assert ready["quote_action"] == "draft"
    assert len(ready["sections"]) == 10
    blocked = outline_ready({"model_ids": []})
    assert blocked["outline_ready"] is False
    assert blocked["price_allowed"] is False


def test_copy_headings_never_fills_price_on_repo():
    copied = copy_headings(COMPLETE)
    assert copied["headings_copyable"] is True
    assert copied["price_allowed"] is False
    assert copied["fill_on_repo"]["commercial_figure_off_repo"] is False
    assert all(
        copied["fill_on_repo"][key] is True
        for key in copied["headings"]
        if key != "commercial_figure_off_repo"
    )
    blocked = copy_headings({"model_ids": []})
    assert blocked["headings_copyable"] is False
    assert blocked["headings"] == []
    assert blocked["price_allowed"] is False
    assert blocked["fill_on_repo"]["commercial_figure_off_repo"] is False


def test_public_fill_keys_excludes_commercial_figure():
    keys = public_fill_keys(COMPLETE)
    assert "commercial_figure_off_repo" not in keys
    assert "parties_and_date" in keys
    assert "who_measures_joules" in keys
    assert "what_stays_public" in keys
    assert len(keys) == 9
    blocked = public_fill_keys({"model_ids": []})
    assert blocked == []


def test_off_repo_keys_only_when_ready():
    keys = off_repo_keys(COMPLETE)
    assert keys == ["commercial_figure_off_repo"]
    assert set(keys).isdisjoint(public_fill_keys(COMPLETE))
    blocked = off_repo_keys({"model_ids": []})
    assert blocked == []


def test_partition_keys_ready_covers_and_stays_disjoint():
    part = partition_keys(COMPLETE)
    assert part["outline_ready"] is True
    assert part["price_allowed"] is False
    assert part["disjoint"] is True
    assert part["covers_outline"] is True
    assert part["off_repo_keys"] == ["commercial_figure_off_repo"]
    assert "commercial_figure_off_repo" not in part["public_fill_keys"]
    assert set(part["public_fill_keys"]) | set(part["off_repo_keys"]) == set(
        OUTLINE_SECTIONS
    )
    blocked = partition_keys({"model_ids": []})
    assert blocked["outline_ready"] is False
    assert blocked["public_fill_keys"] == []
    assert blocked["off_repo_keys"] == []
    assert blocked["disjoint"] is True
    assert blocked["covers_outline"] is False
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
    test_copy_headings_never_fills_price_on_repo()
    test_public_fill_keys_excludes_commercial_figure()
    test_off_repo_keys_only_when_ready()
    test_partition_keys_ready_covers_and_stays_disjoint()
    print("inquiry_completeness tests passed")
