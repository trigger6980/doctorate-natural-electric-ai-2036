# Measurement hold (no prices)

This page lists when the honest next step is **wait for a named measurement plan**, not a quote with invented joules. It is not a ticket SLA, not a lab booking system, and not a claim that any inquiry is currently on hold.

Companions: [`order-and-contract.md`](order-and-contract.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`decline-or-defer.md`](decline-or-defer.md), [`handoff-to-public-tree.md`](handoff-to-public-tree.md), [`inquiry-response-template.md`](inquiry-response-template.md).

## When this page may be used

After an inquiry exists and the six completeness items are present, but one or more energy-honesty rows are marked `to-be-measured` **and** neither party has named who measures them.

A measurement hold is a *scope-honesty decision*: a quote that pretends those rows are already known would be false.

Until completeness exists, questions remain the default. A hold is appropriate when the missing object is a measurement plan — not when the sender only needed a public card (that is [`handoff-to-public-tree.md`](handoff-to-public-tree.md)) and not when the work cannot be quoted at all (that is [`decline-or-defer.md`](decline-or-defer.md)).

A hold is **not** a packet, **not** a closeout, and **not** a queue position.

## What a hold note must name

| Field | Rule |
| --- | --- |
| Inquiry reference | Off-repo label or GitHub issue number only; do not invent a public case id |
| Decision | `measurement-hold` / `undecided` |
| Why | `unlabeled-who-measures` / `buyer-lab-pending` / `joint-test-pending` / `later-phase` / `other` |
| Rows held | Exact scope-assumption or energy-honesty row ids |
| Commercial figure | None. A hold does not include a price |

## Allowed hold classes

- The inquiry is complete, but joule / voltage / harvest rows stay `to-be-measured` with no named lab.
- The buyer asked for a certified energy number that the public cards mark as placeholders.
- Operator AI integration is in scope only after a rail measurement exists, and that measurement is not scheduled.
- The sender wants a quote “as if” Models 19–25 were already calibrated.

## Forbidden classes (on this page and in cover letters)

- Using a hold to hide a decline that should follow [`decline-or-defer.md`](decline-or-defer.md).
- Inventing a waitlist, “N business days,” or lab-slot SLA.
- Attaching a placeholder price to a hold.
- Claiming Models 19–25 became certified because a hold note listed them.
- Treating a hold as if a packet or change order already exists.
- Treating host stubs (`host_voltage_reader`, `feed_via_reader`, `first_boot`, `duty_to_policy.fixture_log`, sandbox composition demos, `energy_observer`, `claim_gate`) as substitutes for a named-lab + instrument-class + measurement-method plan. Those stubs carry `is_field_measurement=False` / `reader_is_field_measurement=False` and must stay off any quote that implies measured joules or calibrated C. The shared `feed_via_reader` path and its three host call sites are never instrument-class evidence; `claim_gate` refuses field_generation / quote_evidence / result_record with the token `observer_not_evidence`.

### claim_gate evaluation order (pointer)

When a host sample is presented for a claim, `AGENTS/claim_gate.refuse_reason` evaluates in fixed order (unit-tested; full wording on [`result-record.md`](result-record.md)): unknown_claim → unknown_source → observer_not_evidence → ok. Empty sample lists are not evidence. This keeps unlabeled or host-only numbers from being promoted into a hold or later result record.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Name the `to-be-measured` rows that block an honest quote.
2. Ask who measures: buyer lab, joint test, or later phase. Do not invent a lab.
3. Do not write a quote that fills those rows with simulator placeholders presented as field data.
4. If the sender later supplies a measurement plan, re-enter [`quote-draft-outline.md`](quote-draft-outline.md). If they only needed the public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md).

No prices, customers, or SLAs are added by this page.
