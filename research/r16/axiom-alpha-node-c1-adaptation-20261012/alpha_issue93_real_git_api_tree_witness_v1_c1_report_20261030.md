# AXIOM Alpha-Node — actual GitHub API tree/blob witness for Issue #93 V1 · 2026-10-30

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_REAL_GIT_API_TREE_WITNESS_V1_20261030_R0
DECISION=KNOWLEDGE_APPEND_C1_REAL_SOURCE_TREE_WITNESS
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
REPOSITORY=nexusomegac27/NEXUS-OMEGA-EVIDENCE
PINNED_MAIN_BEFORE=b76994d0e431949e03e37d32ea45e179034550f8
PREDECESSOR_MAIN=8ce99dd243c6d3450ddaa7308a0fc4c5d52c71cc
PREDECESSOR_PR=206
PREDECESSOR_ISSUE93_RECEIPT=6512611228
FROZEN_EVALUATOR_FIRST_BRANCH_COMMIT=e72231f5d92f979d5ea18bc700354edd3958c5c2
ACTUAL_API_WITNESS_SECOND_BRANCH_COMMIT=19c48aba7849c1bd57d709b3acc1582213fc1ec2
REAL_COMMIT_RAW_BYTE_REHASH=NOT_ESTABLISHED
GITHUB_API_COMMIT_SIGNATURE=VERIFIED_REPORTED_BY_GITHUB_NOT_LOCALLY_REVERIFIED
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## 1. Why this is new

The previous [PR #206](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/206) tested an isolated Git commit/tree/path/blob validator on synthetic Git objects only (16/16 synthetic subprocess tests). Its report explicitly identified the absence of a real GitHub object-chain test. This iteration closes a *bounded part* of that real-source gap without altering the validator, frozen historical oracle, CI, governance or runtime.

**Negative hypothesis:** the GitHub API tree entries may not reconstruct to the advertised tree SHA-1, or the pinned file may not be the blob named by the last tree. The counterexample would be any SHA mismatch or a path/entry mismatch in the real GitHub object chain.

## 2. Immutable source and provenance

Pinned main: [b76994d0e431949e03e37d32ea45e179034550f8](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/b76994d0e431949e03e37d32ea45e179034550f8), parent `8ce99dd243c6d3450ddaa7308a0fc4c5d52c71cc`.

Target original:
`research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_git_tree_binding_preflight_v1_20261030.py`.

Source acquisition used the connected GitHub API on that immutable commit: `GET /git/commits/{sha}`, four `GET /git/trees/{sha}` calls, and `GET /contents/{path}?ref={sha}`. The API returned `verification.verified=true` for the commit signature. That is a GitHub API observation, not independent local GPG validation. No raw commit object bytes were obtained; consequently the **commit object's own SHA-1 was not independently rehashed**. The API JSON tree entries were reserialized into Git's binary tree-entry representation (mode, filename, NUL, 20-byte object ID) and independently rehashed.

| Level | Expected Git tree SHA-1 | Entries | Reconstructed raw bytes | Independent rehash |
|---|---|---:|---:|---|
| Repository root | `3a2e8300090345a1fa6ac6b4263431247af42bab` | 23 | 848 | MATCH |
| `research/` | `63cfad14733cd3e8f359a6c5c83f39a3204750a5` | 21 | 668 | MATCH |
| `research/r16/` | `f8e960e6b53a14ba11dbc63ebf5df43012a6de50` | 4 | 226 | MATCH |
| R16 Alpha research directory | `b771c2d64efd165ba2e7f76530033ccf49827932` | 209 | 16,608 | MATCH |

Final path entry: mode `100644`, blob `b58dbdcd5d1ac64c717331a60641daa951043a50`.

File readback: **5,447 UTF-8 bytes**, independently calculated SHA-256 `fb62398c4f1f97a9fcb7a9900c1a24df81220231df8ab9b7076169959389f1ae`, independently calculated Git blob SHA-1 `b58dbdcd5d1ac64c717331a60641daa951043a50`; all match the immutable GitHub file readback and historical PR #206 bindings.

The new additive `alpha_issue93_real_git_api_tree_witness_v1_20261030.json` contains the exact reconstructed raw tree and file bytes as Base64, the pinned identifiers and the source URLs. It is a derived witness, **not** an original GitHub commit byte stream or a credential-bearing authenticated actor receipt.

## 3. Separate evaluator and negative fixtures

The new standalone `frozen_alpha_issue93_real_git_api_tree_oracle_v1_20261030.py` was committed **before** the derived witness. It imports neither the previous V1 validator nor its frozen evaluator. Its local `--selftest` was executed before publication: **10/10 PASS** (one synthetic positive, nine synthetic negative controls). These include altered root tree OID, modified tree bytes, swapped same-size blob, wrong byte count, wrong SHA-256, absent path, path traversal, missing tree level and duplicate JSON key.

Separately, a second independent JavaScript SHA-1 implementation reconstructed and checked the **four actual GitHub API trees** and the **one actual file blob**: **5/5 MATCH**. Mutating one byte in each of the four reconstructed real trees and in the real file blob yielded **5/5 expected hash mismatches**. The JavaScript SHA-1 implementation was checked against the standard `abc` digest; its SHA-256 implementation was checked against the standard `abc` digest and the real file's published SHA-256.

**Scope limitation:** the frozen Python evaluator's `--selftest` was run on local synthetic inputs; its execution on the newly published *real GitHub witness JSON* has not been independently observed in this environment. The actual-source 5/5 and real-byte negative mutations were independently evaluated with the separate JavaScript implementation. Do not combine these into an invented end-to-end Python PASS.

To reproduce after fetching the two new immutable files from GitHub:
```sh
python frozen_alpha_issue93_real_git_api_tree_oracle_v1_20261030.py --selftest
python frozen_alpha_issue93_real_git_api_tree_oracle_v1_20261030.py < alpha_issue93_real_git_api_tree_witness_v1_20261030.json
```

## 4. Before/after, falsifier and decision

| Scoped measure | Before (PR #206) | After (this source-bound iteration) |
|---|---:|---:|
| Actual GitHub tree objects independently reconstructed and rehashed | 0 | **4/4** |
| Actual GitHub file blob independently Git-OID/SHA-256 checked | Synthetic-only V1 evaluation | **1/1** |
| Real-source one-byte negative mutations detected | 0 actual-source tests | **5/5** |
| Independent frozen evaluator local synthetic selftests | Not applicable to this new witness | **10/10** |
| Raw Git commit SHA-1 independently rehashed | No | **No** |
| Independent expert/actor authentication | No | **No** |
| Production integration | No | **No** |

A failed reconstruction of any real tree, a wrong final file blob, or a negative fixture accepted by the evaluator falsifies the scoped improvement. A successful Git tree rehash is **not** a proof of independent GitHub actor identity, scientific correctness, Git SHA-1 collision resistance, commit signature validity independently of GitHub, or source-to-WWW parity.

## 5. Project metrics and R10 boundary

The complete authenticated population of all accessible, routine, public and authorized handoff attempts—including failures—is still missing. Therefore `AUTOMATION_RATE=NOT_COMPUTABLE` and `FULL_READBACK_RATE_PROJECT_WIDE=NOT_COMPUTABLE`. No synthetic percentage is substituted for an observed project rate.

The additional R10 check was read-only. [PR #115](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/115) remained open with no PR comments, review submissions or review threads. The original detached manifest was fetched at immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and its Git blob ID `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` matched the prior register. No new independent receiver receipt was present in the examined GitHub surfaces. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. The R10 actor allowlist remains without authorized external actors; no registration or merge is performed.

## 6. Publication boundary

This is a **single**, additive, reversible R16 research witness, not a validator promotion. Existing source files, evaluator oracles, rulesets, pipeline roots and running services are unchanged. No Hostinger, WWW, Cursor or external expert write is authorized or attempted. Merge and main readback must be checked independently after existing CI. An Issue #93 receipt must append the exact final main and file identities.
