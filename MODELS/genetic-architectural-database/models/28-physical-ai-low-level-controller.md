# 28 — Physical AI Low-Level Controller

**Domain:** Robotics / Physical  
**Energy Profile:** Medium  
**Status:** Catalog + interface specification (no actuator driver, no motion certificate, no measured command joules)  
**Operator role:** Optional host gate that refuses a physical command when the rail cannot pay the next command-plus-sense pair, or when the named plant bounds are missing. Not a production motion stack and not a safety-PLC certificate.

## Description
Some off-grid plants only need a staged refuse: *hold*, *arm*, *step*, *sense*, or *unknown*. A full physical-AI stack (motor drivers, kinematics, measured command joules, listed safety PLC) is out of scope until a named actuator class and plant bounds exist on the intended node.

This card specifies the host-facing interface. There is **no GPIO/PWM driver, no public kinematics file, and no measured joule-per-command** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A physical-controller decision is a *policy event*, not proof the plant moved safely.
- Host evaluation of a fixture command length on a laptop is not a field motion certificate.
- Do not claim SIL, PL, ISO 13849, or “certified physical AI” status from this card.
- Distinct from Model 27: Model 27 gates whether *noise* may be added before a release. This card gates whether a *physical command* may leave the host.
- Distinct from Model 03: Model 03 is a duty-cycle policy on a harvest rail. This card is a command gate for an actuator class that may not yet exist.
- Distinct from Model 21: Model 21 votes among named control leaves. This card does not train or vote a forest.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `cmd_len` | input | Named placeholder command length. Uncalibrated |
| `plant_bounds` | input | Named placeholder limits. Uncalibrated; not a live kinematic model |
| `mech_id` | input | Ancestry id (`28` or `28-custom-<slug>`). Not an actuator hash |
| `max_cmd_len` | input | Design cap. Longer command trains are out of this card |
| `phys_action` | output | `hold` / `arm` / `step` / `sense` / `unknown` |
| `steps_issued` | output | Planned count after the action |
| `phys_ok` | output | Boolean: the next command-plus-sense pair may run |
| `refuse_reason` | output | `energy` / `missing_bounds` / `no_checkpoint` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action |

Planned entry points:
- `phys_step(energy_state, cmd_len, plant_bounds) -> phys_action`
- `phys_ok(energy_state, cmd_len, plant_bounds) -> bool`
- `gate_task(task_id, phys_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture command length on the laptop CI runner; that is still not an actuator driver.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
3. Model 12 checkpoint present — refuse step unless a host JSON path exists.
4. Model 21 `rf_ok()` when a forest vote precedes the command — otherwise omit.
5. Model 28 `phys_ok()` — refuse arm/step unless the named sizes fit.
6. Only then `gate_task(allow)` for the command step.

Missing bound fields must refuse with `missing_bounds`. An `unknown` action must skip the command-sense pair unless a later custom card says otherwise.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU or driver before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-arm | 0.001–0.05 J | Cheap compares, not PWM or encoder traces |
| Skip (`phys_ok` false) | 0 J extra | Gate via Model 01 / 12 / 19 / 21 / 28 |
| On-device command + sense | unknown | Do not schedule until measured |
| Listed safety PLC path | unknown | Do not treat host fixture walk as measured |

Safety rules:
- Never schedule an arm or step when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `step` as proof the *plant* moved or is safe — only that the named sizes fit the budget.
- Do not invent torque, current, or joules-per-command numbers in host logs.

## Key Traits
- Physical AI is a refuse/allow gate, not a certified motion runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* control/checkpoint gates and *before* any GPIO write
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_bounds` or `no_checkpoint` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, or `dp`. Keep joule costs labeled uncalibrated until an MCU/driver measurement exists. Do not check actuator firmware or kinematics into this public card.

## Next measurements (not done)
- Time and current for arm vs step vs hold on the intended runtime.
- Decide whether command length is fixed, adaptive, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a motion certificate.
- Optional host stub: `phys_ok()` on a fixture command length in CI — still not an actuator driver.
