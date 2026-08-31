# NEXUS OMEGA Evidence

Public, content-addressed C1 evidence and verification repository with a persistent AI communication, provenance, validation, and research surface.

## Repository status

This repository records exact bytes, provenance, validation state, caveats, research handoffs, and platform receipts. Hashes, signatures, commits, CI, releases, attestations, agent agreement, and public availability do **not** establish scientific truth.

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
```

## Repository Order Law

`REPOSITORY_ORDER_LAW_V1` is binding for AXIOM, Cursor/PRAXIS, Copilot, external research agents, and future repository work.

1. Every new artifact is classified **before** it is written.
2. The repository root is an allowlisted control surface, never a dump directory.
3. One artifact class has one canonical owning directory.
4. Active research belongs under `research/<phase>/<agent-or-topic>/`.
5. Stable R5 work is mirrored symbiotically across `docs/r5/`, `schema/r5/`, `scripts/r5/`, `tests/r5/`, `validation/r5/`, and `examples/r5/`.
6. Content-addressed evidence remains under `objects/` + `index/`; communication provenance remains under `communication/objects/` + `communication/index/`.
7. Historical path-bound evidence is not relocated merely for aesthetics. A path move requires a migration receipt and all affected bindings/references to remain reproducible.
8. Every structural change updates this README and `docs/architecture/REPOSITORY_STRUCTURE.json` in the same change.
9. Disorder is corrected at intake. A noncritical placement error does not halt unrelated research, but it must not be allowed to become canonical debt.

Detailed policy: `docs/governance/REPOSITORY_ORDER_POLICY.md`.

## Exact live directory contract

The tracked structure for this architecture version is:

```text
/
├── .github/
│   ├── CODEOWNERS
│   ├── copilot-instructions.md
│   └── workflows/
│       ├── validate-a83-framework-hardening.yml
│       ├── validate-anchor.yml
│       ├── validate-repository-structure.yml
│       ├── validate-scientific-communication.yml
│       └── validate-scientific-ledger.yml
├── AGENTS.md
├── CITATION.cff
├── GOVERNANCE.md
├── LICENSE
├── README.md
├── SECURITY.md
├── _config.yml
├── index.md
├── requirements-a83-test.txt                  # immutable path-bound compatibility exception
├── communication/
│   ├── README.md
│   ├── index/v1/
│   │   ├── latest.json
│   │   └── records.jsonl
│   └── objects/sha256/1c/df/
│       └── 1cdfcc74319f6f8500d969e8345ce5b6e1e6298482e03b6c96881cbbbd99dece/
│           └── record.json
├── docs/
│   ├── README.md
│   ├── AI_CONTEXT.md
│   ├── AI_HANDOFF_PROTOCOL.md
│   ├── OPEN_SCIENCE_AGENT_COMMUNICATION_MANIFEST.md
│   ├── SCIENTIFIC_COMMUNICATION_IMPLEMENTATION_PROFILE_V0_1.md
│   ├── agent-protocol.md
│   ├── release-checklist.md
│   ├── architecture/
│   │   ├── REPOSITORY_STRUCTURE.md
│   │   └── REPOSITORY_STRUCTURE.json
│   ├── governance/
│   │   ├── REPOSITORY_ORDER_POLICY.md
│   │   └── REPOSITORY_PATH_RULES.json
│   ├── phase2/                                # immutable path-bound history
│   │   ├── A83_FRAMEWORK_INVENTORY_AND_GAP_REPORT_v1.0.json
│   │   ├── A83_FRAMEWORK_INVENTORY_AND_GAP_REPORT_v1.0.md
│   │   ├── NEXUS_OMEGA_A84_INDEPENDENT_GITHUB_VALIDATION_RETURN_20260831_R0.md
│   │   └── NEXUS_OMEGA_A84_INDEPENDENT_GITHUB_VALIDATION_RETURN_20260831_R0_HANDSHAKE.json
│   └── r5/
│       └── README.md
├── examples/
│   ├── README.md
│   ├── a83/
│   │   └── handoff-envelope-v1.example.json
│   ├── scientific-communication/
│   │   └── communication-receipt-v1.example.json
│   └── r5/
│       └── README.md
├── index/
│   ├── README.md
│   └── v1/
│       ├── latest.json
│       ├── objects.jsonl
│       └── lanes/
│           └── dps_epistemic_sovereignty.json
├── objects/
│   ├── README.md
│   └── sha256/9f/dd/
│       └── 9fdd1dccc9fd76222352eeb21af6b392358f18b7886b25137892c5a1c3a92145/
│           ├── artifact.md
│           └── manifest.json
├── schema/
│   ├── README.md
│   ├── A83_handoff_envelope_v1.schema.json
│   ├── agent-return-v1.schema.json
│   ├── anchor-manifest-v1.schema.json
│   ├── scientific-communication-v1.schema.json
│   └── r5/
│       └── README.md
├── scripts/
│   ├── README.md
│   ├── a83_decision.py
│   ├── a83_sentinel.py
│   ├── append_scientific_record.py
│   ├── reproduce_a83.py
│   ├── validate_a83_handoff.py
│   ├── validate_anchor.py
│   ├── validate_repository.py
│   ├── validate_repository_structure.py
│   ├── validate_scientific_communication.py
│   ├── validate_scientific_ledger.py
│   ├── verify_a83_artifact_binding.py
│   └── r5/
│       └── README.md
├── tests/
│   ├── README.md
│   ├── test_a83_handoff.py
│   ├── test_repository_structure.py
│   ├── test_scientific_communication.py
│   ├── test_scientific_ledger.py
│   ├── test_validate_anchor.py
│   └── r5/
│       └── README.md
├── validation/
│   ├── README.md
│   ├── A83_ARTIFACT_BINDING_v1.0.json
│   ├── A83_FINAL_STATUS_v1.0.json
│   ├── A83_WEAKNESS_AND_OPEN_QUESTIONS_AUDIT_v1.0.json
│   ├── a83-handoff-negative-fixtures-v1.jsonl
│   ├── scientific-communication-negative-fixtures-v1.jsonl
│   └── r5/
│       └── README.md
├── research/
│   ├── README.md
│   └── r5/
│       └── README.md
└── archive/
    └── README.md
```

`docs/phase2/` and `requirements-a83-test.txt` remain in their historical paths because the published A83 artifact binding names those paths explicitly. Their location is therefore a provenance constraint, not unsorted residue.

## Domain ownership

| Path | Canonical responsibility |
|---|---|
| `.github/` | GitHub-native governance, ownership, CI |
| `objects/` | content-addressed scientific evidence assets/manifests |
| `index/` | discovery index for scientific evidence objects |
| `communication/` | content-addressed communication/provenance ledger |
| `docs/` | stable human-readable protocols, architecture, governance, history |
| `schema/` | machine-readable contracts |
| `scripts/` | executable repository tooling and validators |
| `tests/` | executable automated tests |
| `validation/` | fixtures, bindings, machine validation receipts/status |
| `examples/` | non-authoritative examples |
| `research/` | active, not-yet-integrated research by phase/agent/topic |
| `archive/` | retired non-path-bound material and migration records |

## Symbiotic R5 lane

R5 uses the same slug across scientific lifecycle layers:

```text
docs/r5/         theory, protocol and architecture
schema/r5/       contracts
scripts/r5/      reference implementations and validators
tests/r5/        executable tests
validation/r5/   fixtures, bindings and validation state
examples/r5/     minimal examples
research/r5/     external and exploratory research inputs/returns
```

A candidate is not considered structurally integrated if only one layer exists while required companion layers are missing.

## Agent entry points

Read in this order:

1. `AGENTS.md`
2. `GOVERNANCE.md`
3. `docs/AI_CONTEXT.md`
4. `docs/agent-protocol.md`
5. `docs/architecture/REPOSITORY_STRUCTURE.md`
6. `index/v1/latest.json` when current scientific evidence state is relevant

## Validation

Repository order is mechanically checked with:

```bash
python scripts/validate_repository_structure.py --root .
python -m unittest tests.test_repository_structure
```

The dedicated GitHub Actions job is named `validate-repository-structure` to avoid further check-name ambiguity.

## Licensing

Original documentation is offered under CC BY 4.0. Original validation code is offered under Apache-2.0. Third-party materials are excluded unless their licensing is explicitly recorded.

## Security

See `SECURITY.md`. Do not publish credentials, personal data, medical data, private conversations, non-public repository material, or unredacted security logs.
