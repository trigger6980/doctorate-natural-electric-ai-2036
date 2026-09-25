# Off-Grid AI Box — BOM orientation

This is a **research shopping list**, not a certified build and not a store SKU. Prices below are order-of-magnitude street ranges seen on commodity parts in 2025–2026 and will drift. Substitute freely. No vendor is endorsed.

Companion: [`README.md`](README.md), energy-harvester-tinyml scheduler concepts, Model 35 (hand-crank / solar duty planner) and Model 10 (offline LLM runtime adapter) cards.

## Compute

| Item | Example class | Notes | Approx. USD |
|------|---------------|-------|-------------|
| SBC | Raspberry Pi Zero 2W / Orange Pi Zero class | Lowest idle draw path | 15–35 |
| Alternate SBC | Raspberry Pi 4/5 or equivalent | Only if the optional secondary LLM is required | 35–80 |
| Storage | microSD 32–128 GB industrial if possible | Models + offline index | 8–25 |
| RTC / watchdog | Optional DS3231 or board watchdog | Survives brownouts | 2–8 |

## Power path

| Item | Example class | Notes | Approx. USD |
|------|---------------|-------|-------------|
| PV panel | 6–20 W 5–18 V portable | Indoor harvest is usually not enough for an LLM duty cycle | 15–40 |
| Hand-crank / dynamo | Commercial crank bank or 5 V dynamo | Burst top-up only | 15–40 |
| Power bank / Li-ion pack | 10–20k mAh with USB-C PD if the SBC needs it | Treat as the energy reservoir | 20–50 |
| MPPT / charge board | Small MPPT or “solar power manager” | Do not parallel unknown chargers | 10–30 |
| Supercap (optional) | 1–10 F on the 5 V rail | Softens crank / PV ripple; not the main store | 3–12 |
| Inline voltage sense | ADC on MCU or USB power meter | Required before any “measured joules” claim | 5–20 |

## I/O (all optional)

| Item | Example class | Notes | Approx. USD |
|------|---------------|-------|-------------|
| Display | 2–7 in HDMI / DSI or none (headless) | Headless is the energy-honest default | 0–40 |
| Audio | USB / I2S mic + speaker | Local wake word later; not in v0 | 8–25 |
| Camera | CSI / USB | Only if a card names a vision model | 8–30 |
| Enclosure | IP-rated box + cable glands | Heat and condensation are the real enemies | 10–40 |

## Software bill (no license fees claimed)

- Host OS: Raspberry Pi OS Lite or equivalent Debian.
- Runtime target: **primary = TinyML policy** (threshold / quantized classifier or scheduler, same class as energy-harvester-tinyml). **Optional secondary = llama.cpp-class quantized LLM** only when duty grants INFER and budget supports it.
- Energy duty helper in this folder (`energy_duty.py`) is a **host stub**. It does not read a real ADC.
- Refuse path: pack voltage below `FLOOR_VOLTS` (3.50 V placeholder) → REFUSE/SLEEP → policy SLEEP; no inference runs.

## Energy honesty

- Do not publish runtime hours until a named lab records pack voltage and load current with [`ENTERPRISE/measurement-method.md`](../../ENTERPRISE/measurement-method.md).
- Simulator or placeholder joules from other host tests are not this box’s field numbers.
- If PV + crank cannot cover the chosen model’s idle + burst budget, the honest action is **sleep / refuse**, not a smaller claimed watt-hour number.

## Next hardware slice (not done)

- [ ] Photograph a first physical assembly.
- [ ] Record idle current of the chosen SBC at the intended voltage.
- [x] Decide one primary workload (TinyML policy vs local LLM). **Done:** TinyML-first; LLM optional secondary (see README).
- [ ] Write a first-boot script that refuses inference when the voltage proxy is below a documented threshold.
