# Result record (no prices)

This page lists when a measurement-method note can accept **results that already exist**. It is not a results database, not a certificate archive, and not a claim that any energy row has been measured in this repository.

Companions: [`order-and-contract.md`](order-and-contract.md), [`measurement-method.md`](measurement-method.md), [`instrument-list.md`](instrument-list.md), [`named-lab-plan.md`](named-lab-plan.md), [`measurement-hold.md`](measurement-hold.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md).

## When this page may be used

After a [`measurement-method.md`](measurement-method.md) note exists (method class is named) and at least one party can attach a **result label** for a row.

A result record is a *scope-honesty object*: it records source class, units class, and that unlabeled simulator placeholders stay unlabeled. It does not invent joules, sample counts, or “N runs passed.”

Until a result exists, stay on the measurement-method page. If the method class is still unknown, stay on [`measurement-method.md`](measurement-method.md). If the instrument class is still unknown, stay on [`instrument-list.md`](instrument-list.md). If who-measures is still unknown, stay on [`named-lab-plan.md`](named-lab-plan.md) or [`measurement-hold.md`](measurement-hold.md). If the sender only needed a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md).

A result record is **not** a packet, **not** a quote price, and **not** a field certificate.

## What a result record must name

| Field | Rule |
| --- | --- |
| Inquiry reference | Off-repo label or GitHub issue number only; do not invent a public case id |
| Decision | `result-record` / `undecided` |
| Who measures | Copied from the named-lab-plan note — do not invent a new lab |
| Instrument class | Copied from the instrument-list note — do not invent a new meter |
| Method class | Copied from the measurement-method note — do not invent a new SOP |
| Rows covered | Exact scope-assumption or energy-honesty row ids |
| Source class | `sender-supplied` / `joint-lab` / `none` — never `simulator-as-field` |
| Units class | Named unit the sender used, or `unlabeled` |
| Commercial figure | None. A result record does not include a price |

## Allowed result classes

- The method note exists and the buyer attached a labeled reading they already took.
- Joint test later produced a labeled interval; no extra runs are invented here.
- Operator AI integration stays out of the quote until labeled results replace placeholders.
- Models 19–29 remain interface cards until labeled results replace placeholder joules.

## Forbidden classes (on this page and in cover letters)

- Using a result record to publish simulator placeholders as field data.
- Inventing a joule number, sample count, pass rate, or “N business days.”
- Attaching a placeholder price to a result record.
- Claiming Models 19–29 became certified because a note named `sender-supplied`.
- Treating a result record as if a packet, change order, or closeout already exists.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the who-measures class from the named-lab-plan note.
2. Copy the instrument class from the instrument-list note.
3. Copy the method class from the measurement-method note.
4. Record only the source class and units class the sender actually named.
5. Keep unlabeled rows `to-be-measured` on the quote until results exist.
6. If results later arrive labeled, re-enter [`quote-draft-outline.md`](quote-draft-outline.md) and keep the source class visible. If no result exists, return to [`measurement-method.md`](measurement-method.md).

No prices, customers, or SLAs are added by this page.
