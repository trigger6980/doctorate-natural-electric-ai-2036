"""Host claim gate for energy samples.

Maps an EnergySample (or a source label) onto allowed uses.
Host-placeholder and hardware-pending samples may be logged for tests.
They may not be used as field generation figures, quote evidence, or
result-record numbers.

This is not a legal opinion and not a measurement instrument.
"""

from __future__ import annotations

from typing import Iterable

from energy_observer import ALLOWED_SOURCES, EnergySample

ALLOWED_CLAIMS = frozenset({"host_log", "sandbox_demo"})
REFUSED_CLAIMS = frozenset({"field_generation", "quote_evidence", "result_record"})


def refuse_reason(source: str, claim: str) -> str:
    if claim not in ALLOWED_CLAIMS | REFUSED_CLAIMS:
        return "unknown_claim"
    if source not in ALLOWED_SOURCES:
        return "unknown_source"
    if claim in REFUSED_CLAIMS:
        return "observer_not_evidence"
    return "ok"


def allow(source: str, claim: str) -> bool:
    return refuse_reason(source, claim) == "ok"


def allow_sample(sample: EnergySample, claim: str) -> bool:
    if sample.is_field_measurement():
        # Current stub never returns True; keep the branch honest.
        return claim in ALLOWED_CLAIMS
    return allow(sample.source, claim)


def scan_samples(samples: Iterable[EnergySample], claim: str) -> str:
    """First refuse token across a list, or ok."""
    for sample in samples:
        reason = refuse_reason(sample.source, claim)
        if reason != "ok":
            return reason
    return "ok"
