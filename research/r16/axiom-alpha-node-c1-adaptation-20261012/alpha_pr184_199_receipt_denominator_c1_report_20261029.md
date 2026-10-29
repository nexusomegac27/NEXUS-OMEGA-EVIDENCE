# AXIOM Alpha-Node — bounded GitHub PR/receipt denominator census · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_PR184_199_RECEIPT_DENOMINATOR_CENSUS_20261029_R0
DECISION = KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 2b3e27383d7d86e9742af00d39e8c6e2e70c59f1
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/199
PREDECESSOR_ISSUE93_RECEIPT = 6504918426
FROZEN_EVALUATOR_FIRST_COMMIT = c14540c6a162b2cfa1994a1aa0ce1b85ad79ccd3
API_SNAPSHOT_SECOND_COMMIT = 124af45fcb4a4e60a218c1d75a57b43504629246
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## OBSERVE / physical API source and provenance

The GitHub API returned main at the pinned SHA above, the repository governance and R16 Alpha-Node contract, Issue #93 with 189 comments, PR #115 and the exact 16 PRs numbered 184 through 199. PR #185 remained open; the other 15 PRs were merged. For each merged PR, the independently queried Git Commit REST object reports a valid GitHub signature and a direct-parent link in a contiguous 15-commit chain, ending at the pinned main. The first commit's parent is 623ac73ae19f7000cabb050066667e0eff49e5a8.

All 15 merged PRs have one exact-key owner Issue-#93 receipt: the receipt's own PR URL and ACTUAL_MAIN_READBACK SHA match the PR's actual GitHub merge SHA. Each of the 15 individual GitHub REST issue-comment objects was retrieved separately: actor nexusomegac27, author_association OWNER, and created_at equals updated_at at observation time. PR #185 was not counted as merged or as having a receipt. A predecessor PR reference in another receipt is not the receipt's own PR attribution.

The accompanying JSON snapshot is normalized, derived GitHub API metadata, NOT original response bytes or a permanent immutable archive of mutable GitHub comments. It contains the 16 explicit PR rows, the 15 receipt IDs, merge SHA and parent SHA, signature result and timestamps. To reproduce, re-fetch GitHub REST /pulls/{pr}, /git/commits/{merge_sha}, and /issues/comments/{receipt_id} for nexusomegac27/NEXUS-OMEGA-EVIDENCE and compare to the snapshot. The source bytes of every research file across these 15 PRs were NOT rehashed in this iteration; earlier byte censuses remain separately scoped.

## NEGATIVE HYPOTHESIS / independent evaluator

A reported 100% publication-readback ratio may be inflated by silently excluding a failed publication, counting an open PR, treating PREDECESSOR_PR as PR, accepting mismatched SHAs, duplicate or edited receipts, another actor, invalid GitHub signature or a broken parent chain. The separate frozen evaluator was committed before the snapshot and report. Local execution against the byte-identical versioned JSON and evaluator yielded 12/12 PASS: one positive 16-row real-API metadata snapshot plus 11 distinct fail-closed mutations (missing receipt, wrong SHA, predecessor misattribution, duplicate receipt, wrong actor, edited receipt, invalid signature, broken parent, missing PR, unmerged PR counted as merged, and receipt predating merge).

Reproduce: python frozen_alpha_pr184_199_receipt_census_oracle_v1_20261029.py alpha_pr184_199_api_receipt_snapshot_c1_20261029.json

Falsifier: any of the above 11 mutations accepted as 15/15 invalidates the scoped evaluator result. This is a local independent test file and not external third-party scientific validation. The evaluator checks the pinned metadata snapshot, not direct GitHub API authentication on its own.

## PINNED BASELINE / BEFORE → AFTER

| Metric | Before this scoped census | Observed after |
|---|---|---|
| PRs explicitly enumerated in range #184–#199 | NOT_MEASURED_AS_ONE_POPULATION | 16/16 |
| Actually merged in that range | NOT_MEASURED_AS_ONE_POPULATION | 15/16, PR #185 excluded |
| Exact owner receipt/merge-SHA matches | NOT_MEASURED_AS_ONE_POPULATION | 15/15 |
| Verified GitHub signatures / first-parent chain | NOT_MEASURED_AS_ONE_POPULATION | 15/15 / 15/15 |
| Receipts unedited at read time | NOT_MEASURED_AS_ONE_POPULATION | 15/15 |
| Source and test original bytes for all 15 PRs | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Eligible public routine handoff attempts including failures | UNKNOWN | UNKNOWN |
| Project-wide handoff automation / full-readback rates | NOT_COMPUTABLE | NOT_COMPUTABLE |

The 15/15 result establishes ONLY bounded GitHub PR/receipt/commit metadata consistency, NOT full commit/source/test/receipt readback for every publication, project-wide 100%, 90% automation, independent external expert work or zero project-wide unauthorized actions. A coherent but fabricated owner receipt remains a counterexample. GitHub comments can be edited later; created_at == updated_at describes this snapshot, not immutable content.

## R10 auxiliary readback

PR #115 remains open with no new PR discussion comments, review submissions or review threads. PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED. Historical R10 detached manifest original bytes were not rehashed in this run. No R10 merge, worker, Cursor dispatch or external registration.

## DECISION

One append-only, public-safe research census with an actual bounded denominator and negative controls. No changes to historical sources, independent oracle after freezing, runtime, Hostinger, WWW, permissions, model weights or scientific claim ceiling. BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE; C1_DESCRIPTIVE_ONLY.
