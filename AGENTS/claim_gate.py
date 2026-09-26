"""Host claim gate for energy samples.

Maps an EnergySample (or a source label) onto allowed uses.
Host-placeholder and hardware-pending samples may be logged for tests.
They may not be used as field generation figures, quote evidence, or
result-record numbers.

This is not a legal opinion and not a measurement instrument.

Honesty boundary (same chain as energy_observer, FIRST-BOOT, and
ENTERPRISE result-record):
Refused claims (field_generation, quote_evidence, result_record) map to
the requirement that a named lab + instrument class + measurement-method
note exist before any result is labeled. See ENTERPRISE/: measurement-hold
→ named-lab-plan → instrument-list → measurement-method → result-record.
Allowed claims (host_log, sandbox_demo) never promote host stubs into
that chain; observer_not_evidence stays the refuse token.

Evaluation order of refuse_reason (locked by tests):
1. unknown_claim  — claim not in ALLOWED_CLAIMS | REFUSED_CLAIMS
2. unknown_source — source not in energy_observer.ALLOWED_SOURCES
3. observer_not_evidence — claim in REFUSED_CLAIMS
4. ok             — claim in ALLOWED_CLAIMS and source allowed
When both claim and source are unknown, unknown_claim is returned first.
"""

from __future__ import annotations

from typing import Iterable, Mapping

from energy_observer import ALLOWED_SOURCES, EnergySample, as_dict

ALLOWED_CLAIMS = frozenset({"host_log", "sandbox_demo"})
REFUSED_CLAIMS = frozenset({"field_generation", "quote_evidence", "result_record"})


def refuse_reason(source: str, claim: str) -> str:
    # Order: unknown_claim → unknown_source → observer_not_evidence → ok
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


def stamp(sample: EnergySample, claims: Iterable[str] | None = None) -> dict:
    """Attach claim reasons to an observer dict. Host labels only."""
    checks = list(claims) if claims is not None else [
        "host_log",
        "sandbox_demo",
        "field_generation",
        "quote_evidence",
        "result_record",
    ]
    payload = as_dict(sample)
    payload["claims"] = {claim: refuse_reason(sample.source, claim) for claim in checks}
    return payload


def stamp_many(
    samples: Iterable[EnergySample], claims: Iterable[str] | None = None
) -> Mapping[str, str]:
    """First refuse token per claim across a sample list."""
    material = list(samples)
    checks = list(claims) if claims is not None else [
        "host_log",
        "sandbox_demo",
        "field_generation",
        "quote_evidence",
        "result_record",
    ]
    return {claim: scan_samples(material, claim) for claim in checks}
