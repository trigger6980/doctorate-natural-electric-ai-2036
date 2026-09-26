# Named lab plan (no prices)

This page lists when a measurement hold can become a **named measurement plan**. It is not a lab booking system, not a certificate, and not a claim that any lab is currently scheduled.

Companions: [`order-and-contract.md`](order-and-contract.md), [`measurement-hold.md`](measurement-hold.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md), [`inquiry-response-template.md`](inquiry-response-template.md).

## When this page may be used

After an inquiry is complete and a [`measurement-hold.md`](measurement-hold.md) note exists (or would exist), and at least one party can name **who measures** which energy-honesty rows.

A named lab plan is a *scope-honesty object*: it records who measures, which rows, and that results stay unlabeled until they exist. It does not invent joules.

Until a who-measures name exists, stay on the hold page. If the sender only needed a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md). If the work cannot be quoted, use [`decline-or-defer.md`](decline-or-defer.md).

A named lab plan is **not** a packet, **not** a quote price, and **not** a field certificate.

## What a plan note must name

| Field | Rule |
| --- | --- |
| Inquiry reference | Off-repo label or GitHub issue number only; do not invent a public case id |
| Decision | `named-lab-plan` / `undecided` |
| Who measures | `buyer-lab` / `joint-test` / `later-phase` / `other` — a real name or org only if the sender supplied it |
| Rows planned | Exact scope-assumption or energy-honesty row ids |
| Site class | Home-lab / plant-floor / unknown — no invented coordinates |
| Commercial figure | None. A plan does not include a price |

## Allowed plan classes

- The inquiry is complete, rows stay `to-be-measured`, and the buyer named their own lab.
- Both parties agree a joint test will happen later; no date is invented here.
- Operator AI integration stays out of the quote until the named plan produces numbers.
- Models 19–26 remain interface cards until the plan replaces placeholder joules.

## Forbidden classes (on this page and in cover letters)

- Using a plan to publish simulator placeholders as field data.
- Inventing a lab name, address, accreditation, or “N business days.”
- Attaching a placeholder price to a plan.
- Claiming Models 19–26 became certified because a plan listed them.
- Treating a plan as if a packet, change order, or closeout already exists.
- Treating host stubs (`host_voltage_reader`, `feed_via_reader`, `first_boot`, `duty_to_policy.fixture_log`, sandbox composition demos, `energy_observer`, `claim_gate`) as substitutes for a named-lab + instrument-class + measurement-method plan. Those stubs carry `is_field_measurement=False` / `reader_is_field_measurement=False` and must stay off any quote that implies measured joules or calibrated C. The shared `feed_via_reader` path and its three host call sites are never instrument-class evidence; `claim_gate` refuses field_generation / quote_evidence / result_record with the token `observer_not_evidence`.

### claim_gate evaluation order (pointer)

When a host sample is presented for a claim, `AGENTS/claim_gate.refuse_reason` evaluates in fixed order (unit-tested; full wording on [`result-record.md`](result-record.md)): unknown_claim → unknown_source → observer_not_evidence → ok. Empty sample lists are not evidence. This keeps unlabeled or host-only numbers from being promoted into a named-lab plan or later result record.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the held row ids from the measurement-hold note.
2. Record only the who-measures class the sender actually named.
3. Keep those rows `to-be-measured` on the quote until results exist.
4. If results later arrive, re-enter [`quote-draft-outline.md`](quote-draft-outline.md) and label the source. If no who-measures name exists, return to [`measurement-hold.md`](measurement-hold.md).

No prices, customers, or SLAs are added by this page.
