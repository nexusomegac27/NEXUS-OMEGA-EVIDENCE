# Governance

## Evidence before agreement

Agent agreement, model identity, fluent language, signatures, hashes, and popularity are not evidence of semantic correctness. Claims must remain within their manifest scope and claim ceiling.

## Roles

- **Operator:** binds repository, licenses, public release, and any later promotion.
- **Publisher:** publishes only after deterministic gates succeed.
- **Validator:** independently verifies assets and manifests; it cannot promote.
- **External agent:** consumes public bytes and returns an independently anchored result.

## Append-only correction

Published assets are never silently replaced. A correction receives a new object/version and a `supersedes` reference. The old record remains discoverable.

## Required public state

An object may be called `EXTERNALLY_ANCHORED_C1` only after:

1. exact public asset bytes and SHA-256 are verified;
2. a GitHub immutable release and release asset verify successfully;
3. at least one independent witness (Zenodo DOI or Software Heritage SWHID) resolves to the same object;
4. privacy, secrets, rights, license, and C1 gates pass.

## Prohibited implications

```text
PUBLICLY_ACCESSIBLE => TRUE                 = PROHIBITED
SIGNED_OR_ATTESTED => SCIENTIFICALLY_VALID = PROHIBITED
TWO_WITNESSES => CLAIM_PROMOTION           = PROHIBITED
WEBHOOK_RECEIVED => EXECUTION_AUTHORIZED    = PROHIBITED
```
