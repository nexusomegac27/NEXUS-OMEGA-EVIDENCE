# AXIOM Alpha-Node — Git commit/tree/blob binding preflight V1 — 2026-10-30

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_GIT_TREE_BINDING_PREFLIGHT_V1_20261030_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
REPOSITORY=nexusomegac27/NEXUS-OMEGA-EVIDENCE
PINNED_MAIN_BEFORE=8ce99dd243c6d3450ddaa7308a0fc4c5d52c71cc
PREDECESSOR_PR=205
PREDECESSOR_ISSUE93_RECEIPT=6512184316
BASELINE_PATH=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_receipt_byte_preflight_v1_20261030.py
BASELINE_GIT_BLOB=3d9a9e65969cc78ed4ad0f6f16f91df4398204ca
FROZEN_ORACLE_FIRST_BRANCH_COMMIT=6eede1d9db52fd47dee0067e5817f8af4659c129
CANDIDATE_SECOND_BRANCH_COMMIT=af9fa30282935728a873c9f8d6844f6b0c13eeea
GITHUB_AUTHENTICATION=NOT_ESTABLISHED_BY_ISOLATED_CANDIDATE
PRODUCTION_INTEGRATION=NO
HOSTINGER_WRITE=NO
WWW_PARITY=NOT_ESTABLISHED
```

## Source observation and negative hypothesis

The pinned predecessor V1 verifies caller-supplied file bytes against a caller-supplied Git-blob SHA-1 and optionally claimed SHA-256/byte count. It validates the shape of a `commit_sha` string but does **not** bind that commit to the path or blob; the source explicitly disclaims GitHub authentication. This is a scoped *coverage gap*, not a false claim in V1.

**Negative hypothesis:** a fabricated 40-hex commit ID paired with a self-consistent blob can pass V1's byte-only checks. V1's source code contains no Git commit or tree object verification. A commit/path/blob linkage test should reject this mutation without changing V1 or declaring remote authenticity.

## Isolated candidate and falsifier

The new preflight reads caller-supplied raw Git commit, tree-chain and blob bytes (Base64); recomputes the Git object IDs for commit, each tree and blob; walks exact path components; rejects missing entries, nonregular/symlink modes, malformed trees, changed object bytes, wrong length and wrong SHA-256. It is **read-only**, offline, limited to the existing R16 research path and one blob per invocation. It does not update existing checks, evaluator files, GitHub configuration, identities, rights or running services.

**Falsifier:** if a fake pinned commit ID, altered tree or same-size substituted blob passes while a genuine synthetic chain fails, the claimed integrity improvement is refuted. Git SHA-1 is not collision-resistant against a sufficiently capable adversary; a self-consistent caller-generated object chain does not authenticate GitHub origin or actor identity. A real GitHub checkout/API proof, source-transport binding, security review and external validation remain separate.

## Frozen independent subprocess evaluation

The evaluator constructs its own synthetic Git objects without importing the candidate and executes the candidate in isolated Python subprocesses. It was versioned in the owner branch **before** the candidate commit. The exact frozen evaluator and candidate bytes were separately rehashed and their Git-blob IDs checked against the branch.

| Metric | Predecessor V1 | Isolated new preflight |
|---|---|---|
| Commit-to-tree-to-path-to-blob verification | 0 checks (source inspection; by design) | 1 full synthetic chain check |
| Fabricated commit SHA with matching blob | Not rejected by commit/path binding (source inspection) | `COMMIT_OID_MISMATCH` |
| Changed root tree | No tree-chain check | `TREE_OID_MISMATCH` |
| Same-length substituted blob | Blob check exists | `BLOB_OID_MISMATCH` |
| Frozen subprocess tests | Not applicable to V1 | **16/16 PASS** |
| External GitHub actor authentication | None | None |

The 16 cases include 3 positive/label controls and 13 negative/constraint checks: wrong commit, changed commit bytes, changed tree, absent path, substituted blob, wrong byte count/SHA-256, missing tree level, duplicate JSON key, traversal, malformed Base64, symlink mode and truncated tree. The legacy baseline was assessed by source inspection rather than a fresh V1 execution. The new tests use synthetic Git objects only; no real GitHub commit/tree chain was executed in this evaluation.

## Byte identity of proposed additive research files

| File | UTF-8 bytes | SHA-256 | Git-blob SHA-1 |
|---|---:|---|---|
| `frozen_alpha_issue93_git_tree_binding_oracle_v1_20261030.py` | 6539 | `3bb08d395f81d82e2172e48b6dfd0563d409f9f9b8d83cb4609491777e82917f` | `913a628a6536a98f54c8e25a4b2852d8b8d88c8d` |
| `alpha_issue93_git_tree_binding_preflight_v1_20261030.py` | 5447 | `fb62398c4f1f97a9fcb7a9900c1a24df81220231df8ab9b7076169959389f1ae` | `b58dbdcd5d1ac64c717331a60641daa951043a50` |

## Boundaries and target metrics

This candidate does **not** establish an authenticated GitHub source, successful repository-wide validator integration, scientific correctness, GitHub-to-WWW parity, or a production fix. The complete authenticated denominator for routine authorized public handoff attempts remains unavailable: `AUTOMATION_RATE=NOT_COMPUTABLE`; project-wide full-readback denominator remains `NOT_COMPUTABLE`. Synthetic 16/16 is not a project-wide success rate. No new R10 independent expert receipt was found in PR #115 comments/reviews/threads during this read-only check; owner SEND remains distinct from independent receiver ACK and executed expert research.

Publication requires existing owner branch/PR/CI checks, immutable main readback, and a separate append-only Issue #93 receipt. A PR branch commit or this report alone does not prove merge or main publication.
