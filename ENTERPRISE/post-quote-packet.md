# Post-quote packet checklist (no prices)

This page lists what a **written packet** should contain after a quote drafted from [`quote-draft-outline.md`](quote-draft-outline.md) is accepted in writing. It is not a shipping SLA, not a checkout, and not a claim that any packet has already been sent.

Companions: [`order-and-contract.md`](order-and-contract.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md), [`inquiry-response-template.md`](inquiry-response-template.md), [`licensing-boundary.md`](licensing-boundary.md), [`well-being-alignment.md`](well-being-alignment.md).

## When this checklist may be used

Only after:
1. The six completeness items are present.
2. A quote following the ten-section outline exists *off-repo*.
3. The buyer has accepted that quote in writing.

Until those three are true, the next action is still questions or a quote — not a packet.

## Packet contents (minimum honest set)

| Item | Public tree copy | Private delivery | Notes |
| --- | --- | --- | --- |
| Model cards named in the quote | Yes | Optional signed snapshot | Cards 02–17 are interfaces unless the quote lists extra files |
| Host tests named in the quote | Yes | Optional | Still laptop/CI tests, not field certification |
| Energy-honesty table as agreed | Yes (template) | Filled copy | Do not upgrade “to-be-measured” after acceptance |
| BOM / integration notes if in scope | If already public | If custom | No invented part numbers |
| Private pack (weights, indexes, measurement files) | No | Only if the quote listed them | Most public cards do not include these |
| Transfer method | n/a | Air-gap media or private repo, as quoted | No telemetry back-channel |

## What must be labeled in the packet cover sheet

- Model numbers and identical vs custom (copied, not inferred).
- Deliverable shape (research replica / field customization / operator integration / sovereign).
- Who measures joules (buyer lab / joint / later phase).
- Which files are public-tree copies vs private artifacts.
- Explicit out-of-scope list from the quote (weights, flash mapping, coil/piezo/photodiode drivers, listed-appliance claims, Generator COP, TPM, measured hash or parse joules — unless the quote moved a row in-scope).

## Language that must not appear on the cover sheet

- Customer logos or case studies this repository does not have.
- SLA or MTBF numbers that have not been measured as a service.
- Claims that host sandbox logs certify field energy or heat stages.
- Claims that cards 02–17 are licensed weight files.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the accepted quote sections 1–10 without rewriting energy marks.
2. List each file as public-tree copy or private.
3. Name the transfer method that was quoted.
4. Do not add a second commercial figure on the cover sheet.

No prices, customers, or SLAs are added by this page.
