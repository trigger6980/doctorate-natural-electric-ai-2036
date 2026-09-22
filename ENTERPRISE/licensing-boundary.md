# Licensing boundary (what a contract can and cannot pretend to sell)

This page is for buyers and for the maintainer writing a quote. It does not add prices, customers, SLAs, or case studies.

Companions: [order-and-contract.md](order-and-contract.md), [engagement-faq.md](engagement-faq.md), [scope-assumptions.md](scope-assumptions.md), [inquiry-template.md](inquiry-template.md).

Mission alignment: Natural Electric + Future AI work is for human well-being. A license that hides energy cost, ships an unauditable blob as “the model,” or treats host-simulator logs as field certification is out of mission even if someone would pay for it.

## Public license vs commercial contract

| Layer | What it covers today | What it does not cover |
| --- | --- | --- |
| Public code (MIT unless a file says otherwise) | Study, fork, run host tests and the sandbox | Production shipment of a catalog model as a product |
| Public docs (CC-BY-4.0 unless a file says otherwise) | Citation and reuse of the cards with attribution | Claiming the cards are certified energy ratings |
| Written contract (not in this tree) | Identical snapshot, custom variant, private pack, air-gap media — *after* scope is labeled | Anything the scope-assumptions table still marks false |

If there is no signed writing, there is no commercial license beyond the public files.

## Identical vs custom, restated as a license object

- **Identical** licenses the *published interface and host artifacts as they sit in the tree* (plus packaging the buyer pays for). It does not conjure weights, flash drivers, or joule fits.
- **Custom** licenses a *delta* (energy budget, sensors, security boundary, or scale). Ancestry stays `NN-custom-<slug>` unless the contract requires a private name.
- **Operator integration** is a separate object: task-graph mapping and energy gates. It is not implied by “I licensed model 01.”
- **Sovereign / air-gap** is a *delivery method*, not extra physics. Offline media does not make simulator joules measured.

## Objects that are not for sale until they exist
Do not put these on a quote cover as if they were in the public tree:

- Trained weights, private indexes, local LLM runtime packs
- Board-specific measurement packs presented as already complete
- Mesh radios, energy markets, on-device flash checkpoint firmware
- Coil / TEG / piezo / photodiode drivers and their calibration fits
- Response-time SLAs, safety listings, EMC certificates, customer logos

Those can become scope *after* the inquiry marks them to-be-measured or in-scope. They are not implied by a model number.

## Language a quote may use
Allowed:
- “Interface card NN plus host tests as published on date D.”
- “Custom variant of NN for buyer energy floor X (buyer will measure X).”
- “Air-gap copy of the public tree plus private notes listed in the SOW.”

Not allowed:
- “Certified field joules” when only `SANDBOX/` exists.
- “Includes Model 11 market / Model 13 harvester / Model 14 TENG / Model 15 indoor PV” when those cards are observer interfaces.
- Any sentence that needs a customer name this repository does not have.

## How this page should be used in an inquiry
One line is enough: “We read `ENTERPRISE/licensing-boundary.md` and we are asking for identical / custom / operator / sovereign as defined there.” If the buyer needs an object from the not-for-sale list, name it as new scope — do not hide it inside a model number.
