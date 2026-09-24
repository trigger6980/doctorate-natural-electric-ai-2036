# Inquiry completeness gate

This page is a checklist the maintainer can apply before drafting a quote. It is not an SLA, not a price list, and not an intake bot.

Companions: [`inquiry-template.md`](inquiry-template.md), [`scope-assumptions.md`](scope-assumptions.md), [`engagement-faq.md`](engagement-faq.md), [`well-being-alignment.md`](well-being-alignment.md), [`order-and-contract.md`](order-and-contract.md), [`measurement-hold.md`](measurement-hold.md), [`quote-draft-outline.md`](quote-draft-outline.md).

## Complete enough to discuss

An inquiry is complete enough when all of the following are present:

1. Model number(s) from the public catalog, or an explicit “undecided + driving constraint.”
2. Identical vs custom vs undecided.
3. Deployment context in one sentence (lab, field node, plant floor, air-gap shop).
4. Energy-honesty marks on the inquiry template (agreed / to-be-measured / out of scope).
5. Scope-assumptions table with the same marks.
6. Deliverable-shape checkbox (research replica / field customization / operator integration / sovereign).

Missing any of those six items means the next action is questions, not a draft quote.

Host helper: `ENTERPRISE/inquiry_completeness.py`. Optional field `energy_evidence` is *not* one of the six items. If it is set to an observer token (`observer`, `energy_observer`, `energy_observer.json`, `host_placeholder`, `hardware_pending`, `sandbox_observer`, `claim_scan`), the helper returns `observer_not_evidence` and `quote_action` is `ask`. That token is the same refuse used by `AGENTS/claim_gate.py`.

Optional field `intended_use` is also not one of the six items. Allowed values: `discuss`, `ask`, `host_log`, `sandbox_demo`. Refused values (same set as the claim gate): `field_generation`, `quote_evidence`, `result_record`. Those return `observer_not_evidence` and `quote_action` is `ask`. Unknown uses return `unknown_claim` and also `ask`.

`stamp(inquiry)` returns a host label packet (`items_present`, `refuse_reason`, `quote_action`, `intended_use`, `energy_evidence`, `inquiry_ok`, `outline_ready`, `price_allowed`, `outline_sections`). It is a checklist snapshot, not a signed quote and not energy evidence. The sandbox writes the same packet to `SANDBOX/out/inquiry_stamp.json`.

`outline_ready(inquiry)` is true only when `quote_action` is `draft`. `price_allowed` is always `false` on this host helper. Section names match [`quote-draft-outline.md`](quote-draft-outline.md); they are headings, not filled commercial terms.

## Incomplete patterns that stay incomplete

- “Need the 50 models” with no identical/custom split.
- A request for measured COP, kWh, or crop yield taken from this public tree.
- A request to hide an energy cost or to treat host-sandbox joules as certified field performance.
- Attaching `SANDBOX/out/energy_observer.json` as proof of harvest or consumption.
- Treating a host `claim_scan` of `host_log: ok` as permission to quote joules.
- Treating `inquiry_stamp.quote_action = draft` as a price or SLA.
- Treating `outline_ready = true` as permission to publish a rate card in this repository.
- A cover letter that needs customer logos or SLA numbers this repository does not have.

Those patterns fail the well-being tests in `well-being-alignment.md`. Narrow scope or decline; do not invent a case study.

## What completeness does *not* imply

- A turnaround time.
- A published price.
- That weights, flash mapping, or hardware observers exist.
- That Generator 01–03 sketches are listed appliances.
- That a host claim-gate pass (`host_log` / `sandbox_demo`) is a field certificate.
- That `stamp()` is a contract record.
- That `price_allowed` will become true in this public tree.

## Maintainer reply shape (when complete)

1. Acknowledge receipt and list the six items as present.
2. Ask who measures joules.
3. Ask which files count as “done.”
4. Only then consider writing a quote document off-repo.

No prices, customers, or SLAs are added by this page.
