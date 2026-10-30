# AXIOM Alpha-Node — Handoff denominator V2 source-scope binding (C1, 2026-10-30)

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_DENOMINATOR_SCOPE_BINDING_V2_20261030_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=4235539c67d8a2af203898886f55252ec495d17a
PREDECESSOR_PR=223
PREDECESSOR_ISSUE93_RECEIPT=6531871051
FROZEN_EVALUATOR_FIRST_COMMIT=b299db42dcabac81e0980bc69cf99e94cb641033
CANDIDATE_SECOND_COMMIT=cfa5bc6b2146efee0b07212fd55ab48fdaafdcfe
EXTERNAL_ACTOR_ALLOWLIST=EMPTY
PRODUCTION_INTEGRATION=NO
```

## Original sources, hypothesis and pinned baseline

Two pre-existing Python files were fetched from immutable main and independently reconstructed as local UTF-8 Git blobs: `alpha_handoff_attempt_denominator_v1_20261030.py` (4,835 bytes, Git blob `9aa7501579db9e1cc1ef64648df10e8e20a7fa07`, SHA-256 `854c83cd67b365f6f8aeace3346da116aff2694591dcabaa9b62de5a4727f46f`) and `alpha_handoff_source_url_guard_v1_20261030.py` (2,954 bytes, Git blob `2b5011a574f1a24fedca98e9817381760abe68af`, SHA-256 `92fe99e09228096c976bb33537fac30d615842a5881f9023ca6c885b5007c1e2`). Both originals remain unchanged.

The V1 denominator accepts any `source_ref` beginning with `https://github.com/`, including another repository. A separate URL guard had been independently tested and published in PR #220, but was not called by the denominator. Negative hypothesis: the denominator's own source-scope predicate still admits a foreign-repository source in a formally eligible sample, even when the isolated guard correctly rejects it. This is a syntax/scope weakness, not proof of a forged real receipt.

## One isolated candidate and independent test

The V2 wrapper invokes the existing V1 attempt reducer and then applies the existing immutable-source URL guard to **every** attempt before returning a result. It changes no historical file, evaluator, production validator or denominator population. The new output explicitly labels source checking as `CANONICAL_REPO_SYNTAX_ONLY_NOT_AUTHENTICATED`; project-level rates remain `null`.

A black-box Python subprocess oracle was committed **first**, before the candidate file. It imports neither candidate nor predecessor, and invokes both by separate `python -S` processes. Local execution with byte-matched predecessor source files: **25/25 PASS**, including **17/17 negative/malformed controls** and **5/5 canonical URL controls**. The frozen oracle source is 5,362 bytes, SHA-256 `541c6e04a58fecc581267f63b0bf775ecaab5b609a5c48d4222241b13b40be9f`; candidate is 1,352 bytes, SHA-256 `1b54aaed98dba63d4d96bddd86138978dbc5d40ee31976e76eb6282d482927c4`.

| Fixed synthetic measurement | V1 | V2 |
|---|---:|---:|
| Foreign-repository source accepted | 1/1 | 0/1 |
| Eligible attempts (one verified, one failed) | 2 | 2 |
| Sample autonomous handoff rate | 1/2 = 50% | 1/2 = 50% |
| Published with full readback | 0/1 | 0/1 |
| Project-wide authenticated eligible denominator | UNKNOWN | UNKNOWN |
| Project-wide automation and readback rates | NOT_COMPUTABLE | NOT_COMPUTABLE |

**Falsifier:** the foreign-repository or mutable-branch blob fixture returns success from V2; any canonical pinned issue/PR/commit/blob control is rejected; the failed eligible attempt disappears from the denominator; or V2 emits a numeric project-wide rate from unauthenticated declarations. Any such observation invalidates the corresponding improvement claim.

Reproduce from `research/r16/axiom-alpha-node-c1-adaptation-20261012/`:

```sh
python -S frozen_alpha_handoff_denominator_scope_binding_oracle_v1_20261030.py alpha_handoff_denominator_scope_binding_v2_20261030.py alpha_handoff_attempt_denominator_v1_20261030.py
```

## Boundaries and passive R10 check

URL scope is not URL retrieval, GitHub actor authentication, source-byte integrity, independent expert ACK, complete handoff census, or evidence of non-intervention. The wrapper is **not** wired into production. An otherwise valid URL may refer to nonexistent or incorrect content. The complete population of eligible/failed routine public authorized handoffs is not available, so no 90% target achievement or project-wide 100% readback rate is asserted.

At this readback PR #115 was open/unmerged; its immutable R10 manifest at head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was physically fetched as a GitHub blob (`0c2ca57a40f519da45ce60b565e8aadb4c9b95df`). Issue #93 had 213 comments, all GitHub API actor `nexusomegac27`; no PR discussion/reviews/threads yielded a new independently authenticated expert return. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`.

Publication is conditional on existing CI, actual merge, exact immutable `main` readback, per-file bytes/sha/blob checks and a separate append-only Issue #93 receipt. No additional automation, worker, pipeline root, runtime/Hostinger/WWW change, external registration or claim promotion is authorized by this report.
