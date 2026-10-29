# AXIOM Alpha-Node C1 - bounded FIFO nonblocking fixity preflight V2 (2026-10-29)

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_FIFO_NONBLOCKING_FIXITY_V2_20261029_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = a2da485b293023a8b687440462b3794a1880bd86
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/198
PREDECESSOR_ISSUE93_RECEIPT = 6504006308
FROZEN_ORACLE_FIRST_COMMIT = d91ace5dd6df35aa33afe64934abca3d99d33e87
CANDIDATE_SECOND_COMMIT = d2bba1557cebd8407e99c25b21f4a67b68cf4008
PRODUCTION_INTEGRATION = NO
R10_EXPERT_RETURN = SOURCE_NOT_PRESENT_IN_CHECKED_PR_DISCUSSIONS
WWW_PARITY = NOT_ESTABLISHED

## OBSERVE / original bytes / provenance

The latest physically retrieved main at start was a2da485b293023a8b687440462b3794a1880bd86, immediately after PR #198. The existing governance, Alpha-Node R0 contract, repository order, pipeline policy, Repository Steward V1, Issue #93 and external write-slot registry were read on that immutable main. The owner registry still had an empty external actor allowlist. The source predecessor is the existing V1 research-only preflight at research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py, 4194 bytes, SHA-256 0fb4f5408d4c61d3a2e4c9bd160cc63afe68b077febbdd288e757b0fb324af23, Git blob 80ed3eee7bf66c8076ce4f06c1eac5e9904ded48. The retrieved source was reconstructed locally byte-exact; local SHA-256 and git hash-object matched those pinned identifiers.

## NEGATIVE HYPOTHESIS / independent falsifier

A malicious or accidental POSIX named pipe at an expected dependency filename can make the V1 os.open(path, O_RDONLY) block before fstat can reject nonregular input. An unattended read-only preflight can therefore hang even though it ultimately intends to reject nonregular files.

The frozen evaluator creates a named pipe at a scoped expected path with no writer, then runs the original V1 in a separate Python subprocess with a 1.2-second timeout. V1 demonstrably exceeded the timeout. The V2 successor adds os.O_NONBLOCK to the open flags and preserves the fstat regular-file check; the identical FIFO fixture returned a NONREGULAR_FILE failure inside the same 1.2-second bound. This is a synthetic availability falsification, not evidence of an actual attack or GitHub repository compromise.

Falsifier: V2 must fail if a POSIX FIFO still blocks past the fixed deadline, or if the change permits a FIFO, symlink, missing file, truncated file or same-size SHA-256 mutation to pass as MATCH. Positive regular files must continue to pass. A platform lacking POSIX mkfifo/O_NONBLOCK is explicitly not covered by the FIFO test.

## PINNED BASELINE / isolated candidate / evaluator

- Frozen evaluator first: frozen_issue93_fifo_preflight_oracle_v1_20261029.py, 5558 bytes, SHA-256 f03554118a1851798c980bde876dbdce8236d08383dc19565b79ba8873cfc2ed, Git blob a1bf95676ff381d7f2d78b36aa1cc6f58bf1232f.
- Candidate second: alpha_issue93_v7_dependency_fixity_preflight_v2_20261029.py, 4397 bytes, SHA-256 e224c42beced1c23748f241532b467b4a8ef9ef097e69c95d74e67a667748312, Git blob c3d451b9eb59dc5f45d8299602d2ea145aeca216.
- The evaluator was frozen locally and committed before the V2 candidate was committed. The candidate does not edit its evaluator or the historical V1 source. The two source files were fetched again from their exact branch commits, with Git blobs matching independently computed local git hash-object values.
- Command: python frozen_issue93_fifo_preflight_oracle_v1_20261029.py -v
- Observed local isolated result on a POSIX Linux container: 12/12 PASS, including positive regular-file control, SHA-256 mutation, missing file, truncation, symlink, directory, FIFO timeout differential, unsafe path, malformed digest, empty manifest, scoped extra file and unchanged seven-file expected inventory.
- The negative FIFO fixture is measured as V1 = timeout >1.2 s and V2 = fail-closed <1.2 s. This is one fixture, not a latency distribution or a production SLA.
- Independent evaluation here means a separate versioned test file pinned before candidate code and separate subprocesses for the FIFO differential; it does not mean external third-party validation.
- No actual seven-file repository checkout was tested with the new V2 CLI; actual-source end-to-end integration remains NOT_EXECUTED.

## DECISION / bounded outcome

V2 is a public-safe additive research-only candidate for nonblocking detection of POSIX named pipes. It does not authenticate GitHub actors, receipts or scientific claims, guarantee Windows behavior, eliminate filesystem races, or modify any live parser. No runtime, Hostinger, WWW, external worker, external actor registry, historical source, CI oracle or model weights were modified.

The R10 PR #115 was read: it remained open, with zero comments, zero reviews and zero review threads in this check. No independently authenticated expert receiver ACK or executed expert research is established. The historical R10 detached manifest was not rehashed in this iteration.

Target handoff automation >=90% and full-readback 100% remain NOT_COMPUTABLE project-wide: the complete eligible handoff and failed-attempt denominators are not available. This iteration publishes at most one isolated C1 candidate, not a claim of project-wide automation progress.

BLOCKED_LANE != BLOCKED_SYSTEM
DRIFT_RESET = NON_DESTRUCTIVE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
