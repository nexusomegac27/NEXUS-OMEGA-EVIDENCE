# AXIOM Alpha-Node C1 — Steward Unicode normalization collision witness (2026-10-27)

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_UNICODE_NFC_COLLISION_20261027_R0
DECISION = PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PREDECESSOR_ISSUE93_RECEIPT = 6454429786
PINNED_MAIN_BEFORE = 6a72d67461496960de732b64669ed186874fd713
PRODUCTION_STEWARD_UNCHANGED = YES
GITHUB_TO_WWW_PARITY = NOT_ESTABLISHED

## Original source and counter-hypothesis

- Original: scripts/nexus_repository_steward.py at pinned main, Git blob 296c7dc67b40f28270c92512ca6f67f8ad25fc50, 8,023 UTF-8 bytes, independently calculated SHA-256 94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998.
- Test source: tests/test_nexus_repository_steward.py, Git blob 063365adf8d4e8738412b917df9ff1d69f44e808, 4,445 bytes, independently calculated SHA-256 76e8701cb52a7ad54a5ede01d3f6c04193b21885996f4bf597112276623614a0.
- Original path-key predicate: identity = path.casefold(); the existing test covers ASCII case collision, not NFC/NFD equivalence.
- Hypothesis: two distinct Git paths that differ only in canonical Unicode normalization can escape the original collision predicate, even though they may be ambiguous on some checkout filesystems. This is a *portability-risk witness*, not proof of an exploit or an existing production collision.
- Counter-hypothesis: on normalization-sensitive filesystems, both names may coexist safely; even on other filesystems, Git checkout behavior may reject them earlier. The witness intentionally reports a conservative scoped HOLD, not a universal security vulnerability.
- Current immutable Git tree inventory: 568 tracked blob paths, 0 non-ASCII path names; no current collision asserted.

## Frozen independent evaluator, candidate and measured result

- Evaluator committed **first**: 33508803433f899a20430d71f3e188910411f862, file frozen_steward_unicode_collision_evaluator_v1_20261027.py, Git blob 2ff5124c5afa037d83e0a793e2650f48bbe7155e, 4,053 bytes, SHA-256 b5c74bd1e5dbf97f3a2a04a806e6c54c6ae4b71b564315a5e14246ee397e6fdb.
- Candidate committed **second**: 1c62c57258d24398804eb6177ede402e9cc8561f, file alpha_steward_unicode_collision_witness_v1_20261027.py, Git blob d59f6284ceee9702ce04d980c5f6230f901b8d0f, 1,752 bytes, SHA-256 a25cebefc86e12561b87b94fc98f6485b14ad9d0c5a13246cff3c0059c95e97a.
- Black-box execution under Python 3.13.5 in separate processes: **16/16 fixtures PASS**, including 11 valid path sets and five invalid-input fail-closed controls.
- Three focused NFC/NFD negative fixtures: pinned V1 .casefold() expression detects **0/3**; candidate NFC+casefold witness detects **3/3**.
- Independent negative mutant omitting NFC: **12/16 PASS, four expected failures**, including the three targeted negatives.
- Existing ASCII case-fold behavior retained; exact duplicate names not flagged; NFKC-only compatibility distinctions not folded. No independent third-party scientific validation asserted.

Reproduction from these two immutable GitHub files:

    python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_steward_unicode_collision_evaluator_v1_20261027.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_steward_unicode_collision_witness_v1_20261027.py

## Scientific and operational boundary

This is an **additive isolated research candidate**. It does not edit the productive Steward, GitHub rulesets, Git tree, filesystem, registered actor, runtime, Hostinger, WWW or model. The frozen evaluator was not modified after the candidate was introduced. The witness is not a complete cross-platform path-equivalence oracle and is not a substitute for full-Steward integration, filesystem-specific adversarial tests, bounded-input performance checks or independent third-party review. No historical paths are migrated. Future integration requires separately authorized change and tests.

The complete eligible public-handoff project census is absent: PROJECT_AUTOMATION_RATE = NOT_COMPUTABLE; PROJECT_READBACK_100_PERCENT = NOT_ESTABLISHED. This candidate does not improve either project-wide numerator or denominator by itself.
