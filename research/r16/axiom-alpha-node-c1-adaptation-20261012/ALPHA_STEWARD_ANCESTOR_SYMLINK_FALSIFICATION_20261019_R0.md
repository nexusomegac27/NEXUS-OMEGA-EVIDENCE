# AXIOM Alpha-Node C1 — Git worktree ancestor-symlink guard

OBJECT = NEXUS_OMEGA_ALPHA_STEWARD_ANCESTOR_SYMLINK_FALSIFICATION_20261019_R0
STATE = TESTED_IMPROVEMENT_ISOLATED_C1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
SOURCE = scripts/nexus_repository_steward.py
SOURCE_BYTES = 8023
SOURCE_SHA256 = 94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
SOURCE_GIT_BLOB = 296c7dc67b40f28270c92512ca6f67f8ad25fc50

## Reproduced counterexample

The existing steward checks the final path component with `is_symlink()` but not its ancestor directories. A symlinked ancestor can redirect the hash read outside the checkout. With byte-identical external content, the baseline accepts that file without an integrity fault. This is a local negative fixture, not evidence of actual exploitation in NEXUS.

## Pre-frozen independent test

Evaluator SHA-256: 7423aedf0d3a01c53b6eed7af5039629c6e7f27e4932d9bc2af44e1e3fc559c5.
Baseline: 4/7. Isolated candidate: 7/7. Deliberate first-ancestor-only mutant: 6/7.
Three negative fixtures: symlinked first ancestor with matching bytes; first ancestor with mismatching bytes; nested symlink ancestor. Candidate returns WORKTREE_SYMLINK_ANCESTOR and does not hash content.
Controls: regular tracked file, leaf symlink, missing file, changed tracked bytes.
Candidate SHA-256: 8a38589870213aa315a5ba3acd9a51634b5a2c0a1add26fae49ff95c66bc6b86.

## Scope and falsifier

Research candidate only; baseline code and independent oracle unchanged. Falsify if any symlinked ancestor is accepted and hashed, a regular file is rejected, or historical regressions fail.
The mitigation uses non-atomic path checks: concurrent symlink swaps (TOCTOU), Windows reparse-point behavior, and full repository regression are NOT_TESTED. Do not call this a complete filesystem sandbox or a production fix.
No main merge, runtime/Hostinger write, new namespace, source overwrite, external actor registration, scientific claim promotion or independent expert ACK is implied by this report.
