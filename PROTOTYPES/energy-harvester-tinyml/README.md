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

## Software Architecture

```
energy_state = read_supercap_voltage()          # proxy for available energy
prediction   = tiny_lstm_or_rf.predict(lux_history)  # optional forecast
action       = policy(energy_state, prediction) # SENSE / INFER / TX / SLEEP
execute(action)
log_and_sleep_until_next_slot()
```

Policy can be a simple threshold rule or a quantized RL policy trained offline.

## Directory Layout

- `src/` — core C++/MicroPython or Arduino sketches
- `models/` — quantized models (placeholder for now)
- `tests/` — energy and functional tests
- `docs/` — measurement methodology

## Status
Skeleton. Core scheduler sketch and test harness structure pushed. Full quantized models, real energy traces, and hardware photos are next vertical slices.

## Reproducibility
All code is intended to compile and run on commodity ESP32 boards. No proprietary silicon required.
