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

`stamp(inquiry)` returns a host label packet (`items_present`, `refuse_reason`, `quote_action`, `intended_use`, `energy_evidence`, `inquiry_ok`, `outline_ready`, `price_allowed`, `outline_sections`, `headings_copyable`, `headings`, `fill_on_repo`, `public_fill_keys`, `off_repo_keys`, `partition_disjoint`, `partition_covers_outline`, `section_lanes`, `lane_counts`, `next_action`, `next_action_copy_headings`, `action_flags`, `action_exactly_one`). It is a checklist snapshot, not a signed quote and not energy evidence. The sandbox writes the same packet to `SANDBOX/out/inquiry_stamp.json`.

`outline_ready(inquiry)` is true only when `quote_action` is `draft`. `price_allowed` is always `false` on this host helper. Section names match [`quote-draft-outline.md`](quote-draft-outline.md); they are headings, not filled commercial terms.

`copy_headings(inquiry)` returns those titles only when the outline is ready. `headings` is an empty list when `quote_action` is not `draft`. `fill_on_repo["commercial_figure_off_repo"]` is always `false`. Copying headings is not permission to publish a rate card.

`public_fill_keys(inquiry)` is the filtered list of keys where `fill_on_repo[key]` is true. When the outline is ready that list has nine keys and never includes `commercial_figure_off_repo`. When the outline is not ready the list is empty.

`off_repo_keys(inquiry)` is the complementary list: when the outline is ready it is exactly `["commercial_figure_off_repo"]`. When the outline is not ready it is empty. Presence of that key is not a price and is not permission to invent dollars in this repository.

`partition_keys(inquiry)` joins those two lists and records `disjoint` plus `covers_outline`. When a draft is allowed the union of the lists equals the ten outline headings and the lists share no key. When a draft is not allowed both lists are empty, `disjoint` stays true, and `covers_outline` is false. Neither flag is a commercial figure.

`section_lane(inquiry, key)` is the per-heading view of the same partition. Known keys return `public_fill` or `off_repo` only when the outline is ready; otherwise they return `not_ready`. A key that is not one of the ten headings returns `unknown_section`. `section_lanes(inquiry)` is the map of all ten known keys. `price_allowed` stays false on every lane packet.

`lane_counts(inquiry)` tallies those known headings: when ready, `public_fill=9`, `off_repo=1`, `not_ready=0`; when not ready, `not_ready=10`. `sums_to_known` must stay true. The tally is a filing aid, not a price column.

`next_maintainer_action(inquiry)` is one filing verb: `decline` when well-being fails, `ask` when an item is missing or an observer / refused-use token is present, `copy_headings` when the six items passed. There is no `publish_price` verb. Stamp fields: `next_action`, `next_action_copy_headings`. `price_allowed` stays false.

`action_flags(inquiry)` is the mutex view of that verb: exactly one of `decline`, `ask`, or `copy_headings` is true, and `publish_price` is always false. Stamp fields: `action_flags`, `action_exactly_one`. `exactly_one` must stay true. The flags are not a checkout form.

## Incomplete patterns that stay incomplete

- “Need the 50 models” with no identical/custom split.
- A request for measured COP, kWh, or crop yield taken from this public tree.
- A request to hide an energy cost or to treat host-sandbox joules as certified field performance.
- Attaching `SANDBOX/out/energy_observer.json` as proof of harvest or consumption.
- Treating a host `claim_scan` of `host_log: ok` as permission to quote joules.
- Treating `inquiry_stamp.quote_action = draft` as a price or SLA.
- Treating `outline_ready = true` or `headings_copyable = true` as permission to publish a rate card in this repository.
- Treating `public_fill_keys` as permission to write dollars into a public file.
- Treating `off_repo_keys` as a published price column.
- Treating `partition_disjoint` or `partition_covers_outline` as a signed quote.
- Treating `section_lane(..., "commercial_figure_off_repo").lane = off_repo` as a published dollar amount.
- Treating `lane_counts.off_repo = 1` as a published dollar amount.
- Treating `next_action = copy_headings` as permission to publish a rate card.
- Treating `action_flags.copy_headings = true` or `action_exactly_one = true` as a published dollar amount.
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
- That `fill_on_repo` or `public_fill_keys` authorizes writing dollars into a public file.
- That `off_repo_keys` is a rate card.
- That `partition_keys` is a checkout form.
- That `section_lane` or `section_lanes` is a checkout form.
- That `lane_counts` is a checkout form.
- That `next_maintainer_action` is a checkout form.
- That `action_flags` or `action_exactly_one` is a checkout form.

## Maintainer reply shape (when complete)

1. Acknowledge receipt and list the six items as present.
2. Ask who measures joules.
3. Ask which files count as “done.”
4. Only then consider writing a quote document off-repo.

No prices, customers, or SLAs are added by this page.
