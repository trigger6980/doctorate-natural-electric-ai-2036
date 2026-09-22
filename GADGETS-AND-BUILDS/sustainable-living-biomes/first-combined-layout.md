# First Combined Biome Layout (Energy + Water + Basic Food)

**Status:** schematic only. No site, no measured yields, no claimed self-sufficiency days.

This is the first combined layout that sits the three hot-water generators next to a water loop and a small food loop. It exists so later sensor and control work has named zones instead of a blank page.

## Zones (names only)

| Zone | Role | Coupled generators |
| --- | --- | --- |
| Z-E energy pad | PV array, optional thermoelectric stack, supercap / battery placeholder | Gen 03 primary, Gen 01 collector nearby |
| Z-T thermal spine | Collector → tank → distribution, plus biomass backup path | Gen 01 thermosiphon, Gen 02 water jacket |
| Z-W water | Rain capture, first-flush, cold store, hot store, greywater hold | All three generators as heat users |
| Z-F food | One raised bed or greenhouse bay that can take residual warmth and greywater after treatment | Heat from Z-T; nutrients from compost, not claimed biogas |
| Z-C control | Host / off-grid AI box, Operator AI task graph, sensor placeholders | Observes, does not invent joules |

## Suggested adjacency (plan view, not a CAD file)

```
        [rain catchment]
              |
         [first-flush] ----> [cold cistern] ----> [hot tank / Gen01+02]
              |                                         |
         [grey hold] <--- kitchen/bath                  |
              |                                         v
         [treated grey] ----> [Z-F bed / greenhouse] <--+ residual warmth

  [Z-E PV / TEG pad] --electric--> [Z-C control + supercap placeholder]
  [Gen 02 combustion] --flue (see flue notes)--> stack, *not* through food zone
```

Combustion air and flue stay isolated from Z-F. Do not route rocket exhaust through a greenhouse.

## Energy + water + food couplings that are allowed in this sketch

- Gen 01 heats the hot tank when sun is present (thermosiphon; no pump claimed).
- Gen 02 heats the same tank through a *separate* water-side exchanger (see `../offgrid-hot-water-generators/02-rocket-mass-biomass-hybrid/water-side-exchanger.md`).
- Gen 03 may tap a *small* ΔT on the thermal spine or a dedicated cook-stove face; it does not justify a COP claim.
- Z-F may receive leftover tank heat via a low-temperature loop **after** domestic hot-water priority. Priority order is a policy, not a measured schedule.
- Z-C may later subscribe to named sensor placeholders: collector T, tank T, exhaust T, cistern level, bed soil T. Those sensors are not wired in this file.

## Explicit non-claims

- No calorie yield, no liters-per-day, no kWh-per-day.
- No statement that one household is covered.
- No combined control policy executable here — only zone names for a future policy.
- Compost is assumed aerobic and outdoor; biogas is out of scope for this layout.

## Next layout steps

1. Bind collector T / tank T / exhaust T names to the host scheduler sketch.
2. Add a cistern-level placeholder (empty / low / ok / full) without inventing liters.
3. Keep food-loop irrigation as gravity or hand-carry until a pump energy budget is measured.
