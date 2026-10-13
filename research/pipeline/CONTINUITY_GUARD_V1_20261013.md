# NEXUS OMEGA · Archive Continuity Guard V1 · 2026-10-13

```text
OBJECT = NEXUS_OMEGA_RESEARCH_CONTINUITY_GUARD_V1_20261013
STATE = READONLY_ORGANIZATIONAL_OBSERVABILITY_CANDIDATE
PIPELINE = research/pipeline/ EXISTING_SHARED_PIPELINE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = OPERATOR_DIRECT_RESEARCH_AND_ORGANIZATION_CONTINUITY
GITHUB_ACTIONS = EXISTING_validate-research-pipeline_WORKFLOW_EXTENDED
NEW_MCP_BUS = NO
NEW_WORKFLOW_FILE = NO
NEW_DATABASE = NO
MODEL_INFERENCE_IN_AUDIT = NO
NODE_RESTART = NO
WWW_NEW_DESIGN_DEPLOY = NO
```

## Problem and root cause

On 2026-10-13, six-week-old NEXUS research and organizational artifacts had to be rediscovered from context rather than from an always-current authoritative inventory. The **existence** of source archives does not imply **findability**, current lineage, or resumed processing. The GitHub shared pipeline already uses stable package paths, event-sourced lifecycle and immutable snapshots, but its *derived* `research/pipeline/index/latest.json` and `packages.json` were last generated on **2026-09-01** and show one historical READY_FOR_CURSOR package. This may indicate stale navigation, **not** proof of a failing pipeline or of forgotten private artifacts.

AXIOM independently read the latest GitHub structure v1.7.13 and confirmed all 23 registered `research/**/README.md` exist. The previous historical package SHA256SUMS was independently tested 7/7 MATCH and pipeline tool tests 4/4 PASS. Consequently the immediate remediation is **freshness detection plus actionable source identity**, not replacing existing infrastructure.

## High-end open-source principles, chosen by measured fit

| Public source | Reusable principle | NEXUS action | Standalone infrastructure now? |
|---|---|---|---|
| [OpenLineage job/run/dataset facets](https://openlineage.io/docs/spec/facets/) | Typed source→job→output lineage, event-time/actor/run identity | Design future optional `PROV_EDGE` projection backed by existing canonical events; do not infer unsupported semantic/causal edges | NO |
| [OCFL 1.1](https://ocfl.io/1.1/spec/) | Versioned archival objects, content fixity, preservation completeness | Retain immutable sealed vN and detached SHA-256; avoid unearned OCFL conformance | NO |
| [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) | Self-describing research object metadata (JSON-LD) | Future optional export of existing manifests after schema validation | NO |
| [DataHub OSS](https://github.com/datahub-project/datahub) / [OpenMetadata](https://docs.open-metadata.org/) | Searchable data catalogs, owners, lineage, status | Candidate for later scale-triggered metadata search only; no duplicate truth DB | NO |
| [Prefect](https://github.com/PrefectHQ/prefect) / [Kestra](https://github.com/kestra-io/kestra) | Scheduling and recoverable task orchestration | Retain existing Node Bus / Cursor and GitHub workflow first; actual orchestration gaps must be measured | NO |

These are referenced design patterns, not installed packages, endorsed vendors, imported binaries or validated certification claims. Different editions/licenses and third-party dependencies require their own review.

## Actual V1 executable

`python scripts/archive_continuity_guard.py --root . --max-age-days 30 --fail-on-integrity`

Stdlib-only, no LLM client or networking. It reads existing `REPOSITORY_STRUCTURE.json`, registered lane directory/README existence, historical `research/pipeline/packages/*/*/NEXUS_RP_*/manifest.json`, event JSON identity/timestamps and derived index generation timestamp.

The tool reports **two disjoint classes**:
- `INTEGRITY`: missing registered physical lane/README, path duplicate, package ID mismatch, invalid package/event/index timestamps or invalid event identity. With `--fail-on-integrity`, these fail the GitHub job. Invalid JSON/duplicate keys fail closed with nonzero error.
- `REVIEW_ONLY`: open packages with manifest age >=30 days; derived navigation index age >=30 days. An old **terminal** package is not flagged as open. These are prompts to reconcile against authoritative events, **never evidence a package is scientifically invalid** and **never block unrelated C1 publication**.

The output is machine-readable derived JSON on stdout (not a new canonical event). It exposes `local_windows_archive_roots=NOT_ACCESSED`, `runtime_mcp_node_bus=NOT_ASSESSED`, and `website_publication_parity=NOT_ASSESSED`; it does not invent a Windows or web result. The user can replay the exact temporal scenario with `--as-of 2026-10-13T00:00:00Z`. Unit tests: `python -m unittest tests.test_archive_continuity_guard -v`, 10 isolated negative fixtures.

**Existing** workflow `.github/workflows/validate-research-pipeline.yml` now runs daily at 05:17 UTC (subject to GitHub scheduling behavior/delays) and on changed pipeline, structure, script or tests; it produces a simple workflow-step summary and preserves all historical existing checks. No new workflow/privileged token, network ingress, Hostinger write or autonomous action engine. It **does not write an updated derived index**: event-sourced indexes must only be rebuilt deterministically after independent source reconciliation, with appropriate scoped authorization.

## Time-based research continuity requirements

For each physical Node/TRANSFER/local archive object, the existing Node-Bus crosslane Cursor G02/G06 return should **append** a source-exact record:
```text
OBJECT_ID · PHYSICAL_SHA256 · SOURCE_ROOT_CLASS · SOURCE_TIMESTAMP_UTC
FOUND_AT_UTC · LAST_VALIDATED_AT_UTC · AUTHORITY_AND_PRIVACY_CLASS
STABLE_LANE_ID · PARENT_IDS · SUCCESSOR_IDS · CURRENT_OPEN_OR_TERMINAL_STATE
LAST_EVENT_ID · LAST_SEALED_SNAPSHOT · VALIDATOR_INDEPENDENCE
RUNTIME_STATUS · GITHUB_RECEIPT · WWW_PARITY_RECEIPT_OR_GAP
```

Source file paths and private log bodies are local-only. Public derivatives may contain only sanitized IDs, hash identities and permissible research metadata. A material original reappearance is an intake event, not permission to rewrite existing history. More than one full week without physically corroborated original source checks is an observation gap, not a claim the source disappeared.

### Proposed service levels (measurable, not already achieved)

- **At intake:** source ID + privacy classification + original bytes SHA-256 or named SOURCE_GAP.
- **Within the next successfully executed audit:** all registered lanes discoverable, readme+source refs valid, newly seen local-only objects appended, duplicates linked rather than copied.
- **At 7 days since last verified observation:** review flagged; this requires local Node-Bus evidence not currently available from GitHub-only scans.
- **At 30 days of an open package / derived index:** REVIEW_ONLY aging, not system-wide HOLD.
- **On changed original hash or missing sealed item:** INTEGRITY/HOLD_SCOPED with source reference; never silently overwrite.
- **On final return:** independent source-exact readback; only then bind completed status and release website public-safe derivative through existing Hostinger publication process.

## Status limits

The first GitHub-only guard is one concrete preventive layer, **not yet a full archival inventory, not a production-connected MCP worker, and not proof that every 6-week-old local artifact has been recovered**. A future phase must bind the actual Windows archives and the existing `NEXUS_NODE_BUS` via the already issued Cursor audit order `NEXUS_OMEGA_AXIOM_TO_CURSOR_NEXUS_NODE_BUS_TOKENNEUTRAL_ALL_LANE_CROSSVALIDATION_20261013_R0`, without creating another Cursor order or bus. All unresolved scientific R17/R18/R32/R33 gaps and GitHub↔WWW parity states remain unchanged.

`BLOCKED_LANE != BLOCKED_SYSTEM · SOURCE_EXISTS != SOURCE_DISCOVERABLE · SOURCE_DISCOVERABLE != SOURCE_VALIDATED`.
