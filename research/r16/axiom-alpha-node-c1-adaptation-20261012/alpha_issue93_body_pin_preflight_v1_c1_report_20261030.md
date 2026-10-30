# AXIOM Alpha-Node — Issue #93 body-byte pin preflight V1 (C1, 2026-10-30)

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_BODY_PIN_PREFLIGHT_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = bed81432f77c6e0326bd8095af72cc5c52d7d683
PREDECESSOR_PR = 210
PREDECESSOR_ISSUE93_RECEIPT = 6516064455
SCOPE = ISOLATED_RECEIPT_BODY_BYTE_INTEGRITY; NOT_PRODUCTION_INTEGRATED
WWW_PARITY = NOT_ESTABLISHED

## Original source, baseline and negative hypothesis

The predecessor alpha_issue93_full_comment_census_v1_20261030.py was retrieved from immutable main bed81432f77c6e0326bd8095af72cc5c52d7d683. Its exact original bytes independently reconstructed locally: 3,253 bytes, SHA-256 639d2a03919cff1ac4faba756a6b2e3ca6b59b4c737082f43ada92c30fb297d1, Git blob d051dea0a30e8a96e51ee890b9e1e0575ca9f5bc. V1 checks the previously declared 199/199 comment metadata rows, but does not bind actual body bytes to a digest. Equal GitHub timestamps are not body-content checksums.

Negative hypothesis: a body-only mutation preserving comment ID, actor, timestamps and predecessor metadata is accepted by V1. A separate Python subprocess replay of the exact V1 source with a one-comment synthetic fixture confirmed PASS_METADATA_CENSUS for both body ORIGINAL and body MUTATED! (2/2 nominal PASS; 0/1 body mutation detected). This is a V1 scope gap, NOT evidence of any real GitHub comment edit.

## Isolated candidate and frozen independent evaluator

The candidate compares ordered observed Unicode comment bodies against a separately supplied per-ID SHA-256 and UTF-8 byte-count inventory. It fails closed for a body changed under unchanged pins, Unicode character/byte confusion, missing rows, duplicate/mismatched IDs, wrong source, invalid digest and malformed JSON. It does not fetch GitHub, grant actor rights, alter historical evidence, or change any running validator.

The independent frozen Python subprocess evaluator was committed BEFORE the candidate on the owner branch. It does not import the candidate. Local execution: 14/14 PASS (one positive and thirteen negative/malformed fixtures; 13/13 expected rejections). In particular, same-length hello to HELLO under unchanged pins returns BODY_SHA256_MISMATCH, while the old V1 accepts a body-only change. The Unicode fixture Grüße Ω distinguishes code-point count from UTF-8 byte count. Falsifier: if a body changes under a fixed independently pinned digest and the candidate returns PASS, the improvement is disproved.

| Scoped metric | V1 baseline | New isolated candidate |
|---|---|---|
| Changed-body fixture rejected | 0/1 | 1/1 |
| Frozen candidate evaluator | Not applicable | 14/14 PASS |
| Independent negative fixtures | Not applicable | 13/13 rejected |
| Actual Issue #93 body digests independently anchored | 0/200 established | 0/200 established |
| Authenticated project-wide handoff denominator | Unknown | Unknown |

## Exact additive files

Frozen evaluator: frozen_alpha_issue93_body_pin_oracle_v1_20261030.py, 3,023 UTF-8 bytes, SHA-256 98cf65f58be30cd0626e236a48de3fdb39c0b5eeb3d16e7449da2fe969b43262, Git blob 79c28d5fe3516a76b4866ee17f7f41b85e6b03ff.

Candidate: alpha_issue93_body_pin_preflight_v1_20261030.py, 2,549 UTF-8 bytes, SHA-256 8c1c359daf91feb363c7b60553a676802807a353aa54d50cc45d67e1b3138ecd, Git blob d9c89f94bdb56e37a46e114b05b1459f30ec715b.

Run the frozen evaluator with Python, passing the candidate path as its only argument. No dependency on the productive runtime.

## Trust limits and decision

CRITICAL: observed bodies and pins can be rewritten together. The preflight only detects divergence from independently retained pins; it does not authenticate pin origin, raw HTTP transport, GitHub actors, comment deletions, API pagination or completeness. No independently anchored actual 200-comment body-hash population is claimed. No real tampering observed. The isolated scaffold is NOT production integration.

AUTOMATION_RATE=NOT_COMPUTABLE and PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE: the complete authenticated eligible handoff denominator is unavailable. This is not a new R10 expert receipt.

R10 passive readback: PR #115 OPEN; detached manifest at pinned commit 539d4bb33d2ba2c4895713c1bc437ece0743eeea was fetched (4,588 UTF-8 bytes), but is not on current main. No independent receiver ACK, authenticated external GitHub actor, scientific adjudication or executed expert return found in PR discussion, reviews, review threads or Issue #93. PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED. Empty external actor allowlist unchanged.

Only the existing owner GitHub branch/PR/CI path may publish this public-safe reversible C1 research. Merge, main readback and append-only Issue #93 receipt require independent post-merge verification. No Hostinger/WWW write, new automation, runtime/worker change, secret, historical overwrite or claim promotion.
