# First-boot refuse sketch (host only)

Host script that refuses inference below the documented voltage floor.

## What it is
- `first_boot.py` — host function + CLI (`python first_boot.py 3.2`)
- `test_first_boot.py` — unit tests on the same floor as `energy_duty.FLOOR_VOLTS`
  (including optional `via_host_reader` cases)
- `host_voltage_reader.py` — pure host reader that returns a pack_volts record
  suitable for feeding `first_boot` / `energy_duty.decide` (sources:
  `host_placeholder` | `hardware_pending` only). Shared helper
  `feed_via_reader(pack_volts, source=...)` returns `(feed_volts, reader_meta)`
  and is the single path used by first_boot, duty_to_policy.fixture_log, and
  compose_first_boot.
- `duty_to_policy.fixture_log(..., via_host_reader=True)` — same feed contract
  for the duty → policy adapter path (see `test_duty_to_policy.py`)
- `SANDBOX/compose_first_boot_demo.py` — same feed contract for composition
  with optional Model 05 joules when `C_farads` is explicit

## What it is not
- Not ESP32 firmware
- Not an ADC read
- Not a field energy certificate
- Not a reason to claim measured joules in a quote

## Behavior
| Pack volts vs `FLOOR_VOLTS` (3.50 placeholder) | infer requested | Result |
| --- | --- | --- |
| below floor | yes | REFUSE → policy SLEEP, `inference_allowed=false` |
| below floor | no | SLEEP, no workload |
| at/above floor | yes | INFER, primary workload `tinyml_policy` |
| at/above floor | no | IDLE_LISTEN, no workload |

Optional secondary offline LLM is only named when `allow_secondary_llm=True`
**and** inference is allowed. Default stays TinyML-first.

## Run
```
cd PROTOTYPES/offgrid-ai-box
python first_boot.py 3.2
python -m pytest test_first_boot.py test_host_voltage_reader.py test_duty_to_policy.py -q
```

## Host policy interface contract for a future ADC (documentation only)

A future on-device voltage reader (ESP32-C3 ADC, SBC sysfs, USB power meter, etc.)
may feed this host path only by satisfying the same call shape already used by
`energy_duty.decide` and `first_boot`:

```text
pack_volts: float          # >= 0; caller-supplied or measured
infer_requested: bool      # whether an inference duty is being asked
floor_volts: float = 3.50  # documented placeholder; not a lab calibration
```

Return shape from `first_boot` (host record, never a field certificate):

```text
{
  "pack_volts": float,
  "floor_volts": float,
  "infer_requested": bool,
  "duty": "SLEEP" | "IDLE_LISTEN" | "INFER" | "REFUSE",
  "policy_action": "SLEEP" | "SENSE" | "INFER" | ...,
  "inference_allowed": bool,
  "workload": "tinyml_policy" | "offline_llm" | None,
  "via_host_reader": bool,
  "source": "host_first_boot",
  "is_field_measurement": False,
  "is_firmware": False
  # when via_host_reader=True also:
  # "reader_source": "host_placeholder" | "hardware_pending",
  # "reader_is_field_measurement": False,
  # "reader_is_firmware": False
}
```

### Host voltage reader (explicit feed path)

`host_voltage_reader.read_pack_volts(...)` produces a small record that can be
passed through `as_feed` into `first_boot`, `energy_duty.decide`, or
`duty_to_policy.fixture_log`:

```text
{
  "pack_volts": float,
  "source": "host_placeholder" | "hardware_pending",
  "is_field_measurement": False,
  "is_firmware": False,
  "note": "..."
}
```

Preferred single entry for the optional reader path is
`feed_via_reader(pack_volts, source=...)` → `(feed_volts, reader_meta)`.
`first_boot(..., via_host_reader=True, reader_source=...)`,
`duty_to_policy.fixture_log(..., via_host_reader=True)`, and
`compose_first_boot(..., via_host_reader=True)` all use that helper.
All three remain host-only.

Rules that stay true after any hardware plug-in:

1. Low voltage always wins; no “try the model anyway” path.
2. `is_field_measurement` remains False until a named lab + instrument class +
   measurement-method note exist and a result record is labeled (see the full
   chain under ENTERPRISE/: measurement-hold → named-lab-plan → instrument-list
   → measurement-method → result-record). Host stubs never skip that chain.
3. Host composition with Model 05 joules is allowed only when `C_farads` is
   explicit; that value is analytic, not measured.
4. On-device first-boot firmware, calibrated C, idle current photos, and
   measured joules remain open work and are not claimed by this sketch.
5. The host reader never emits source=`measured`; that label is refused so
   sandbox numbers cannot be promoted into field claims.
6. The duty adapter (`duty_to_policy.fixture_log`), the first-boot path, and
   the composition path share the same feed contract via `feed_via_reader`;
   none is firmware.
7. Host stubs (`host_voltage_reader`, `feed_via_reader`, `first_boot`,
   `duty_to_policy.fixture_log`, sandbox composition demos, `energy_observer`,
   `claim_gate`) never substitute for a named-lab + instrument-class +
   measurement-method plan. `claim_gate` refuses field_generation /
   quote_evidence / result_record with the token `observer_not_evidence`.

This contract advances the STATUS priority “wire a real ADC into the same
policy interface” without inventing firmware, serial numbers, or field numbers.
