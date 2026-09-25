"""Host tests for host_voltage_reader. Not a hardware certificate."""

import pytest

from host_voltage_reader import (
    ALLOWED_SOURCES,
    as_feed,
    feed_via_reader,
    read_pack_volts,
)
from first_boot import first_boot


def test_explicit_volts_host_placeholder():
    rec = read_pack_volts(3.2, source="host_placeholder")
    assert rec["pack_volts"] == 3.2
    assert rec["source"] == "host_placeholder"
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False


def test_default_placeholder_when_none():
    rec = read_pack_volts(source="host_placeholder")
    assert rec["pack_volts"] == 3.70
    assert rec["source"] == "host_placeholder"


def test_hardware_pending_requires_value():
    with pytest.raises(ValueError, match="hardware_pending requires"):
        read_pack_volts(source="hardware_pending")


def test_hardware_pending_with_value():
    rec = read_pack_volts(3.55, source="hardware_pending")
    assert rec["pack_volts"] == 3.55
    assert rec["source"] == "hardware_pending"
    assert rec["is_field_measurement"] is False


def test_measured_source_refused():
    with pytest.raises(ValueError, match="not allowed"):
        read_pack_volts(3.6, source="measured")


def test_negative_volts_refused():
    with pytest.raises(ValueError, match=">= 0"):
        read_pack_volts(-0.1)


def test_as_feed_and_first_boot_composition():
    reading = read_pack_volts(3.2, source="host_placeholder")
    volts = as_feed(reading)
    boot = first_boot(volts, infer_requested=True)
    assert boot["duty"] == "REFUSE"
    assert boot["inference_allowed"] is False
    assert boot["is_field_measurement"] is False


def test_allowed_sources_frozenset():
    assert "host_placeholder" in ALLOWED_SOURCES
    assert "hardware_pending" in ALLOWED_SOURCES
    assert "measured" not in ALLOWED_SOURCES


def test_feed_via_reader_host_placeholder():
    volts, meta = feed_via_reader(3.2, source="host_placeholder")
    assert volts == 3.2
    assert meta["reader_source"] == "host_placeholder"
    assert meta["reader_is_field_measurement"] is False
    assert meta["reader_is_firmware"] is False


def test_feed_via_reader_hardware_pending():
    volts, meta = feed_via_reader(3.9, source="hardware_pending")
    assert volts == 3.9
    assert meta["reader_source"] == "hardware_pending"
    assert meta["reader_is_field_measurement"] is False
    assert meta["reader_is_firmware"] is False


def test_feed_via_reader_measured_refused():
    with pytest.raises(ValueError, match="not allowed"):
        feed_via_reader(3.6, source="measured")
