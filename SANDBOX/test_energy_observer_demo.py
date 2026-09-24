"""Sandbox must surface observer source labels, not field joules."""

from __future__ import annotations

import unittest

from energy_observer import as_dict, record_sample


class SandboxObserverDemoTests(unittest.TestCase):
    def test_demo_row_matches_host_contract(self) -> None:
        sample = record_sample(4.6, 0.05, source="host_placeholder")
        row = as_dict(sample)
        self.assertEqual(row["source"], "host_placeholder")
        self.assertFalse(row["is_field_measurement"])


if __name__ == "__main__":
    unittest.main()
