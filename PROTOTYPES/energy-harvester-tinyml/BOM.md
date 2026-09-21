# Bill of Materials — Energy-Harvester TinyML Node

## Minimum Viable (ESP32-C3 path)

- ESP32-C3-MINI or DevKit — low-power WiFi/BLE MCU
- Small monocrystalline or indoor PV cell (5 V class)
- Power-path / MPPT board (e.g. DFRobot Sun Power Manager or equivalent)
- Supercapacitor 0.47 F – 1 F (or small LiPo + protection)
- Optional: BH1750 or analog lux sensor, DHT22 / BME280
- Enclosure suitable for outdoor or indoor placement

## Extended (Pi Zero path for larger models)

- Raspberry Pi Zero 2W
- Larger solar panel (6–10 W) + charge controller
- LiPo pack with capacity matched to expected duty cycle
- Same sensor suite

## Notes
Costs are approximate 2026 retail. Prefer open, commodity parts so independent researchers can reproduce. Update this file with exact part numbers and links as builds are validated.
