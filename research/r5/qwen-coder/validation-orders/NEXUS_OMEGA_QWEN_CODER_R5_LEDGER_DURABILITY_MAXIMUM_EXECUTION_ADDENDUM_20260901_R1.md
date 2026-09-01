# NEXUS OMEGA — QWEN-CODER R5 LEDGER DURABILITY MAXIMUM EXECUTION ADDENDUM

```text
OBJECT =
NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_MAXIMUM_EXECUTION_ADDENDUM_20260901_R1

STATE =
BINDING_CONTINUATION_OF_R0_INDEPENDENT_VALIDATION_ORDER

PARENT_ORDER =
NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_INDEPENDENT_VALIDATION_ORDER_20260901_R0

ROLE =
INDEPENDENT_TECHNICAL_VALIDATOR_AND_LOCAL_CANDIDATE_EXPERIMENTER

CLAIM_CEILING =
C1

CLAIM_PROMOTION =
FALSE

INTEGRATION_AUTHORITY =
NONE

PUBLIC_GITHUB_WRITE =
NO

AUTO_CONTINUE_WITHIN_THIS_ORDER =
YES

AUTO_FOLLOW_ON_BEYOND_THIS_ORDER =
NO

WORK_CONSERVING =
YES

BLOCKED_LANE_NOT_BLOCKED_SYSTEM =
ACTIVE

MAXIMUM_ORDER_DOCTRINE =
ACTIVE
```

---

# 1. Binding interpretation

This addendum strengthens execution semantics of the R0 order. It does not replace its scientific requirements.

A message such as:

```text
validation initiated
Gate 0 started
research underway
tests scheduled
next I will ...
```

is **not a terminal return**.

Once this order has started, continue autonomously through every lawful and technically executable phase until one of the explicit terminal states in Section 20 is reached.

Do not stop merely because one phase completed.

Do not request a new micro-order between Gate 0, semantic audit, baseline reproduction, candidate prototyping, fault injection, ranking, tie-break testing, or return persistence.

The intended execution chain is one continuous run:

```text
G0 PHYSICAL REHASH
→ G1 RETURN COMPLETENESS
→ G2 SOURCE / CLAIM AUDIT
→ G3 CURRENT NEXUS BASELINE REPRODUCTION
→ G4 CONTROL ARCHITECTURES
→ G5 TOP-8 CANDIDATE VALIDATION
→ G6 COMMON FAULT-INJECTION MATRIX
→ G7 COMPARATIVE SCORING
→ G8 TIE-BREAK / SENSITIVITY TESTS
→ G9 CANDIDATE IMPLEMENTATION RECOMMENDATION
→ G10 FINAL PERSISTENCE / SELF-REHASH
→ TERMINAL RETURN
```

---

# 2. Stop policy

Use risk-adaptive continuation.

```text
NONCRITICAL_GAP
→ RECORD
→ CONTINUE

ONE_CANDIDATE_BLOCKED
→ MARK NOT_COMPUTABLE / SOURCE_NOT_PRESENT / DEPENDENCY_UNAVAILABLE
→ CONTINUE ALL OTHER CANDIDATES

ONE_TEST_NOT_APPLICABLE
→ MARK NOT_APPLICABLE
→ CONTINUE

MATERIAL SOURCE IDENTITY FAILURE FOR QWEN RETURN
→ DO NOT VALIDATE THAT EXACT PRODUCER CLAIM
→ CONTINUE PUBLIC-SOURCE AUDIT + NEXUS BASELINE + INDEPENDENT EXPERIMENTS

PUBLIC WRITE / AUTHORITY / CLAIM-PROMOTION BOUNDARY
→ FAIL CLOSED FOR THAT ACTION ONLY
```

Never treat:

```text
BLOCKED_LANE = BLOCKED_SYSTEM
```

and never treat uncertainty as a global stop condition.

---

# 3. Gate 0 — physical return intake must execute, not merely start

Perform the complete independent measurement of the received final QWEN return family.

Producer-reported logical family:

```text
FILE_COUNT = 10
TOTAL_BYTES = 136693
```

Required logical files:

```text
RESEARCH_RETURN.md
OPEN_SOURCE_ARTIFACT_REGISTER.json
OPEN_RESEARCH_REGISTER.json
FAILURE_MODEL_MATRIX.json
ARCHITECTURE_COMPARISON.json
TOP8_SHORTLIST.json
QWEN_CODER_VALIDATION_HANDOFF.md
PRIMARY_SOURCE_REGISTER.json
RETURN_MANIFEST.json
SHA256SUMS.txt
```

Mandatory outputs:

```text
OUTER_OBJECT_PATH_OR_ID
OUTER_OBJECT_BYTES
OUTER_OBJECT_SHA256
FILE_COUNT_ACTUAL
TOTAL_LOGICAL_RETURN_BYTES_ACTUAL
EXTRA_FILES
MISSING_FILES
MANIFEST_PARSE
SHA256SUMS_PARSE
MANIFEST_VS_ACTUAL
SHA256SUMS_VS_ACTUAL
MANIFEST_VS_SHA256SUMS
G0_VERDICT
```

If a container contains unrelated workspace files, distinguish:

```text
OUTER_CONTAINER_CONTENT
vs
LOGICAL_QWEN_RETURN_FAMILY
```

Do not stop at G0_PASS. Continue immediately to G1–G10.

---

# 4. Gate 1 — structural/completeness audit

Independently verify:

- all ten required files are present;
- JSON files parse;
- Markdown files are nonempty and internally coherent;
- SHA256SUMS binds final files rather than stale predecessors;
- RETURN_MANIFEST binds all required final objects;
- filenames and object roles agree across manifest, SHA256SUMS and actual files;
- no duplicate logical object is silently substituted under another name;
- final source register exists and is referenced by the research narrative;
- timestamps/workspace identities are internally plausible.

Return explicit defect list even if nonterminal.

---

# 5. Gate 2 — source and claim audit

Audit every material source used to justify the Top-8.

For each high-impact claim classify:

```text
NORMATIVE_PRIMARY_SOURCE
UPSTREAM_IMPLEMENTATION
UPSTREAM_DOCUMENTATION
PEER_REVIEWED_OR_OPEN_ACCESS_RESEARCH
REPRODUCED_EXPERIMENT
STATIC_CODE_OBSERVATION
SECONDARY_SOURCE
INFERENCE
HYPOTHESIS
NOT_ESTABLISHED
```

At minimum independently validate the source basis for:

```text
SQLite WAL / synchronous FULL / NORMAL
Git update-ref expected-old OID and transaction semantics
Tessera sequencing/durable integration/ack semantics
LMDB writer serialization and durability flags
RocksDB WAL / WriteBatch / transactions / sync settings
single-writer service failure semantics
POSIX flock limitations
2PC prepare/commit/recovery requirements
WOLVES
PoWER
other research used materially in ranking
```

A source citation that exists but does not support the claimed mechanism counts as a source-binding defect.

---

# 6. Gate 3 — reproduce actual current NEXUS baseline

Against frozen base:

```text
MAIN = 93c306a8944ac0a0a10fc7803d8ea4ddfe01477d
TREE = 37cbb9d5b83b004b1da62863804a31d02c085183
```

Reproduce the current ledger behavior before candidate comparison.

Required base cases:

```text
B01 validate untouched ledger
B02 single append
B03 dual writers same predecessor/head
B04 triple writers same predecessor/head
B05 duplicate record_id race
B06 distinct record_id same successor race
B07 kill after object persistence
B08 kill after index persistence
B09 kill before latest/head persistence
B10 recovery/revalidation after each partial state
```

For concurrency cases use randomized jitter and enough trials to distinguish deterministic from probabilistic failure.

Minimum where executable:

```text
DUAL_WRITER_TRIALS >= 20
TRIPLE_WRITER_TRIALS >= 20
```

Record exact counts, seeds where practical, final ledger validity and observed lost-update/orphan/head-mismatch states.

---

# 7. Gate 4 — controls

Two mandatory controls:

```text
C0 = CURRENT NEXUS LEDGER
C1 = CURRENT NEXUS LEDGER + GLOBAL SAME-HOST POSIX WRITER LOCK
```

C1 lock scope must include:

```text
acquire
→ validate current state
→ read head/index
→ derive successor
→ write object
→ write index
→ write latest/head
→ post-validate
→ defined durability sync
→ release
```

Do not lock only the write calls.

Explicitly measure what C1 fixes and what remains:

```text
same-host concurrency
process death
cross-file crash state
orphan state
fsync/directory durability
multi-host/network-FS support
```

This control is essential: a complex architecture must demonstrate material benefit over the smallest plausible remediation.

---

# 8. Gate 5 — validate every Top-8 candidate

Candidate set:

```text
A1 SQLite WAL
A2 Immutable Object + CAS Head
A3 Immutable Object + Sequencer / Tessera-style
A4 LMDB
A5 Git-Native Ledger
A6 Single-Writer Service
A7 RocksDB + External Coordination
A8 Lock + Two-Phase Commit
```

Do not skip a candidate merely because another looks stronger.

For each candidate create a candidate evidence record containing:

```text
candidate_id
implementation_profile
upstream_version_or_commit
prototype_scope
executed_vs_source_only
writer_model
authoritative_commit_point
acknowledgment_point
durability_profile
recovery_algorithm
idempotency_model
unsupported_modes
trial_counts
failures
residual_risks
NEXUS_migration_cost
```

If full upstream execution is too heavy, implement the smallest mechanism-faithful prototype and separately classify upstream-system claims.

---

# 9. Gate 6 — normalized fault injection

Run the common fault model from R0 across every technically applicable candidate and both controls.

Minimum categories:

```text
CONCURRENCY
PROCESS_DEATH
POWER_LOSS_PROXY / DURABILITY_ORDERING
PARTIAL_WRITE
ENOSPC
STALE_HEAD
STALE_LOCK
DUPLICATE_REQUEST
REPLAY
RECOVERY_TWICE
ORPHAN_OBJECT
MISSING_OBJECT
HEAD_INDEX_DIVERGENCE
UNSUPPORTED_FILESYSTEM
MULTI_HOST_ATTEMPT
```

For executable candidate profiles, minimum intensity:

```text
DUAL_WRITER >= 20
TRIPLE_WRITER >= 20
RESTART_RECOVERY >= 20
REPLAY >= 20
```

These are trial counts, not assertion counts.

For each candidate × failure class return:

```text
PASS_EXPECTED
FAIL_EXPECTED_SAFE
FAIL_UNSAFE
NOT_APPLICABLE
NOT_COMPUTABLE
```

and preserve raw counts.

---

# 10. Candidate-specific maximum validation

## A1 SQLite

At minimum test separately:

```text
WAL + synchronous=FULL
WAL + synchronous=NORMAL
```

If external content-addressed object bytes remain outside the DB transaction, test:

```text
object-before-DB-commit crash
DB-commit-before-object-durability failure
orphan object
DB row/head references missing object
recovery reconciliation
```

Also test transactional expected-head predicate and unique record_id/idempotency.

## A2 Immutable + CAS

Build at least:

```text
A2a filesystem prototype
A2b Git expected-old-OID prototype
```

Required invariants:

```text
head references existing object
stale writer cannot overwrite winner
failed CAS preserves winner
crash before CAS preserves old head
crash after CAS leaves committed state recoverable
orphan is detectable
replay is safe
head cannot silently move backward
```

Test fsync/file/parent-directory ordering where applicable.

## A3 Sequencer

Explicitly distinguish:

```text
accepted
sequenced
durably integrated
checkpointed/witnessed
```

Test every acknowledgment boundary.

## A4 LMDB

Record exact durability/sync flags and test writer serialization, process death and replay.

## A5 Git-native

Test object write + fsync assumptions + update-ref CAS + reflog/recovery + fsck after termination.

Prefer one authoritative ref; separately test multi-ref visibility if used.

## A6 Single-writer service

Must test ambiguous client timeout:

```text
commit happened / response lost
client retries
```

plus service restart, duplicate active writer and failover fencing model.

## A7 RocksDB

Separate profiles:

```text
WriteBatch
transaction API
sync=true
sync=false
optimistic
pessimistic
```

Do not hide external coordinator correctness inside RocksDB score.

## A8 Lock + 2PC

Persist explicit:

```text
transaction id
expected predecessor
prepare
object identity
commit decision
recovery state
```

Inject failure after every transition.

---

# 11. Gate 7 — quantitative comparative scoring

Score all A1–A8 plus C0/C1 on at least these axes:

```text
S01 same-host concurrency safety
S02 stale-writer exclusion
S03 crash consistency
S04 acknowledged durability
S05 recovery determinism
S06 replay/idempotency
S07 partial-state containment
S08 orphan handling
S09 auditability
S10 NEXUS content-addressed fit
S11 implementation simplicity
S12 operational complexity
S13 dependency burden
S14 migration cost
S15 testability
S16 performance at current NEXUS scale
S17 multi-host extensibility
S18 upstream maturity
S19 portability
S20 failure observability
```

For every numeric score store a rationale and evidence type.

Do not use false precision. Ordinal scoring is acceptable if justified.

---

# 12. Gate 8 — tie-break and sensitivity analysis

A ranking is not final until sensitivity is tested.

Mandatory ranking views:

```text
R1_MINIMAL_NEXUS_SAME_HOST
R2_MAXIMUM_DURABILITY_SAME_HOST
R3_FUTURE_MULTIWRITER_EXTENSIBLE
R4_MINIMUM_CUSTOM_CORRECTNESS_LOGIC
R5_MAXIMUM_AUDITABILITY
```

Then vary weighting assumptions.

If winner changes materially under reasonable weights, return:

```text
NO_DOMINANT_WINNER
```

and recommend conditional architecture selection rather than forcing one global rank.

Perform direct tie-break experiments for top candidates when scores are close.

---

# 13. Gate 9 — implementation recommendation

Return at least:

```text
PRIMARY_RECOMMENDATION_CURRENT_NEXUS
SECONDARY_RECOMMENDATION_CURRENT_NEXUS
FUTURE_SCALE_RECOMMENDATION
REJECTED_OR_DEFERRED_CANDIDATES
```

The recommendation must specify an implementation contract, not merely a product name.

For example, if A2 wins, specify:

```text
immutable-object write procedure
byte verification
file fsync
parent-directory fsync if required
one authoritative head
expected-old CAS
winner/loser semantics
orphan policy
replay/idempotency key
startup recovery
validator invariants
migration path
```

If A1 wins, specify database schema/transaction boundary, synchronous mode, external object handling and migration.

---

# 14. Local candidate implementation

Unless all candidate execution is blocked, produce at least one local implementation-grade candidate or patch for the strongest current-NEXUS recommendation.

Requirements:

```text
NO PUBLIC WRITE
NO MAIN MUTATION
LOCAL/EPHEMERAL ONLY
PATCH OR SOURCE FILES PERSISTED IN RETURN
TESTS PERSISTED IN RETURN
EXACT BASE COMMIT RECORDED
```

Prefer a small auditable patch over a broad rewrite.

Do not call it integrated.

---

# 15. Validation harness quality

The harness itself must be tested.

Include at minimum:

```text
known-good fixture
one deliberately broken implementation per key invariant where feasible
fault injector smoke test
seed reproducibility check
negative test proving harness detects lost update
negative test proving harness detects head→missing-object state
negative test proving replay defect is detected
```

A harness that never produces a failure is not sufficient evidence.

---

# 16. Performance and operational measurements

This is not a performance competition, but measure enough to rule out absurd operational cost.

At minimum for locally executed finalists:

```text
single append latency
20-writer burst completion time or supported equivalent
recovery time after injected crash
storage growth per append
custom code surface / changed LOC estimate
dependency count delta
```

Use current NEXUS scale as the primary performance context.

---

# 17. Security and abuse cases

Test/model at minimum:

```text
malicious stale writer
replay flood
record_id collision
path/object substitution
head rollback attempt
lock-file poisoning/stale lock
corrupted WAL/journal/head
untrusted recovery input
symlink/path traversal where filesystem paths are constructed
```

Do not broaden this into a general security audit unrelated to the ledger commit mechanism.

---

# 18. Required terminal return family

Persist at minimum:

```text
01_GATE0_PHYSICAL_REHASH.json
02_QWEN_RETURN_SOURCE_AUDIT.json
03_BASELINE_REPRODUCTION.json
04_CONTROL_RESULTS.json
05_CANDIDATE_RESULTS.json
06_FAULT_MATRIX.json
07_TRIAL_LOG_SUMMARY.json
08_ARCHITECTURE_SCORES.json
09_RANKINGS_AND_SENSITIVITY.json
10_FINAL_RECOMMENDATION.md
11_LOCAL_CANDIDATE_PATCH.diff
12_LOCAL_CANDIDATE_TESTS.md
13_VALIDATION_HARNESS_DESCRIPTION.md
14_PRIMARY_SOURCE_REGISTER.json
15_QWEN_CODER_RETURN_MANIFEST.json
16_SHA256SUMS.txt
```

If a logically required file is not applicable, preserve a small explicit NOT_APPLICABLE artifact rather than silently omitting it.

For each deliverable:

```text
WRITE
→ CLOSE
→ READ BACK
→ BYTE COUNT
→ SHA256
→ VERIFY EXISTS
```

Generate `16_SHA256SUMS.txt` only after all other final return objects are closed.

Then read back and rehash `16_SHA256SUMS.txt` itself and record that hash in the terminal message/manifest without recursively inserting it into itself.

---

# 19. Required terminal message

Do not end with "work started".

Return a compact terminal summary containing:

```text
RUN_STATE
FROZEN_BASE
QWEN_RETURN_G0_VERDICT
QWEN_RETURN_ACTUAL_FILE_COUNT
QWEN_RETURN_ACTUAL_TOTAL_BYTES
BASELINE_RACE_REPRODUCED = YES|NO|PARTIAL
CONTROL_C1_RESULT
TOP_CURRENT_NEXUS_CANDIDATE
TOP_FUTURE_CANDIDATE
NO_DOMINANT_WINNER = YES|NO
LOCAL_CANDIDATE_IMPLEMENTED = YES|NO
TOTAL_FAULT_CASES_EXECUTED
TOTAL_TRIALS_EXECUTED
UNRESOLVED_MATERIAL_CAVEATS
RETURN_FILE_COUNT
RETURN_TOTAL_BYTES
RETURN_MANIFEST_SHA256
SHA256SUMS_SHA256
PUBLIC_WRITE = NO
CLAIM_PROMOTION = FALSE
INDEPENDENT_VALIDATION = COMPLETED|PARTIAL
```

---

# 20. Allowed terminal states

Only these states terminate the order:

```text
T1_COMPLETE_INDEPENDENT_VALIDATION_WITH_RECOMMENDATION_C1

T2_COMPLETE_INDEPENDENT_VALIDATION_NO_DOMINANT_WINNER_C1

T3_PARTIAL_VALIDATION_WITH_MATERIAL_BLOCKED_CANDIDATES_C1
    # only after all unblocked lanes are exhausted

T4_GATE0_SOURCE_OBJECT_FAILURE_BUT_INDEPENDENT_BASELINE_AND_PUBLIC_SOURCE_VALIDATION_COMPLETED_C1

T5_GLOBAL_EXECUTION_BLOCKED_NO_VALIDATION_POSSIBLE
    # only if the environment prevents essentially all meaningful lanes
```

The following are explicitly **nonterminal**:

```text
INITIATED
STARTED
GATE_0_RUNNING
GATE_0_PASS
SOURCES_REVIEWED
BASELINE_REPRODUCED
CANDIDATE_TESTS_STARTED
WAITING_FOR_NEXT_INSTRUCTION
```

---

# 21. Handoff boundary

After a terminal state, stop before public integration.

The next authority remains:

```text
QWEN-CODER TERMINAL RETURN
→ AXIOM ADJUDICATION
→ SHARED RESEARCH PIPELINE PACKAGE
→ CURSOR/PRAXIS FOUR-EYES IMPLEMENTATION / VM VALIDATION
```

No self-promotion to Cursor-ready integrated state is allowed.

---

# 22. Permanent execution principle for this run

```text
MAXIMUM_ORDER =
ALL_LAWFUL_INDEPENDENT_WORK_UNTIL_TRUE_TERMINAL_GATE

MICRO_STOP_AFTER_PHASE =
PROHIBITED

UNCERTAINTY =
RECORD_AND_CONTINUE_WHERE_REVERSIBLE

BLOCKED_LANE =
NOT_BLOCKED_SYSTEM

PRODUCER_CLAIM =
NOT_VALIDATION_RESULT

HASH_MATCH =
NOT_SCIENTIFIC_TRUTH

CI_PASS =
NOT_CLAIM_PROMOTION
```

Execute the entire R0 + R1 scope as one continuous independent validation assignment.