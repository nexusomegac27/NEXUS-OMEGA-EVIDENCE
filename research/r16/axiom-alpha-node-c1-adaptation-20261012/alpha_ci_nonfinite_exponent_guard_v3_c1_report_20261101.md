# AXIOM Alpha-Node — CI JSON nonfinite-exponent fail-closed V3 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_NONFINITE_EXPONENT_GUARD_V3_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=d81dab8a6c1c57fe238c8e54a17e91c9386ddb63
PREDECESSOR_PR=261
PREDECESSOR_ISSUE93_RECEIPT=6555719137
FROZEN_EVALUATOR_FIRST_COMMIT=8fbd3c266cb9f637aec55f3328425d32d6d2a352
CANDIDATE_SECOND_COMMIT=1caf72d5f133dbe89235f09dc919803840e8e6e6
STDOUT_THIRD_COMMIT=81696cc185c6e8d31930df523c4c145c36a07c98
PRODUCTION_INTEGRATION=NO
```

## Source and hypothesis

At pinned main, `alpha_publication_ci_name_app_binding_guard_v2_20261101.py` is 1869 bytes, SHA-256 `bf92523f502b5ca2039696e8b0cef2d5d4841a18fb41655691ddd22eb0a47b8f`, Git blob `363ca6cee49e4e3c6a78fbc3b5a6127c1f006588`. Its `json.loads` uses `parse_constant=reject_constant` but no `parse_float` override. Python parses JSON number `1e309` to positive infinity. A structurally valid seven-PR matrix with an additional `"probe":1e309` field therefore receives `accepted=true`, despite containing a nonfinite numeric value. This is a bounded input-format false acceptance, **not** evidence that real GitHub CI was compromised.

The frozen upstream dependencies were independently rehashed against their published receipts: matrix V2 2754 bytes SHA-256 `12bc7cb28030635fe5d07a2f54e6a17a7e86c5c5f2881ed3f1cc12fc704d9e90`; CI identity V1 2410 bytes SHA-256 `65ef7e3773a13b21abb20c7912b81587b151d49e35969be6f7a94653742e8c51`.

**Negative hypothesis:** Rejecting all overflow exponents may also reject valid finite exponents or break positive historical fixtures. **Falsifier:** V3 accepts any of five overflow fixtures, rejects either of two valid positives, or differs on the two existing malformed controls.

## Frozen independent evaluator and measured delta

The evaluator was committed before the candidate, and executes the original V2 and new V3 as **separate Python subprocesses**. It uses a synthetic seven-PR matrix with the historical frozen PR/commit/receipt chain, positive CI-name/app multiset and valid run identities. The five negative fixtures inject `1e309`, `-1e309`, `9e999`, `1e999999`, and nested `3.14e9999` without changing required structural fields.

| Metric | V2 original | V3 candidate |
|---|---:|---:|
| Valid positive controls accepted | 2/2 | 2/2 |
| New nonfinite exponent negatives rejected | 0/5 | 5/5 |
| Existing NaN and duplicate-key negatives rejected | 2/2 | 2/2 |
| Expected outcomes | 4/9 | 9/9 |

The independently frozen evaluator returned 9/9 expected comparison outcomes, exit 0. The `parse_float` hook rejects nonfinite `float` results via `math.isfinite`, while retaining duplicate-key and literal-NaN rejection. No historical file, V2 validator, frozen evaluator, workflow, permissions, registry or productive runtime was modified.

Local source and stdout SHA-256:
- Frozen evaluator: 3983 bytes, `9c043c44b50caef6ad9faf8e79cccd48c805ba0c437908c829d6923d923cfe18`
- V3 candidate: 2059 bytes, `89634a4707cbc0b4da8955045df254f948ae7c9dae1f88222a50a2c9aca2d81a`
- Stdout JSONL: 1295 bytes, `1ce6992dda81aca996ce9e9aede631a713086738573abe18672f0f61201e67f7`

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_nonfinite_exponent_evaluator_v1_20261101.py
```

## Scope and publication boundary

This is a **synthetic JSON-format regression** of a research-only CI-provenance guard for the historical seven-PR cohort. It does not fetch GitHub API originals, authenticate a GitHub actor, validate the complete repository, prove all source hashes, or establish a production security failure rate. It is not a universal JSON parser proof. No R10 receiver ACK, external actor registration, Hostinger/WWW parity, scientific claim promotion or autonomous runtime is implied.

Project-wide handoff automation and publication readback rates remain `NOT_COMPUTABLE`: the complete authenticated eligible-attempt and publication denominators are not available. A successful isolated PR must be followed by actual CI, merge/main, four-file byte/SHA-256/blob and Issue #93 append-only readback before being called published.
