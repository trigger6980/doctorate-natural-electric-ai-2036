"""Tests for the host energy observer stub."""

from __future__ import annotations

import unittest

from energy_observer import as_dict, record_sample


class EnergyObserverTests(unittest.TestCase):
    def test_host_placeholder_is_not_field(self) -> None:
        sample = record_sample(4.6, 0.05, source="host_placeholder")
        self.assertFalse(sample.is_field_measurement())
        self.assertEqual(sample.source, "host_placeholder")

    def test_hardware_pending_is_not_field(self) -> None:
        sample = record_sample(0.0, 0.0, source="hardware_pending")
        self.assertFalse(sample.is_field_measurement())
        doc = as_dict(sample)
        self.assertFalse(doc["is_field_measurement"])

    def test_measured_label_refused(self) -> None:
        with self.assertRaises(ValueError):
            record_sample(4.6, 0.05, source="measured")

    def test_negative_values_refused(self) -> None:
        with self.assertRaises(ValueError):
            record_sample(-1.0, 0.05)
        with self.assertRaises(ValueError):
            record_sample(4.6, -0.01)


if __name__ == "__main__":
    unittest.main()
