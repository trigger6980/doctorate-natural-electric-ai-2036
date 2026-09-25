"""Host voltage reader stub for the Off-Grid AI Box.

Not an ADC driver. Not firmware. Not a field instrument.

Produces a voltage reading record that can feed energy_duty.decide
and first_boot while remaining explicitly host-sourced. Allowed
sources match the energy_observer honesty set:
  - host_placeholder — a number used so host tests and demos can run
  - hardware_pending — the slot exists; no instrument is attached

The label "measured" is refused. Callers that need a real ADC must
implement a separate path that still returns only pack_volts: float
and keeps is_field_measurement=False until a named lab + instrument
class + measurement-method note exist (see ENTERPRISE/).

Shared helper feed_via_reader() is the single path used by first_boot,
duty_to_policy.fixture_log, and SANDBOX/compose_first_boot_demo so the
feed contract stays uniform.
"""

from __future__ import annotations

from typing import Optional, Tuple

ALLOWED_SOURCES = frozenset({"host_placeholder", "hardware_pending"})

# Keys attached by feed_via_reader to first_boot / fixture_log / compose records.
# Call sites must not invent additional field-measurement claims under these names.
READER_META_KEYS = frozenset(
    {
        "reader_source",
        "reader_is_field_measurement",
        "reader_is_firmware",
    }
)


def read_pack_volts(
    pack_volts: Optional[float] = None,
    *,
    source: str = "host_placeholder",
    default_placeholder_volts: float = 3.70,
) -> dict:
    """Return a host voltage reading record.

    If pack_volts is None, uses default_placeholder_volts only when
    source is host_placeholder. hardware_pending with no value raises.
    Never claims field measurement or firmware.
    """
    if source not in ALLOWED_SOURCES:
        raise ValueError(
            f"source {source!r} is not allowed; use host_placeholder or hardware_pending"
        )
    if pack_volts is None:
        if source == "hardware_pending":
            raise ValueError(
                "hardware_pending requires an explicit pack_volts; "
                "do not invent a measured value"
            )
        volts = float(default_placeholder_volts)
    else:
        volts = float(pack_volts)
    if volts < 0.0:
        raise ValueError("pack_volts must be >= 0")
    return {
        "pack_volts": volts,
        "source": source,
        "is_field_measurement": False,
        "is_firmware": False,
        "note": (
            "Host voltage reader stub only. Not an ADC read, not calibrated, "
            "not a field certificate. Feed first_boot / energy_duty.decide."
        ),
    }


def as_feed(reading: dict) -> float:
    """Extract pack_volts for first_boot / energy_duty.decide."""
    if not isinstance(reading, dict) or "pack_volts" not in reading:
        raise ValueError("reading must be a dict with pack_volts")
    if reading.get("is_field_measurement") is True:
        raise ValueError("field measurement claims are refused on this host path")
    return float(reading["pack_volts"])


def feed_via_reader(
    pack_volts: float,
    *,
    source: str = "host_placeholder",
) -> Tuple[float, dict]:
    """Single host path: pack_volts → read_pack_volts → as_feed + reader_meta.

    Used by first_boot, duty_to_policy.fixture_log, and compose_first_boot
    so the documented feed contract stays uniform. Returns
    (feed_volts, reader_meta) where reader_meta carries exactly
    READER_META_KEYS:
      reader_source, reader_is_field_measurement, reader_is_firmware
    Never claims field measurement or firmware.
    """
    reading = read_pack_volts(float(pack_volts), source=source)
    feed_volts = as_feed(reading)
    reader_meta = {
        "reader_source": reading["source"],
        "reader_is_field_measurement": reading["is_field_measurement"],
        "reader_is_firmware": reading["is_firmware"],
    }
    # Contract guard: meta keys stay the documented set only.
    assert set(reader_meta.keys()) == READER_META_KEYS
    return feed_volts, reader_meta
