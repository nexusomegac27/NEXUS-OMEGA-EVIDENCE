# AXIOM Alpha-Node: PR #184-#190 cumulative original-byte census (2026-10-29)

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_PR184_190_CUMULATIVE_ORIGINAL_BYTE_CENSUS_20261029_R0
DECISION=KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=5a02976c63067f451bbac111f8d7ff287671dc54
PREDECESSOR_ISSUE93_RECEIPT=6489508368

## Scope and outcome

The previously incomplete retrospective cumulative original-byte audit of PR #184 and #186-#190 was completed against immutable main 5a02976c63067f451bbac111f8d7ff287671dc54. Six PRs were merged and each had three additive files. PR #185 was OPEN/UNMERGED and excluded as a negative control.

All 18 original UTF-8 files (80,397 bytes total) were fetched from GitHub. For each, the independently recomputed byte count, SHA-256 and Git blob SHA-1 matched its exact-key Issue #93 receipt, and the computed blob SHA-1 matched GitHub's file API SHA: 18/18 for each of four checks. The SHA algorithms passed known abc test vectors. All six immutable merge commits had matching direct parents, GitHub-reported valid signatures and exactly three additive files with no modifications or deletions.

## Merge and receipt bindings

| PR | Merge SHA | Issue #93 receipt |
|---|---|---|
| 184 | 05748765ab35d87d6bfa79377a97d7c0ff2c2807 | 6485768210 |
| 186 | 3c68b978d2d3273c4684b2dafa33dfac5376cc7e | 6486339190 |
| 187 | 09f517e544056c7217a800f1f596cedb356db2c2 | 6486832437 |
| 188 | 8b7ac2a34175f520f7fd9c1fe738cb902f0e6c41 | 6487895710 |
| 189 | 1208a338714c78951371fa431e13261726c6b590 | 6489031228 |
| 190 | 5a02976c63067f451bbac111f8d7ff287671dc54 | 6489508368 |

The six cited receipts at https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93 contain exact per-file paths, byte lengths, SHA-256 and Git blob IDs. This report does not rewrite or replace them.

## Separate evaluation and falsifier

A separate in-session Python evaluator checked a fixed 7-PR observation snapshot. Positive control 1/1 PASS. Six mutations were rejected (6/6): missing receipt, changed SHA-256 match flag, changed blob match flag, wrong byte count, false merge of PR #185, and duplicate receipt. The Python evaluator did not independently fetch or hash the source bytes, and was not frozen before this run or third-party validated.

Falsifier: any independently retrieved file differs from its receipt, a receipt is absent or duplicated, a merge parent differs, or PR #185 is counted as merged.

## Before / after and limits

Retrospective cumulative audit: 0/18 completed before this run, 18/18 after this run. The previous individual PR readbacks remain historical evidence, not zeroed. This 6/6 PR slice is NOT the full project denominator. Projectwide eligible handoff automation numerator/denominator = UNKNOWN/UNKNOWN; projectwide publication readback numerator/denominator = UNKNOWN/UNKNOWN; both rates NOT_COMPUTABLE. No production integration, new worker, pipeline, runtime, Hostinger or WWW change. No claim promotion.

R10 PR #115 remained open, with zero PR comments, reviews and review threads observed. No new independently authenticated expert return found in the checked PR/Issue #93 surfaces. Original R10 manifest SHA-256 was not rehashed this run. INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED.

This is source-scoped C1 descriptive provenance evidence. GitHub hashes and signatures do not establish scientific validity, independent external authentication or GitHub-to-WWW parity.
