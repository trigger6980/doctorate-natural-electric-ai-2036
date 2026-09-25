import unittest

from energy_duty import decide, hours_remaining, FLOOR_VOLTS


class EnergyDutyTests(unittest.TestCase):
    def test_refuse_below_floor_when_infer_requested(self):
        self.assertEqual(decide(FLOOR_VOLTS - 0.1, infer_requested=True), "REFUSE")

    def test_sleep_below_floor_when_idle(self):
        self.assertEqual(decide(3.0, infer_requested=False), "SLEEP")

    def test_infer_above_floor(self):
        self.assertEqual(decide(3.8, infer_requested=True), "INFER")

    def test_listen_above_floor(self):
        self.assertEqual(decide(3.8, infer_requested=False), "IDLE_LISTEN")

    def test_rejects_negative_volts(self):
        with self.assertRaises(ValueError):
            decide(-0.1)

    def test_hours_are_pack_over_load(self):
        self.assertAlmostEqual(hours_remaining(10.0, infer_requested=False, idle_w=2.0), 5.0)
        self.assertAlmostEqual(hours_remaining(10.0, infer_requested=True, infer_w=5.0), 2.0)

    def test_hours_reject_negative_pack(self):
        with self.assertRaises(ValueError):
            hours_remaining(-1.0)


if __name__ == "__main__":
    unittest.main()
