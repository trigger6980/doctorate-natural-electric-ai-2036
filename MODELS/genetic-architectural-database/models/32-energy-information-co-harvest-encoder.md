# 32 — Energy-Information Co-Harvest Encoder

**Domain:** Dual Harvest  
**Energy Profile:** Ultra-low (uncalibrated)  
**Status:** Catalog + interface specification (no co-harvest transducer, no measured bit-per-joule, no dual-harvest certificate)  
**Operator role:** Optional host gate that refuses an encode-plus-store step when the rail cannot pay the next sample-plus-pack pair, or when the named bit budget is missing. Not a production RF-energy/comms encoder and not a harvest certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *sample_e*, *pack_bits*, *store*, or *unknown*. A full co-harvest stack (shared antenna or piezo path that both charges a rail and encodes a packet, measured bits-per-joule, listed RF certificate) is out of scope until a named bit budget and plant bounds exist on the intended node.

This card specifies the host-facing interface. There is **no co-harvest transducer, no public BER curve, and no measured joule-per-bit** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- An encode decision is a *policy event*, not proof a physical wave both charged the rail and carried payload.
- Host evaluation of a fixture bit budget on a laptop is not a dual-harvest certificate.
- Do not claim RF energy-harvesting radios, simultaneous wireless information and power transfer (SWIPT) products, or “certified co-harvest AI” status from this card.
- Distinct from Model 13: Model 13 gates a magnetic-field harvest *predictor*. This card gates an *encode-plus-store* step that claims a shared energy/information path.
- Distinct from Model 14: Model 14 extracts vibration/TENG features. This card does not claim a piezo driver.
- Distinct from Model 18: Model 18 gates mesh routing policy. This card does not drive a radio hop.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `bit_budget` | input | Named placeholder payload width. Uncalibrated |
| `pack_bounds` | input | Named placeholder pack limits. Uncalibrated; not a live transducer |
| `coh_id` | input | Ancestry id (`32` or `32-custom-<slug>`). Not a radio lot |
| `max_bits` | input | Design cap. Wider packets are out of this card |
| `coh_action` | output | `hold` / `sample_e` / `pack_bits` / `store` / `unknown` |
| `bits_issued` | output | Planned width after the action |
| `coh_ok` | output | Boolean: the next sample-plus-pack pair may run |
| `refuse_reason` | output | `energy` / `missing_bits` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `coh_step(energy_state, bit_budget, pack_bounds) -> coh_action`
- `coh_ok(energy_state, bit_budget, pack_bounds) -> bool`
- `gate_task(task_id, coh_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture bit budget on the laptop CI runner; that is still not a co-harvest transducer.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse pack_bits unless a host JSON path exists.
4. Model 32 `coh_ok()` — refuse sample/pack unless the named sizes fit.
5. Only then `gate_task(allow)` for the encode step.

Missing bit-budget fields must refuse with `missing_bits`. An `unknown` action must skip the sample-pack pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or transducer before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-store | 0.001–0.05 J | Cheap compares, not BER traces |
| Skip (`coh_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 32 |
| On-device sample_e + pack_bits | unknown | Do not schedule until measured |
| Listed dual-harvest path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule a sample_e or pack_bits when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `store` as proof the *physical path* both charged the rail and delivered bits — only that the named sizes fit the budget.
- Do not invent bits-per-joule, carrier frequency, or SWIPT efficiency numbers in host logs.

## Key Traits
- Co-harvest lite is a refuse/allow gate, not a certified dual-harvest runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any analog sample on a shared transducer
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_bits` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, or `ion`. Keep joule costs labeled uncalibrated until an MCU/transducer measurement exists. Do not check RF recipes or SWIPT firmware into this public card.

## Next measurements (not done)
- Time and current for sample_e vs pack_bits vs hold on the intended runtime.
- Decide whether bit budget is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a dual-harvest certificate.
- Optional host stub: `coh_ok()` on a fixture bit budget in CI — still not a co-harvest transducer.
