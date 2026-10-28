# AXIOM Alpha-Node · Historical GitHub main ancestry witness V2 · 2026-10-28

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_HISTORICAL_MAIN_LINEAGE_20261028_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 59bc5b6aeeda70e11f342f3cb745c4da4b651146  
PREDECESSOR_MAIN = 6e700be6fd408c3d78d3d7e08619b635de92966f  
PREDECESSOR_ISSUE93_RECEIPT = 6480022471  
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/179  
SCOPE = EXISTING_R16_RESEARCH_ONLY; NO_PRODUCTION_INTEGRATION

## Observation and negative hypothesis

The previous published `alpha_issue93_api_crosscheck_v1_20261028.py` (Git blob `b886dff345bc0a572c8554d42fad68e1cddaca1f`) requires `branch.commit.sha == receipt merge SHA`. This is correct for a point-in-time publication readback, but a **historical** receipt would fail once legitimate new commits advance main. Do not reinterpret that as a past invalid merge.

A read-only GitHub compare on 2026-10-28 used immutable base `6e700be6fd408c3d78d3d7e08619b635de92966f` (PR #178 merged commit, receipt #6478246029) and main `59bc5b6aeeda70e11f342f3cb745c4da4b651146` (PR #179). GitHub reported `status=ahead`, `ahead_by=1`, `behind_by=0`, `total_commits=1`, `base_commit.sha=merge_base_commit.sha=6e700be6fd408c3d78d3d7e08619b635de92966f`. This is a bounded **actual GitHub REST observation**; the offline fixture contains a caller-supplied reduced projection, not original HTTP bytes.

H0: a historical PR receipt is valid only while main still equals its merge commit. The actual one-commit descendant is a counterexample to that restrictive historical rule. V2 accepts a declared exact match OR an explicitly checked descendant relation, with source-bound merge-base and count checks. It does not alter V1, the historical receipt, or its original at-merge readback.

## Independent frozen evaluator and falsifier

The subprocess evaluator was authored and locally executed separately from the candidate and **committed first** to the owner branch. It tests two valid cases (current main equals merge, current main is descendant) and 16 fail-closed cases, including forged merge base, diverged branch, behind count, wrong base/head/receipt SHA, inconsistent counts, boolean-as-integer, invalid status, duplicate JSON key, nonfinite JSON, foreign repository, extra field and empty input.

- Frozen oracle first commit: `32580477fad6102547452ba82971842d809145c6`; 4,355 bytes; local SHA-256 `aa3b79bd47395b30337e9669ddbba3f0b47b6bce5ff5b8150b5fbb3e377d93f9`.
- Candidate commits: `b13ba66199eb7123fafcf3a1ee40e7ba57e1e82d`, then corrected exact regex-anchor source `310a352c6d9de139967b1446e92fa710e9e0fb8f`; final 3,902 bytes; local SHA-256 `8c4c4df2e0258b9f09a17fcbcdd7484c1e357570159697dce4aadfa37832228a`.
- Local Linux/Python 3.13 subprocess evaluation: **18/18 PASS** against the final local candidate.
- True negative mutant: removing the `merge_base_commit.sha` comparison yields **17/18 PASS**, with the forged merge-base case failing the frozen oracle as intended.
- Reproduce within this existing directory: `python frozen_issue93_historical_lineage_oracle_v2_20261028.py alpha_issue93_historical_lineage_guard_v2_20261028.py`.

**Falsifier:** a genuine GitHub compare showing the merge SHA is *not* the merge base, or a later main not descending from that merge, must fail the ancestry claim. A consistently forged caller-supplied compare may still pass: `api_origin_authenticated=false`. This candidate does not fetch APIs or verify original response bytes. It cannot establish that a GitHub actor is an independent expert, or that any scientific claim is valid.

## Before/after and scope

- Before: the V1 source equality check would reject the observed historical PR #178 merge when supplied current main `59bc...`; baseline observed by source inspection, **V1 not rerun**.
- After: V2 accepts **1/1** actual API-derived descendant projection and rejects **16/16** constructed invalid cases under the separate oracle. This is **not** 1/1 project handoff automation or a complete inventory.
- Project-wide eligible automation numerator/denominator: `UNKNOWN/UNKNOWN`; `AUTOMATION_RATE=NOT_COMPUTABLE`.
- Project-wide publication/readback numerator/denominator: `UNKNOWN/UNKNOWN`; `READBACK_RATE=NOT_COMPUTABLE`.
- This iteration's publication/readback count remains `0/0` at report authoring; only a subsequent actual PR merge, exact main-file readback and Issue #93 receipt may change it.

R10 PR #115 remains owner-mediated, open and unmerged. Its current head is `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, distinct from the original pinned `539d4bb33d2ba2c4895713c1bc437ece0743eeea`. No new PR comments, reviews or review threads were observed. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. External actor registry remains empty.

All files are additive in the existing R16 research directory. No production Steward, historical source, governance, external registry, Cursor, Hostinger, WWW, runtime, worker, model weight, system instruction or claim promotion changes. `WWW_PARITY=NOT_ESTABLISHED`.
