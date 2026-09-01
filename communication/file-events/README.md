# NEXUS OMEGA File Event Ledger

This is the append-only provenance archive for substantive agent file transactions.

```text
objects/sha256/<aa>/<bb>/<digest>/event.json
index/v1/events.jsonl
index/v1/latest.json
```

The event object is authoritative for the recorded transaction; the index/head are derived discovery metadata.

A file event records who changed what, when, under which task/admission/capability context, and the before/after raw-byte SHA-256 identities. Git commit and PR identities are supplementary platform locators.

The ledger does not make the underlying change scientifically correct.

```text
FILE_EVENT_PRESENT != CHANGE_VALID
GIT_COMMIT_PRESENT != AGENT_IDENTITY_COMPLETE
HASH_MATCH != SEMANTIC_VALIDITY
```

Ledger-internal object/index/head writes are deterministic `LEDGER_DERIVED_METADATA` and terminate recursive self-logging. All other agent-authored repository mutations remain in scope.
