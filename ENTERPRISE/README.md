# Enterprise & Business

This folder holds the **public commercial process** for organizations that want an identical copy or a custom variant of work in this portfolio.

Nothing in this folder is a checkout cart, a published rate card, or a claim that field measurements already exist. Money figures stay off-repo until a written quote exists after a complete inquiry.

Mission alignment: Natural Electric + Future AI is built for human well-being — energy state is a first-class refuse signal, off-grid sites are first-class contexts, and public cards stay honest about what is measured versus what is still a host stub.

## How to inquire (short path)

1. Read [`order-and-contract.md`](order-and-contract.md) for the process and [`licensing-boundary.md`](licensing-boundary.md) for what a license can and cannot cover.
2. Copy [`inquiry-template.md`](inquiry-template.md) into a GitHub issue titled `enterprise-inquiry: <model ids>`.
3. Mark energy honesty rows and complete [`scope-assumptions.md`](scope-assumptions.md). Incomplete checklists get questions, not quotes.
4. The host helper `inquiry_completeness.py` can stamp whether the six public items are present. A stamp is not a contract.
5. If the request is already answered by a public card, the maintainer may hand off with [`handoff-to-public-tree.md`](handoff-to-public-tree.md) instead of opening a commercial lane.

Payment infrastructure is not finalized. Repositories may stay private until it is. Draft contract and billing pages exist for review only.

## Document index

### Start here

| Document | Purpose |
|----------|---------|
| [order-and-contract.md](order-and-contract.md) | Order process, identical vs custom, what happens after inquiry |
| [inquiry-template.md](inquiry-template.md) | Copy-paste issue template |
| [inquiry-completeness.md](inquiry-completeness.md) | Six-item completeness rules used by the host stamp |
| [inquiry-response-template.md](inquiry-response-template.md) | Maintainer reply shape |
| [engagement-faq.md](engagement-faq.md) | Buyer questions without invented prices |
| [first-page-routing.md](first-page-routing.md) | Which page to open first |
| [well-being-alignment.md](well-being-alignment.md) | Mission constraints on commercial language |

### Licensing and work shape

| Document | Purpose |
|----------|---------|
| [licensing-boundary.md](licensing-boundary.md) | What is licensed vs what stays public research |
| [placeholder-engagement-tiers.md](placeholder-engagement-tiers.md) | Named shapes of work — not SKUs, not prices |
| [scope-assumptions.md](scope-assumptions.md) | Shared assumptions table |
| [allowed-cover-claims.md](allowed-cover-claims.md) | Claims that may appear on a cover sheet |
| [quote-draft-outline.md](quote-draft-outline.md) | Headings for a later quote; commercial figure stays blank on-repo |
| [post-quote-packet.md](post-quote-packet.md) | What follows a written quote if one is issued |

### Contract and money process (drafts)

| Document | Purpose |
|----------|---------|
| [CONTRACT.md](CONTRACT.md) | Draft contract template — not executed |
| [PAYMENT-BILLING.md](PAYMENT-BILLING.md) | Invoicing process and *indicative* framework; no live checkout |
| [change-order.md](change-order.md) | Scope change after an engagement exists |
| [correction-notice.md](correction-notice.md) | How public or private claims get corrected |
| [decline-or-defer.md](decline-or-defer.md) | Honest no / later |
| [engagement-closeout.md](engagement-closeout.md) | End of an engagement |
| [reopen-after-close.md](reopen-after-close.md) | How a closed file may reopen |
| [records-retention.md](records-retention.md) | What is kept and for how long |
| [handoff-to-public-tree.md](handoff-to-public-tree.md) | Send the buyer to public files instead of a quote |

### Measurement honesty

| Document | Purpose |
|----------|---------|
| [measurement-hold.md](measurement-hold.md) | Hold commercial claims until a lab and method exist |
| [measurement-method.md](measurement-method.md) | Method class, not a certificate |
| [named-lab-plan.md](named-lab-plan.md) | Who would measure, when named |
| [instrument-list.md](instrument-list.md) | Instrument class list |
| [result-record.md](result-record.md) | How a later measured result would be labeled |

### Host helpers (not a CRM)

| File | Purpose |
|------|---------|
| [inquiry_completeness.py](inquiry_completeness.py) | Completeness, stamp, lanes, action flags; `publish_price` stays blocked |
| Tests in this folder | Guard the stamp invariants and sealed commercial lane |

## What this folder will not do

- Publish a dollar amount, “starting at” price, or fake case study.
- Treat host sandbox joules as field certification.
- Pretend payment rails or legal review are finished.

Questions: open a GitHub issue with the `enterprise-inquiry` label, or use the contact method written in an active SOW if one exists.
