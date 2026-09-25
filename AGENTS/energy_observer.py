"""Host energy observer stub.

Records labeled samples. This is not a hardware ADC, not a coulomb
counter, and not a field measurement.

Allowed source labels:
- host_placeholder — a number used so host tests and the sandbox can run
- hardware_pending — the slot exists; no instrument is attached

The label `measured` is refused. Do not publish these values as joules
generated or consumed in the field.

Honesty boundary (same chain as FIRST-BOOT and ENTERPRISE result-record):
Host samples stay non-evidence until a named lab + instrument class +
measurement-method note exist and a result record is labeled. See the
full path under ENTERPRISE/: measurement-hold → named-lab-plan →
instrument-list → measurement-method → result-record. This stub never
substitutes for that chain; is_field_measurement remains False.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

ALLOWED_SOURCES = frozenset({"host_placeholder", "hardware_pending"})


@dataclass(frozen=True)
class EnergySample:
    voltage_v: float
    estimated_joules: float
    source: str

    def is_field_measurement(self) -> bool:
        return False


def record_sample(
    voltage_v: float,
    estimated_joules: float,
    source: str = "host_placeholder",
) -> EnergySample:
    if source not in ALLOWED_SOURCES:
        raise ValueError(
            f"source {source!r} is not allowed; use host_placeholder or hardware_pending"
        )
    if voltage_v < 0.0:
        raise ValueError("voltage_v must be non-negative")
    if estimated_joules < 0.0:
        raise ValueError("estimated_joules must be non-negative")
    return EnergySample(
        voltage_v=voltage_v,
        estimated_joules=estimated_joules,
        source=source,
    )


def as_dict(sample: EnergySample) -> dict:
    return {
        "voltage_v": sample.voltage_v,
        "estimated_joules": sample.estimated_joules,
        "source": sample.source,
        "is_field_measurement": sample.is_field_measurement(),
        "note": "Host stub only. Not a measured generation or consumption figure.",
    }


def log_samples(samples: List[EnergySample]) -> List[dict]:
    return [as_dict(s) for s in samples]
