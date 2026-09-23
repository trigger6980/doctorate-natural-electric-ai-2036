# 36 — BLE / Mesh Energy-Aware MAC

**Domain:** Networking  
**Energy Profile:** Ultra-low (uncalibrated)  
**Status:** Catalog + interface specification (no BLE/mesh radio driver, no measured TX/RX joules, no MAC certificate)  
**Operator role:** Optional host gate that refuses a radio-on slot when the named MAC table is missing, the listen window exceeds the rail floor, or a row is marked `to-be-measured` without a hold. Not a production BLE stack and not a mesh-MAC certificate.

## Description
Harvested-power nodes that speak BLE or a local mesh still need a cheap staged refuse: *hold*, *advertise_only*, *listen_window*, *tx_slot*, *defer*, or *unknown*. A full MAC (link-layer firmware, connection events, adaptive interval, certified coexistence) is out of scope until a named slot table and measurement hold exist on the intended radio + MCU pair.

This card specifies the host-facing interface. There is **no SoftDevice / Zephyr / NimBLE driver, no public airtime suite, and no measured joule-per-advertisement** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A MAC decision is a *policy event*, not proof a physical radio delivered the planned airtime on hardware.
- Host evaluation of a fixture slot table on a laptop is not a MAC certificate.
- Do not claim BLE SIG qualification, Thread certification, or “AI-optimized mesh radio” status from this card.
- Distinct from Model 01: Model 01 is the live rail floor. This card chooses which *named radio slots* may consume that rail.
- Distinct from Model 11: Model 11 partitions a local joule pool among tasks. This card decides whether a *radio slot* is even legal.
- Distinct from Model 18: Model 18 is the next-hop / payload-class policy layer. This card is the energy-aware MAC slot layer beneath it.
- Distinct from Model 34: Model 34 chooses generic multi-source power paths. This card does not claim MPPT or converter control.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `EnergyState` | input | Shared Model 01 rail (`rail_voltage_v`, optional `C_farads`) |
| `slot_table` | input | Named placeholder rows (`agreed` / `to-be-measured` / `out of scope`). Uncalibrated |
| `hold_token` | input | Named placeholder measurement-hold id. Not a lab certificate |
| `mac_id` | input | Ancestry id (`36` or `36-custom-<slug>`). Not a radio lot |
| `max_slots` | input | Design cap on named MAC slots. Wider tables are out of this card |
| `route_ok` | input | Optional Model 18 result; a deny-listed hop should refuse the TX slot |
| `mac_action` | output | `hold` / `advertise_only` / `listen_window` / `tx_slot` / `defer` / `unknown` |
| `slots_checked` | output | Planned row count after the action |
| `mac_ok` | output | Boolean: the next scheduled radio slot may run under the named table |
| `refuse_reason` | output | `energy` / `missing_slot` / `unmeasured` / `no_hold` / `route` / `unknown` / `ok` |
| `joules_used_est` | output | Placeholder cost of the named action (not measured TX energy) |

Planned entry points:
- `mac_step(energy_state, slot_table, hold_token) -> mac_action`
- `mac_ok(energy_state, slot_table, hold_token) -> bool`
- `gate_task(task_id, mac_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may walk a fixture slot table on the laptop CI runner; that is still not radio firmware.

Typical composition:
1. Model 01 floor — refuse if the rail is already in SLEEP.
2. Model 16 / 17 when routing-table bytes are in scope — otherwise omit.
3. Model 18 `route_ok()` when a named next hop is required for `tx_slot` — otherwise omit.
4. Model 19 `neutral_ok()` when a burst cost is known — otherwise omit.
5. Model 36 `mac_ok()` — refuse unless every in-scope slot is `agreed` or has a named hold.
6. Only then `gate_task(allow)` for the scheduled radio slot.

Missing slot-table fields must refuse with `missing_slot`. Rows marked `to-be-measured` without `hold_token` must refuse with `unmeasured` or `no_hold`. An `unknown` action must skip the step unless a later custom card says otherwise. A charged rail with `route_ok` false must still refuse `tx_slot`.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + radio before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of hold-or-defer | 0.0005–0.02 J | Cheap table compares, not airtime traces |
| Skip (`mac_ok` false) | 0 J extra | Gate via Model 01 / 18 / 19 / 36 |
| On-device advertise_only / listen_window / tx_slot | unknown | Do not schedule until measured |
| Connection events / mesh flooding | unknown | Out of scope for this card |

Safety rules:
- Never schedule `tx_slot` or `listen_window` when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `mac_ok` as proof a *packet left the antenna* — only that the named table is internally consistent with the hold policy.
- Do not invent RSSI, advertising interval, or certified airtime joules in host logs.
- Do not treat this card as a radio-regulatory or coexistence qualification.

## Key Traits
- Energy-aware MAC lite is a refuse/allow gate, not a certified radio runtime
- Reuses Model 01 floor so energy state stays first-class
- Intended to run *after* integrity / config / route gates and *before* any field radio slot that depends on agreed MAC rows
- Compatible with enterprise energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`) and measurement-hold packets

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `missing_slot`, `unmeasured`, or `no_hold` as well as `energy`, `policy`, `integrity`, `config`, `route`, `uncertain`, `disagg`, `rf`, `cascade`, `full`, `spec`, `learn`, `agg`, `dp`, `phys`, `wm`, `res`, `ion`, `coh`, `ctr`, `ppo`, or `hcd`. Keep joule costs labeled uncalibrated until an MCU + radio measurement exists. Do not check proprietary BLE stacks or fake SIG certificates into this public card.

## Next measurements (not done)
- Time and current for advertise_only vs listen_window vs tx_slot vs hold on the intended radio.
- Decide whether slot tables are fixed, versioned, or out of this card.
- Wire a skip reason through `policy_gated_executor` without claiming a MAC certificate.
- Optional host stub: `mac_ok()` on a fixture slot table in CI — still not radio firmware.
