# Placeholder engagement tiers (not a rate card)

This page names **shapes of work**, not prices. There is no checkout SKU, no published dollar amount, and no implied availability SLA. A written quote, if one is ever issued, follows [`quote-draft-outline.md`](quote-draft-outline.md) after a complete inquiry.

Companion files: [`order-and-contract.md`](order-and-contract.md), [`engagement-faq.md`](engagement-faq.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`well-being-alignment.md`](well-being-alignment.md), [`licensing-boundary.md`](licensing-boundary.md).

## Why tiers exist here
Buyers asked which *kind* of engagement they were requesting. Naming the kind early reduces mismatched quotes. It does **not** create a menu of fees.

If a later contract publishes numbers, STATUS.md will say so. Until then every money field stays blank on purpose.

## Tiers (placeholders only)

| Placeholder name | What it usually means | What it never means |
| --- | --- | --- |
| **Study replica** | Public cards, host tests, and documentation packaged as a snapshot the buyer can read offline | Weights, measured joules, or field certification |
| **Field customization** | A `NN-custom-<slug>` ancestry card plus named sensors / energy rows marked `to-be-measured` | A calibrated plant, an SLA, or a customer logo |
| **Operator integration** | Wiring an existing host gate (`gate_task`, broker, checkpoint, duty→policy) into the buyer’s own runner | On-device flash mapping or a hardware energy observer |
| **Sovereign / air-gap pack** | Private transfer media and a written licensing boundary | Implied export clearance or classified handling |
| **Measurement phase** | Who-measures, instrument class, method class, then a labeled result record | A certificate that the public tree does not contain |

Pick one primary tier on the inquiry. A second tier may be listed as *later phase* only. Do not stack all five to sound complete.

## Prototype workload alignment (truthful scope)

Public prototypes document a **primary workload** so operator-integration and study-replica scopes stay honest:

- Off-Grid AI Box (`PROTOTYPES/offgrid-ai-box/`): **TinyML policy first**; offline LLM is optional secondary only when duty grants INFER and budget supports it. Refuse path below the documented voltage floor is SLEEP / policy_sleep — no inference runs.
- Energy-Harvester TinyML: same energy-first class (Models 01 / 05).

When an inquiry names “operator integration,” the public refuse path and primary-workload note are part of the inspectable surface. They are not a product guarantee and do not invent measured joules.

## Alignment with the mission
Every tier is intended to stay compatible with Natural Electric + Future AI human well-being:

- Energy state remains a first-class refuse signal.
- Off-grid and low-power sites are first-class contexts, not afterthoughts.
- Public catalog ancestry is kept wherever a custom card is required.
- No invented customers, revenue, or measured MTBF appear in this file.

## How a maintainer uses this page
1. Read the inquiry’s deliverable-shape checkbox.
2. Map it onto one row above.
3. If the map is unclear, ask — do not invent a sixth tier.
4. If the request is already answered by a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md) instead of a tier.
5. If energy rows stay `to-be-measured` with no named lab, use [`measurement-hold.md`](measurement-hold.md).

## What this page will not grow into
No rate card. No “starting at” language. No invented case studies. Placeholder names may be renamed if a later complete inquiry proves they confuse buyers; that rename is a documentation change, not a commercial launch.
