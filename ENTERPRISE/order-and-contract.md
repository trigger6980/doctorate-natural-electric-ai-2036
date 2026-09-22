# Enterprise Order & Contract Page

**Identical / Custom Architectural Models for Enterprise Use**

This page describes how organizations may request identical copies or customized variants of the architectural models catalogued in this repository for internal, commercial, or production use under formal contract.

Mission alignment: Natural Electric systems and Future AI work in this portfolio is aimed at human well-being — reliable off-grid intelligence, honest energy accounting, and operator tooling that remains inspectable. Commercial engagements are expected to keep that orientation: no fabricated performance claims, no hidden energy costs, and no deployment that the buyer cannot audit. Allowed vs forbidden cover-letter claims are listed in [`well-being-alignment.md`](well-being-alignment.md).

Companion pages: [Scope assumptions for a quote](scope-assumptions.md) — the facts a quote must label true or false. [Inquiry template](inquiry-template.md). [Inquiry completeness gate](inquiry-completeness.md). [Quote draft outline](quote-draft-outline.md) — sections a written quote should contain after the gate. [Inquiry response template](inquiry-response-template.md) — what the maintainer pastes back. [Post-quote packet checklist](post-quote-packet.md) — files after written acceptance. [Change order after packet](change-order.md) — how scope changes are recorded. [Engagement closeout](engagement-closeout.md) — how an engagement is closed after packet and change orders. [Records retention after closeout](records-retention.md) — keep vs discard after the closeout note. [Correction notice after retention](correction-notice.md) — factual errors after the retention note. [Engagement FAQ (process only)](engagement-faq.md). [Licensing boundary](licensing-boundary.md) — what public licenses cover versus what a contract may sell. [Well-being alignment](well-being-alignment.md) — what commercial language may repeat.

## What Is Offered
- Access to any of the 50 architectural models (or future additions) in the Genetic / Architectural Model Database.
- Option for **identical** reproduction of a published model (same architecture, quantization, and reference implementation where available).
- Option for **customized** variants (different energy targets, sensor suites, security requirements, or scale).
- Supporting documentation, BOM guidance, and integration notes with the Operator AI Machinery.

## Public tree vs contracted delivery (honest split)

| You can do this from the public tree | This still requires a contract |
| --- | --- |
| Read every model card and interface table | Receive trained weights, a private index, a local LLM runtime pack, or a board-specific measurement pack |
| Run host tests and the host sandbox (scheduler, voltage helper, task-graph, policy gate, listen inventory, energy broker, brokered executor, Gen03 control stub) | Claim those tests or sandbox logs as certified field performance |
| Fork and study under the public licenses | Ship a product that treats a catalog model as a commercial deliverable |
| Open an `enterprise-inquiry` issue | Receive a written quote or private artifacts |

Interface-specified cards (currently 02–21) are design contracts, not finished binaries. Model 11’s host allocator is a local partitioner, not a licensed energy market or mesh stack. Model 12’s checkpoint is host JSON, not flash. Model 13 has no coil driver and no tesla-to-joule calibration. Model 14 has no piezo/TENG driver and no joule-per-cycle calibration. Model 15 has no photodiode driver and no lux-to-joule calibration. Model 16 has no TPM binding and no measured hash energy. Model 17 has no on-device schema compiler and no measured parse energy. Model 18 has no radio driver and no measured hop energy. Model 19 has no survival-curve fit and no energy-neutral certificate. Model 20 has no trained decision tree and no NILM certificate. Model 21 has no trained random forest and no control certificate.

## Inquiry process
1. Review the public catalog: `MODELS/genetic-architectural-database/`.
2. Identify the model number(s) of interest and any customization needs.
3. Open a GitHub issue titled `enterprise-inquiry: <model ids>` **or** contact the maintainer (kalidd komoddo / trigger6980) using the email on the GitHub profile. Include the checklist below **and** the scope-assumptions table.
4. The maintainer replies with questions and a draft statement of work. Nothing is owed until a written contract is signed. The paste-back text lives in [`inquiry-response-template.md`](inquiry-response-template.md).
5. Upon agreement and execution of the contract, the requested artifacts are delivered. The packet shape is listed in [`post-quote-packet.md`](post-quote-packet.md). Later scope changes follow [`change-order.md`](change-order.md). Closeout follows [`engagement-closeout.md`](engagement-closeout.md). Keep vs discard after closeout follows [`records-retention.md`](records-retention.md). Factual errors after retention follow [`correction-notice.md`](correction-notice.md).

Use [`inquiry-template.md`](inquiry-template.md) as the paste-in form. An inquiry is complete enough to discuss only when the six items in [`inquiry-completeness.md`](inquiry-completeness.md) are present. After that gate, a written quote should follow [`quote-draft-outline.md`](quote-draft-outline.md). After written acceptance, the packet follows [`post-quote-packet.md`](post-quote-packet.md). After a packet exists, changes follow [`change-order.md`](change-order.md). After packet and change orders settle, closeout follows [`engagement-closeout.md`](engagement-closeout.md). After closeout, records follow [`records-retention.md`](records-retention.md). After retention, factual corrections follow [`correction-notice.md`](correction-notice.md). Process questions that are not model-specific live in [`engagement-faq.md`](engagement-faq.md). License-object definitions live in [`licensing-boundary.md`](licensing-boundary.md). Cover-letter claim limits live in [`well-being-alignment.md`](well-being-alignment.md).

### Inquiry checklist (paste into the issue)
- Model number(s):
- Identical copy or custom variant:
- Deployment context (lab, field node, plant floor, etc.):
- Approximate node count or scale (order-of-magnitude is enough):
- Energy / off-grid constraints:
- Preferred contact method and timezone:
- Any confidentiality requirement:
- Scope-assumptions table (see `ENTERPRISE/scope-assumptions.md`): each row marked agreed / to-be-measured / out of scope

## What happens after an inquiry (honest sequence)
There is no ticket SLA and no automated intake bot. The sequence below is the intended human process, not a measured service metric.

1. **Acknowledge** that the issue or email was received and that the checklist is complete enough to discuss — or list the missing fields. Completeness is defined in [`inquiry-completeness.md`](inquiry-completeness.md). Use [`inquiry-response-template.md`](inquiry-response-template.md).
2. **Clarify scope** against the public model cards (identical vs custom, Operator AI integration, air-gap delivery).
3. **State assumptions** about energy budgets: simulator placeholders vs numbers the buyer will measure. Use the scope-assumptions table; do not skip it.
4. **Write a quote** only after those assumptions are explicit. Follow [`quote-draft-outline.md`](quote-draft-outline.md). The quote is a document, not a checkout button.
5. **Contract then delivery.** Work starts after written agreement. Public-tree files stay public; private deliverables stay private. Packet contents: [`post-quote-packet.md`](post-quote-packet.md).
6. **Change after packet.** New files or moved energy rows follow [`change-order.md`](change-order.md). Work on the change starts only after written acceptance of that change.
7. **Closeout.** After packet delivery and settled change orders, record the final file list and still-open measurement rows with [`engagement-closeout.md`](engagement-closeout.md).
8. **Records after closeout.** Keep vs discard private drafts with [`records-retention.md`](records-retention.md). Public cards stay public.
9. **Correction after retention.** Errors in already-named files follow [`correction-notice.md`](correction-notice.md). New scope still needs a change order or a new inquiry.

If an inquiry is incomplete, the only next step is questions — not a placeholder price.

## How a quote is formed (no published prices)
There is no storefront and no rate card in this repository. A written quote, when one is issued, is assembled from the inquiry — not from a hidden price list.

Typical inputs to a quote (all optional until the buyer provides them):
- Which model numbers, and whether the request is identical or custom.
- Whether Operator AI task-graph integration is in scope.
- Whether delivery must be air-gapped (sovereign tier).
- Whether the buyer needs help taking hardware measurements (the public cards mark simulator numbers as unmeasured).
- Which rows of the scope-assumptions table are in-scope measurements vs accepted unknowns.

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

Licenses for commercial production use are negotiated. The public tree stays MIT (code) and CC-BY-4.0 (docs) unless a file says otherwise. See [`licensing-boundary.md`](licensing-boundary.md) for objects that are not implied by a model number.

## Value propositions (truthful)
- Energy-first control: policies that refuse work when joules are insufficient.
- Inspectable operators: task graphs and checkpoints you can read, not a black box.
- Shared research surface: enterprise variants stay compatible with the public catalog where possible.
- Human-well-being framing: off-grid and low-power intelligence for places the grid does not reliably reach.

What is **not** claimed: production SLAs, certified safety ratings, measured field MTBF, or existing enterprise customer logos. See [`well-being-alignment.md`](well-being-alignment.md).

## FAQ
**Is the public repo free to study?** Yes, under the stated licenses, for research and non-commercial exploration.

**Can I ship a product using these models without a contract?** Commercial / production use of identical or derivative models is intended to occur under explicit contract. Open an `enterprise-inquiry` issue before you ship.

**Do you have an automated checkout?** No. Engagements are manual so scope and energy assumptions stay explicit.

**Will you invent case studies or metrics to close a deal?** No. Measured numbers appear only after they are measured.

**How are custom models named?** They keep the public model number as ancestry (e.g. `01-custom-<org-slug>`) unless the contract requires a private identifier.

**Where do prices appear?** Only in a written quote after an inquiry. This page will not grow a price column until a real, repeatable quote process exists.

**What if I only want the public cards?** Use the repository. An inquiry is for identical/custom *delivery under contract*, not for reading the catalog.

**What if my inquiry skips the assumptions table?** Expect questions first. A quote will not be drafted on unlabeled energy claims. See [`inquiry-completeness.md`](inquiry-completeness.md).

**Does an interface-specified card mean the model is ready to license as weights?** No. Cards 02–21 document interfaces. Weights, indexes, local LLM runtimes, mesh radios, flash drivers, coil firmware, tesla fits, piezo/TENG drivers, joule-per-cycle fits, photodiode drivers, lux-to-joule fits, TPM bindings, measured hash joules, on-device schema compilers, measured parse joules, radio drivers, measured hop joules, survival-curve fits, energy-neutral certificates, trained NILM trees, trained forests, and joule measurements are separate scoped work.

**Does Model 11 include a multi-node energy market?** No. The public stub only partitions one local pool. A contracted mesh or market would be custom scope.

**Does Model 13 include a calibrated magnetic harvester?** No. The public card is an observer interface. Coil hardware, isolation, and tesla-to-joule fits are custom scope.

**Does Model 14 include a calibrated vibration or TENG harvester?** No. The public card is an observer interface. Piezo/TENG hardware, machine-safety diagnostics, and joule-per-cycle fits are custom scope.

**Does Model 15 include a calibrated indoor-PV or lux meter?** No. The public card is an observer interface. Photodiode hardware, photometry certification, and lux-to-joule fits are custom scope.

**Does Model 16 include a TPM or certified secure boot?** No. The public card is an integrity-gate interface. TPM binding, fuse programming, and measured hash energy are custom scope.

**Does Model 17 include an on-device policy compiler or STIG/CIS certification?** No. The public card is a config-gate interface. Schema compilers, signed-config services, and measured parse energy are custom scope.

**Does Model 18 include a mesh radio or certified routing stack?** No. The public card is a hop-policy interface. Radio drivers, neighbor discovery, and measured hop energy are custom scope.

**Does Model 19 include an energy-neutral certificate?** No. The public card is a probability-gate interface. Survival-curve fits, harvest-process models, and certified energy-neutral proofs are custom scope.

**Does Model 20 include a trained NILM tree or appliance certificate?** No. The public card is a shallow-tree gate interface. Trained weights, ADC traces, and certified disaggregation are custom scope.

**Does Model 21 include a trained random forest or plant-control certificate?** No. The public card is an ensemble-vote gate interface. Trained weights, actuator traces, and certified control are custom scope.

**Does the host sandbox certify field energy use?** No. `SANDBOX/` runs placeholder joules on a laptop or CI runner. The Gen03 control stub names refuse/run states only. `gen03_decisions.json` is a host log of named scenarios, not a heat-stage certificate.

**What if scope changes after the packet?** Use [`change-order.md`](change-order.md). Do not silently add files or move energy rows.

**When is an engagement closed?** After the packet exists and open change orders are accepted or declined. Use [`engagement-closeout.md`](engagement-closeout.md). Remaining `to-be-measured` rows stay listed; they are not done because a packet shipped.

**What is kept after closeout?** Public cards stay public. Private drafts follow [`records-retention.md`](records-retention.md). This page does not invent a statutory retention period.

**What if a named file is wrong after retention?** Use [`correction-notice.md`](correction-notice.md). Do not treat a typo fix as new scope or as a certificate.

Process-only questions (identical vs custom, complete-inquiry contents, allowed cover-letter claims) are expanded in [`engagement-faq.md`](engagement-faq.md) and [`inquiry-completeness.md`](inquiry-completeness.md). License-object definitions are in [`licensing-boundary.md`](licensing-boundary.md). Mission language limits are in [`well-being-alignment.md`](well-being-alignment.md). Quote section order is in [`quote-draft-outline.md`](quote-draft-outline.md). Maintainer paste-back text is in [`inquiry-response-template.md`](inquiry-response-template.md). Packet contents after acceptance are in [`post-quote-packet.md`](post-quote-packet.md). Scope changes after a packet are in [`change-order.md`](change-order.md). Closeout after settled changes is in [`engagement-closeout.md`](engagement-closeout.md). Keep vs discard after closeout is in [`records-retention.md`](records-retention.md). Factual corrections after retention are in [`correction-notice.md`](correction-notice.md).

## Contact for Enterprise Inquiries
Open a GitHub issue in this repository with the title prefix `enterprise-inquiry` and the checklist above.

You will receive a response with next steps toward a formal contract. Response timing is not published because it has not been operated as a measured service.

---

*This page exists to make legitimate enterprise interest straightforward while protecting the open research character of the public portfolio.*
