# NEXUS OMEGA — Alpha-Node · R10 real-source commit-tree path gate V1 (C1)

```text
OBJECT = NEXUS_OMEGA_ALPHA_R10_REAL_COMMIT_TREE_PATH_GATE_V1_20261030_R0
STATE = TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PREDECESSOR_MAIN = dab73d377c66fc146c7c647d3873988db181b8bb
PREDECESSOR_ISSUE93_RECEIPT = 6522407193
SOURCE_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/115
SOURCE_COMMIT = dab7c59070d67e7e2a244bd6d05db9a4d37460e3
SOURCE_ORIGINAL_MANIFEST_COMMIT = 539d4bb33d2ba2c4895713c1bc437ece0743eeea
SOURCE_ROOT_TREE = d743c5d926d469470afa0d7331d5c56b8262d56c
SOURCE_BYTES = 4380
SOURCE_SHA256 = 60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5
SOURCE_GIT_BLOB = 4e31f92be1f673f49a2c27e570b5849e754cca78
INDEPENDENT_RECEIVER_ACK = NOT_ESTABLISHED
AUTHENTICATED_EXTERNAL_ACTOR = NOT_ESTABLISHED
EXPERT_RESEARCH_ACTUALLY_EXECUTED = NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read the actual GitHub main and prior Issue #93 receipt before selecting one candidate. R10 PR #115 remained open, with no independent review, review-thread or PR discussion return in the inspected API population. The external actor registry remains default DENY and its allowlist is empty. No new independent R10 expert return was established.

The earlier V2 source-byte gate explicitly left the source-to-claimed-commit/path association unverified and had not executed the real 4,380-byte R10 ACK file end-to-end. The exact owner-mediated file is `research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt` at immutable commit `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`. It is **not** an independently authenticated expert receipt.

The GitHub connector returned the original file as base64; the 98 wrapped base64 lines were compared against the retrieved representation, and the reconstructed physical bytes independently hashed with Python hashlib: **4,380 bytes**, SHA-256 `60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5`, Git blob `4e31f92be1f673f49a2c27e570b5849e754cca78`. These match the GitHub file and tree entry. No original source text is duplicated into this research publication.

Read-only GitHub Git Data API returned commit root tree `d743c5d926d469470afa0d7331d5c56b8262d56c` and five successive tree entries: `research` → `r10` → `biocomputing-independent-experts-20261016` → `returns_20261016` → the exact source filename. Every directory entry has mode `040000` and type `tree`; the leaf has mode `100644`, type `blob`, size `4380` and the expected blob SHA. All five tree API responses reported `truncated=false`. The compact JSON projection records those API fields; it is not the original full tree API response or a cryptographic Merkle proof.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

A correct source SHA-256 and Git-blob ID alone do not prove that the source file belongs to the claimed Git commit **at the claimed path**. A substituted path or broken parent/child tree chain could pass a source-only hash gate. Prior V2 report: 24/24 synthetic tests and one real-registry-plus-synthetic-source probe, but **0/1 real R10 ACK + commit-tree path end-to-end test**.

Falsifier: change one byte of the original source without changing the pins; change any intermediate tree parent, path component, leaf blob, file size, mode, expected commit/root SHA, or truncate the API tree projection. Each must fail closed. A genuine unmodified file and the five matching API tree hops must pass without promoting an independent receiver ACK.

## ISOLATED_CANDIDATE / SEPARATE_EVALUATOR

Four **additive** research artifacts under the existing R16 Alpha-Node path:

- `frozen_alpha_r10_commit_tree_path_oracle_v1_20261030.py`: separate black-box subprocess evaluator, committed before the candidate.
- `alpha_r10_commit_tree_path_gate_v1_20261030.py`: offline path-chain, file mode, exact byte count, SHA-256 and Git-blob consistency gate.
- `r10_commit_tree_path_api_projection_v1_20261030.json`: source-exact compact API-field projection of the five Git tree hops, not a raw API receipt.
- This report.

Local independent evaluator result: **23/23 PASS** on the physically reconstructed original R10 source, including **22/22 fail-closed negative fixtures** (same-length mutation, truncation, append, false source/tree/commit pins, wrong path, altered tree links, altered blob/size/mode, truncated tree, missing/extra hop, duplicate JSON keys, NaN and malformed JSON). A separate direct invocation on the real source and projection returned `source_bytes_sha256_git_blob=MATCH` and `commit_tree_path=API_METADATA_CONSISTENT_NOT_AUTHENTICATED`.

Reproduction, after obtaining the exact immutable source bytes from the existing GitHub PR (no ZIP courier or new transport):

```bash
python -S frozen_alpha_r10_commit_tree_path_oracle_v1_20261030.py \
  alpha_r10_commit_tree_path_gate_v1_20261030.py \
  /path/to/exact/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt \
  r10_commit_tree_path_api_projection_v1_20261030.json
```

## BEFORE / AFTER / DECISION

| Comparable measurement | Before | After |
| --- | --- | --- |
| Real R10 ACK bytes + five-hop commit-path consistency exercised | 0/1 established | 1/1 local PASS |
| Real source mutation rejected with unchanged pins | Not tested in prior V2 | 1/1 FAIL_EXPECTED |
| Independent black-box candidate evaluation | Prior V2: 24/24 synthetic | New candidate: 23/23, including real positive |
| GitHub actor authentication / independent ACK | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Production integration | NO | NO |

**Decision:** TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE. This narrows the specific source-to-path consistency gap; it does not establish independent authenticity of the GitHub API, raw commit/tree-object cryptographic reconstruction, trusted timestamp, expert identity, scientific adjudication or real external expert execution. The API-field projection could be forged together with its pins; authoritative source acquisition and independent verification remain necessary. No R10 PR merge, actor registration, new worker, runtime, Hostinger, WWW or claim promotion.

The project-wide automation rate and complete-publication-readback rate remain **NOT_COMPUTABLE** because the authenticated population of all eligible attempts, including failures, is unavailable. The one successful local candidate test is not a handoff automation numerator. GitHub publication, CI, immutable main readback and append-only Issue #93 receipt are separate post-report gates; none is presumed successful by this report.
