"""Host tests for compose_first_boot_demo. Not a hardware certificate."""

from compose_first_boot_demo import compose_first_boot, demo_rows
from host_voltage_reader import READER_META_KEYS


def test_below_floor_refuses_and_leaves_joules_unset_without_c():
    rec = compose_first_boot(3.2, infer_requested=True)
    assert rec["duty"] == "REFUSE"
    assert rec["inference_allowed"] is False
    assert rec["workload"] is None
    assert rec["estimated_joules"] is None
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False
    assert rec["source"] == "host_compose_first_boot"
    assert rec["via_host_reader"] is False


def test_above_floor_with_c_attaches_analytic_joules():
    rec = compose_first_boot(3.8, infer_requested=True, C_farads=1.0)
    assert rec["duty"] == "INFER"
    assert rec["inference_allowed"] is True
    assert rec["workload"] == "tinyml_policy"
    assert rec["estimated_joules"] is not None
    assert rec["estimated_joules"] > 0.0
    assert rec["C_farads_used"] == 1.0
    assert "caller-supplied" in rec["joules_note"]


def test_listen_only_no_workload_even_with_c():
    rec = compose_first_boot(3.8, infer_requested=False, C_farads=1.0)
    assert rec["duty"] == "IDLE_LISTEN"
    assert rec["workload"] is None
    assert rec["estimated_joules"] is not None


def test_demo_rows_are_host_only():
    rows = demo_rows()
    assert len(rows) >= 5
    for r in rows:
        assert r["is_field_measurement"] is False
        assert r["is_firmware"] is False


def test_via_host_reader_below_floor():
    rec = compose_first_boot(
        3.2,
        infer_requested=True,
        via_host_reader=True,
        reader_source="host_placeholder",
    )
    assert rec["via_host_reader"] is True
    assert rec["reader_source"] == "host_placeholder"
    assert rec["reader_is_field_measurement"] is False
    assert rec["reader_is_firmware"] is False
    # Contract: reader meta keys are exactly the documented set (third call site).
    reader_keys = {k for k in rec if k.startswith("reader_")}
    assert reader_keys == READER_META_KEYS
    assert rec["duty"] == "REFUSE"
    assert rec["inference_allowed"] is False
    assert rec["is_field_measurement"] is False


def test_via_host_reader_with_c_and_hardware_pending():
    rec = compose_first_boot(
        3.8,
        infer_requested=True,
        C_farads=1.0,
        via_host_reader=True,
        reader_source="hardware_pending",
    )
    assert rec["via_host_reader"] is True
    assert rec["reader_source"] == "hardware_pending"
    assert rec["duty"] == "INFER"
    assert rec["estimated_joules"] is not None
    assert rec["is_field_measurement"] is False
    assert rec["reader_is_field_measurement"] is False
    reader_keys = {k for k in rec if k.startswith("reader_")}
    assert reader_keys == READER_META_KEYS


if __name__ == "__main__":
    test_below_floor_refuses_and_leaves_joules_unset_without_c()
    test_above_floor_with_c_attaches_analytic_joules()
    test_listen_only_no_workload_even_with_c()
    test_demo_rows_are_host_only()
    test_via_host_reader_below_floor()
    test_via_host_reader_with_c_and_hardware_pending()
    print("test_compose_first_boot_demo: ok")
