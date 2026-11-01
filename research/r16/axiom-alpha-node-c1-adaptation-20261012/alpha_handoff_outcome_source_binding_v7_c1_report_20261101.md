# NEXUS OMEGA · AXIOM Alpha-Node · V7 outcome-source binding · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_OUTCOME_SOURCE_BINDING_V7_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=265d760ce6a1e0e0bf4e526e48881d9ef55e3144
PREDECESSOR_PR=278
PREDECESSOR_ISSUE93_RECEIPT=6564141672
FROZEN_EVALUATOR_FIRST_COMMIT=37784d349388fc94076c8289eea7711155f0083a
CANDIDATE_SECOND_COMMIT=e7b808eabc8b26699ef89310c25f2ed9318f5f43
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

At pinned main, V6 `alpha_handoff_inventory_source_binding_guard_v6_20261101.py` was independently fetched and byte-reconstructed: 3,258 bytes; SHA-256 `01872e43b23e5de5989bfdf2fa07d3ca75ffb50842ebd03c6feb8f5f65a9f6e1`; Git blob `c8a4d93f430062bd0f7708800cf50c7a3f78035a`. Its immutable dependencies V5, V4 and V3 were separately reconstructed and Git-blob-matched: `fa3f98e48a32a1df618c05ea6bdeeefd0ca7bd44`, `f78106128faf0f1af869958897fea315fa349cfc`, `b79b70e92771700afba4f5c860471da09c2775ed`. No predecessor was modified.

## NEGATIVE_HYPOTHESIS / COUNTEREXAMPLE

V6 binds the **inventory** to independently supplied source bytes, but its source schema does not bind the **attempt outcome rows**. With a fixed two-attempt source A=completed and B=failed, the pinned V6 original returns **1/2 = 50%**. Changing only B's `completed` to `true`, without changing source bytes or expected SHA-256, returns **2/2 = 100%** under V6. The same issue affects `receipt_verified`, `operator_nudge`, eligibility flags and `evidence_ref`. These are synthetic adversarial fixtures, not observed real NEXUS handoff tampering.

## ISOLATED CANDIDATE / FROZEN EVALUATOR

V7 requires the exact SHA-256-pinned UTF-8 JSON source snapshot to contain `inventory`, `attempts`, `pinned_commit`, `coverage_source`. It compares the complete attempt rows and inventory against the snapshot using deterministic JSON serialization, avoiding Python `True == 1` equivalence. A mismatch fails closed as `NOT_COMPUTABLE`. V5 arithmetic, the 1 MiB source cap, strict base64, duplicate-key rejection and pinned commit check remain unchanged. The expected digest MUST come from an independent trusted caller; this tool cannot authenticate its provenance.

The separate frozen evaluator was committed first at `37784d349388fc94076c8289eea7711155f0083a`, verified against its Git blob, and was not changed when V7 was authored. Python subprocess tests used the exact reconstructed V3–V6 Git blobs and a fixed 18-case oracle.

| Fixed-oracle measure | V6 original | V7 isolated |
|---|---:|---:|
| Expected outcomes | 9/18 | **18/18 PASS** |
| Positive/regression controls | 4/4 | **4/4** |
| Negative fixtures correctly rejected | 5/14 | **14/14** |
| New false-accept classes exposed | 9 | **0/9 remaining in fixed suite** |
| Forged completion against unchanged pinned source | Incorrect 2/2 | **NOT_COMPUTABLE** |
| Actual authenticated project-wide automation | NOT_COMPUTABLE | NOT_COMPUTABLE |

Evaluator: `frozen_alpha_handoff_outcome_source_evaluator_v7_20261101.py` · 5,110 bytes · SHA-256 `65f313f51a9ec59fff7a78a0a3c3fc336eab36304ece35824b0971393a5e6393` · Git blob `e4a9398059fab812ff1f3a4f2d36d427b7c3a58c`.

Candidate: `alpha_handoff_inventory_outcome_source_binding_guard_v7_20261101.py` · 3,882 bytes · SHA-256 `417c986a185430e4db87c9762b3acb300f096cc19ee83aebc71e625fd37dffd5` · Git blob `17b78f0c95cb9c469d654e70977c82354bb960ed`.

Local evaluator stdout SHA-256: V6 `e95e37447dddaed2fe65c4342f3d6fb32cd85d44bbbda260c840ca2b085c5128`; V7 `46b441ac5e21cce2d05b8943d15e253652c552ea4453bf0a349b8aea4e0f2ab4`. Local stdout is not independently archived as a GitHub object.

Reproduce from the existing research directory:

```sh
python frozen_alpha_handoff_outcome_source_evaluator_v7_20261101.py alpha_handoff_inventory_source_binding_guard_v6_20261101.py --mode v6
# expected: 9/18; exit 1
python frozen_alpha_handoff_outcome_source_evaluator_v7_20261101.py alpha_handoff_inventory_outcome_source_binding_guard_v7_20261101.py --mode v7
# expected: 18/18; exit 0
```

## FALSIFIER / BOUNDARIES / DECISION

If an attacker changes **both** source snapshot and purported independently pinned digest, V7 may still accept a false 2/2; the evaluator's valid matching-source 2/2 fixture explicitly demonstrates this boundary. V7 does not authenticate the source producer, GitHub actor, event completeness, independent SHA-256 pin, real handoff numerator/denominator, or external expert research. A real authenticated source event census is required before any 90% target measurement. This is an append-only isolated C1 research scaffold, not a production integration, runtime/Hostinger change, branch-ruleset modification, or claim promotion.
