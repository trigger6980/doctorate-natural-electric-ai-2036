# First Concrete Sustainable Living Biome Layout

**Dyad process:** Lumen designed a minimal closed-loop household-scale biome. Aegis constrained it to what can actually be built and monitored with the tools already in this repository.

## Design Goal
Support a small research station or 1–2 person household with:
- Reliable hot water
- Basic electricity for controls, lighting, and communications
- Modest food production
- Water capture and basic treatment
- Intelligent prioritization when energy or water is scarce

## Spatial / Functional Layout (Logical)

```
[Solar Thermal Collector Array] ----thermosiphon----> [Insulated Hot Water Tank]
         |                                              |
         | (optional heat dump)                         +-- tempered hot water to use points
         v
[Rocket-Mass Heater with Water Heat Exchanger] --------+
         |
         +-- residual heat --> thermal mass / greenhouse

[PV Array] --> [MPPT + Storage] --> [ESP32 Energy-Aware Controller]
                                      |
                                      +-- drives circulation pumps, heat-pump/TEC (Gen 03)
                                      +-- monitors all temperatures & voltages
                                      +-- talks to Operator AI / local off-grid AI box

[Rainwater Catchment] --> [First-flush + Storage Cistern] --> [Basic filtration] --> cold water + makeup

[Greenhouse / Growing Beds] <--- thermal mass + greywater nutrients (carefully managed)
```

## Priority Order When Resources Are Limited (Operator AI Policy Sketch)
1. Protect storage voltage / energy state (never deep-discharge critical controls).
2. Maintain freeze protection and combustion safety interlocks.
3. Keep hot-water tank above a minimum usable temperature if solar or biomass is available.
4. Run food-production environmental controls (ventilation, minimal lighting) only when energy surplus exists.
5. Log state and defer non-essential tasks.

## Water Loop
- Rainwater primary source.
- Greywater from sinks (not toilets in first version) directed to mulch basins or carefully designed plant beds after basic settling/filtration.
- Hot water is a high-value output; cold water is prioritised for drinking after proper treatment.

## Food Loop (Minimal)
- Small greenhouse or protected beds that benefit from residual heat of the rocket-mass system and from the thermal mass of the hot-water tank.
- Compost from kitchen and garden waste returns nutrients.

## Monitoring & Control
All critical temperatures, voltages, and tank levels become inputs to the energy-aware scheduler and Operator AI Machinery already defined in this repository. The off-grid AI box can host local dashboards and knowledge without external connectivity.

## Status
First concrete logical layout complete. This is a planning and integration document, not a full construction blueprint. Dimensional drawings, exact plumbing schematics, and local-code compliance remain the responsibility of the builder and must incorporate the safety guidance from Generators 01 and 02.
