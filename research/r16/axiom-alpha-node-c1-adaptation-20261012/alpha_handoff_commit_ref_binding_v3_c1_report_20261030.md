# AXIOM Alpha-Node — isolated commit URL/source commit binding V3 (C1, 2026-10-30)

OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_COMMIT_REF_BINDING_V3_20261030_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE_PUBLICATION_CONDITIONAL
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=68719c2aedaf8aa325d3319d3e49d98e3ded70bd
PREDECESSOR_PR=224
PREDECESSOR_ISSUE93_RECEIPT=6532872551
FROZEN_ORACLE_FIRST_COMMIT=abdbc6f67e66820c356af13ac7ac9acda25c5130
CANDIDATE_SECOND_COMMIT=44d487a5091f419139d4bab0b61aec6f93848ee9
PRODUCTION_INTEGRATION=NO
EXTERNAL_ACTOR_ALLOWLIST=EMPTY

## Original bytes and negative hypothesis

On pinned main, alpha_handoff_denominator_scope_binding_v2_20261030.py has 1,352 UTF-8 bytes, SHA-256 1b54aaed98dba63d4d96bddd86138978dbc5d40ee31976e76eb6282d482927c4, Git blob 7c58679f3b4c7c6959666f1840d8a72709486412. Its underlying alpha_handoff_source_url_guard_v1_20261030.py has 2,954 bytes, SHA-256 92fe99e09228096c976bb33537fac30d615842a5881f9023ca6c885b5007c1e2, Git blob 2b5011a574f1a24fedca98e9817381760abe68af. The V1 attempt reducer has 4,835 bytes, SHA-256 854c83cd67b365f6f8aeace3346da116aff2694591dcabaa9b62de5a4727f46f, Git blob 9aa7501579db9e1cc1ef64648df10e8e20a7fa07. Local test copies independently rehashed and matched these pinned Git blobs.

NEGATIVE_HYPOTHESIS: V2 accepts a canonical same-repository commit URL naming SHA A paired with source_commit SHA B when A != B. V1 URL guard checks equality for blob URLs but not commit URLs. This is a source-consistency defect, not evidence of an actual forged handoff.

## One isolated candidate and independent evaluator

V3 invokes unchanged V2 first, then requires equality between a commit URL's SHA and the declared source_commit. It retains the V2 denominator, failed eligible attempts, safety unknowns and null project-wide rates. The black-box Python oracle was committed FIRST and invokes V2 and V3 as separate python -S subprocesses, importing neither.

FROZEN_ORACLE_BYTES=4319
FROZEN_ORACLE_SHA256=47d7527b40a7f57f813be7e3722e7d0766dbf396faba2d0ba4a97daa7278316f
V3_CANDIDATE_BYTES=1452
V3_CANDIDATE_SHA256=425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3

| Fixed synthetic check | V2 baseline | V3 candidate |
|---|---:|---:|
| Mismatched commit locator accepted | 1/1 | 0/6 |
| Valid canonical controls | Not separately retested | 5/5 PASS |
| Black-box oracle | — | 19/19 PASS |
| Negative and malformed controls | — | 12/12 FAIL_CLOSED |
| Eligible sample attempts, including one failure | 2 | 2 |
| Synthetic sample autonomous rate | 1/2 | 1/2 |
| Project-wide automation and readback | NOT_COMPUTABLE | NOT_COMPUTABLE |

FALSIFIER: V3 accepts a mismatched commit URL, rejects a matching commit/issue/PR/pinned blob, removes a failed eligible attempt, or computes a project-wide rate without a complete authenticated census. Each observation disproves its respective improvement claim.

Reproduction from research/r16/axiom-alpha-node-c1-adaptation-20261012/:
python -S frozen_alpha_handoff_commit_ref_binding_oracle_v1_20261030.py alpha_handoff_commit_ref_binding_v3_20261030.py alpha_handoff_denominator_scope_binding_v2_20261030.py

## Passive R10 readback and boundaries

PR #115 is open at head dab7c59070d67e7e2a244bd6d05db9a4d37460e3. Detached R10 manifest at pinned commit 539d4bb33d2ba2c4895713c1bc437ece0743eeea: 4,588 actual ASCII/UTF-8 bytes, independently calculated SHA-256 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc and Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df MATCH. Issue #93 has 214 comments, all API-authored by owner; PR #115 has no discussion comments, reviews or review threads. No independently authenticated new expert return.

PUBLIC_SEND=OBSERVED
INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED
AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED
AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED
EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED

V3 is syntax/consistency checking only, not URL retrieval, actor authentication, independent handoff verification, full attempt census or productive integration. Existing CI, merge, immutable main byte/hash/blob readback and append-only Issue #93 receipt are mandatory before any publication success claim. No new automation, worker, pipeline root, Hostinger/WWW write, external registration, evaluator self-approval or C1 claim promotion.
