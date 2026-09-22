# Generator 02 — Water-Side Heat Exchanger Notes

**Status:** first-cut planning notes. Separate from flue / clearance / combustion safety.
**Not** a listed-appliance sheet. **Not** a measured UA, LMTD, or recovery-rate table.

Flue, draft, and people-safety live in [`flue-clearance-and-safety.md`](flue-clearance-and-safety.md). This file only talks about how water might pick up heat *after* combustion gases are already in a designed path.

## Allowed exchanger classes (choose one family per build)

| Class | Sketch | Why it is listed | What this repo does **not** claim |
| --- | --- | --- | --- |
| A — tank water jacket | Annular or wrap jacket on the storage tank, fed from a short gravity loop near the heat-exchange barrel | Simple, few joints, inspectable | No watt rating |
| B — coil in heat-exchange barrel | Copper or stainless coil in the barrel / bell, closed loop to the tank | Higher ΔT near the riser | No coil length formula presented as measured |
| C — tubes in thermal mass | PEX or copper embedded in cob/brick bench after the barrel | Residual heat after the fast path | No claim that mass replaces a relief valve |

Do not mix Class B combustion-side coils with potable water unless the loop is explicitly closed and isolated. Prefer a closed loop + tank coil for potable service.

**Home-lab pick:** Class A is the named first sketch — [`home-lab-class-a-slope-sketch.md`](home-lab-class-a-slope-sketch.md).

## Isolation and potable-water rule

- Potable tank water should not be the same fluid that sits inside a combustion-adjacent coil unless a listed double-wall exchanger is used. This repo does not specify a listed part number.
- A closed secondary loop (water or water-glycol) with its own fill, air separator, and relief is the default sketch.
- Glycol is a *site choice*. No freeze-point table is published here.

## Gravity vs pumped (honesty)

- Default sketch: **gravity / thermosiphon on the water side** only if the coil sits below the tank and piping slopes continuously. That is a layout constraint, not a measured head.
- A pump is allowed only as a future energy-budget item. Do not assume a pump in the Operator AI policy until joules for that pump are measured.

## Sizing language that is allowed vs forbidden

Allowed:
- Name the class (A/B/C).
- Name pipe family (copper / stainless / PEX) and that joints must be serviceable.
- State that exchanger area must be *designed on site* from desired tank ΔT and available gas temperature — then measured.

Forbidden in this file and in enterprise quotes that cite it:
- Invented kW, GPM, or “recovers X gallons per hour.”
- Copying a vendor UA and calling it this build’s result.
- Treating mass-bench tubes as a substitute for temperature-and-pressure relief on the tank.

## Sensor placeholders that belong on the water side

| Name | Meaning | Used for |
| --- | --- | --- |
| `tank_t` | Stored water temperature | Domestic priority vs leftover heat to food zone |
| `loop_t_out` | Exchanger outlet (closed loop) | Detect no-flow or dry coil |
| `loop_t_in` | Exchanger inlet | Crude ΔT only; not a wattmeter |

These names match the biome layout document. They are not wired to firmware in this commit.

## Safety that remains on the water side

- Temperature-and-pressure relief on the tank, piped to a safe discharge.
- No isolation valve that can trap the coil without its own relief.
- Anti-scald mixing for any fixture — product selection is site work.
- Do not use the rocket path as the only freeze protection for the potable tank.

## Next engineering steps (not done)

1. Pick one class for a named home-lab sketch. **Done for Class A** — see [`home-lab-class-a-slope-sketch.md`](home-lab-class-a-slope-sketch.md).
2. Draw pipe slopes and high-point vents on a *dimensioned* bench (still open).
3. Measure `loop_t_out - loop_t_in` *and* tank rise before anyone writes watts.
