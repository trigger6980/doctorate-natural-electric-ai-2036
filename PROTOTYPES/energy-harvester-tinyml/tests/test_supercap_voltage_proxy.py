"""Tests for Model 05 voltage <-> joule helper."""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supercap_voltage_proxy import (
    joules_from_voltage,
    voltage_from_joules,
    apply_leakage,
)


def test_zero_below_floor():
    assert joules_from_voltage(3.3, C_farads=1.0) == 0.0
    assert joules_from_voltage(3.0, C_farads=1.0) == 0.0


def test_positive_above_floor():
    e = joules_from_voltage(4.2, C_farads=1.0, v_min_useful=3.3)
    assert e > 0.0
    expected = 0.5 * 1.0 * (4.2 * 4.2 - 3.3 * 3.3)
    assert abs(e - expected) < 1e-12


def test_inverse_roundtrip():
    v = 4.2
    e = joules_from_voltage(v, C_farads=2.0, v_min_useful=3.3)
    v2 = voltage_from_joules(e, C_farads=2.0, v_min_useful=3.3)
    assert abs(v2 - v) < 1e-9


def test_voltage_from_zero_joules_is_floor():
    assert voltage_from_joules(0.0, C_farads=1.0, v_min_useful=3.3) == 3.3


def test_leakage():
    assert apply_leakage(1.0, leak_w=0.1, dt_s=2.0) == 0.8
    assert apply_leakage(0.01, leak_w=1.0, dt_s=1.0) == 0.0


if __name__ == "__main__":
    test_zero_below_floor()
    test_positive_above_floor()
    test_inverse_roundtrip()
    test_voltage_from_zero_joules_is_floor()
    test_leakage()
    print("proxy tests passed.")
