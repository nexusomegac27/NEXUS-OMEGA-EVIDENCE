# AXIOM Alpha-Node — Issue #93 receipt ↔ GitHub PR chain audit V1 (C1, 2026-10-30)

```text
OBJECT=NEXUS_OMEGA_ALPHA_ISSUE93_RECEIPT_PR_CHAIN_AUDIT_V1_20261030_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=1d31c841cbd4c25cbe5550177a17cc5638f57667
PREDECESSOR_PR=221
PREDECESSOR_ISSUE93_RECEIPT=6527434004
ORACLE_FIRST_COMMIT=55d9d45b4d4854530debe5bc37eb00deff3718fd
DATA_SECOND_COMMIT=703b0cea0795d0d4e463feb58bdf934b32829c2d
EXTERNAL_ACTOR_ALLOWLIST=EMPTY_AT_OBSERVATION
PRODUCTION_INTEGRATION=NO
```

## OBSERVE → ORIGINAL_BYTES/PROVENANCE → NEGATIVE_HYPOTHESIS

At the pinned GitHub main, Issue #93 had **211 comments**; the last ten owner-authored Alpha-Node receipts were IDs 6517745738 through 6527434004 and referenced PRs #212–#221. GitHub PR metadata was independently fetched for each PR, and GitHub compare API was separately queried for each receipt's claimed predecessor and main SHA. The source of this snapshot is the GitHub connector, not a ChatGPT/agent summary. These are **API-provided observations**, not raw cryptographic Git objects or a third-party witness.

Negative hypothesis: a self-reported `ACTUAL_MAIN_READBACK=...` and `PR_SQUASH_MERGED=TRUE` inside an Issue comment can be false, inconsistent with the actual PR merge commit, or linked to a predecessor that was not the prior observed main. A comment is not its own independent verification. Checking only the receipt text cannot detect that defect.

The frozen independent oracle contains the ten PR/receipt/commit/file-count expectations gathered from the API before the candidate JSON was committed. The candidate JSON separately records each Issue #93 receipt claim and the corresponding GitHub PR and compare API observations. Both are fixed to the exact 2026-10-30 snapshot; the tool is **not** a production GitHub crawler.

## PINNED_BASELINE → ISOLATED_CANDIDATE → INDEPENDENT_TEST

| Fixed-snapshot metric | Prior evidence | This candidate |
|---|---|---|
| Cross-run Issue receipt ↔ PR API ↔ compare API ledger | Not established as a single frozen independent test | **10/10 rows consistent** |
| Receipt-claimed main SHA vs PR API merge SHA | Per-receipt assertions existed | **10/10 MATCH** in independently retrieved PR metadata |
| Claimed predecessor vs PR base and preceding receipt main | Not established as a ten-row chain | **10/10 MATCH** |
| GitHub compare API predecessor→merge | Per-receipt claims existed | **10/10 ahead=1, behind=0** |
| GitHub compare API nonadditive paths | Not jointly audited in this sample | **0/34 nonadditive; 34/34 added** |
| Frozen evaluator local run | No oracle for this exact ten-row sample | **18/18 PASS** |
| Real project-wide eligible handoff attempt denominator | UNKNOWN | **UNKNOWN** |

The sample is deliberately selected as the latest ten receipts at cutoff, **not** a representative or complete project-wide census. A row passing means the specific GitHub API views are internally consistent. It does not establish that each published file's original bytes were independently rehashed, that CI was sufficient, that the publisher was autonomous, or that the source API was independently authenticated.

The separate evaluator `alpha_issue93_pr_receipt_chain_oracle_v1_20261030.py` was committed first, before the JSON data. It was run locally using a Python subprocess against the separate JSON file. Observed result: **18/18 PASS** = one fixed real-snapshot positive evaluation and **17/17 negative/parse controls rejected**. Controls include forged repository, claimed main, merge SHA, predecessor, actor, PR merge state, population completeness, claim promotion, omitted/duplicated/reordered receipts, hidden nonadditive changes, boolean-as-integer, duplicate JSON keys and NaN. The evaluator does not import the candidate as Python code and does not perform network calls.

**Falsifier:** if a receipt-claimed main SHA diverges from GitHub PR `merge_commit_sha`, a claimed predecessor diverges from the prior main or PR base, or a compare response contains a nonadditive change, the fixed-snapshot validation must fail. A forged `pr_api_merge_sha` in one candidate row is a real negative fixture and is rejected. A coordinated modification of both the frozen oracle and the candidate, or a compromised GitHub API, is outside this test's security claim.

## REPRODUCTION / MATERIAL IDENTITIES

- Frozen oracle: **6,737 UTF-8 bytes**; SHA-256 `b4b73f5deb9f8898835ee2384a403d5180e4806468ffda40bce599d30289c785`; Git blob `4d5a0ff330f889b45328b3ecd303939b034ba1a6`.
- Fixed candidate JSON: **5,203 UTF-8 bytes**; SHA-256 `a16f417851d6af8d3a95c4b15a6eb3b2028874776cba4f45b3dec4e1e5fd0c22`; Git blob `7fe4b9256411695829d0fe9e1144252bcd35bd03`.
- Command from this directory: `python alpha_issue93_pr_receipt_chain_oracle_v1_20261030.py alpha_issue93_pr_receipt_chain_v1_20261030.json`.
- Source scope: `https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93`; `https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/212` through `/pull/221`; immutable cutoff main `1d31c841cbd4c25cbe5550177a17cc5638f57667`.

## PASSIVE R10 AND GOVERNANCE BOUNDARY

R10 PR #115 remains **OPEN / NOT MERGED** at observation. No new PR conversation comment, submitted review, inline review thread, or non-owner Issue #93 receipt was found. The original detached R10 manifest at immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was freshly retrieved and independently rehashed in JavaScript: **4,588 UTF-8 bytes**, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, MATCH. SHA-256 implementation was checked against empty-string and `abc` known vectors. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

The authenticated project-wide eligible-attempt denominator remains unavailable. Therefore `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. Ten successful historical receipts cannot be relabeled as 90% autonomous handoffs or 100% project-wide readback. Local/private inaccessible returns are not counted as successful automated handoffs. No new worker, scheduler, pipeline root, runtime, Hostinger/WWW write, Cursor dispatch, R10 merge, external actor registration, original-source overwrite, evaluator override or claim promotion.

## PUBLICATION GATE

This document records the isolated candidate before PR/CI/merge. `MAIN_PUBLICATION=NOT_YET_ESTABLISHED` at report authoring. A later verified merge/main readback and append-only Issue #93 receipt are required. This report itself is not a substitute for that readback.
