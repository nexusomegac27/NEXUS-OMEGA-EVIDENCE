# NEXUS OMEGA Canonical File Event Archive V1

```text
OBJECT = NEXUS_OMEGA_CANONICAL_FILE_EVENT_ARCHIVE_V1
STATE = IMPLEMENTATION_CANDIDATE
CLAIM_CEILING = C1
```

## Requirement

Every substantive create, modify, delete, move, copy, restore or generated-file action performed by an agent must be reconstructible.

Each event records at minimum:

- actor type, role, provider, model and session/admission identifiers;
- task/order identity and order SHA-256 when known;
- operation;
- path before and/or after;
- file role/class;
- raw-byte size and SHA-256 before and after;
- reason;
- timestamp in UTC;
- Git repository/base/result commit and PR when applicable;
- validation/independence state.

## Storage

```text
communication/file-events/
├── objects/sha256/<aa>/<bb>/<digest>/event.json
├── index/v1/events.jsonl
└── index/v1/latest.json
```

Event objects are immutable exact UTF-8 JSON bytes. The index is a discovery/hash-chain layer and does not replace the event objects.

## Recursion termination

A ledger append necessarily changes ledger bookkeeping. Those deterministic object/index/head writes are `LEDGER_DERIVED_METADATA` and do not recursively require another per-file event. The event object itself is the canonical record of the substantive transaction.

This exemption is narrow. It does not apply to schemas, scripts, tests, research returns, source artifacts, governance files or other agent-produced content.

## Commit audit pattern

Preferred repository pattern:

```text
COMMIT_A = substantive agent changes
COMMIT_B = append-only file-event audit for COMMIT_A
```

CI validates that each non-ledger changed path in `COMMIT_A` has an event whose `git.result_commit` equals `COMMIT_A` and whose before/after identity matches the repository state.

## Boundaries

```text
GIT_HISTORY != COMPLETE_AGENT_IDENTITY
FILE_EVENT_LEDGER != SCIENTIFIC_TRUTH
HASH_MATCH != SEMANTIC_VALIDITY
DELETE_EVENT != AUTHORITY_TO_DELETE
```

Corrections are new events. Historical event objects are never silently rewritten.
