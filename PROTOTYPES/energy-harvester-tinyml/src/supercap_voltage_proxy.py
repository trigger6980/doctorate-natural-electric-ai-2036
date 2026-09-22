"""
Model 05 host helper: voltage <-> estimated joules.

Analytic form only. C_farads is a caller-supplied parameter, not a
calibrated board constant. Do not treat the default 1.0 F as hardware.
"""

from __future__ import annotations

import math


def joules_from_voltage(
    voltage_v: float,
    C_farads: float,
    v_min_useful: float = 3.3,
) -> float:
    """Remaining energy above v_min_useful using E = 0.5 * C * (V^2 - Vmin^2)."""
    if C_farads <= 0.0:
        raise ValueError("C_farads must be positive; unknown C is not a license to guess")
    if voltage_v <= v_min_useful:
        return 0.0
    energy = 0.5 * C_farads * (voltage_v * voltage_v - v_min_useful * v_min_useful)
    return max(0.0, energy)


def voltage_from_joules(
    joules: float,
    C_farads: float,
    v_min_useful: float = 3.3,
) -> float:
    """Inverse of joules_from_voltage. joules <= 0 maps to v_min_useful."""
    if C_farads <= 0.0:
        raise ValueError("C_farads must be positive; unknown C is not a license to guess")
    if joules <= 0.0:
        return v_min_useful
    return math.sqrt(v_min_useful * v_min_useful + (2.0 * joules / C_farads))


def apply_leakage(joules: float, leak_w: float, dt_s: float) -> float:
    """Subtract constant leakage over dt_s. leak_w defaults to 0 until measured."""
    if dt_s < 0.0:
        raise ValueError("dt_s must be non-negative")
    if leak_w < 0.0:
        raise ValueError("leak_w must be non-negative")
    return max(0.0, joules - leak_w * dt_s)
