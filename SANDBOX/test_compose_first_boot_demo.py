"""Host tests for compose_first_boot_demo. Not a hardware certificate."""

from compose_first_boot_demo import compose_first_boot, demo_rows


def test_below_floor_refuses_and_leaves_joules_unset_without_c():
    rec = compose_first_boot(3.2, infer_requested=True)
    assert rec["duty"] == "REFUSE"
    assert rec["inference_allowed"] is False
    assert rec["workload"] is None
    assert rec["estimated_joules"] is None
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False
    assert rec["source"] == "host_compose_first_boot"


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
    assert len(rows) >= 3
    for r in rows:
        assert r["is_field_measurement"] is False
        assert r["is_firmware"] is False


if __name__ == "__main__":
    test_below_floor_refuses_and_leaves_joules_unset_without_c()
    test_above_floor_with_c_attaches_analytic_joules()
    test_listen_only_no_workload_even_with_c()
    test_demo_rows_are_host_only()
    print("test_compose_first_boot_demo: ok")
