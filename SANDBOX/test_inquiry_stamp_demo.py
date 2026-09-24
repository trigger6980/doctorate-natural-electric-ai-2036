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


def test_quote_evidence_asks():
    demo = run_inquiry_stamp_demo()
    refused = demo["refused_quote_evidence"]
    assert refused["refuse_reason"] == "observer_not_evidence"
    assert refused["quote_action"] == "ask"
    assert refused["inquiry_ok"] is False
    assert refused["energy_evidence"] == "claim_scan"
    assert refused["outline_ready"] is False
    assert refused["price_allowed"] is False


if __name__ == "__main__":
    test_discuss_may_draft()
    test_quote_evidence_asks()
    print("sandbox inquiry stamp demo tests passed")
