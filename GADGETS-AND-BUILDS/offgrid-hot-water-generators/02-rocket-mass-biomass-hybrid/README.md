# Generator 02 — Rocket-Mass / Biomass Hybrid Hot Water Heater

## Principle
High-efficiency rocket stove or rocket mass heater combusts small-diameter wood or agricultural biomass. Exhaust path is routed through a heat exchanger (water jacket, copper coil, or thermal-mass bench with embedded water tubes) to capture a large fraction of the heat for domestic hot water and space heating.

## Key Components (BOM outline)
- Rocket stove combustion unit (J-tube or batch-box style)
- Insulated riser and heat-exchange section
- Water jacket or copper coil heat exchanger
- Insulated storage tank
- Optional thermal mass (cob, brick, or stone) for residual heat storage
- Safety: pressure relief, temperature relief, proper clearances, and flue design
- Sensors: exhaust temperature, water temperature, optional CO / draft monitoring

## Performance Notes
- Very high combustion efficiency when designed correctly (often >80–90 % of available heat captured in well-built systems).
- Excellent for cold climates or locations with sustainable local biomass.
- Requires responsible fuel sourcing and operator training.
- Can be combined with solar thermal as a hybrid (solar primary, biomass backup).

Those efficiency figures are literature ranges for well-built systems, not measurements from this repository.

## Control / Monitoring Sketch
Exhaust and water temperatures feed safety interlocks and the Operator AI / energy-aware layer. System can signal when biomass firing is needed versus when solar has already satisfied demand.

## Safety-critical notes
Dimensional ranges, flue / draft rules of thumb, clearances to combustibles, and the minimum people-safety checklist live in [`flue-clearance-and-safety.md`](flue-clearance-and-safety.md). Those notes are a first cut, not a listed-appliance sheet.

## Status
Design principles, high-level BOM, and first-cut flue / clearance / combustion-safety notes are in-tree. Water-side exchanger sizing, named-site draft measurements, and sensor integration remain open.
