# AXIOM Alpha-Node — Win32 superscript device-name witness · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_WIN32_SUPERSCRIPT_DEVICE_NAMES_20261028_R0
STATE=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=bfd1a3f35ec6d565519f9a2de256e9d6d4ca5e8e
PINNED_STEWARD_PATH=scripts/nexus_repository_steward.py
PINNED_STEWARD_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
FROZEN_EVALUATOR_COMMIT=1e255e5871cff7483ea2730979cf1c0a635305f2
CANDIDATE_COMMIT=013c86b1e1afd5416c6912b829ab176d204d90e1
PRODUCTION_STEWARD_CHANGED=NO
RUNTIME_CHANGED=NO
```

## Primary source and falsifiable hypothesis

The pinned steward source has `RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\\..*)?$", re.I)`. This predicate excludes the six Win32 device-name bases `COM¹`, `COM²`, `COM³`, `LPT¹`, `LPT²`, `LPT³`. Microsoft explicitly lists those six and their extension forms as reserved in its primary Win32 naming reference: https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file (consulted 2026-10-28).

Negative hypothesis: the current predicate fails to flag these names despite a valid Git tree path on a case-sensitive filesystem. Alternative: the full steward may reject such a path through an unrelated integrity rule; this isolated predicate test does not establish full-program acceptance.

## Frozen evaluator and isolated test

Evaluator: `test_win_device_witness_v1.py`, independently committed *before* candidate as `1e255e5871cff7483ea2730979cf1c0a635305f2`; Git blob `fbe881dca860c73894a0008aecb004c26ce795ba`; SHA-256 `d19287e99201b3d348f3bd720751641a8e5e43d76634ccb328198f924eb72e11`; 2649 UTF-8 bytes.

Candidate: `win_device_name_witness_v1.py`; Git blob `6c8e9cedea425c8a01a0e59539b218458b18d066`; SHA-256 `4db9eca80cd5ee47b004b5b835960293eff45b13e5ed19c7d367cb4b3db94ee2`; 1004 UTF-8 bytes.

Reproduce from this directory: `python test_win_device_witness_v1.py`. Locally observed with a separate Python process: **5/5 unittest methods PASS**. The superscript fixture matrix covers 2 prefixes × 3 superscript digits × 2 suffixes = **12/12 cases**. Baseline predicate: **0/12 flagged**. Candidate: **12/12 flagged**. Existing ASCII device names, eight nondevice controls, nested path checks and invalid relative path checks also pass. This is not a Windows filesystem execution test.

Falsifier/mutant: replace `COM[1-9¹²³]|LPT[1-9¹²³]` with `COM[1-9]|LPT[1-9]` in a *temporary copy of the candidate only*. The unchanged frozen evaluator exits 1, reporting 13 failures (12 superscript subtests plus one nested-path assertion). The committed evaluator was not edited.

## Scope and limits

This witness is isolated research; it does **not** modify or automatically approve `scripts/nexus_repository_steward.py`, GitHub branch rules, repository order, Windows runtime, the external actor registry, or any model/runtime instructions. The full original steward was not run end-to-end against a synthetic Git tree in this iteration. No claim that a currently tracked repository path is affected; no external third-party scientific validation. No claim promotion. A production fix would require separate platform-aware end-to-end tests, code review and governed integration.

Baseline and denominator here are **12 targeted negative path cases**, not a project-wide handoff census. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_100_PERCENT_READBACK=NOT_ESTABLISHED` until an independently complete event census exists.
