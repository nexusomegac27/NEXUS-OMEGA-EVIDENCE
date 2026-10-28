# AXIOM Alpha-Node — source-pinned full-CLI parent-symlink falsification · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_PARENT_SYMLINK_E2E_20261028_R0
PREDECESSOR=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_DIRECTORY_PREFIX_ALIAS_20261028_R0
PINNED_MAIN_BEFORE=ab52f92a37c02459d0794f7193de05cdef4c34da
SOURCE=scripts/nexus_repository_steward.py
SOURCE_BYTES=8023
SOURCE_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_SHA256=94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
FROZEN_EVALUATOR_FIRST_COMMIT=d79a4a3fbe0e66399e06013c24c4836e9e3f2566
CANDIDATE_SECOND_COMMIT=d964ca23e4a2f0795da4dc72df85dd9309b32d8d
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
DECISION=PATCH_CANDIDATE_TESTED_ISOLATED_RESEARCH_ONLY
PRODUCTION_STEWARD_CHANGED=NO
```

## Why this iteration

The earlier additive research witness in PR #157 demonstrated a parent-symlink issue at the isolated path-predicate level. Its explicit limitation was that the **complete production steward CLI** had not been tested. This iteration closes that narrow evidentiary gap, without production integration or any new root/lane.

## Source-exact negative hypothesis and counterhypothesis

The pinned production steward checks `actual.is_file()` and `not actual.is_symlink()` only on the final path. A tracked regular file may be replaced in the working tree by a parent directory symlink to an outside directory containing byte-identical content. The original full CLI could then report `integrity_error_count=0` despite reading outside the checkout.

**Counterhypothesis:** the full Git tree inventory, blob comparison or existing path policy may already detect the redirection. The independent full-CLI fixture tests this directly; it does not assume the isolated predicate witness is conclusive.

## Independent evaluator, measured baseline, candidate

The frozen evaluator `test_steward_parent_symlink_e2e_v1.py` was committed first, at `d79a4a3fbe0e66399e06013c24c4836e9e3f2566`, before the candidate. Its SHA-256 is `fab242de843a64185609f1eb901321b251e87e20444dd3548bc49e27409f9758`, 5,014 bytes, Git blob `6c72599fffe49c58036e73d917f78fddaa5c606e`. The evaluator invokes the actual CLI as a subprocess in freshly created temporary Git repositories, with a tracked file and pinned source. It does not edit its oracle to accommodate the candidate.

**Baseline:** original full CLI, identical-byte parent symlink to a directory outside checkout: **1/1 false accepts**, return code 0, zero integrity faults. Original normal control: **1/1 accepted**. This is a local synthetic proof of a scoped false-negative condition, not evidence of a malicious event in the live repository.

**Candidate:** `steward_parent_symlink_e2e_patch_candidate_v1.py`, second commit `d964ca23e4a2f0795da4dc72df85dd9309b32d8d`, SHA-256 `c3f2c5a15591127b7a1957132bbcfb74bd227d803efa00063b4d3a5c1b85f0c5`, 3,004 bytes, Git blob `86320cd79bfc0e4280f06af5c23bfbf8cb712cd0`. It constructs a source-exact, disposable patch of the original steward, using `dir_fd` + `O_NOFOLLOW` on every ancestor and leaf, and records `UNSAFE_PATH_COMPONENT` on an unsafe read. It refuses a source SHA mismatch. It is **not** a change to `scripts/nexus_repository_steward.py`.

**After:** isolated patched full CLI, identical-byte parent symlink: **0/1 false accepts**, return code 1 and `UNSAFE_PATH_COMPONENT`. Frozen evaluator **11/11 PASS**, including two parent-symlink negatives, regular-file hash mismatch, leaf symlink, positive report parity, source drift rejection and no source mutation. A separately constructed negative mutant that removes `O_NOFOLLOW` fails **2/11 evaluator methods** as expected. The evaluator's parity check excludes synthetic Git commit IDs, which legitimately differ between independently initialized fixture repositories.

## Reproduction and falsifier

From the repository root on Linux/POSIX with Python and Git available:

`python research/r16/axiom-alpha-node-c1-adaptation-20261012/test_steward_parent_symlink_e2e_v1.py`

**Falsifier:** if the frozen evaluator accepts the parent-symlink mutant, fails the positive controls, or the candidate changes the original production source, reject the candidate. The evaluator and candidate are independently versioned. The local tests were executed in separate subprocesses; GitHub CI, if green, is a separate platform observation, not a substitute for the isolated test.

## Scope and limits

No Windows filesystem or macOS validation; `O_NOFOLLOW` availability and semantics vary by platform. No adversarial mount-point, hardlink or concurrent rename proof. The root path is resolved by the original CLI. A source-exact patch constructor is not a production remediation, CI merge gate, or authority to deploy. The full project-wide handoff denominator remains unknown, so `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_100_PERCENT_READBACK=NOT_ESTABLISHED`.

No external actor registration, source overwrite, Hostinger/WWW write, runtime modification, new automation, or claim promotion. `BLOCKED_LANE != BLOCKED_SYSTEM`; `WWW_PARITY=NOT_ESTABLISHED`.
