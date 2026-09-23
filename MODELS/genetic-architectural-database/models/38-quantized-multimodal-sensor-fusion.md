# 38 — Quantized Multimodal Sensor Fusion

**Domain:** Sensing  
**Energy Profile:** Low–Medium (uncalibrated)  
**Status:** Catalog + interface specification (no trained fusion weights, no sensor-driver stack, no fusion certificate)  
**Operator role:** Optional host gate that refuses a fused-inference slot when a required modality is missing, a row is `to-be-measured` without a hold, or the fusion class is unknown. Not a production multimodal runtime and not a calibrated sensor-fusion certificate.

## Description
Harvested-power nodes often see more than one cheap sensor at once (voltage proxy, lux, vibration, indoor RF proxy). A full late-fusion network with calibrated cross-attention is out of scope until named modality tables and measurement holds exist on the intended MCU + sensor pair.

This card specifies the host-facing interface. There is **no trained fusion graph, no I2C/SPI sensor-driver stack, no calibrated cross-modal weights, and no measured joule-per-fusion** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A fusion decision is a *policy event*, not proof that two physical sensors were sampled on hardware.
- Host evaluation of a fixture modality table on a laptop is not a fusion certificate.
- Do not claim Kalman, factor-graph SLAM, or “AI-certified multimodal perception” status from this card.
- Distinct from Model 04: Model 04 estimates energy state from PV + RF *as energy*. This card fuses *task features* after that state exists.
- Distinct from Model 06 / 07: those are single-stream classifiers. This card refuses if a required second stream is absent.
- Distinct from Model 20: Model 20 is a NILM-style disaggregator on one power trace. This card does not claim appliance labels.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named fusion slot* may consume that rail.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `modality_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `fus_id` | input | Ancestry id (`38` or `38-custom-<slug>`). Not a silicon lot |
| `max_modalities` | input | Design cap on named streams. Wider tables are out of this card |
| `integrity_ok` | input | Optional Model 16 result; a failed auditor should refuse `fuse_slot` |
| `fus_action` | output | `hold` / `fuse_cheap` / `fuse_slot` / `defer` / `unknown` |
| `modalities_checked` | output | Planned row count after the action |
| `fus_ok` | output | Boolean: the next scheduled fusion slot may run under the named table |
| `refuse_reason` | output | `energy` / `missing_modality` / `unmeasured` / `no_hold` / `integrity` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured fusion energy) |

Planned entry points:
- `fus_step(energy_state, modality_table, hold_token) -> fus_action`
- `fus_ok(energy_state, modality_table, hold_token) -> bool`
- `gate_task(task_id, fus_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture modality table on the laptop CI runner; that is still not a trained fusion graph.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 16 `integrity_ok()` when a prior image hash is in scope — otherwise omit.
3. Model 37 `att_ok()` when the load slot itself is gated — otherwise omit.
4. Model 38 `fus_ok()` — refuse unless every in-scope modality row is `agreed` or has a named hold.
5. Only then `gate_task(allow)` for the scheduled fusion slot.

Missing modality-table fields must refuse with `missing_modality`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `integrity_ok` false must still refuse `fuse_slot`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + sensors before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not ADC traces |
| Skip (`fus_ok` false) | 0 J extra | Gate via Model 01 / 16 / 38 |
| On-device fuse_cheap / fuse_slot | unknown | Do not schedule until measured |
| Calibrated late-fusion / attention | unknown | Out of scope for this card |

Safety rules:
- Never schedule `fuse_slot` or `fuse_cheap` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `fus_ok` as proof that *two physical sensors were sampled together* — only that the named table is internally consistent with the hold policy.
- Do not invent cross-attention weights, Kalman covariances, or certified fusion joules in host logs.
- Do not treat this card as a perception, SLAM, or safety-PLC qualification.

## Key Traits
- Fusion lite is a refuse/allow gate, not a trained multimodal runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional attestation) and *before* any field inference that depends on agreed modality rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_modality`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, or `att`. Keep joule costs labeled uncalibrated until an MCU + sensor measurement exists. Do not check proprietary fusion weights or fake certification marks into this public card.

## Next measurements (not done)
- Time and current for fuse_cheap vs fuse_slot vs hold on the intended MCU + sensors.
- Decide whether modality tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a fusion certificate.
- Optional host stub: `fus_ok()` on a fixture modality table in CI — still not a trained fusion graph.
