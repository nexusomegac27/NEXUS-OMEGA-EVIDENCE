# AXIOM Alpha-Node · postpublication fsync uncertainty · 2026-10-28 R0

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_POSTPUBLISH_FSYNC_STATUS_20261028_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=1157a2f9d9affc71414ca750333bcd2a1810c9db
PREDECESSOR_ISSUE93_RECEIPT=6461898518
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/165
RESEARCH_LANE=research/r16/axiom-alpha-node-c1-adaptation-20261012/
PRODUCTION_STEWARD=scripts/nexus_repository_steward.py
PRODUCTION_STEWARD_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
PRODUCTION_STEWARD_SHA256=94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
PRODUCTION_STEWARD_MODIFIED=NO

## Observation / original bytes / falsifier

The v2 atomic guard links the complete temporary file into its final name, unlinks the temporary name, and THEN fsyncs the parent directory. If that directory fsync fails, the complete final file is already visible but the function returns a generic OSError. An error exit therefore does not prove that publication did not occur. The previous R0 report explicitly excludes postpublication errors.

Pinned baseline: steward_output_atomic_guard_candidate_v2_20261028.py; 3187 bytes; Git blob e7fbad4dd0cd24f6f03c80b9ebbb709c2e14384c; independently rehashed SHA-256 441bffe0285183605b8d76d9f4d542ebf06f8e63e4f8cc92112550bc4df93841. Its predecessor v1: 3856 bytes; blob b697ebb2f0908cd09956bce880c78695f083a4c0; SHA-256 0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74.

Falsifier: the pinned v2 guard already emits a distinct published-but-durability-unknown result, or its final file is absent after an injected directory-fsync error. Baseline-only black-box oracle instead observed generic OSError and exact complete final bytes: 3/3 PASS.

## One candidate and frozen independent test

Candidate v3 preserves no-overwrite, checkout exclusion, O_NOFOLLOW parent traversal, file-fsync-before-link and temporary cleanup. ONLY after an error on postlink directory fsync, it reads the final file via the pinned directory descriptor and checks exact bytes. A match raises distinct PublishedDurabilityUncertain with marker PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN plus byte count and SHA-256. A readback error or mismatch is labeled PUBLISHED_READBACK_GAP_DURABILITY_UNKNOWN or PUBLISHED_READBACK_MISMATCH_DURABILITY_UNKNOWN. This is NOT a crash-durability guarantee.

EVALUATOR_FIRST_COMMIT=60351ef42d4a7b5103db1446191dfe612fc0dc2b
EVALUATOR_PATH=frozen_steward_postpublish_fsync_evaluator_v3_20261028.py
EVALUATOR_BYTES=6326
EVALUATOR_GIT_BLOB=9770506b270248f56b23859b94fb094f73ba4cd7
EVALUATOR_SHA256=636bb9780143dc7ec9f8df9053a5e56969479e182b30cf73a1f5a23e1555a17f
CANDIDATE_SECOND_COMMIT=aca92e8f2c53d4d1bab9f814f35391e783c83b2a
CANDIDATE_PATH=steward_output_postpublish_status_candidate_v3_20261028.py
CANDIDATE_BYTES=4191
CANDIDATE_GIT_BLOB=89d5df5726ed25756ca0550559eae268db3c1b36
CANDIDATE_SHA256=847c3bd775b195f30617174904af6644ab1d13dd30725a9f44e40fe797423578

Evaluator was committed BEFORE candidate. It runs modules in separate Python subprocesses, injects deterministic EIO on directory or file fsync, checks exception status, exact output bytes, cleanup and negative controls. The oracle does not import candidate logic. Independent test implementation is NOT independent third-party scientific validation.

## Executed synthetic tests

Environment: Linux, Python 3.13.5; temporary public-safe fixtures only. Baseline-only: 3/3 PASS. Candidate: 16/16 PASS. Injected directory-fsync error: original generic OSError with complete final file 1/1; candidate explicit uncertainty with exact final bytes and no leftover temporary file 1/1. Injected file-fsync error: no final file and no false publication marker. Normal success, no-replace, checkout denial and symlink-parent denial PASS. Negative mutant replacing distinct exception with generic OSError: 15/16 (expected failure). Negative mutant replacing uncertainty marker with PUBLISHED_SUCCESS: 15/16 (expected failure). Both mutants stayed local.

Reproduction: run frozen_steward_postpublish_fsync_evaluator_v3_20261028.py with --baseline pointing to v2; add --candidate pointing to v3 for full 16-test run. Both paths are in this existing R16 lane.

## Decision / limitations

Isolated diagnostic observability improvement only. Immediate readback is NOT power-loss durability. Failures during temporary cleanup, hostile concurrent changes, full CLI integration, process kill/crash, disk corruption and Windows/macOS behavior are untested. No production source edits, evaluator modification after freeze, folder migration, runtime/Hostinger/WWW write, new actor/worker, R10 expert acceptance or claim promotion.

PROJECT_ELIGIBLE_HANDOFF_DENOMINATOR=NOT_ESTABLISHED
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_100_PERCENT_READBACK=NOT_ESTABLISHED
R10_INDEPENDENT_EXPERT_RETURN=SOURCE_NOT_PRESENT
PUBLICATION=PENDING_PR_CI_MAIN_READBACK
WWW_PARITY=NOT_ESTABLISHED
