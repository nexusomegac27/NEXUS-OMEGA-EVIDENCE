# AXIOM Alpha-Node — Issue #93 multiline raw-HTML receipt guard V6 (2026-10-29)

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_MULTILINE_RAW_HTML_GUARD_V6_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=c7a69c537616ad9da142a83b25da2c43c3efaf4f
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/193
PREDECESSOR_ISSUE93_RECEIPT=6496658656

## Source-exact baseline and negative hypothesis

The five published V1–V5 predecessor Python files were retrieved from the pinned repository commit, independently reconstructed as actual UTF-8 bytes, and hashed in an isolated local directory. SHA-256: V1 `4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c` (5,622 B); V2 `05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91` (1,769 B); V3 `dd5875d92cd674c1b4f4428afea05aefcac769023f95e360960b627864ce5f96` (2,407 B); V4 `582bc71f0607664ad299a18058b1403c305fe265b5089ce136c4926bcbdcc21a` (2,772 B); V5 `acd0777f1ba8500ae3e4b0205bee3cc2d5807425dceb85c45319caed8f76a5c7` (3,939 B). GitHub V5 blob: `f0a854d8a1e34eef03f3917536031467d0c81ebc`. The original V5 frozen evaluator (5,548 B, SHA-256 `dcdf35a91a14fcccf608cdc1ae44bb03e5b1c10d84d39f984557f55e61055b50`) was also reconstructed exactly.

Negative hypothesis: V5's quote-aware single-line HTML scanner safely excludes receipts inside raw `<pre>`, `<script>`, `<style>`, and `<textarea>` blocks whose opening tags span multiple lines. Falsifier: synthetic owner-labelled PR #183 receipt, fully inside `<pre\n class="x">\n...\n</pre>`, is accepted by the exact V5 subprocess (exit 0, `matched_receipt_count=2`), despite only the genuine PR #182 receipt being operative. V5 stops scanning an incomplete opening tag without carrying parser state across lines. This is a synthetic false acceptance, not a claim of a real GitHub attack.

## Frozen independent subprocess evaluator and additive V6

The 24-case evaluator was authored and executed **before** V6 implementation and is separate from the target process: `frozen_issue93_multiline_raw_oracle_v6_20261029.py`, 5,303 B, SHA-256 `45c14c1daea47b8c5fb08efd5b4e0d91ec964b4c39fa5a388f05e6bd0f144d1e`, Git blob `3bd92ba990d8382c28930ff2791352b410e7ff28`. It checks four raw-block types, mixed case, multiline quoted attributes with embedded `>`, fake close tags, three-line tags, unclosed/oversized tags, duplicate receipt, wrong merge, non-owner, Markdown fences, HTML comments, legitimate receipts after closing tags, and duplicate examples. The same frozen evaluator on exact V5: **10/24 PASS**, 14 failures; on V6: **24/24 PASS**. The *prior, independently frozen V5 evaluator* also passed **24/24** when targeting V6. Total candidate test outcomes: 48/48 PASS across two unchanged subprocess evaluators. V5 is the targeted negative mutant. No external third-party validation is asserted.

V6 is an additive research-only wrapper importing V5 without modifying V1–V5 or either frozen evaluator. It carries HTML tag and quote state across lines, suppresses lines within raw blocks, and rejects incomplete or oversized tags before delegating to V5's existing receipt parser. V6: 3,940 B, SHA-256 `73311462e79da1bb940e8c23f8b34fb8c17d84941051f5f17883264aca384dfd`, Git blob `c611a92d97a07839aece5724c571edc66596f6d1`. Its conservative masking may reject some valid markup; this is a fail-closed tradeoff, not a complete CommonMark/HTML parser.

Reproduce from this directory with all historical files present:

```bash
AXIOM_CANDIDATE=alpha_issue93_quoted_attribute_guard_v5_20261029.py python frozen_issue93_multiline_raw_oracle_v6_20261029.py -q  # 14 expected failures
python frozen_issue93_multiline_raw_oracle_v6_20261029.py -q  # 24 PASS
AXIOM_CANDIDATE=alpha_issue93_multiline_raw_guard_v6_20261029.py python frozen_issue93_quoted_attribute_oracle_v5_20261029.py -q  # 24 PASS
```

## Authority, scope, limits, metrics

Only three **new** files are proposed under the existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` directory. The frozen oracle precedes candidate source in commit order. No existing file, directory, task anchor, external actor registry, runtime, evaluator, CI rule, Hostinger asset, WWW deployment, model weights, identity, or claim ceiling is changed. This parser consumes caller-supplied API projections and cannot authenticate GitHub origin or scientific content. The synthetic 10/24 → 24/24 metric is not an operational handoff rate. Project-wide eligible handoff and complete-readback numerator/denominator remain UNKNOWN/UNKNOWN and rates NOT_COMPUTABLE. R10 PR #115 has no independently authenticated receiver ACK in the checked PR comments, reviews or threads; no expert research execution is established. No new external writer registration or expert dispatch.

This document is a candidate report. Merge, main readback, CI completion and append-only Issue #93 receipt must be verified as separate subsequent GitHub events; publication cannot be inferred from this report alone.
