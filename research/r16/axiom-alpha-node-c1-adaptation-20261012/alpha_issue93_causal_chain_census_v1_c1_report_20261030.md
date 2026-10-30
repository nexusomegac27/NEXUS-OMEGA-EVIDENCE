# AXIOM Alpha-Node - scoped Issue #93 PR/receipt causal-chain census V1 - 2026-10-30

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_CAUSAL_CHAIN_CENSUS_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 79c04d951ba5e0b46dabb698e9a86400c6b64982
PREDECESSOR_PR = 208
PREDECESSOR_ISSUE93_RECEIPT = 6514491213
SCOPE = PR199_TO_PR208_AND_THEIR_TEN_OWNER_RECEIPTS_ONLY
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## 1. One bounded improvement

PR #200 published a scoped metadata census of PR #184-199. This iteration extends causal coverage to the ten consecutive PRs #199-208, including nine PRs outside the prior cohort. The objective is not to improve a percentage by choosing successful PRs. It is to make broken predecessor references, false merge assertions, missing declared receipts, wrong PR heads and a stale final main fail closed in a declared population.

Negative hypothesis: at least one owner receipt or corresponding GitHub PR metadata record in the selected ten-event chain does not agree with its predecessor, PR head, base or merge commit. Falsifier: any single field mismatch or any negative mutation accepted by the frozen evaluator.

## 2. Source and observed results

GitHub API source surfaces were read at this run: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pulls/199 through /pull/208, and https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93 . PR metadata, the ten owner-authored Issue #93 comment bodies, the current main, and the immutable predecessor commits were inspected. The resulting JSON is a derived, bounded API-metadata witness, not a direct copy of raw GitHub HTTP response bytes or an authenticated external expert receipt.

Declared PR population = 10; present PR metadata = 10/10; corresponding owner receipts = 10/10; merge state, head, base, receipt predecessor, and main-commit continuity = 10/10 MATCH. Baseline main before PR199: a2da485b293023a8b687440462b3794a1880bd86. Final actual main after PR208: 79c04d951ba5e0b46dabb698e9a86400c6b64982. Previous Issue #93 receipt: 6504006308; terminal receipt: 6514491213.

This is **not** a proof of a complete handoff-event population, full historical original-file byte validation, external actor authentication, independent expert research, or complete project-wide readback. The Issue comment body strings were retrieved through GitHub but not independently authenticated as raw transport bytes.

## 3. Independent test and frozen oracle

The isolated Python evaluator `frozen_alpha_issue93_causal_chain_oracle_v1_20261030.py` was committed first, before the API-derived witness. It was executed in a separate local Python process. Synthetic selftest: 16/16 PASS (one positive and fifteen negative, including duplicate JSON keys). The exact witness was then evaluated in the same isolated executable: 10/10 PRs and 10/10 receipts MATCH. Five additional real-witness mutations (broken receipt predecessor, wrong merge, omitted row, forged receipt actor and false final main) produced 5/5 expected fail-closed results.

The evaluator checks caller-supplied metadata consistency only. It does not authenticate GitHub or independently validate source bytes. The two new source files were separately checked against their published Git-blob IDs before this report.

## 4. Before/after and denominator

| Scoped measurement | Before | After |
|---|---|---|
| PRs covered by this new ten-PR causal-chain witness | 0 | 10/10 |
| New PRs outside prior PR184-199 census | 0 | 9/9 (PR200-208) |
| Exact owner receipt predecessor links in this cohort | Not jointly measured | 10/10 MATCH |
| Isolated negative synthetic fixtures | Not available for this new evaluator | 15/15 rejected |
| Real-witness deliberate mutations | 0 | 5/5 rejected |
| Full original comment HTTP bytes independently rehashed | No | No |
| Project-wide eligible handoff attempts including failures | Unknown | Unknown |

AUTOMATION_RATE = NOT_COMPUTABLE; PROJECT_FULL_READBACK_RATE = NOT_COMPUTABLE. No local or private handoff is counted as an automated success. The 10/10 value describes selected merged PR/receipt metadata, not a 100% handoff automation rate or a project-wide security result.

## 5. R10 passive readback and authority boundary

PR #115 remains open at head dab7c59070d67e7e2a244bd6d05db9a4d37460e3; the checked PR conversation, reviews and review threads contain no independently authenticated expert return. Historical immutable R10 source head remains 539d4bb33d2ba2c4895713c1bc437ece0743eeea. PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED.

Publication is confined to three additive files under the existing R16 Alpha research directory. No external write slot, historical file rewrite, model modification, new automation, Cursor dispatch, R10 merge, Hostinger/runtime/WWW action, production integration or claim promotion. Merge, actual main and append-only Issue #93 receipt require independent post-publication readback.
