# AXIOM Alpha-Node · C1 structural publication matrix strict-flag guard V2

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_MATRIX_STRICT_FLAGS_V2_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=daffb9c7f80eb3f5d12af48e66dd5306d11cec1e
PREDECESSOR_MAIN=ec887632a4f1659a29c01f4db8bbf1cc79c30ae6
PREDECESSOR_RECEIPT=6550946364
FROZEN_V1_SOURCE_COMMIT=80dcb7d9f0ed29e36eef3fa7b1e47f9299dc7064
FROZEN_V1_BLOB=91bfa833837a3f90b88d35fc557da483cbb79ebc
FROZEN_V1_SHA256=96b2b69f0ebb201ea4289c08908d8133e0caf67a5acb704bfefefbe123d74995
FROZEN_EVALUATOR_FIRST_COMMIT=30890956c3c726e60153c4195dd43e4884d83c19
FROZEN_EVALUATOR_SHA256=0b89b6b64f9332d99ff5da71adcc5c35f3124ff3319c794381ce18066b1e69c8
CANDIDATE_SECOND_COMMIT=3d5abd8f6e4e58e3c60d0a33e5e0191b9a9333ce
CANDIDATE_SHA256=12bc7cb28030635fe5d07a2f54e6a17a7e86c5c5f2881ed3f1cc12fc704d9e90
ORIGINAL_BLOB_COPY_COMMIT=4075515d2e3409a17d0f95bfcc23cad76306b89c
PRODUCTION_INTEGRATION=NO
EXTERNAL_SCIENTIFIC_VALIDATION=NO
```

## Observation, counterhypothesis, and falsifier

The frozen V1 matrix oracle accepted rows with a missing `sha_match`, `blob_match`, or `bytes_match` key, an empty file assertion object, or the string `"false"` in boolean status fields. This follows from `all(f.values())` and Python truthiness. Therefore a structurally passing matrix is **not** evidence that each required assertion was present and true. The original V1 file is preserved byte-identically; V2 is an additive, isolated successor.

Counterhypothesis: V1 already rejects every absent or non-boolean required assertion. Falsifier for V2: any of the seven targeted malformed rows is accepted, or the unchanged positive matrix fails. A later falsifier for operational usefulness is an authentic GitHub evidence input that is rejected despite a valid source-bound matrix; no such E2E run was performed here.

## Frozen independent subprocess evaluation

The evaluator was committed before the candidate. It runs the original V1 `check()` and launches V2 as a separate Python subprocess, with fixed expected results. Local execution on the exact source bytes:

| Fixed fixture group | V1 | V2 | Expected |
|---|---:|---:|---:|
| Unchanged positive matrix | 1/1 accepted | 1/1 accepted | accept |
| Five pre-existing negative fixtures | 5/5 rejected | 5/5 rejected | reject |
| Seven new missing/non-boolean assertion fixtures | 0/7 rejected | 7/7 rejected | reject |
| **All expected outcomes** | **6/13** | **13/13** | exact |

The seven new fixtures are: missing SHA key, missing Git blob key, missing byte-count key, empty file assertion, string `"false"` for SHA match, string `"false"` for additive status, and string `"false"` for signature status. V2 also rejects duplicate JSON keys at the CLI boundary; that additional behavior is **not** included in the frozen 13-case measurement.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_matrix_type_evaluator_v1_20261101.py \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_census_oracle_v1_20261101.py \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_census_matrix_guard_v2_20261101.py
python scripts/validate_repository_structure.py --root .
```

## Limits and governance

This tests only a **synthetic structural assertion matrix**. No GitHub source content, CI checks, issue actor, actual commit signatures, file bytes, or SHA-256 claims are authenticated by V2. Its fixed seven-PR chain is not a project-wide denominator. The separate evaluator is frozen before the candidate but is not an external scientific reviewer. The original source was taken from the immutable V1 commit, its Git blob and SHA-256 independently matched. No existing files, oracles, runtime, workers, GitHub rules, Hostinger content, or WWW pages are modified. Publication, if successful, requires PR/CI and immutable main readback plus append-only Issue #93 receipt. No claim promotion.

Target metrics remain **NOT_COMPUTABLE** project-wide without a full authenticated denominator of eligible handoffs and publications. The isolated improvement is from 0/7 to 7/7 rejection of the new adversarial fixture class, not a measured increase in the 90% handoff automation objective.
