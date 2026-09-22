# 18 — Local Mesh Routing Policy

**Domain:** Sovereign Networking  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no radio driver, no mesh stack, no measured hop joules)  
**Operator role:** Optional host gate that refuses a forward/send step when the local energy rail or an air-gap allow-list says the hop is not permitted. Not a mesh product and not a routing protocol implementation.

## Description
Sovereign and off-grid nodes still need a cheap answer to “may this packet leave this node, and toward which named neighbor?” A full mesh stack (radio duty cycle, neighbor discovery, multi-hop forwarding firmware) is out of scope for harvested-power nodes until the energy cost of a single hop is measured on the intended radio + MCU pair.

This card specifies the host-facing interface. There is **no radio driver, no neighbor table firmware, and no measured hop energy** in this repository. Numbers below are design targets, not bench results.

Honesty rules:
- A refused hop is a *policy event*, not proof of a jammed radio or a hostile neighbor.
- Host simulation of a route table on a laptop is not the same as on-device radio measurement.
- Do not claim LoRaWAN, Thread, Zigbee, 6LoWPAN, or “sovereign mesh certified” status from this card.
- Distinct from Model 17: Model 17 answers “do these config bytes mean an allowed policy?” This card answers “may a named next-hop consume energy right now?”
- Distinct from Model 11: Model 11 partitions a *local* joule pool among tasks. This card decides whether a *forward* task is even legal.
- Distinct from Model 36: Model 36 is the MAC-layer energy sketch. This card is the policy layer above it.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `neighbor_id` | input | Named next hop from a prior air-gap copy of the allow-list |
| `payload_class` | input | Short class (`control`, `telemetry`, `bulk`) — not a byte dump of the packet |
| `EnergyState` | input | Shared Model 01 rail so a hop can be refused when energy is low |
| `config_ok` | input | Optional Model 17 result; a schema miss should refuse the hop |
| `integrity_ok` | input | Optional Model 16 result; a digest miss should refuse the hop |
| `route_ok` | output | Boolean: neighbor allowed + class allowed + energy sufficient |
| `refuse_reason` | output | `energy` / `deny_neighbor` / `deny_class` / `config` / `integrity` / `ok` |
| `joules_used_est` | output | Placeholder cost of this policy decision (not the radio TX) |

Planned entry points:
- `may_forward(neighbor_id, payload_class, energy_state) -> RouteResult`
- `may_tx(energy_state) -> bool` — refuse when Model 01 would choose SLEEP
- `gate_task(task_id, route_ok) -> allow | skip` — Operator AI policy hook

No host helper is checked in for this card yet. A later stub may evaluate a fixture neighbor table on the laptop CI runner; that is still not a radio stack.

Typical composition:
1. Model 16 `audit()` — routing table bytes match the air-gap copy.
2. Model 17 `validate()` — those bytes still satisfy the declared schema.
3. Model 18 `may_forward()` — the named neighbor and class are allowed *and* the rail can pay.
4. Only then `gate_task(allow)` for a send step.

A valid schema with an energy miss must still refuse. A charged rail with a deny-listed neighbor must still refuse.

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the intended MCU + radio before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Policy lookup on a small neighbor table (host sim) | 0.0005–0.005 J | Cheap allow/deny |
| Skip (policy = SLEEP or deny) | 0 J extra | Gate via Model 01 |
| Actual radio TX / RX of one hop | unknown | Do not schedule until measured |
| Neighbor discovery / flooding | unknown | Out of scope for this card |

Safety rules:
- Never schedule a radio TX when `rail_voltage_v` is below Model 01 `v_min_safe`.
- Never treat `route_ok` as proof the *payload* is good — only that the hop is allowed under the current table and energy state.
- Do not invent RSSI, SNR, or hop-count metrics in host logs.

## Key Traits
- Forward permission is a refuse/allow gate, not a mesh-management product
- Reuses Model 01 energy refusal so a hop cannot drain a dying node
- Intended to run *after* Models 16 and 17 so bytes, meaning, and hop policy are all checked
- Compatible with sovereign / air-gap delivery language on the enterprise pages

## Implementation Notes
Not implemented. When added, live under `AGENTS/` next to the policy-gated executor so a skip reason can be `route` as well as `energy`, `policy`, `integrity`, or `config`. Keep joule costs labeled uncalibrated until an MCU + radio measurement exists. Do not fetch neighbor tables over a live network from this card.

## Next measurements (not done)
- Time and current for a policy lookup vs a real TX pulse on the intended radio.
- Decide whether neighbor tables live in host JSON (like Model 12 checkpoints) or on write-once media beside Model 16 digests.
- Wire a skip reason through `policy_gated_executor` without claiming a mesh-protocol implementation.
- Optional host stub: `may_forward()` a fixture table in CI — still not on-device radio policy.
