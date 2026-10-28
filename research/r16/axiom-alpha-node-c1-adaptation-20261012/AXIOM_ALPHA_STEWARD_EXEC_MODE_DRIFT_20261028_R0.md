# AXIOM Alpha-Node — POSIX Git executable-mode drift witness · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_EXEC_MODE_DRIFT_20261028_R0
PREDECESSOR=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_PARENT_SYMLINK_E2E_20261028_R0
PREDECESSOR_ISSUE93_RECEIPT=6458304725
PINNED_MAIN_BEFORE=8b4d27bc5bf1a1874665e793802443dcdc2040a9
SOURCE=scripts/nexus_repository_steward.py
SOURCE_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_BYTES=8023
SOURCE_SHA256_PRIOR_RECEIPT=94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
SOURCE_SHA256_RECOMPUTED_THIS_RUN=NO
EVALUATOR_FIRST_COMMIT=47632d4e347b76f4b036557b6f54280d7c49596a
CANDIDATE_SECOND_COMMIT=2527c773cbf3ca67312bee0afa5b2a11f4a08c76
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
STATE=PATCH_CANDIDATE_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
```

## One negative hypothesis, independent countercheck

The pinned production steward inventories Git mode values but its `audit()` checks only file presence, bytes and Git blob identity, not executable permission bits. Therefore a tracked `100755` file changed to nonexecutable (`0644`), or a tracked `100644` file made executable (`0755`), may retain matching bytes/blob while the worktree execution semantics diverge. This is a reproducibility and portability risk, not a claim of a real repository incident.

**Counterhypothesis:** Git content hashing or the existing steward path policy might already detect the permission drift. Direct inspection of the pinned source shows no `st_mode` or equivalent executable-bit comparison. The independent POSIX Git fixture demonstrates that the content SHA-1 Git blob remains identical after chmod, while Git's committed mode remains `100755`. This is source inspection plus isolated Git-fixture evidence; the original complete steward CLI was **not** re-executed against this new fixture.

## Frozen evaluator and isolated candidate

The independent evaluator `test_steward_exec_mode_witness_v1.py` was committed first. Its original local SHA-256 is `ab5d618c7e72c1eabf22b974572f685a9dd8a674f1ff594a5a50d2d2e956ee3f`, 3,415 bytes, Git blob `02b890c79c6216d408eb849428fb6157265f7fff`. The candidate `steward_exec_mode_witness_v1.py` was committed second; local SHA-256 `3dd87336845b7e01df3acaf367ebd2531e6141edcb747bce85f636958c93314f`, 1,852 bytes, Git blob `a3c9501de72ced4ae366851c0bb4ba1b49e57e8d`.

Measured POSIX fixture results: positive controls **2/2 accepted**; executable-bit negative fixtures **2/2 detected** (removed + added executable permission); byte-identical Git-blob negative control **1/1 detected by the candidate while the blob still matched**; unsafe parent symlink and traversal **2/2 flagged as NOT_ASSESSED**, not silently accepted. Frozen evaluator **8/8 PASS** in a separate Python process. A one-defect negative mutant suppressing the mode comparison failed **3/8 methods**, as expected (two errors, one failure).

**Before/after detection on the two mode-drift fixtures:** source-inspected baseline mode-specific detection **0/2** (not full-CLI black-box measured); isolated candidate **2/2**. No project-wide defect-rate inference is permitted.

## Reproduction, falsifier and limitations

From repository root on a POSIX host with Python and Git:

`python research/r16/axiom-alpha-node-c1-adaptation-20261012/test_steward_exec_mode_witness_v1.py`

Reject the candidate if either permission mutation is missed, a positive control is flagged, the Git blob no longer matches after chmod, or the negative mutant passes. The witness uses `lstat` for research-only observations; it is **not** race-safe security confinement. POSIX-only; no Windows/macOS filesystem proof, no live-repository mode-drift census, no productive steward change, no new authority or runtime worker. GitHub CI and merge/main/receipt readbacks are separate publication gates.

The full authenticated project-wide eligible handoff denominator remains unknown. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_100_PERCENT_READBACK=NOT_ESTABLISHED`. No R10 expert return or external-actor authority is implied. No Hostinger/WWW write, no model self-modification, no Claim-Promotion.
