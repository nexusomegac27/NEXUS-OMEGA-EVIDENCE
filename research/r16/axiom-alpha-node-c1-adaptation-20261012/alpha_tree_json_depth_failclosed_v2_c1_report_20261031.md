# AXIOM Alpha-Node — Git-tree JSON nesting fail-closed V2 (2026-10-31)

```text
OBJECT=NEXUS_OMEGA_ALPHA_R16_TREE_JSON_DEPTH_FAIL_CLOSED_V2_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=5805c4ed63e3d0aad4dffc26cf47d7c1112c39cb
PREDECESSOR_MAIN=1abc0f06dd43553113c0eb1f3099e5e39cfb2879
PREDECESSOR_PR=228
PREDECESSOR_ISSUE93_RECEIPT=6536869554
FROZEN_EVALUATOR_FIRST_COMMIT=a74e282891affd3ab7ba7a0a4aeb10941370e9ed
ISOLATED_CANDIDATE_SECOND_COMMIT=1322a2f8c97c42519432d60a5ee5272011d86566
PRODUCTION_INTEGRATION=NO
```

## OBSERVE → ORIGINAL_BYTES / PROVENANCE

Read the actual GitHub `main` at the pinned SHA above, `AGENTS.md`, `GOVERNANCE.md`, the Alpha-Node adaptation contract, owner publication directive, task-anchor norm, repository order policy, research/pipeline README, external write-slot registry, and Issue #93. The last Issue #93 receipt is `6536869554` (PR #228). R10 PR #115 remains a distinct passive observation lane.

The prior Python tree-closure candidate `alpha_source_git_tree_closure_v1_20261031.py` at immutable `main` is **4,634 UTF-8 bytes**, SHA-256 `41ba3417f2f5c52e81722d60dabc89a85da41c380880ae228716fc166abff8d1`, Git blob `1b4f58153ce0d6a9e4fd86ee980ce57981dbb1eb`. A local byte-exact copy independently matched both SHA-256 and Git blob. The original V1 remains unchanged.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

H0: a bounded input size does not guarantee a structured JSON failure envelope. Deeply nested, syntactically valid JSON under the 1-MiB input cap can exceed CPython's JSON parser recursion limit. The original V1 catches `ValueError` etc., but not `RecursionError`, so downstream automated consumers receive an uncaught traceback and no machine-readable `FAIL_CLOSED` record.

**Actual falsification of V1's implicit structured-error expectation:** Python 3.13.5, `python -S`, depth 10,000 / 20,000 / 40,000 nested arrays, input sizes 20,001 / 40,001 / 80,001 bytes. V1 returned exit code 1 with no JSON on stdout in **3/3** cases. The valid Git-CLI-built four-hop control passed.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The black-box evaluator was frozen in GitHub commit `a74e282891affd3ab7ba7a0a4aeb10941370e9ed` **before** the candidate commit. It builds the positive four-hop Git tree from Git CLI `git hash-object -t tree --stdin`, runs the candidate via a separate Python subprocess, and checks exact output state, exit code and stderr. It does not import the candidate or allow the candidate to edit its oracle.

- Frozen evaluator: `frozen_alpha_tree_json_depth_oracle_v1_20261031.py`; **3,158 bytes**, SHA-256 `ab8abac1d400dd6e491d74e452fde23a36b98df730834f880c44f8dd5e5deb82`, Git blob `6d033e222b0de087f6be704d1442c5c72574738c`.
- V2 isolated candidate: `alpha_source_git_tree_closure_depth_guard_v2_20261031.py`; **4,774 bytes**, SHA-256 `cf07ecd9192f5e0455b21a9262376ef0cacc2a01bd73694141064f5119fe93fc`, Git blob `eb4584cc8c53dc645dabc68d3089ad9b773c08d3`.
- V2 adds only an explicit `RecursionError` branch returning exit code 2 and `{"state":"FAIL_CLOSED","reason":"JSON_NESTING_LIMIT"}`. All original parsing and tree-identity rules remain byte-identical.

Local separate black-box test: **11/11 PASS**, consisting of **1/1 positive Git-CLI four-hop control** and **10/10 negative controls FAIL_CLOSED** (three deep JSON arrays; duplicate keys; nonfinite JSON; malformed JSON; wrong root; invalid UTF-8; wrong top-level type; oversized input). Git 2.47.3 and Python 3.13.5. The original V1 failed the frozen oracle on the first depth control, as expected.

| Measured metric | V1 baseline | V2 tested |
| --- | ---: | ---: |
| Deep-nesting negatives with structured fail-closed JSON | 0/3 | **3/3** |
| Valid synthetic Git-tree control accepted | 1/1 | **1/1** |
| Frozen independent evaluator full suite | FAIL (depth) | **11/11 PASS** |
| Real 43,911-byte R16 API projection through Python candidate | NOT_EXECUTED | **NOT_EXECUTED** |
| Productive integration / independent root authority | NO / NOT_ESTABLISHED | NO / NOT_ESTABLISHED |

**Falsifier:** if any of the three depth fixtures produces exit code other than 2, an unparseable stdout envelope, stderr traceback, or reason other than `JSON_NESTING_LIMIT`, the robustness claim fails. If the valid four-hop control is rejected, the candidate regresses. This tests error-envelope reliability, not cryptographic authority or scientific correctness.

## DECISION / SCOPE

`TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE`. This is a measurable local reliability repair, not a production fix. The prior real-projection Python end-to-end gap remains open. GitHub CI, actual main publication and Issue #93 receipt must be checked independently after the PR; do not infer them from this report. The complete project-wide 90% automated handoff and 100% publication readback rates remain `NOT_COMPUTABLE` because authenticated full denominators including failed eligible attempts are missing; local tests are excluded from both numerators.

R10 remains separate: `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`. No new independently authenticated return was present in the checked PR #115 conversation/reviews/threads or Issue #93. The external actor allowlist remains empty.

No new pipeline root, workflow, automation, worker, Cursor dispatch, runtime/Hostinger/WWW change, historical overwrite, evaluator self-approval, R10 merge, biological experiment or claim promotion.

Reproduce from a checkout:

```bash
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_tree_json_depth_oracle_v1_20261031.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_source_git_tree_closure_depth_guard_v2_20261031.py
```
