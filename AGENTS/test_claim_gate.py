"""Tests for the host energy claim gate."""

from __future__ import annotations

import unittest

from claim_gate import allow, allow_sample, refuse_reason, scan_samples
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


if __name__ == "__main__":
    unittest.main()
