# 17 — Air-Gap Config Validator

**Domain:** Security / Networking  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no schema compiler on-device, no signed-config service, no measured parse joules)  
**Operator role:** Optional host gate that refuses a task-graph step when a local config artifact fails a declared schema or an air-gap allow-list. Not a network-policy product and not a certificate authority.

## Description
Air-gapped and sovereign nodes still need a cheap answer to “is this YAML/JSON/TOML the shape we agreed to run?” A full policy compiler or remote config service is out of scope for harvested-power nodes until the energy cost of parsing is measured on the intended MCU.

This card specifies the host-facing interface. There is **no on-device schema compiler, no signed-config pipeline, and no measured parse energy** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A schema miss is a *policy event*, not proof of a named attacker or a compromised vendor.
- Host validation of a file on a laptop is not the same as on-device flash measurement.
- Do not claim STIG, CIS, Common Criteria, or “air-gap certified” status from this card.
- Distinct from Model 16: Model 16 answers “did the bytes change?” This card answers “do the bytes *mean* an allowed config?”

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `config_path` | input | Local file the operator wants checked |
| `schema_id` | input | Named schema from a prior air-gap copy (not fetched live) |
| `allow_list_path` | input | Optional list of permitted keys / endpoints / radios |
| `EnergyState` | input | Shared Model 01 rail so parsing can be refused when energy is low |
| `config_ok` | output | Boolean: parse + schema + allow-list all passed |
| `violations` | output | Short codes (`missing_key`, `unknown_key`, `bad_type`, `deny_list`, `parse_error`) |
| `refuse_reason` | output | `energy` / `missing_file` / `invalid` / `ok` |
| `joules_used_est` | output | Placeholder cost of this validate step |

Planned entry points:
- `validate(config_path, schema_id, energy_state) -> ConfigResult`
- `may_parse(energy_state) -> bool` — refuse when Model 01 would choose SLEEP
- `gate_task(task_id, config_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may parse a fixture file on the laptop CI runner; that is still not on-device policy enforcement.

Typical composition with Model 16:
1. `audit()` — digest matches the expected air-gap copy.
2. `validate()` — the matched bytes still satisfy the declared schema.
3. Only then `gate_task(allow)`.

A matching digest with a schema miss must still refuse. A valid schema with a digest mismatch must still refuse.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Parse a small policy/config file (host sim) | 0.001–0.01 J | Cheap schema check |
| Skip (policy = SLEEP or missing file) | 0 J extra | Gate via Model 01 |
| Full mesh-policy compile | unknown | Do not schedule until measured |

Safety rules:
- Never parse a large artifact when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `config_ok` as proof the *intent* is good — only that the file matches a declared schema and allow-list.
- Distinct from Model 18 (local mesh routing policy) and Model 42 (tool-use guardrail).

## Key Traits
- Config validity is a refuse/allow gate, not a network-management product
- Reuses Model 01 energy refusal so parsing cannot drain a dying node
- Intended to run *after* Model 16 so bytes and meaning are both checked
- Compatible with air-gap / sovereign delivery language on the enterprise pages

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `config` as well as `energy`, `policy`, or `integrity`. Keep joule costs labeled uncalibrated until an MCU measurement exists. Do not fetch schemas over a network from this card.

## Next measurements (not done)
- Time and current for parsing a 4 KiB YAML/JSON policy file vs a multi-megabyte inventory file on the intended board.
- Decide whether schemas live in host JSON (like Model 12 checkpoints) or on write-once media beside Model 16 digests.
- Wire a skip reason through `policy_gated_executor` without claiming STIG or CIS semantics.
- Optional host stub: `validate()` a fixture file in CI — still not on-device enforcement.
