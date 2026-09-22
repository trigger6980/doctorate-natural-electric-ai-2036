# Generator 02 — Home-lab Class A slope sketch

**Chosen class:** A — tank water jacket (from [`water-side-exchanger.md`](water-side-exchanger.md)).
**Status:** named layout constraints only. No UA, GPM, recovery rate, or measured ΔT.
**Not** a listed-appliance sheet. **Not** a construction drawing set.

This sketch exists so a first home-lab build can name *where pipes go* without inventing heat-transfer numbers. Combustion path and people-safety stay in [`flue-clearance-and-safety.md`](flue-clearance-and-safety.md).

## Named home-lab intent

A short gravity loop between a jacketed storage tank and a heat-exchange barrel that sits *below* the tank. The jacket is the only water-side surface on the barrel in this sketch. Class B coils and Class C mass-bench tubes are out of scope here.

## Elevation and slope rules (layout, not measured head)

- Tank bottom sits above the highest point of the jacket so the loop can thermosiphon if the site later proves a continuous rise.
- Supply (hot) riser leaves the top of the jacket and enters the tank sidewall above the tank mid-height.
- Return (cool) leaves the tank near the bottom and enters the jacket low point.
- Every horizontal run slopes continuously toward a named high-point vent. No flat pockets.
- One high-point vent on the hot riser, serviceable without opening the tank.
- One drain at the jacket low point, piped to a safe discharge — not onto combustibles.

Slope language allowed here: “continuous rise / fall, no traps.” Slope language forbidden here: a numeric inches-per-foot presented as measured.

## Isolation (Class A)

- Jacket fluid is a **closed secondary loop**, not the potable tank volume, unless a later listed double-wall part is chosen on site.
- Fill / air-separator / relief live on the closed loop.
- No isolation valve that can trap the jacket without its own relief.
- Tank still has temperature-and-pressure relief independent of the jacket.

## Sensors that belong on this sketch

Reuse names from the water-side notes and the biome layout:

| Name | Placement on this sketch |
| --- | --- |
| `tank_t` | Upper third of the storage tank |
| `loop_t_out` | Hot riser just after the jacket exit |
| `loop_t_in` | Cool return just before the jacket inlet |

These names are placeholders. No firmware wiring is claimed.

## What a first lab session should record (not invented here)

1. Whether the hot riser is actually hotter than the return after a short fire (ΔT sign only).
2. Whether the tank temperature rises at all during that fire.
3. Whether any joint leaked or any vent spat air.

Do **not** convert those observations into watts until flow and temperatures are both measured with instruments named in a later lab note.

## Explicitly not in this sketch

- Pump. A pump would be a future energy-budget item.
- Glycol freeze point. Site choice.
- Mixing-valve product number.
- Claim that Class A outperforms Class B or C.

## Next engineering steps (not done)

1. Photograph or dimension a real bench so elevations stop being abstract.
2. Log `loop_t_out`, `loop_t_in`, and `tank_t` on the same clock.
3. Only then decide whether gravity is enough or a pump budget is required.
