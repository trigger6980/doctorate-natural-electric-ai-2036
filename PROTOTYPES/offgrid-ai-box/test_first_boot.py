"""Host tests for first_boot refuse sketch. Not a hardware certificate."""

from first_boot import PRIMARY_WORKLOAD, first_boot
from energy_duty import FLOOR_VOLTS


def test_below_floor_refuses_inference():
    rec = first_boot(3.2, infer_requested=True)
    assert rec["duty"] == "REFUSE"
    assert rec["policy_action"] == "SLEEP"
    assert rec["inference_allowed"] is False
    assert rec["workload"] is None
    assert rec["is_field_measurement"] is False
    assert rec["via_host_reader"] is False


def test_above_floor_allows_tinyml_primary():
    rec = first_boot(3.8, infer_requested=True, allow_secondary_llm=False)
    assert rec["duty"] == "INFER"
    assert rec["inference_allowed"] is True
    assert rec["workload"] == PRIMARY_WORKLOAD
    assert rec["via_host_reader"] is False


def test_listen_only_does_not_claim_workload():
    rec = first_boot(3.8, infer_requested=False)
    assert rec["duty"] == "IDLE_LISTEN"
    assert rec["workload"] is None


def test_via_host_reader_below_floor_host_placeholder():
    rec = first_boot(
        FLOOR_VOLTS - 0.2,
        infer_requested=True,
        via_host_reader=True,
        reader_source="host_placeholder",
    )
    assert rec["via_host_reader"] is True
    assert rec["reader_source"] == "host_placeholder"
    assert rec["reader_is_field_measurement"] is False
    assert rec["reader_is_firmware"] is False
    assert rec["duty"] == "REFUSE"
    assert rec["policy_action"] == "SLEEP"
    assert rec["inference_allowed"] is False
    assert rec["workload"] is None
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False
    assert rec["source"] == "host_first_boot"


def test_via_host_reader_above_floor_hardware_pending():
    rec = first_boot(
        3.9,
        infer_requested=True,
        via_host_reader=True,
        reader_source="hardware_pending",
    )
    assert rec["via_host_reader"] is True
    assert rec["reader_source"] == "hardware_pending"
    assert rec["reader_is_field_measurement"] is False
    assert rec["reader_is_firmware"] is False
    assert rec["duty"] == "INFER"
    assert rec["policy_action"] == "INFER"
    assert rec["inference_allowed"] is True
    assert rec["workload"] == PRIMARY_WORKLOAD
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False


if __name__ == "__main__":
    test_below_floor_refuses_inference()
    test_above_floor_allows_tinyml_primary()
    test_listen_only_does_not_claim_workload()
    test_via_host_reader_below_floor_host_placeholder()
    test_via_host_reader_above_floor_hardware_pending()
    print("test_first_boot: ok")
