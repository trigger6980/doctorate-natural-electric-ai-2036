# Off-Grid Hot Water Generators + Sustainable Living Biomes

**Natural Electric track extension** — Three practical, reproducible off-grid hot-water generation systems designed for integration into sustainable living biomes (closed-loop energy / water / food / waste systems).

## Design Philosophy
- Zero or near-zero grid dependence after installation.
- Prefer passive or low-power active systems that can run on harvested energy (solar, biomass, residual heat, thermoelectric).
- Modular so they can be combined inside a larger biome.
- Open BOMs, clear physics, and control sketches that an independent builder or research team can reproduce.
- Energy state remains a first-class signal (compatible with the energy-harvester-tinyml and Operator AI Machinery work).

## The Three Generators

| # | Name | Primary Energy Source | Peak / Typical Output | Best Fit |
|---|------|-----------------------|-----------------------|----------|
| 1 | Solar Thermal Thermosiphon + Batch | Solar (direct thermal) | 50–200 L/day depending on collector area & climate | Sunny climates, low-tech reliability |
| 2 | Rocket-Mass / Biomass Hybrid Heater | Biomass (wood, agricultural waste) + residual heat recovery | High short-term output, excellent for cold climates | Areas with sustainable biomass |
| 3 | Thermoelectric + PV Hybrid Heat Pump Assist | Solar PV + thermoelectric / low-power heat-pump assist | Moderate continuous output, highest efficiency when electricity is scarce | Variable climates, integration with existing PV + battery/supercap systems |

Detailed design files for each generator live in their respective subfolders.

## Sustainable Living Biome Integration
Each generator is intended to plug into a larger closed-loop biome that also handles:
- Rainwater / greywater capture and treatment
- Food production (greenhouse, aquaponics, or soil-based)
- Waste-to-resource loops (compost, biogas optional)
- Local energy storage and intelligent duty-cycling (links to energy-harvester-tinyml and Operator AI Machinery)

See `sustainable-living-biomes/` for the overarching biome architecture.

## Status
Initial design documentation and BOMs pushed. Control sketches and measurement protocols will be added in subsequent vertical slices. Physical builds and performance data will be documented as they are completed.
