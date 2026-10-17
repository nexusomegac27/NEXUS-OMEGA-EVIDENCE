# AXIOM R99 — Portable directory case-collision guard (isolated C1 research)

```text
OBJECT = NEXUS_OMEGA_AXIOM_R99_PORTABLE_DIRECTORY_CASE_COLLISION_GUARD_20261017_R0
STATE = TESTED_IMPROVEMENT_CANDIDATE_C1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR = R98_NONFINITE_JSON_METADATA_FAIL_CLOSED_C1_BYTE_AND_ISOLATED_REPLAY_VERIFIED
SOURCE = scripts/nexus_repository_steward.py
SOURCE_GIT_BLOB = 296c7dc67b40f28270c92512ca6f67f8ad25fc50
SOURCE_BYTES = 8023
SOURCE_SHA256 = 94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998
LEGACY_TEST_BLOB = 063365adf8d4e8738412b917df9ff1d69f44e808
LEGACY_TEST_BYTES = 4445
LEGACY_TEST_SHA256 = 76e8701cb52a7ad54a5ede01d3f6c04193b21885996f4bf597112276623614a0
```

## Source-exact finding and counterhypothesis

The pinned Repository Steward V1 detects full-file casefold collisions, but does not detect two differently cased *directory prefixes* when their files have different basenames. Synthetic counterexample: `research/r5/alpha/README.md` and `research/r5/ALPHA/notes.md`. On a case-insensitive checkout these directory names can collapse. The main-tree census of 501 blobs found **zero actual casefold-colliding directory groups**; this is a prospective quality guard, not evidence of current damage.

## Isolated test and falsifier

A separate 14-case evaluator was frozen **before** implementing the candidate; its SHA-256 is `cfe52ee7a4e3905c0a78e7fce1c005d7390e093f0a2cb93dae900cc4d79ed371`.

| Metric | Pinned original | Isolated candidate |
|---|---:|---:|
| Frozen evaluator | 9/14 | **14/14 PASS** |
| Five divergent-parent negative fixtures detected | 0/5 | **5/5** |
| Unchanged legacy test suite | 12/12 | **12/12 PASS** |

Candidate SHA-256: `7d182638d439b981f2776a2490c9a6168870aedc38c777aa820e369e8179112e`.

The isolated patch computes casefold identities for **each tracked directory prefix**, flags any key with more than one distinct spelling, and emits `PORTABLE_DIRECTORY_CASE_COLLISION` for affected tracked files as an integrity fault. It does not move, overwrite or mutate source files.

**Falsifier:** If the original detects both affected paths in the divergent-parent fixture, the bug hypothesis fails; if the candidate misses either affected path or flags a same-spelling/unrelated directory, the candidate fails. The baseline failed five negative cases, while the candidate passed them; the original 12 tests remain green.

## Governance and limitations

This is a **tested isolated scaffold candidate**, not a production-integrated steward or independent external acceptance. Unicode normalization and filesystem-specific aliasing are not covered. This report does not publish the executable candidate or frozen evaluator bytes; those are separately hashed in the local reproducible archive and remain a transport gap until published. No self-approval of evaluator, no runtime, no Hostinger, no WWW, no main merge, no R9/R10 scientific promotion.

The authorized 30-day public handoff denominator and verified autonomous-success numerator remain **UNKNOWN**, so the 90% target is **NOT_COMPUTABLE**. A branch commit alone is not main publication or scientific validity.
