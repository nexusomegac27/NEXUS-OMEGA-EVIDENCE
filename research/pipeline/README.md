# NEXUS OMEGA Shared Research Pipeline Archive

```text
OBJECT = NEXUS_OMEGA_SHARED_RESEARCH_PIPELINE_ARCHIVE_V1
STATE = RESEARCH_INFRASTRUCTURE_CANDIDATE
OWNERS = AXIOM + CURSOR/PRAXIS
CLAIM_CEILING = C1
```

This directory is the shared AXIOM↔Cursor research-pipeline archive. Its purpose is to accumulate many small research deltas into orderly, timestamped, provenance-preserving research packages so the Operator does not need to commission every intermediate step separately.

## Design basis

The NEXUS profile borrows complementary principles from established research-data/archive models without claiming conformance by default:

- **RO-Crate**: self-describing research objects and machine-readable contextual metadata.
- **W3C PROV**: explicit Entity → Activity → Agent provenance relations.
- **OCFL**: immutable historical versions, inventory/fixity discipline, stable object identity and a derived current head.
- **BagIt**: complete checksum manifests over transferred payload snapshots.
- **Git**: immutable commits/blobs and reviewable causal change history.

The package path is stable. Lifecycle state is represented by append-only event objects, not by moving a package between `inbox/active/processed` directories.

## Canonical topology

```text
research/pipeline/
├── README.md
├── POLICY.md
├── index/
│   ├── latest.json              # derived navigation view; not authority
│   └── packages.json            # derived package catalog
├── events/
│   └── README.md                # one immutable JSON event per file
├── packages/
│   └── README.md                # stable package roots, timestamp partitioned
└── templates/
    ├── package-manifest.template.json
    └── event.template.json
```

Runtime-created package shape:

```text
packages/YYYY/MM/<PACKAGE_ID>/
├── manifest.json                # current bounded package description
├── provenance.json              # entity/activity/agent graph
├── items.json                   # exact source/artifact references
├── timeline.json                # derived ordered event view
└── snapshots/
    └── vN/
        ├── manifest.json         # immutable sealed snapshot
        ├── items.json
        ├── provenance.json
        ├── SHA256SUMS.txt
        └── CURSOR_HANDOFF.md
```

## Lifecycle

```text
INTAKE
→ ACTIVE
→ READY_FOR_CURSOR
→ CURSOR_PROCESSING
→ PROCESSED
```

Additional bounded states:

```text
BLOCKED
SUPERSEDED
REOPENED
```

Lifecycle changes are append-only event files under `events/YYYY/MM/DD/`. `index/latest.json` and `index/packages.json` are rebuildable projections.

## Package identity

Recommended ID:

```text
NEXUS_RP_<UTC-YYYYMMDDTHHMMSSZ>_<slug>_<8hex>
```

Every package records:

- creation timestamp in UTC;
- phase/strand;
- producer(s) and intended processor;
- predecessor packages when applicable;
- research questions;
- source/artifact references;
- exact Git commit/blob identities where available;
- SHA-256/bytes for physical files where available;
- findings and uncertainty classes;
- current lifecycle state;
- snapshot history;
- claim ceiling and promotion boundary.

## AXIOM operating rule

AXIOM may continuously accumulate lawful research deltas into an active package during normal work. Small steps do not each require a separate Cursor execution order.

A package is sent to Cursor only after it reaches `READY_FOR_CURSOR` and a sealed snapshot has been generated.

## Cursor operating rule

Cursor consumes the sealed snapshot, records processing/validation results as new package events or a successor snapshot, and does not silently rewrite the original AXIOM research history.

## Authority boundary

```text
PIPELINE_PACKAGE != IMPLEMENTATION_AUTHORITY
RESEARCH_ACCUMULATION != CURSOR_EXECUTION
READY_FOR_CURSOR != VALIDATED
PROCESSED != CLAIM_PROMOTED
```

Package/archive metadata may improve provenance and efficiency. It cannot promote scientific claims.
