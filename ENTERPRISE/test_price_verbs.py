"""Host tests for price_verbs_blocked. Not a sales test."""

from inquiry_completeness import (
    ACTION_ASK,
    ACTION_COPY_HEADINGS,
    ACTION_DECLINE,
    price_verbs_blocked,
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


def test_price_verbs_blocked_on_ready_ask_decline():
    ready = price_verbs_blocked(COMPLETE)
    assert ready["ok"] is True
    assert ready["verb"] == ACTION_COPY_HEADINGS
    assert ready["publish_price"] is False
    assert ready["price_allowed"] is False
    assert "publish_price" in ready["blocked_verbs"]
    assert ACTION_COPY_HEADINGS in ready["allowed_verbs"]

    asked = price_verbs_blocked({"model_ids": []})
    assert asked["ok"] is True
    assert asked["verb"] == ACTION_ASK

    harm = dict(COMPLETE)
    harm["wellbeing_ok"] = False
    declined = price_verbs_blocked(harm)
    assert declined["ok"] is True
    assert declined["verb"] == ACTION_DECLINE

    labeled = stamp(COMPLETE)
    assert labeled["price_verbs_blocked"] is True
    assert labeled["covers_or_idle"] is True
    assert labeled["price_verbs"]["ok"] is True
    assert labeled["stamp_invariants"]["price_verbs_blocked"] is True

    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    idle = stamp(refused)
    assert idle["covers_or_idle"] is True
    assert idle["partition_covers_outline"] is False
    assert idle["price_verbs_blocked"] is True
    assert stamp_invariants(refused)["price_verbs_blocked"] is True


if __name__ == "__main__":
    test_price_verbs_blocked_on_ready_ask_decline()
    print("price_verbs_blocked tests passed")
