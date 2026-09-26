"""Tests for the host energy observer stub."""

from __future__ import annotations

import unittest

from energy_observer import ALLOWED_SOURCES, as_dict, record_sample


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

    def test_as_dict_honesty_note_and_keys(self) -> None:
        """as_dict must surface the host-stub note and keep is_field_measurement False."""
        sample = record_sample(3.7, 0.01, source="host_placeholder")
        doc = as_dict(sample)
        self.assertIn("note", doc)
        self.assertIn("Host stub only", doc["note"])
        self.assertIn("Not a measured generation or consumption figure", doc["note"])
        self.assertFalse(doc["is_field_measurement"])
        self.assertEqual(doc["source"], "host_placeholder")
        self.assertEqual(doc["voltage_v"], 3.7)
        self.assertEqual(doc["estimated_joules"], 0.01)

    def test_allowed_sources_set(self) -> None:
        """Allowed sources stay the documented host-only pair."""
        self.assertEqual(ALLOWED_SOURCES, frozenset({"host_placeholder", "hardware_pending"}))


if __name__ == "__main__":
    unittest.main()
