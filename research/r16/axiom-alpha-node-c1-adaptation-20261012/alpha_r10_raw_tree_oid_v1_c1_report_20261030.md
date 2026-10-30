# NEXUS OMEGA · AXIOM Alpha-Node · R10 raw Git-tree OID reconstruction V1 · 2026-10-30

```text
OBJECT = NEXUS_OMEGA_ALPHA_R10_RAW_GIT_TREE_OID_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 70bf5b69f16e548f2f3d671995e0db08c8eeecd9
PREDECESSOR_ISSUE93_RECEIPT = 6523624851
PREDECESSOR_PR = 217
SOURCE_R10_PR = 115_OPEN_UNMERGED
SOURCE_R10_COMMIT = dab7c59070d67e7e2a244bd6d05db9a4d37460e3
SOURCE_R10_ORIGINAL_HEAD = 539d4bb33d2ba2c4895713c1bc437ece0743eeea
SOURCE_R10_ROOT_TREE = d743c5d926d469470afa0d7331d5c56b8262d56c
SOURCE_R10_ACK_BLOB = 4e31f92be1f673f49a2c27e570b5849e754cca78
SOURCE_R10_ACK_BYTES = 4380
SOURCE_R10_ACK_SHA256 = 60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5
INDEPENDENT_RECEIVER_ACK = NOT_ESTABLISHED
AUTHENTICATED_EXTERNAL_ACTOR = NOT_ESTABLISHED
PRODUCTION_INTEGRATION = NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The previous R10 five-hop path gate verified *API metadata consistency* but explicitly did not reconstruct the raw Git tree-object identifiers. Read-only GitHub Git Data API returned five complete, non-truncated trees for the immutable R10 source commit: 23, 22, 1, 10 and 6 entries. The exact source path is `research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt`.

The source is an **owner-mediated ACK assertion**, not an independently authenticated expert receipt. PR #115 had no new independent PR discussion, reviews or review threads at the checked cutoff; the external GitHub actor registry remained empty. Issue #93 contained 207 owner-authored comments at the checked cutoff.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

A tree-path chain can appear consistent when only the parent/child SHA fields are compared, while one entry's bytes have been altered and the reported parent tree SHA has not been recomputed. The previous candidate had **0/5 independently reconstructed complete tree OIDs**. Falsifier: an altered mode, path, SHA, entry count/order or truncation must fail closed, while the unchanged five API entry sets must reconstruct the exact five immutable SHA-1 tree IDs.

## ISOLATED_CANDIDATE / INDEPENDENT TEST

All files are additive under the existing R16 Alpha-Node research path; no production validator or oracle was modified:

1. `frozen_alpha_r10_raw_tree_oid_oracle_v1_20261030.py` — independent subprocess evaluator, committed **before** candidate.
2. `alpha_r10_raw_tree_oid_gate_v1_20261030.py` — reconstructs Git tree serialization (`mode SP name NUL 20-byte-oid`) and hashes `tree <size> NUL <bytes>` with SHA-1; enforces exact five-hop path and fail-closed JSON parsing.
3. `r10_full_tree_api_entries_v1_20261030.json` — complete compact projection of all 62 GitHub API entries; not raw HTTP response bytes.
4. This report.

The projection was constructed from the five actual immutable GitHub Git-tree API responses. A **separate Python hashlib implementation**, using an independently transcribed copy of the same API entries, recomputed all five SHA-1 OIDs and matched the expected identifiers: **5/5 MATCH**. Tree serialized byte lengths: **848, 698, 68, 733, 447**. The independent black-box subprocess oracle against the exact versioned candidate and projection returned **19/19 PASS**, including **18/18 negative fail-closed cases**. Mutations include a same-length path change, leaf SHA, mode, tree ordering, missing/extra entries, duplicate path/JSON key, wrong root/commit/child link, truncated tree, nonfinite and malformed JSON, and forged authentication field. The oracle file was frozen in a separate earlier branch commit.

The versioned projection has **9,969 UTF-8 bytes**, SHA-256 `7ed776c5993c2a283dd3f2cdc49b51dc56338bd293dc6ac77ccd5c366782f39d`, Git blob `3c9bf11ce4668800506fa5b248e9caecff352c78`.

Reproduce within this directory:

```bash
python -S frozen_alpha_r10_raw_tree_oid_oracle_v1_20261030.py alpha_r10_raw_tree_oid_gate_v1_20261030.py r10_full_tree_api_entries_v1_20261030.json
```

## BEFORE / AFTER / LIMITS

| Comparable measure | Before | After |
| --- | --- | --- |
| Real complete R10 tree OIDs reconstructed | 0/5 established | 5/5 MATCH |
| Separate candidate subprocess oracle | Prior path-only oracle 23/23 | New raw-tree oracle 19/19, 18 negative |
| Cryptographic linkage of supplied tree entry bytes to supplied SHA-1 IDs | Not tested | Reconstructed for five trees |
| Original raw Git tree/commit bytes obtained independently | NO | NO |
| Authenticated external actor / independent R10 receiver ACK | NO | NO |
| Productive integration or scientific promotion | NO | NO |

**Scientific limitation:** GitHub API entry sets are still the acquisition source. Reconstruction proves internal Git-object hash consistency **conditional on those entries and the separately pinned commit root**; it does not authenticate raw Git commit bytes, GitHub API provenance, PGP signature, expert identity, scientific execution or receipt authority. Git SHA-1 also has known collision-resistance limitations. A forged internally consistent projection together with changed pins is outside this gate. No biological experiments, R10 merge, runtime/Hostinger/WWW writes, new workers or external actor registration.

Project-wide eligible handoff attempt denominator remains unavailable: `AUTOMATION_RATE=NOT_COMPUTABLE`, `FULL_READBACK_RATE=NOT_COMPUTABLE`. A successful research candidate is not a handoff automation success. GitHub PR, CI, actual-main readback and append-only Issue #93 receipt are separate subsequent publication gates; this report does not pre-assert their success.
