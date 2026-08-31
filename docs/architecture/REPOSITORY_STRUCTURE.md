# NEXUS OMEGA Repository Structure Contract V1

## Purpose

This contract defines the canonical GitHub repository topology and the placement semantics for every artifact class. The structure is designed for scientific reproducibility, provenance preservation, machine validation, independent review, and long-lived multi-agent collaboration.

## Design principles

1. **Root minimalism.** Root is reserved for universal repository controls and historically path-bound compatibility files.
2. **Single ownership.** Each artifact class has one owning directory.
3. **Evidence/provenance separation.** Scientific evidence (`objects` + `index`) and communication provenance (`communication`) remain distinct stores.
4. **Symbiotic lifecycle.** A phase/domain can be traced across documentation → schema → implementation → tests → validation → examples → research.
5. **Immutable history.** A published binding that names a path makes that path part of the reproducibility contract unless an explicit migration is created.
6. **Machine enforcement.** Structural rules are validated by `scripts/validate_repository_structure.py` and CI.
7. **Risk-adaptive order.** Misplacement is corrected promptly, but ordinary routing errors do not freeze unrelated research.

## Canonical top-level domains

| Directory | Responsibility | May contain canonical scientific evidence? |
|---|---|---|
| `.github/` | platform governance, CODEOWNERS, CI | platform receipts only |
| `objects/` | content-addressed scientific evidence assets/manifests | yes |
| `index/` | discovery/index state for `objects/` | yes, provenance/index |
| `communication/` | content-addressed communication/provenance ledger | process/provenance evidence |
| `docs/` | stable documentation, protocol, architecture, governance, history | descriptive only unless separately bound |
| `schema/` | machine contracts | structural |
| `scripts/` | executable tooling/validators | implementation |
| `tests/` | automated tests | validation support |
| `validation/` | fixtures, bindings, status/validation artifacts | validation evidence |
| `examples/` | non-authoritative examples | no |
| `research/` | active/pre-integration research | candidate only |
| `archive/` | retired non-path-bound material and migration records | historical only |

## Symbiotic phase lane

For R5 and later, use the same phase slug across lifecycle domains:

```text
docs/r5/
schema/r5/
scripts/r5/
tests/r5/
validation/r5/
examples/r5/
research/r5/
```

This provides deterministic traceability. A schema points to its validator/tests/fixtures through the same phase namespace rather than scattered filenames.

## Historical compatibility rule

The A83 artifact binding names multiple exact paths, including `docs/phase2/*`, `schema/A83_handoff_envelope_v1.schema.json`, `scripts/a83_*`, `tests/test_a83_handoff.py`, `validation/*A83*`, `examples/a83/*`, `requirements-a83-test.txt`, and the A83 workflow. Those paths remain valid historical compatibility surfaces.

Do not move them only to make the tree prettier. New generations should use the symmetric phase namespaces instead.

## Research intake

Active external-agent or exploratory work goes to:

```text
research/<phase>/<agent-or-topic>/
```

Recommended substructure when the volume warrants it:

```text
research/<phase>/<agent>/
├── README.md
├── orders/
├── returns/
├── receipts/
├── sources/
├── experiments/
└── patches/
```

Research artifacts are not live implementation merely because they are public.

## Structural change procedure

A structural change must update in one change set:

1. `README.md`;
2. `docs/architecture/REPOSITORY_STRUCTURE.md` if semantics change;
3. `docs/architecture/REPOSITORY_STRUCTURE.json`;
4. affected domain README(s);
5. `scripts/validate_repository_structure.py` and tests if rules change;
6. all path references and artifact bindings that are legitimately versioned;
7. an explicit migration note when a historical canonical path changes.

## Trigger

AXIOM and Cursor/PRAXIS treat this contract as a permanent pre-ingest check. Every future agent order involving repository artifacts should preserve the intended target path or explicitly classify the output as external/unintegrated.
