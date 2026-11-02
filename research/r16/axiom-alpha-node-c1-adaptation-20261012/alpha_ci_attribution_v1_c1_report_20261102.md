# NEXUS OMEGA — AXIOM Alpha-Node — CI check attribution V1 — 2026-11-02 — C1

OBJECT = NEXUS_OMEGA_ALPHA_CI_HEAD_ATTRIBUTION_AND_SCIENCE_COVERAGE_V1_20261102_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = bae9dc84fe030cf3214c55edd1d646640efc3811
PREDECESSOR_PR = 289
PREDECESSOR_ISSUE93_RECEIPT = 6575253285
FROZEN_EVALUATOR_FIRST_COMMIT = aac3880b798750cd9a265646b4636ea0b6b68f19
CANDIDATE_SECOND_COMMIT = 0406b7263ed759194216d499051575de8993d845

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The actual GitHub main was read at the pinned SHA above, including AGENTS.md, GOVERNANCE.md, the Alpha-Node contract, operator publication rule, task anchor, external actor registry and repository order policy. PR #289 is merged into that main SHA. Latest Issue #93 receipt before this run was #6575253285; all 270/270 comments were owner-authored.

PR #289 immutable head = 1d95422ce7ca4651478668c6e867473d959ed3e6. The GitHub check-run API returned 8/8 completed-success checks, all 8/8 with exactly this head SHA. Six workflow runs were reported, plus a Semgrep check. Six checked-in workflow YAML files were independently fetched from pinned main, totaling 9,252 UTF-8 bytes. Independent JavaScript SHA-256 passed the empty and abc known vectors. The six original source bindings were:

| .github/workflows/ file | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| validate-external-agent-pr.yml | 1784 | 7c75b82bc022fed1129adea0322f0cfb90e601e35626e90d85d1974630d6326c | 065cf5b248d2ed4be6f3be3440da0289cc23e4c0 |
| validate-scientific-ledger.yml | 919 | c64e4967901c86b65b0bfb1ccdde77305621e420924687e560366d28b183ce2c | 787cc06380be6b3981ba2ab0fd20e53cb13881b4 |
| validate-repository-structure.yml | 2207 | 42d0c3c1d314fa95a84859e3ae07743272fcd8e2be817780543992baacaac55f | 7dae4e8eb4705421e801ce109a46fe41632c115e |
| validate-scientific-communication.yml | 1126 | beed2aae5db97e47776cfcc91b3b3b1c4b9d8f7c0fe80701cd733002dfb15a5f | 082979fd7531b22873f0a93a8418a5e7d5b6693a |
| validate-a83-framework-hardening.yml | 2078 | 8c2bf1b279707e78ed96f56091c4e82faef887b456d08c1bb484c366e404cea1 | b03b029f7c168ac80ae42f3a40a3ad9481c367a7 |
| validate-anchor.yml | 1138 | 1cbaced667407db1edecdce713c75c9ad10e155a81cc15f5eb70e2c941fb61a3 | 3ab2bfecc4949cf23bc9ea1eafeb65c342cf0b0e |

EXPLICIT_V6_FROZEN_EVALUATOR_REFERENCE_IN_WORKFLOW_YAML = 0/6.
V6 evaluator = frozen_alpha_cohort_decode_budget_evaluator_v6_20261102.py.
This does not establish absence of indirect execution. Actual V6 scientific evaluator execution through GitHub CI = NOT_ESTABLISHED. The previously reported local 12/12 V6 synthetic tests remain distinct from green GitHub checks.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

A naive classifier that equates all green checks with scientific validation accepts checks from a different commit. Two frozen wrong-head fixtures (one or all eight head_sha fields replaced by another 40-hex SHA) were accepted 2/2 by the naive all-success classifier in local Python. A green check set without explicit target evaluator references is also not evidence of target execution.

## ISOLATED CANDIDATE / INDEPENDENT TEST

Frozen evaluator committed FIRST at aac3880b798750cd9a265646b4636ea0b6b68f19: frozen_alpha_ci_attribution_evaluator_v1_20261102.py, 2,908 bytes, SHA-256 6d4fab6ca23fbf9405e1823009170a097e385725b0a45d8d161dea400053c4f4, Git blob 29b7ebadd3db2d34f426604e33d443439eefa07d.

Candidate committed SECOND at 0406b7263ed759194216d499051575de8993d845: alpha_ci_attribution_guard_v1_20261102.py, 2,310 bytes, SHA-256 04a79fd3df4264fd89e30495ed5bbdf5982229adee9dd6fea678db3216aebb64, Git blob 79c21bbe315e4e37b94ea11db447ec7204e7e9de.

The frozen evaluator was not modified after candidate authoring. Its 12/12 synthetic Python cases passed on the actual candidate, including wrong-head, failed/neutral checks, malformed inputs, self-asserted science pass, comment-only workflow reference, and no explicit target reference. Both wrong-head fixtures were rejected 2/2 by the candidate versus 0/2 by naive baseline. Separate independent JavaScript classification on actual GitHub API check records and original YAML sources yielded CI_GREEN_NO_EXPLICIT_TEST_REFERENCE, 8/8 correct head SHA, 8/8 green, 0/6 explicit target references. Python was not run on the live GitHub records; these two evaluations are separate.

Reproduction from this existing R16 research directory:
python frozen_alpha_ci_attribution_evaluator_v1_20261102.py alpha_ci_attribution_guard_v1_20261102.py

## FALSIFIER / SCOPE

If all provider check-run records, head fields and workflow sources are jointly forged, the guard can accept the self-consistent inputs. It cannot authenticate GitHub or certify scientific execution. A comment containing the target filename is only a reference, never an execution proof. Actual trusted job logs could disprove a broader claim that V6 was never run; no such claim is made. The guard never returns SCIENCE_PASS. No production CI integration or runtime update occurred.

## R10 PASSIVE SIDE READ — NOT A SECOND CANDIDATE

PR #115 remains OPEN, current owner head dab7c59070d67e7e2a244bd6d05db9a4d37460e3, 9 ahead / 0 behind original SEND 539d4bb33d2ba2c4895713c1bc437ece0743eeea. Original and current detached R10 manifest bytes match: 4,588 UTF-8 bytes, SHA-256 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc, Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df. PR comments/reviews 0/0; Issue #93 270/270 owner-authored. Owner-mediated expert texts exist; independent authenticated receiver ACK, actual expert execution and scientific adjudication NOT_ESTABLISHED. External actor allowlist remains empty. No R10 write or merge.

## DECISION / LIMITS

TESTED_IMPROVEMENT_C1_ISOLATED means only two wrong-head synthetic CI attribution errors are now fail-closed and CI-versus-science scope is explicit. It does not prove actual V6 Python E2E on 36 source files. This report is authored BEFORE PR CI, merge, actual main readback and append-only Issue #93 receipt; those are separate gates. Project-wide 90% automation and 100% publication-readback rates remain NOT_COMPUTABLE (full authenticated numerators and denominators unavailable). No new automated handoffs, pipeline, worker, evaluator self-approval, production integration, Windows node, Hostinger/WWW change, historical overwrite, or claim promotion. BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE.
