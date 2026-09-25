"""Host tests for commercial_figure_blank. Not a sales test."""

from inquiry_completeness import (
    COMMERCIAL_KEY,
    commercial_figure_blank,
    stamp,
    stamp_invariants,
)

COMPLETE = {
    "model_ids": ["01"],
    "license_shape": "identical",
    "deploy_context": "lab replica of public scheduler",
    "energy_honesty": "to-be-measured",
    "scope_table": {"joules": "to-be-measured"},
    "deliverable_shape": "research_replica",
}


def test_commercial_figure_blank_ready_and_idle():
    ready = commercial_figure_blank(COMPLETE)
    assert ready["ok"] is True
    assert ready["key"] == COMMERCIAL_KEY
    assert ready["on_repo_value"] is None
    assert ready["fill_on_repo"] is False
    assert ready["off_repo_when_ready"] is True
    assert ready["price_allowed"] is False
    assert ready["publish_price"] is False

    idle = commercial_figure_blank({"model_ids": []})
    assert idle["ok"] is True
    assert idle["on_repo_value"] is None
    assert idle["off_repo_when_ready"] is False
    assert idle["outline_ready"] is False

    labeled = stamp(COMPLETE)
    assert labeled["commercial_figure_blank"] is True
    assert labeled["commercial_figure"]["on_repo_value"] is None
    assert labeled["stamp_invariants"]["commercial_figure_blank"] is True
    assert COMMERCIAL_KEY not in labeled["public_fill_keys"]
    assert stamp_invariants(COMPLETE)["ok"] is True

    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    idle_stamp = stamp(refused)
    assert idle_stamp["commercial_figure_blank"] is True
    assert idle_stamp["commercial_figure"]["on_repo_value"] is None
    assert idle_stamp["off_repo_keys"] == []


if __name__ == "__main__":
    test_commercial_figure_blank_ready_and_idle()
    print("commercial_figure_blank tests passed")
