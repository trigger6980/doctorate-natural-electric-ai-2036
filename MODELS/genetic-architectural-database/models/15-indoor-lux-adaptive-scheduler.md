# 15 — Indoor Lux Adaptive Scheduler

**Domain:** Indoor PV  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no photodiode driver, no measured lux-to-current fit, no indoor-PV I–V curve)  
**Operator role:** Optional harvest observer that turns a cheap lux or photodiode reading into a coarse indoor-PV hint for Model 01 / Model 04 / Model 05. Not a lux meter certification and not a lighting-control product.

## Description
Indoor photovoltaic harvest is usually milliwatts or less. A node that treats outdoor-PV thresholds as indoor truth will either sleep forever or waste ADC energy sampling a dark desk.

This card specifies the host-facing interface. There is **no photodiode firmware, no measured lux time series, and no calibrated lux-to-joule implementation in this repository**. Numbers below are design targets, not bench results.

Analytic reminder (uncalibrated, host-only):

- Indoor illuminance (lux) is not irradiance (W/m²). Converting lux to watts requires a spectrum and a sensor responsivity that this repo does not measure.
- Harvested current scales with cell area and indoor-PV efficiency; both must be measured on the intended cell.
- A host stub may treat `lux` as a *proxy*, never as harvested joules, until cell area, efficiency, and storage `C_farads` are measured.
- Model 01 already carries `EnergyState.lux` as an unused optional field. This card is the place that field would become meaningful.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `lux` | input | Cheap illuminance or photodiode-proxy reading |
| `rail_voltage_v` | input | Storage rail already used by Model 01 |
| `dt_s` | parameter | Sample interval |
| `lux_min_useful` | parameter | Below this, indoor PV is treated as dark |
| `EnergyState.voltage_v` | output | Same struct Model 01 consumes |
| `EnergyState.lux` | output | Echo / smoothed lux into the shared state |
| `EnergyState.estimated_joules` | optional output | Prefer Model 05 when a supercap model exists |
| `indoor_pv_useful` | output | Boolean: light looks worth another sample |
| `joules_used_est` | output | Placeholder cost of this observe step |

Planned entry points:
- `observe(lux, rail_voltage_v) -> EnergyState`
- `indoor_looks_useful(lux) -> bool`
- `may_sample(energy_state) -> bool` — refuse extra ADC when Model 01 would choose SLEEP

No host helper is checked in for this card yet. Do not invent a lux-to-watt or lux-to-joule conversion without a measured cell area and indoor-PV efficiency.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended indoor cell + MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Photodiode / lux ADC burst | 0.0002–0.001 J | One or a few illuminance samples |
| Skip (policy = SLEEP or dark) | 0 J extra | Gate via Model 01 |
| Indoor harvest (sim, 500 lx example) | +0.0015 J / step | Same placeholder Model 01 already uses |

Safety rules:
- Never treat `lux` as harvested watts.
- Never enable a light sensor when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Do not claim lighting-control certification, photometry accuracy, or outdoor-PV equivalence from this card.
- Distinct from Model 04 (hybrid outdoor PV + RF). Indoor spectrum and cell geometry are different problems.

## Key Traits
- Illuminance is a *hint*, never a certified harvest wattage
- Falls back to rail voltage when lux is missing
- Reuses `EnergyState.lux` so Model 01 does not grow a second type
- Distinct from Model 04 (outdoor PV + RF), Model 13 (magnetic), and Model 14 (mechanical / TENG)

## Implementation Notes
Not implemented. When added, live under `PROTOTYPES/energy-harvester-tinyml/` next to the Model 05 voltage helper and the Model 01 scheduler (which already accepts unused `lux`). Keep any lux-to-energy math labeled uncalibrated until cell area and efficiency are measured on the intended indoor PV.

## Next measurements (not done)
- Log simultaneous `lux`, rail voltage, and (if possible) indoor-PV short-circuit current on a known fixture (desk lamp vs window).
- Fit cell area × efficiency; do not publish lux-to-joule tables before that fit.
- Confirm the extra ADC cost is cheaper than a wasted INFER/TRANSMIT under typical indoor flicker.
- Decide whether a simple `lux_min_useful` threshold is enough versus a short moving average.
