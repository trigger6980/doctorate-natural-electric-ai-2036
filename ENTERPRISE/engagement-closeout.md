# Engagement closeout after change orders (no prices)

This page lists how an engagement is **closed** after a packet from [`post-quote-packet.md`](post-quote-packet.md) exists and any scope changes from [`change-order.md`](change-order.md) are either accepted or explicitly declined. It is not a warranty, not an SLA, and not a claim that any engagement has already closed.

Companions: [`order-and-contract.md`](order-and-contract.md), [`post-quote-packet.md`](post-quote-packet.md), [`change-order.md`](change-order.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`licensing-boundary.md`](licensing-boundary.md), [`well-being-alignment.md`](well-being-alignment.md).

## When this page may be used

Only after:
1. The six completeness items were present.
2. A quote following the ten-section outline existed off-repo.
3. The buyer accepted that quote in writing.
4. A packet cover sheet exists (public vs private files named).
5. Open change orders are either accepted in writing or marked declined on the off-repo change document.

Until those five are true, the next action is still questions, a quote, a packet, or a change order — not closeout.

## What a closeout note must name

| Field | Rule |
| --- | --- |
| Models delivered | Copied from the last accepted quote or change order |
| Identical vs custom | Final ancestry ids, including any `NN-custom-<slug>` |
| File list | Same public vs private marks as the last packet cover sheet |
| Energy-honesty rows | Final agreed / to-be-measured / out of scope — no silent upgrades |
| Open measurements | Rows still `to-be-measured` stay listed; they are not “done” |
| Transfer method | Air-gap or private repo, copied from the last accepted document |
| Commercial figure | Written only on the off-repo closeout note — never on this page |

## Allowed closeout classes

- Packet delivered; no further files planned under this quote.
- Packet delivered; named measurement rows remain buyer-lab work.
- Engagement paused; packet frozen; a later inquiry must restart the completeness gate.
- Engagement declined after packet draft; no private files retained beyond what the off-repo note lists.

## Forbidden closeout classes (on this page and in cover letters)

- Declaring host sandbox logs or `gen03_decisions.json` as field certificates.
- Relabeling cards 02–19 as licensed weight files or energy-neutral proofs.
- Publishing prices, SLAs, testimonials, or customer logos in the public tree.
- Treating remaining `to-be-measured` rows as completed because the packet shipped.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the last accepted packet cover sheet.
2. List open measurement rows without converting them to agreed.
3. Confirm no unaccepted change order is still pending.
4. Write the off-repo closeout note. Do not invent a public “case study” from it.

No prices, customers, or SLAs are added by this page.
