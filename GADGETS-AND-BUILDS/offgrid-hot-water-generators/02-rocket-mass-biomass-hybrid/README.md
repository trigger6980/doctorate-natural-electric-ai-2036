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

## Water-side exchanger
Jacket / coil / mass-bench classes, potable isolation, and gravity-vs-pump honesty live in [`water-side-exchanger.md`](water-side-exchanger.md). No UA, GPM, or recovery-rate numbers are published.

A first named home-lab layout for **Class A (tank water jacket)** lives in [`home-lab-class-a-slope-sketch.md`](home-lab-class-a-slope-sketch.md). Elevations and vents only — still no measured ΔT.

## Status
Design principles, high-level BOM, first-cut flue / clearance / combustion-safety notes, first-cut water-side exchanger classes, and a Class A home-lab slope sketch are in-tree. Named-site draft measurements, measured exchanger performance, and sensor integration remain open.
