# 16 — Secure Integrity Auditor

**Domain:** Security  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no TPM binding, no measured hash joules, no remote attestation service)  
**Operator role:** Optional host gate that refuses a task-graph step when a local artifact hash does not match an expected digest. Not a certified secure-boot product and not a remote-attestation SaaS.

## Description
Off-grid and air-gapped nodes still need a cheap answer to “did this model file or policy file change since the last trusted copy?” A full measured-boot stack is out of scope for harvested-power nodes until the energy cost of hashing is measured on the intended MCU.

This card specifies the host-facing interface. There is **no TPM driver, no fuse-bit programming, and no measured hash energy** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A digest mismatch is a *policy event*, not proof of a named attacker.
- Host SHA-256 of a file on a laptop is not the same as on-device flash measurement.
- Do not claim Common Criteria, FIPS, or measured-boot certification from this card.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `artifact_path` | input | Local file the operator wants checked |
| `expected_digest_hex` | input | Trusted hex digest from a prior air-gap copy |
| `algo` | parameter | Host default `sha256`; other algos are custom scope |
| `EnergyState` | input | Shared Model 01 rail so hashing can be refused when energy is low |
| `integrity_ok` | output | Boolean: digest matches |
| `digest_hex` | output | Computed digest (empty if hashing was refused) |
| `refuse_reason` | output | `energy` / `missing_file` / `mismatch` / `ok` |
| `joules_used_est` | output | Placeholder cost of this hash step |

Planned entry points:
- `audit(artifact_path, expected_digest_hex, energy_state) -> IntegrityResult`
- `may_hash(energy_state) -> bool` — refuse when Model 01 would choose SLEEP
- `gate_task(task_id, integrity_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may hash files on the laptop CI runner; that is still not on-device attestation.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Hash a small policy file (host sim) | 0.001–0.01 J | Cheap integrity check |
| Skip (policy = SLEEP or missing file) | 0 J extra | Gate via Model 01 |
| Full firmware image hash | unknown | Do not schedule until measured |

Safety rules:
- Never hash a large artifact when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat a matching digest as proof the weights are *good* — only that they match the expected copy.
- Distinct from Model 37 (secure boot + model attestation lite), which would bind to boot hardware.

## Key Traits
- Integrity is a refuse/allow gate, not a threat-intel product
- Reuses Model 01 energy refusal so hashing cannot drain a dying node
- Compatible with air-gap / sovereign delivery language on the enterprise pages
- Distinct from Model 17 (config validator) and Model 42 (tool-use guardrail)

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `integrity` as well as `energy` or `policy`. Keep joule costs labeled uncalibrated until an MCU measurement exists.

## Next measurements (not done)
- Time and current for SHA-256 of a 4 KiB policy file vs a multi-megabyte weight file on the intended board.
- Decide whether expected digests live in host JSON (like Model 12 checkpoints) or on write-once media.
- Wire a skip reason through `policy_gated_executor` without claiming TPM semantics.
