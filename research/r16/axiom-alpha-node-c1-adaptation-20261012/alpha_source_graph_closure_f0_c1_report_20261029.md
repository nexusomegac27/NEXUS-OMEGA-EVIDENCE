# NEXUS OMEGA · AXIOM Alpha-Node · F0 source-graph closure C1 candidate · 2026-10-29

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_SOURCE_GRAPH_CLOSURE_F0_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=09f517e544056c7217a800f1f596cedb356db2c2
PREDECESSOR_ISSUE93_RECEIPT=6486832437
DESIGN_INPUT_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/185
DESIGN_INPUT_HEAD=68886fa89937de25edd38220f5242bc43e54554b
DESIGN_INPUT_PATH=docs/architecture/NEXUS_GITHUB_EXPERT_EXCHANGE_V1_DRAFT.md
DESIGN_INPUT_BYTES=5933
DESIGN_INPUT_SHA256=7efaa6504e0f6a4697472f7bb12860b654621ef6a8d9387deeda820c065c07e3
DESIGN_INPUT_GIT_BLOB=943d0bddd557d5c823aaa218ca86e4a77f26d639
DESIGN_PR_STATE=DRAFT_OPEN_UNMERGED
FROZEN_ORACLE_FIRST_COMMIT=668a47f4b02ae4343f01f455119d56c5ca077cc1
CANDIDATE_INITIAL_COMMIT=67c2f5500feaf486e0ae370269583d8e4453afcf
CANDIDATE_SYNTAX_CORRECTION_COMMIT=cf56baeed85c271616308fc658661f0362097856
PRODUCTION_INTEGRATION=NO
EXTERNAL_DISPATCH=NO
R10_PR115_MERGE=NO
WWW_PARITY=NOT_ESTABLISHED
```

## Observe, source and negative hypothesis

The physically retrieved draft PR #185 introduces a staged F0 offline archive/source-closure verifier before any expert dispatch. It is an **owner draft**, not a merged authorization or operational worker. The repository's R16 handoff metric witness already demonstrates synthetic arithmetic, but does not prove an authenticated inventory or the completeness of source dependencies. No existing F0 source-graph byte-closure executable was found in the scoped R16 candidate inventory. The absence of a found executable is not proof that no similar tool exists anywhere.

**Negative hypothesis:** A task appears ready when a manifest lists all required parents but a required source is missing, cyclic, private, unpinned, or has mismatched byte/hash bindings. A URL or owner assertion cannot cure these conditions.

**Falsifier:** If the frozen evaluator finds acceptance of a missing required parent, cyclic dependency, changed SHA-256, changed Git blob, changed byte count, unpinned commit, unsafe path, non-public input or duplicate identity, F0 fails. A future actual receiver must independently fetch source bytes before any READY_FOR_EXPERT state is permitted.

## One isolated candidate and independent test

Only three additive research files in the existing R16 Alpha-Node lane are proposed:

- `frozen_source_graph_closure_f0_oracle_v1_20261029.py` — 4,668 bytes, SHA-256 `e5373fe0c61c8cde7bd8da439fe03f735403686d98e460a115f5ed95ef4b3fb6`, Git blob `2f8adc62a778a5662b4b82f2ab18730d2e311ab6`; committed first.
- `alpha_source_graph_closure_f0_v1_20261029.py` — 5,274 bytes, SHA-256 `c39208bffdc60ef8072cc7fb82a8aead459870f840e4ff7c9a0e4f79a59e051b`, Git blob `0a156f3b0044b1f389237e53e8a3175f13f2483a`; committed after evaluator, with one pre-PR syntax correction recorded as an additional commit.
- This report; append-only, not a rewrite of PR #185 or existing source.

Reproduction in the same directory: `python frozen_source_graph_closure_f0_oracle_v1_20261029.py -q`. The frozen evaluator invokes the candidate through a separate Python subprocess, without importing candidate code or sharing its validation helpers.

**Observed local result:** 22/22 oracle tests PASS, including three positive controls and 19 targeted invalid/negative controls. A negative mutant that bypassed the SHA-256 check yielded 21/22 PASS and one expected failure (test_07), demonstrating oracle sensitivity. The mutant was not published. Test execution was in an isolated local sandbox, not a GitHub-hosted or independent third-party runtime.

**Before/after:** No F0 executable was established as a baseline, so no valid numerical before/after improvement rate exists. After: 22/22 synthetic oracle checks pass. The bounded synthetic example checks three source nodes and two required edges. This does not prove a reduction in operator file hunts, an achieved 90% handoff rate, or a complete real-source census.

## Safety and provenance boundary

The candidate accepts caller-supplied base64 bytes and validates transitive parent closure, size, SHA-256 and Git blob SHA-1, strict JSON, paths, rights/public-safe flags and cycles. It does **not** fetch GitHub bytes itself, authenticate API origin, verify that rights flags are true, prove source completeness outside the declared graph, authenticate an external actor, or establish receiver execution. Output always sets `ready_for_expert=NOT_ESTABLISHED`, `receiver_ack_established=false`, `api_origin_authenticated=false`, `expert_research_executed=false`.

The draft's requested **real operator-provided missing-path regression is NOT_EXECUTED**; only a synthetic missing-parent fixture was tested. No new worker, webhook, ZIP courier, task anchor publication, pipeline root, Hostinger write, Windows node action, CI workflow or scientific claim promotion.

## R10 and project-wide metrics

R10 PR #115 is still OPEN, owner-authored and without new independent PR discussion/review evidence in this check. Its original manifest at head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` remains source-pinned; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED` and `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. The empty external actor registry remains decisive.

`PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_READBACK_RATE=NOT_COMPUTABLE` because the authenticated complete numerator and denominator including failed/absent handoffs are unavailable. No private or inaccessible material is counted as automated. This research candidate is not an eligible completed expert handoff.

**Publication and verification:** This pre-merge report makes no claim that CI, merge, actual main readback, or Issue #93 receipt have already occurred. Those are separate gates. `BLOCKED_LANE != BLOCKED_SYSTEM`, `DRIFT_RESET=NON_DESTRUCTIVE`, `C1_DESCRIPTIVE_ONLY`.
