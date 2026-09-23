# 31 — Ionic Synapse Conductance Model

**Domain:** Neuromorphic Materials  
**Energy Profile:** Research (uncalibrated)  
**Status:** Catalog + interface specification (no wet-lab cell, no measured siemens-per-joule, no materials certificate)  
**Operator role:** Optional host gate that refuses a conductance-update step when the rail cannot pay the next write-plus-read pair, or when the named channel count is missing. Not a production memristor/ionic runtime and not a materials certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *write_g*, *read_g*, *settle*, or *unknown*. A full ionic-synapse stack (electrolyte cell, measured conductance curve, listed materials certificate) is out of scope until a named channel count and plant bounds exist on the intended node.

This card specifies the host-facing interface. There is **no wet-lab cell, no public I-V curve, and no measured joule-per-write** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A conductance decision is a *policy event*, not proof a physical synapse changed state.
- Host evaluation of a fixture channel count on a laptop is not a materials certificate.
- Do not claim memristor foundry parts, living-tissue synapses, or “certified ionic AI” status from this card.
- Distinct from Model 08: Model 08 is an event-driven spiking encoder gate. This card gates an *ionic write/read* step.
- Distinct from Model 30: Model 30 gates a reservoir inject/read. This card does not claim echo-state dynamics.
- Distinct from Model 28: Model 28 gates actuator motion. This card does not drive motors.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `channel_count` | input | Named placeholder synapse width. Uncalibrated |
| `g_bounds` | input | Named placeholder conductance limits. Uncalibrated; not a live cell |
| `ion_id` | input | Ancestry id (`31` or `31-custom-<slug>`). Not a materials lot |
| `max_channels` | input | Design cap. Wider arrays are out of this card |
| `ion_action` | output | `hold` / `write_g` / `read_g` / `settle` / `unknown` |
| `channels_issued` | output | Planned width after the action |
| `ion_ok` | output | Boolean: the next write-plus-read pair may run |
| `refuse_reason` | output | `energy` / `missing_channels` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `ion_step(energy_state, channel_count, g_bounds) -> ion_action`
- `ion_ok(energy_state, channel_count, g_bounds) -> bool`
- `gate_task(task_id, ion_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture channel count on the laptop CI runner; that is still not a wet-lab cell.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse write_g unless a host JSON path exists.
4. Model 31 `ion_ok()` — refuse write/read unless the named sizes fit.
5. Only then `gate_task(allow)` for the conductance step.

Missing channel fields must refuse with `missing_channels`. An `unknown` action must skip the write-read pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or materials cell before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-settle | 0.001–0.05 J | Cheap compares, not I-V traces |
| Skip (`ion_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 31 |
| On-device write_g + read_g | unknown | Do not schedule until measured |
| Listed materials-cell path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a write_g or read_g when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `settle` as proof the *physical channel* reached a stable siemens value — only that the named sizes fit the budget.
- Do not invent mobility, ion species, or joules-per-write numbers in host logs.

## Key Traits
- Ionic-synapse lite is a refuse/allow gate, not a certified materials runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any analog write to a cell
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_channels` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, or `res`. Keep joule costs labeled uncalibrated until an MCU/materials measurement exists. Do not check wet-lab recipes into this public card.

## Next measurements (not done)
- Time and current for write_g vs read_g vs hold on the intended runtime.
- Decide whether channel count is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a materials certificate.
- Optional host stub: `ion_ok()` on a fixture channel count in CI — still not a wet-lab cell.
