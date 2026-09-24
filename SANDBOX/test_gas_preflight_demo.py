"""Host tests for the sandbox Model 49 preflight surface."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "SANDBOX"))
sys.path.insert(0, str(ROOT / "AGENTS"))
sys.path.insert(0, str(ROOT / "PROTOTYPES" / "energy-harvester-tinyml" / "src"))

from run_prototypes import run_gas_preflight_demos


def test_ok_and_missing_table_labels():
    demo = run_gas_preflight_demos()
    assert demo["ok_gas_reason"] == "ok"
    assert demo["missing_table_gas_reason"] == "missing_table"
    assert demo["missing_table_aborted_reason"] == "gas_missing_table"
    assert "research skip label" in demo["note"]


if __name__ == "__main__":
    test_ok_and_missing_table_labels()
    print("sandbox gas preflight demo tests passed")
