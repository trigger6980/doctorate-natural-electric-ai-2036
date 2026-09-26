"""Tests for the host energy claim gate."""

from __future__ import annotations

import unittest

from claim_gate import (
    ALLOWED_CLAIMS,
    REFUSED_CLAIMS,
    allow,
    allow_sample,
    refuse_reason,
    scan_samples,
    stamp,
    stamp_many,
)
from energy_observer import ALLOWED_SOURCES, record_sample


class ClaimGateTests(unittest.TestCase):
    def test_host_log_allowed(self) -> None:
        self.assertTrue(allow("host_placeholder", "host_log"))
        self.assertEqual(refuse_reason("host_placeholder", "sandbox_demo"), "ok")

    def test_quote_evidence_refused(self) -> None:
        self.assertFalse(allow("host_placeholder", "quote_evidence"))
        self.assertEqual(
            refuse_reason("hardware_pending", "quote_evidence"),
            "observer_not_evidence",
        )

    def test_field_and_result_refused(self) -> None:
        self.assertEqual(
            refuse_reason("host_placeholder", "field_generation"),
            "observer_not_evidence",
        )
        self.assertEqual(
            refuse_reason("host_placeholder", "result_record"),
            "observer_not_evidence",
        )

    def test_sample_helper(self) -> None:
        sample = record_sample(4.6, 0.05, source="host_placeholder")
        self.assertTrue(allow_sample(sample, "host_log"))
        self.assertFalse(allow_sample(sample, "quote_evidence"))

    def test_scan_stops_on_refuse(self) -> None:
        samples = [
            record_sample(4.6, 0.05, source="host_placeholder"),
            record_sample(0.0, 0.0, source="hardware_pending"),
        ]
        self.assertEqual(scan_samples(samples, "host_log"), "ok")
        self.assertEqual(scan_samples(samples, "quote_evidence"), "observer_not_evidence")

    def test_unknown_claim(self) -> None:
        self.assertEqual(refuse_reason("host_placeholder", "certified_kwh"), "unknown_claim")

    def test_unknown_source(self) -> None:
        """refuse_reason must surface unknown_source before claim evaluation."""
        self.assertEqual(
            refuse_reason("measured", "host_log"),
            "unknown_source",
        )
        self.assertEqual(
            refuse_reason("field_meter", "sandbox_demo"),
            "unknown_source",
        )
        # Unknown source still yields unknown_claim when claim is also unknown.
        self.assertEqual(
            refuse_reason("measured", "certified_kwh"),
            "unknown_claim",
        )

    def test_refuse_reason_evaluation_order(self) -> None:
        """Lock the documented precedence: unknown_claim → unknown_source → observer_not_evidence → ok."""
        # 1. unknown claim wins even when source is also unknown
        self.assertEqual(refuse_reason("measured", "certified_kwh"), "unknown_claim")
        # 2. known claim + unknown source → unknown_source
        self.assertEqual(refuse_reason("measured", "host_log"), "unknown_source")
        self.assertEqual(refuse_reason("field_meter", "sandbox_demo"), "unknown_source")
        # 3. known source + refused claim → observer_not_evidence
        self.assertEqual(
            refuse_reason("host_placeholder", "field_generation"),
            "observer_not_evidence",
        )
        # 4. known source + allowed claim → ok
        self.assertEqual(refuse_reason("host_placeholder", "host_log"), "ok")
        self.assertEqual(refuse_reason("hardware_pending", "sandbox_demo"), "ok")

    def test_scan_samples_unknown_source(self) -> None:
        """scan_samples surfaces unknown_source when any sample has a refused source label."""
        # record_sample itself refuses unknown sources, so build a minimal
        # stand-in that only exposes .source for the scan path.
        class _BadSource:
            source = "measured"

        samples = [
            record_sample(4.6, 0.05, source="host_placeholder"),
            _BadSource(),  # type: ignore[list-item]
        ]
        self.assertEqual(scan_samples(samples, "host_log"), "unknown_source")
        self.assertEqual(scan_samples(samples, "sandbox_demo"), "unknown_source")
        # Unknown claim still precedes when the claim itself is unknown
        self.assertEqual(scan_samples(samples, "certified_kwh"), "unknown_claim")

    def test_scan_samples_empty(self) -> None:
        """Empty iterable is not evidence of a refused source or claim; returns ok."""
        self.assertEqual(scan_samples([], "host_log"), "ok")
        self.assertEqual(scan_samples([], "sandbox_demo"), "ok")
        self.assertEqual(scan_samples([], "field_generation"), "ok")
        self.assertEqual(scan_samples([], "quote_evidence"), "ok")
        self.assertEqual(scan_samples([], "result_record"), "ok")
        # Unknown claim on empty list still surfaces unknown_claim (claim check is independent of samples).
        self.assertEqual(scan_samples([], "certified_kwh"), "unknown_claim")

    def test_stamp_many_empty(self) -> None:
        """stamp_many on empty list yields ok for every documented claim; empty is not a refuse."""
        scan = stamp_many([])
        self.assertEqual(scan["host_log"], "ok")
        self.assertEqual(scan["sandbox_demo"], "ok")
        self.assertEqual(scan["field_generation"], "ok")
        self.assertEqual(scan["quote_evidence"], "ok")
        self.assertEqual(scan["result_record"], "ok")
        # Custom claims list still respects evaluation order on empty material.
        scan_custom = stamp_many([], claims=["host_log", "certified_kwh"])
        self.assertEqual(scan_custom["host_log"], "ok")
        self.assertEqual(scan_custom["certified_kwh"], "unknown_claim")

    def test_stamp_labels_allowed_and_refused(self) -> None:
        sample = record_sample(4.6, 0.05, source="host_placeholder")
        payload = stamp(sample)
        self.assertEqual(payload["claims"]["host_log"], "ok")
        self.assertEqual(payload["claims"]["quote_evidence"], "observer_not_evidence")
        self.assertFalse(payload["is_field_measurement"])

    def test_stamp_many_scan(self) -> None:
        samples = [
            record_sample(4.6, 0.05, source="host_placeholder"),
            record_sample(0.0, 0.0, source="hardware_pending"),
        ]
        scan = stamp_many(samples)
        self.assertEqual(scan["sandbox_demo"], "ok")
        self.assertEqual(scan["result_record"], "observer_not_evidence")

    def test_stamp_many_custom_claims_only_those_keys(self) -> None:
        """Custom claims list on non-empty samples yields exactly those keys; maps host_log→ok / result_record→observer_not_evidence."""
        samples = [
            record_sample(4.0, 0.02, source="hardware_pending"),
            record_sample(3.7, 0.01, source="host_placeholder"),
        ]
        scan = stamp_many(samples, claims=["host_log", "result_record"])
        self.assertEqual(set(scan.keys()), {"host_log", "result_record"})
        self.assertEqual(scan["host_log"], "ok")
        self.assertEqual(scan["result_record"], "observer_not_evidence")
        # Empty custom list yields empty mapping (no invented defaults).
        scan_empty = stamp_many(samples, claims=[])
        self.assertEqual(scan_empty, {})

    def test_stamp_many_custom_claims_unknown_source(self) -> None:
        """Custom claims list on samples containing an unknown source yields unknown_source for allowed claims; unknown_claim still precedes."""
        class _BadSource:
            source = "measured"

        samples = [
            record_sample(4.0, 0.02, source="host_placeholder"),
            _BadSource(),  # type: ignore[list-item]
        ]
        scan = stamp_many(samples, claims=["host_log", "result_record", "certified_kwh"])
        self.assertEqual(set(scan.keys()), {"host_log", "result_record", "certified_kwh"})
        self.assertEqual(scan["host_log"], "unknown_source")
        self.assertEqual(scan["result_record"], "unknown_source")
        # unknown_claim still wins for the unknown claim token
        self.assertEqual(scan["certified_kwh"], "unknown_claim")

    def test_allowed_and_refused_claims_sets(self) -> None:
        """Allowed and refused claim sets stay the documented host-only partition."""
        self.assertEqual(ALLOWED_CLAIMS, frozenset({"host_log", "sandbox_demo"}))
        self.assertEqual(
            REFUSED_CLAIMS,
            frozenset({"field_generation", "quote_evidence", "result_record"}),
        )
        # Partition: no overlap, and refuse_reason covers the union.
        self.assertTrue(ALLOWED_CLAIMS.isdisjoint(REFUSED_CLAIMS))

    def test_shares_allowed_sources_with_observer(self) -> None:
        """claim_gate must use the same ALLOWED_SOURCES set as energy_observer."""
        self.assertEqual(
            ALLOWED_SOURCES,
            frozenset({"host_placeholder", "hardware_pending"}),
        )
        # unknown_source is the only path for labels outside that set
        self.assertEqual(refuse_reason("measured", "host_log"), "unknown_source")

    def test_stamp_preserves_honesty_note(self) -> None:
        """stamp must retain the observer as_dict honesty note and is_field_measurement=False."""
        sample = record_sample(3.7, 0.01, source="host_placeholder")
        payload = stamp(sample)
        self.assertIn("note", payload)
        self.assertIn("Host stub only", payload["note"])
        self.assertIn("Not a measured generation or consumption figure", payload["note"])
        self.assertFalse(payload["is_field_measurement"])
        self.assertEqual(payload["source"], "host_placeholder")
        self.assertEqual(payload["claims"]["host_log"], "ok")
        self.assertEqual(payload["claims"]["field_generation"], "observer_not_evidence")

    def test_stamp_empty_claims_list(self) -> None:
        """Empty claims iterable still preserves honesty note; claims dict is empty (not invented)."""
        sample = record_sample(3.7, 0.01, source="host_placeholder")
        payload = stamp(sample, claims=[])
        self.assertIn("note", payload)
        self.assertIn("Host stub only", payload["note"])
        self.assertIn("Not a measured generation or consumption figure", payload["note"])
        self.assertFalse(payload["is_field_measurement"])
        self.assertEqual(payload["source"], "host_placeholder")
        self.assertEqual(payload["claims"], {})

    def test_stamp_custom_claims_only_those_keys(self) -> None:
        """Custom claims list yields exactly those keys; no default claims are invented."""
        sample = record_sample(4.0, 0.02, source="hardware_pending")
        payload = stamp(sample, claims=["host_log", "result_record"])
        self.assertEqual(set(payload["claims"].keys()), {"host_log", "result_record"})
        self.assertEqual(payload["claims"]["host_log"], "ok")
        self.assertEqual(payload["claims"]["result_record"], "observer_not_evidence")
        self.assertIn("note", payload)
        self.assertIn("Host stub only", payload["note"])
        self.assertFalse(payload["is_field_measurement"])


if __name__ == "__main__":
    unittest.main()
