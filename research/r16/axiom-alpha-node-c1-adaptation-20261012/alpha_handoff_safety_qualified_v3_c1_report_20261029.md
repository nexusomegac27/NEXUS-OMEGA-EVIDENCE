# AXIOM Alpha-Node — safety-qualified handoff sample metrics V3 · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_SAFETY_QUALIFIED_V3_20261029_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 469972ecd376b1babeb005cc44ed5dfa0de52022  
MAIN_PARENT = 3df2b6bf7849284d96e07b5f50b528aeda5a345d  
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/202  
PREDECESSOR_ISSUE93_RECEIPT = 6508787857  
PUBLICATION = BRANCH_PR_PENDING_AT_REPORT_AUTHORING  
PRODUCTION_INTEGRATION = NO  
WWW_PARITY = NOT_ESTABLISHED

## Source and scoped authority

Read current main, GitHub commit/parent and the latest Issue #93 receipt from the GitHub API; read `AGENTS.md`, `GOVERNANCE.md`, `docs/AI_CONTEXT.md`, `docs/agent-protocol.md`, `docs/architecture/REPOSITORY_STRUCTURE.md`, `docs/governance/REPOSITORY_ORDER_POLICY.md`, `docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md`, `docs/governance/NEXUS_OMEGA_TASK_ANCHOR_NORM_V1.md`, the R16 Alpha contract and the R27-E external write-slot registry. The authenticated owner is `nexusomegac27`; the external actor allowlist is empty. Existing research directory reused; no new root, pipeline, worker, or external slot.

The V2 original at pinned main `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_denominator_guard_v2_20261029.py` was reconstructed as **4,759 UTF-8 bytes**, independently SHA-256 `3028c3dfa23ad2e267cddf7e56c7a2f18ef55bdc171ec9c45036061d03fb7148`, Git blob `6a725d1f014910c1a23a3d7ec4f227188abd6696`: **MATCH**. Historical V2 unchanged.

## One candidate, negative hypothesis and falsifier

V2 already records `reported_violations` and `safety_status=VIOLATION_REPORTED`, but its **nominal** `automated_success` and `full_readback` can still equal 1/1 when the same caller-supplied row declares `concealed_source_gap=true`, `unauthorized_write=true`, `overwrite=true`, or `claim_promotion=true`. This is not a V2 failure to flag violations; it is a potential metric-conflation error if nominal automation/readback is presented as *safety-qualified* progress.

Hypothesis: preserving the original V2 arithmetic while separately reporting `safety_qualified_automated_success`, `unsafe_automated_success`, `safety_qualified_full_readback`, `unsafe_full_readback`, and their declared-cohort ratios makes the distinction machine-readable. The new fields are **reported-input arithmetic**, not independently authenticated safety facts.

Falsifier: V3 gives safety-qualified 1/1 on a single otherwise eligible, delivered, automatically completed and fully read-back handoff with any violation flag; V3 changes any legacy V2 output field on identical input; V3 promotes a synthetic sample to a project-wide rate; or V3 accepts a missing declared attempt.

## Frozen independent evaluation and measured delta

1. Frozen evaluator committed **before** candidate: `frozen_handoff_safety_qualified_oracle_v3_20261029.py`, **5,775 bytes**, SHA-256 `b143a3f6c9d4adacc0947b57b2b94b65939b1601378a5932014b15e7e7944c2f`, Git blob `ba2484285c0f07e492d66013e266a21911682192`; first branch commit `a7d0e9e582df275bb6382a3d3b8196bbd0c50a82`.
2. V3 candidate committed second: `alpha_handoff_denominator_guard_v3_20261029.py`, **5,664 bytes**, SHA-256 `5fc12dbf825e9b0ab0057e393bc6a644512e8ffce9bf04a239b5385c445c7f1c`, Git blob `407b6eea176d23a6d8cdbe8a4b9d19cf9db23638`; second branch commit `95e7b277cee2b03207e97094e9c08ff021c45320`.
3. Command: `python frozen_handoff_safety_qualified_oracle_v3_20261029.py -q`. Isolated Linux Python subprocesses, same pinned V2 reconstructed original and V3 candidate: **16/16 PASS**, 12.387 seconds. This is an internal independent-process evaluator, not an external third-party audit. Published Git blobs of evaluator and candidate independently matched the locally tested bytes.
4. **Negative fixture:** one eligible, delivered, automatic, published, fully read-back handoff declaring `concealed_source_gap=true`. V2: nominal automation `1/1`, full readback `1/1`, and `reported_violations=1`. V3: nominal automation still `1/1`, but **safety-qualified automation `0/1`** and unsafe automated count 1. With `overwrite=true`, V3 safety-qualified readback is **0/1** while nominal readback remains `1/1`.
5. **Positive controls:** two clean handoffs yield safety-qualified `2/2`; manual nudges remain excluded; all four violation flags, unauthorized publication, incomplete readback, zero denominator, duplicate IDs, missing attempts, incomplete cohort and no project-rate promotion were checked. Legacy V2 fields preserved in an explicit regression fixture.

## Decision and limits

**TESTED_IMPROVEMENT** is limited to a separate, falsifiable sample-accounting signal on caller-declared inputs. It does not demonstrate an unauthorized GitHub write, a concealed real-world gap, or a project-wide rate. The declaration `scope_complete=true`, the safety flags and all four readback flags are unauthenticated; an omitted attempt absent from both declared and observed lists remains invisible. Neither V2 nor V3 authenticates the source population. Therefore `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`, `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`, and `GLOBAL_ZERO_VIOLATIONS=NOT_ESTABLISHED`. Production integration, WWW receipts, external scientific validation and runtime changes remain **NO**.

R10 passive check: PR #115 remains open; current owner head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, historical pinned head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`, detached manifest 4,588 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. At this check: zero PR comments, reviews and review threads; Issue #93 recent receipts were owner-authored Alpha-Node records. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. No new R10 expert-original return is claimed.

`BLOCKED_LANE != BLOCKED_SYSTEM`  
`DRIFT_RESET = NON_DESTRUCTIVE`  
`CLAIM_CEILING = C1_DESCRIPTIVE_ONLY`
