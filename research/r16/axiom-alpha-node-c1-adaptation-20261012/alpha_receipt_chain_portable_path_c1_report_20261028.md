# AXIOM Alpha-Node · Portable receipt-inventory path guard · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_CHAIN_PORTABLE_PATH_GUARD_20261028_R0
DECISION=TESTED_C1_ISOLATED_CANDIDATE_PENDING_PUBLICATION_READBACK
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=0bf3ac5a36402ed526cfaf222c011dfe2feea595
PREDECESSOR_MAIN=c0f69e9fcd2ff54243ffa1bf3aa9d90ce2bda62d
PREDECESSOR_ISSUE93_RECEIPT=6473538115
FROZEN_EVALUATOR_FIRST_COMMIT=42973eb8baffff28d7d1dbc9096860864492acfa
CANDIDATE_SECOND_COMMIT=f406c5135015e347a700229e68e0aaac34ef3f54
EXTERNAL_ACTOR_REGISTRY=EMPTY_DEFAULT_DENY_UNCHANGED
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_READBACK_RATE=NOT_COMPUTABLE
```

## OBSERVE / ORIGINAL BYTES / NEGATIVE HYPOTHESIS

The original V2 reconciler, `alpha_receipt_chain_reconciler_v2_20261028.py`, was read at immutable main `0bf3ac5a36402ed526cfaf222c011dfe2feea595`. Original: **5,666 bytes**, Git blob `9dc125ed90be9f875e698a6189d3007787394f7e`, independently computed SHA-256 `cfa795f78bbc54d6eec9a4b5c0e44e9b36ee56285aff0cc379b2638b75d6a627`. The V2 path predicate requires ASCII, the canonical R16 prefix, no traversal or backslash, and literal path uniqueness. It does **not** reject Windows-reserved device basenames, forbidden Windows characters, trailing dot/space or case-insensitive aliases. This is a narrow cross-platform inventory ambiguity, **not** proof that these paths were ever published.

**Falsifier:** V3 must accept the same valid synthetic 4+4-file chain and one-PR four-file subset, but reject every V2-accepted portable-path negative fixture. V3 must retain V2's strict JSON, predecessor and inventory gates and all nonclaims.

## PINNED BASELINE / ISOLATED CANDIDATE / SEPARATE EVALUATOR

The frozen black-box oracle was committed first, at `42973eb8baffff28d7d1dbc9096860864492acfa`, before V3 was committed. It invokes V2 and V3 as separate subprocesses; it does not import candidate code. Its Git blob is `29b7dffae45c024cf453bfe8191bbf78fb760cb9`, SHA-256 `e71a80691bcefb4d20839d434e2325f2f4447fc652dd35647f124bd64cd333f5`, **6,070 bytes**.

V3 was committed second at `f406c5135015e347a700229e68e0aaac34ef3f54`, Git blob `2f8389788b429a1c0bb890984e66c9de5cf64a03`, SHA-256 `3f4a4c6d845e2ee302c9ebcce6c99cebbe04fb2751e8bc2a0fe7f591ebaf7ef0`, **2,389 bytes**. It imports immutable V2 and adds a fail-closed portable-path check. No existing source, productive Steward, oracle, runtime or permission is modified.

| Scoped metric | V2 baseline | V3 isolated |
|---|---:|---:|
| Nine V2-accepted ambiguous-path negative fixtures detected | 0/9 | **9/9** |
| Valid 4+4 synthetic chain | PASS | PASS |
| Separate frozen black-box tests (Python 3.13.5, Linux) | N/A | **18/18 PASS** |
| Mutant omitting case-fold collision check | N/A | **2/2 expected failures** |
| Mutant omitting device-name guard | N/A | **3/3 expected failures** |
| API origin / PR actor authentication | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Project-wide eligible handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

Nine negative fixtures: two case-only aliases (same/across PR), three Windows device basenames (`CON.py`, `lpt9.log`, `NUL`), two forbidden Windows characters (colon/NTFS stream and wildcard), and two trailing-dot/space names. The baseline accepted all nine as syntactically valid metadata; V3 rejected all nine. Three positive controls and six retained parser/chain negatives complete the 18 tests. The two targeted mutants were **not** committed; they were run only as isolated local negative controls.

Reproduce from the existing R16 directory:

```bash
python frozen_receipt_chain_portable_paths_oracle_v3_20261028.py -v
```

## DECISION / LIMITATIONS

`TESTED_IMPROVEMENT` is limited to these isolated Linux/Python subprocess tests and the explicitly described synthetic metadata fixtures. Windows-native filesystem behavior, live GitHub API authentication, original PR file-byte validation, CI execution of this oracle and external third-party adjudication are **NOT_ESTABLISHED**. A forged but internally consistent metadata chain can still pass. The candidate is not production-integrated and cannot establish 90% automation or 100% project-wide readback. No new worker, root, runtime, Hostinger/WWW action, external actor registration, claim promotion or historical-path mutation. Actual PR merge, main and append-only Issue #93 receipt require separate subsequent verification.
