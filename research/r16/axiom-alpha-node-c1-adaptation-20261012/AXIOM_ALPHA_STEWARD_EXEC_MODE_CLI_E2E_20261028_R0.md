# AXIOM Alpha-Node — POSIX executable-mode drift · complete Steward CLI falsification · 2026-10-28 R0

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_EXEC_MODE_CLI_E2E_20261028_R0
CLASS=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
PREDECESSOR=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_EXEC_MODE_DRIFT_20261028_R0
PREDECESSOR_ISSUE93_RECEIPT=6459186780
PINNED_MAIN_BEFORE=87a03eaeea53df76aade881259600fe6e08ee0ec
SOURCE_PATH=scripts/nexus_repository_steward.py
SOURCE_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_BYTES=8023
SOURCE_SHA256_INDEPENDENT_LOCAL=94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
EVALUATOR_FIRST_COMMIT=7bc179301f9bab494dd3458adc8c7a4d70163217
CANDIDATE_SECOND_COMMIT=315ad820d23fedd5a793f99e63b1dc178084ec4e
EVALUATOR_GIT_BLOB=2dafc69c9124246ee387ffd371b1ded2d2dab1a5
EVALUATOR_SHA256=d267372499b2323ccbd42e26fa19087795368c241775bf182ee964b4dcec91c2
EVALUATOR_BYTES=5211
CANDIDATE_GIT_BLOB=133bd8e8ea0da7aff3c64a94ab8dad32fb07db06
CANDIDATE_SHA256=3b059f484dd1ace86d047077a90d70a7f7408483635024cc6ce869274bcde67b
CANDIDATE_BYTES=1252
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY

## Negative hypothesis and falsifier

Does the **actual pinned complete Steward CLI** falsely accept a synthetic Git checkout whose committed executable mode and POSIX worktree executable bits disagree despite matching Git blob bytes? This was not established by the predecessor's source inspection and isolated witness alone.

Counterhypothesis: the complete CLI, policy, Git-tree parsing or integrity exit gate already detects executable-mode drift. Falsifier: if the original CLI exits nonzero with a mode-specific integrity finding for either drift fixture, the claimed original-CLI detection gap is refuted.

## Original bytes, isolation and measured results

The exact original Steward script was fetched from immutable main and independently reconstituted in a local isolated directory. Its 8,023 bytes match the pinned SHA-256 and Git blob above. Tests create temporary POSIX Git repositories with committed modes 100755 or 100644, then alter only worktree executable bits; file content and committed Git blob remain unchanged. Both complete CLIs run with --fail-on-integrity.

| Fixture | Original CLI | Isolated patched CLI |
|---|---|---|
| Git 100755, worktree executable | exit 0 | exit 0 |
| Git 100644, worktree nonexecutable | exit 0 | exit 0 |
| Git 100755, worktree nonexecutable | false accept: exit 0 | reject: exit 1, GIT_WORKTREE_EXEC_MODE_MISMATCH |
| Git 100644, worktree executable | false accept: exit 0 | reject: exit 1, GIT_WORKTREE_EXEC_MODE_MISMATCH |

Before/after mode-drift detection: **0/2 → 2/2 synthetic negatives**. The evaluator was committed before the candidate. Local evaluator: **12/12 PASS** on Python 3.13.5, Git 2.47.3, Linux/POSIX. A separate mutant disabling the new conditional produced **2 expected evaluator failures** (test_08 and test_09). Original source unchanged; positive-output parity compared after removing only the fixture-specific Git source_commit.

## Reproduce

Run: python research/r16/axiom-alpha-node-c1-adaptation-20261012/test_steward_exec_mode_cli_e2e_v2.py -v

The evaluator loads scripts/nexus_repository_steward.py from the checkout and applies the source-pinned patch constructor to an in-memory string. Only temporary fixture checkouts are mutated. No productive Steward, historical evidence, ruleset, CI oracle, runtime, Hostinger or WWW file is changed.

## Scientific limits and decision

This is an isolated **research-only** integration witness. The mode check uses stat() and **does not solve** the independently documented parent-symlink vulnerability, TOCTOU races, Windows/macOS portability, or filesystems where executable-bit semantics differ. It is not a deployed security repair, real incident finding, external third-party validation, or scientific claim promotion.

The complete eligible project Handoff denominator is not independently authenticated; project-wide 90% automation and 100% readback remain NOT_ESTABLISHED. Publication, if authorized and CI-clean, requires actual immutable main readback and a separate append-only Issue #93 receipt. R10 expert-receiver and GitHub-actor states remain independently gated.
