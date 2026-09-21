# 04 — Hybrid PV-RF Energy State Estimator

**Domain:** Harvest Sensing  
**Energy Profile:** Ultra-low  
**Status:** Catalog + interface specification (no fusion code in-tree yet)  
**Operator role:** Energy-state observer plug-in that feeds Model 01 / Model 05 / later policies

## Description
Fuses photovoltaic current/voltage readings with a coarse ambient RF power estimate to produce a more robust energy-state signal than rail voltage alone, especially under indoor or partially shaded conditions.

This card specifies the *intended* observer interface. There is **no calibrated fusion implementation in this repository yet**. Numbers below are design targets, not measured results.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `pv_voltage_v` | input | Panel or harvester output voltage |
| `pv_current_ma` | input | Optional; omit if only voltage is available |
| `rf_rssi_dbm` | optional input | Coarse ambient RF proxy; not a calibrated power meter |
| `rail_voltage_v` | input | Storage / supercap rail seen by Model 01 |
| `dt_s` | parameter | Sample interval |
| `EnergyState.voltage_v` | output | Same struct Model 01 already consumes |
| `EnergyState.estimated_joules` | output | Prefer Model 05 when a supercap model exists |
| `EnergyState.lux` | optional output | May be left unset; Model 02 owns lux forecasting |

Planned entry points:
- `observe(pv_voltage_v, pv_current_ma, rf_rssi_dbm, rail_voltage_v) -> EnergyState`
- `may_sample(energy_state) -> bool` — refuse extra ADC work when Model 01 would choose SLEEP

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the target board before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| PV voltage ADC sample | 0.0005–0.002 J | One conversion |
| Optional current sense | 0.001 J | Shunt or INA-class read |
| RF RSSI peek | 0.0002–0.001 J | Radio already powered, RSSI register only |
| Skip (policy = SLEEP) | 0 J extra | Gate via Model 01 |

Safety rule: never enable extra harvest sensors when `rail_voltage_v < v_min_safe` from Model 01.

## Key Traits
- Treats voltage-only sensing as the fallback, not a failure
- RF term is a *hint*, never a claimed harvest wattage
- Output is an `EnergyState` so schedulers do not grow a second state type
- Compatible with the Operator AI energy observer slot (not yet wired)

## Implementation Notes
Not implemented. When added, live under `PROTOTYPES/energy-harvester-tinyml/` and write into the same `EnergyState` Model 01 already uses.

## Next measurements (not done)
- Log simultaneous PV voltage, optional current, rail voltage, and RSSI indoors.
- Compare voltage-only vs fused estimates against a known supercap energy (Model 05).
- Confirm the extra ADC cost is cheaper than a wasted INFER/TRANSMIT.
