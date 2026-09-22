# Correction notice after retention (no prices)

This page lists how a **factual correction** is recorded after a retention note from [`records-retention.md`](records-retention.md) exists. It is not a warranty claim process, not a ticket SLA, and not a claim that any correction archive already exists.

Companions: [`order-and-contract.md`](order-and-contract.md), [`records-retention.md`](records-retention.md), [`engagement-closeout.md`](engagement-closeout.md), [`change-order.md`](change-order.md), [`well-being-alignment.md`](well-being-alignment.md).

## When this page may be used

Only after:
1. The six completeness items were present.
2. A quote following the ten-section outline existed off-repo.
3. The buyer accepted that quote in writing.
4. A packet cover sheet exists.
5. Open change orders were accepted or declined.
6. A closeout note exists.
7. A retention note exists that names keep vs discard.

Until those seven are true, the next action is still questions, a quote, a packet, a change order, closeout, or retention — not a correction notice.

A correction notice is for *errors in already-named files* (wrong model ancestry, mis-copied energy-honesty mark, missing file on the closeout list). It is **not** a way to add new deliverables. New files or moved energy rows still require [`change-order.md`](change-order.md) and a new completeness pass if the original engagement is closed.

## What a correction notice must name

| Field | Rule |
| --- | --- |
| File being corrected | Must already appear on the closeout file list |
| Error class | `ancestry` / `honesty-mark` / `file-list` / `typo` |
| Old text | Quoted; do not paraphrase |
| New text | Quoted; no silent energy upgrade |
| Public-tree effect | Usually none; public cards stay as committed |
| Commercial figure | Written only on the off-repo notice — never on this page |

## Allowed correction classes

- Fix a mistyped model ancestry (`20-custom-<slug>` written as `21-custom-<slug>`).
- Restore an energy-honesty row that was copied as `agreed` when closeout still said `to-be-measured`.
- Add a file that the closeout list named but the private packet snapshot omitted.
- Correct a typo that does not change scope.

## Forbidden correction classes (on this page and in cover letters)

- Adding a new model number or weight file without a change order or a new inquiry.
- Relabeling `to-be-measured` as `agreed` because time passed.
- Publishing buyer names, logos, or prices in the public tree.
- Treating host sandbox logs as corrected field certificates.
- Claiming Model 21 `rf_ok` (or Models 19–20 gates) became certified because a typo was fixed.

See [`well-being-alignment.md`](well-being-alignment.md).

## Maintainer fill order

1. Confirm the retention note exists.
2. Quote the old text and the new text.
3. Confirm the file was already on the closeout list.
4. Write the off-repo correction notice. Do not invent a public errata page from it unless the public tree itself is wrong — in that case use a normal commit, not this form.

No prices, customers, or SLAs are added by this page.
