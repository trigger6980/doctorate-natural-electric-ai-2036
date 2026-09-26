# Measurement method (no prices)

This page lists when an instrument list can name **how** a still-open energy-honesty row will be taken. It is not a lab SOP library, not a calibration procedure, and not a claim that any method has been run.

Companions: [`order-and-contract.md`](order-and-contract.md), [`instrument-list.md`](instrument-list.md), [`named-lab-plan.md`](named-lab-plan.md), [`measurement-hold.md`](measurement-hold.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md).

## When this page may be used

After an [`instrument-list.md`](instrument-list.md) note exists (instrument class is named) and at least one party can name the **method class** for a row.

A measurement-method note is a *scope-honesty object*: it records method class, which rows, and that results stay unlabeled until they exist. It does not invent sample rates, dwell times, or “N runs.”

Until a method class exists, stay on the instrument-list page. If the instrument class is still unknown, stay on [`instrument-list.md`](instrument-list.md). If who-measures is still unknown, stay on [`named-lab-plan.md`](named-lab-plan.md) or [`measurement-hold.md`](measurement-hold.md). If the sender only needed a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md).

A measurement-method note is **not** a packet, **not** a quote price, and **not** a field certificate.

## What a method note must name

| Field | Rule |
| --- | --- |
| Inquiry reference | Off-repo label or GitHub issue number only; do not invent a public case id |
| Decision | `measurement-method` / `undecided` |
| Who measures | Copied from the named-lab-plan note — do not invent a new lab |
| Instrument class | Copied from the instrument-list note — do not invent a new meter |
| Method class | `spot` / `logged-interval` / `before-after` / `other` — a real SOP id only if the sender supplied it |
| Rows covered | Exact scope-assumption or energy-honesty row ids |
| Sample-rate claim | None unless the sender supplied one; do not invent Hz or dwell |
| Commercial figure | None. A method note does not include a price |

## Allowed method classes

- The instrument list exists and the buyer named a spot reading they already take.
- Joint test will use a logged interval later; no sample rate is invented here.
- Operator AI integration stays out of the quote until listed methods produce numbers.
- Models 19–28 remain interface cards until listed methods replace placeholder joules.

## Forbidden classes (on this page and in cover letters)

- Using a method note to publish simulator placeholders as field data.
- Inventing a SOP id, sample rate, dwell, run count, or “N business days.”
- Attaching a placeholder price to a method note.
- Claiming Models 19–28 became certified because a note named `spot`.
- Treating a method note as if a packet, change order, or closeout already exists.
- Treating host stubs (`host_voltage_reader`, `feed_via_reader`, `first_boot`, `duty_to_policy.fixture_log`, sandbox composition demos, `energy_observer`, `claim_gate`) as substitutes for a named-lab + instrument-class + measurement-method plan. Those stubs carry `is_field_measurement=False` / `reader_is_field_measurement=False` and must stay off any quote that implies measured joules or calibrated C. The shared `feed_via_reader` path and its three host call sites are never instrument-class evidence; `claim_gate` refuses field_generation / quote_evidence / result_record with the token `observer_not_evidence`.

### claim_gate evaluation order (pointer)

When a host sample is presented for a claim, `AGENTS/claim_gate.refuse_reason` evaluates in fixed order (unit-tested; full wording on [`result-record.md`](result-record.md)): unknown_claim → unknown_source → observer_not_evidence → ok. Empty sample lists are not evidence. This keeps unlabeled or host-only numbers from being promoted into a measurement-method note or later result record.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the who-measures class from the named-lab-plan note.
2. Copy the instrument class from the instrument-list note.
3. Record only the method class the sender actually named.
4. Keep those rows `to-be-measured` on the quote until results exist.
5. If results later arrive, re-enter [`quote-draft-outline.md`](quote-draft-outline.md) and label the source. If no method class exists, return to [`instrument-list.md`](instrument-list.md).

No prices, customers, or SLAs are added by this page.
