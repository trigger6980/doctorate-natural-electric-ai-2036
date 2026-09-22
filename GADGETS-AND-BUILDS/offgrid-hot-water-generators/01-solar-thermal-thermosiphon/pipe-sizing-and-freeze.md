# Generator 01 — Pipe Sizing, Slope, and Freeze Protection

**Status:** engineering notes for builders. These are starting ranges, not a certified plumbing design. Local code, potable-water rules, and freeze climate govern the build. No field measurements from this repository are claimed here.

## Thermosiphon loop intent
The collector-to-tank loop relies on density difference. The hot riser must rise continuously toward the tank; the cold return must fall continuously toward the collector. Air pockets stop the loop.

## Starting pipe diameters (copper or equivalent ID)
Use these as a first cut for a single collector bank feeding one tank. Confirm pressure drop and velocity after you fix collector area.

| Daily useful hot water (order of magnitude) | Typical collector area (sunny climate) | Riser / return ID (starting range) | Notes |
| --- | --- | --- | --- |
| ~50 L | ~1 m² | 15–18 mm | Small batch or single-panel systems |
| ~100–150 L | ~2–3 m² | 18–22 mm | Common household day-use sketch |
| ~200 L | ~4 m² | 22–28 mm | Keep velocity low; avoid many elbows |

Rules of thumb (not measurements):
- Prefer short, smooth runs over long, elbow-heavy runs.
- Match collector header ID rather than undersizing the riser.
- Do not use a smaller return than the riser without a reason recorded in the build log.

## Slope and layout
- Continuous rise from collector outlet to tank inlet: target **≥ 1:20** (5 cm rise per metre of run) where the site allows.
- No horizontal sag. Any dip needs a high-point air vent or a redesign.
- Tank heat-exchanger coil (if used) should sit above the collector top by a clear vertical offset so the thermosiphon has a driving head.
- Isolation valves and a drain at the low point so the loop can be emptied for freeze or service.

## Freeze-protection strategies (choose by climate)
Document which strategy you actually built. Mixing them without a drawing causes stagnation and burst pipes.

1. **Drain-back (preferred where the site can slope).** Water leaves the collector when circulation stops. Needs a drain-back reservoir and no trapped high points in the collector itself.
2. **Closed loop + antifreeze heat exchanger.** Collector loop uses a non-toxic heat-transfer fluid rated for the design low temperature. Potable water stays on the tank side. Requires a pressure-relief path and a labeled fluid.
3. **Recirculation / dump** (only if a small harvested-energy pump is in the BOM). Circulate or dump heat when collector temperature approaches freeze. This is *not* a passive system anymore; log the watt-hours.
4. **Seasonal drain.** Simplest in climates with a hard winter and unused collectors. Must be written into the operator checklist.

Stagnation (no flow, full sun) is a separate failure mode from freeze. Include a pressure-relief / temperature-relief path on the collector loop and a tempering valve on the delivery side so tap water cannot exceed a safe mixed temperature.

## Safety notes (minimum)
- Tempering / mixing valve on the delivered hot line.
- Temperature-pressure relief on the storage tank per local code.
- No unmarked glycol in a potable loop.
- Scald and steam risk at stagnation; treat collector fittings as hot-work.
- This file is not a permit drawing.

## What still needs measurement
- Actual rise, run length, and elbow count for a named site.
- Freeze-hour climate file for that site.
- Collector stagnation temperature on a no-load day.
- Sensor integration with `energy-harvester-tinyml` (collector T, tank T).

## Next slice
Wire two temperature placeholders into the host scheduler sketch and record units in the build log. Hardware ADC mapping remains open.
