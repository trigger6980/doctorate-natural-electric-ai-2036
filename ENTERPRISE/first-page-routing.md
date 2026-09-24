# First-page routing (no prices)

This page tells a first-time enterprise reader **which public page to open first**. It is not an intake bot, not an SLA, and not a claim that a human is standing by.

Companions: [`order-and-contract.md`](order-and-contract.md), [`inquiry-template.md`](inquiry-template.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`engagement-faq.md`](engagement-faq.md), [`handoff-to-public-tree.md`](handoff-to-public-tree.md), [`decline-or-defer.md`](decline-or-defer.md), [`well-being-alignment.md`](well-being-alignment.md), [Model 50 commercial template](../MODELS/genetic-architectural-database/models/50-enterprise-identical-model-template.md).

## Start here

| If you already know… | Open this page next |
| --- | --- |
| You only need what the public catalog already states | [`handoff-to-public-tree.md`](handoff-to-public-tree.md) |
| You want identical or custom work and can name a model number | [`inquiry-template.md`](inquiry-template.md) then [`inquiry-completeness.md`](inquiry-completeness.md) |
| You need the commercial *object* (identical vs custom, no prices) | [Model 50 card](../MODELS/genetic-architectural-database/models/50-enterprise-identical-model-template.md) |
| You need the commercial shape, not a form yet | [`order-and-contract.md`](order-and-contract.md) |
| You need process answers (what a quote is / is not) | [`engagement-faq.md`](engagement-faq.md) |
| You need what public licenses already cover | [`licensing-boundary.md`](licensing-boundary.md) |
| Energy numbers are still unlabeled | [`scope-assumptions.md`](scope-assumptions.md) then [`measurement-hold.md`](measurement-hold.md) |
| You already have a written quote to accept | [`post-quote-packet.md`](post-quote-packet.md) |
| Scope changed after a packet | [`change-order.md`](change-order.md) |
| The work is finished or stopped | [`engagement-closeout.md`](engagement-closeout.md) |
| The inquiry should not be quoted | [`decline-or-defer.md`](decline-or-defer.md) |

## Research gates are not commercial objects

Model 49 (`gas_ok` in `AGENTS/gas_search_gate.py`) is a research refuse/allow gate on a fixture candidate table. Passing that host test does **not** mean a custom architecture is for sale, measured, or certified.

The policy-gated executor may record refuse tokens as `aborted_reason='gas_<reason>'`. The host sandbox may also print `_gas_reason_ok` / `_gas_reason_missing_table` in `SANDBOX/out/summary.json`. Those tokens are **research skip labels**. They are not decline codes, not quote statuses, not `inquiry_ok`, and not evidence that a search farm exists. Commercial language stays on Model 50 and the pages in this folder. Do not send an inquiry to Model 49.

## Host observer samples are not quote evidence

`AGENTS/energy_observer.py` may write `host_placeholder` or `hardware_pending` samples into `SANDBOX/out/energy_observer.json`. Those rows exist so host tests can run. They are not field measurements. Do not attach them to a quote, completeness packet, or result record as proof of harvest or consumption. Use [`measurement-hold.md`](measurement-hold.md) and [`measurement-method.md`](measurement-method.md) when energy numbers matter.

`AGENTS/claim_gate.py` encodes the same rule: `host_log` and `sandbox_demo` may pass; `field_generation`, `quote_evidence`, and `result_record` return `observer_not_evidence`. The inquiry helper uses that same token if `energy_evidence` names the observer file.

## What this page must not do

- Invent a case id, turnaround clock, or price.
- Send the reader to a private CRM that this repository does not operate.
- Treat Model 49 or Model 50 as certified products.
- Promise that filling the inquiry template starts a contract.
- Treat `eim_ok` / `inquiry_ok` / `gas_ok` / `gas_<reason>` as a signed agreement.
- Treat sandbox `_gas_reason_*` fields as a commercial score.
- Treat sandbox observer samples as measured joules or as a deliverable.
- Treat a claim-gate `host_log` pass as a field certificate.

## Maintainer use

When a new message arrives without a model number, point here first. If the public tree already answers, stay on the handoff page. If the six completeness items are present (`ENTERPRISE/inquiry_completeness.py` returns `ok`), then — and only then — consider [`quote-draft-outline.md`](quote-draft-outline.md).

No prices, customers, or SLAs are added by this page.
