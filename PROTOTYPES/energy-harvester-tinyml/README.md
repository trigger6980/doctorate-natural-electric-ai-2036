# Energy-Harvester TinyML Node

**Natural Electric prototype #1** — Self-powered or energy-aware edge node that treats harvested energy as a first-class runtime signal.

## Goal
Demonstrate a minimal, reproducible system in which:
- Ambient energy (primarily indoor/outdoor PV + optional magnetic/RF) charges a supercapacitor or small battery.
- Voltage (or estimated energy state) is observed by the MCU.
- A quantized TinyML model (or simple policy) decides whether to sense, infer, transmit, or sleep.
- The node aims for energy-neutral or near-perpetual operation under realistic light/vibration traces.

## Hardware Target (BOM)

| Item | Example / Notes | Approx. Cost |
|------|-----------------|--------------|
| MCU | ESP32-C3 or ESP32-S3 (or Raspberry Pi Zero 2W for larger models) | $3–$15 |
| Solar / Indoor PV | 5V 1W outdoor panel or indoor DSSC/OPV evaluation cell | $5–$25 |
| Power manager | DFRobot Sun Power Manager or equivalent MPPT + battery/supercap charger | $10–$20 |
| Storage | 0.47F–1F supercapacitor or small LiPo | $2–$8 |
| Sensors | Temperature, light (lux), optional vibration/magnetic | $2–$10 |
| Optional | BLE/WiFi already on ESP32; external antenna for better harvest monitoring | — |

Full schematic guidance and photos will be added as physical builds are completed. Start with ESP32-C3 + small solar + supercap for lowest power.

See also [`BOM.md`](BOM.md).

## Software Architecture

```
energy_state = read_supercap_voltage()          # proxy for available energy
prediction   = tiny_lstm_or_rf.predict(lux_history)  # optional forecast
action       = policy(energy_state, prediction) # SENSE / INFER / TX / SLEEP
execute(action)
log_and_sleep_until_next_slot()
```

Policy can be a simple threshold rule or a quantized RL policy trained offline.

Host-side helpers already in tree:
- `src/energy_aware_scheduler.py` — threshold / policy skeleton
- `src/supercap_voltage_proxy.py` — analytic voltage↔joules helper (uncalibrated; C must be supplied)
- Tests under `tests/` run on CI via `.github/workflows/host-tests.yml`

## Directory Layout

- `src/` — core Python host stubs (and future C++/MicroPython / Arduino sketches)
- `models/` — quantized models (placeholder for now)
- `tests/` — energy and functional tests (host)
- `docs/` — measurement methodology (to be filled when lab method exists)

## Status (honest)

**Present:** Host scheduler skeleton, uncalibrated supercap voltage proxy, unit tests, and a commodity-oriented BOM.

**Not present:** Trained/quantized on-device models, measured field joules, calibrated C for the voltage proxy, hardware photos, or energy-neutral certificates.

This prototype maps to Model 01 (Threshold Energy Scheduler) and Model 05 (Supercap Voltage Proxy) in the Genetic / Architectural Model Database. Host numbers are not field certificates.

## Next vertical slices (ordered, no invented claims)

1. Capture a short host voltage log under controlled indoor light (still host, not field certificate).
2. Wire a real ESP32-C3 ADC read into the same policy interface used by the host tests.
3. Add a measurement-method note under `docs/` once a lab and instrument class are named (see ENTERPRISE/measurement-method.md).
4. Only after (3): publish a labeled result record if joules are measured.

## Reproducibility
All host code runs under the public CI workflow. Board firmware targets commodity ESP32 boards. No proprietary silicon required. Physical builds remain open work.
