# AXIOM Alpha-Node — isolated full-publication-readback preflight V1 (2026-10-31)

```text
OBJECT = NEXUS_OMEGA_ALPHA_PUBLICATION_FULL_READBACK_PREFLIGHT_V1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 0e32161a7599291ff581b8c8c1b072c37d2d99ec
PINNED_MAIN_PARENT = 03906d3c1cdc64fe6f1830808d18b765f90a830d
PREDECESSOR_PR = 239
PREDECESSOR_ISSUE93_RECEIPT = 6542955861
FROZEN_ORACLE_FIRST_COMMIT = e39df56a709335bf011400b2e9639014c73fdcf9
CANDIDATE_SECOND_COMMIT = 332b26871ee2b265bd91ee661691709dcfd76a95
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## One bounded candidate and negative hypothesis

The preceding PR #238 reconciliation established 10/10 *PR/merge/Issue-93 receipt relationships* in a scoped window, but explicitly did **not** establish full original-source byte readback or a project-wide 100% publication denominator. A later self-authored receipt cannot substitute for an independent byte check. This iteration introduces one additive **offline preflight** that checks a caller-supplied declared publication set for original byte count, SHA-256, Git blob, path uniqueness, PR/parent/merge consistency, CI success and exact receipt binding. It does not change the existing PR #238 source or its evaluator.

**Negative hypothesis:** an incomplete or mutated publication evidence envelope could be accepted as a full readback merely because its PR/receipt identifiers agree. **Falsifier:** any of the 18 independently frozen negative fixtures yields a successful preflight, or the positive fixture is rejected. A second falsifier for a future API-integrated version is an actual GitHub changed file omitted from the supplied declared file list.

## Source, original bytes and isolated test

Authoritative source files `AGENTS.md`, `GOVERNANCE.md`, R16 Alpha contract, Operator direct-publication rule, Task Anchor Norm, repository order policy, pipeline README, Repository Steward V1 and external write-slot registry were read at immutable `main` above. GitHub issue #93 contained 229 comments, all owner-authored, at observation; PR #115 remained OPEN and unmerged. These GitHub API reads establish repository transport observations, not independent scientific or actor identity.

Both new Python files were created in the existing registered R16 research lane; no existing file was modified. The evaluator was committed and fetched at its Git blob **before** the candidate was created. Independent local hashes of the exact candidate bytes were compared with GitHub blob readback before the subprocess execution.

| Additive file | Bytes | Independent SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `frozen_alpha_publication_readback_oracle_v1_20261031.py` | 4568 | `eab0589bace114fa78339dab40c6df11691fa5827762cbf7d4e84692ad2672cf` | `a4c98d74fac66c47fd1b46abf011cc258e13ceea` |
| `alpha_publication_full_readback_preflight_v1_20261031.py` | 5120 | `d9195e7aca20ace53b3eff3b159898b5efa0836d40204cd9acd5c9e7885eae4b` | `4ffbc155a6c20eb6b08bf41a167e85d6ba9cf6a0` |

Reproduce in a Python 3 standard-library-only sandbox from this directory:

```sh
python frozen_alpha_publication_readback_oracle_v1_20261031.py alpha_publication_full_readback_preflight_v1_20261031.py
# observed: {"oracle": "FROZEN_PUBLICATION_READBACK_ORACLE_V1", "passed": 23, "tests": 23}
```

The frozen black-box oracle runs the candidate as a separate Python subprocess and asserts **5 positive controls plus 18 negative fixtures**: missing source, changed SHA-256/blob/bytes, duplicate or traversal path, wrong main/parent, unmerged PR, wrong receipt commit/actor, absent or failed CI, C2 promotion, corrupt base64, duplicate JSON keys, NaN and malformed JSON. All 23/23 assertions passed, exit code 0.

**Before/after:** prior bounded PR/receipt mapping had **no executed original-file-byte completeness gate**; the new isolated fixture has **2/2 synthetic original-file bytes checked** against SHA-256 and Git blob and **18/18 negative cases rejected**. This is a measured test capability, **not** an observed improvement in the operational 100% publication metric.

## Scope limitations and decision

The preflight's `declared_changed_files` and `declared_checks` are caller-controlled. Its output deliberately says `LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT`, `complete_api_changed_file_census=NOT_ESTABLISHED`, `api_transport_authenticated=false`, `receipt_actor_authenticated=false` and `project_full_readback_rate=NOT_COMPUTABLE`. A full API-native consumer must independently fetch **all** PR changed-file pages, the exact main commit and its parents, the complete CI check set and the actual Issue-93 comment before any real scoped readback claim. A synthetically matching file list cannot establish completeness, and a user-supplied actor name cannot authenticate a GitHub principal.

R10 secondary watch: PR #115 current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` differs from immutable original `539d4bb33d2ba2c4895713c1bc437ece0743eeea`. The detached R10 manifest at the original head was fetched as 4,588 UTF-8 characters with Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. No new expert comment in PR #115 and no non-owner Issue-93 comment. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`. No new expert original is asserted.

No production integration, new automation, GitHub ruleset change, external actor registration, Cursor dispatch, Hostinger/WWW write, biological experiment or claim promotion. Actual PR merge, CI, main source readback and append-only Issue-93 receipt are **pending**, not predeclared as successes in this file.
