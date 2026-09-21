# Enterprise Order & Contract Page

**Identical / Custom Architectural Models for Enterprise Use**

This page describes how organizations may request identical copies or customized variants of the architectural models catalogued in this repository for internal, commercial, or production use under formal contract.

Mission alignment: Natural Electric systems and Future AI work in this portfolio is aimed at human well-being — reliable off-grid intelligence, honest energy accounting, and operator tooling that remains inspectable. Commercial engagements are expected to keep that orientation: no fabricated performance claims, no hidden energy costs, and no deployment that the buyer cannot audit.

## What Is Offered
- Access to any of the 50 architectural models (or future additions) in the Genetic / Architectural Model Database.
- Option for **identical** reproduction of a published model (same architecture, quantization, and reference implementation where available).
- Option for **customized** variants (different energy targets, sensor suites, security requirements, or scale).
- Supporting documentation, BOM guidance, and integration notes with the Operator AI Machinery.

## Inquiry process
1. Review the public catalog: `MODELS/genetic-architectural-database/`.
2. Identify the model number(s) of interest and any customization needs.
3. Open a GitHub issue titled `enterprise-inquiry: <model ids>` **or** contact the maintainer (kalidd komoddo / trigger6980) using the email on the GitHub profile. Include the checklist below.
4. The maintainer replies with questions and a draft statement of work. Nothing is owed until a written contract is signed.
5. Upon agreement and execution of the contract, the requested artifacts are delivered.

### Inquiry checklist (paste into the issue)
- Model number(s):
- Identical copy or custom variant:
- Deployment context (lab, field node, plant floor, etc.):
- Approximate node count or scale (order-of-magnitude is enough):
- Energy / off-grid constraints:
- Preferred contact method and timezone:
- Any confidentiality requirement:

## What happens after an inquiry (honest sequence)
There is no ticket SLA and no automated intake bot. The sequence below is the intended human process, not a measured service metric.

1. **Acknowledge** that the issue or email was received and that the checklist is complete enough to discuss — or list the missing fields.
2. **Clarify scope** against the public model cards (identical vs custom, Operator AI integration, air-gap delivery).
3. **State assumptions** about energy budgets: simulator placeholders vs numbers the buyer will measure.
4. **Write a quote** only after those assumptions are explicit. The quote is a document, not a checkout button.
5. **Contract then delivery.** Work starts after written agreement. Public-tree files stay public; private deliverables stay private.

If an inquiry is incomplete, the only next step is questions — not a placeholder price.

## How a quote is formed (no published prices)
There is no storefront and no rate card in this repository. A written quote, when one is issued, is assembled from the inquiry — not from a hidden price list.

Typical inputs to a quote (all optional until the buyer provides them):
- Which model numbers, and whether the request is identical or custom.
- Whether Operator AI task-graph integration is in scope.
- Whether delivery must be air-gapped (sovereign tier).
- Whether the buyer needs help taking hardware measurements (the public cards mark simulator numbers as unmeasured).

Typical outputs of a quote:
- Scope list tied to model numbers and deliverable files.
- Assumptions about energy budgets (simulator vs measured).
- A single commercial figure or a small set of options — written in the quote, not on this page.
- What remains public vs what is delivered privately.

No quote is generated automatically. No turnaround time is promised here because none has been measured as a service metric.

## Placeholder licensing tiers (not a price list)
These tiers exist so a conversation can start. **No prices are published. No customers or revenue are claimed.** Actual terms are written per engagement.

| Tier | Intent | Typical deliverable shape |
| --- | --- | --- |
| Research replica | Identical architecture for internal evaluation | Public code snapshot + model card + test notes |
| Field customization | Same family, different energy or sensor budget | Custom parameters, BOM notes, integration sketch |
| Operator integration | Models plugged into Operator AI Machinery | Task-graph mapping, energy gates, checkpoint policy |
| Sovereign / air-gapped | Offline delivery and reviewable artifacts only | Media or private repo transfer; no telemetry |

Licenses for commercial production use are negotiated. The public tree stays MIT (code) and CC-BY-4.0 (docs) unless a file says otherwise.

## Value propositions (truthful)
- Energy-first control: policies that refuse work when joules are insufficient.
- Inspectable operators: task graphs and checkpoints you can read, not a black box.
- Shared research surface: enterprise variants stay compatible with the public catalog where possible.
- Human-well-being framing: off-grid and low-power intelligence for places the grid does not reliably reach.

What is **not** claimed: production SLAs, certified safety ratings, measured field MTBF, or existing enterprise customer logos.

## FAQ
**Is the public repo free to study?** Yes, under the stated licenses, for research and non-commercial exploration.

**Can I ship a product using these models without a contract?** Commercial / production use of identical or derivative models is intended to occur under explicit contract. Open an `enterprise-inquiry` issue before you ship.

**Do you have an automated checkout?** No. Engagements are manual so scope and energy assumptions stay explicit.

**Will you invent case studies or metrics to close a deal?** No. Measured numbers appear only after they are measured.

**How are custom models named?** They keep the public model number as ancestry (e.g. `01-custom-<org-slug>`) unless the contract requires a private identifier.

**Where do prices appear?** Only in a written quote after an inquiry. This page will not grow a price column until a real, repeatable quote process exists.

**What if I only want the public cards?** Use the repository. An inquiry is for identical/custom *delivery under contract*, not for reading the catalog.

## Contact for Enterprise Inquiries
Open a GitHub issue in this repository with the title prefix `enterprise-inquiry` and the checklist above.

You will receive a response with next steps toward a formal contract. Response timing is not published because it has not been operated as a measured service.

---

*This page exists to make legitimate enterprise interest straightforward while protecting the open research character of the public portfolio.*
