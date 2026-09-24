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


if __name__ == "__main__":
    test_observer_labels_are_not_field()
    print("sandbox energy observer demo tests passed")
