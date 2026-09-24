"""Host tests for the sandbox inquiry stamp surface."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "SANDBOX"))
sys.path.insert(0, str(ROOT / "AGENTS"))
sys.path.insert(0, str(ROOT / "ENTERPRISE"))

from run_prototypes import run_inquiry_stamp_demo


def test_discuss_may_draft():
    demo = run_inquiry_stamp_demo()
    assert demo["discuss"]["items_present"] == 6
    assert demo["discuss"]["quote_action"] == "draft"
    assert demo["discuss"]["intended_use"] == "discuss"
    assert demo["discuss"]["inquiry_ok"] is True
    assert demo["discuss"]["outline_ready"] is True
    assert demo["discuss"]["price_allowed"] is False
    assert demo["discuss"]["headings_copyable"] is True
    assert demo["discuss"]["fill_on_repo"]["commercial_figure_off_repo"] is False
    assert demo["discuss"]["stamp_invariants_ok"] is True
    assert demo["discuss"]["stamp_invariants"]["ok"] is True
    assert demo["discuss"]["stamp_invariants"]["publish_price"] is False
    assert demo["discuss"]["stamp_invariants"]["covers_outline"] is True
    assert demo["discuss"]["covers_or_idle"] is True
    assert demo["discuss"]["price_verbs_blocked"] is True
    assert demo["discuss"]["next_action"] == "copy_headings"


def test_quote_evidence_asks():
    demo = run_inquiry_stamp_demo()
    refused = demo["refused_quote_evidence"]
    assert refused["refuse_reason"] == "observer_not_evidence"
    assert refused["quote_action"] == "ask"
    assert refused["inquiry_ok"] is False
    assert refused["energy_evidence"] == "claim_scan"
    assert refused["outline_ready"] is False
    assert refused["price_allowed"] is False
    assert refused["headings_copyable"] is False
    assert refused["headings"] == []
    assert refused["fill_on_repo"]["commercial_figure_off_repo"] is False
    assert refused["stamp_invariants_ok"] is True
    assert refused["stamp_invariants"]["covers_outline"] is False
    assert refused["stamp_invariants"]["covers_or_idle"] is True
    assert refused["covers_or_idle"] is True
    assert refused["price_verbs_blocked"] is True
    assert refused["stamp_invariants"]["publish_price"] is False
    assert refused["next_action"] == "ask"


if __name__ == "__main__":
    test_discuss_may_draft()
    test_quote_evidence_asks()
    print("sandbox inquiry stamp demo tests passed")
