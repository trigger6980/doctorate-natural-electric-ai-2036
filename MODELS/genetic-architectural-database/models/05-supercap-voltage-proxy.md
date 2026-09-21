# 05 — Supercap Voltage Proxy Model

**Domain:** Power Management  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (analytic form only; not calibrated)  
**Operator role:** Converts measured rail voltage into `EnergyState.estimated_joules` for Model 01 and the task-graph energy gate

## Description
Lightweight model (or calibrated equation) that converts measured supercapacitor voltage into estimated remaining joules, accounting for leakage and non-ideal capacitance. Provides the numeric energy budget used by higher-level schedulers.

The host simulator in Model 01 currently uses a linear `cost * 0.1` voltage drop. This card is the intended replacement: `E = 0.5 * C_eff * V^2` with an explicit leakage term. **No board-specific C_eff has been measured in this repository.**

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `voltage_v` | input | Instantaneous rail voltage |
| `C_farads` | parameter | Effective capacitance; unknown until measured |
| `v_min_useful` | parameter | Below this, treat remaining energy as 0 for scheduling |
| `leak_w` | parameter | Optional constant leakage watts; default 0 until measured |
| `dt_s` | optional input | Needed only if leakage is applied over an interval |
| `estimated_joules` | output | `max(0, 0.5 * C * (V^2 - v_min_useful^2) - leak_w * dt_s)` |

Planned entry points:
- `joules_from_voltage(voltage_v, C_farads, v_min_useful=3.3) -> float`
- `apply_leakage(joules, leak_w, dt_s) -> float`

## Energy budget (example, not measured hardware)
Evaluating the equation is cheap compared with any sensor read.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Voltage → joules evaluation | ~0 J extra | Arithmetic on an already-sampled ADC value |
| ADC for voltage | counted under Model 01 / 04 | Do not double-count |

Placeholder simulator values (not hardware):
- Example C = 1.0 F only as a *host default* for unit tests
- Example leak_w = 0 until a discharge curve exists

## Key Traits
- Physics-first: energy stored in a capacitor is quadratic in voltage
- Fail-safe: if C is unknown, callers must keep using Model 01's existing estimate and mark it uncalibrated
- Feeds `min_joules` gates on the task-graph executor
- Does not invent harvest; harvest remains a separate observer (Model 04 / lux)

## Implementation Notes
Not implemented on-device. The next host helper should live next to `energy_aware_scheduler.py` and be called before `TaskGraphExecutor.run(estimated_joules=...)`.

## Next measurements (not done)
- Measure discharge of the actual supercap from a known voltage with a known load.
- Fit C_eff and leak_w; replace the linear voltage model in the simulator.
- Record the fit coefficients in this card with date and instrument notes.
