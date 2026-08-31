# NEXUS OMEGA Repository Order Policy

```text
OBJECT = NEXUS_OMEGA_REPOSITORY_ORDER_POLICY_V1
STATE = ACTIVE
TRIGGER = EVERY_REPOSITORY_INTAKE_AND_HANDOFF
CLAIM_CEILING = C1
```

## Fundamental rule

Order is an operational integrity property. Every artifact must have one obvious home, one declared lifecycle state, and one discoverable causal relation to the work that produced it.

## Intake decision

Before any write, answer:

1. Is this universal repository control? → root or `.github/` only if allowlisted.
2. Is this content-addressed scientific evidence? → `objects/` + `index/`.
3. Is this communication/provenance ledger material? → `communication/`.
4. Is this stable documentation? → `docs/`.
5. Is this a machine contract? → `schema/`.
6. Is this executable repository tooling? → `scripts/`.
7. Is this an automated test? → `tests/`.
8. Is this a validation fixture/binding/status artifact? → `validation/`.
9. Is this an example? → `examples/`.
10. Is this active/pre-integration research? → `research/<phase>/<agent-or-topic>/`.
11. Is this retired, non-path-bound historical material? → `archive/`.

## Root prohibition

Do not add loose agent returns, ZIPs, patches, receipts, experimental outputs, research notes, temporary logs, or one-off JSON files to repository root.

## Symbiotic phase rule

When a research result becomes implementation-grade, its phase/domain must be represented consistently across the lifecycle layers it actually uses:

```text
docs/<phase>/
schema/<phase>/
scripts/<phase>/
tests/<phase>/
validation/<phase>/
examples/<phase>/
```

Research source/returns remain under `research/<phase>/...` and are not silently reclassified as implementation.

## Path-bound history

Paths named by immutable bindings, manifests, receipts, or historical validation artifacts are scientific provenance. They are not moved for cosmetic reasons. A relocation requires a new migration object that preserves old identity, declares new identity, updates references, and is independently validated where material.

## AXIOM / Cursor trigger

AXIOM and Cursor/PRAXIS permanently check repository order when:

- creating a new order;
- receiving an agent return;
- preparing a patch;
- preparing a commit/PR;
- ingesting a new research package;
- closing a phase.

If routing is wrong but evidence identity is unaffected, correct routing and continue. If routing changes a bound path or source identity, treat it as a material migration.

## Validation

Run:

```bash
python scripts/validate_repository_structure.py --root .
python -m unittest tests.test_repository_structure
```

A structure change is incomplete until both the human-readable and machine-readable structure contracts agree.
