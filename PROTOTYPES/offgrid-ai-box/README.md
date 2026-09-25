# Off-Grid AI Box (Portable Self-Powered Intelligence Node)

**Natural Electric prototype #2** — A portable, multi-source-powered AI-in-a-box capable of running local models with zero external connectivity after initial provisioning.

## Goal
Demonstrate a minimal, reproducible portable system in which:
- Multiple energy sources (solar, hand-crank / dynamo, battery bank, USB) feed a shared rail.
- Voltage (or estimated energy state) is observed and treated as a first-class refuse signal.
- A duty policy decides whether to IDLE_LISTEN, INFER, REFUSE, or SLEEP.
- A local (offline) model runtime may run only when the duty and energy budget allow.
- The node remains useful under intermittent harvest and intermittent human crank input.

## Primary workload decision (host documentation)

**Primary:** TinyML policy (threshold / simple quantized classifier or scheduler), the same energy-honest class as the companion [`../energy-harvester-tinyml/`](../energy-harvester-tinyml/) prototype.

**Optional secondary:** Local offline LLM (Model 10 class) only when the duty grants `INFER` **and** the energy budget (joules or voltage proxy) supports the higher cost. Secondary is not the default duty cycle.

Rationale (honesty, not a product claim):
- Intermittent solar + hand-crank favors low idle and short burst inference.
- TinyML keeps the refuse path cheap and testable on host fixtures.
- An always-on or frequently-woken LLM would violate the energy-first refuse signal under the documented floor.

This decision is a documentation and architecture choice for the host path. It does not claim trained weights, measured joules, or a field certificate.

## Refuse path when voltage proxy is below the floor

Documented floor: `FLOOR_VOLTS = 3.50` in [`energy_duty.py`](energy_duty.py) (1S Li-ion proxy placeholder; **not** a lab calibration).

| Condition | `infer_requested` | Duty action | Policy mapping | Runtime effect |
| --- | --- | --- | --- | --- |
| `pack_volts < FLOOR_VOLTS` | True | `REFUSE` | `SLEEP` | No inference; graph aborted with `policy_sleep` |
| `pack_volts < FLOOR_VOLTS` | False | `SLEEP` | `SLEEP` | Idle/sleep only |
| `pack_volts >= FLOOR_VOLTS` | True | `INFER` | `INFER` | Inference allowed if joule budget also permits |
| `pack_volts >= FLOOR_VOLTS` | False | `IDLE_LISTEN` | `SENSE` | Listen / sense-class only |

Implementation (host):
- `energy_duty.decide(...)` returns the duty string.
- `duty_to_policy.duty_string_to_policy_action` / `make_duty_policy_fn` map `REFUSE` and `SLEEP` onto the Operator AI `Action.SLEEP` (or string `"SLEEP"`).
- `policy_gated_executor.decide_and_run` then sets `aborted_reason = "policy_sleep"` and runs no tagged tasks.

Low voltage always wins over an inference request. There is no “try the LLM anyway” path on the host stubs.

## Hardware Target (BOM orientation)

See [`BOM.md`](BOM.md) for a commodity parts orientation (not a store SKU). Minimum viable path:

1. Compute: Raspberry Pi Zero 2W or equivalent low-power SBC / Android compute module.
2. Power: commercial solar + hand-crank power bank (or discrete solar + MPPT + LiPo + hand-crank generator).
3. Storage: sufficient for one or more quantized models (8–32 GB class).
4. I/O: optional small display or pure headless with Bluetooth/USB keyboard.

Full schematic guidance and photos will be added as physical builds are completed. Headless is the energy-honest default.

## Software Architecture

```
pack_volts = read_pack_voltage()                 # proxy for available energy (caller-supplied on host)
action     = energy_duty.decide(pack_volts, ...) # SLEEP / IDLE_LISTEN / INFER / REFUSE
policy     = duty_to_policy.map(action)          # → Operator AI Action (SLEEP/SENSE/INFER)
if policy allows INFER:
    run_primary_workload(...)                    # TinyML policy first; optional LLM only if budgeted
else:
    sleep_or_listen()
```

Host-side helpers already in tree:
- [`energy_duty.py`](energy_duty.py) — decides SLEEP / IDLE_LISTEN / INFER / REFUSE from a caller-supplied pack voltage. It does **not** read an ADC.
- [`duty_to_policy.py`](duty_to_policy.py) — maps those strings onto the Operator AI policy Action interface and supplies a `policy_fn` for `decide_and_run` (host path). Also provides `fixture_log` for controlled voltage rows.
- Tests: [`test_energy_duty.py`](test_energy_duty.py), [`test_duty_to_policy.py`](test_duty_to_policy.py) (host).

Planned composition with Operator AI Machinery:
- Model 01 (Threshold Energy Scheduler) supplies the live rail floor.
- Model 35 (Hand-Crank + Solar Duty Planner) names the portable source mix (solar_only / crank_assist / hold).
- Model 10 (Offline LLM Runtime Adapter) is the **optional** GENERATE body when INFER is granted and the secondary workload is enabled.
- Primary TinyML policy aligns with the energy-harvester-tinyml stack (Models 01 / 05).
- Model 12 checkpoint and Model 11 energy broker may sit in front of any longer graph.

## Directory Layout

- `energy_duty.py` — host duty stub
- `duty_to_policy.py` — host adapter to policy Action / policy_fn
- `test_energy_duty.py` — host unit tests for duty
- `test_duty_to_policy.py` — host unit tests for the adapter
- `BOM.md` — commodity parts orientation
- (future) `src/`, `docs/`, first-boot scripts, enclosure notes

## Status (honest)

**Present:** Outline, BOM orientation, host energy-duty stub with unit tests, host duty→policy adapter with unit tests, controlled host voltage fixture log (sandbox), primary-workload decision (TinyML-first, LLM optional secondary), documented refuse path below floor, and explicit links to Model 10 / Model 35 / Model 01.

**Not present:** Trained/quantized on-device models, measured field joules, calibrated pack C, hardware photos, enclosure notes, first-boot scripts, measured idle current, or energy-neutral certificates.

This prototype maps to Model 10 (Offline LLM Runtime Adapter — optional secondary), Model 35 (Hand-Crank + Solar Duty Planner), and reuses Model 01 (Threshold Energy Scheduler) for the rail floor. Host numbers are not field certificates. See also the companion prototype [`../energy-harvester-tinyml/`](../energy-harvester-tinyml/) and [`AGENTS/operator-ai-machinery.md`](../../AGENTS/operator-ai-machinery.md).

## Next vertical slices (ordered, no invented claims)

1. Capture a short host voltage / duty log under controlled pack-voltage fixtures (still host, not field certificate). **Done (host):** `duty_to_policy.fixture_log` + `SANDBOX/out/offgrid_duty_log.json`.
2. Wire the duty decision into the same policy interface used by the Operator AI task-graph / policy-gated executor (host path only). **Done (host):** `make_duty_policy_fn` → `decide_and_run(policy_fn=...)`.
3. Decide one primary workload (TinyML policy vs local LLM) and document the refuse path when the voltage proxy is below the documented floor. **Done (documentation):** TinyML-first; refuse path table above; BOM checkbox closed.
4. Add a measurement-method note under `docs/` once a lab and instrument class are named (see ENTERPRISE/measurement-method.md).
5. Only after (4): publish a labeled result record if pack current and voltage are measured on hardware.

## Reproducibility
All host code runs under ordinary Python unit tests. Board firmware targets commodity SBCs. No proprietary silicon required. Physical builds remain open work.
