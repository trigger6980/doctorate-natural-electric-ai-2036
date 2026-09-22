# Generator 01 — Solar Thermal Thermosiphon + Batch Heater

## Principle
Passive solar thermal collectors heat water. Density-driven thermosiphon circulation moves hot water to an insulated storage tank without pumps. A simple batch heater variant can be used for smaller or lower-cost installations.

## Key Components (BOM outline)
- Flat-plate or evacuated-tube solar collector (area sized to daily hot-water demand and local insolation)
- Insulated storage tank (preferably with heat exchanger coil)
- Thermosiphon loop piping (correct slope and diameter critical)
- Tempering / mixing valve for safe delivery temperature
- Optional: small PV-powered circulation pump as backup or for forced systems
- Sensors: collector temperature, tank temperature, optional flow

## Performance Notes
- Typical useful output in good sun: 40–80 L of 40–60 °C water per m² of collector per day (highly climate-dependent).
- Completely passive when designed correctly — zero operating energy.
- Freeze protection and stagnation protection must be designed for the local climate.

## Control / Monitoring Sketch
Temperature sensors on collector and tank can feed the energy-aware scheduler. When tank is already hot, collector loop can be isolated or excess heat diverted (e.g., to thermal mass or a second priority load).

## Status
Design principles and BOM outline complete. Detailed pipe sizing tables, freeze-protection strategies, and sensor integration code will follow.
