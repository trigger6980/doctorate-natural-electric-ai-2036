# Off-Grid AI Box (Portable Self-Powered Intelligence Node)

**Natural Electric prototype #2** — A portable, multi-source-powered AI-in-a-box capable of running local models with zero external connectivity after initial provisioning.

## Goal
Demonstrate a minimal, reproducible portable system in which:
- Multiple energy sources (solar, hand-crank / dynamo, battery bank, USB) feed a shared rail.
- Voltage (or estimated energy state) is observed and treated as a first-class refuse signal.
- A duty policy decides whether to IDLE_LISTEN, INFER, REFUSE, or SLEEP.
- A local (offline) model runtime may run only when the duty and energy budget allow.
- The node remains useful under intermittent harvest and intermittent human crank input.

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
if action == "INFER":
    run_local_model(...)                         # only when budget allows; no WAN fallback
else:
    sleep_or_listen()
```

Host-side helper already in tree:
- [`energy_duty.py`](energy_duty.py) — decides SLEEP / IDLE_LISTEN / INFER / REFUSE from a caller-supplied pack voltage. It does **not** read an ADC.
- Tests: [`test_energy_duty.py`](test_energy_duty.py) (host).

Planned composition with Operator AI Machinery:
- Model 01 (Threshold Energy Scheduler) supplies the live rail floor.
- Model 35 (Hand-Crank + Solar Duty Planner) names the portable source mix (solar_only / crank_assist / hold).
- Model 10 (Offline LLM Runtime Adapter) is the optional GENERATE body when INFER is granted.
- Model 12 checkpoint and Model 11 energy broker may sit in front of any longer graph.

## Directory Layout

- `energy_duty.py` — host duty stub
- `test_energy_duty.py` — host unit tests
- `BOM.md` — commodity parts orientation
- (future) `src/`, `docs/`, first-boot scripts, enclosure notes

## Status (honest)

**Present:** Outline, BOM orientation, host energy-duty stub with unit tests, and explicit links to Model 10 / Model 35 / Model 01.

**Not present:** Trained/quantized on-device models, measured field joules, calibrated pack C, hardware photos, enclosure notes, first-boot scripts, measured idle current, or energy-neutral certificates.

This prototype maps to Model 10 (Offline LLM Runtime Adapter), Model 35 (Hand-Crank + Solar Duty Planner), and reuses Model 01 (Threshold Energy Scheduler) for the rail floor. Host numbers are not field certificates. See also the companion prototype [`../energy-harvester-tinyml/`](../energy-harvester-tinyml/) and [`AGENTS/operator-ai-machinery.md`](../../AGENTS/operator-ai-machinery.md).

## Next vertical slices (ordered, no invented claims)

1. Capture a short host voltage / duty log under controlled pack-voltage fixtures (still host, not field certificate).
2. Wire the duty decision into the same policy interface used by the Operator AI task-graph / policy-gated executor (host path only).
3. Decide one primary workload (TinyML policy vs local LLM) and document the refuse path when the voltage proxy is below the documented floor.
4. Add a measurement-method note under `docs/` once a lab and instrument class are named (see ENTERPRISE/measurement-method.md).
5. Only after (4): publish a labeled result record if pack current and voltage are measured on hardware.

## Reproducibility
All host code runs under ordinary Python unit tests. Board firmware targets commodity SBCs. No proprietary silicon required. Physical builds remain open work.
