# AXIOM Alpha-Node — strict raw-HTML close guard V7 (2026-10-29)

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_STRICT_RAW_CLOSE_GUARD_V7_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=e0af98acaed7ea3357fcb5169a4ec3a31ba8ff5d
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/194
PREDECESSOR_ISSUE93_RECEIPT=6498003720

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The six V1–V6 Issue #93 guard sources were fetched from immutable main, reconstructed byte-exact in an isolated local directory, and independently SHA-256/Git-blob rehashed. All six match GitHub metadata and the previous reports. V6: 3940 bytes; SHA-256 73311462e79da1bb940e8c23f8b34fb8c17d84941051f5f17883264aca384dfd; Git blob c611a92d97a07839aece5724c571edc66596f6d1. Existing frozen V6 oracle: 5303 bytes; SHA-256 45c14c1daea47b8c5fb08efd5b4e0d91ec964b4c39fa5a388f05e6bd0f144d1e.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

V6's scanner delegates HTML raw closing tags to V4's regular expression r'</(pre|script|style|textarea)\b[^>]*>'. A word boundary before a hyphen is accepted, and arbitrary suffix text is consumed. Consequently a distinct closing tag such as </pre-foo> incorrectly closes <pre>. The exact V6 Python subprocess accepted a synthetic owner-labelled PR #183 receipt between that forged close and the actual </pre>, exit 0 and matched_receipt_count=2. This is a synthetic false acceptance, NOT a claim of a real attack or authenticated GitHub provenance.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

An independent 20-case subprocess oracle was authored and committed before the V7 source. On the same frozen oracle, V6 passed 12/20 and failed eight adversarial negatives; V7 passed 20/20. The pre-existing, unchanged frozen V6 24-case oracle passed 24/24 on V7: total V7 44/44. Both oracles run the candidate as a separate Python process. External third-party validation is not claimed.

V7 retains V6's multiline scanner and uses strict raw close matching r'</(pre|script|style|textarea)\s*>\Z', rejecting distinct tag-name suffixes and closing-tag attributes while preserving ordinary closing whitespace. It imports historical V5 without modifying any historical source or oracle. V7: 4079 bytes; SHA-256 6c680b8cd487e52492c7cca35174947c85a0e79a98081371d29048d5e0d48d33; Git blob 50824cd1d661ce36ac47c50ca610535d16f09cd5. New frozen oracle: 4802 bytes; SHA-256 363bbf275af6b6ccc7ddd0a9d3b4bfc81f1002ebb5d47144b16664c5e1f33fbc; Git blob 40cdf5953d96493e6dc85539241b60aa3b1d2503.

Falsifier: a reproducible case where V7 accepts a receipt enclosed by a raw block with only a noncanonical closing tag, or rejects a valid receipt after a canonical closing tag. These tests do not establish complete HTML/CommonMark parsing, GitHub API authentication, scientific truth, runtime integration, or project-wide rates. Fail-closed masking may reject some legitimate markup.

Reproduction commands (from the existing R16 research directory):
- AXIOM_CANDIDATE=alpha_issue93_multiline_raw_guard_v6_20261029.py python frozen_issue93_strict_raw_close_oracle_v7_20261029.py -q  (8 expected failures)
- python frozen_issue93_strict_raw_close_oracle_v7_20261029.py -q  (20 PASS)
- AXIOM_CANDIDATE=alpha_issue93_strict_raw_close_guard_v7_20261029.py python frozen_issue93_multiline_raw_oracle_v6_20261029.py -q  (24 PASS)

## DECISION / PUBLICATION BOUNDARY

Exactly three additive research files in the existing R16 directory are proposed; no old source, evaluator, CI, governance, actor registry, runtime, Hostinger/WWW, model weights or permissions change. PR, CI, merge, main readback, and append-only Issue #93 receipt are separate events requiring subsequent verification. Eligible project handoff numerator and denominator remain UNKNOWN/UNKNOWN; AUTOMATION_RATE=NOT_COMPUTABLE and READBACK_RATE=NOT_COMPUTABLE. R10 PR #115 remains PUBLIC_SEND only; no independently authenticated receiver ACK or executed expert research was observed in checked PR discussions. BLOCKED_LANE != BLOCKED_SYSTEM.
