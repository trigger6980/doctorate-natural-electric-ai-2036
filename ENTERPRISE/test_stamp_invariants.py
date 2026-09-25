"""Host tests for stamp_invariants. Not a sales test."""

from inquiry_completeness import (
    ACTION_ASK,
    ACTION_COPY_HEADINGS,
    ACTION_DECLINE,
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


def test_stamp_invariants_ready_and_idle():
    ready = stamp_invariants(COMPLETE)
    assert ready["ok"] is True
    assert ready["action_consistent"] is True
    assert ready["exactly_one"] is True
    assert ready["partition_disjoint"] is True
    assert ready["covers_outline"] is True
    assert ready["covers_or_idle"] is True
    assert ready["sums_to_known"] is True
    assert ready["commercial_lane_sealed"] is True
    assert ready["lane_fill_aligned"] is True
    assert ready["publish_price"] is False
    assert ready["price_allowed"] is False
    missing = stamp_invariants({"model_ids": []})
    assert missing["ok"] is True
    assert missing["covers_outline"] is False
    assert missing["covers_or_idle"] is True
    assert missing["commercial_lane_sealed"] is True
    assert missing["lane_fill_aligned"] is True
    harm = dict(COMPLETE)
    harm["wellbeing_ok"] = False
    declined = stamp_invariants(harm)
    assert declined["ok"] is True
    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    asked = stamp_invariants(refused)
    assert asked["ok"] is True
    labeled = stamp(COMPLETE)
    assert labeled["stamp_invariants_ok"] is True
    assert labeled["stamp_invariants"]["ok"] is True
    assert labeled["stamp_invariants"]["publish_price"] is False
    assert labeled["commercial_lane_sealed"] is True
    assert labeled["lane_fill_aligned"] is True
    assert labeled["action_flag_verb"] == ACTION_COPY_HEADINGS
    idle = stamp(refused)
    assert idle["stamp_invariants_ok"] is True
    assert idle["action_flag_verb"] == ACTION_ASK
    harm_stamp = stamp(harm)
    assert harm_stamp["stamp_invariants_ok"] is True
    assert harm_stamp["next_action"] == ACTION_DECLINE


if __name__ == "__main__":
    test_stamp_invariants_ready_and_idle()
    print("stamp_invariants tests passed")
