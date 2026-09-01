# NEXUS OMEGA — QWEN-CODER R5 LEDGER DURABILITY INDEPENDENT VALIDATION ORDER

```text
OBJECT =
NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_INDEPENDENT_VALIDATION_ORDER_20260901_R0

STATE =
AUTHORIZED_INDEPENDENT_VALIDATION_RUN

FROM =
OPERATOR_ALEXANDER_VIA_AXIOM

TO =
QWEN-CODER

ROLE =
INDEPENDENT_TECHNICAL_VALIDATOR_AND_LOCAL_CANDIDATE_EXPERIMENTER

CLAIM =
C1_DESCRIPTIVE_ONLY

CLAIM_CEILING =
C1

CLAIM_PROMOTION =
FALSE

INTEGRATION_AUTHORITY =
NONE

PUBLIC_GITHUB_WRITE =
NO

PUSH =
NO

PR_CREATE =
NO

MERGE =
NO

MAIN_MUTATION =
NO

RULESET_MUTATION =
NO

RELEASE =
NO

TAG =
NO

ATTESTATION_PUBLICATION =
NO

AUTO_FOLLOW_ON =
NO

WORK_CONSERVING =
YES

BLOCKED_LANE_NOT_BLOCKED_SYSTEM =
ACTIVE
```

---

# 1. Mission

Independently validate the fresh QWEN R5 Ledger Durability Research Return and experimentally falsify its selected architecture candidates against the actual NEXUS OMEGA communication-ledger problem.

This is **not** a confirmation exercise.

Your job is to attempt to break the producer's conclusions and determine which mechanisms survive independent reproduction.

Primary scientific problem:

```text
CURRENT NEXUS COMMUNICATION LEDGER

READ HEAD / INDEX
→ DERIVE NEXT SEQUENCE
→ WRITE CONTENT-ADDRESSED OBJECT
→ WRITE INDEX
→ WRITE LATEST/HEAD

KNOWN GAP FAMILY =
MULTIWRITER SERIALIZATION
+ EXPECTED-HEAD / CAS
+ CROSS-FILE ATOMICITY
+ CRASH CONSISTENCY
+ DURABILITY ORDERING
+ RECOVERY / REPLAY
+ ORPHAN / PARTIAL-TRANSACTION HANDLING
```

The output of this run must identify the strongest implementation path(s), but it must not integrate or publish them.

---

# 2. Frozen public NEXUS baseline

Repository:

`nexusomegac27/NEXUS-OMEGA-EVIDENCE`

Frozen validation base:

```text
MAIN =
93c306a8944ac0a0a10fc7803d8ea4ddfe01477d

TREE =
37cbb9d5b83b004b1da62863804a31d02c085183

PARENT =
5bebbe6775695dbe8028cfe7fb72ff30065ddd42
```

The base commit is GitHub-verified/signed.

The current active `main-evidence-protection` ruleset remains a platform/governance fact, not an implementation correctness proof.

Do not silently switch to a newer repository state if `main` moves during the run.

Record:

```text
LIVE_MAIN_AT_START =
FROZEN_BASE_MATCH = YES|NO
LIVE_MAIN_DRIFT =
```

If live `main` differs, preserve both identities and continue against the frozen validation base unless the difference is required to reproduce a specific current behavior.

---

# 3. QWEN producer return expected for this run

The operator will provide the complete fresh QWEN Ledger Durability return package separately from this GitHub order.

Producer reports final return family:

```text
FILE_COUNT = 10
TOTAL_REPORTED_BYTES = 136693
```

Expected logical family includes at minimum:

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

The producer previously reported eight core files and then performed a surgical completeness remediation adding:

```text
PRIMARY_SOURCE_REGISTER.json
RETURN_MANIFEST.json
```

Do not trust producer byte counts or producer hashes merely because the package says they match.

---

# 4. Gate 0 — independent physical intake and rehash

This is mandatory before semantic validation.

For the exact received package/container:

```text
IDENTIFY OUTER TRANSPORT OBJECT
→ COMPUTE OUTER BYTES
→ COMPUTE OUTER SHA256
→ EXTRACT WITHOUT MUTATING SOURCE
→ ENUMERATE FILES
→ VERIFY REQUIRED FILE FAMILY
→ READ EACH FILE AS BYTES
→ COMPUTE EACH BYTE COUNT
→ COMPUTE EACH SHA256
→ PARSE RETURN_MANIFEST.json
→ PARSE SHA256SUMS.txt
→ COMPARE PRODUCER DECLARATIONS TO INDEPENDENT MEASUREMENTS
```

Return explicit classifications:

```text
OUTER_OBJECT_BYTES =
OUTER_OBJECT_SHA256 =
FILE_COUNT_ACTUAL =
TOTAL_RETURN_BYTES_ACTUAL =
REQUIRED_FILE_COUNT = 10
MANIFEST_PARSE = PASS|FAIL
SHA256SUMS_PARSE = PASS|FAIL
MANIFEST_VS_ACTUAL = MATCH|MISMATCH
SHA256SUMS_VS_ACTUAL = MATCH|MISMATCH
MANIFEST_VS_SHA256SUMS = MATCH|MISMATCH
```

Do not count directory entries, Git metadata, editor metadata, caches or unrelated workspace files as return deliverables unless the manifest explicitly binds them.

If the package contains more than the ten logical return files, classify the extras rather than discarding them.

Gate-0 terminal states:

```text
G0_PASS_EXACT
G0_PASS_WITH_NONMATERIAL_EXTRAS
G0_FAIL_MISSING_REQUIRED_FILE
G0_FAIL_BYTES_MISMATCH
G0_FAIL_DIGEST_MISMATCH
G0_FAIL_MANIFEST_CONTRADICTION
G0_FAIL_SOURCE_OBJECT_AMBIGUITY
```

Only `G0_PASS_EXACT` or a justified `G0_PASS_WITH_NONMATERIAL_EXTRAS` permits full producer-return semantic adjudication.

If Gate 0 fails, continue independent public-source and NEXUS-baseline experiments where possible, but do not claim validation of QWEN's exact return.

---

# 5. Independence boundary

QWEN-CODER must remain independent from QWEN producer conclusions.

```text
QWEN = PRODUCER
QWEN-CODER = INDEPENDENT_VALIDATOR
```

Never use:

```text
QWEN_SAYS_PASS
→ QWEN_CODER_PASS
```

For every major conclusion classify evidence as one of:

```text
FACT_FROM_PHYSICAL_BYTES
FACT_FROM_PUBLIC_GITHUB
FACT_FROM_NORMATIVE_PRIMARY_SOURCE
FACT_FROM_UPSTREAM_IMPLEMENTATION
EXPERIMENTAL_RESULT
STATIC_CODE_ANALYSIS
INFERENCE
HYPOTHESIS
NOT_ESTABLISHED
NOT_COMPUTABLE
```

---

# 6. Producer Top-8 candidate set

QWEN reported these eight candidates:

```text
A1 SQLite WAL Mode
A2 Immutable Object + CAS Head
A3 Immutable Object + Sequencer / Tessera-style
A4 LMDB
A5 Git-Native Ledger
A6 Single-Writer Service
A7 RocksDB + External Coordination
A8 Lock + Two-Phase Commit
```

The producer ranking is a hypothesis.

Do not preserve the order unless your independent tests support it.

You may:

```text
REORDER
MERGE DUPLICATE MECHANISMS
SPLIT A CANDIDATE INTO CONFIGURATION PROFILES
REJECT A CANDIDATE
ADD A CONTROL ARCHITECTURE
```

but retain traceability back to A1–A8.

---

# 7. AXIOM pre-validation corrections that must be tested

AXIOM independently spot-checked the architecture direction and established the following **candidate corrections**, which are themselves subject to your validation:

## 7.1 SQLite

Do not test merely "SQLite WAL" as one undifferentiated system.

At minimum separate:

```text
SQLITE_WAL_SYNCHRONOUS_FULL
SQLITE_WAL_SYNCHRONOUS_NORMAL
```

Test whether acknowledged transactions survive the tested failure model.

A SQLite transaction only closes NEXUS cross-file atomicity if the authoritative state actually belongs to the same database transaction boundary.

If content-addressed payload files remain outside SQLite, test that boundary explicitly.

## 7.2 Immutable Object + CAS Head

Preferred mechanism to attack:

```text
WRITE IMMUTABLE OBJECT
→ DURABLY PERSIST OBJECT
→ CAS ONE AUTHORITATIVE HEAD FROM EXPECTED_OLD_TO_NEW
```

Do not assume object persistence and head publication form one atomic operation.

Test orphan-object recovery and crash points between those operations.

Prefer one authoritative head over multiple semantically meaningful refs unless a multi-ref protocol is independently justified.

## 7.3 Tessera-style sequencing

Distinguish:

```text
ENTRY_ACCEPTED_IN_MEMORY
ENTRY_ASSIGNED_DURABLE_SEQUENCE
ENTRY_COMMITTED_TO_APPEND_ONLY_LOG
```

Test process death before and after durable sequencing.

## 7.4 Network/multi-host semantics

Do not use the blanket statement:

```text
NFS_IS_PROBLEMATIC_FOR_MOST_APPROACHES
```

Instead return backend-specific states:

```text
SAME_HOST_LOCAL_FS =
MULTI_PROCESS_SAME_HOST =
MULTI_HOST_SHARED_FS =
NETWORK_FS =
OBJECT_STORE =
```

Unsupported environments are legitimate exclusions if explicit.

---

# 8. Actual NEXUS implementation to reproduce

Inspect the frozen base implementation, especially:

```text
scripts/append_scientific_record.py
scripts/validate_scientific_ledger.py
communication/index/v1/records.jsonl
communication/index/v1/latest.json
communication/objects/sha256/...
```

First reproduce the current single-writer happy path.

Then independently reproduce or refute the known multiwriter weakness.

Minimum base experiments:

```text
B01_CURRENT_LEDGER_VALID
B02_SINGLE_APPEND_VALID
B03_DUAL_WRITER_SAME_HEAD
B04_TRIPLE_WRITER_SAME_HEAD
B05_DUPLICATE_RECORD_ID_RACE
B06_DISTINCT_RECORD_IDS_SAME_HEAD
```

Do not infer concurrency failure from static code alone if you can execute it.

Record exact trial counts and residual ledger validity.

---

# 9. Common fault model

Every viable candidate must be tested against the same normalized failure model where technically applicable.

At minimum:

```text
F01 two concurrent writers
F02 three concurrent writers
F03 writers begin from identical expected head
F04 duplicate record_id contention
F05 distinct records competing for same successor
F06 process death before durable payload persistence
F07 process death after payload persistence but before authoritative commit
F08 process death during authoritative commit
F09 process death immediately after commit acknowledgment
F10 crash during recovery
F11 recovery executed twice
F12 replay of identical append request
F13 stale expected head / CAS conflict
F14 stale lock
F15 abandoned lock owner / process death
F16 ENOSPC before commit
F17 ENOSPC during metadata/index/head publication
F18 partial/truncated write
F19 corrupted authoritative head
F20 orphan immutable object
F21 head references missing object
F22 index/head disagreement
F23 reordered durability operations
F24 directory metadata durability boundary where applicable
F25 abrupt worker termination under load
F26 repeated restart/recovery cycles
F27 unsupported/network filesystem mode
F28 multi-host writer attempt where candidate claims support
```

For each candidate/failure pair classify:

```text
PASS_EXPECTED
FAIL_EXPECTED_SAFE
FAIL_UNSAFE
NOT_APPLICABLE
NOT_COMPUTABLE
```

A rejected operation is not a failure if the architecture explicitly does not support that mode and fails safely.

---

# 10. Required experimental intensity

At minimum, for candidates that can be locally prototyped without excessive dependency burden:

```text
DUAL_WRITER_TRIALS >= 20
TRIPLE_WRITER_TRIALS >= 20
RESTART_RECOVERY_TRIALS >= 20
REPLAY_TRIALS >= 20
```

Use randomized jitter/seeds where useful.

Record seeds when deterministic reproduction is possible.

Do not inflate counts by counting assertions as independent trials.

For heavyweight candidates such as Tessera or RocksDB, if full executable setup is unavailable, distinguish:

```text
UPSTREAM_MECHANISM_VERIFIED
LOCAL_PROTOTYPE_EXECUTED
FULL_SYSTEM_EXECUTED
```

Do not convert source inspection into an executed-system PASS.

---

# 11. Candidate A1 — SQLite WAL validation

Build the smallest honest prototype that represents the NEXUS authoritative state.

Minimum questions:

```text
Q1 Is one writer enforced under contention?
Q2 What exactly is the acknowledged commit point?
Q3 What changes under synchronous=FULL vs NORMAL?
Q4 What happens if process dies during WAL append?
Q5 What happens during checkpoint interruption?
Q6 Can replay be made idempotent using record_id uniqueness?
Q7 Can expected-head semantics be represented transactionally?
Q8 If payload remains external, how is DB-to-object consistency recovered?
Q9 Can orphan external objects be detected/reclaimed safely?
Q10 What is the same-host multi-process behavior?
```

Do not call SQLite "cross-file atomic" unless your prototype puts all authoritative state inside the same transaction boundary or supplies a separately validated recovery protocol for external objects.

---

# 12. Candidate A2 — Immutable Object + CAS Head

Build a minimal prototype using immutable object storage and exactly one authoritative expected-head update.

Required invariants:

```text
I1 committed head always identifies an existing valid object
I2 stale expected head cannot overwrite a newer head
I3 failed CAS never destroys winning state
I4 orphan object does not become committed state
I5 replay is idempotent or safely rejected
I6 crash before CAS leaves old head authoritative
I7 crash after successful CAS leaves new head recoverable
I8 head update cannot silently move backwards
```

Test at least two implementations if practical:

```text
A2a local filesystem atomic-head/CAS prototype
A2b Git ref expected-old-OID prototype
```

For Git, separately record:

```text
single-ref semantics
multi-ref transaction semantics
reader visibility behavior
reflog/recovery behavior
object durability assumptions
```

---

# 13. Candidate A3 — Sequenced append-only log

Validate the conceptual split:

```text
admission
→ sequencing/index assignment
→ durable integration
→ checkpoint/head publication
```

Determine exactly when an acknowledgment may be safely returned.

If Tessera itself can be executed, report exact version/commit and storage backend.

If not, build a small sequencer prototype and keep Tessera conclusions at upstream-source level.

Required tests:

```text
pre-sequence crash
post-sequence crash
concurrent submit
sequence uniqueness
restart
replay
partial batch
witness/checkpoint lag if modeled
```

---

# 14. Candidate A4 — LMDB

Test:

```text
single-writer serialization
concurrent readers
multi-process same-host
commit durability configuration
process death during write transaction
recovery after process death
replay/idempotency
expected-head representation
```

Document all sync flags/options that materially change durability.

Do not generalize beyond supported filesystem/platform semantics.

---

# 15. Candidate A5 — Git-native ledger

Model the ledger using immutable Git objects plus one authoritative ref where possible.

Test:

```text
update-ref expected-old OID
concurrent update-ref writers
single-ref CAS conflict
crash around object creation and ref update
orphan Git object
reflog recovery
repository fsck after forced termination
```

Do not equate Git object integrity with application scientific validity.

---

# 16. Candidate A6 — Single-writer service

A single writer eliminates one local race class but introduces service-level failure modes.

Test/model:

```text
idempotent request key
client retry after ambiguous timeout
writer crash before commit
writer crash after commit before reply
restart/replay
queue durability
failover fencing
second active writer accidental startup
```

A single process without durable request semantics is not a complete solution.

---

# 17. Candidate A7 — RocksDB + coordination

Separate:

```text
RocksDB local transaction guarantees
external coordination/fencing guarantees
```

Test/write down exact settings:

```text
WAL enabled/disabled
sync true/false
WriteBatch vs transaction API
optimistic vs pessimistic transaction
conflict detection
recovery after kill
```

If an external coordinator is required, its correctness belongs to the architecture and must not be ignored in scoring.

---

# 18. Candidate A8 — Lock + two-phase commit

Use this candidate as a control against bespoke protocol complexity.

A valid implementation must persist at least:

```text
transaction id
expected predecessor/head
prepare record
payload/object identity
commit decision/marker
recovery state
```

Test crashes after each state transition.

If a home-grown 2PC requires substantially more custom correctness logic than A1/A2/A4/A5, score that implementation burden explicitly.

---

# 19. Scoring model

Do not rank by subjective preference alone.

Score each candidate from 0–5 on each axis, with evidence references:

```text
C1 concurrent-writer safety
C2 crash consistency
C3 acknowledged-commit durability
C4 recovery determinism
C5 replay/idempotency
C6 orphan/partial-state containment
C7 same-host implementation simplicity
C8 dependency/operational complexity
C9 auditability / provenance clarity
C10 fit with content-addressed NEXUS design
C11 ability to preserve current public data model
C12 testability/falsifiability
C13 migration cost
C14 network/multi-host extensibility if actually required
C15 upstream maturity / maintenance risk
```

Return raw axis scores plus weighting assumptions.

Provide at least two ranking views:

```text
RANKING_MINIMAL_NEXUS_SAME_HOST
RANKING_FUTURE_MULTIWRITER_EXTENSIBLE
```

Do not hide sensitivity to weights.

---

# 20. Mandatory comparative controls

At minimum compare the final top candidates against:

```text
CONTROL_0 = current NEXUS implementation
CONTROL_1 = current implementation + global POSIX flock only
```

This matters because a complex architecture must demonstrate material advantage over a minimal lock remediation.

For `flock` control, scope claims honestly:

```text
same-host local POSIX filesystem only unless separately established
```

---

# 21. Research-return semantic audit

Independently audit QWEN's research files for:

```text
source existence
source authority classification
repository identity
license claims
release/commit claims
file/function pins
paper venue/year
open-access status
mechanism description
QWEN inference vs source fact
ranking evidence
```

For the strongest 10 open-source artifacts and strongest 10 research papers, independently verify the cited source rather than trusting the register.

Record corrections explicitly.

Do not reject the whole return because one source pin is stale if the architecture conclusion remains independently supported.

---

# 22. Required upstream targets

At minimum independently inspect current primary/upstream material for:

```text
SQLite WAL and transaction/durability documentation
Git update-ref and ref transaction semantics
LMDB transaction/durability semantics
RocksDB WAL / WriteBatch / transaction semantics
Tessera sequencing/storage semantics
Trillian where historically relevant
Sigstore/Rekor only where relevant to append-only transparency behavior
WOLVES / WOFS OSDI 2025
PoWER Never Corrupts OSDI 2025
F2FSJ OSDI 2025 if QWEN materially relied on it
relevant FAST 2025/2026 crash-consistency work cited by QWEN
```

Prefer primary project documentation, code, papers and artifact repositories.

---

# 23. Local candidate code

You are authorized to create **local ephemeral prototypes and patches only**.

Allowed:

```text
scratch SQLite prototype
scratch CAS-head prototype
scratch Git-ref prototype
scratch lock control
fault-injection harness
benchmark/failure harness
candidate patch against frozen NEXUS base
```

Not allowed:

```text
git push
gh pr create
GitHub mutation
main mutation
ruleset mutation
release/tag
public attestation
```

If a candidate patch against NEXUS is created, it must remain a local candidate and be fully byte-bound in the return.

---

# 24. Non-interference

Do not mutate historical evidence merely to make tests easier.

The frozen base is a subject, not a disposable fixture.

Use copies/temporary repositories for destructive tests.

Preserve:

```text
communication genesis/history
A83 path-bound artifacts
research pipeline archive
public main state
```

---

# 25. Required terminal conclusions

At the end, answer all of these explicitly:

```text
1. Did Gate 0 independently match the producer package?
2. Did current NEXUS multiwriter failure reproduce?
3. Which QWEN hypotheses were confirmed?
4. Which QWEN hypotheses were refuted?
5. Which source claims required correction?
6. Which candidate had best same-host NEXUS fit?
7. Which candidate had best crash/recovery behavior?
8. Which candidate had smallest trustworthy commit surface?
9. Does global flock alone solve enough of the current problem?
10. Is SQLite materially better than CAS-head for current NEXUS?
11. Is CAS-head materially better than SQLite for current NEXUS?
12. Does Tessera-style sequencing provide value proportional to complexity?
13. Are LMDB/RocksDB justified at current scale?
14. Is Git-native ledger operationally credible or only attractive for auditability?
15. Is bespoke 2PC dominated by simpler candidates?
16. What exact candidate(s) should Cursor implement/validate next?
17. What remains NOT_ESTABLISHED?
```

---

# 26. Required output package

Physically expose at minimum:

```text
1. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_VALIDATION_RETURN_20260901_R0.md
2. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_GATE0_BINDING_20260901_R0.json
3. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_SOURCE_AUDIT_20260901_R0.json
4. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_FAILURE_MATRIX_20260901_R0.json
5. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_ARCHITECTURE_SCORES_20260901_R0.json
6. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_EXPERIMENT_RESULTS_20260901_R0.json
7. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_RECOMMENDATION_20260901_R0.md
8. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_CURSOR_HANDOFF_20260901_R0.md
9. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_RETURN_MANIFEST_20260901_R0.json
10. NEXUS_OMEGA_QWEN_CODER_R5_LEDGER_DURABILITY_SHA256SUMS_20260901_R0.txt
```

If code/prototypes/patches are material to your verdict, additionally expose:

```text
11. candidate.patch
12. PATCH_INVENTORY.json
13. FAULT_INJECTION_HARNESS/
14. REPRODUCTION_COMMANDS.md
```

Do not omit outputs because the run became large.

---

# 27. Persistence gate

For every material output:

```text
WRITE
→ CLOSE
→ READ_BACK
→ BYTE_COUNT
→ SHA256
→ VERIFY_EXISTS
```

Then generate final `RETURN_MANIFEST`.

Then regenerate final `SHA256SUMS`.

Then independently read back both final binding files.

Never report `COMPLETE` before this gate.

---

# 28. Required environment record

Return exact:

```text
OS
KERNEL
FILESYSTEM
CPU_ARCH
PYTHON
NODE
GIT
SQLITE_LIBRARY_VERSION
LMDB_VERSION_IF_USED
ROCKSDB_VERSION_IF_USED
TESSERA_COMMIT_IF_USED
TEST_FRAMEWORKS
FAULT_INJECTION_METHOD
DEPENDENCY_LOCK_STATE
```

For each test suite:

```text
COMMAND
EXIT_CODE
PASS
FAIL
SKIP
DURATION
SEED_IF_APPLICABLE
```

---

# 29. Terminal state vocabulary

Use one primary terminal state:

```text
PASS_INDEPENDENT_R5_LEDGER_DURABILITY_VALIDATION_WITH_CAVEATS_C1
PASS_PARTIAL_R5_LEDGER_DURABILITY_VALIDATION_WITH_CAVEATS_C1
FAIL_MAJOR_QWEN_RETURN_BINDING_C1
FAIL_MAJOR_ARCHITECTURE_HYPOTHESES_NOT_REPRODUCED_C1
FAIL_MAJOR_VALIDATION_ENVIRONMENT_INSUFFICIENT_C1
```

Producer-return semantic disagreement is allowed and expected.

---

# 30. Final governance boundary

Even if one architecture dominates experimentally:

```text
QWEN_CODER_PASS
!=
CURSOR_IMPLEMENTATION_AUTHORIZED

QWEN_CODER_PASS
!=
MAIN_MUTATION

QWEN_CODER_PASS
!=
CLAIM_PROMOTION
```

Return to AXIOM/operator for adjudication.

Terminal target:

```text
INDEPENDENTLY_REHASHED
+ SOURCE_AUDITED
+ FAILURE_INJECTED
+ COMPARATIVELY_SCORED
+ CURSOR_READY_CANDIDATE_RECOMMENDATION
```
