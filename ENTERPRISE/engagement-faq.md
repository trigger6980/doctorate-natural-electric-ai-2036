# Enterprise engagement FAQ (process only)

This page restates how a conversation becomes a written quote. It does not add prices, customers, SLAs, or case studies. Companion files: [`order-and-contract.md`](order-and-contract.md), [`inquiry-template.md`](inquiry-template.md), [`scope-assumptions.md`](scope-assumptions.md).

## Identical copy vs custom variant

**Identical copy** means the public architecture, interface table, and host tests stay the contract of record. Delivery under contract may still include private packaging (a snapshot, a signed tree, air-gap media). It does not mean weights or calibrated joule numbers exist in the public tree.

**Custom variant** means at least one of energy budget, sensors, security boundary, or scale changes. The public model number remains ancestry (`01-custom-<slug>`) unless the contract requires a private identifier.

If you are unsure which you need, mark the inquiry as *undecided* and say which constraint is driving the work (air-gap, measured joules, plant-floor sensors). Do not pick “custom” to sound serious.

## What a complete inquiry contains
1. The header and model list from `inquiry-template.md`.
2. Every energy-honesty line marked agreed / to-be-measured / out of scope.
3. The scope-assumptions table with the same marks.
4. A deliverable-shape checkbox (research replica / field customization / operator integration / sovereign).

Incomplete inquiries receive questions. They do not receive a draft quote.

## How licensing language stays honest
- Public licenses (MIT for code, CC-BY-4.0 for docs, unless a file says otherwise) cover study and non-commercial exploration of the public tree.
- Commercial or production use of identical or derivative models is intended to occur under a written contract.
- A model card is an interface contract, not a binary, not a weight file, and not a certified energy rating.
- Operator AI pieces in this repository are host sketches. On-device flash mapping and hardware energy observers are still open unless a later commit says they shipped.

## Value propositions that are allowed in a quote cover letter
Use only claims the public tree can support:

- Energy-first refusal: host policies that skip work when the budget says no.
- Inspectable operators: task graphs and checkpoints a buyer can read.
- Catalog compatibility: custom work should keep the public model number as ancestry where possible.
- Human well-being mission: off-grid and low-power intelligence for places the grid does not reliably reach.

Do not put measured MTBF, customer logos, or field certification in a cover letter until those objects exist.

## What the maintainer will ask next
Typical clarifying questions after a complete inquiry:
- Which files would count as “done” for you (cards, tests, BOM notes, private pack)?
- Who measures joules — buyer lab, joint test, or later phase?
- Is Operator AI in scope or only the model card?
- Air-gap media or private repository transfer?

## What this page will not grow into
No rate card, no checkout SKU, no invented testimonials. If a repeatable quote process is later measured, STATUS.md will say so.
