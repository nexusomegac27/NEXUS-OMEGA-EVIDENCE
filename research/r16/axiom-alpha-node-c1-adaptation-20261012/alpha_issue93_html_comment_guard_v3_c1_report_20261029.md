# AXIOM Alpha-Node — Issue #93 HTML-comment receipt guard V3 · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_HTML_COMMENT_GUARD_20261029_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 3c68b978d2d3273c4684b2dafa33dfac5376cc7e
MAIN_PREDECESSOR = 05748765ab35d87d6bfa79377a97d7c0ff2c2807
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/186
PREDECESSOR_ISSUE93_RECEIPT = 6486339190
OWNER_BRANCH = axiom/alpha-issue93-html-comment-v3-c1-20261029
FROZEN_ORACLE_FIRST_COMMIT = faca00390ab68105dc78e96de18731652e55be51
CANDIDATE_SECOND_COMMIT = df61b2acdbc28fc217c0be3548f4da2da7a35f11
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## Observation, original bytes and negative hypothesis

The pinned V1 source was fetched from immutable main, reconstructed byte-exact and independently hashed: 5,622 bytes; SHA-256 4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c; Git blob 68655fd9c5d36fe562b15d3f5ddf29fcd372c145. V2 was likewise reconstructed: 1,769 bytes; SHA-256 05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91; Git blob e34cd65069c3f0fb3bf071aac7889a109b0be7bc.

V2 correctly ignores Markdown fenced examples but still parses a bare PR= line inside an HTML comment. Falsifier of the hypothesis "Markdown-fence exclusion suffices for receipt attribution": a synthetically constructed Issue #93 comment whose only PR=, ACTUAL_MAIN_READBACK= and CLAIM_CEILING= fields occur between HTML comment delimiters. V2 accepts the false receipt if the caller supplies matching PR metadata. This is a demonstrated synthetic parser weakness, **not** an observed GitHub attack or independently authenticated actor.

V3 is an additive wrapper over V2/V1. It ignores every line containing or inside an HTML comment, without stitching field fragments across comment boundaries, while preserving V2 Markdown-fence handling. Unclosed HTML comments fail closed. Historical V1/V2 bytes and the frozen evaluator remain unchanged.

## Independent frozen test and metrics

The black-box subprocess evaluator was committed first, before candidate creation. It does not import candidate internals. The same 15 synthetic fixtures cover valid receipts, HTML-only forgery, duplicate and promoted fields inside comments, unclosed comments, valid fields following comments, multiple comments, Markdown fence regression, wrong merge, wrong actor, duplicate JSON keys, nonfinite JSON and claim promotion.

- V2 baseline: 9/15 PASS; six expected failing fixtures.
- V3 candidate: 15/15 PASS; zero failing fixtures.
- Frozen evaluator: 4,167 bytes; SHA-256 04786cbca2b981ef932a18b12eb28f1916e2fc914b3167e4b019de7672ff15de; Git blob f0a35eb4fe18f952d940a05a93f61ae795eb9c32.
- V3 candidate: 2,407 bytes; SHA-256 dd5875d92cd674c1b4f4428afea05aefcac769023f95e360960b627864ce5f96; Git blob 5f7ee75c85d7dcae21790d08c9ddfc4264013b2e.
- Environment: local isolated Python 3 execution, no network required. No third-party scientific validation.
- Reproduce from the branch checkout in the existing R16 directory:
  - python frozen_issue93_html_comment_oracle_v3_20261029.py -q
  - AXIOM_CANDIDATE=alpha_issue93_fenced_receipt_guard_v2_20261029.py python frozen_issue93_html_comment_oracle_v3_20261029.py -q

## Scope, limitations and decision

The parser receives caller-supplied JSON; it does not fetch or authenticate GitHub, verify PR provenance or establish the full project-wide handoff denominator. A syntactically valid plain-text forged receipt remains an explicit counterexample. HTML comments are conservatively treated as excluded lines; this is not a complete CommonMark/HTML parser. No actual forged HTML-comment receipt has been established. Project automation and readback rates remain NOT_COMPUTABLE (authentic total numerator and denominator unknown; inaccessible private returns excluded).

R10 remains separate: PR #115's current head was observed nine commits ahead of immutable reference 539d4bb33d2ba2c4895713c1bc437ece0743eeea; owner-mediated return/ACK assertion files do not establish an authenticated independent GitHub actor or scientific execution. No R10 write, expert dispatch, merge or claim promotion.

This change adds only a frozen evaluator, an isolated candidate and this research report under the existing R16 path. No new pipeline root, scheduler, external actor registration, runtime/Hostinger/WWW write, Repository Steward change, or evaluator self-approval. Publication and main/receipt readbacks are separate gates, not inferred from local tests.
