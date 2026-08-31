# NEXUS OMEGA — AXIOM → QWEN
## R5 Maximum-Depth Open-Source & Open-Access Research Order
### Communication Ledger Multiwriter Serialization, Crash Consistency, Durability & Recovery

```text
OBJECT = NEXUS_OMEGA_QWEN_R5_LEDGER_DURABILITY_MAXIMUM_DEPTH_RESEARCH_ORDER_20260831_R0
STATE = AUTHORIZED_RESEARCH_ONLY
FROM = OPERATOR_ALEXANDER_VIA_AXIOM
TO = QWEN
ROLE = EXTERNAL_RESEARCHER
CLAIM = C1_DESCRIPTIVE_ONLY
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
CODE_IMPLEMENTATION = NO
GITHUB_WRITE = NO
PR = NO
MERGE = NO
RULESET_MUTATION = NO
NEXT_VALIDATOR = QWEN-CODER
BLOCKED_LANE_NOT_BLOCKED_SYSTEM = ACTIVE
```

---

# 0. Mission

Conduct an intensive, evidence-driven search for **open-source artifacts, freely accessible technical documentation, reproducible experiments, and open-access research** that can materially improve the NEXUS OMEGA communication ledger in the following exact gap area:

```text
MULTIWRITER_SERIALIZATION
+ COMPARE_AND_SWAP / HEAD VERSIONING
+ CROSS_FILE_TRANSACTION_ATOMICITY
+ CRASH CONSISTENCY
+ DURABILITY / FSYNC SEMANTICS
+ RECOVERY / REPLAY
+ ORPHAN / PARTIAL-TRANSACTION HANDLING
+ APPEND-ONLY / TAMPER-EVIDENT LOGGING
```

The purpose is not to produce a generic storage-systems literature review.

The purpose is to identify **concrete, transferable mechanisms** that could be independently validated by QWEN-CODER and later adapted to the actual NEXUS ledger.

Your final result must answer:

> Which existing open-source mechanisms and recent freely available research provide the strongest, simplest, most falsifiable path from the current three-file NEXUS append procedure to a robust same-host ledger transaction model, and what stronger path should remain available for future multi-host or transparency-log evolution?

---

# 1. Frozen live baseline

Repository:

```text
nexusomegac27/NEXUS-OMEGA-EVIDENCE
```

Frozen public baseline for this research round:

```text
MAIN = 5bebbe6775695dbe8028cfe7fb72ff30065ddd42
TREE = eda69dc3d7cbd100deb92a29bca4f7b718fd57ba
```

First independently verify this commit and inspect at minimum:

```text
scripts/append_scientific_record.py
scripts/validate_scientific_ledger.py
communication/index/v1/records.jsonl
communication/index/v1/latest.json
communication/objects/sha256/
```

Do not rely on this order's description if the code says something different.

If live `main` has advanced, preserve the frozen baseline and separately record current live state. Do not silently rebase the research question.

---

# 2. Starting hypotheses — MUST be independently tested, not accepted

Treat these as falsifiable hypotheses from prior AXIOM static analysis:

## H1 — Multiwriter serialization gap

The current writer appears to lack a lock, CAS token, transaction generation, or equivalent serialization covering the full sequence:

```text
VALIDATE_CURRENT_LEDGER
→ READ_HEAD / INDEX
→ DERIVE_SEQUENCE / PREVIOUS_HASH
→ WRITE_OBJECT
→ WRITE_INDEX
→ WRITE_LATEST
```

Hypothesis:

```text
MULTIWRITER_SERIALIZATION = NOT_ESTABLISHED
```

Refute H1 if the actual frozen code or a hidden/indirect mechanism establishes serialization.

## H2 — Cross-file atomicity gap

The object, index, and latest pointer are written as separate filesystem objects.

Hypothesis:

```text
CROSS_FILE_TRANSACTION_ATOMICITY = NOT_ESTABLISHED
```

Refute H2 if the actual implementation or filesystem contract establishes all-or-nothing visibility/durability for the full state transition.

## H3 — Crash-durability profile gap

The current code fsyncs temporary file content before replace, but a complete explicitly documented durability protocol for containing-directory metadata and the whole multi-file transaction is not apparent.

Hypothesis:

```text
CRASH_DURABILITY_PROFILE = NOT_ESTABLISHED
```

Do not overstate filesystem-specific behavior. Distinguish process crash, kernel crash, power loss, storage failure, and unsupported filesystem semantics.

## H4 — Detection without recovery

The ledger validator detects several inconsistent states, including orphan objects/head mismatches, but a formal automatic transaction recovery/replay protocol is not apparent.

Hypothesis:

```text
PARTIAL_TRANSACTION_DETECTION = PARTIAL_PRESENT
AUTOMATIC_RECOVERY_PROTOCOL = NOT_ESTABLISHED
```

Refute or refine this based on actual code.

---

# 3. Research principle

Search for **mechanisms, not brands**.

For every candidate, identify the exact mechanism:

```text
LOCK
CAS
GENERATION / REVISION TOKEN
WAL
ROLLBACK JOURNAL
COMMIT MARKER
WRITE BATCH
COPY-ON-WRITE
SHADOW PAGING
APPEND JOURNAL
MERKLE LOG
SINGLE WRITER SERVICE
TRANSACTIONAL DATABASE
ATOMIC RENAME
DIRECTORY FSYNC
GROUP COMMIT
CHECKPOINT
REPLAY
IDEMPOTENT RETRY
CRASH FAULT INJECTION
FORMAL RECOVERABILITY INVARIANT
```

Do not recommend a large dependency merely because it has transactions.

A small extracted design pattern is often more valuable than adopting an entire database.

---

# 4. Mandatory search lanes

Execute all independent lanes. A weak result in one lane does not stop the others.

## Lane A — POSIX same-host serialization

Research:

- `flock`, `fcntl`/advisory locks, lock files;
- atomic create/link/rename patterns;
- stale-lock and process-death behavior;
- lock scope across processes/threads;
- local filesystem assumptions;
- NFS/network-filesystem caveats;
- lock acquisition before revalidation;
- lock release and exception behavior.

Find mature open-source examples where a read-modify-write filesystem transaction is serialized safely.

Do not conclude `flock = universal safety`.

## Lane B — compare-and-swap / expected-head transactions

Research mechanisms where a writer supplies the expected predecessor/version and the update fails if current state has changed.

Mandatory seed:

```text
Git git-update-ref transaction protocol
```

Inspect exact transaction semantics, lock preparation, old-OID verification, commit/abort behavior, and the documented caveat that concurrent readers may see subsets of multi-ref modifications.

Also search:

- etcd MVCC transactions;
- object-store conditional writes / ETag CAS patterns where open-source clients/tests exist;
- database optimistic concurrency control;
- Git ref backends / reftable if relevant.

Assess whether NEXUS should add an explicit `expected_head_sha256` / generation token even if same-host locking is used.

## Lane C — SQLite transactional patterns

Inspect actual SQLite mechanisms, not marketing summaries:

- rollback-journal atomic commit;
- WAL commit record semantics;
- writer concurrency model;
- checkpointing;
- synchronous modes;
- crash-test VFS;
- power-loss testing philosophy;
- directory/file synchronization assumptions.

Answer separately:

1. Should NEXUS adopt SQLite as the ledger state backend?
2. If not, which SQLite **design patterns/tests** should NEXUS copy conceptually?

Do not assume a database dependency is automatically preferable.

## Lane D — RocksDB / transactional KV patterns

Inspect:

- WAL;
- `WriteBatch` atomic updates;
- `TransactionDB`;
- optimistic vs pessimistic conflict handling;
- sequence numbers;
- prepare/commit markers;
- WAL recovery modes;
- synchronous vs asynchronous durability;
- process lock semantics.

Extract transferable ideas only.

## Lane E — LMDB / copy-on-write single-writer designs

Study:

- single-writer/multi-reader architecture;
- MVCC;
- copy-on-write page/root updates;
- commit-point/root-pointer semantics;
- durability options;
- recovery characteristics.

Question:

Could a **single-writer + immutable object + atomic root/head publication** model fit NEXUS more naturally than a general WAL?

## Lane F — content-addressed / transactional filesystem publication

Inspect open-source systems such as:

```text
OSTree
Git object/ref publication
Nix / content-addressed store mechanisms where relevant
```

Look for patterns where immutable objects are created first and a small mutable pointer is atomically advanced later.

This is especially relevant because NEXUS already stores immutable content-addressed record objects.

Test the architectural hypothesis:

```text
IMMUTABLE_OBJECTS_FIRST
+ SINGLE_COMMIT_RECORD_OR_HEAD_POINTER_LAST
```

may reduce the required atomicity surface.

## Lane G — append-only transparency logs

Mandatory systems:

```text
Trillian
Tessera
Sigstore Rekor / Rekor v2 evolution
```

Research:

- sequencing;
- integration queues;
- tree heads/checkpoints;
- Merkle inclusion/consistency proofs;
- POSIX storage driver patterns;
- synchronous integration;
- witness support;
- deduplication/idempotence;
- storage backend abstraction;
- operator recovery.

Pay special attention to **Tessera**, not just legacy Trillian. Modern Tessera is explicitly positioned as the newer transparency-log approach and includes a POSIX backend.

Question:

Which transparency-log mechanisms are useful for NEXUS **without prematurely turning the small communication ledger into a distributed service**?

## Lane H — tamper-evident databases

Mandatory seed:

```text
immudb
```

Search additional open-source append-only/auditable databases if technically credible.

Extract:

- transaction numbering;
- cryptographic state roots;
- audit proofs;
- state signing;
- append-log recovery;
- client verification patterns.

Distinguish:

```text
TAMPER EVIDENCE
!=
CRASH ATOMICITY
!=
CONCURRENCY CONTROL
```

## Lane I — crash-consistency testing artifacts

Mandatory artifact:

```text
CrashMonkey + Ace
```

Search for additional freely available tools/frameworks for:

- fault injection;
- simulated power loss;
- filesystem crash exploration;
- syscall-level failure injection;
- deterministic record/replay;
- workload generation;
- crash-state checking;
- mutation/fuzz testing of recovery.

Determine which tools can realistically test a Python three-file transactional writer in a Linux VM.

Do not discard older artifacts solely because of age if they remain technically useful.

## Lane J — formal verification / crash invariants

Mandatory recent research seed:

```text
PoWER Never Corrupts — OSDI 2025
```

Search freely available work on:

- recoverability specifications;
- write preconditions;
- crash Hoare logic;
- verified KV stores/filesystems;
- lightweight state-machine/model checking usable without formally verifying the entire Python implementation.

Goal:

Extract **small invariants that QWEN-CODER can test**, even if full formal verification is impractical.

## Lane K — recent open-access storage research, 2025–2026

Search FAST, OSDI, SOSP, EuroSys, ATC, VLDB, arXiv and relevant open research repositories.

Mandatory seeds to independently inspect:

```text
OSDI 2025:
- Fast and Synchronous Crash Consistency with Metadata Write-Once File System (WOFS/WOLVES)
- PoWER Never Corrupts
- Decentralized, Epoch-based F2FS Journaling with Fine-grained Crash Recovery (F2FSJ)

FAST 2025:
- Silhouette
- Ananke
- DJFS
- NVLog / transparent NVM write-ahead logging
- AWUPF Rediscovered

FAST 2026:
- MlsDisk
- relevant append-only / log-structured deployed-system work such as ByteStore/DisCoGC
```

Do not force transferability. For every paper, identify exactly what applies and what does not.

## Lane L — GitHub-native / repository-native options

Search whether NEXUS can exploit Git/GitHub-native transactional primitives instead of inventing a mini-database:

- Git refs transactions;
- commit/tree object immutability;
- compare expected parent/head;
- branch update semantics;
- repository serialization patterns;
- Actions-based validation/recovery monitors.

Question:

Could the communication ledger eventually use Git itself as the authoritative append transaction boundary while retaining content-addressed record objects?

Analyze benefits and limitations, including local/offline behavior and dependency on repository commits.

---

# 5. Search depth and source-quality requirements

Do not optimize for counts, but perform a genuinely broad search.

Targets:

```text
QUALIFIED_OPEN_SOURCE_ARTIFACTS >= 25
TARGET_OPEN_SOURCE_ARTIFACTS = 40

QUALIFIED_OPEN_ACCESS_RESEARCH_ITEMS >= 20
TARGET_RESEARCH_ITEMS = 30
```

If quality saturates below a target, stop adding weak items and explain saturation.

For every artifact/research item classify source strength:

```text
P0 = NORMATIVE / PRIMARY SPECIFICATION
P1 = UPSTREAM SOURCE CODE / DESIGN DOC / TESTS / RELEASE
P2 = PEER-REVIEWED OPEN-ACCESS PAPER / AUTHOR ARTIFACT
P3 = SECONDARY TECHNICAL ANALYSIS
P4 = EXPLORATORY LEAD ONLY
```

Core conclusions must not rest only on P3/P4.

---

# 6. Open-source artifact register — mandatory fields

For each qualified artifact capture:

```text
ARTIFACT_ID
PROJECT
REPOSITORY_URL
LICENSE
UPSTREAM_OR_FORK
CURRENT_STATUS
LATEST_VERIFIED_RELEASE_OR_COMMIT
PRIMARY_LANGUAGE
STORAGE_MODEL
WRITER_MODEL
CONCURRENCY_CONTROL
COMMIT_POINT
DURABILITY_MECHANISM
CRASH_RECOVERY
FSYNC_OR_DURABILITY_ASSUMPTIONS
IDEMPOTENCE / REPLAY
FAULT_INJECTION_TESTS
FORMAL_VERIFICATION_IF_ANY
EXACT_RELEVANT_FILES_OR_FUNCTIONS
NEXUS_TRANSFERABLE_MECHANISM
NEXUS_NON_TRANSFERABLE_ASSUMPTIONS
ADOPTION_COST
DEPENDENCY_COST
RISK
SOURCE_CLASS
```

Exact relevant source files/functions are important. A project name alone is insufficient.

---

# 7. Research-paper register — mandatory fields

For each qualified paper/report:

```text
RESEARCH_ID
TITLE
AUTHORS
VENUE
YEAR
OPEN_ACCESS_URL
ARTIFACT_URL_IF_AVAILABLE
PEER_REVIEW_STATUS
PROBLEM
MECHANISM
FAILURE_MODEL
CONCURRENCY_MODEL
RECOVERY_MODEL
EVALUATION_METHOD
FAULT_INJECTION_OR_PROOF_METHOD
OPEN_SOURCE_ARTIFACT_AVAILABLE
KEY_RESULT
LIMITATIONS
NEXUS_TRANSFERABILITY
NEXUS_TESTABLE_HYPOTHESIS
SOURCE_CLASS
```

Do not repeat abstract text. Extract the mechanism and falsifiable relevance.

---

# 8. Failure-model matrix

Build one explicit matrix covering at least:

```text
F01 two writers start from same ledger head
F02 three writers start from same ledger head
F03 duplicate record_id contention
F04 process crash before object write
F05 crash after object write, before index write
F06 crash after index write, before latest write
F07 crash after latest write, before post-validation
F08 power loss after write before fsync
F09 rename completed but containing-directory metadata not durable
F10 stale lock
F11 process dies holding/advising lock
F12 retry after ambiguous prior commit
F13 duplicated client request / replay
F14 orphan content-addressed object
F15 stale latest pointer
F16 truncated/corrupted index tail
F17 partial disk write
F18 ENOSPC during transaction
F19 permission / read-only transition during transaction
F20 filesystem lacking assumed lock/durability semantics
F21 NFS / network filesystem execution
F22 multi-host writers
F23 rollback/recovery itself crashes
F24 recovery executed twice
F25 validator crashes after repair starts
```

For every candidate architecture, state which failures it prevents, detects, tolerates, recovers, or leaves out of scope.

---

# 9. Candidate architecture families to compare

At minimum compare these families:

## A1 — Current architecture + POSIX global writer lock

```text
flock/fcntl
+ revalidate under lock
+ existing object/index/latest writes
+ directory fsync profile
```

## A2 — Lock + explicit transaction journal / commit marker

```text
lock
+ immutable transaction record
+ staged writes
+ commit marker
+ deterministic recovery
```

## A3 — Immutable object + append journal as sole authoritative mutable stream

```text
record object
+ one append-only transaction journal
+ derived latest/index
```

Question whether `latest.json` and/or full index should become derived/cache state.

## A4 — Immutable object + CAS/versioned single head

```text
record object first
+ expected_head
+ atomic/CAS head advance
+ index derived/rebuilt
```

## A5 — SQLite-backed ledger state

Content objects may remain files while sequence/head/index transaction state moves into SQLite.

## A6 — Embedded KV/WAL backend

Examples: RocksDB/LMDB or smaller equivalent. Evaluate dependency cost heavily.

## A7 — Git-native transaction boundary

Use immutable Git objects/commits plus expected parent/ref update as the append transaction boundary.

## A8 — Transparency-log architecture

Use or borrow Tessera/Trillian-style sequencing/checkpoint/proof mechanisms.

Do not assume A8 is appropriate for current scale.

## A9 — Single-writer service

One process serializes append requests; clients submit immutable entries. Evaluate operational complexity.

---

# 10. NEXUS-specific scoring model

Score every serious candidate from 0–5 on:

```text
CORRECTNESS
CRASH_RECOVERY
MULTIWRITER_SAFETY
DURABILITY_CLARITY
AUDITABILITY
CONTENT_ADDRESS_COMPATIBILITY
IMPLEMENTATION_SIMPLICITY
DEPENDENCY_MINIMALITY
PORTABILITY
TESTABILITY
FAULT_INJECTION_TESTABILITY
BACKWARD_COMPATIBILITY
MIGRATION_RISK
PERFORMANCE_AT_CURRENT_SCALE
FUTURE_SCALABILITY
```

Also apply hard penalties for:

```text
requires distributed infrastructure for a local problem
requires opaque proprietary service
cannot reproduce failure semantics locally
weak/no license clarity
inactive/unmaintained with no transferable mechanism
requires historical hash/path rewrites
mixes tamper evidence with crash atomicity claims
```

Produce weighted and unweighted rankings. Explain weights.

---

# 11. Mandatory architecture question: reduce the atomicity surface

Investigate this specific NEXUS redesign hypothesis in depth:

Current state has three logically coupled writes:

```text
record object
records.jsonl
latest.json
```

Research whether a stronger model is:

```text
1. WRITE IMMUTABLE CONTENT OBJECT
2. COMMIT EXACTLY ONE AUTHORITATIVE TRANSACTION/HEAD RECORD
3. DERIVE INDEX AND LATEST VIEWS FROM AUTHORITATIVE LOG/HEAD
```

If so, determine:

- which object is authoritative;
- how sequence numbers are allocated;
- how expected predecessor is checked;
- how replay works;
- how duplicate submissions are handled;
- how orphan pre-commit objects are treated;
- whether garbage collection is needed;
- whether derived `latest.json` can safely lag;
- how validation determines committed vs staged objects.

This question has high priority.

---

# 12. Mandatory durability question: `fsync` and rename are not enough as slogans

Research exact semantics and practical guidance for:

```text
write
flush
fdatasync
fsync(file)
rename/replace
fsync(directory)
filesystem barriers/order
```

Distinguish:

```text
PROCESS_CRASH
KERNEL_CRASH
POWER_LOSS
DEVICE_CACHE_FAILURE
FILESYSTEM_BUG
```

Do not produce universal POSIX claims where real guarantees are filesystem/OS dependent.

Identify test strategies that can establish the **actual supported NEXUS environment profile** rather than theoretical universal safety.

---

# 13. Mandatory concurrency question: lock vs CAS vs both

Determine whether the strongest practical same-host design should use:

```text
LOCK_ONLY
CAS_ONLY
LOCK + EXPECTED_HEAD
SINGLE_WRITER_ONLY
TRANSACTIONAL_BACKEND
```

Important:

A lock prevents concurrent critical-section execution only within its supported scope.

An expected-head/CAS condition additionally detects stale writers and can improve retry/recovery semantics.

Research whether **defense in depth through both** is justified for NEXUS or merely redundant complexity.

---

# 14. Mandatory crash-testing plan for QWEN-CODER

Your research return must hand QWEN-CODER a concrete independent validation plan.

It must specify how to reproduce/falsify the recommended design using at least:

```text
20 dual-writer trials
20 triple-writer trials
randomized launch jitter
forced process kill at each transaction phase
SIGKILL
fault injection around fsync/rename
ENOSPC simulation if practical
replay of same request
crash during recovery
recovery twice
validator after recovery
```

Include which open-source crash-testing/fault-injection artifacts should be tried first and which are too heavyweight.

QWEN-CODER must be able to validate the design without trusting your conclusion.

---

# 15. Mandatory open-source code acquisition standard

For top candidates, do not cite only project home pages.

Pin where feasible:

```text
repository
branch/tag/release
commit SHA
exact file path
function/type/module
license
```

If a project evolves quickly, distinguish current main from stable release.

Record whether source was actually inspected or only documentation was read.

---

# 16. Mandatory novelty / recency search

Search up to the current date, including 2025–2026 work.

Use at least:

```text
USENIX FAST 2025
USENIX FAST 2026
OSDI 2025
SOSP / EuroSys / ATC if relevant
arXiv recent systems/storage papers
artifact repositories linked from papers
GitHub repositories of author artifacts
```

Prioritize papers with open code/artifacts.

Report **newer replacement/evolution paths**, e.g. modern Tessera vs legacy Trillian, rather than recommending an obsolete architecture because it is famous.

---

# 17. Required falsification behavior

Actively try to disprove attractive candidates.

Examples:

- Does `flock` fail our portability/multi-host goals?
- Does SQLite solve more than we need and introduce unnecessary semantic migration?
- Does LMDB impose a storage model incompatible with existing JSONL/public review?
- Does Git-native commit coupling make local append too heavy?
- Does Tessera solve transparency but not our local crash transaction problem?
- Does a WAL improve recovery but still require serialization?
- Does CAS prevent lost updates but not cross-file crash inconsistency?
- Does a commit marker solve recovery but still leave directory durability ambiguous?

A candidate that survives falsification should rank higher than one with impressive features but untested mismatch risk.

---

# 18. Required top-level decision outputs

Your final report must contain these explicit conclusions:

```text
CURRENT_H1_MULTIWRITER_GAP = CONFIRMED / REFUTED / PARTIAL / NOT_ESTABLISHED
CURRENT_H2_CROSS_FILE_ATOMICITY_GAP = CONFIRMED / REFUTED / PARTIAL / NOT_ESTABLISHED
CURRENT_H3_DURABILITY_PROFILE_GAP = CONFIRMED / REFUTED / PARTIAL / NOT_ESTABLISHED
CURRENT_H4_RECOVERY_GAP = CONFIRMED / REFUTED / PARTIAL / NOT_ESTABLISHED
```

Then provide:

```text
BEST_MINIMAL_SAME_HOST_DESIGN = <one architecture>
BEST_ALTERNATE_SAME_HOST_DESIGN = <one architecture>
BEST_STRONGER_FUTURE_DESIGN = <one architecture>
BEST_CRASH_TESTING_TOOLCHAIN = <toolchain>
BEST_FORMAL_INVARIANT_SET = <short set>
DATABASE_DEPENDENCY_RECOMMENDED = YES / NO / CONDITIONAL
TRANSPARENCY_LOG_BACKEND_RECOMMENDED_NOW = YES / NO / CONDITIONAL
GIT_NATIVE_TRANSACTION_RECOMMENDED = YES / NO / CONDITIONAL
```

Every recommendation must include reasons and falsification conditions.

---

# 19. Required Top-8 shortlist

Produce **5–8 finalists**, not 25 vague options.

For each finalist provide:

```text
RANK
ARCHITECTURE
OPEN_SOURCE_REFERENCE(S)
RECENT_RESEARCH_REFERENCE(S)
WHY_IT_FITS_NEXUS
WHAT_IT_SOLVES
WHAT_IT_DOES_NOT_SOLVE
IMPLEMENTATION_SIZE_ESTIMATE
NEW_DEPENDENCIES
BACKWARD_COMPATIBILITY
MIGRATION_PATH
QWEN_CODER_VALIDATION_PLAN
KILL_CRITERIA
```

`KILL_CRITERIA` is mandatory: specify what finding should cause us to reject the option.

---

# 20. Required output files

Return at minimum these physical UTF-8 artifacts:

```text
1. NEXUS_OMEGA_QWEN_R5_LEDGER_DURABILITY_RESEARCH_RETURN_20260831_R0.md
2. NEXUS_OMEGA_QWEN_R5_LEDGER_OPEN_SOURCE_ARTIFACT_REGISTER_20260831_R0.json
3. NEXUS_OMEGA_QWEN_R5_LEDGER_OPEN_RESEARCH_REGISTER_20260831_R0.json
4. NEXUS_OMEGA_QWEN_R5_LEDGER_FAILURE_MODEL_MATRIX_20260831_R0.json
5. NEXUS_OMEGA_QWEN_R5_LEDGER_ARCHITECTURE_COMPARISON_20260831_R0.json
6. NEXUS_OMEGA_QWEN_R5_LEDGER_TOP8_SHORTLIST_20260831_R0.json
7. NEXUS_OMEGA_QWEN_R5_LEDGER_QWEN_CODER_VALIDATION_HANDOFF_20260831_R0.md
8. NEXUS_OMEGA_QWEN_R5_LEDGER_PRIMARY_SOURCE_REGISTER_20260831_R0.json
9. NEXUS_OMEGA_QWEN_R5_LEDGER_SHA256SUMS_20260831_R0.txt
```

Optional but strongly encouraged:

```text
10. NEXUS_OMEGA_QWEN_R5_LEDGER_SOURCE_CODE_PIN_REGISTER_20260831_R0.json
11. NEXUS_OMEGA_QWEN_R5_LEDGER_RESEARCH_GAPS_AND_NEGATIVE_RESULTS_20260831_R0.md
12. NEXUS_OMEGA_QWEN_R5_LEDGER_REFERENCE_DIAGRAMS_20260831_R0.md
```

Do not create a candidate implementation patch in this QWEN round.

Implementation/falsification of the selected design belongs to QWEN-CODER.

---

# 21. Return persistence

For each output:

```text
WRITE
→ CLOSE
→ READ BACK
→ BYTE COUNT
→ SHA256
→ VERIFY FILE EXISTS
```

The SHA256SUMS file must bind all required outputs.

If your environment cannot physically expose files, provide the complete output contents in clearly separated blocks and report:

```text
PHYSICAL_FILE_EXPORT = NOT_AVAILABLE_IN_CURRENT_ENVIRONMENT
```

Do not pretend a file exists when it does not.

---

# 22. Research metrics

Report:

```text
SEARCH_QUERIES_EXECUTED
OPEN_SOURCE_CANDIDATES_SCREENED
OPEN_SOURCE_CANDIDATES_QUALIFIED
SOURCE_CODE_REPOS_ACTUALLY_INSPECTED
EXACT_CODE_PINS_RECORDED
OPEN_ACCESS_RESEARCH_SCREENED
OPEN_ACCESS_RESEARCH_QUALIFIED
2025_2026_ITEMS_QUALIFIED
AUTHOR_ARTIFACTS_FOUND
CANDIDATES_REJECTED
HYPOTHESES_REFUTED
HYPOTHESES_CONFIRMED_OR_SUPPORTED
NOT_ESTABLISHED_ITEMS
```

Counts are descriptive only. Do not game them.

---

# 23. Search saturation criterion

Do not search forever.

Research may be considered saturated when:

1. all mandatory lanes A–L have at least one high-quality primary result or a documented no-result;
2. three consecutive materially different search strategies produce no new architecture family relevant to NEXUS;
3. the Top-8 ranking remains stable after adding the latest credible candidates;
4. key mechanisms are supported by primary code/docs and, where possible, research evidence.

State whether saturation was reached.

---

# 24. Independence and handoff boundary

QWEN is the researcher for this round.

QWEN-CODER will later act as the independent technical validator/implementer.

Therefore:

```text
QWEN_RESEARCH_RECOMMENDATION
!=
QWEN_CODER_INDEPENDENT_VALIDATION
```

Do not mark any design as independently validated.

Required terminal field:

```text
INDEPENDENT_QWEN_CODER_VALIDATION = NOT_YET_EXECUTED
```

---

# 25. No broad paranoia / work-conserving rule

Use pragmatic research behavior.

```text
UNCERTAINTY != GLOBAL_STOP
BLOCKED_LANE != BLOCKED_SYSTEM
REVERSIBLE_ERROR != HARD_FAIL
```

If one repository is unavailable, continue other sources.

If one paper has no code, inspect its mechanism but rank reproducibility accordingly.

If a candidate cannot be fully verified, mark it `PARTIAL` and continue.

Hard stop only if the frozen NEXUS baseline itself cannot be identified sufficiently to understand the target problem.

---

# 26. Terminal verdict vocabulary

Choose one:

```text
PASS_RESEARCH_SATURATED_TOP_CANDIDATES_READY_FOR_QWEN_CODER_C1
PASS_RESEARCH_WITH_MATERIAL_GAPS_TOP_CANDIDATES_READY_C1
INCOMPLETE_RESEARCH_TARGET_BASE_NOT_AVAILABLE_C1
FAIL_MAJOR_RESEARCH_NO_TRANSFERABLE_ARCHITECTURE_FOUND_C1
```

The preferred outcome is not a PASS label; it is a high-quality, independently testable shortlist.

---

# 27. Required terminal machine block

```text
OBJECT = NEXUS_OMEGA_QWEN_R5_LEDGER_DURABILITY_RESEARCH_RETURN_20260831_R0
STATE = <ACTUAL>

FROZEN_MAIN_EXPECTED = 5bebbe6775695dbe8028cfe7fb72ff30065ddd42
FROZEN_MAIN_VERIFIED = <YES/NO>
CURRENT_MAIN_OBSERVED = <SHA>

H1_MULTIWRITER = <CONFIRMED/REFUTED/PARTIAL/NOT_ESTABLISHED>
H2_CROSS_FILE_ATOMICITY = <...>
H3_DURABILITY_PROFILE = <...>
H4_RECOVERY_PROTOCOL = <...>

QUALIFIED_OPEN_SOURCE_ARTIFACTS = <N>
QUALIFIED_OPEN_ACCESS_RESEARCH = <N>
QUALIFIED_2025_2026_RESEARCH = <N>
SOURCE_CODE_REPOS_INSPECTED = <N>

BEST_MINIMAL_SAME_HOST_DESIGN = <ID>
BEST_ALTERNATE_SAME_HOST_DESIGN = <ID>
BEST_STRONGER_FUTURE_DESIGN = <ID>
BEST_CRASH_TESTING_TOOLCHAIN = <ID>

TOP8_READY = <YES/NO>
SEARCH_SATURATION = <YES/NO>

CODE_IMPLEMENTATION = NO
PUBLIC_GITHUB_WRITE = NO
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
INDEPENDENT_QWEN_CODER_VALIDATION = NOT_YET_EXECUTED

NEXT = QWEN_CODER_INDEPENDENT_VALIDATION_OF_SELECTED_CANDIDATES
```

---

# 28. Final instruction

Do not give us a storage encyclopedia.

Give us a **decision-grade research package** that lets QWEN-CODER independently answer:

> Can we demonstrably eliminate the current NEXUS ledger's lost-update and partial-transaction classes with a minimal, testable design while preserving content-addressed history, transparent JSON artifacts, C1 governance, and future migration options?

Search aggressively. Reject weak analogies. Pin code. Use current open research. Preserve negative results. End with falsifiable architecture candidates.
