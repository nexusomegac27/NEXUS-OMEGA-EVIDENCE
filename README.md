# NEXUS OMEGA Evidence

Public, content-addressed C1 evidence and verification repository with persistent AI communication, provenance, validation, research and a shared AXIOM↔Cursor research-pipeline archive.

## Repository status

This repository records exact bytes, provenance, validation state, caveats, research handoffs and platform receipts. Hashes, signatures, commits, CI, releases, attestations, agent agreement and public availability do **not** establish scientific truth.

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
```

## Repository Order Law

`REPOSITORY_ORDER_LAW_V1` is binding for AXIOM, Cursor/PRAXIS, Copilot, external research agents and future repository work.

1. Every new artifact is classified before it is written.
2. The root is an allowlisted control surface, never a dump directory.
3. One artifact class has one canonical owning directory.
4. Normal active research belongs under `research/<phase>/<agent-or-topic>/`.
5. `research/pipeline/` is the sole cross-phase research-infrastructure exception and is jointly owned by AXIOM and Cursor/PRAXIS.
6. `research/pipeline/handoff/` is the fixed GitHub Inbox -> Validate -> Bind -> Relay -> Ack surface for external agent and Cursor returns.
7. Stable R5 work is mirrored symbiotically across `docs/r5/`, `schema/r5/`, `scripts/r5/`, `tests/r5/`, `validation/r5/`, `examples/r5/` and `research/r5/`.
8. Scientific evidence remains under `objects/` + `index/`; communication provenance remains under `communication/objects/` + `communication/index/`.
9. Historical path-bound evidence is not relocated merely for aesthetics.
10. Structural changes update this README and `docs/architecture/REPOSITORY_STRUCTURE.json` in the same change.
11. Disorder is corrected at intake; noncritical placement errors do not halt unrelated research.

Detailed policy: `docs/governance/REPOSITORY_ORDER_POLICY.md`.

## Exact live directory contract

```text
/
├── .github/
│   ├── CODEOWNERS
│   ├── copilot-instructions.md
│   └── workflows/
│       ├── validate-a83-framework-hardening.yml
│       ├── validate-anchor.yml
│       ├── validate-artifact-handoff.yml
│       ├── validate-repository-structure.yml
│       ├── validate-research-pipeline.yml
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
├── requirements-a83-test.txt
├── communication/
│   ├── README.md
│   ├── index/v1/{latest.json,records.jsonl}
│   └── objects/sha256/.../record.json
├── docs/
│   ├── README.md
│   ├── AI_CONTEXT.md
│   ├── AI_HANDOFF_PROTOCOL.md
│   ├── OPEN_SCIENCE_AGENT_COMMUNICATION_MANIFEST.md
│   ├── SCIENTIFIC_COMMUNICATION_IMPLEMENTATION_PROFILE_V0_1.md
│   ├── artifact-handoff-protocol.md
│   ├── agent-protocol.md
│   ├── release-checklist.md
│   ├── architecture/
│   │   ├── REPOSITORY_STRUCTURE.md
│   │   ├── REPOSITORY_STRUCTURE.json
│   │   └── SHARED_RESEARCH_PIPELINE_ARCHITECTURE.md
│   ├── governance/
│   │   ├── REPOSITORY_ORDER_POLICY.md
│   │   └── REPOSITORY_PATH_RULES.json
│   ├── phase2/                         # immutable path-bound history
│   └── r5/README.md
├── examples/
│   ├── README.md
│   ├── a83/
│   ├── artifact-handoff/
│   ├── scientific-communication/
│   └── r5/README.md
├── index/
│   ├── README.md
│   └── v1/
├── objects/
│   ├── README.md
│   └── sha256/
├── schema/
│   ├── README.md
│   ├── A83_handoff_envelope_v1.schema.json
│   ├── agent-return-v1.schema.json
│   ├── artifact-handoff-envelope-v1.schema.json
│   ├── artifact-handoff-ledger-event-v1.schema.json
│   ├── artifact-handoff-receipt-v1.schema.json
│   ├── anchor-manifest-v1.schema.json
│   ├── research-pipeline-event-v1.schema.json
│   ├── research-pipeline-package-v1.schema.json
│   ├── scientific-communication-v1.schema.json
│   └── r5/README.md
├── scripts/
│   ├── README.md
│   ├── a83_decision.py
│   ├── a83_sentinel.py
│   ├── append_scientific_record.py
│   ├── artifact_handoff.py
│   ├── reproduce_a83.py
│   ├── research_pipeline.py
│   ├── validate_a83_handoff.py
│   ├── validate_anchor.py
│   ├── validate_repository.py
│   ├── validate_repository_structure.py
│   ├── validate_scientific_communication.py
│   ├── validate_scientific_ledger.py
│   ├── verify_a83_artifact_binding.py
│   └── r5/README.md
├── tests/
│   ├── README.md
│   ├── test_a83_handoff.py
│   ├── test_artifact_handoff.py
│   ├── test_repository_structure.py
│   ├── test_research_pipeline.py
│   ├── test_scientific_communication.py
│   ├── test_scientific_ledger.py
│   ├── test_validate_anchor.py
│   └── r5/README.md
├── validation/
│   ├── README.md
│   ├── A83_ARTIFACT_BINDING_v1.0.json
│   ├── A83_FINAL_STATUS_v1.0.json
│   ├── A83_WEAKNESS_AND_OPEN_QUESTIONS_AUDIT_v1.0.json
│   ├── a83-handoff-negative-fixtures-v1.jsonl
│   ├── artifact-handoff-negative-fixtures-v1.jsonl
│   ├── scientific-communication-negative-fixtures-v1.jsonl
│   └── r5/
├── research/
│   ├── README.md
│   ├── pipeline/
│   │   ├── README.md
│   │   ├── POLICY.md
│   │   ├── events/README.md
│   │   ├── handoff/
│   │   │   ├── README.md
│   │   │   ├── inbox/
│   │   │   ├── bound/
│   │   │   ├── relay/
│   │   │   └── ack/
│   │   ├── packages/README.md
│   │   ├── index/
│   │   │   ├── latest.json
│   │   │   └── packages.json
│   │   └── templates/
│   │       ├── event.template.json
│   │       └── package-manifest.template.json
│   └── r5/
│       ├── README.md
│       ├── axiom-platform-audit/
│       └── qwen-coder/
└── archive/
    └── README.md
```

`docs/phase2/` and `requirements-a83-test.txt` remain in historical paths because A83 artifact bindings name those paths explicitly. Their location is a provenance constraint, not unsorted residue.

## Shared AXIOM↔Cursor research pipeline

`research/pipeline/` accumulates coherent research intervals into timestamped packages. Packages remain at stable paths; lifecycle changes are append-only events.

```text
INTAKE
→ ACTIVE
→ READY_FOR_CURSOR
→ CURSOR_PROCESSING
→ PROCESSED
```

AXIOM may continuously add causally related research items without a separate Cursor Auftrag for each small step. Cursor consumes an immutable sealed snapshot and names the exact package ID + snapshot version in its result.

The pipeline uses a NEXUS profile inspired by RO-Crate research objects, W3C PROV provenance, OCFL immutable version/fixity principles and BagIt checksum-manifest discipline. Conformance to those external standards is not claimed unless separately validated.

See:

- `research/pipeline/README.md`
- `research/pipeline/POLICY.md`
- `docs/architecture/SHARED_RESEARCH_PIPELINE_ARCHITECTURE.md`

## Artifact handoff automation

External agent and Cursor returns enter through:

```text
research/pipeline/handoff/inbox/<HANDOFF_ID>/handoff.json
```

The GitHub workflow `validate-artifact-handoff` performs:

```text
INBOX
-> VALIDATE
-> BIND
-> RELAY
-> ACK
```

It validates byte references, Entry/Exit Receipts, File-Event Ledgers,
Workflow-Event Ledgers, token/continuation status and Authority-Gates. It fails
closed on missing evidence, self-validation, merge, main write, force-push,
claim promotion or foundation promotion.

The current R3 completion return is seeded as:

```text
NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0
```

under PR15/R3 research branch scope. R2 and PR13 remain separate lanes.

## Domain ownership

| Path | Canonical responsibility |
|---|---|
| `.github/` | GitHub-native governance, ownership, CI |
| `objects/` | content-addressed scientific evidence |
| `index/` | discovery index for scientific evidence |
| `communication/` | content-addressed communication/provenance ledger |
| `docs/` | stable specifications, architecture and governance |
| `schema/` | machine-readable contracts |
| `scripts/` | executable tooling and validators |
| `tests/` | automated tests |
| `validation/` | fixtures, bindings and validation receipts/state |
| `examples/` | non-authoritative examples |
| `research/` | active research plus the shared pipeline control/archive surface |
| `archive/` | retired non-path-bound material and migration records |

## Agent entry points

Read in this order:

1. `AGENTS.md`
2. `GOVERNANCE.md`
3. `docs/AI_CONTEXT.md`
4. `docs/agent-protocol.md`
5. `docs/artifact-handoff-protocol.md` when receiving or relaying an agent return
6. `docs/architecture/REPOSITORY_STRUCTURE.md`
7. `research/pipeline/README.md` when accumulating or processing batched research
8. `index/v1/latest.json` when current scientific evidence state is relevant

## Validation

```bash
python scripts/validate_repository_structure.py --root .
python -m unittest tests.test_repository_structure
python scripts/research_pipeline.py --root . validate
python -m unittest tests.test_research_pipeline
python scripts/artifact_handoff.py --root . validate
python -m unittest tests.test_artifact_handoff
```

Dedicated CI checks: `validate-research-pipeline`, `validate-artifact-handoff`.

## Licensing

Original documentation is offered under CC BY 4.0. Original validation/tooling code is offered under Apache-2.0. Third-party materials are excluded unless their licensing is explicitly recorded.

## Security

See `SECURITY.md`. Do not publish credentials, personal data, medical data, private conversations, non-public repository material or unredacted security logs.
