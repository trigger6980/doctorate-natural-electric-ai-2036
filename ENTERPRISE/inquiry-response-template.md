# Maintainer inquiry-response template (no prices)

This page is what the maintainer pastes when an `enterprise-inquiry` issue or email arrives. It is not a quote, not an SLA, and not an intake bot.

Use after reading [`inquiry-completeness.md`](inquiry-completeness.md). If the six items are missing, send only the incomplete branch. If they are present, send the complete branch and then draft against [`quote-draft-outline.md`](quote-draft-outline.md).

Companions: [`order-and-contract.md`](order-and-contract.md), [`engagement-faq.md`](engagement-faq.md), [`well-being-alignment.md`](well-being-alignment.md).

## Incomplete inquiry (questions only)

```
Thank you for the enterprise inquiry.

This repository does not issue a quote until the completeness gate in ENTERPRISE/inquiry-completeness.md is met. Still needed:

- [ ] Model number(s) from the public catalog
- [ ] Identical / custom / undecided
- [ ] Deployment context in one sentence
- [ ] Deliverable-shape checkbox (research replica / field customization / operator integration / sovereign)
- [ ] Energy-honesty marks (agreed / to-be-measured / out of scope)
- [ ] Scope-assumptions table with the same marks

Please paste the missing rows. No commercial figure will be written while those rows are blank.
```

## Complete inquiry (acknowledge, then quote offline)

```
Thank you. The completeness gate looks met enough to discuss.

I am treating this as:
- Models: <ids>
- Identical vs custom: <as written>
- Deliverable shape: <tier>
- Who measures joules: <buyer lab / joint / later phase>

Next step on my side is a written quote following ENTERPRISE/quote-draft-outline.md. That document is not a checkout and is not published as a rate card.

Public-tree files stay public. Anything private will be listed as private in the quote. I will not add customer logos, SLAs, or field certifications that this repository does not have.
```

## Language the maintainer must not add in either reply

- A price, discount, or “typical contract value.”
- A promised response time presented as a measured SLA.
- A claim that cards 02–16 are licensed weight files.
- A claim that `SANDBOX/out/gen03_decisions.json` certifies a heat stage.
- Invented case studies.

If the inquirer asks for those objects first, point at [`well-being-alignment.md`](well-being-alignment.md) and stay on questions.

## Fill order after the complete reply

1. Copy model numbers and identical/custom into the quote outline.
2. Copy energy-honesty marks without upgrading “to-be-measured” into “agreed.”
3. List files that count as done.
4. Only then write a commercial figure *off-repo*.

No prices, customers, or SLAs are added by this page.
