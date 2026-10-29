# AXIOM Alpha-Node — Issue #93 quoted HTML attribute guard V5 (2026-10-29)

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_QUOTED_ATTRIBUTE_GUARD_V5_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=f7379d164d6f55120f4f80372ba3cb115a12f77f
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/192
PREDECESSOR_ISSUE93_RECEIPT=6495585764

## Original bytes and falsifier

The physically fetched V1/V2/V3/V4 predecessor Python sources were locally reconstructed byte-for-byte and independently SHA-256 rehashed. V1: 5,622 B, '4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c'; V2: 1,769 B, '05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91'; V3: 2,407 B, 'dd5875d92cd674c1b4f4428afea05aefcac769023f95e360960b627864ce5f96'; V4: 2,772 B, '582bc71f0607664ad299a18058b1403c305fe265b5089ce136c4926bcbdcc21a'. All match previously bound original source hashes; V4 Git blob '35c99bed1c0fb0fecc13ea313916c156cfd567cf' was independently retrieved at pinned main.

Negative hypothesis: V4's raw-HTML tag matcher cannot be fooled by a closing-tag-looking sequence inside a quoted HTML attribute. Falsifier: an owner-labelled, syntactically complete synthetic receipt appearing only inside '<pre>' is accepted if an earlier nested tag contains 'data-x="</pre>"'. Executing unmodified V4 on the synthetic fixture returned exit 0 and 'matched_receipt_count=2', although the second receipt is inside the raw block. This is an isolated parser false acceptance, **not** an observed Issue #93 attack or independently authenticated owner comment.

## Frozen oracle and isolated V5

Frozen subprocess oracle committed first: 'frozen_issue93_quoted_attribute_oracle_v5_20261029.py' (5,548 B; SHA-256 'dcdf35a91a14fcccf608cdc1ae44bb03e5b1c10d84d39f984557f55e61055b50'; Git blob '1e3e85c808576ebe2e94c39a13b498b3a2c4fbd0'). It has 24 deterministic synthetic cases and does not import the candidate. Original V4 baseline: **15/24 PASS**, nine failures; V5 candidate: **24/24 PASS** on the same frozen evaluator. Targeted negatives cover both quote styles, '>' inside quoted attributes, uppercase tags, nested tags and comment-like attribute text. Positive controls cover genuine receipts after proper closing tags, duplicate examples ignored, Markdown fences and HTML comments. Wrong merge, non-owner and duplicate receipt checks remain fail-closed.

V5 is additive and imports V4 without changing historical source/evaluator bytes. It scans complete HTML tags with quote awareness, so an apparent closing tag inside a quoted attribute cannot terminate raw-block suppression. V5 source: 3,939 B; SHA-256 'acd0777f1ba8500ae3e4b0205bee3cc2d5807425dceb85c45319caed8f76a5c7'; Git blob 'f0a854d8a1e34eef03f3917536031467d0c81ebc'. Tests were executed locally as Python subprocesses, with the evaluator authored by AXIOM before the V5 candidate; this is separation of test artifact and candidate, **not** external third-party validation.

Reproduction from this directory: 'AXIOM_CANDIDATE=alpha_issue93_raw_html_block_guard_v4_20261029.py python frozen_issue93_quoted_attribute_oracle_v5_20261029.py -q' (expected nine failures); 'python frozen_issue93_quoted_attribute_oracle_v5_20261029.py -q' (expected 24 passes). Run in a disposable isolated checkout with the four unchanged predecessor scripts available.

## Boundaries and project metrics

V5 parses caller-supplied projections, not authenticated GitHub API provenance. It is not CommonMark/HTML-complete, does not establish expert ACK, does not authorize runtime integration, and is not deployed. A coherently forged input remains a counterexample. The project-wide eligible automated handoff numerator/denominator and publication complete-readback numerator/denominator remain UNKNOWN/UNKNOWN and both rates NOT_COMPUTABLE. Synthetic oracle cases are not operational handoffs. R10 PR #115 remained open, with zero independently attributable PR comments, reviews or review threads and no authenticated external receiver ACK. External actor allowlist remains empty. No worker, Hostinger/WWW, runtime, governance, identity or claim changes.
