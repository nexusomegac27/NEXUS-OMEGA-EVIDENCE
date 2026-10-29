# AXIOM Alpha-Node · Remaining 37 original-byte census · 2026-10-29

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_REMAINING37_ORIGINAL_BYTE_CENSUS_20261029_R0
DECISION = KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 9aa55c904a33caca8c419639c0650cd294bd4d25
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/182
PREDECESSOR_ISSUE93_RECEIPT = 6483634724
PR_SCOPE = 164_TO_180
SOURCE_DIRECTORY = research/r16/axiom-alpha-node-c1-adaptation-20261012/
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Observation, actual bytes and metric

The immutable main above and actual Issue #93 comments were read before the audit. The predecessor PR #182 physically sampled 17 of 54 files (74,347 bytes) at an earlier immutable main, and explicitly left 37 files unchecked. The current main still has the same 54-file source series. This **single bounded candidate** closes that precise audit gap without modifying any of the 54 originals.

The remaining **37/37** actual source bodies were fetched via the connected GitHub contents API at the pinned main with `encoding=base64`, decoded as bytes (no newline or Unicode conversion), and independently hashed using in-session SHA-256 and Git-object SHA-1 routines. Three bounded batches (13 + 13 + 11) crosschecked computed Git blob SHA-1 against both the contents API and the pinned commit's nontruncated recursive Git tree. **37/37 byte counts, SHA-256 calculations and Git blob comparisons completed without mismatch; 169,889 bytes actually fetched.**

| Scope | Before | After |
|---|---:|---:|
| Actual original bodies rehashed within the enumerated 54-file series (cumulative across two explicitly distinguished iterations) | 17/54 | **54/54** |
| Newly fetched and rehashed in this iteration | 0/37 | **37/37** |
| New source bytes independently hashed | 0 | **169,889** |
| Combined original bytes across predecessor and this audit | 74,347 | **244,236** |
| New computed Git blob SHA-1 vs two GitHub metadata surfaces | 0/37 | **37/37 MATCH** |
| Eligible project-wide automated handoff numerator/denominator | UNKNOWN/UNKNOWN | **NOT_COMPUTABLE** |
| Project-wide full commit/source/test/receipt readback numerator/denominator | UNKNOWN/UNKNOWN | **NOT_COMPUTABLE** |

The 54/54 is a **closed, deliberately selected historical PR-file inventory**, not a project-wide completeness claim and not a single-run 54-file rehash. The 17 earlier hashes are inherited from the physically published PR #182 source report and corrected Issue #93 receipt, not silently presented as newly fetched. GitHub is the common upstream of both byte bodies and metadata.

## Exact new original-byte inventory

Relative paths are under the existing R16 directory named above. Columns: PR, filename, bytes, computed SHA-256, independently computed Git blob SHA-1.

164 | `frozen_steward_output_guard_evaluator_v1_20261028.py` | 5790 | `cb2a6b3d8324d6e11690e7d0a03a97d7f15b65c718520c2b1199a12244bf542b` | `c0538cae4ba8d6c4b12ced190d56f4262e78f117`
164 | `steward_output_guard_candidate_v1_20261028.py` | 3856 | `0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74` | `b697ebb2f0908cd09956bce880c78695f083a4c0`
165 | `frozen_steward_atomic_output_evaluator_v2_20261028.py` | 4611 | `f173dbce994b66d9c9cd3f65b2df881ee9fbdbd589da304e76478a352db7e692` | `85bf666208f98048960151b40bd62afa62b2b6e6`
165 | `steward_output_atomic_guard_candidate_v2_20261028.py` | 3187 | `441bffe0285183605b8d76d9f4d542ebf06f8e63e4f8cc92112550bc4df93841` | `e7fbad4dd0cd24f6f03c80b9ebbb709c2e14384c`
166 | `frozen_steward_postpublish_fsync_evaluator_v3_20261028.py` | 6326 | `636bb9780143dc7ec9f8df9053a5e56969479e182b30cf73a1f5a23e1555a17f` | `9770506b270248f56b23859b94fb094f73ba4cd7`
166 | `steward_output_postpublish_status_candidate_v3_20261028.py` | 4191 | `847c3bd775b195f30617174904af6644ab1d13dd30725a9f44e40fe797423578` | `89d5df5726ed25756ca0550559eae268db3c1b36`
167 | `frozen_steward_postpublish_readback_evaluator_v4_20261028.py` | 7225 | `4d98704e9d15163ac0c54db99a0fde5241769e0188b97606a37af26bf650e084` | `fed4d0de9644835efc20880a4409ebf3a3ee49b6`
167 | `steward_output_postpublish_readback_candidate_v4_20261028.py` | 4770 | `bc08d2b6ab1e12059418b6573192af2b1f7f1c0d381100d22d40d932a8cdafd2` | `03aa7ee31d56b5c91fc44e2635c96b3e15b9681d`
168 | `alpha_receipt_file_digest_witness_v1_20261028.py` | 4899 | `5ac7c5fd88b78c80e502bd01a4bc7fcbfd810179672486dec408ea9ac5617a9b` | `5523bea43be23d96b37432b7147183818ab58c81`
168 | `frozen_receipt_file_digest_evaluator_v1_20261028.py` | 4625 | `3da82354c24dc2961ed20ef839f2b420c04db6e4723ee4c0a6e6491c9e4062c8` | `1428ec4c20063dac82fd6d8d578d7ba3b41e587c`
169 | `alpha_handoff_metric_witness_v1_20261028.py` | 6431 | `df569e5ff841157d72379c344c8e1997e820911479efe2faa05c708fdf1b16b0` | `c98b8e9334255ad82c04788450ef1b17360f66ed`
169 | `frozen_handoff_metric_evaluator_v1_20261028.py` | 5266 | `67b2ff73c2f1cfc6ef36738ea1fd1951c4526084054ef587b342db2c6449ab8e` | `6419917ab52b1f13c9fed8bcb54649f72b569b1f`
170 | `alpha_handoff_page_census_witness_v2_20261028.py` | 8528 | `c16806be3d00810b0e6d6ddeefc336c7428c9f6104c050c52815deb725cac8fd` | `e7882865407d2beb1b522182a86bf3351a7ef824`
170 | `frozen_handoff_page_census_evaluator_v2_20261028.py` | 6255 | `43032eb24cc7c4aaae798bfcbbd8cf64e8ba16b3b4966d904485d2c0e0491a6d` | `73b8a1ad805f08e56e6d7d667578e94fcd58b98d`
171 | `alpha_handoff_readback_scope_c1_report_20261028.md` | 3471 | `6211dc04abfbaf14a1f9820df1362065dd6e569a2777e385e19744af8eff1ca0` | `1bbb76944129401e3f30e898102c58f252282632`
171 | `frozen_readback_scope_smoke_v3_20261028.py` | 2580 | `7c5a00b7a0e71e22bbef688794aaa122ca6ad1d5b801482b31799d95b714828a` | `e178f8235e5d674ee62682ac7f0efa5b0fce8019`
172 | `alpha_handoff_pinned_input_guard_v4_20261028.py` | 1605 | `e629233ecdfbf4fc0f808ed745387ec2d8dcb1d7db5132809bc863a8b5c582ec` | `538f20a3dc6a2c84ce17f6c914d7faa4ac9354a1`
172 | `frozen_pinned_census_input_oracle_v4_20261028.py` | 4710 | `d34128355a0f1907935d2c5c259f4a84706e194b0db8ab492576de5313523838` | `65fc69d88060efa5418264b5145db94c2f4ce453`
173 | `alpha_receipt_chain_observed_snapshot_20261028.json` | 4693 | `f9c78661d0f026ff9fea26a6ad60291e382c71b2d95403e26519e32c8d59842a` | `0b08ff347b8fe06cfdef7759c076bea29be7610a`
173 | `alpha_receipt_chain_reconciler_v1_20261028.py` | 4797 | `b38125d20729cad52a0c40a59589dafe144ef80ccc620f734974a2aea16729ba` | `f7614d8a134066bf74f52544342bd7e03f31a7a3`
173 | `frozen_receipt_chain_oracle_v1_20261028.py` | 3821 | `39048860f13bec9cfcf6a5736d44c36e3e3c4f828ff43dafdddaec8778ca543f` | `d839e09aaed324d03fd082b888ab4656ff9e0b03`
174 | `alpha_receipt_chain_reconciler_v2_20261028.py` | 5666 | `cfa795f78bbc54d6eec9a4b5c0e44e9b36ee56285aff0cc379b2638b75d6a627` | `9dc125ed90be9f875e698a6189d3007787394f7e`
174 | `alpha_receipt_chain_variable_inventory_c1_report_20261028.md` | 4815 | `40e27f3e513889c3519fcd212bbf1cbee6e55883551a952d546c575061b13ee8` | `b3fe17c2b516b8a514aeaa4e095ed3c70ae38388`
174 | `frozen_receipt_chain_variable_inventory_oracle_v2_20261028.py` | 4234 | `326793e634c3bb1d126423052a8a75da66313522d0cdc7fd8987e22bb53ff3b2` | `6d527fd2153bdd4e34cc0eaef3b027f3e0b5cfce`
175 | `alpha_receipt_chain_reconciler_v3_20261028.py` | 2389 | `3f4a4c6d845e2ee302c9ebcce6c99cebbe04fb2751e8bc2a0fe7f591ebaf7ef0` | `2f8389788b429a1c0bb890984e66c9de5cf64a03`
175 | `frozen_receipt_chain_portable_paths_oracle_v3_20261028.py` | 6070 | `e71a80691bcefb4d20839d434e2325f2f4447fc652dd35647f124bd64cd333f5` | `29b7dffae45c024cf453bfe8191bbf78fb760cb9`
176 | `alpha_receipt_chain_reconciler_v4_20261028.py` | 1723 | `139e7048d443e160707805281a762b6931bca6e4d6733870a580c082eb1a8506` | `af8d0d6851901338a2ad384f17a08918a15219a4`
176 | `frozen_receipt_chain_prefix_oracle_v4_20261028.py` | 5777 | `5048ba9d0b72c1e5a73a4afeff933087cea6be84292ac493fccd6378eedf0cc2` | `d9dbaad6a3daf6dec820c2423b4ed47f4d00ca74`
177 | `alpha_receipt_chain_reconciler_v5_20261028.py` | 1523 | `eda09c5c82908be15385080c319bb88fdec9fccdd381414ae488fb8f73af3e55` | `4f3dc94e61a12b34141aa6f0ce178c39056818ad`
177 | `frozen_receipt_chain_commit_acyclic_oracle_v5_20261028.py` | 5563 | `c9aba3ed0eef0e97863340903c5b366c9c967060b28d6a979a2a4ca646328a65` | `719d82975d8628dee9907aef2b057dd649d3dfad`
178 | `alpha_receipt_order_guard_v1_20261028.py` | 2823 | `ca04bf21025f7aac77eef522240cd4bf9940bdb86f640a7233059f3468245793` | `19eea36ffbde83473cab4a7a082a2afe36176f99`
178 | `frozen_receipt_order_oracle_v1_20261028.py` | 4283 | `01614236a06a163697fd573d7ecbb5c40b4d238ea988ab70db36333ae2de22de` | `ef9170ba34d7689a5a0b1ea29c617aa9ceb2752a`
179 | `alpha_issue93_api_crosscheck_v1_20261028.py` | 5931 | `bee92d67b18d1b831dee259ec633018509d803081bce5b776fd9d455205a981d` | `b886dff345bc0a572c8554d42fad68e1cddaca1f`
179 | `alpha_issue93_api_projection_pr178_20261028.json` | 2280 | `9e445ccbd81a835feede78660b2b776b239915076f1afe71315f4fb103c9984b` | `3ab0342a4326b47eef7bce862bc48b94665ab6af`
179 | `frozen_issue93_api_crosscheck_oracle_v1_20261028.py` | 5535 | `7f19b770e53351bae9fac8c740cc4b66b3ad6c29e9f093158ad60396d23fdb0d` | `09a23719c776849497b1141239c652962b6ba25d`
180 | `alpha_issue93_historical_main_lineage_c1_report_20261028.md` | 5285 | `6958649a1d94f355794faa92a2987130b9b97a159f253c25fba076a389ad493d` | `f738bebe57ea7430d6c7bebfa5c72af31f83ba45`
180 | `frozen_issue93_historical_lineage_oracle_v2_20261028.py` | 4355 | `aa3b79bd47395b30337e9669ddbba3f0b47b6bce5ff5b8150b5fbb3e377d93f9` | `13be7585c231a27acdbfb08125c9af353d0c426b`

## Negative hypothesis, evaluator and falsifier

**H0:** the earlier cross-endpoint 54/54 Git-blob metadata agreement could hide a divergent actual source body in any of the 37 unsampled files. In this bounded retrieval, no such contradiction was observed. The SHA-256 routine passed standard empty-string and `abc` vectors; the Git-object SHA-1 routine passed the empty-blob known vector. The computed blob IDs matched the pinned tree and contents metadata for every new source.

A **separate Python 3 standard-library in-session inventory evaluator**, independent of the JavaScript byte-hash implementation, checked the 37 rows, unique paths, per-PR cardinality, SHA-256 and Git-blob syntax and positive byte counts: **37/37 positive rows accepted**. Four one-defect negative fixtures were executed separately: deleted row -> `COUNT/PR_CARDINALITY`; duplicate path -> `DUPLICATE_PATH`; malformed digest -> `SHA256_FORMAT`; negative byte count -> `BYTE_SIZE`. **4/4 rejected as expected**. This structural evaluator does **not** independently rehash original source bytes, was not precommitted/frozen, and is not third-party validation. A changed original body with a different computed SHA-256 or Git blob on a repeated pinned fetch, or an independently observed discrepancy, falsifies the corresponding scoped identity result.

**Execution negative evidence:** An initial attempt to combine all 17 PR metadata fetches and 54 source fetches into one connector execution was rejected by the connected tool's per-execution call limit. It was not counted as a completed audit. The successful bounded three-batch read used the existing API and no new transport.

## Governance and residual limits

Only a new, additive public-safe C1 research report is proposed. The existing 54 source bodies, historical paths, independent test oracles, productive Repository Steward, workflows, governance, actor registry, runtime, Hostinger and WWW are unchanged. No claim that the source content is scientifically correct, that the external GitHub actor is an independent expert, or that the 90%/100% project objectives have been reached. A full **eligible-attempt census including failures, retries, pending and inaccessible private handoffs** remains necessary for project-wide ratios. No new pipeline root, worker, model change, Cursor dispatch or R10 promotion.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
