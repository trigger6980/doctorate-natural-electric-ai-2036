# 50 — Enterprise Identical Model Template

**Domain:** Commercial / Contract  
**Energy Profile:** Configurable (inherits the referenced catalog card; never invents joules)  
**Status:** Catalog + commercial interface (not a product sheet, not a price list, not a certified SKU)  
**Operator role:** Optional host gate that refuses a *quote-draft* when the six inquiry-completeness items are missing. Not a CRM, not an SLA clock, and not proof that a contract exists.

## Description
Models 01–49 describe research interfaces. This card describes the *commercial object* those interfaces may become **after** a written inquiry is complete and a separate quote exists. It is the public template for “identical snapshot of card NN” or “custom variant of card NN.” It does not add weights, flash drivers, or field joules that the referenced card does not already contain.

This card specifies the host-facing commercial interface. There is **no product catalog SKU, no published price, no customer list, and no measured commercial energy rating** in this repository. Numbers below are process targets, not sales results.

Honesty rules:
- A completeness decision is a *document event*, not proof that money changed hands.
- Host evaluation of a fixture inquiry on a laptop is not a signed contract.
- Do not claim a product line, certified SKU, SLA, or “enterprise-ready shipment” from this card.
- Distinct from Model 01: Model 01 gates energy. This card gates *whether a quote draft may start*.
- Distinct from Model 11: Model 11 grants energy to a requester. This card does not grant energy.
- Distinct from Model 33: Model 33 checks an energy contract *inside* a runtime. This card checks an *inquiry packet*.
- Distinct from Model 37: Model 37 attests an image. This card does not attest software.
- Distinct from Model 47 / 48 / 49: those cards sequence agents, slots, or architecture candidates. This card sequences *paperwork*.
- The order page remains [`ENTERPRISE/order-and-contract.md`](../../../ENTERPRISE/order-and-contract.md). This card is not a second storefront.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `model_ids` | input | Public catalog numbers, or explicit `undecided` plus a driving constraint |
| `license_shape` | input | `identical` / `custom` / `undecided` (see licensing-boundary.md) |
| `deploy_context` | input | One sentence: lab / field node / plant floor / air-gap shop |
| `energy_honesty` | input | Per-row marks: `agreed` / `to-be-measured` / `out of scope` |
| `scope_table` | input | Same marks as scope-assumptions.md |
| `deliverable_shape` | input | `research_replica` / `field_custom` / `operator_integration` / `sovereign` |
| `hold_eim` | input | Named placeholder measurement-hold id when energy is `to-be-measured` |
| `eim_id` | input | Ancestry id (`50` or `50-custom-<slug>`). Not a SKU |
| `wellbeing_ok` | input | Optional well-being-alignment check; refuse if the ask hides energy cost |
| `quote_action` | output | `ask` / `draft` / `decline` / `defer` / `unknown` |
| `items_present` | output | Count of the six completeness items that are filled |
| `eim_ok` | output | Boolean: a quote *draft* may be considered (not that a quote is sent) |
| `refuse_reason` | output | `missing_model` / `missing_shape` / `missing_context` / `missing_honesty` / `missing_scope` / `missing_deliverable` / `wellbeing` / `unknown` / `ok` |

Planned entry points:
- `eim_step(inquiry) -> quote_action`
- `eim_ok(inquiry) -> bool`
- Host helper: `ENTERPRISE/inquiry_completeness.py` (`inquiry_ok`) — fixture checklist only

Typical composition:
1. Reader lands on [`first-page-routing.md`](../../../ENTERPRISE/first-page-routing.md).
2. If they only need public files, stop at [`handoff-to-public-tree.md`](../../../ENTERPRISE/handoff-to-public-tree.md).
3. If they want identical/custom work, fill [`inquiry-template.md`](../../../ENTERPRISE/inquiry-template.md).
4. Model 50 `eim_ok()` — refuse unless the six completeness items are present.
5. Only then consider [`quote-draft-outline.md`](../../../ENTERPRISE/quote-draft-outline.md).
6. Energy numbers still unlabeled stay on [`measurement-hold.md`](../../../ENTERPRISE/measurement-hold.md).

Missing any of the six items must refuse with the matching `missing_*` reason. A wellbeing fail must refuse with `wellbeing`. An `unknown` action must not become `draft`.

## Energy budget (example, not measured hardware)
This card does **not** consume field energy. Host checklist cost is laptop CI only.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Host walk of six-item checklist | negligible | File compares on CI, not a sales engine |
| Skip (`eim_ok` false) | 0 J extra | Stay on questions; do not draft |
| Signed contract + packaged media | unknown | Out of this public card |

Safety rules:
- Never treat `eim_ok` as proof that *a contract was signed* — only that the named inquiry packet is internally complete.
- Do not invent prices, case ids, turnaround clocks, or customer names in host logs.
- Do not treat this card as a product sheet, SKU list, or certified commercial energy rating.
- Identical licenses the published interface as it sits in the tree. Custom licenses a labeled delta. Neither conjures missing hardware.

## Key Traits
- Commercial template is a refuse/allow gate for *quote drafts*, not a storefront
- Reuses the six-item completeness list already published under ENTERPRISE/
- Compatible with energy-honesty rows (`agreed` / `to-be-measured` / `out of scope`)
- Mission: Natural Electric + Future AI for human well-being — a packet that hides energy cost fails `wellbeing_ok`

## Implementation Notes
Host checklist lives in `ENTERPRISE/inquiry_completeness.py`. It does not send email, mint case ids, or store buyer data. Keep commercial language inside ENTERPRISE pages. Do not check fake invoices or customer logos into this public card.

## Next measurements (not done)
- None required for the checklist itself.
- Hardware joules remain on the *referenced* model card, not here.
- Optional later: map `quote_action=decline` to the public decline-or-defer page without adding an SLA.
