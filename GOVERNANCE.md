# Governance

## Evidence before agreement

Agent agreement, model identity, fluent language, signatures, hashes, and popularity are not evidence of semantic correctness. Claims must remain within their manifest scope and claim ceiling.

## Roles

- **Operator:** binds repository mutation, licenses, public release, and any later promotion.
- **Publisher:** publishes only within operator authority and after required deterministic gates.
- **Validator:** independently verifies assets and manifests; it cannot promote.
- **External agent:** consumes retrievable bytes and returns bounded research or validation evidence.

## Append-only correction

Published assets are never silently replaced. A correction receives a new object/version and a `supersedes` reference. The old record remains discoverable.

## Repository Order Governance

`REPOSITORY_ORDER_LAW_V1` is a permanent repository invariant.

- Root paths are allowlisted.
- Every artifact class has a canonical owning directory.
- Active research is isolated under `research/<phase>/<agent-or-topic>/` until integration is separately governed.
- Stable phase work uses mirrored domain paths across documentation, schemas, tooling, tests, validation, and examples.
- Content-addressed evidence and communication ledgers remain separate failure/provenance domains.
- Historical path-bound evidence is not moved solely for cosmetic normalization.
- Any structural change must update `README.md`, `docs/architecture/REPOSITORY_STRUCTURE.json`, and pass the structure validator in the same change.
- AXIOM and Cursor/PRAXIS enforce this rule at intake and handoff boundaries.

Order enforcement is risk-adaptive: routine placement errors are corrected while unrelated research continues; mutations that would invalidate evidence bindings require an explicit migration receipt and revalidation.

## Required public state

An object may be called `EXTERNALLY_ANCHORED_C1` only after its required external-anchor conditions are actually satisfied by the governing profile. Hashes or platform controls alone cannot establish scientific validity.

## Prohibited implications

```text
PUBLICLY_ACCESSIBLE => TRUE                 = PROHIBITED
SIGNED_OR_ATTESTED => SCIENTIFICALLY_VALID = PROHIBITED
TWO_WITNESSES => CLAIM_PROMOTION           = PROHIBITED
WEBHOOK_RECEIVED => EXECUTION_AUTHORIZED    = PROHIBITED
ORDERED_PATH => SCIENTIFICALLY_VALID        = PROHIBITED
```
