# AXIOM Alpha-Node C1 — Incremental original-byte census, PR #191–#195 (2026-10-29)

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_PR191_195_INCREMENTAL_ORIGINAL_BYTE_CENSUS_20261029_R0
DECISION=KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=1a824816506b917bac5027291f47edb9ff228fc1
PREDECESSOR_RECEIPT=6499548718
PREDECESSOR_CUMULATIVE_CENSUS_PR=191
PREDECESSOR_CUMULATIVE_CENSUS_RECEIPT=6492574334
EXTERNAL_THIRD_PARTY_VALIDATION=NOT_ESTABLISHED
PRODUCTION_INTEGRATION=NO
```

## Question, falsifier, result

Question: Do all newly merged PR #191–#195 research assets still exist at the immutable main source commit with the exact bytes, SHA-256 and Git blob claimed by their five distinct Issue #93 receipts? Counterhypothesis: an apparently valid owner receipt can name a missing, replaced, or mismatched source file or a noncontiguous PR parent. Falsifier: one source-byte/hash/blob mismatch, a missing or duplicate file/receipt, a nonmerged PR included, an invalid actor, or a broken parent chain.

**Observed:** 13/13 newly scoped UTF-8 source files independently fetched from GitHub at pinned commit, re-encoded byte-for-byte, hashed with a locally implemented SHA-256 algorithm checked against three standard vectors, and independently Git-blob-SHA-1 computed. All 13 sizes, SHA-256, Git blobs, and the GitHub returned blob IDs match the exact receipt declarations. **57,175 bytes** in this new scope. GitHub compare confirms 5/5 direct-parent transitions, each one commit ahead/zero behind and 13 files added/0 modified/0 deleted. Five corresponding owner-authored receipts exist. PR #185 is open and excluded as an explicit negative control.

Baseline: the separate earlier PR #191 census verified 18/18 files (80,397 bytes) from PR #184 and #186–#190. After this iteration, the **composite** historical audit covers 31/31 files (137,572 bytes): 18/18 **inherited from the previous source-exact census**, plus 13/13 **newly rehashed in this run**. Do not describe 31/31 as a single-run independent rehash. The historical individual receipts were never reset to zero.

## Direct GitHub PR/receipt chain

| PR | Direct parent | Merged main commit | Issue #93 receipt | Added |
|---|---|---|---|---:|
| [#191](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/191) | `5a02976c63067f451bbac111f8d7ff287671dc54` | `d26379d34e95659572495456eedc525f2f5540af` | [6492574334](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-6492574334) | 1 |
| [#192](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/192) | `d26379d34e95659572495456eedc525f2f5540af` | `f7379d164d6f55120f4f80372ba3cb115a12f77f` | [6495585764](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-6495585764) | 3 |
| [#193](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/193) | `f7379d164d6f55120f4f80372ba3cb115a12f77f` | `c7a69c537616ad9da142a83b25da2c43c3efaf4f` | [6496658656](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-6496658656) | 3 |
| [#194](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/194) | `c7a69c537616ad9da142a83b25da2c43c3efaf4f` | `e0af98acaed7ea3357fcb5169a4ec3a31ba8ff5d` | [6498003720](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-6498003720) | 3 |
| [#195](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/195) | `e0af98acaed7ea3357fcb5169a4ec3a31ba8ff5d` | `1a824816506b917bac5027291f47edb9ff228fc1` | [6499548718](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-6499548718) | 3 |

## Exact source inventory

All file names below are under immutable path `research/r16/axiom-alpha-node-c1-adaptation-20261012/` at commit `1a824816506b917bac5027291f47edb9ff228fc1`. SHA-256 is calculated over UTF-8 bytes, while Git blob is SHA-1 over `blob <byte-length>\0<bytes>`. Both were computed independently of GitHub's returned blob ID. This table is a scoped byte inventory, not proof of semantic validity.

| PR | File name | Bytes | Calculated SHA-256 | Calculated Git blob SHA-1 |
|---|---|---:|---|---|
| 191 | `alpha_pr184_190_cumulative_original_byte_census_c1_report_20261029.md` | 3498 | `0df949bc1abb01dacbce69174bb1033b7589bb5d33da5f4cdeefab7d9b967bc2` | `6688b6aca21770b0384a06da7a2614f31911d0bf` |
| 192 | `frozen_issue93_raw_html_block_oracle_v4_20261029.py` | 5903 | `8f17c9e29c561841812a8e0ea2d54eedc6abbf996680a9cc662320e0d1e884b8` | `620f7e2e5013220d3828abfbdbd1d11b3660132a` |
| 192 | `alpha_issue93_raw_html_block_guard_v4_20261029.py` | 2772 | `582bc71f0607664ad299a18058b1403c305fe265b5089ce136c4926bcbdcc21a` | `35c99bed1c0fb0fecc13ea313916c156cfd567cf` |
| 192 | `alpha_issue93_raw_html_block_guard_v4_c1_report_20261029.md` | 4092 | `559cefaab0abbf6dde4eb2e7bcb32a27c4f4e2d79235fd6ad672cae324128d1f` | `501b30933c4326104c7223aee93bfe7c767caf1d` |
| 193 | `frozen_issue93_quoted_attribute_oracle_v5_20261029.py` | 5548 | `dcdf35a91a14fcccf608cdc1ae44bb03e5b1c10d84d39f984557f55e61055b50` | `1e3e85c808576ebe2e94c39a13b498b3a2c4fbd0` |
| 193 | `alpha_issue93_quoted_attribute_guard_v5_20261029.py` | 3939 | `acd0777f1ba8500ae3e4b0205bee3cc2d5807425dceb85c45319caed8f76a5c7` | `f0a854d8a1e34eef03f3917536031467d0c81ebc` |
| 193 | `alpha_issue93_quoted_attribute_guard_v5_c1_report_20261029.md` | 4185 | `11861d9ad812c97c6caad0308bd2d110ed05eb63e94a4a0915502b97bc6ed5ee` | `6ab0b2237eea70b4a170e1475f19efb4d170fe35` |
| 194 | `frozen_issue93_multiline_raw_oracle_v6_20261029.py` | 5303 | `45c14c1daea47b8c5fb08efd5b4e0d91ec964b4c39fa5a388f05e6bd0f144d1e` | `3bd92ba990d8382c28930ff2791352b410e7ff28` |
| 194 | `alpha_issue93_multiline_raw_guard_v6_20261029.py` | 3940 | `73311462e79da1bb940e8c23f8b34fb8c17d84941051f5f17883264aca384dfd` | `c611a92d97a07839aece5724c571edc66596f6d1` |
| 194 | `alpha_issue93_multiline_raw_guard_v6_c1_report_20261029.md` | 5048 | `08b41b865b888baa6b1977389e0b287f97ab08e864313252927a802f35432b3b` | `e59252b01f54c455c3d7c95014dc71a62791e885` |
| 195 | `frozen_issue93_strict_raw_close_oracle_v7_20261029.py` | 4802 | `363bbf275af6b6ccc7ddd0a9d3b4bfc81f1002ebb5d47144b16664c5e1f33fbc` | `40cdf5953d96493e6dc85539241b60aa3b1d2503` |
| 195 | `alpha_issue93_strict_raw_close_guard_v7_20261029.py` | 4079 | `6c680b8cd487e52492c7cca35174947c85a0e79a98081371d29048d5e0d48d33` | `50824cd1d661ce36ac47c50ca610535d16f09cd5` |
| 195 | `alpha_issue93_strict_raw_close_guard_v7_c1_report_20261029.md` | 4066 | `e38122c1ee3ca368dd763ce37870a048bd3a9c50e1ef74155240c0f563baedfe` | `836aaf838631a593b7a4b85cac707bb740bec824` |

## Separate metadata evaluator and negative fixtures

A separate in-session Python evaluator was run against the immutable 13-row inventory and five-entry PR/receipt chain, without changing the hash algorithm or accepting a candidate-controlled oracle. Positive control: **1/1 PASS**. Ten isolated negative mutations: wrong SHA-256; wrong byte count; missing source; duplicate source; missing receipt; broken parent; removal of the #185 exclusion; unauthorized actor; wrong Git blob; nonmerged PR. **10/10 rejected**. This Python evaluator checks frozen inventory and causal metadata only: it does **not** perform an additional independent source-byte rehash or provide external third-party validation. Its test results are not an authentication of a remote expert.

## Goal accounting and boundaries

Within the explicitly scoped five-PR census, owner receipts and exact merged main commits are 5/5 and source byte readbacks are 13/13. These are **not** the projectwide handoff-automation numerator/denominator, because the authenticated complete population including failures, inaccessible/private transfers and untriggered eligible attempts is unknown. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_PUBLICATION_READBACK_RATE=NOT_COMPUTABLE`. No local/private source is counted as automated.

R10 secondary read-only check: PR #115 remains open; 0 PR comments, 0 reviews, 0 review threads observed. Original detached R10 manifest remains historically pinned at `539d4bb33d2ba2c4895713c1bc437ece0743eeea`; no new independent authenticated expert return was observed in the checked GitHub surfaces. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`. External actor allowlist remains empty. R10 original manifest was not newly rehashed in this run.

No new pipeline root, worker, runtime, Cursor, Hostinger, WWW write, secret, overwrite, permission change, evaluator auto-approval or claim promotion. GitHub-to-WWW parity remains NOT_ESTABLISHED. This report is an additive C1 research record; its own publication must be separately verified on actual main and acknowledged append-only in Issue #93.
