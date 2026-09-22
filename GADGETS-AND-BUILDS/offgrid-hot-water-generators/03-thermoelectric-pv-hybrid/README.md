# Generator 03 — Thermoelectric + PV Hybrid Heat-Pump Assist

## Principle
A low-power heat-pump or thermoelectric (Peltier) module is driven by PV + modest energy storage (battery or supercapacitor). The system prioritizes efficiency when electricity is scarce and can fall back to pure resistive or passive modes. Thermoelectric generators can also harvest residual heat from other sources (e.g., rocket stove exhaust) to produce a small amount of electricity that helps run circulation or controls.

## Key Components (BOM outline)
- PV array sized for the heat-pump / thermoelectric load + controls
- Charge controller + modest battery or supercapacitor bank
- Low-power DC heat-pump or thermoelectric heating module
- Heat exchanger and insulated storage
- Optional TEG (thermoelectric generator) modules on residual heat sources
- Sensors: PV voltage/current, storage state-of-charge, water temperature, ambient
- Microcontroller (ESP32 or similar) running energy-aware policy

Detail and refuse/run states: [component-selection-and-control.md](component-selection-and-control.md). Planning ranges only; no measured COP.

## Performance Notes
- Highest system-level efficiency when the heat-pump coefficient of performance (COP) is leveraged under good conditions.
- Can operate at very low power draw compared with pure resistive electric water heating.
- Naturally integrates with the existing energy-harvester-tinyml and Operator AI Machinery work.
- More complex and higher capital cost than pure solar thermal or rocket systems, but excellent for electrified off-grid biomes.

## Control Sketch
The energy-aware scheduler (Model 01 and successors) decides when to run the heat-pump / thermoelectric stage based on storage state, solar forecast, and current hot-water priority. Residual-heat TEGs can trickle-charge the same storage. Named host states (`IDLE`, `CHARGE`, `HEAT_PUMP_RUN`, `PELTIER_ASSIST`, `REFUSE`, `TEG_TRICKLE`) live in the component-selection note. Firmware is not wired yet.

## Status
Architecture, component classes, placeholder electrical budget, and control-state names are documented. COP targets and on-device firmware remain open until hardware exists.
