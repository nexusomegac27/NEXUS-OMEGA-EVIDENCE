# NEXUS OMEGA Shared AXIOM↔Cursor Research Pipeline Architecture v1

## Purpose

The pipeline converts continuous research work into coherent, timestamped, provenance-preserving packages that can be accumulated by AXIOM and processed by Cursor/PRAXIS in batches.

The architecture is intentionally hybrid:

- RO-Crate-inspired research-object metadata;
- W3C PROV-inspired Entity/Activity/Agent relations;
- OCFL-inspired immutable version/snapshot and fixity discipline;
- BagIt-inspired complete checksum manifests for sealed transfer snapshots;
- Git-native immutable commits/blobs and PR review.

This is a NEXUS profile. It does not claim conformance to those standards unless a specific package/profile is independently validated against the relevant specification.

## Why packages do not move between lifecycle directories

A conventional `inbox/ → active/ → processed/` directory workflow makes human navigation easy but changes repository paths every time state changes. For NEXUS, path stability and historical reproducibility matter more.

Therefore:

```text
PACKAGE_PATH = STABLE
STATE = EVENT_SOURCED
INDEX = DERIVED
```

A package stays at one stable timestamped path. State transitions are new immutable event objects.

## Control plane vs research payload

The pipeline is an orchestration/archive control plane. It references existing research objects instead of copying all data.

```text
RAW_AGENT_RESEARCH
        ↓ reference
PIPELINE_PACKAGE
        ↓ sealed snapshot
CURSOR_PROCESSING
        ↓ result references/events
PROCESSED_PACKAGE
```

Agent-specific raw material remains under its canonical agent/topic research lane. Stable framework code/docs remain under their existing domain paths.

## Package lifecycle

```text
INTAKE
  ↓
ACTIVE
  ↓
READY_FOR_CURSOR
  ↓
CURSOR_PROCESSING
  ↓
PROCESSED
```

`BLOCKED` is lane-scoped. `REOPENED` and `SUPERSEDED` are explicit successor transitions.

## Research item model

A package item should describe a research entity by reference:

```text
item_id
role
repository
commit
path
git_blob
bytes
sha256
source_status
producer
observed_at_utc
research_relevance
uncertainty
```

Not every field is always computable. Missing values remain null/NOT_ESTABLISHED rather than inferred.

## Provenance model

NEXUS uses these conceptual mappings:

| NEXUS | W3C PROV analogy |
|---|---|
| source/return/receipt/artifact | Entity |
| search/extraction/validation/synthesis/package processing | Activity |
| AXIOM/Cursor/external agent/platform | Agent |
| predecessor/derivation relation | wasDerivedFrom / used / wasGeneratedBy |

The mapping is conceptual until a formal PROV serialization is emitted and validated.

## Snapshot model

When AXIOM decides a coherent research interval is ready for Cursor, the active package is sealed as `snapshots/vN/`.

The snapshot contains at minimum:

```text
manifest.json
items.json
provenance.json
SHA256SUMS.txt
CURSOR_HANDOFF.md
```

Optional:

```text
ro-crate-metadata.json
source-register.json
finding-register.json
implementation-candidates.json
```

A sealed snapshot is immutable. Corrections create a new snapshot.

## Fixity

`SHA256SUMS.txt` covers every file stored within the sealed snapshot except itself. The checksum file is written last.

This follows the general fixity discipline used by archival packaging systems: payload identity is verified over bytes, not semantic interpretation.

## Queue model

No authoritative mutable queue file is required. Current queues are projections reconstructed from event state:

- active package set;
- ready-for-Cursor set;
- Cursor-processing set;
- processed set.

`index/latest.json` and `index/packages.json` are navigation caches and can be rebuilt.

## Event store

One event per file avoids introducing another shared append-only JSONL race while the existing ledger concurrency research is still open.

Event path:

```text
research/pipeline/events/YYYY/MM/DD/<timestamp>_<event-id>.json
```

Event content states the package, actor, activity, prior/new state, subjects, evidence and notes.

## Automatic assembly rule

AXIOM automatically groups new work into the current package when all are true:

1. the research objective remains coherent;
2. the same strand/phase applies;
3. the same intended Cursor processing mode applies;
4. authority/publication class is compatible;
5. the package remains reviewable as one scientific unit.

Otherwise a new package is created and linked by predecessor/sibling relations.

## Cursor handoff rule

Cursor is expected to process sealed snapshots, not an unbounded mutable working directory. This creates a reproducible processing boundary.

Cursor's return must name the exact package ID and snapshot version it processed.

## Artifact handoff rule

External agent and Cursor returns that should continue autonomously through
GitHub use `research/pipeline/handoff/`.

Unlike package lifecycle state, handoff stage names are fixed directories
because they are transport receipts, not moving research objects:

```text
inbox/  -> submitted handoff envelope
bound/  -> generated byte-binding receipt
relay/  -> generated relay packet
ack/    -> generated acknowledgement receipt
```

Each inbox entry references the original research-lane artifacts by exact path,
byte length and SHA-256. The generated receipts are workflow/provenance objects
only and cannot promote claims, foundations, merge status or integration
authority.

## Artifact rollout preparation rule

Validated handoff chains that need a complete rollout package use
`research/pipeline/rollout/`, separate from `handoff/`.

```text
plans/     -> rollout-preparation plan
receipts/  -> readiness, authority-gate, ack and workflow-event receipts
```

The rollout sequence is `PREPARE -> VALIDATE -> PACKAGE -> AUTHORITY_GATE ->
ACK`. It stops at pending Operator gates and cannot execute merge, main write,
force-push, public release, deployment, claim promotion, foundation promotion
or integration authority.

## Scientific boundaries

```text
PACKAGE_SEALED != VALIDATED
CURSOR_ACK != CURSOR_PASS
PROCESSED != INTEGRATED
ARCHIVED != TRUE
HANDOFF_ACK != SCIENTIFIC_VALIDATION
ROLLOUT_PREPARED != ROLLOUT_EXECUTED
```

## Future optional interoperability

Later versions may add:

- validated RO-Crate 1.2 metadata;
- formal PROV-O/PROV-JSON export;
- BagIt export for offline transfer;
- OCFL-compatible archival export;
- external timestamp/transparency witness;
- Software Heritage/DOI archival for selected public research packages.
