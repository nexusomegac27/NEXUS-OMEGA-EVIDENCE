# NEXUS OMEGA R5 — Ledger concurrency and crash-consistency analysis

```text
OBJECT = NEXUS_OMEGA_R5_AXIOM_LEDGER_CONCURRENCY_CRASH_ANALYSIS_20260831_R0
STATE = STATIC_CODE_ANALYSIS_C1
BASE_MAIN = 5bebbe6775695dbe8028cfe7fb72ff30065ddd42
CLAIM_CEILING = C1
IMPLEMENTATION_CHANGE = NO
```

## Scope

This analysis is based on the current `scripts/append_scientific_record.py` and `scripts/validate_scientific_ledger.py` on `main@5bebbe6775695dbe8028cfe7fb72ff30065ddd42`.

## Current transaction shape

The current append writer performs, conceptually:

```text
READ_SOURCE
→ SEMANTIC_VALIDATE_SOURCE
→ VALIDATE_CURRENT_LEDGER
→ READ_INDEX_AND_HEAD
→ DERIVE_SEQUENCE_AND_PREVIOUS_HASH
→ DERIVE_OBJECT_PATH
→ WRITE_OBJECT_ATOMICALLY
→ WRITE_INDEX_ATOMICALLY
→ WRITE_LATEST_ATOMICALLY
→ POST_VALIDATE_LEDGER
```

Each file replacement is individually atomic through a temporary file + `os.replace`, with flush/fsync on the temporary file before replacement.

## Finding L1 — no writer serialization / CAS

No repository-visible cross-process lock, compare-and-swap token, transaction generation, or equivalent writer serialization is present around the complete read/derive/write sequence.

Therefore two writers operating on the same filesystem can both:

1. validate the same current head;
2. read the same existing index;
3. derive the same next sequence number and previous index-line hash;
4. independently construct competing next index/head states;
5. interleave their individually atomic file replacements.

This is a structural race possibility. Exact empirical frequency is **not established by this static analysis**.

```text
FINDING = LEDGER_MULTIWRITER_SERIALIZATION_NOT_ESTABLISHED
SEVERITY = MATERIAL_IMPLEMENTATION_GAP
EVIDENCE_CLASS = STATIC_CODE_ANALYSIS
```

## Finding L2 — multi-file atomicity is not established

`record.json`, `records.jsonl`, and `latest.json` are replaced in separate operations. A process crash, host crash, abrupt termination, filesystem error, or storage failure between replacements can leave a partially advanced transaction.

Examples include:

```text
OBJECT_WRITTEN / INDEX_OLD / LATEST_OLD
OBJECT_WRITTEN / INDEX_NEW / LATEST_OLD
```

The validator can detect some resulting inconsistencies, including orphan objects and head mismatches. Detection after the fact is valuable but is not equivalent to transaction atomicity.

```text
FINDING = MULTI_FILE_TRANSACTION_ATOMICITY_NOT_ESTABLISHED
RECOVERY = DETECTION_PRESENT; AUTOMATIC_RECOVERY_PROTOCOL_NOT_ESTABLISHED
```

## Finding L3 — directory durability boundary is unspecified

The writer fsyncs temporary file contents before `os.replace`, but the current implementation does not visibly fsync the containing directories after renames. Exact crash-durability guarantees therefore depend on filesystem/OS semantics and are not explicitly established by the implementation profile.

```text
FINDING = DIRECTORY_ENTRY_DURABILITY_PROFILE_NOT_ESTABLISHED
```

This is not a claim that the current implementation necessarily loses data under ordinary operation.

## Candidate same-host remediation profile

For a **single-host, shared POSIX-filesystem** implementation, the minimum candidate critical section is:

```text
LOCK_ACQUIRE
→ REVALIDATE_CURRENT_LEDGER
→ READ_HEAD_AND_INDEX
→ DERIVE_NEXT_STATE
→ WRITE_OBJECT
→ WRITE_INDEX
→ WRITE_LATEST
→ POST_VALIDATE
→ DURABILITY_SYNC_AS_DEFINED
→ LOCK_RELEASE
```

The lock must cover revalidation and all state derivation, not merely the writes.

A lock-file design based on `fcntl.flock` may establish process serialization on supported local POSIX filesystems, but that claim must remain scoped. It must **not** be generalized to distributed filesystems, multi-host writers, cloud object stores, or network filesystems without separate evidence.

## Stronger future profile

A stronger ledger implementation could introduce a version/generation token or CAS-style commit protocol with an immutable transaction/journal object. Candidate goals:

- explicit expected predecessor/head identity;
- one durable transaction identity;
- replay/idempotence detection;
- crash-recovery procedure;
- orphan transaction discovery;
- no silent lost update;
- deterministic recovery to either predecessor or one committed successor;
- optional multi-host backend with backend-specific concurrency semantics.

## Required empirical tests before stable adoption

At minimum:

1. repeated dual-writer append trials from identical head;
2. repeated triple-writer trials;
3. duplicate `record_id` contention;
4. distinct records with same starting head;
5. forced termination after object write;
6. forced termination after index write;
7. forced termination before latest write;
8. recovery/retry after partial transaction;
9. idempotent replay behavior;
10. unsupported/non-POSIX environment fail-closed behavior for any POSIX-lock implementation.

## Boundary

No code is changed by this document. It does not claim an empirical race reproduction on the current `main`; it establishes that serialization and cross-file transaction atomicity are not guaranteed by the visible implementation structure.
