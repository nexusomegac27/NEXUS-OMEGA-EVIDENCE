# NEXUS OMEGA Shared Research Pipeline Policy v1

## Core law

The pipeline is an append-only orchestration and archive layer for AXIOM↔Cursor research. It reduces Auftrag fragmentation without weakening provenance.

```text
BLOCKED_LANE != BLOCKED_SYSTEM
UNCERTAINTY != STOP_CONDITION
RESEARCH_PACKAGE != IMPLEMENTATION_AUTHORITY
```

## 1. Stable package location

A package is created once under:

```text
research/pipeline/packages/YYYY/MM/<PACKAGE_ID>/
```

Its package root is never renamed merely because lifecycle state changes.

## 2. Event-sourced lifecycle

Every material state transition creates a new immutable event file under:

```text
research/pipeline/events/YYYY/MM/DD/<UTC_TIMESTAMP>_<EVENT_ID>.json
```

Events are ordered by their declared UTC timestamp plus event ID. Derived indexes may be rebuilt from package/event records.

## 3. Lifecycle states

- `INTAKE`: package identity established; contents may still be sparse.
- `ACTIVE`: AXIOM is accumulating research deltas.
- `READY_FOR_CURSOR`: AXIOM has sealed a handoff snapshot.
- `CURSOR_PROCESSING`: Cursor has acknowledged and started the sealed snapshot.
- `PROCESSED`: Cursor processing has terminal output for the snapshot.
- `BLOCKED`: a named lane is blocked; independent lanes may continue.
- `SUPERSEDED`: a successor package replaces this package for a declared purpose.
- `REOPENED`: new evidence requires a successor snapshot or renewed processing.

## 4. Package contents are references first

The pipeline does not duplicate every repository artifact. `items.json` should prefer exact references containing:

```text
repository
commit
path
git_blob
bytes
sha256
object_role
source_status
```

Physical copies are included only when preservation, transport, legal availability, or independent validation requires them.

## 5. Snapshot rule

An active package may evolve. A `READY_FOR_CURSOR` transition requires an immutable snapshot under `snapshots/vN/` with:

```text
manifest.json
items.json
provenance.json
SHA256SUMS.txt
CURSOR_HANDOFF.md
```

A correction after sealing creates `vN+1`; it does not mutate the sealed prior snapshot.

## 6. Provenance model

The pipeline uses a NEXUS profile inspired by W3C PROV:

- Entity: source file, report, return, receipt, code object, experiment output, package snapshot.
- Activity: research, extraction, comparison, validation, synthesis, packaging, Cursor processing.
- Agent: Operator, AXIOM, Cursor/PRAXIS, QWEN, QWEN-CODER, GROK, MANUS, KIMI, platform/service.

Every derived finding should identify the activity and source entities that support it when feasible.

## 7. RO-Crate compatibility direction

Sealed snapshots may additionally emit `ro-crate-metadata.json`. NEXUS does not claim RO-Crate conformance unless the metadata passes the declared RO-Crate profile. The core NEXUS manifest remains authoritative for NEXUS lifecycle/governance semantics.

## 8. Fixity

Every sealed snapshot must include a complete `SHA256SUMS.txt` over files within the snapshot, analogous to BagIt/OCFL fixity discipline. A snapshot is `SEALED` only after all files are closed and checksums computed.

## 9. Immutability

Historical snapshots and event objects are immutable. A correction is a new event and, where needed, a new snapshot.

## 10. Automatic accumulation

AXIOM should append research items to the current active package when they are causally related and share a processing objective. Start a new package when at least one of these changes materially:

- research objective;
- phase/strand;
- intended Cursor processing mode;
- authority boundary;
- source confidentiality/publication class;
- package would become too heterogeneous for independent review.

## 11. Recommended bundle size

A package should generally represent a coherent research interval rather than a single message. Package size is bounded by reviewability, not by an arbitrary item count.

## 12. No silent completion

`PROCESSED` requires a Cursor terminal processing event or another explicitly authorized processor. AXIOM may prepare, seal and adjudicate research, but does not mark Cursor processing complete on Cursor's behalf.
