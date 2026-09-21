"""Tests for Model 05 voltage proxy. Uncalibrated analytic form only."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supercap_voltage_proxy import joules_from_voltage, apply_leakage


def test_zero_below_vmin():
    assert joules_from_voltage(3.2, C_farads=1.0, v_min_useful=3.3) == 0.0


def test_quadratic_increase():
    low = joules_from_voltage(3.6, C_farads=1.0)
    high = joules_from_voltage(4.5, C_farads=1.0)
    assert high > low > 0.0


def test_known_formula():
    # 0.5 * 1.0 * (16 - 10.89) = 2.555
    got = joules_from_voltage(4.0, C_farads=1.0, v_min_useful=3.3)
    expected = 0.5 * (16.0 - 3.3 * 3.3)
    assert abs(got - expected) < 1e-9


def test_rejects_nonpositive_c():
    try:
        joules_from_voltage(4.0, C_farads=0.0)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_leakage():
    assert apply_leakage(1.0, leak_w=0.1, dt_s=2.0) == 0.8
    assert apply_leakage(0.05, leak_w=0.1, dt_s=2.0) == 0.0


if __name__ == "__main__":
    test_zero_below_vmin()
    test_quadratic_increase()
    test_known_formula()
    test_rejects_nonpositive_c()
    test_leakage()
    print("All proxy tests passed.")
