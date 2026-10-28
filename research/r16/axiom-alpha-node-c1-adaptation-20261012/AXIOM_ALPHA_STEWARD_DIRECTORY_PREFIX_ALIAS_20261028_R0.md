# AXIOM Alpha-Node — directory-prefix alias witness · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_DIRECTORY_PREFIX_ALIAS_20261028_R0
DECISION=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=51f10691cbc411b1e338e1d232d2901245608306
PINNED_MAIN_PARENT=bfd1a3f35ec6d565519f9a2de256e9d6d4ca5e8e
SOURCE_PATH=scripts/nexus_repository_steward.py
SOURCE_GIT_BLOB=296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_BYTES=8023
SOURCE_SHA256=94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
FROZEN_EVALUATOR_COMMIT=89d17ee38a51322a70ec694d20729bcce492f40e
CANDIDATE_COMMIT=a1c1419a2f9dfa6a2368b01b1d8591722074f0f0
PRODUCTION_STEWARD_CHANGED=NO
RUNTIME_CHANGED=NO
```

## One falsifiable quality gap

The pinned production steward uses `identity = path.casefold()` for each **complete file path** and compares that identity only against earlier complete file paths. Two different leaf filenames under directory prefixes differing only by case or NFC/NFD spelling therefore evade this specific full-path collision check. The directory-name policy may emit a legacy naming *review*, but this is not an integrity fault.

Negative fixture: `research/r16/Case/a.txt` and `research/r16/case/b.txt`. Their complete casefolded file paths differ, but their directory prefixes alias under the witness's conservative NFC/casefold portability key. A second negative fixture uses NFC/NFD variants of `café` as a directory prefix.

Alternative explanation: other repository-structure checks or actual target filesystem behavior may reject or disambiguate these paths. The test below isolates the relevant predicate, **not** the entire production steward or a real Windows/macOS filesystem.

## Frozen evaluator, candidate, metrics and falsifier

The independent test module `test_steward_directory_alias_witness_v1.py` was committed first, before the candidate, at `89d17ee38a51322a70ec694d20729bcce492f40e`; SHA-256 `e2b40b582aa2afd18d5d727b1321a404c1c565f82bd67951d03085a181db5fb7`; 3,079 bytes; Git blob `1398847390eb88f87552f36c37e52842cba5f1cd`. The candidate `steward_directory_alias_witness_v1.py` was committed separately at `a1c1419a2f9dfa6a2368b01b1d8591722074f0f0`; SHA-256 `fa963851a972ba523862ced3c6ddf2fea2e2f41534f39cdbc158eadd7a481e84`; 1,369 bytes; Git blob `f9902d8e56151864bce2076f957764d0e62c1e9b`.

Baseline: **0/3** targeted directory-prefix aliases detected by the pinned complete-path casefold predicate (one case variant, one nested case variant, one NFC/NFD variant). The isolated candidate detects **3/3**. Separate evaluator: **9/9 unittest methods PASS** under local Python. Positive controls cover distinct directories, multiple files in one directory, leaf-only case differences, and duplicate paths; malformed paths raise `ValueError`. These are synthetic fixtures, not a project-wide event census.

Independent negative mutants, applied only to a temporary candidate copy without changing the evaluator: removal of directory-prefix iteration produces **3 failing test methods**; removal of NFC normalization produces **1 failing test method**. This is the falsifier: if the witness cannot distinguish the negative fixtures from positive controls under the frozen evaluator, the candidate is rejected.

Reproduce from this existing research directory: `python test_steward_directory_alias_witness_v1.py`. All files are additive, public-safe Apache-2.0 research. No third-party code copied, no production steward modification, no external actor registration, no runtime or WWW change.

## Scope and target metrics

This is a conservative **portability warning witness**, not proof of actual filesystem aliasing, a production fix, an end-to-end audit, or scientific claim promotion. Production integration requires separate platform-specific tests and authorization. The source is unchanged. No GitHub-to-WWW parity claim is made.

`PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_ELIGIBLE_HANDOFF_DENOMINATOR=UNKNOWN`; `PROJECT_100_PERCENT_FULL_READBACK=NOT_ESTABLISHED`. The denominator **3** above is only the targeted synthetic alias-fixture cohort. `C1_DESCRIPTIVE_ONLY`.
