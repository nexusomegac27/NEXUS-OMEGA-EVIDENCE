# AXIOM Alpha-Node · 17-PR original-byte sample · 2026-10-29

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_17PR_ORIGINAL_BYTE_SAMPLE_20261029_R0
DECISION = KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN = 1b1a09f277bf14b14886a4a09a8e5222fbc7ec14
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/181
PREDECESSOR_ISSUE93_RECEIPT = 6482166560
SCOPE = 1_EXPLICIT_FILE_PER_PR_164_TO_180
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Evidence and bounded improvement

The previous 17-PR metadata census explicitly performed **0/54 original-body SHA-256 rehashes**. This new, non-random **one-file-per-PR sample** retrieved the exact 17 public source bodies at immutable main `1b1a09f277bf14b14886a4a09a8e5222fbc7ec14` using the GitHub contents API `encoding=base64`, decoded the byte streams without Unicode/newline conversion, and computed their SHA-256 and Git blob SHA-1 locally. Original merge-commit file metadata was independently retrieved for the selection; the computed blob IDs match both the commit-file listing and pinned-main contents API blob ID.

| Check | Before | After |
|---|---:|---:|
| Source bodies independently SHA-256-rehashed within 54-file scoped census | 0/54 | **17/54** |
| PRs represented by at least one byte-rehashed file | 0/17 | **17/17** |
| Selected computed Git blob vs commit and pinned-main contents | not performed | **17/17 MATCH** |
| Retrieved byte total | not recorded | **74347** |
| SHA-256/Git SHA-1 known-vector pairs (empty, ASCII, Unicode) | not performed | **3/3 MATCH** |
| Separate in-session inventory evaluator | not performed | **17/17 PASS** |
| Negative fixtures: altered blob, missing row, invalid SHA-256 | not performed | **3/3 REJECTED** |
| Remaining files not independently rehashed in this scope | 54 | **37** |
| Project-wide handoff automation rate | UNKNOWN/UNKNOWN | **NOT_COMPUTABLE** |

## Exact source inventory

`PR | filename relative to existing R16 directory | original bytes | SHA-256 | computed Git blob SHA-1`

164 | `AXIOM_ALPHA_STEWARD_OUTPUT_CLOBBER_20261028_R0.md` | 4487 | `8fb7e84295bf35116d617ddea17f45a5260625710d7ead569b85241a6d7d641d` | `1264b9be81af02e21a04c081229fb55010569fc8`
165 | `AXIOM_ALPHA_STEWARD_ATOMIC_OUTPUT_20261028_R0.md` | 5534 | `2537a27dbf4a8a124ca5ca9a063ffaeb793dd66316df4ba7532325fa3b61dbe2` | `c13fd304e60554dfc7307cbd33efa3042e0694e0`
166 | `AXIOM_ALPHA_STEWARD_POSTPUBLISH_FSYNC_STATUS_20261028_R0.md` | 5023 | `d5024e2a5fdc5845ce108f4a3ef2a9958f0df300ed7902757a7c78504b4f14a8` | `51feb9cdb04b0e4673cd1caed541da7ae828f2c2`
167 | `AXIOM_ALPHA_STEWARD_POSTPUBLISH_READBACK_20261028_R0.md` | 4928 | `61112acf83e0e173ad7e19ae364703808d012e9a7d101e22999b93bc3123834e` | `4ab4760a378707f6049cde97c7fd2e8208ab71e8`
168 | `AXIOM_ALPHA_RECEIPT_FILE_DIGEST_WITNESS_20261028_R0.md` | 3620 | `d195950fbcbacc76c2def0ddfd4533b8c65e889c3940e4170fcd07d9e508e40a` | `e7db10dc81fc74d1d8d05a06739bfda67fbe1848`
169 | `AXIOM_ALPHA_HANDOFF_DENOMINATOR_WITNESS_20261028_R0.md` | 5293 | `3e001def488f94dc7bf30831f10ee9c0bbcd9c96a0d9e62e8800855f806083c6` | `f00147c0550facc6ae7f00820f66de966d05446d`
170 | `alpha_handoff_page_census_c1_report_20261028.md` | 4711 | `4a2927b37480258a3920f6b1d812c7a8f984ad5097162f926d375bc009c94f19` | `0906d2640b4239b35c1da4da0bed27f2171189c5`
171 | `alpha_handoff_readback_scope_adapter_v3_20261028.py` | 1198 | `6f93b45bbaa0f1e7debae7b45e6ea06f4f5a59ceecc9d4fa7b9d34180a84e476` | `35fea2e9d4b97eb14bb2dacbe1bf9ad17415688f`
172 | `alpha_handoff_pinned_input_guard_c1_report_20261028.md` | 4651 | `b5350998de6fa6d0c01174f93cad39b1a2ba76177457f98258b257a7a284bede` | `2dd59ab0e8b5fefa87bd8e5a58d6a5a1da0b4f53`
173 | `alpha_receipt_chain_audit_c1_report_20261028.md` | 6328 | `1a5a1c0f4b62a6e72945e1fde244d88351dcf003b82657e13070ddb2320f70ae` | `2e6fd7955a15bd010bb3a1642a85f0f86acf8d3a`
174 | `alpha_receipt_chain_pr173_observed_fixture_v2_20261028.json` | 1367 | `70544c8d596973ff252a925bbf257ce1acbea31881e27407c46a03324cc2fc33` | `84db26edd8c605c452e490a0b82ed06c08fb9010`
175 | `alpha_receipt_chain_portable_path_c1_report_20261028.md` | 4427 | `31879aafff8d6d657e90a4235561200536b92d6704762dedcd9adbe9f4b9a957` | `465d6522d57dc6230f4c858e292746b865ff282d`
176 | `alpha_receipt_chain_prefix_conflict_c1_report_20261028.md` | 4069 | `a45711f2de53e2fed29443d8649d1011930ef37dc3ff478e17c05380b7b039a6` | `b2909f4be994dd3463f8ed2960bc048df78e1a94`
177 | `alpha_receipt_chain_commit_acyclic_c1_report_20261028.md` | 4673 | `098963c090509545cfa26e294b2d08cef03d9ad27cba9e151a3ad19644e0e6ac` | `639a925dd4018fc0afe659b694c6abb7171c8a5b`
178 | `alpha_receipt_order_chronology_c1_report_20261028.md` | 4600 | `837e909fe1d862d3d89b4e00776843bc4f2c7057dcfbd28aed54daeda2f86120` | `fe431e4568e9f825fbeaefbcb3cffb498084788f`
179 | `alpha_issue93_api_crosscheck_c1_report_20261028.md` | 5536 | `037c0ddc33a66d5f7f740c26f8529fc2b6fde1b997fe3e4d79a661390a01f69b` | `25b93db94d4769f6d304816b38ba66c544f01d6f`
180 | `alpha_issue93_historical_lineage_guard_v2_20261028.py` | 3902 | `8c4c4df2e0258b9f09a17fcbcdd7484c1e357570159697dce4aadfa37832228a` | `247d0dd284655461ec0a33b9901330406893c729`

## Negative hypothesis, falsifier and limits

H0: matching metadata between two GitHub endpoints need not establish byte identity. This sample found no mismatch for the 17 specified source bodies. A separate in-session inventory evaluator checked cardinality, unique PRs, SHA-256 syntax and the two blob bindings; 3/3 single-defect mutated negative inventories were rejected. The digest implementation passed three standard-library-derived fixed test vectors. This is **not a frozen precommitted independent oracle**, not a random or representative sample of the 54 files, not third-party authentication and not proof of scientific correctness. A changed body with mismatching computed Git blob, a digest mismatch on repeat, or a conflicting independent source falsifies the respective scoped finding.

GitHub remains the common upstream of contents and metadata. The 37 untested files remain explicitly out of the numerator. A success-only PR sample does not enumerate failed/pending handoffs and must not be used as the 90%/100% project denominator. No production code, historical source, evaluator, registry, CI, runtime, Hostinger, WWW or model weights were changed.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
