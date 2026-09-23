# 39 — Anomaly Detector (Energy Signature)

**Domain:** Monitoring  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no trained detector, no residual certificate, no field alarm log)  
**Operator role:** Optional host gate that refuses an anomaly-watch slot when the signature table is missing, a baseline row is `to-be-measured` without a hold, or the detector class is unknown. Not a production IDS and not a calibrated energy-signature certificate.

## Description
Harvested-power nodes often need a cheap check that the *shape* of recent energy use still matches a named baseline (idle floor, harvest bump, radio burst). A full residual network with labeled field incidents is out of scope until named signature tables and measurement holds exist on the intended MCU + rail pair.

This card specifies the host-facing interface. There is **no trained anomaly detector, no residual model, no calibrated signature library, and no measured joule-per-score** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- An anomaly decision is a *policy event*, not proof that a physical rail was scored on hardware.
- Host evaluation of a fixture signature table on a laptop is not an anomaly certificate.
- Do not claim IDS, SCADA-alarm, predictive-maintenance, or “AI-certified fault detection” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named watch slot* may consume that rail.
- Distinct from Model 04: Model 04 estimates energy state. This card scores *deviation from a named baseline* after that state exists.
- Distinct from Model 06 / 07: those are single-stream classifiers for sensing tasks. This card refuses if the baseline row is absent.
- Distinct from Model 20: Model 20 is a NILM-style disaggregator. This card does not claim appliance labels.
- Distinct from Model 38: Model 38 fuses agreed modality rows. This card scores one named energy-signature table.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `signature_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `ano_id` | input | Ancestry id (`39` or `39-custom-<slug>`). Not a silicon lot |
| `max_windows` | input | Design cap on named windows. Wider tables are out of this card |
| `integrity_ok` | input | Optional Model 16 result; a failed auditor should refuse `watch_slot` |
| `ano_action` | output | `hold` / `score_cheap` / `watch_slot` / `defer` / `unknown` |
| `windows_checked` | output | Planned row count after the action |
| `ano_ok` | output | Boolean: the next scheduled watch slot may run under the named table |
| `refuse_reason` | output | `energy` / `missing_baseline` / `unmeasured` / `no_hold` / `integrity` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured detector energy) |

Planned entry points:
- `ano_step(energy_state, signature_table, hold_token) -> ano_action`
- `ano_ok(energy_state, signature_table, hold_token) -> bool`
- `gate_task(task_id, ano_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture signature table on the laptop CI runner; that is still not a trained detector.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 16 `integrity_ok()` when a prior image hash is in scope — otherwise omit.
3. Model 37 `att_ok()` when the load slot itself is gated — otherwise omit.
4. Model 39 `ano_ok()` — refuse unless every in-scope signature row is `agreed` or has a named hold.
5. Only then `gate_task(allow)` for the scheduled watch slot.

Missing signature-table fields must refuse with `missing_baseline`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `integrity_ok` false must still refuse `watch_slot`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not ADC traces |
| Skip (`ano_ok` false) | 0 J extra | Gate via Model 01 / 16 / 39 |
| On-device score_cheap / watch_slot | unknown | Do not schedule until measured |
| Calibrated residual / isolation forest | unknown | Out of scope for this card |

Safety rules:
- Never schedule `watch_slot` or `score_cheap` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `ano_ok` as proof that *a physical signature was scored* — only that the named table is internally consistent with the hold policy.
- Do not invent residual thresholds, ROC curves, or certified detector joules in host logs.
- Do not treat this card as an IDS, SCADA, or predictive-maintenance qualification.

## Key Traits
- Anomaly lite is a refuse/allow gate, not a trained detector runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional attestation) and *before* any field watch that depends on agreed signature rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_baseline`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, or `fus`. Keep joule costs labeled uncalibrated until an MCU + rail measurement exists. Do not check proprietary detector weights or fake certification marks into this public card.

## Next measurements (not done)
- Time and current for score_cheap vs watch_slot vs hold on the intended MCU + rail.
- Decide whether signature tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an anomaly certificate.
- Optional host stub: `ano_ok()` on a fixture signature table in CI — still not a trained detector.
