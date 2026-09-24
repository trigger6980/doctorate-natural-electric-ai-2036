"""Host tests for action_consistent. Not a sales test."""

from inquiry_completeness import (
    ACTION_ASK,
    ACTION_COPY_HEADINGS,
    ACTION_DECLINE,
    action_consistent,
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


def test_action_consistent_matches_verb_and_flag():
    ready = action_consistent(COMPLETE)
    assert ready["match"] is True
    assert ready["verb"] == ACTION_COPY_HEADINGS
    assert ready["flag_verb"] == ACTION_COPY_HEADINGS
    assert ready["exactly_one"] is True
    assert ready["publish_price"] is False
    assert ready["price_allowed"] is False
    missing = action_consistent({"model_ids": []})
    assert missing["match"] is True
    assert missing["verb"] == ACTION_ASK
    assert missing["flag_verb"] == ACTION_ASK
    harm = dict(COMPLETE)
    harm["wellbeing_ok"] = False
    declined = action_consistent(harm)
    assert declined["match"] is True
    assert declined["verb"] == ACTION_DECLINE
    assert declined["flag_verb"] == ACTION_DECLINE
    refused = dict(COMPLETE)
    refused["intended_use"] = "quote_evidence"
    asked = action_consistent(refused)
    assert asked["match"] is True
    assert asked["verb"] == ACTION_ASK
    labeled = stamp(COMPLETE)
    assert labeled["action_consistent"] is True
    assert labeled["action_flag_verb"] == ACTION_COPY_HEADINGS
    idle = stamp(refused)
    assert idle["action_consistent"] is True
    assert idle["action_flag_verb"] == ACTION_ASK


if __name__ == "__main__":
    test_action_consistent_matches_verb_and_flag()
    print("action_consistent tests passed")
