# AXIOM Alpha-Node — Issue #93 bounded JSON V4 · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_BOUNDED_JSON_GUARD_V4_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 8bb1861d8d548a3bec172ae892b4cda0e20ee559  
PREDECESSOR_PR = 250  
PREDECESSOR_ISSUE93_RECEIPT = 6549272854  
FROZEN_ORACLE_FIRST_COMMIT = c6a50dc156a39fbe35f67188d1ec5f1d7b4cee6e  
CANDIDATE_SECOND_COMMIT = c2a9d79e8ea908875f1a0c7271671b0c634e81a3  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Original source and counter-hypothesis

The actual V3 source at pinned main was retrieved and independently reconstructed byte-for-byte: 1,246 UTF-8 bytes; SHA-256 `e17749dd802096fc95ff56c8023674e767d3dc64668508286473768b26c45fe0`; Git blob `4a0663fc7769f7cc56ff161a1383ea72f3453503`. Its unchanged V2 and V1 imports were likewise byte-reconstructed and matched their Git blobs. Governance was read from the same pinned main. No historical source file was modified.

**Negative hypothesis:** V3's unbounded `sys.stdin.read()` can accept arbitrarily large, semantically ignored JSON subtrees; deeply nested JSON triggers an uncaught `RecursionError` rather than structured `FAIL_CLOSED`. This is a parser robustness finding, **not** evidence that GitHub supplied a malicious comment or that scientific content was compromised.

## Isolated candidate and independent-code test

V4 reads at most 4 MiB + 1 byte from binary stdin, rejects a larger input with `FAIL_CLOSED`, decodes strict UTF-8, reuses the unchanged V3 scalar validator and V2 finite-number parser, and maps recursion errors to structured `FAIL_CLOSED` (exit 2). It is a versioned research-only CLI; no production integration, live API call, persistent worker, or new pipeline.

The black-box subprocess evaluator was committed **first**, before candidate code, and does not import V4. Executed locally with Python 3:

`python frozen_alpha_issue93_bounded_json_oracle_v1_20261031.py alpha_issue93_unicode_scalar_guard_v3_20261031.py alpha_issue93_bounded_json_guard_v4_20261031.py`

Result: **15/15 expected outcomes** (6 positive, 9 negative). Boundary control: valid JSON exactly 4 MiB accepted; 4 MiB + 1 byte and +100 bytes rejected. Two nested-depth mutations rejected with structured exit 2. Duplicate keys, nonfinite exponent, unpaired surrogate, invalid UTF-8, and count drift rejected. Valid owner/non-owner labels, valid Unicode, and finite floats retained their expected descriptive behavior.

**Before/after metrics:** V3 accepts the oversized +1 byte fixture (false accept **1/1**), V4 rejects it (**1/1**). V3 returns unstructured traceback for the depth fixture (**1/1**), V4 returns structured `FAIL_CLOSED` (**1/1**). These denominators are the deliberately targeted synthetic fixtures, not project-wide incident rates or Handoff success rates. The complete 46-case earlier regression suite was **not rerun** for V4; no claim is made that it passed.

## Byte identity and falsifier

- Frozen oracle: 3,692 UTF-8 bytes; SHA-256 `90bb84a98760131b7d1fcfe4fda2a7ce82defacbf00c01f521f3fc118d542de0`; Git blob `dc174d900724d111e3a360b1340a4e05f9d8cfbd`.
- V4 candidate: 1,213 UTF-8 bytes; SHA-256 `9fe29bc6e49cbc16b0395e4a883829b9d46f658c4ba2c713818948a11dd0cbc8`; Git blob `c414358a03968f604842e6425316437d041afcff`.

**Falsifier:** A V4 run that accepts a byte input longer than 4 MiB, returns an unstructured crash on the depth fixture, or rejects the exact-limit positive control disproves this bounded improvement. Further limitations: the 4 MiB ceiling is an engineering choice, not a proven safe maximum for future full Issue #93 inventories; deeply nested JSON remains rejected rather than processed; no authenticated or atomic GitHub snapshot is proven; Python runtime memory cannot be globally bounded by this input guard.

## R10, denominator, and scope

At observation, Issue #93 contained 239 normalized comments, all owner-authored; R10 PR #115 was open and its discussion had no independently authenticated expert return. Its pinned detached manifest was physically retrievable at `539d4bb33d2ba2c4895713c1bc437ece0743eeea` with Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`. No external actor registration or R10 merge.

`AUTOMATION_RATE=NOT_COMPUTABLE` and `FULL_READBACK_RATE=NOT_COMPUTABLE` at project level: authenticated eligible handoff/publication denominators are not available. The 239 comments and 15 synthetic tests are not denominators for those objectives. This report does not assert actual WWW parity, a new runtime, a biological experiment, a claim promotion, or independent external scientific validation. GitHub PR/CI, actual merge/main readback, and append-only Issue #93 receipt require separate verification after publication.
