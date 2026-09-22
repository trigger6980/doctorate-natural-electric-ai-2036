# 14 — Vibration / TENG Feature Extractor

**Domain:** Mechanical Harvest  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no piezo/TENG driver, no measured strain series, no calibrated joule-per-cycle fit)  
**Operator role:** Optional harvest observer that turns a cheap vibration or triboelectric front-end into a coarse energy hint for Model 01 / Model 04 / Model 05. Not a wattmeter and not a structural-health monitor.

## Description
Extracts short-horizon usefulness of mechanical harvest (piezoelectric patch or triboelectric nanogenerator) from cheap observables so a batteryless node does not spend ADC and radio energy on a still machine.

This card specifies the host-facing interface. There is **no piezo/TENG firmware, no measured acceleration or open-circuit voltage series, and no calibrated energy-per-cycle implementation in this repository**. Numbers below are design targets, not bench results.

Analytic reminder (uncalibrated, host-only):

- For a first-order piezo, harvested charge scales with strain rate and capacitance of the element.
- For a contact-separation TENG, open-circuit voltage is highly load- and gap-dependent; treating peak ADC counts as joules is incorrect.
- A host stub may treat `teng_vpeak` or `accel_rms_g` as a *proxy*, never as harvested joules, until `C_farads` (storage) and coupling are measured.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `teng_vpeak` | input | Peak voltage at rectifier front-end (TENG or piezo) |
| `accel_rms_g` | optional input | Cheap accelerometer RMS if a sensor exists |
| `cycle_hz` | optional input | Dominant vibration frequency hint |
| `rail_voltage_v` | input | Storage rail already used by Model 01 |
| `dt_s` | parameter | Sample interval |
| `EnergyState.voltage_v` | output | Same struct Model 01 consumes |
| `EnergyState.estimated_joules` | optional output | Prefer Model 05 when a supercap model exists |
| `motion_useful` | output | Boolean: vibration looks worth another sample |
| `joules_used_est` | output | Placeholder cost of this observe step |

Planned entry points:
- `observe(teng_vpeak, accel_rms_g, cycle_hz, rail_voltage_v) -> EnergyState`
- `motion_looks_useful(teng_vpeak, accel_rms_g) -> bool`
- `may_sample(energy_state) -> bool` — refuse extra ADC when Model 01 would choose SLEEP

No host helper is checked in for this card yet. Do not invent a strain-to-joule or TENG-to-joule conversion without a measured coupling factor.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended transducer + MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Rectifier-front-end ADC burst | 0.0005–0.002 J | A few peak/RMS samples |
| Optional accel peek | 0.0002–0.001 J | Sensor already biased |
| Skip (policy = SLEEP or motion dead) | 0 J extra | Gate via Model 01 |

Safety rules:
- Never treat `teng_vpeak` or `accel_rms_g` as harvested watts.
- Never enable an accelerometer when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Do not claim structural-health diagnostics, machine-safety certification, or high-voltage TENG isolation from this card; those are hardware and process problems, not software ones.

## Key Traits
- Mechanical term is a *hint*, never a certified harvest wattage
- Falls back to rail voltage when TENG / accel inputs are missing
- Shares `EnergyState` with Models 01, 04, 05, and 13 so schedulers do not grow a second type
- Distinct from Model 04 (PV + RF) and Model 13 (magnetic / inductive)

## Implementation Notes
Not implemented. When added, live under `PROTOTYPES/energy-harvester-tinyml/` next to the Model 05 voltage helper. Keep any piezo/TENG math labeled uncalibrated until a coupling factor is measured on the intended transducer.

## Next measurements (not done)
- Log simultaneous `teng_vpeak`, optional `accel_rms_g`, and rail voltage on a known vibrating fixture.
- Fit a coupling factor; do not publish joule-per-cycle tables before that fit.
- Confirm the extra ADC cost is cheaper than a wasted INFER/TRANSMIT.
- Decide whether frequency lock is worth the extra samples versus a simple peak threshold.
