"""Host tests for Model 49 fixture table. Not a NAS test."""

from gas_search_gate import gas_action, gas_ok, refuse_reason

CHARGED = {"rail_voltage_v": 4.8}
SLEEPY = {"rail_voltage_v": 2.9}

AGREED = [{"id": "parent-a", "status": "agreed"}]
UNMEASURED = [{"id": "child-b", "status": "to-be-measured"}]
HELD = [{"id": "child-b", "status": "to-be-measured", "hold_id": "hold-gas-1"}]
AIRGAP = [{"id": "pull-c", "status": "agreed", "needs_outbound_dataset": True}]


def test_agreed_table_ok():
    assert refuse_reason(CHARGED, AGREED) == "ok"
    assert gas_ok(CHARGED, AGREED) is True
    assert gas_action(CHARGED, AGREED, wake_class="keep_parent") == "keep_parent"


def test_missing_table_refuses():
    assert refuse_reason(CHARGED, None) == "missing_table"
    assert gas_ok(CHARGED, []) is False


def test_unmeasured_without_hold_refuses():
    assert refuse_reason(CHARGED, UNMEASURED) == "no_hold"
    assert gas_ok(CHARGED, UNMEASURED, hold_gas="hold-gas-1") is True
    assert refuse_reason(CHARGED, HELD, hold_gas="hold-other") == "unmeasured"


def test_low_rail_defers():
    assert refuse_reason(SLEEPY, AGREED) == "energy"
    assert gas_action(SLEEPY, AGREED, wake_class="mutate") == "defer"


def test_optional_upstream_gates():
    assert refuse_reason(CHARGED, AGREED, energy_grant_ok=False) == "grant"
    assert refuse_reason(CHARGED, AGREED, scr_ok=False) == "slot"
    assert refuse_reason(CHARGED, AGREED, airgap_required=True) == "ok"
    assert refuse_reason(CHARGED, AIRGAP, airgap_required=True) == "airgap"


def test_unknown_wake_skips():
    assert refuse_reason(CHARGED, AGREED, wake_class="evolve-farm") == "unknown"
    assert gas_action(CHARGED, AGREED, wake_class="evolve-farm") == "unknown"


if __name__ == "__main__":
    test_agreed_table_ok()
    test_missing_table_refuses()
    test_unmeasured_without_hold_refuses()
    test_low_rail_defers()
    test_optional_upstream_gates()
    test_unknown_wake_skips()
    print("gas_search_gate tests passed")
