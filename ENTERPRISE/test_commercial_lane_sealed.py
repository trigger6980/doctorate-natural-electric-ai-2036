"""Host tests for commercial_lane_sealed. Not a sales test."""

from inquiry_completeness import (
    COMMERCIAL_KEY,
    LANE_NOT_READY,
    LANE_OFF_REPO,
    LANE_PUBLIC,
    commercial_lane_sealed,
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


def test_commercial_lane_sealed_ready_and_idle():
    ready = commercial_lane_sealed(COMPLETE)
    assert ready["ok"] is True
    assert ready["key"] == COMMERCIAL_KEY
    assert ready["lane"] == LANE_OFF_REPO
    assert ready["expected_lane"] == LANE_OFF_REPO
    assert ready["never_public_fill"] is True
    assert ready["on_repo_value"] is None
    assert ready["price_allowed"] is False
    assert ready["publish_price"] is False
    assert ready["lane"] != LANE_PUBLIC

    idle = commercial_lane_sealed({"model_ids": []})
    assert idle["ok"] is True
    assert idle["lane"] == LANE_NOT_READY
    assert idle["expected_lane"] == LANE_NOT_READY
    assert idle["never_public_fill"] is True
    assert idle["on_repo_value"] is None

    labeled = stamp(COMPLETE)
    assert labeled["commercial_lane_sealed"] is True
    assert labeled["commercial_lane"]["lane"] == LANE_OFF_REPO
    assert labeled["stamp_invariants"]["commercial_lane_sealed"] is True
    assert COMMERCIAL_KEY not in labeled["public_fill_keys"]
    assert stamp_invariants(COMPLETE)["ok"] is True

    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    idle_stamp = stamp(refused)
    assert idle_stamp["commercial_lane_sealed"] is True
    assert idle_stamp["commercial_lane"]["lane"] == LANE_NOT_READY
    assert idle_stamp["off_repo_keys"] == []


if __name__ == "__main__":
    test_commercial_lane_sealed_ready_and_idle()
    print("commercial_lane_sealed tests passed")
