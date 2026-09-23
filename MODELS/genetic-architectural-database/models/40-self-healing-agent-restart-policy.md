# 40 — Self-Healing Agent Restart Policy

**Domain:** Resilience  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no watchdog firmware, no crash dump store, no restart certificate)  
**Operator role:** Optional host gate that refuses a restart slot when the last-good checkpoint is missing, a crash row is `to-be-measured` without a hold, or the restart class is unknown. Not production HA and not a certified self-heal runtime.

## Description
Harvested-power agents die mid-step. A cheap policy can decide whether the *next* wake should resume from a named last-good checkpoint, defer, or stay down so the rail can recover. A full watchdog + dump store + measured reboot joules is out of scope until named checkpoint rows and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no watchdog firmware, no crash-dump store, no calibrated restart library, and no measured joule-per-reboot** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A restart decision is a *policy event*, not proof that a physical node rebooted.
- Host evaluation of a fixture checkpoint table on a laptop is not a self-heal certificate.
- Do not claim HA cluster, systemd-watchdog, k8s-restart, or “AI-certified resilience” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named restart slot* may consume that rail.
- Distinct from Model 12: Model 12 is the checkpoint *format* (host JSON). This card decides whether that checkpoint may be *applied* after a named fail.
- Distinct from Model 16 / 37: those check image integrity and attestation. This card refuses if the last-good row is absent even when the image hashes.
- Distinct from Model 19: Model 19 estimates energy-neutral probability. This card does not claim survival after restart.
- Distinct from Model 39: Model 39 scores energy-signature deviation. This card scores *process liveness policy*, not rail shape.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `checkpoint_table` | input | Named last-good rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `rst_id` | input | Ancestry id (`40` or `40-custom-<slug>`). Not a silicon lot |
| `max_restarts` | input | Design cap on named restart attempts in one wake window |
| `integrity_ok` | input | Optional Model 16 result; a failed auditor should refuse `restart_slot` |
| `att_ok` | input | Optional Model 37 result; a failed attestation should refuse `restart_slot` |
| `rst_action` | output | `hold` / `resume_cheap` / `restart_slot` / `defer` / `unknown` |
| `restarts_checked` | output | Planned attempt count after the action |
| `rst_ok` | output | Boolean: the next scheduled restart slot may run under the named table |
| `refuse_reason` | output | `energy` / `missing_checkpoint` / `unmeasured` / `no_hold` / `integrity` / `attestation` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured reboot energy) |

Planned entry points:
- `rst_step(energy_state, checkpoint_table, hold_token) -> rst_action`
- `rst_ok(energy_state, checkpoint_table, hold_token) -> bool`
- `gate_task(task_id, rst_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture checkpoint table on the laptop CI runner; that is still not watchdog firmware.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 16 `integrity_ok()` when a prior image hash is in scope — otherwise omit.
3. Model 37 `att_ok()` when the load slot itself is gated — otherwise omit.
4. Model 12 checkpoint row must exist as the *object* to resume — format only.
5. Model 40 `rst_ok()` — refuse unless every in-scope last-good row is `agreed` or has a named hold.
6. Only then `gate_task(allow)` for the scheduled restart slot.

Missing checkpoint-table fields must refuse with `missing_checkpoint`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `integrity_ok` or `att_ok` false must still refuse `restart_slot`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not MCU reboot traces |
| Skip (`rst_ok` false) | 0 J extra | Gate via Model 01 / 16 / 37 / 40 |
| On-device resume_cheap / restart_slot | unknown | Do not schedule until measured |
| Full watchdog + dump + calibrated reboot | unknown | Out of scope for this card |

Safety rules:
- Never schedule `restart_slot` or `resume_cheap` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `rst_ok` as proof that *a physical node restarted* — only that the named last-good table is internally consistent with the hold policy.
- Do not invent MTBF, crash rates, or certified reboot joules in host logs.
- Do not treat this card as HA, watchdog, or cluster qualification.

## Key Traits
- Restart lite is a refuse/allow gate, not a watchdog runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional integrity/attestation) and *before* any field resume that depends on agreed last-good rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_checkpoint`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, or `ano`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary crash dumps or fake HA marks into this public card.

## Next measurements (not done)
- Time and current for resume_cheap vs restart_slot vs hold on the intended MCU + rail.
- Decide whether last-good tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a restart certificate.
- Optional host stub: `rst_ok()` on a fixture checkpoint table in CI — still not watchdog firmware.
