"""Host tests for host_voltage_reader. Not a hardware certificate."""

import pytest

from host_voltage_reader import (
    ALLOWED_SOURCES,
    READER_META_KEYS,
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
    assert ALLOWED_SOURCES == frozenset({"host_placeholder", "hardware_pending"})


def test_feed_via_reader_host_placeholder():
    volts, meta = feed_via_reader(3.2, source="host_placeholder")
    assert volts == 3.2
    assert meta["reader_source"] == "host_placeholder"
    assert meta["reader_is_field_measurement"] is False
    assert meta["reader_is_firmware"] is False
    assert set(meta.keys()) == READER_META_KEYS


def test_feed_via_reader_hardware_pending():
    volts, meta = feed_via_reader(3.9, source="hardware_pending")
    assert volts == 3.9
    assert meta["reader_source"] == "hardware_pending"
    assert meta["reader_is_field_measurement"] is False
    assert meta["reader_is_firmware"] is False
    assert set(meta.keys()) == READER_META_KEYS


def test_feed_via_reader_measured_refused():
    with pytest.raises(ValueError, match="not allowed"):
        feed_via_reader(3.6, source="measured")


def test_reader_meta_keys_contract():
    """Meta attached by feed_via_reader is exactly the documented key set."""
    assert READER_META_KEYS == frozenset(
        {
            "reader_source",
            "reader_is_field_measurement",
            "reader_is_firmware",
        }
    )
    _, meta = feed_via_reader(3.5, source="host_placeholder")
    assert set(meta.keys()) == READER_META_KEYS
    # Honesty: none of these keys ever carry a True field claim from this path.
    assert meta["reader_is_field_measurement"] is False
    assert meta["reader_is_firmware"] is False


def test_read_pack_volts_preserves_honesty_note():
    """read_pack_volts must surface the host-stub honesty note and keep flags False."""
    rec = read_pack_volts(3.7, source="host_placeholder")
    assert "note" in rec
    assert "Host voltage reader stub only" in rec["note"]
    assert "Not an ADC read" in rec["note"]
    assert "not a field certificate" in rec["note"]
    assert rec["is_field_measurement"] is False
    assert rec["is_firmware"] is False
    assert rec["source"] == "host_placeholder"
    assert rec["pack_volts"] == 3.7


def test_shared_honesty_sources_with_energy_observer():
    """host_voltage_reader and energy_observer share the same allowed source set.

    Import is path-tolerant: when run under (cd PROTOTYPES/offgrid-ai-box)
the AGENTS package may not be on sys.path; in that case the check is skipped
rather than inventing a different source list.
    """
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    agents = root / "AGENTS"
    if str(agents) not in sys.path:
        sys.path.insert(0, str(agents))
    try:
        from energy_observer import ALLOWED_SOURCES as OBSERVER_SOURCES
    except ImportError:
        return  # CI path without AGENTS on path is fine; other jobs cover observer
    assert ALLOWED_SOURCES == OBSERVER_SOURCES
    assert "measured" not in OBSERVER_SOURCES
