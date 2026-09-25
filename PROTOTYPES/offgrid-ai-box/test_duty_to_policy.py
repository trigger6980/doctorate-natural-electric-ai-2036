"""Host tests for duty_to_policy adapter. Not hardware."""

import unittest

from duty_to_policy import (
    duty_string_to_policy_action,
    fixture_log,
    make_duty_policy_fn,
)
from energy_duty import FLOOR_VOLTS


class DutyToPolicyTests(unittest.TestCase):
    def test_refuse_maps_to_sleep(self):
        self.assertEqual(duty_string_to_policy_action("REFUSE"), "SLEEP")

    def test_sleep_maps_to_sleep(self):
        self.assertEqual(duty_string_to_policy_action("SLEEP"), "SLEEP")

    def test_idle_listen_maps_to_sense(self):
        self.assertEqual(duty_string_to_policy_action("IDLE_LISTEN"), "SENSE")

    def test_infer_maps_to_infer(self):
        self.assertEqual(duty_string_to_policy_action("INFER"), "INFER")

    def test_unknown_raises(self):
        with self.assertRaises(ValueError):
            duty_string_to_policy_action("TRANSMIT")

    def test_fixture_log_below_floor(self):
        rows = fixture_log([FLOOR_VOLTS - 0.2], infer_requested=True)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["duty"], "REFUSE")
        self.assertEqual(rows[0]["policy_action"], "SLEEP")
        self.assertIs(rows[0]["is_field_measurement"], False)
        self.assertEqual(rows[0]["source"], "host_fixture")

    def test_fixture_log_above_floor_infer(self):
        rows = fixture_log([3.9], infer_requested=True)
        self.assertEqual(rows[0]["duty"], "INFER")
        self.assertEqual(rows[0]["policy_action"], "INFER")

    def test_fixture_log_above_floor_idle(self):
        rows = fixture_log([3.9], infer_requested=False)
        self.assertEqual(rows[0]["duty"], "IDLE_LISTEN")
        self.assertEqual(rows[0]["policy_action"], "SENSE")

    def test_policy_fn_callable_shape(self):
        class _State:
            voltage_v = 3.0
            estimated_joules = 1.0

        class _Cfg:
            pass

        fn = make_duty_policy_fn(infer_requested=True)
        result = fn(_State(), _Cfg())
        # string or Action enum member with .name
        name = result if isinstance(result, str) else getattr(result, "name", str(result))
        self.assertEqual(name, "SLEEP")


if __name__ == "__main__":
    unittest.main()
