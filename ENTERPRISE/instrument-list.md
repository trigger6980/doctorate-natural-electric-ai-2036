# Instrument list (no prices)

This page lists when a named lab plan can name **which instruments** will take the still-open energy-honesty rows. It is not an equipment catalog, not a calibration certificate, and not a claim that any meter is currently booked.

Companions: [`order-and-contract.md`](order-and-contract.md), [`named-lab-plan.md`](named-lab-plan.md), [`measurement-hold.md`](measurement-hold.md), [`scope-assumptions.md`](scope-assumptions.md), [`inquiry-completeness.md`](inquiry-completeness.md), [`quote-draft-outline.md`](quote-draft-outline.md).

## When this page may be used

After a [`named-lab-plan.md`](named-lab-plan.md) note exists (who measures is named) and at least one party can name the **instrument class** for a row.

An instrument list is a *scope-honesty object*: it records meter class, which rows, and that results stay unlabeled until they exist. It does not invent joules, serial numbers, or calibration dates.

Until an instrument class exists, stay on the named-lab-plan page. If who-measures is still unknown, stay on [`measurement-hold.md`](measurement-hold.md). If the sender only needed a public card, use [`handoff-to-public-tree.md`](handoff-to-public-tree.md).

An instrument list is **not** a packet, **not** a quote price, and **not** a field certificate.

## What a list note must name

| Field | Rule |
| --- | --- |
| Inquiry reference | Off-repo label or GitHub issue number only; do not invent a public case id |
| Decision | `instrument-list` / `undecided` |
| Who measures | Copied from the named-lab-plan note — do not invent a new lab |
| Instrument class | `dmm` / `scope` / `current-shunt` / `temp-logger` / `other` — a real make/model only if the sender supplied it |
| Rows covered | Exact scope-assumption or energy-honesty row ids |
| Calibration claim | None unless the sender supplied a certificate id; do not invent one |
| Commercial figure | None. A list does not include a price |

## Allowed list classes

- The named lab plan exists and the buyer named a DMM or logger they already own.
- Joint test will use a class of instrument later; no serial number is invented here.
- Operator AI integration stays out of the quote until listed instruments produce numbers.
- Models 19–27 remain interface cards until listed instruments replace placeholder joules.

## Forbidden classes (on this page and in cover letters)

- Using a list to publish simulator placeholders as field data.
- Inventing a make, model, serial, accreditation, or “N business days.”
- Attaching a placeholder price to a list.
- Claiming Models 19–27 became certified because a list named a DMM.
- Treating a list as if a packet, change order, or closeout already exists.
- Treating host stubs (`host_voltage_reader`, `feed_via_reader`, `first_boot`, `duty_to_policy.fixture_log`, sandbox composition demos, `energy_observer`, `claim_gate`) as substitutes for a named-lab + instrument-class + measurement-method plan. Those stubs carry `is_field_measurement=False` / `reader_is_field_measurement=False` and must stay off any quote that implies measured joules or calibrated C. The shared `feed_via_reader` path and its three host call sites are never instrument-class evidence; `claim_gate` refuses field_generation / quote_evidence / result_record with the token `observer_not_evidence`.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Copy the who-measures class from the named-lab-plan note.
2. Record only the instrument class the sender actually named.
3. Keep those rows `to-be-measured` on the quote until results exist.
4. If results later arrive, re-enter [`quote-draft-outline.md`](quote-draft-outline.md) and label the source. If no instrument class exists, return to [`named-lab-plan.md`](named-lab-plan.md).

No prices, customers, or SLAs are added by this page.
