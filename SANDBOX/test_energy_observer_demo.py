"""Host tests for the sandbox energy observer surface."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "SANDBOX"))
sys.path.insert(0, str(ROOT / "AGENTS"))

from run_prototypes import run_observer_demo


def test_observer_labels_are_not_field():
    demo = run_observer_demo()
    assert demo["placeholder"]["source"] == "host_placeholder"
    assert demo["placeholder"]["is_field_measurement"] is False
    assert demo["hardware_pending"]["source"] == "hardware_pending"
    assert demo["hardware_pending"]["is_field_measurement"] is False
    assert "is_field_measurement is always false" in demo["note"]


def test_observer_claim_scan_refuses_quote():
    demo = run_observer_demo()
    assert demo["placeholder"]["claims"]["host_log"] == "ok"
    assert demo["placeholder"]["claims"]["quote_evidence"] == "observer_not_evidence"
    assert demo["claim_scan"]["sandbox_demo"] == "ok"
    assert demo["claim_scan"]["result_record"] == "observer_not_evidence"
    assert demo["claim_scan"]["field_generation"] == "observer_not_evidence"


if __name__ == "__main__":
    test_observer_labels_are_not_field()
    test_observer_claim_scan_refuses_quote()
    print("sandbox energy observer demo tests passed")
