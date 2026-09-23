# Enterprise engagement FAQ (process only)

This page restates how a conversation becomes a written quote. It does not add prices, customers, SLAs, or case studies. Companion files: [`order-and-contract.md`](order-and-contract.md), [`inquiry-template.md`](inquiry-template.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md), [`inquiry-response-template.md`](inquiry-response-template.md), [`post-quote-packet.md`](post-quote-packet.md), [`change-order.md`](change-order.md), [`engagement-closeout.md`](engagement-closeout.md), [`records-retention.md`](records-retention.md), [`correction-notice.md`](correction-notice.md), [`reopen-after-close.md`](reopen-after-close.md), [`decline-or-defer.md`](decline-or-defer.md), [`handoff-to-public-tree.md`](handoff-to-public-tree.md), [`measurement-hold.md`](measurement-hold.md), [`named-lab-plan.md`](named-lab-plan.md), [`instrument-list.md`](instrument-list.md), [`measurement-method.md`](measurement-method.md), [`result-record.md`](result-record.md), [`placeholder-engagement-tiers.md`](placeholder-engagement-tiers.md).

## Identical copy vs custom variant

**Identical copy** means the public architecture, interface table, and host tests stay the contract of record. Delivery under contract may still include private packaging (a snapshot, a signed tree, air-gap media). It does not mean weights or calibrated joule numbers exist in the public tree.

**Custom variant** means at least one of energy budget, sensors, security boundary, or scale changes. The public model number remains ancestry (`01-custom-<slug>`) unless the contract requires a private identifier.

If you are unsure which you need, mark the inquiry as *undecided* and say which constraint is driving the work (air-gap, measured joules, plant-floor sensors). Do not pick “custom” to sound serious.

## What a complete inquiry contains
The six-item gate is listed in [`inquiry-completeness.md`](inquiry-completeness.md). In short:

1. The header and model list from `inquiry-template.md`.
2. Every energy-honesty line marked agreed / to-be-measured / out of scope.
3. The scope-assumptions table with the same marks.
4. A deliverable-shape checkbox (research replica / field customization / operator integration / sovereign). Map that checkbox onto one row in [`placeholder-engagement-tiers.md`](placeholder-engagement-tiers.md) — those names are work shapes, not prices.
5. Identical vs custom vs undecided.
6. Deployment context in one sentence.

Incomplete inquiries receive questions. They do not receive a draft quote. After the gate, a written quote should follow [`quote-draft-outline.md`](quote-draft-outline.md). The maintainer paste-back lives in [`inquiry-response-template.md`](inquiry-response-template.md). After written acceptance, packet contents live in [`post-quote-packet.md`](post-quote-packet.md). After a packet exists, scope changes follow [`change-order.md`](change-order.md). After packet and change orders settle, closeout follows [`engagement-closeout.md`](engagement-closeout.md). After closeout, keep vs discard follows [`records-retention.md`](records-retention.md). After retention, factual corrections follow [`correction-notice.md`](correction-notice.md). After closeout and retention, new scope follows [`reopen-after-close.md`](reopen-after-close.md) as a new inquiry — not as a correction. An inquiry that cannot be quoted honestly follows [`decline-or-defer.md`](decline-or-defer.md). A question already answered by the public catalog follows [`handoff-to-public-tree.md`](handoff-to-public-tree.md). A complete inquiry that still lacks a named measurement plan follows [`measurement-hold.md`](measurement-hold.md). When who-measures is named, record it with [`named-lab-plan.md`](named-lab-plan.md). When an instrument class is named after that plan, record it with [`instrument-list.md`](instrument-list.md). When a method class is named after that list, record it with [`measurement-method.md`](measurement-method.md). When a labeled result exists after that method, record it with [`result-record.md`](result-record.md).

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

Do not put measured MTBF, customer logos, or field certification in a cover letter until those objects exist. Do not treat `SANDBOX/out/gen03_decisions.json` as a heat-stage certificate. Do not treat Model 19 `neutral_ok` as an energy-neutral certificate. Do not treat Model 20 `disagg_ok` as a NILM certificate. Do not treat Model 21 `rf_ok` as a control certificate. Do not treat Model 22 `cascade_ok` as an inference certificate. Do not treat Model 23 `kv_ok` as a context-window certificate. Do not treat Model 24 `spec_ok` as an accept-rate certificate. Do not treat Model 25 `learn_ok` as a plasticity certificate. Do not treat Model 26 `agg_ok` as a federation or privacy certificate. Do not treat Model 27 `dp_ok` as a differential-privacy certificate. Do not treat Model 28 `phys_ok` as a motion or safety-PLC certificate. Do not treat Model 29 `wm_ok` as a dynamics or spatial-intelligence certificate. Do not treat Model 30 `res_ok` as a reservoir or analog-neuromorphic certificate.

## What the maintainer will ask next
Typical clarifying questions after a complete inquiry:
- Which files would count as “done” for you (cards, tests, BOM notes, private pack)?
- Which placeholder tier names the shape of work (study replica / field customization / operator integration / sovereign pack / measurement phase)?
- Who measures joules — buyer lab, joint test, or later phase?
- Which instrument class will take those rows — only if already named?
- Which method class will take those rows — only if already named?
- Which result source and units class exist — only if already labeled?
- Is Operator AI in scope or only the model card?
- Air-gap media or private repository transfer?

Paste order for those replies is in [`inquiry-response-template.md`](inquiry-response-template.md). After acceptance, use [`post-quote-packet.md`](post-quote-packet.md). After a packet exists, use [`change-order.md`](change-order.md). After settled changes, use [`engagement-closeout.md`](engagement-closeout.md). After closeout, use [`records-retention.md`](records-retention.md). After retention, use [`correction-notice.md`](correction-notice.md) only for errors in already-named files. After closeout, new scope uses [`reopen-after-close.md`](reopen-after-close.md). If the request cannot be quoted honestly, use [`decline-or-defer.md`](decline-or-defer.md). If the request is already answered by a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md). If energy rows stay `to-be-measured` with no named lab, use [`measurement-hold.md`](measurement-hold.md). If who-measures is named, use [`named-lab-plan.md`](named-lab-plan.md). If an instrument class is named after that plan, use [`instrument-list.md`](instrument-list.md). If a method class is named after that list, use [`measurement-method.md`](measurement-method.md). If a labeled result exists after that method, use [`result-record.md`](result-record.md).

## What this page will not grow into
No rate card, no checkout SKU, no invented testimonials. Placeholder engagement tiers name work shapes only. If a repeatable quote process is later measured, STATUS.md will say so.
