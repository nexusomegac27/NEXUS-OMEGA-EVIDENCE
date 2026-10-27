# NEXUS OMEGA · Alpha-Node · Steward parent-symlink C1 falsification and isolated candidate · 2026-10-27

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_PARENT_SYMLINK_NOFOLLOW_20261027_R0
DECISION=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=f3f14505bba6bd6cfea7248f4c9ace4a328362a6
PREDECESSOR_ISSUE93_RECEIPT=6450097551
NO_PRODUCTION_STEWARD_CHANGE=YES
NO_RUNTIME_OR_HOSTINGER_OR_WWW_CHANGE=YES
```

## Source/provenance (actual immutable GitHub file readback)

- Original steward: `scripts/nexus_repository_steward.py` at pinned main, **8,023 UTF-8 bytes**, Git blob `296c7dc67b40f28270c92512ca6f67f8ad25fc50`, independently computed SHA-256 `94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998`.
- Existing tests: `tests/test_nexus_repository_steward.py` at pinned main, Git blob `063365adf8d4e8738412b917df9ff1d69f44e808`; they test leaf/path traversal but contain no parent-directory-symlink fixture.
- Original `audit()` calls `actual = root.joinpath(*parts)` and checks `actual.is_file() and not actual.is_symlink()` before `actual.read_bytes()`. This checks the final path component, not each parent. Git-blob recomputation checks the read bytes, not their containment within the intended checkout.
- Authority: `AGENTS.md`, `GOVERNANCE.md`, operator direct C1 publication rule, Repository Steward V1 and existing R16 Alpha-Node adaptation contract. Research-only additive artifacts in an already registered lane.

## Negative hypothesis and falsifier

**H0 (desired containment):** A tracked path whose parent directory is replaced with a symlink to a location outside the checkout cannot be accepted as an in-checkout source, even if the outside file has exactly the expected Git blob bytes.

**Observed scoped counterexample:** In a disposable Linux temporary checkout, `research/r5` is a parent symlink to an external directory containing identical bytes for `alpha/README.md`. `leaf.is_file() == True`, `leaf.is_symlink() == False`, the recomputed Git blob matches, but `leaf.resolve()` is outside the checkout. The source-level steward predicate accepts this path. This is a **predicate-level falsification**; the full original steward CLI was **NOT_EXECUTED** on this fixture.

**Alternative explanation / scope:** A pristine, trusted Git checkout may never contain this substituted parent symlink. This is not evidence of a current repository compromise, private-file disclosure, or an exploited production issue. It is a potential false-green condition if the worktree is altered or untrusted.

## One isolated candidate; independent frozen evaluator

- Frozen evaluator first commit: `710258e4f09444bcedd42efdfce7aae5a1831812`; path `frozen_steward_nofollow_evaluator_v1_20261027.py`; **3,176 bytes**, SHA-256 `5a2fce329434475b03ae96038160d3856def0509e0066895869e5857adf84c93`.
- Isolated candidate second commit: `36014e26246b5a6d36b0952b3b38d3e586324646`; path `alpha_steward_nofollow_read_candidate_v1_20261027.py`; **2,017 bytes**, SHA-256 `c8fd1e8b33c9522b757f84929e2fac5e4198e545ed5590022514d2cfdca11a5b`.
- Candidate uses descriptor-relative `os.open` with `O_DIRECTORY|O_NOFOLLOW` on every parent, `O_NOFOLLOW` on the leaf, regular-file verification, a bounded read, and conservative path validation. It **fails closed** where required POSIX features are unavailable; Windows implementation is **NOT_ESTABLISHED**.
- Evaluator executed on Linux / Python 3.13.5 in an isolated temporary filesystem. **7/7 PASS**: regular positive, parent-symlink negative, leaf-symlink negative, traversal negative, directory negative, size-budget negative, empty-path negative.
- Baseline path predicate: **1/1 adversarial parent-symlink fixture falsely accepted**; isolated candidate: **0/1 falsely accepted**. This is a synthetic fixture denominator, not a project-wide failure rate.
- Falsification sensitivity: remove `| os.O_NOFOLLOW` from `directory_flags` in an uncommitted local mutant; frozen evaluator becomes **6/7 PASS**, with exactly the parent-symlink negative failing. The frozen evaluator was not changed to fit the candidate.

## Decision and boundaries

`PATCH_CANDIDATE` for a future, separately reviewed steward integration. This is **not** `TESTED_IMPROVEMENT_IN_PRODUCTION`: full original `steward.audit()` integration, Windows semantics, full-tree CI and all adversarial race cases remain untested. The prototype does not authenticate a GitHub actor or source origin. No new pipeline root, permission, worker, CI workflow, runtime, or source overwrite. Existing production steward and independent repository tests remain byte-identical.

Reproduction from repository checkout:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_steward_nofollow_evaluator_v1_20261027.py -v
```

**Project metrics:** `AUTOMATION_RATE=NOT_COMPUTABLE` because a complete independently authenticated eligible handoff census and denominator are absent. `PROJECT_FULL_READBACK=NOT_ESTABLISHED`. R10 independent receiver ACK/expert execution remain `NOT_ESTABLISHED`; this candidate is not an R10 expert return.

`BLOCKED_LANE != BLOCKED_SYSTEM` · `DRIFT_RESET=NON_DESTRUCTIVE` · `WWW_PARITY=NOT_ESTABLISHED`.
