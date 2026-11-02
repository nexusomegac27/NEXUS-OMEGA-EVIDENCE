# NEXUS OMEGA — AXIOM Alpha-Node — declared CI run classification V2 — 2026-11-02 — C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_DECLARED_RUN_SEMANTICS_V2_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_PREPUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=c22382b1d7326ece4de940d06834ee5e5ba4964b
PREDECESSOR_PR=290
PREDECESSOR_ISSUE93_RECEIPT=6576414292
FROZEN_EVALUATOR_FIRST_COMMIT=b0e05df77af2083a48ffd85f8f843e687d9582f6
FINAL_CANDIDATE_BRANCH_COMMIT=d657e72d556dd06a60fbfe6b31831ec35f5aff56
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

GitHub `main` was physically read at the immutable SHA above; AGENTS.md, GOVERNANCE.md, the R16 Alpha adaptation contract, operator C1 publication directive, task-anchor norm, external actor registry, repository order policy, bootstrap documents and the predecessor PR/Issue #93 were retrieved. The authenticated GitHub writer was the owner `nexusomegac27`. The external actor allowlist was empty. The predecessor V1 source at the pinned main is **2,310 UTF-8 bytes**, SHA-256 `04a79fd3df4264fd89e30495ed5bbdf5982229adee9dd6fea678db3216aebb64`, Git blob `79c21bbe315e4e37b94ea11db447ec7204e7e9de`.

V1 counts `target in workflow_text` as an `explicit_workflow_references` value. This is a **text mention**, not an executable run-step declaration. V1 already correctly refused to attest to scientific execution. Its field name nevertheless risks confusing incidental text with a declared test command. This is a classification-quality gap, not evidence that V1 falsely approved a scientific claim.

Six existing workflow YAML files were separately fetched from pinned main (9,252 UTF-8 bytes; original Git blobs recorded in predecessor report). None of the six contained the target V6 evaluator filename. This observational check does not establish indirect execution or exhaust every GitHub job log.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

A source comment, shell `echo`, YAML environment variable, or unrelated Python module mentioning the evaluator may be mistaken for a declared execution step by a naive text-presence check. Seven fixed negative fixture workflows each contain the target filename but **no direct Python run command**. The actual V1 Python implementation counted text mentions for **7/7**; the V2 Python candidate counted declared run steps for **0/7**. This comparison measures semantic discrimination, not the accuracy of actual CI execution verification.

## FROZEN EVALUATOR / ISOLATED CANDIDATE / INDEPENDENT TEST

Independent Python evaluator was committed **before** candidate authoring and never edited:
- `frozen_alpha_ci_declared_run_evaluator_v2_20261102.py`, first commit `b0e05df77af2083a48ffd85f8f843e687d9582f6`, **3,801 bytes**, SHA-256 `1107ff2c9bfe0439313bbb57aec0e2f9b9d5953db3ea2dc4b4c82a55a20fb17e`, Git blob `d0c2d0ace8236565978e7190ed54b54f4ec9ac7a`.
- `alpha_ci_declared_run_guard_v2_20261102.py`, final tested branch commit `d657e72d556dd06a60fbfe6b31831ec35f5aff56`, **3,230 bytes**, SHA-256 `5b64e7018450a8bc8aac8d1c7708f5739eb1173728ab09db6a71682254bcfa97`, Git blob `9d9f0d834dc2b51eb75ad7d5280c480c0d23082c`.

Two transient candidate-only source-escaping corrections were committed on the **unmerged research branch**, preserving Git history. Only the final candidate blob above was independently tested and is proposed for merge. No historical main source was overwritten and the evaluator's blob remained unchanged.

The frozen evaluator executed against the final candidate bytes in a separate local Python process: **17/17 expected outcomes PASS**, including inline and multiline positive declarations, seven negative text-only controls, wrong-head and failed-check rejection, malformed inputs, and a self-asserted science-pass field ignored. The captured JSON stdout was **3,950 bytes**, SHA-256 `e1a95971188c28771c53582d8b3d3755c261ebdcdd6f6237fb178c1d3a13679d`. The stdout is a local execution artifact, **not** a separately published GitHub CI job-log receipt.

Reproduce from the existing R16 research directory:

```bash
python frozen_alpha_ci_declared_run_evaluator_v2_20261102.py alpha_ci_declared_run_guard_v2_20261102.py
```

V2 uses a conservative dependency-free textual scanner for direct `python`/`python3` commands under YAML `run:` keys. It is **not a complete YAML/shell interpreter**. In particular, aliases, indirect invocations, composite actions, scripts, expressions, here-documents and dynamically constructed commands are not fully analyzed. Every outcome retains `scientific_test_execution=NOT_ESTABLISHED`.

## FALSIFIER / COUNTEREXAMPLE

A workflow can declare `run: python target.py` while the job never reaches that step, the script exits early, or a provider supplies forged records. V2 then reports `CI_GREEN_DECLARED_RUN_NOT_EXECUTION` if its supplied check records are green; it never returns `SCIENCE_PASS`. Therefore the candidate **does not prove actual execution**. An independently authenticated job-step/log readback would be necessary for a stronger but still bounded claim.

## R10 PASSIVE SIDE READ — NOT A SECOND CANDIDATE

PR #115 remained OPEN with zero PR discussion comments and zero reviews in the observed read. The original R10 detached manifest at `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and the current PR head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` have identical Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. Independent JavaScript SHA-256 over fetched original UTF-8 content (empty and abc known vectors PASS) gave **4,588 bytes**, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`. The original SEND is not an independent receiver ACK. Operator-mediated expert reports exist, but `INDEPENDENT_RECEIVER_ACK`, `AUTHENTICATED_GITHUB_ACTOR`, `AXIOM_SCIENTIFIC_ADJUDICATION` and `EXPERT_RESEARCH_ACTUALLY_EXECUTED` remain NOT_ESTABLISHED. No R10 write or merge.

## DECISION / METRIC LIMIT

This is one candidate: a **measured, independently tested reduction in text-mention versus declared-run confusion** for a fixed synthetic set, not a new production check. The bounded improvement is V1 text-only mentions 7/7 versus V2 false declared runs 0/7. Real automated handoff success added: **0 established**. Full project numerator/denominator for the 90% handoff objective and 100% publication-readback objective remain `NOT_COMPUTABLE`. No runtime, CI workflow, Windows node, Hostinger/WWW, external worker, source overwrite, new pipeline, independent-oracle change, biological experiment or claim promotion.

Publication is **not assumed in this pre-merge report**. PR CI, actual merge, immutable main byte/hash/blob readback and append-only Issue #93 receipt are separate required gates. `BLOCKED_LANE != BLOCKED_SYSTEM`; `DRIFT_RESET=NON_DESTRUCTIVE`.
