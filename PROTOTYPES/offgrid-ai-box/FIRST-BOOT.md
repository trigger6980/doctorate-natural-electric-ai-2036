# First-boot refuse sketch (host only)

This is STATUS next-priority item 4 from the 2026-09-25 cycle: a script that
refuses inference below the documented voltage floor.

## What it is
- `first_boot.py` — host function + CLI (`python first_boot.py 3.2`)
- `test_first_boot.py` — three unit tests on the same floor as `energy_duty.FLOOR_VOLTS`

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
python -m pytest test_first_boot.py -q
```
