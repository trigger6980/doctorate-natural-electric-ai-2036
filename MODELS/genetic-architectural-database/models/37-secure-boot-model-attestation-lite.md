# 37 — Secure Boot + Model Attestation Lite

**Domain:** Security  
**Energy Profile:** Low (uncalibrated)  
**Status:** Catalog + interface specification (no measured boot-ROM joules, no TPM/secure-element driver, no attestation certificate)  
**Operator role:** Optional host gate that refuses a model-load or firmware-advance slot when the named attestation table is missing, a row is `to-be-measured` without a hold, or the digest class is unknown. Not a production secure-boot chain and not a Common Criteria / PSA Certified / FIPS certificate.

## Description
Harvested-power nodes that load a TinyML weight file or a firmware slot still need a cheap staged refuse: *hold*, *verify_digest*, *attest_slot*, *defer*, or *unknown*. A full secure-boot chain (ROM root of trust, measured boot, remote attestation protocol, certified HSM) is out of scope until a named digest table and measurement hold exist on the intended MCU + storage pair.

This card specifies the host-facing interface. There is **no boot ROM, no TPM 2.0 / secure-element driver, no remote-attestation protocol, and no measured joule-per-verify** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- An attestation decision is a *policy event*, not proof a physical root of trust measured the loaded image on hardware.
- Host evaluation of a fixture digest table on a laptop is not an attestation certificate.
- Do not claim PSA Certified, Common Criteria, FIPS 140, or “AI-hardened secure boot” status from this card.
- Distinct from Model 16: Model 16 is a runtime integrity auditor (hash-as-you-go). This card is the *boot / load slot* gate before that auditor runs.
- Distinct from Model 17: Model 17 validates air-gap config schema. This card does not parse policy files.
- Distinct from Model 33: Model 33 checks energy-contract proofs. This card does not claim formal verification of the boot graph.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses whether a *named load slot* may consume that rail.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `digest_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `att_id` | input | Ancestry id (`37` or `37-custom-<slug>`). Not a silicon lot |
| `max_slots` | input | Design cap on named load / boot slots. Wider tables are out of this card |
| `integrity_ok` | input | Optional Model 16 result; a failed auditor should refuse `attest_slot` |
| `att_action` | output | `hold` / `verify_digest` / `attest_slot` / `defer` / `unknown` |
| `slots_checked` | output | Planned row count after the action |
| `att_ok` | output | Boolean: the next scheduled load slot may run under the named table |
| `refuse_reason` | output | `energy` / `missing_slot` / `unmeasured` / `no_hold` / `integrity` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured verify energy) |

Planned entry points:
- `att_step(energy_state, digest_table, hold_token) -> att_action`
- `att_ok(energy_state, digest_table, hold_token) -> bool`
- `gate_task(task_id, att_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture digest table on the laptop CI runner; that is still not boot firmware.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 16 `integrity_ok()` when a prior image hash is in scope — otherwise omit.
3. Model 17 when the load also depends on a named config schema — otherwise omit.
4. Model 37 `att_ok()` — refuse unless every in-scope digest row is `agreed` or has a named hold.
5. Only then `gate_task(allow)` for the scheduled load slot.

Missing digest-table fields must refuse with `missing_slot`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `integrity_ok` false must still refuse `attest_slot`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + storage before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not ROM traces |
| Skip (`att_ok` false) | 0 J extra | Gate via Model 01 / 16 / 37 |
| On-device verify_digest / attest_slot | unknown | Do not schedule until measured |
| Remote attestation / HSM session | unknown | Out of scope for this card |

Safety rules:
- Never schedule `attest_slot` or `verify_digest` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `att_ok` as proof a *root of trust measured the image* — only that the named table is internally consistent with the hold policy.
- Do not invent digest algorithms, fuse maps, or certified boot joules in host logs.
- Do not treat this card as a Common Criteria, PSA, or FIPS qualification.

## Key Traits
- Attestation lite is a refuse/allow gate, not a certified secure-boot runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor and *before* any field model-load that depends on agreed digest rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_slot`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, or `mac`. Keep joule costs labeled uncalibrated until an MCU + storage measurement exists. Do not check proprietary boot blobs or fake certification marks into this public card.

## Next measurements (not done)
- Time and current for verify_digest vs attest_slot vs hold on the intended MCU + flash.
- Decide whether digest tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an attestation certificate.
- Optional host stub: `att_ok()` on a fixture digest table in CI — still not boot firmware.
