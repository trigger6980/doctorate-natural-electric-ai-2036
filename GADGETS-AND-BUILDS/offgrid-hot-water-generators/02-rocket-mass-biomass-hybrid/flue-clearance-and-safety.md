# Generator 02 — Flue, Clearance, and Combustion Safety Notes

**Status:** engineering notes for builders. These are starting ranges drawn from common rocket-mass / masonry-heater practice, not a certified stove design, not a flue calculation for a named site, and not a fire-code approval. Local building and solid-fuel codes govern the build. No field measurements from this repository are claimed here.

Combustion appliances kill people when draft, clearance, or carbon monoxide are treated as optional. Read this file as a checklist of *what must be decided on paper before lighting a first fire*, not as permission to skip a licensed inspection where one is required.

## Design intent (what this file covers)
- Combustion chamber / J-tube or batch-box envelope
- Insulated riser
- Heat-exchange path (water jacket, coil, or mass bench with embedded tubes)
- Exhaust / flue to outdoors
- Clearances to combustibles and operator access

It does **not** size a water-side heat exchanger. That remains a later slice.

## Starting dimensional ranges (first cut only)
Use these only to start a drawing. Confirm against the fuel you will actually burn and the flue height you can actually build.

| Element | Starting range | Why it is here | What you must still measure |
| --- | --- | --- | --- |
| Feed / burn-tunnel ID (J-tube style) | 150–200 mm square equivalent for household heat | Too small starves air; too large cools the burn | Fuel diameter you will split to |
| Insulated riser height | ≥ 2–3× burn-tunnel hydraulic diameter | Riser is the engine; short risers smoke | Stack temperature at riser exit on a test fire |
| Riser insulation | High-temp ceramic or equivalent; not ordinary fiberglass | Skin temperature and draft both depend on it | Skin temp vs clearance chosen |
| Heat-exchange run after riser | Long, mildly sloped, never a sudden choke | Extract heat without killing draft | Draft at the flue cap with all exchangers in place |
| Flue ID after heat exchange | Not smaller than the burn-tunnel ID without a calculated reason | Choke points make CO and smoke | Draft reading (Pa or inH2O) at several fire rates |
| Flue vertical rise above roof | Follow local solid-fuel code (often well above ridge) | Wind and re-entrainment | Site wind and neighboring openings |

Batch-box style systems use a different firebox geometry. Do not mix J-tube numbers onto a batch box without redrawing the air path.

## Draft and flue rules of thumb (not measurements)
- The flue must terminate outdoors. Indoor dump of rocket exhaust is not a design option in this portfolio.
- Horizontal runs after the heat-exchange section should stay short and rise, not sag. Condensate and creosote collect in sags.
- A clean-out at every direction change that a brush cannot pass.
- A way to inspect the riser and the first heat-exchange turn without demolishing the mass.
- Do not add a water jacket that can boil closed. The water side needs a relief path independent of the flue.

If the system smokes at the feed on a cold start, that is a draft / riser / moisture problem. It is not solved by shrinking the flue.

## Clearances to combustibles (minimum planning numbers)
Treat every number below as a *planning floor* until the local inspector or a listed appliance sheet says otherwise.

- Uninsulated single-wall flue or exposed steel near the burn path: plan **900 mm** to wood, furniture, or stores unless a tested clearancesheet exists for that exact assembly.
- Insulated riser skin: still treat as hot. Plan **300–450 mm** until you have a measured skin temperature at full fire.
- Floor protection under the feed and ash path: non-combustible, larger than the ember scatter you will actually produce.
- Water-side piping through mass: dielectric and mechanical isolation so a leak does not quench the burn tunnel from the inside.

Write the clearance you built on the operator card. “Looks fine” is not a recorded clearance.

## Combustion and people safety (minimum)
- Working carbon monoxide alarm in every occupied room that shares air with the appliance, plus one near sleeping areas.
- A plan for makeup air. Tight cabins starve rocket stoves.
- Dry fuel only. Wet biomass makes tar, not heat.
- Never leave a new system unattended through its first ten fires.
- Pressure-temperature relief on any closed water jacket or tank, piped to a safe dump.
- No steam-tight coil without a listed relief device.
- Ash handling: metal container, outdoors, cold.

This file is not a CO-certification, not a UL / CE listing, and not a permit drawing.

## Hybrid note (solar + biomass)
When this generator is the backup to Generator 01, the two heat sources must not be able to lock a tank or coil with no relief. Document which source is primary, which valves isolate which loop, and which sensor tells Operator AI that a fire is lit.

## What still needs measurement
- Riser exit temperature and flue-cap draft on a named fuel and a named stack height.
- Skin temperatures at the planned clearance.
- Water-side ΔT across the jacket or coil at a recorded burn rate.
- CO at operator breathing height during cold start and steady fire.
- Sensor hooks (exhaust T, water T, optional draft) into the host scheduler sketch.

## Next slice
Component selection and a control-code sketch for Generator 03 (thermoelectric + PV hybrid), then a first combined biome layout. Hardware ADC mapping remains open.
