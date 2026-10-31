# AXIOM Alpha-Node — Issue #93 two-phase REST census drift guard · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_TWO_PHASE_SNAPSHOT_GUARD_V1_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = ca8b2f9d7a5cf7371611690c2c4a52e5904f1e67  
PREDECESSOR_PR = 245  
PREDECESSOR_ISSUE93_RECEIPT = 6547058731  
PREDECESSOR_SOURCE = research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_raw_rest_census_v1_c1_report_20261031.md  
PREDECESSOR_SOURCE_GIT_BLOB = 8d39d75630388c2d5ece8d091328f7f0f038b0da  
FROZEN_ORACLE_FIRST_COMMIT = 2da7cef9c289e87dad5841c37f8327286084d7a3  
CANDIDATE_SECOND_COMMIT = 8e142580758c41e44ec8d2f528e0572bef4124eb  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Observation and negative hypothesis

The prior raw REST census V1 validates one caller-supplied issue count against the pages, but has no *second* issue-metadata read after pagination. Counter-hypothesis: if an additional comment arrives between pagination and the end of collection, a snapshot with PRE=235 and 235 items can be accepted despite POST=236. This is a synthetic concurrency adversary, not an observed historical incident. The new guard requires both independent issue metadata projections and equality of PRE, POST and the paginated item count; it refuses a missing or drifting second observation. It does not claim an atomic snapshot.

## Actual GitHub REST read-only observation

At the pinned 2026-10-31 observation, the public GitHub REST issue metadata returned `comments=235` before and after three paginated reads. The three pages contained **100+100+35=235** items, with unique strictly increasing comment IDs, first `6111816879`, last `6547058731`. All 235 visible actor labels were `nexusomegac27`, and all 235 had equal creation and modification timestamps. The issue `updated_at` was `2026-10-31T17:54:53Z` at both metadata reads. A separate JavaScript in-tool check of the actual REST JSON checked counts, ordering, required actor/timestamp fields and temporal order, with zero discrepancies. Raw page payloads were consumed but not archived as original bytes; GitHub actor labels are not independent expert authentication. The actual REST observation was NOT fed through the isolated Python candidate; the Python test below uses synthetic fixtures.

REST source: `https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93` and `/issues/93/comments?per_page=100&page=1..3`. The prior report at pinned main is an immutable documented predecessor, not an original byte archive of today's REST responses.

## Frozen evaluator and isolated candidate

An independent Python black-box subprocess evaluator was committed before the candidate and not modified afterward. Local Python 3 command:

`python frozen_alpha_issue93_two_phase_snapshot_oracle_v1_20261031.py alpha_issue93_two_phase_snapshot_guard_v1_20261031.py`

Result: **18/18 expected outcomes, exit 0**: three positive controls (101 comments, one edited timestamp correctly reported, empty issue) and 15 negative controls (post-growth, pre-mismatch, missing post, missing last page, duplicate ID, out-of-order ID, missing actor, missing body, invalid/reversed timestamps, wrong repository, duplicate JSON keys, nonfinite JSON, malformed JSON, extra page). No oracle changes after the candidate was written. This is separate technical testing, not external third-party scientific validation.

- Frozen oracle: 3,073 UTF-8 bytes; SHA-256 `1411f70f619f92511ee4d597990e1357b8cb43ccedb0687f4916b1447e893ef5`; Git blob `b5a4048fb160a4de35404970aa5b73c180898954`.
- Candidate: 3,657 UTF-8 bytes; SHA-256 `ed8f8d9bbd4fa456d4262f37848e7a4f156de2e3df5384a1a07f52ecff152843`; Git blob `1f0dc0ff0b2494e79a24fe0b11a10db91ce1007c`.

**Bounded before/after metric:** the synthetic PRE=235 / PAGES=235 / POST=236 drift fixture is accepted by a one-count baseline (0/1 drift detected), but rejected by the two-phase candidate (1/1 drift detected). The observed live 235/235/235 snapshot passes the separately implemented in-tool structural check. No real-world rate increase is claimed.

**Falsifier and residual limits:** any unequal pre/post count accepted as `CENSUS_CONSISTENT_NOT_AUTHENTICATED` falsifies this guard. Edits, deletions plus additions, or consistent API misrepresentation with unchanged count can still evade the guard. Two reads do not provide transaction isolation, GitHub transport attestation, actor authentication, original REST byte archives, or scientific expert adjudication. A future production integration would require a separate authorization and real-payload E2E execution.

## Decision and boundary

Additive isolated R16 research files only; no new pipeline root, workflow, external actor, runtime, Cursor dispatch, Hostinger/WWW write, PR #115 merge, biological experiment or claim promotion. R10 `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`; no new independently authenticated expert receipt in PR #115 discussion or the 235 pre-publication Issue #93 comments. PR #246 is a separate open, review-required architectural PR and is not included in this candidate.

Project-wide `AUTOMATION_RATE=NOT_COMPUTABLE` and `FULL_READBACK_RATE=NOT_COMPUTABLE`: complete authenticated eligible-event and publication denominators are unavailable. A local 18/18 fixture result is not either target rate. GitHub→WWW parity is not claimed. Actual merge, CI, immutable main readback and append-only Issue #93 receipt must be separately verified after publication.
