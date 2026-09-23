# 30 — Neuromorphic Reservoir Computer

**Domain:** Physical Reservoir  
**Energy Profile:** Ultra-low–Low  
**Status:** Catalog + interface specification (no analog reservoir, no measured echo-state joules, no physical-node certificate)  
**Operator role:** Optional host gate that refuses a reservoir step when the rail cannot pay the next inject-plus-read pair, or when the named state size is missing. Not a production neuromorphic runtime and not a physical-reservoir certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *inject*, *read*, *classify*, or *unknown*. A full reservoir stack (analog node, echo-state weights, measured joules-per-step, listed physical certificate) is out of scope until a named state size and plant bounds exist on the intended node.

This card specifies the host-facing interface. There is **no analog reservoir, no public weight file, and no measured joule-per-step** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A reservoir decision is a *policy event*, not proof the plant was classified safely.
- Host evaluation of a fixture state vector on a laptop is not a field echo-state certificate.
- Do not claim analog neuromorphic hardware, liquid-state machines, or “certified reservoir AI” status from this card.
- Distinct from Model 08: Model 08 is an event-driven spiking encoder gate. This card gates a *reservoir inject/read* step.
- Distinct from Model 21: Model 21 is a quantized forest policy. This card does not train trees.
- Distinct from Model 29: Model 29 gates video rollout frames. This card does not encode frames.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `state_size` | input | Named placeholder reservoir width. Uncalibrated |
| `inject_bounds` | input | Named placeholder limits. Uncalibrated; not a live analog node |
| `res_id` | input | Ancestry id (`30` or `30-custom-<slug>`). Not a weight hash |
| `max_state` | input | Design cap. Wider reservoirs are out of this card |
| `res_action` | output | `hold` / `inject` / `read` / `classify` / `unknown` |
| `state_issued` | output | Planned width after the action |
| `res_ok` | output | Boolean: the next inject-plus-read pair may run |
| `refuse_reason` | output | `energy` / `missing_state` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `res_step(energy_state, state_size, inject_bounds) -> res_action`
- `res_ok(energy_state, state_size, inject_bounds) -> bool`
- `gate_task(task_id, res_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture state size on the laptop CI runner; that is still not an analog reservoir.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse inject unless a host JSON path exists.
4. Model 30 `res_ok()` — refuse inject/read unless the named sizes fit.
5. Only then `gate_task(allow)` for the reservoir step.

Missing state fields must refuse with `missing_state`. An `unknown` action must skip the inject-read pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or analog node before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-classify | 0.001–0.05 J | Cheap compares, not analog traces |
| Skip (`res_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 30 |
| On-device inject + read | unknown | Do not schedule until measured |
| Listed physical-reservoir path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an inject or read when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `classify` as proof the *plant* was identified or is safe — only that the named sizes fit the budget.
- Do not invent echo-state radius, spectral radius, or joules-per-inject numbers in host logs.

## Key Traits
- Reservoir lite is a refuse/allow gate, not a certified analog runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any analog write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_state` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, or `wm`. Keep joule costs labeled uncalibrated until an MCU/analog measurement exists. Do not check analog weights into this public card.

## Next measurements (not done)
- Time and current for inject vs read vs hold on the intended runtime.
- Decide whether state size is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a reservoir certificate.
- Optional host stub: `res_ok()` on a fixture state size in CI — still not an analog node.
