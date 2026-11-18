# R35 collective experience memory | bounded, typed, append-only
OBJECT = NEXUS_OMEGA_AXIOM_R35_COLLECTIVE_EXPERIENCE_LEDGER_BLUEPRINT_20261118_R0
STATE = DESIGN_ONLY_NO_RUNTIME_BENCHMARK
PRIORITY = SUPPORT_OPPO_BODYTWIN_NOT_REPLACE_LAB
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
DEFAULT_DISCLOSURE = PRIVATE_UNTIL_PUBLIC_SAFE_REVIEWED

## Problem
R31-R34 reports, counterexamples, experiment constraints and failed assumptions are dispersed across PR/ZIP/Markdown. Repeated semantic hunts consume context, invite wrong source substitution and confound producer-reported with independently replayed evidence. The proposed memory is an evidence-indexed working corpus, not autonomous epistemic truth, neural consciousness or a replacement for original scientific data.

## Three-layer candidate architecture
1. Immutable source receipts: original artefact bytes stored in their authorized public or private custody store; canonical SHA256 from original bytes, storage domain, source timestamps and read permissions. No hidden data copied to public Git.
2. Append-only EVENT LEDGER: strictly typed events keyed by stable record_id, gate_id, parent_source_sha256, object_id, evidence_class, adjudication_id, confidence=NOT_NUMERIC, status, visibility, supersedes, discovered_at_utc, event_hash, artifact_ref, counterexample_fixture_ref, rollback_ref. Explicit separate public and private indexes.
3. Derived SNAPSHOT and bounded EXACT LOOKUP INDEX: materialized map by record_id, by gate_id, by (program, topic), by original sha256, immutable generation marker; rebuild deterministically from manifest and hash-check. Derived cache may be thrown away and rebuilt; ledger is authoritative only for provenance, not scientific truth. Signed AXIOM/owner authority required to mark ADJUDICATED. Public collection accepts only public-safe redacted pointers.

## Retrieval contract
Tier 0: exact record_id/gate_id/sha256. Maximum 1 snapshot read and bounded constant-time index probes (design target, not measured). Return provenance, evidence class, open gates and short summary plus original pointer.
Tier 1: controlled keyword lookup ONLY against allowlisted enumerated topical tags, fixed inverted index, max 8 tags, 2 index probes, 20 candidate IDs, 8 final results, one fixed nonrecursive scan, <=16 KiB response. No free text recursive expansion, LLM-to-LLM memory search, automatic web fallback or re-query amplification.
Tier 2: explicit SOURCE_GAP if no match; a human/AXIOM-directed source census is a separately authorized task, not an infinite search loop.
Hard budgets (initial, to benchmark): 3 logical reads, 2 index probes, 20 candidates, max 8 returns, 16KiB serialized response; 50ms local read target on reference machine, NOT MEASURED. Reject stale snapshot or unknown schema, do not silently downgrade evidence class.
The phrase 'one query' is NOT an empirical guarantee; measure full latency/coverage with synthetic corpus sizes 100, 1000 and 10000, cold/warm and adversarial input.

## Write and source governance
Only an AXIOM/Operator adjudicated receipt is eligible for ADJUDICATED append. External agents submit PROPOSED evidence into quarantine/staging with identity SELF_DECLARED_UNVERIFIED. Independent critic assesses original bytes; append transaction requires stable digest, versioned schema, no privacy/secret leakage, monotonic sequence and optimistic concurrency lock. No agent may rewrite entries or delete a contradicting old event. REVOKED, SUPERSEDED or CORRECTED is an appended next event with reason and pointer.
Rolling C1 latest snapshot contains distinct REPORT_ONLY / ORIGINAL_HASH_MATCH / SOURCE_REPLAYED / FORMAL_PROOF_REPLAYED / PHYSICAL_REFERENCE_VALIDATED and NOT_RUN; source integrity not author signature. A failed check remains retrievable as NEGATIVE_EVIDENCE.

## Falsifiers
MEM01: poisoned external abstract cannot overwrite C1 HOLD or valid source SHA.
MEM02: private OPPO raw file reference cannot appear in public payload, log, index key, search result or exception message.
MEM03: stale snapshot/hash tamper rejects with fail-closed, never falls back to unverified free-text guess.
MEM04: contradiction chain A -> correction B -> reversal C returns all versions; no last-write-wins false memory.
MEM05: duplicate keys, NaN, noncanonical source ID, unicode collision, path traversal, symlink and nested JSON bombs reject before indexing.
MEM06: search budget enforced under high entropy query, cyclic supersedes and denial-of-service input.
MEM07: independent source replay of 100 sampled entries has no false ADJUDICATED label.
MEM08: ablation A=normal corpus, B=no memory, C=free search, D=bounded typed index; preregister error recurrence, retrieval precision, latency, privacy leakage and source-discrepancy correction; improvement is HYPOTHESIS until tested.

## Competing architectures welcome
A strict SQLite relational ledger with transaction log and immutable CAS can beat JSON in high volume; JSONL plus generated indexes may be simpler offline. A selective graph-based evidence DAG can aid contradiction tracking; mandatory traversal budget required. An embedding search may be proposed only for offline discovery in isolated candidate staging, NEVER as production authority or unlimited recursive search. Experts must independently compare, including memoryless baseline.

## Causal purpose
Rapidly retrieve 'what we already disproved', not an ever-expanding unverified recollection. Any automated framework improvement from this ledger is only PROPOSED until source, negative, rollback, independent regression and scoped operator authorization complete.
