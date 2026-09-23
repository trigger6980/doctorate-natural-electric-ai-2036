# 48 — Sovereign Compute Resource Allocator

**Domain:** Systems  
**Energy Profile:** Medium (uncalibrated)  
**Status:** Catalog + interface specification (no cluster scheduler, no VM/container orchestrator, no allocation certificate)  
**Operator role:** Optional host gate that refuses a slot assignment when the named slot table is missing, a slot budget is `to-be-measured` without a hold, or the wake class is unknown. Not Kubernetes, not a hypervisor, and not a certified sovereign cluster.

## Description
A hierarchical agent walk (Model 47) decides *who* may wake. It does not decide *which machine slot* may take the work. A cheap policy can decide whether the next compute assignment may pin one named slot, share a bounded partition, or stay deferred so the rail and air-gap boundary can recover. A full cluster scheduler + measured joules-per-slot is out of scope until named slot rows and measurement holds exist on the intended host + rail pair.

This card specifies the host-facing interface. There is **no cluster scheduler, no VM/container orchestrator, no calibrated slot-to-joule library, and no measured joule-per-allocation** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- An allocate decision is a *policy event*, not proof that a slot ran work.
- Host evaluation of a fixture slot table on a laptop is not an allocation certificate.
- Do not claim Kubernetes, Nomad, Mesos, Slurm, hypervisor, or “certified sovereign cluster” from this card.
- Distinct from Model 11: Model 11 grants energy to one requester. This card assigns *named machine slots* after a grant exists.
- Distinct from Model 18: Model 18 is a mesh routing policy. This card assigns compute, not hops.
- Distinct from Model 41: Model 41 plans tokens for one agent. This card reserves *host slots*, not token budgets.
- Distinct from Model 47: Model 47 sequences named child agents. This card sequences *machine partitions*, not roles.
- Distinct from Model 49: Model 49 (still a stub) searches architectures. This card allocates already-named slots.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `slot_table` | input | Named compute-slot rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_scr` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `scr_id` | input | Ancestry id (`48` or `48-custom-<slug>`). Not a silicon lot |
| `max_slots` | input | Design cap on named slots in one wake |
| `airgap_required` | input | If true, refuse any slot marked as needing outbound links |
| `energy_grant_ok` | input | Optional Model 11 result; a refused grant should refuse `share` |
| `hmo_ok` | input | Optional Model 47 result; a refused hierarchy should not pin slots |
| `att_ok` | input | Optional Model 37 result; an unattested image should not occupy a slot |
| `rst_ok` | input | Optional Model 40 result; an unhealthy host should not accept new slots |
| `grd_ok` | input | Optional Model 42 result; a refused tool path should not claim a slot |
| `mac_ok` | input | Optional Model 36 result; a refused radio budget should not pin a networked slot |
| `scr_action` | output | `hold` / `pin_one` / `share` / `defer` / `unknown` |
| `slots_checked` | output | Planned slot-row count after the action |
| `scr_ok` | output | Boolean: the next scheduled slot assignment may run under the named table |
| `refuse_reason` | output | `energy` / `missing_slots` / `unmeasured` / `no_hold` / `grant` / `hierarchy` / `attest` / `restart` / `tool` / `radio` / `airgap` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured allocator energy) |

Planned entry points:
- `scr_step(energy_state, slot_table, hold_scr) -> scr_action`
- `scr_ok(energy_state, slot_table, hold_scr) -> bool`
- `gate_task(task_id, scr_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture slot table on the laptop CI runner; that is still not a cluster scheduler.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 11 grant when multi-slot energy is in scope — otherwise omit.
3. Model 37 `att_ok()` when image attestation is in scope — otherwise omit.
4. Model 40 `rst_ok()` when host health is in scope — otherwise omit.
5. Model 42 `grd_ok()` when the slot would run a tool path — otherwise omit.
6. Model 36 `mac_ok()` when the slot is networked — otherwise omit.
7. Model 47 `hmo_ok()` when the work is hierarchical — otherwise omit.
8. Model 48 `scr_ok()` — refuse unless every in-scope slot row is `agreed` or has a named hold.
9. Only then `gate_task(allow)` for the scheduled slot assignment.

Missing slot-table fields must refuse with `missing_slots`. Rows marked `to-be-measured` without `hold_scr` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `energy_grant_ok`, `hmo_ok`, `att_ok`, `rst_ok`, `grd_ok`, or `mac_ok` false must still refuse `share`. `airgap_required` true plus a slot that needs outbound links must refuse with `airgap`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended host + rail before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not a cluster control plane |
| Skip (`scr_ok` false) | 0 J extra | Gate via Model 01 / 11 / 36 / 37 / 40 / 42 / 47 / 48 |
| On-device pin_one / share | unknown | Do not schedule until measured |
| Full cluster scheduler + calibrated slot-joule | unknown | Out of scope for this card |

Safety rules:
- Never schedule `share` or `pin_one` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `scr_ok` as proof that *a slot ran work* — only that the named table is internally consistent with the hold policy.
- Do not invent latency SLAs, vCPU counts as certificates, or certified allocation joules in host logs.
- Do not treat this card as Kubernetes / Nomad / Mesos / Slurm / hypervisor runtime or a sovereign-cluster certificate.

## Key Traits
- Sovereign compute allocation lite is a refuse/allow gate, not a cluster control plane
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* the rail floor (and optional broker / radio / attestation / restart / tool / hierarchy gates) and *before* any field duty change that depends on agreed slot rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_slots`, `unmeasured`, `no_hold`, or `airgap` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, `hcd`, `mac`, `att`, `fus`, `ano`, `rst`, `tok`, `grd`, `aln`, `rsn`, `gnn`, `tgf`, or `hmo`. Keep joule costs labeled uncalibrated until a host + rail measurement exists. Do not check proprietary scheduler weights or fake allocation marks into this public card.

## Next measurements (not done)
- Time and current for pin_one vs share vs hold on the intended host + rail.
- Decide whether slot tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming an allocation certificate.
- Optional host stub: `scr_ok()` on a fixture slot table in CI — still not a cluster scheduler.
