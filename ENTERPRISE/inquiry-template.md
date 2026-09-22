# Enterprise inquiry template

Copy this into a GitHub issue titled `enterprise-inquiry: <model ids>`.

This template does not create a contract, a price, or a service-level promise. It exists so the maintainer can tell identical-copy work from custom work without guessing energy claims.

## Header
- Date (ISO):
- Contact name / org:
- Preferred contact method and timezone:
- Confidentiality needed? (yes/no + one sentence):

## Models
- Model number(s):
- Identical copy or custom variant:
- If custom: what must change (energy budget, sensors, security, scale)?

## Deployment
- Context (lab / field node / plant floor / other):
- Approximate node count (order of magnitude):
- Air-gapped delivery required? (yes/no):
- Operator AI task-graph in scope? (yes/no):

## Energy honesty
Mark each line **agreed** / **to-be-measured** / **out of scope**. Do not leave them blank.

- Public host tests are not field certification:
- Simulator joule numbers are placeholders until measured:
- Hardware drivers / weights / indexes are not in the public tree unless a card says they are:
- Model 11 public stub is a local pool partitioner, not a mesh market:

Also complete `ENTERPRISE/scope-assumptions.md` and paste or attach the marked table.

## Deliverable shape requested
Pick one tier as a *conversation starter* (not a checkout SKU):

- [ ] Research replica
- [ ] Field customization
- [ ] Operator integration
- [ ] Sovereign / air-gapped

What files do you think you need (cards, tests, BOM notes, private pack)? List them in plain language.

## What we will not invent
Do not ask this inquiry to include fake customers, unpublished prices, or certified MTBF. Those are out of scope until they exist.

## Maintainer next step
Incomplete checklists get questions, not quotes.
