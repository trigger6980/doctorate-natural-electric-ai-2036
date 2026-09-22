# 13 — Magnetic Field Harvest Predictor

**Domain:** Ambient Magnetic / inductive harvest  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no coil driver, no measured B-field, no calibrated Faraday model)  
**Operator role:** Optional harvest observer that estimates *whether* a nearby AC magnetic source is worth sampling, then hands a coarse energy hint to Model 01 / Model 04 / Model 05. Not a wattmeter.

## Description
Predicts short-horizon usefulness of inductive / magnetic harvest from cheap observables (coil RMS voltage or a hall-effect proxy) so a batteryless node does not spend ADC and radio energy chasing a dead field.

This card specifies the host-facing interface. There is **no coil firmware, no measured tesla series, and no calibrated Faraday implementation in this repository**. Numbers below are design targets, not bench results.

Analytic reminder (uncalibrated, host-only):

- Induced EMF magnitude scales with `N * A * dB/dt` for a simple loop.
- A host stub may treat `coil_vrms` as a *proxy*, never as harvested joules, until `C_farads` and coupling are measured.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `coil_vrms` | input | RMS voltage at the coil or rectifier front-end |
| `coil_freq_hz` | optional input | Line / machine frequency hint (50/60 Hz or unknown) |
| `hall_ut` | optional input | Microtesla-class hall reading if a sensor exists |
| `rail_voltage_v` | input | Storage rail already used by Model 01 |
| `dt_s` | parameter | Sample interval |
| `EnergyState.voltage_v` | output | Same struct Model 01 consumes |
| `EnergyState.estimated_joules` | optional output | Prefer Model 05 when a supercap model exists |
| `field_useful` | output | Boolean: field looks worth another sample |
| `joules_used_est` | output | Placeholder cost of this observe step |

Planned entry points:
- `observe(coil_vrms, coil_freq_hz, hall_ut, rail_voltage_v) -> EnergyState`
- `field_looks_useful(coil_vrms, hall_ut) -> bool`
- `may_sample(energy_state) -> bool` — refuse extra ADC when Model 01 would choose SLEEP

No host helper is checked in for this card yet. Do not invent a tesla-to-joule conversion without a measured coupling factor.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended coil + MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Coil RMS ADC burst | 0.0005–0.002 J | A few rectifier-front-end samples |
| Optional hall peek | 0.0002–0.001 J | Sensor already biased |
| Skip (policy = SLEEP or field dead) | 0 J extra | Gate via Model 01 |

Safety rules:
- Never treat `coil_vrms` as harvested watts.
- Never enable a hall sensor when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Do not claim mains-safe isolation from this card; coil coupling to line conductors is a hardware design problem, not a software one.

## Key Traits
- Magnetic term is a *hint*, never a certified harvest wattage
- Falls back to rail voltage when coil / hall inputs are missing
- Shares `EnergyState` with Models 01, 04, and 05 so schedulers do not grow a second type
- Distinct from Model 04 (PV + RF) and Model 14 (vibration / TENG)

## Implementation Notes
Not implemented. When added, live under `PROTOTYPES/energy-harvester-tinyml/` next to the Model 05 voltage helper. Keep any Faraday math labeled uncalibrated until a coupling factor is measured on the intended coil.

## Next measurements (not done)
- Log simultaneous `coil_vrms`, optional `hall_ut`, and rail voltage near a known AC source.
- Fit a coupling factor; do not publish tesla-to-joule tables before that fit.
- Confirm the extra ADC cost is cheaper than a wasted INFER/TRANSMIT.
- Decide whether line-frequency lock is worth the extra samples.
