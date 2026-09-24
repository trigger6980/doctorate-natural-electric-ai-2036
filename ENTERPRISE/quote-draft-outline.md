# Quote draft outline (no prices)

This page is the **shape** of a written quote after an inquiry passes [`inquiry-completeness.md`](inquiry-completeness.md). It is not a rate card, not a checkout form, and not a promise that a quote will be issued.

Companions: [`order-and-contract.md`](order-and-contract.md), [`engagement-faq.md`](engagement-faq.md), [`licensing-boundary.md`](licensing-boundary.md), [`well-being-alignment.md`](well-being-alignment.md).

## When this outline may be used

Only after the six completeness items are present. Until then the next action is questions.

Host helper: `inquiry_completeness.outline_ready(inquiry)` plus the `outline_ready` / `price_allowed` fields on `stamp(inquiry)`. `outline_ready=true` means a maintainer may copy the headings below. `price_allowed` is **always false** on the public host helper. The commercial figure (section 9) is written only in an off-repo quote document.

`copy_headings(inquiry)` is the same permission as a list: when ready it returns the ten section keys; when not ready it returns an empty list. `fill_on_repo["commercial_figure_off_repo"]` stays false in both cases.

`public_fill_keys(inquiry)` is the nine keys a maintainer may actually fill in the public tree. It never contains `commercial_figure_off_repo`. When the outline is not ready it is an empty list.

`off_repo_keys(inquiry)` is the complementary partition: when ready it is exactly `["commercial_figure_off_repo"]`. When not ready it is empty. That list is a reminder of where dollars must not be written in this repository; it is not a price.

`partition_keys(inquiry)` is the joined view: public list, off-repo list, `disjoint` (must stay true), and `covers_outline` (true only when a draft may exist and every heading is assigned to one side). `price_allowed` on that packet is always false. The partition is a filing aid, not a signed quote.

`section_lane(inquiry, key)` answers one heading at a time: `public_fill`, `off_repo`, `not_ready`, or `unknown_section`. `section_lanes(inquiry)` maps all ten known headings. Neither helper publishes a figure. A refused `quote_evidence` intended use keeps every known heading on `not_ready`.

`lane_counts(inquiry)` tallies those known headings. Ready packets report `public_fill=9`, `off_repo=1`, `not_ready=0`. Incomplete or refused packets report `not_ready=10`. `sums_to_known` must stay true. The counts are not a price.

## Sections a written quote should contain

1. **Parties and date** — names as given in the inquiry; no invented company logos.
2. **Model numbers and ancestry** — public catalog ids; custom work keeps `NN-custom-<slug>` unless the buyer requires a private identifier.
3. **Identical vs custom** — copied from the inquiry, not inferred.
4. **Deliverable shape** — research replica / field customization / operator integration / sovereign (air-gap).
5. **In-scope files** — cards, host tests, BOM notes, private pack. Each file listed as public-tree copy or private delivery.
6. **Out of scope** — explicit list. Default out-of-scope objects unless the inquiry marked them in-scope: trained weights, board-specific measurement packs, flash mapping, coil/piezo/photodiode drivers, tesla-to-joule or lux-to-joule fits, listed-appliance certification, Generator 01–03 field COP.
7. **Energy-honesty table** — every row from `scope-assumptions.md` restated as agreed / to-be-measured / out of scope. Host-sandbox joules stay labeled host-sandbox.
8. **Who measures joules** — buyer lab, joint test, or later phase. Blank is not allowed in a quote.
9. **Commercial figure** — one number or a small set of options, written only in the quote document. This repository still has no published price column. Host key: `commercial_figure_off_repo`.
10. **What stays public** — MIT/CC files remain public. Private artifacts stay private.

## Language that must not appear in the outline-as-filled

- Customer logos or case studies this repository does not have.
- SLA or MTBF numbers that have not been measured as a service.
- Claims that `SANDBOX/out/gen03_decisions.json` certifies a heat stage.
- Claims that cards 02–15 are licensed weight files.
- Claims that `stamp().outline_ready`, `stamp().headings_copyable`, `stamp().public_fill_keys`, `stamp().off_repo_keys`, `stamp().partition_disjoint`, `stamp().partition_covers_outline`, `stamp().section_lanes`, or `stamp().lane_counts` is a signed quote or a price.

If a cover letter needs those objects, decline or narrow scope. See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy model numbers and identical/custom from the issue.
2. Copy the energy-honesty marks without upgrading “to-be-measured” into “agreed.”
3. List files that count as done.
4. Only then write a commercial figure off-repo.

No prices, customers, or SLAs are added by this page.
