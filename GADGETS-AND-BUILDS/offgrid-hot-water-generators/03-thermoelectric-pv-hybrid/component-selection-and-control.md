# Generator 03 — Component selection and control sketch

Planning notes only. No field COP, no measured watt-hours, no listed appliance claim.

Companion: [README.md](README.md). Host stub: [`SANDBOX/gen03_control_stub.py`](../../../SANDBOX/gen03_control_stub.py) names the states below and calls `plant_observe_ok`. That stub is not firmware and invents no watts.

## Design intent
Use scarce PV electricity for *work that multiplies heat* (a small DC heat-pump) rather than for resistive heating, and keep a thermoelectric path as a last-resort or residual-heat helper. Controls must refuse the compressor or Peltier stage when storage voltage is below a host-defined floor — same energy-first rule as Model 01 / the energy-aware scheduler.

## Component classes (not a shopping cart)

| Class | Planning range / family | Why it is listed | What is *not* claimed |
| --- | --- | --- | --- |
| PV array | 12–24 V nominal, sized after the *electrical* load of the heat stage + controls, not after a hoped-for tank kWh | Source of the scarce joules | Nameplate watts as delivered hot-water energy |
| Charge path | PWM or MPPT controller matched to the storage chemistry | Prevents uncontrolled PV voltage on the MCU and pump | Measured harvest efficiency |
| Storage | Modest LiFePO4 pack *or* supercapacitor bank | Buffer for night and cloud; supercap fits Model 05 voltage-proxy work | Cycle-life numbers or calibrated `C_farads` |
| Heat stage A (preferred when COP can be used) | Low-voltage DC compressor / mini heat-pump module | Multiplies electrical joules into thermal joules when conditions allow | A published COP; COP is site- and temperature-dependent |
| Heat stage B (fallback) | Peltier / thermoelectric heater-cooler module on a heat exchanger | Works without a compressor; poor COP, useful as a small assist | That Peltier is efficient water heating |
| Residual TEG | Modules on a *measured-hot* surface from Generator 02 or similar | Trickle into the same storage bus | Tesla/TEG wattage without a measured ΔT |
| Circulation | 12 V DC pump, short insulated loop | Moves heat into the tank; pump is itself an energy cost | Hydraulic design complete |
| Sensing | PV V/I, storage voltage (Model 05 proxy), tank T, ambient T, optional exhaust T | Inputs to the refuse/run policy | Calibrated sensors or listed probes |
| Controller | ESP32-class MCU running the host policy port | Same Operator AI energy gate idea | On-device flash checkpoint (still host-only in this repo) |

Substitute parts only after the electrical budget is written. Do not size PV from a marketing COP.

## Electrical budget sketch (placeholders)

Write three numbers before buying parts. Until they are measured, treat them as labeled unknowns.

1. **Idle control draw** — MCU + sensors while the heat stage is off.
2. **Heat-stage electrical watts** — compressor *or* Peltier input, not tank output.
3. **Pump watts** while circulating.

The scheduler should compare `storage_joules_proxy` against `heat_stage_watts * min_run_seconds`. If the proxy cannot cover a minimum useful run, skip. Do not start a compressor for a few seconds and stall.

Model 05 helpers (`joules_from_voltage` / `voltage_from_joules`) apply only when `C_farads` is explicit. This generator does not invent C.

## Control policy (host-first)

States the firmware should eventually encode. The host stub `SANDBOX/gen03_control_stub.py` exercises the same names with caller-supplied flags (no invented joules).

- `IDLE` — sense only.
- `CHARGE` — PV present, heat stage off.
- `HEAT_PUMP_RUN` — storage above floor, tank below target, solar or storage surplus.
- `PELTIER_ASSIST` — heat-pump unavailable or conditions too poor for a compressor start; still requires a storage floor.
- `REFUSE` — floor violated, tank already at target, or sensors missing.
- `TEG_TRICKLE` — residual ΔT present; does not authorize the heat stage by itself.

Refuse beats run. Missing tank temperature is refuse, not heat.

Pseudo-policy (not production firmware):

```
if tank_T_missing or storage_V_missing:
    return REFUSE
if storage_below_floor:
    return CHARGE or IDLE
if tank_T >= target:
    return CHARGE or IDLE
if heat_pump_ok and surplus:
    return HEAT_PUMP_RUN
if peltier_ok and surplus:
    return PELTIER_ASSIST
return REFUSE
```

Host wiring to `plant_observe_ok` exists in the sandbox stub only. No on-device flash mapping and no compressor driver are claimed.

## Safety and honesty bounds
- DC heat-pump and Peltier stages still need listed electrical protection (fuse, polarity, temperature cutout). This page is not a listing.
- Mixing Generator 02 exhaust with TEG modules is a *thermal interface* problem; flue rules stay in `02-rocket-mass-biomass-hybrid/flue-clearance-and-safety.md`.
- No COP target is published here because none has been measured on a built unit.
- Water-side heat-exchanger sizing for Generator 02 remains a separate next priority.

## Next measurements (when hardware exists)
- Storage voltage vs time during a refused vs accepted heat-stage start.
- Electrical watts of the chosen heat stage at two ambient temperatures.
- Tank ΔT over a minimum useful run — still not a COP until both electrical input and thermal output are measured.
