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
6. Stable R5 work is mirrored symbiotically across `docs/r5/`, `schema/r5/`, `scripts/r5/`, `tests/r5/`, `validation/r5/`, `examples/r5/` and `research/r5/`.
7. Scientific evidence remains under `objects/` + `index/`; communication provenance remains under `communication/objects/` + `communication/index/`.
8. Historical path-bound evidence is not relocated merely for aesthetics.
9. Structural changes update this README and `docs/architecture/REPOSITORY_STRUCTURE.json` in the same change.
10. Disorder is corrected at intake; noncritical placement errors do not halt unrelated research.

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
│       ├── validate-repository-structure.yml
│       ├── validate-research-pipeline.yml
│       ├── validate-r7-radiometric.yml
│       ├── validate-r8-custody.yml
│       ├── validate-r8-r1-r2-crossvalidation.yml
│       ├── validate-ix-r1-open-agent-foundation.yml
│       ├── validate-ix-r2-integrity-boundary-foundation.yml
│       ├── validate-ix-r3-controlled-falsification.yml
│       ├── validate-ix-r4-order.yml
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
│   ├── scientific-communication-negative-fixtures-v1.jsonl
│   └── r5/
├── research/
│   ├── README.md
│   ├── fundus/
│   ├── r6/
│   ├── r7/
│   ├── r8/
│   ├── ix/
│   │   ├── README.md
│   │   ├── open-agent-foundation-r1/
│   │   ├── open-agent-foundation-r2/
│   │   ├── open-agent-foundation-r3/
│   │   └── open-agent-foundation-r4/
│   ├── pipeline/
│   │   ├── README.md
│   │   ├── POLICY.md
│   │   ├── events/README.md
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
5. `docs/architecture/REPOSITORY_STRUCTURE.md`
6. `research/pipeline/README.md` when accumulating or processing batched research
7. `index/v1/latest.json` when current scientific evidence state is relevant

## Validation

```bash
python scripts/validate_repository_structure.py --root .
python -m unittest tests.test_repository_structure
python scripts/research_pipeline.py --root . validate
python -m unittest tests.test_research_pipeline
```

Dedicated pipeline CI check: `validate-research-pipeline`.

## Licensing

Original documentation is offered under CC BY 4.0. Original validation/tooling code is offered under Apache-2.0. Third-party materials are excluded unless their licensing is explicitly recorded.

## Security

See `SECURITY.md`. Do not publish credentials, personal data, medical data, private conversations, non-public repository material or unredacted security logs.

## R27-E · External Agent Structural Firewall (C1)

The NEXUS-owned external-agent contract is defined in [docs/governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md](docs/governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md). Only NEXUS provisions return slots; the first preallocated slot is [research/r27/www-extern-wake-isolation-20261011/returns/](research/r27/www-extern-wake-isolation-20261011/returns/). Valid external contributions are **create-only**, limited to exact preapproved filenames and a detached SHA-256 manifest. No external agent may create top-level folders, namespaces, workflows, source-code directories, ZIP dumps or Hostinger mirrors. Machine policy: `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json`; schema: `schema/external-agent-return-r27e-v1.schema.json`; check: `scripts/validate_external_agent_pr.py`, `.github/workflows/validate-external-agent-pr.yml`. Unregistered GitHub identities are denied until approved.

The workflow runs base-branch code only; **a passing workflow is not itself an enforced branch rule**. Required status checks, CODEOWNERS approval and repository write/merge restrictions must be confirmed in GitHub ruleset settings by the Operator. This does not authorize a live WWW broker, privileged internal node, new Cursor worker or scientific promotion.

## R26/P26 → R27 collective expert MAXI research assignment and AXIOM intake · 2026-10-11

NEXUS owner-authorized scientific assignment package (not external writer slot):
[`research/r26/collective-expert-handoffs-20261011/`](research/r26/collective-expert-handoffs-20261011/README.md). Contains the full seven-specialist research brief, seven exact source-hashed orders and the owner-authored assignment ledger. The R27 folder intake is **R26/P26 scientific material**, not proof of an independent R27 experiment. Source PR #92 merged at `c88da5873b5897585ac34e4066dcaabd963fdb03`.

**AXIOM passive handshake inbox:** [NEXUS_OPERATOR_AXIOM GitHub issue #93](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93). Future external returns require independently verified GitHub actor + operator-issued exact write slot, or clearly marked `OPERATOR_TO_AXIOM_BRIDGE`; the default external write allowlist remains EMPTY. Detached handshakes use `schema/expert-hash-handshake-v1.schema.json`, byte-only offline checker `scripts/verify_expert_hash_handshake_v1.py` and regression `tests/test_expert_hash_handshake_v1.py`. Neither matching hashes nor passing CI authorizes runtime, release or scientific promotion. R27-E's seven-file slot and branch-rule enforcement gaps remain unchanged.

## TASK ANCHOR NORM V1 · prospective source-bound task continuity

The operator-issued **internal normative task-contract** is `docs/governance/NEXUS_OMEGA_TASK_ANCHOR_NORM_V1.md`. It is informed by DIN SPEC 92001-1 quality dimensions **but is neither a DIN Norm nor DIN-certified**. New substantial expert, AXIOM and Cursor orders should carry immutable origin/authority/scope, an associated `TASK_ORDER_ANCHOR` envelope and non-destructive `DRIFT_RESET` semantics. `DRIFT_RESET` means rebind-and-append, **not** node-state reset, memory erasure or rollback of negative findings. The required files are `schema/task-anchor-norm-v1.schema.json`, `scripts/validate_task_anchor_norm_v1.py`, `tests/test_task_anchor_norm_v1.py` and `examples/task-anchor-v1.example.json`. DeepSeek's source proposal and limitation audit are recorded separately under `docs/governance/NEXUS_OMEGA_DEEPSEEK_TASK_ANCHOR_ADJUDICATION_20261011_R0.md`.

Repository ordering and the R27-E external-agent firewall remain intact, actor allowlist remains empty, no direct external write or Cursor/Hostinger execution is authorized by the format. The offline test validates structure and reset boundaries only; it does not prove actual runtime integration or a scientific claim. Existing R26/R27 immutable orders are not retroactively rewritten.

## R10R29 · Open-Mind cross-domain C1 scientific foundation

Owner-issued R29 research lane: [`research/r29/r10r29-open-mind-cross-domain-20261011/`](research/r29/r10r29-open-mind-cross-domain-20261011/README.md), governed by `NEXUS_OMEGA_TASK_ANCHOR_NORM_V1` (DRIFT_RESET only, **never NODE_RESET**). This exploratory order follows the source-exact **unmerged** R10R28 branch order (commit `ae543022dce52b45e85b64a48bc1c93357b7522f`) and uses only **methodological**, not empirical, transfer from BTCD/BTMA report-level findings.

Six open research questions and G0–G9 include information loss, time/unit/calibration discipline, synthetic model federation, stochastic geometry, falsifier-led alternative models, and negative-validation contracts. L3-A/B/C remain **not selected and not executed**; NF05/NF06 remains `REVISIONS_REQUIRED`; no privileged runtime, external agent permissions, new worker, repository history rewriting, Hostinger publishing or promotion > C1. Source metadata and public-safe exact-order hashes are kept within the R29 topic; no raw private archives are mirrored.


## R10R29 · Computer + Perplexity C1 source validation · 2026-10-11

Owner-operated, append-only [R10R29 cross-validation intake](research/r29/r10r29-open-mind-cross-domain-20261011/crossvalidation-20261011/README.md) against **PR #97** exact original order. Independent verification covers source/ZIP integrity (**12/12** ZIP SHA256SUMS), Perplexity text receipt, source-level caveats and full 5-file hash ledger. **Binary originals (two PDFs and 512,536-byte ZIP) are inventory-bound, not GitHub-published in this PR.** R29 G1–G9 research remains unexecuted/not proven; no L3 selection, NF05/06 freeze, external direct writer grant, NODE_RESET or Hostinger deployment. C1_DESCRIPTIVE_ONLY.

## Direct C1 research publication (Operator, 2026-10-12)

The Operator authorized AXIOM to publish public-safe, independently source-checked C1 research directly without serial approval paperwork. See [the direct research publication rule](docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md). Existing branch protections, scientific and privacy limits remain. R18 source-bound research: [clean-room-provenance-20261012](research/r18/clean-room-provenance-20261012/README.md). A publication receipt does not establish runtime deployment or scientific truth.

## R16 and R17 original research deposits (Operator direct C1 publication)

The full [R16 AXIOM software-foundation report](research/r16/axiom-software-foundation-20261012/README.md) and [R17/R16 intake adjudication](research/r17/axiom-mind-module-20261012/README.md) are preserved as source-exact research text, not as claims of completed runtime deployment. The original ZIP binaries and external source files are not implicitly uploaded.

## AXIOM ALPHA-NODE · standing C1 adaptation

[Continuous C1 intake contract and tested research reducer](research/r16/axiom-alpha-node-c1-adaptation-20261012/README.md) reuses the existing hourly AXIOM inbox watch and the [direct research publication rule](docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md). Append-only knowledge updates can be published without repeated operator handoffs; isolated code changes remain candidates, not automatic production modification.

## R16 delayed AutoClaw R3 research (2026-10-12)

The [sanitized, independently replayed AutoClaw R3 intake](research/r16/autoclaw-r3-cross-platform-20261012/README.md) records a C1 scoped Linux reproduction, Windows producer reports and an explicit privacy-based original-archive publication gap. Append-only scientific delta; original ZIP is not committed and R17 terminal remains not established.

## R17 one-shot C1 closeout finding (2026-10-12)

A [new scoped R17 source-gap finding](research/r17/axiom-mind-module-20261012/NEXUS_OMEGA_AXIOM_R17_ONE_SHOT_C1_SCOPED_HOLD_20261012_R1.md) follows the earlier source-bound R17/R16 intake. Cursor reports no standalone R17 original; the one-shot audit itself has finished, but R17 science remains HOLD_SCOPED. This report-level finding is published without any new pipeline or productive runtime change.

## Forum GitHub_Implant · Operator public C1 WWW parity (2026-10-12)

The [GitHub_Implant](research/forum/github-implant-20261012/README.md) is a first-party, responsive, read-only GitHub REST viewer, developed for the existing `/forum/github-implant/` path. Its [standalone three-file site](research/forum/github-implant-20261012/site/index.html) and [one-shot Hostinger mount contract](research/forum/github-implant-20261012/FORUM_HOSTINGER_ONE_SHOT_MOUNT.txt) are source-public on GitHub. **GitHub source publication is not proof the Hostinger website serves it.** The current Hostinger AI Builder connection exposes no website; live site deployment and www HTTPS validation are explicitly pending a capable owner-side site transport. A public-safe offline [exact-byte mirror builder](research/forum/github-implant-20261012/tools/mirror_public_git.py) supports the operator's additional source-hosting objective; API browsing itself is not a hosted full mirror. See [GitHub↔WWW parity policy](docs/governance/NEXUS_OMEGA_GITHUB_WWW_PARITY_RULE_V1_20261012_R0.md). C1 only.

## GitHub↔NEXUS Security & Science Gate · 2026-10-12

[Gate source and C1 scientific boundary](research/forum/github-implant-20261012/GATE_INTERFACE_CONTRACT_V1.md) monitor only the three canonical public GitHub_Implant files against the NEXUS WWW copies (SHA-256/byte-length/C1 marker) and display a fallback floating/Picture-in-Picture panel. No new repository root or CI workflow. The user-facing gate will be live only after independently verified existing-site Hostinger installation of the four new `site/gate/` files and the additive gate link in `site/index.html`; the GitHub commit alone is not proof of WWW installation.

## Public research catalog clarity · 2026-10-12 (existing route, no new truth store)

The [existing-source-ledger-driven research catalog interface](research/website/research-catalog-clarity-20261012/README.md) is a minimal, accessible redesign of the **existing** `/research/catalog/` leaf only, inspired by metadata and filtering conventions of Zenodo, OSF and Hugging Face. It retains `/research/catalog.json` as canonical, nine original public-record IDs and seven archived withheld counts with C1 caveats. The historic fallback carries a visibly dated 2026-09-22 snapshot label, never a fake live stamp. The [single existing-site Hostinger mount](research/website/research-catalog-clarity-20261012/SITE_EXISTING_RESEARCH_CATALOG_MOUNT.txt) explicitly preserves the homepage, the registered Living Node Sky, Forum/GitHub_Implant, all detail pages and R19. **Research UI source on GitHub != site deployment**. C1_DESCRIPTIVE_ONLY.

## AXIOM C1 node fit: Gotham-like open analytics components (2026-10-12)

[14 individually license-screened cross-domain candidates](research/architecture/gotham-open-components-c1-prevalidation-20261012/README.md) are bound only as **research options**, not installed Nodes. Jena and existing append-only source provenance for AXIOM, Hop for conditional PRAXIS batch imports, SGP4/Cesium/QGIS for optional ORBIS/ASTRA work, and separately scoped OpenCTI CE for legitimate security research. Neo4j CE has GPLv3 considerations; Memgraph uses BSL/enterprise license; Senzing engine and Maltego application are proprietary notwithstanding free editions/OSS extension libraries. No Gotham code, private identity resolution, scientific claim promotion, site change or R19 runtime action. Original upstream source binaries are not hash-audited. GitHub C1 research publication is distinct from future website mirror verification.

## NSCF R32 / R18 source STOP / Legal-Flex R33 · independent C1 audit (2026-10-12)

The operator-provided [12-artifact NSCF/R18/Legal-Flex intake](research/communication/nscf-r32-r18-seed-r33-legal-20261012/README.md) has an independently replayed 20/20 R32 reference codec suite, 9/9 R33-R1 synthetic structural tests and R33-v2 27 executed PASS + 1 skipped JPlag integration test. The earlier R18 7-fixture source binding remains **STOP_SCOPED**: F01 actual vs declared SHA-256 differs and the submitted branch snapshot has only 2/9 declared children. The one-field F01 hypothetical correction explains the delta without modifying the historical source. Legal clean-room and NLI/embedding gates remain unproven. The original DeepSeek Layer-0/A/B/C drawing is a proposal, not a token-compression benchmark or security certificate. Full historical ZIPs remain outside public GitHub; original source hashes are registered. No Node install, Cursor follow-up, R19 promotion, or website deployment is claimed. C1_DESCRIPTIVE_ONLY.

## Existing NEXUS_NODE_BUS — tokenneutral all-lane C1 VM audit order · 2026-10-13

[Operator-scoped Cursor/PRAXIS single-run order](research/architecture/node-bus-crosslane-tokenneutral-20261013/README.md) checks the existing NEXUS_NODE_BUS JSONL/MCP binding and independently reconciles **all 22 previously registered GitHub research Lanes**, any independently discovered local modules, exact source bytes, scientific negative fixtures, event-sourced archive state and WWW/GitHub provenance. An independently replayed historical pipeline source passed 4/4 unit tests and 7/7 snapshot fixity, but that alone does not establish current MCP runtime or all-lane completion. This is a source-only C1 order: deterministic local computation rather than external LLM calls in the validation hot path; zero measured inference cost and production activation are **not claimed**. No extra pipeline, new bus, Hostinger write, Node reset or reopened unrelated Cursor workflow.

## Research archive continuity · existing pipeline guard · 2026-10-13

The [Continuity Guard V1](research/pipeline/CONTINUITY_GUARD_V1_20261013.md) prevents **silent research-discoverability debt** from being confused with a successful archive. It extends existing shared research pipeline CI with a daily, offline/std-lib, read-only audit of registered lane discovery, event/package integrity, 30-day open-package and navigation-index aging, ten negative fixtures, and GitHub Actions step-summary observability. It is source-only organizational C1 work; no new bus, workflow file, database, external model, host write or claim promotion. Existing Cursor/PRAXIS Node-Bus audit must bind private Windows source inventory separately. `C1_DESCRIPTIVE_ONLY`.


## NEXUS Repository Steward · C1 seedling · 2026-10-13

The [existing-CI repository steward](docs/architecture/NEXUS_REPOSITORY_STEWARD_V1_20261013.md) performs a source-exact read-only inventory of the complete tracked Git tree (source commit, bytes, SHA-256, registered lanes, unsafe paths and review-only naming differences). It runs inside the **existing** repository-structure workflow on PRs/pushes and best-effort daily; it does **not** rename historic bound objects, perform live NEXUS_NODE_BUS discovery, or authorize a claim promotion. Prospective lower-case kebab-case naming is documented; legacy identities are preserved until an independently reviewed migration receipt.


## R17 Evaluator-guided Co-Design · C1 research · 2026-10-18

- [R17 quantum-to-integrity research](research/r17/evaluator-guided-codesign-20261018/) — new owner-research sibling; R18 proposals remain unratified, no runtime or quantum execution.
