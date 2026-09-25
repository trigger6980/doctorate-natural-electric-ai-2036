"""Host tests for lane_fill_aligned. Not a sales test."""

from inquiry_completeness import (
    COMMERCIAL_KEY,
    LANE_NOT_READY,
    LANE_OFF_REPO,
    LANE_PUBLIC,
    lane_fill_aligned,
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


def test_lane_fill_aligned_ready_and_idle():
    ready = lane_fill_aligned(COMPLETE)
    assert ready["ok"] is True
    assert ready["mismatches"] == []
    assert ready["commercial_fill"] is False
    assert ready["commercial_lane"] == LANE_OFF_REPO
    assert ready["price_allowed"] is False
    assert ready["publish_price"] is False
    assert ready["commercial_lane"] != LANE_PUBLIC

    idle = lane_fill_aligned({"model_ids": []})
    assert idle["ok"] is True
    assert idle["mismatches"] == []
    assert idle["commercial_fill"] is False
    assert idle["commercial_lane"] == LANE_NOT_READY

    labeled = stamp(COMPLETE)
    assert labeled["lane_fill_aligned"] is True
    assert labeled["lane_fill"]["ok"] is True
    assert labeled["stamp_invariants"]["lane_fill_aligned"] is True
    assert labeled["fill_on_repo"][COMMERCIAL_KEY] is False
    assert stamp_invariants(COMPLETE)["ok"] is True

    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    idle_stamp = stamp(refused)
    assert idle_stamp["lane_fill_aligned"] is True
    assert idle_stamp["lane_fill"]["commercial_lane"] == LANE_NOT_READY
    assert idle_stamp["public_fill_keys"] == []


if __name__ == "__main__":
    test_lane_fill_aligned_ready_and_idle()
    print("lane_fill_aligned tests passed")
