# AXIOM Alpha-Node — Issue #93 raw HTML block receipt guard V4 (2026-10-29)

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_RAW_HTML_BLOCK_RECEIPT_GUARD_V4_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=d26379d34e95659572495456eedc525f2f5540af
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/191
PREDECESSOR_ISSUE93_RECEIPT=6492574334

## Observation and falsification

The physically retrieved V1/V2/V3 original Python files were reconstructed locally with byte-identical SHA-256 hashes: V1 4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c, V2 05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91, V3 dd5875d92cd674c1b4f4428afea05aefcac769023f95e360960b627864ce5f96. GitHub file-API blob identities were independently observed on the pinned main. V3 excludes Markdown fences and HTML comments, but not raw HTML <pre>, <script>, <style>, <textarea> blocks.

Negative hypothesis: HTML-comment exclusion alone suffices to reject non-operative receipt examples. Falsifier: a complete synthetic PR receipt placed solely inside a raw HTML block is accepted as a real receipt by V3. This falsifier was executed on the unmodified, byte-identical V3 Python source; the V3 black-box oracle returned 12/20 PASS, 8/20 expected FAIL. In particular, four distinct raw-block-only examples were falsely accepted; a duplicate inside <pre> was rejected for the wrong reason. These are synthetic tests, not observed attacks on Issue #93.

## Isolated candidate and independent evaluator

The new V4 is an additive research-only wrapper that imports V3, preserving V1/V2/V3 and their original frozen oracles. It ignores the four raw HTML block types, including uppercase tags and attributes; rejects unclosed raw blocks; preserves V3 Markdown fence/HTML comment behavior. No API fetch, GitHub actor authentication, new pipeline, worker, deployment, runtime, or model self-modification.

Frozen evaluator committed first to the existing R16 research directory: frozen_issue93_raw_html_block_oracle_v4_20261029.py, 5,903 bytes, SHA-256 8f17c9e29c561841812a8e0ea2d54eedc6abbf996680a9cc662320e0d1e884b8, Git blob 620f7e2e5013220d3828abfbdbd1d11b3660132a. Candidate committed second: alpha_issue93_raw_html_block_guard_v4_20261029.py, 2,772 bytes, SHA-256 582bc71f0607664ad299a18058b1403c305fe265b5089ce136c4926bcbdcc21a, Git blob 35c99bed1c0fb0fecc13ea313916c156cfd567cf.

Separate Python subprocess black-box evaluator, same frozen 20 synthetic tests: V3 baseline 12/20 PASS, V4 20/20 PASS. Positive controls include ordinary receipts, legitimate receipts after closed blocks, HTML comments and Markdown fences. Negative controls include four raw block types, mixed case, attributes, hidden duplicate, unclosed block, wrong merge, non-owner and duplicate fields. The evaluator was authored by AXIOM before candidate publication, not an external independent third party. Tests were run locally, not against production GitHub event processing.

## Decision, limitations and target metrics

Before/after: eight failed synthetic oracle cases reduced to zero, on the same 20-case frozen test. This is NOT evidence of an observed production incident or improvement in actual automated handoff percentage. The parser still processes caller-supplied GitHub projections and cannot authenticate origin, guarantee completeness, or prove an external expert ACK. Coherently forged input remains a counterexample. Full CommonMark/HTML equivalence and third-party adversarial validation are not claimed.

Project eligible automated handoff numerator/denominator = UNKNOWN/UNKNOWN; project publication complete-readback numerator/denominator = UNKNOWN/UNKNOWN; both NOT_COMPUTABLE. No private or inaccessible returns counted as successes. R10 PR #115 remained open; no new independent PR comments/reviews/threads or independently authenticated expert returns observed. Actor allowlist empty. No claim promotion, external write, Hostinger/WWW write, or runtime integration. BLOCKED_LANE != BLOCKED_SYSTEM.
