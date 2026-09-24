# 49 — Genetic Architecture Search Lite

**Domain:** Meta / AutoML  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification + host fixture stub (no search trainer, no NAS controller, no architecture certificate)  
**Operator role:** Optional host gate that refuses a search generation when the named search table is missing, a candidate energy row is `to-be-measured` without a hold, or the wake class is unknown. Not AutoML-as-a-service, not a genetic algorithm runtime, and not a certified architecture search.

## Description
A slot allocator (Model 48) decides *which machine partition* may take work. It does not decide *which candidate architecture* may be scored next. A cheap policy can decide whether the next generation may keep one parent, mutate a bounded child, or stay deferred so the rail can recover. A full NAS controller + measured joules-per-generation is out of scope until named candidate rows and measurement holds exist on the intended host + rail pair.

This card specifies the host-facing interface. There is **no search trainer, no NAS controller, no calibrated candidate-to-joule library, and no measured joule-per-generation** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A search decision is a *policy event*, not proof that a candidate was trained.
- Host evaluation of a fixture candidate table on a laptop is not an architecture certificate.
- Do not claim NAS, AutoML SaaS, evolutionary compute farm, or “certified architecture search” from this card.
- Distinct from Model 03: Model 03 duty-cycles one controller. This card scores *candidate architectures*, not one policy.
- Distinct from Model 11: Model 11 grants energy to one requester. This card proposes the next candidate after a grant exists.
- Distinct from Model 25: Model 25 is constrained continual learning on one model. This card searches *across* named candidates.
- Distinct from Model 41: Model 41 plans tokens for one agent. This card reserves *search generations*, not token budgets.
- Distinct from Model 47: Model 47 sequences named child agents. This card sequences *architecture candidates*, not roles.
- Distinct from Model 48: Model 48 assigns already-named slots. This card searches architectures that may later occupy those slots.
- Distinct from Model 50: Model 50 is a commercial template. This card is a research interface, not an order form.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `search_table` | input | Named candidate rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_gas` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `gas_id` | input | Ancestry id (`49` or `49-custom-<slug>`). Not a silicon lot |
| `max_gen` | input | Design cap on generations in one wake |
| `airgap_required` | input | If true, refuse any candidate that needs outbound dataset pulls |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `mutate` |
| `scr_ok` | input | Optional Model 48 result; a refused slot should not host a generation |
| `hmo_ok` | input | Optional Model 47 result; a refused hierarchy should not spawn search workers |
| `att_ok` | input | Optional Model 37 result; an unattested image should not score a candidate |
| `rst_ok` | input | Optional Model 40 result; an unhealthy host should not start a generation |
| `ctr_ok` | input | Optional Model 33 result; a refused energy contract should not score |
| `gas_action` | output | `hold` / `keep_parent` / `mutate` / `defer` / `unknown` |
| `candidates_checked` | output | Planned candidate-row count after the action |
| `gas_ok` | output | Boolean: the next scheduled generation may run under the named table |
| `refuse_reason` | output | `energy` / `missing_table` / `unmeasured` / `no_hold` / `grant` / `slot` / `hierarchy` / `attest` / `restart` / `contract` / `airgap` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured search energy) |

Planned entry points:
- `gas_step(energy_state, search_table, hold_gas) -> gas_action`
- `gas_ok(energy_state, search_table, hold_gas) -> bool`
- `gate_task(task_id, gas_ok) -> allow | skip` — Operator AI policy hook

Host helper (laptop CI only): `AGENTS/gas_search_gate.py` walks a fixture candidate table. Passing those tests is **not** a NAS controller and **not** proof a candidate was trained.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-candidate energy is in scope — otherwise omit.
3. Model 33 `ctr_ok()` when a formal energy contract is in scope — otherwise omit.
4. Model 37 `att_ok()` when image attestation is in scope — otherwise omit.
5. Model 40 `rst_ok()` when host health is in scope — otherwise omit.
6. Model 48 `scr_ok()` when a named slot must host the generation — otherwise omit.
7. Model 47 `hmo_ok()` when search workers are hierarchical — otherwise omit.
8. Model 49 `gas_ok()` — refuse unless every in-scope candidate row is `agreed` or has a named hold.
9. Only then `gate_task(allow)` for the scheduled generation.

Missing search-table fields must refuse with `missing_table`. Rows marked `to-be-measured` without `hold_gas` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `energy_grant_ok`, `scr_ok`, `hmo_ok`, `att_ok`, `rst_ok`, or `ctr_ok` false must still refuse `mutate`. `airgap_required` true plus a candidate that needs outbound dataset pulls must refuse with `airgap`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended host + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not a NAS control plane |
| Skip (`gas_ok` false) | 0 J extra | Gate via Model 01 / 11 / 33 / 37 / 40 / 47 / 48 / 49 |
| On-device keep_parent / mutate | unknown | Do not schedule until measured |
| Full NAS controller + calibrated generation-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `mutate` or `keep_parent` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `gas_ok` as proof that *a candidate was trained* — only that the named table is internally consistent with the hold policy.
- Do not invent accuracy SLAs, search-space certificates, or certified generation joules in host logs.
- Do not treat this card as NAS / AutoML SaaS / evolutionary farm runtime or an architecture-search certificate.

## Key Traits
- Genetic architecture search lite is a refuse/allow gate, not an AutoML control plane
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / contract / attestation / restart / slot / hierarchy gates) and *before* any field duty change that depends on agreed candidate rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Host stub lives at `AGENTS/gas_search_gate.py` with tests in `AGENTS/test_gas_search_gate.py`. A skip reason can be `missing_table`, `unmeasured`, `no_hold`, or `airgap` as well as prior skip tokens (`energy`, `grant`, `slot`, …). Keep joule costs labeled uncalibrated until a host + rail measurement exists. Do not check proprietary search weights or fake architecture marks into this public card.

## Next measurements (not done)
- Time and current for keep_parent vs mutate vs hold on the intended host + rail.
- Decide whether search tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an architecture certificate.
- Host stub exists; it is still not a NAS controller.
