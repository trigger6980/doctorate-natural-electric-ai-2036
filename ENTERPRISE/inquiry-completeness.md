# Inquiry completeness gate

This page is a checklist the maintainer can apply before drafting a quote. It is not an SLA, not a price list, and not an intake bot.

Companions: [`inquiry-template.md`](inquiry-template.md), [`scope-assumptions.md`](scope-assumptions.md), [`engagement-faq.md`](engagement-faq.md), [`well-being-alignment.md`](well-being-alignment.md), [`order-and-contract.md`](order-and-contract.md), [`measurement-hold.md`](measurement-hold.md).

## Complete enough to discuss

An inquiry is complete enough when all of the following are present:

1. Model number(s) from the public catalog, or an explicit “undecided + driving constraint.”
2. Identical vs custom vs undecided.
3. Deployment context in one sentence (lab, field node, plant floor, air-gap shop).
4. Energy-honesty marks on the inquiry template (agreed / to-be-measured / out of scope).
5. Scope-assumptions table with the same marks.
6. Deliverable-shape checkbox (research replica / field customization / operator integration / sovereign).

Missing any of those six items means the next action is questions, not a draft quote.

Host helper: `ENTERPRISE/inquiry_completeness.py`. Optional field `energy_evidence` is *not* one of the six items. If it is set to an observer token (`observer`, `energy_observer`, `energy_observer.json`, `host_placeholder`, `sandbox_observer`), the helper returns `observer_not_evidence` and `quote_action` is `ask`. That token is the same refuse used by `AGENTS/claim_gate.py`.

## Incomplete patterns that stay incomplete

- “Need the 50 models” with no identical/custom split.
- A request for measured COP, kWh, or crop yield taken from this public tree.
- A request to hide an energy cost or to treat host-sandbox joules as certified field performance.
- Attaching `SANDBOX/out/energy_observer.json` as proof of harvest or consumption.
- A cover letter that needs customer logos or SLA numbers this repository does not have.

Those patterns fail the well-being tests in `well-being-alignment.md`. Narrow scope or decline; do not invent a case study.

## What completeness does *not* imply

- A turnaround time.
- A published price.
- That weights, flash mapping, or hardware observers exist.
- That Generator 01–03 sketches are listed appliances.
- That a host claim-gate pass (`host_log` / `sandbox_demo`) is a field certificate.

## Maintainer reply shape (when complete)

1. Acknowledge receipt and list the six items as present.
2. Ask who measures joules.
3. Ask which files count as “done.”
4. Only then consider writing a quote document.

No prices, customers, or SLAs are added by this page.
