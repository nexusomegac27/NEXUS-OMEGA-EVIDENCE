# AXIOM Alpha-Node · File/directory prefix-conflict falsification · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_CHAIN_PREFIX_CONFLICT_20261028_R0
DECISION=PATCH_CANDIDATE_C1_LOCAL_TESTED_PENDING_GITHUB_MAIN_READBACK
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=505afedaf90258c6941ccd54de19746a0d6905c1
PREDECESSOR_MAIN=0bf3ac5a36402ed526cfaf222c011dfe2feea595
PREDECESSOR_ISSUE93_RECEIPT=6474399729
FROZEN_EVALUATOR_FIRST_COMMIT=4e916dd89ba01ba5e29751ec4cae5d9c2d3c9a2f
CANDIDATE_SECOND_COMMIT=2fbe1ccc162a409e596521819f9821fdf713bec4
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_READBACK_RATE=NOT_COMPUTABLE
```

## OBSERVE / ORIGINAL_BYTES / NEGATIVE_HYPOTHESIS

The existing V3 portable receipt-chain reconciler on pinned main is **2,389 bytes**, SHA-256 `3f4a4c6d845e2ee302c9ebcce6c99cebbe04fb2751e8bc2a0fe7f591ebaf7ef0`, Git blob `2f8389788b429a1c0bb890984e66c9de5cf64a03`. Its V2 predecessor is **5,666 bytes**, SHA-256 `cfa795f78bbc54d6eec9a4b5c0e44e9b36ee56285aff0cc379b2638b75d6a627`, Git blob `9dc125ed90be9f875e698a6189d3007787394f7e`. Both sources were reconstructed byte-for-byte from pinned GitHub file contents and independently rehashed locally; Git blob IDs match.

**Negative hypothesis:** V3 rejects exact and case-folded duplicate file paths but does not reject a file that is also the ancestor directory of another added file. Git cannot represent both a regular file at `x` and a file at `x/y` in the same tree. This is a caller-supplied *synthetic metadata* inconsistency, not a claim that an impossible Git tree was published.

**Falsifier:** a valid sibling-file inventory must still pass, while same-record, cross-record, reverse-order, casefolded, and nested file/directory prefix conflicts must fail closed. V3's existing negative guards and project-wide nonclaims must remain intact.

## PINNED_BASELINE / ISOLATED_CANDIDATE / SEPARATE_EVALUATOR

The evaluator was committed first, before the V4 candidate, at `4e916dd89ba01ba5e29751ec4cae5d9c2d3c9a2f`:
`frozen_receipt_chain_prefix_oracle_v4_20261028.py`, **5,777 bytes**, SHA-256 `5048ba9d0b72c1e5a73a4afeff933087cea6be84292ac493fccd6378eedf0cc2`, Git blob `d9dbaad6a3daf6dec820c2423b4ed47f4d00ca74`.

The V4 candidate was committed second at `2fbe1ccc162a409e596521819f9821fdf713bec4`:
`alpha_receipt_chain_reconciler_v4_20261028.py`, **1,723 bytes**, SHA-256 `139e7048d443e160707805281a762b6931bca6e4d6733870a580c082eb1a8506`, Git blob `af8d0d6851901338a2ad384f17a08918a15219a4`.

| Scoped metric | V3 baseline | V4 isolated |
|---|---:|---:|
| Five impossible file/directory prefix fixtures rejected | 0/5 | **5/5** |
| Three positive inventories accepted | 3/3 | **3/3** |
| Frozen independent subprocess evaluator, Linux/Python | N/A | **16/16 PASS** |
| Three selected tests against a no-prefix-check mutant | N/A | **3/3 expected failures** |
| GitHub API actor authentication | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Project-wide eligible handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

The independent evaluator invokes V3 and V4 as separate subprocesses and does not import V4. It includes five baseline-accepted negative fixtures, three positive controls, and eight retained negative/parser checks. Local negative mutant changed only the new prefix guard and failed three targeted oracle tests, as expected. Reproduce from this R16 directory:

```bash
python frozen_receipt_chain_prefix_oracle_v4_20261028.py -v
```

## DECISION / LIMITATIONS

`TESTED_IMPROVEMENT` applies only to the isolated synthetic metadata fixture scope. No production integration, external independent scientific validation, authenticated GitHub API provenance, real file-byte census, Windows-native verification, or project-wide 90%/100% goal attainment is established. This candidate cannot authenticate a forged but internally consistent input. No original bytes, existing oracle, runtime, Hostinger/WWW, external actor register, or claim ceiling is modified. Publication success, actual main and append-only Issue #93 receipt require separate post-merge readback.
