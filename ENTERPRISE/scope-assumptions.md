# Scope assumptions for a quote

Use this page with [order-and-contract.md](order-and-contract.md). It is a **checklist of facts the quote must state**, not a price list and not a service catalog.

Mission alignment: quotes should keep energy accounting honest and should not imply measured hardware performance when only the host simulator exists.

## Assumptions the quote must label as true or false

| Assumption | Public-tree default today | Why it matters |
| --- | --- | --- |
| Energy costs are measured on buyer hardware | False — cards 01–07 mark simulator placeholders | A quote that skips this is selling fiction |
| Model 05 `C_farads` is calibrated | False — helper exists, fit does not | Remaining joules stay untrusted |
| Models 06–07 have trained weights | False — interface only | Inference deliverables are design notes unless scoped |
| Operator AI checkpoints persist on-device flash | False — host JSON file only | Do not promise MCU wear-leveling |
| SLA / response-time metric exists | False | Do not put hours-to-reply in a quote as if measured |
| Public licenses cover production shipment | Not assumed | Production use is intended under explicit contract |

## How to attach this to an inquiry
Paste the table into the `enterprise-inquiry` issue and mark each row agreed / to-be-measured / out of scope. The maintainer will not invent a row.

## What this page does not contain
- Prices
- Customer names
- Turnaround times
- Certified safety or EMC claims
