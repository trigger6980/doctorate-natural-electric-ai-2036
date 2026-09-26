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
from energy_observer import record_sample


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

    def test_allowed_and_refused_claims_sets(self) -> None:
        """Allowed and refused claim sets stay the documented host-only partition."""
        self.assertEqual(ALLOWED_CLAIMS, frozenset({"host_log", "sandbox_demo"}))
        self.assertEqual(
            REFUSED_CLAIMS,
            frozenset({"field_generation", "quote_evidence", "result_record"}),
        )
        # Partition: no overlap, and refuse_reason covers the union.
        self.assertTrue(ALLOWED_CLAIMS.isdisjoint(REFUSED_CLAIMS))

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


if __name__ == "__main__":
    unittest.main()
