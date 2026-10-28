# AXIOM Alpha-Node · Repeated-main-commit falsification · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_CHAIN_COMMIT_ACYCLIC_20261028_R0
DECISION=PATCH_CANDIDATE_C1_LOCAL_TESTED_PENDING_MAIN_READBACK
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=bd1c230cdc005196a256b5f2c23133b5563479a2
PINNED_MAIN_PARENT=505afedaf90258c6941ccd54de19746a0d6905c1
PREDECESSOR_ISSUE93_RECEIPT=6476336042
FROZEN_EVALUATOR_FIRST_COMMIT=fa6a7d3ddd9dd185e0fdf79d9ddec2d0beaba3a8
CANDIDATE_SECOND_COMMIT=3082907987c1d02e0a10dffa8414d14600b7d134
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_READBACK_RATE=NOT_COMPUTABLE
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The source of authority is `nexusomegac27/NEXUS-OMEGA-EVIDENCE` at the pinned `main` above, under `AGENTS.md`, `GOVERNANCE.md`, the standing R16 Alpha-Node contract, direct C1 research publication rule and Repository Order Law V1. Issue #93 last observed receipt `6476336042` is a GitHub owner comment, not a scientific oracle. The V4 original `alpha_receipt_chain_reconciler_v4_20261028.py` was retrieved from that pinned commit and independently reconstructed: **1,723 bytes**, SHA-256 `139e7048d443e160707805281a762b6931bca6e4d6733870a580c082eb1a8506`, Git blob `af8d0d6851901338a2ad384f17a08918a15219a4`. Its immutable V3 and V2 predecessors were also independently rehashed: V3 2,389 bytes, SHA-256 `3f4a4c6d845e2ee302c9ebcce6c99cebbe04fb2751e8bc2a0fe7f591ebaf7ef0`; V2 5,666 bytes, SHA-256 `cfa795f78bbc54d6eec9a4b5c0e44e9b36ee56285aff0cc379b2638b75d6a627`.

## NEGATIVE HYPOTHESIS / FALSIFIER

The existing V4 checks receipt predecessor and `main` parent equality but accepts a syntactically consistent **impossible Git commit history** if the caller supplies a `merge_sha` equal to the base commit, a self-parent, or a cycle to an earlier commit. The `compare.ahead=1` metadata is then contradictory to the repeated commit ID. This is a synthetic metadata acceptance gap, not evidence of a real GitHub commit graph defect.

Falsifier: V4 must accept at least six different cyclic/repeated-ID fixtures while V5 must reject them with `REPEATED_MAIN_COMMIT_SHA`; three distinct acyclic histories must still pass, and all retained V4 negative checks must remain fail-closed. A separate evaluator must fail against a no-acyclic-check mutant.

## PINNED BASELINE / INDEPENDENT EVALUATOR / ISOLATED CANDIDATE

The black-box evaluator was committed **before** the candidate, at `fa6a7d3ddd9dd185e0fdf79d9ddec2d0beaba3a8`:
`frozen_receipt_chain_commit_acyclic_oracle_v5_20261028.py`, **5,563 bytes**, SHA-256 `c9aba3ed0eef0e97863340903c5b366c9c967060b28d6a979a2a4ca646328a65`, Git blob `719d82975d8628dee9907aef2b057dd649d3dfad`.

The V5 candidate was committed second, at `3082907987c1d02e0a10dffa8414d14600b7d134`:
`alpha_receipt_chain_reconciler_v5_20261028.py`, **1,523 bytes**, SHA-256 `eda09c5c82908be15385080c319bb88fdec9fccdd381414ae488fb8f73af3e55`, Git blob `4f3dc94e61a12b34141aa6f0ce178c39056818ad`.

| Scoped test | V4 baseline | V5 isolated |
|---|---:|---:|
| Six repeated/cyclic commit-ID negative fixtures rejected | 0/6 | **6/6** |
| Three valid acyclic controls accepted | 3/3 | **3/3** |
| Frozen independent subprocess oracle (16 tests) | Gap observed | **16/16 PASS** |
| Three targeted tests against a no-check mutant | N/A | **3/3 expected FAIL**, positive control PASS |
| Authenticated GitHub API origin | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Full eligible project handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

Reproduction from the existing R16 directory: `python frozen_receipt_chain_commit_acyclic_oracle_v5_20261028.py -v`. The evaluator invokes V4 and V5 as separate subprocesses, never imports V5, and checks exact failure modes and nonclaims. Local execution used Linux/Python 3.13; external third-party validation is not established. The mutant was an isolated local change (`if commit in seen` replaced by `if False`), not published.

## DECISION / SCIENTIFIC LIMITS

`TESTED_IMPROVEMENT` applies **only** to isolated synthetic commit-chain metadata. No production integration, GitHub actor authentication, independently fetched Git parent verification, real event census, external expert ACK, runtime/Hostinger/WWW change, or C2 promotion is established. Caller-supplied SHA values can still be fabricated consistently; a real API-backed proof would require separate source authentication and commit-byte readback. The evaluator is independent of candidate implementation but not externally peer-reviewed. Historical source files and evaluator contracts remain unchanged. Publication and Issue #93 append-only receipt require a separate actual main readback.
