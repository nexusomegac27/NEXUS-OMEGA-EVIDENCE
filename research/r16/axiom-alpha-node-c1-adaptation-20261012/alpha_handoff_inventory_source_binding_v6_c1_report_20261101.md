# NEXUS OMEGA · AXIOM Alpha-Node · source-byte-bound handoff inventory V6 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_INVENTORY_SOURCE_BYTES_BINDING_V6_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=b23cf96871608a18d21350f9c3df0fb075d9cec1
PREDECESSOR_PR=277
PREDECESSOR_ISSUE93_RECEIPT=6563701606
FROZEN_EVALUATOR_FIRST_COMMIT=03cfe43d60c662249cd975b6ddd55729ea4dc1c6
CANDIDATE_SECOND_COMMIT=f2b324cec0424837b7fb3686d6695b392990e991
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The original V5 inventory-consistency guard was fetched from the immutable main commit above and reconstructed locally: **2,688 bytes**, SHA-256 `dd3a3e1b4d51e71efecc6d4d770d8b15d47e642c5f7f0b90b735b5abb2f2d756`, Git blob `fa3f98e48a32a1df618c05ea6bdeeefd0ca7bd44`. Its unchanged V4 and V3 dependencies were independently matched to the original Git blobs `f78106128faf0f1af869958897fea315fa349cfc` and `b79b70e92771700afba4f5c860471da09c2775ed`. No original was modified.

## NEGATIVE_HYPOTHESIS / FALSIFIER

Hypothesis to falsify: the V5 check of `inventory.expected_attempt_ids` against `attempts` is sufficient to prevent a falsely inflated rate when both are edited together. A synthetic two-attempt source has A successful and B failed. If both the supplied inventory and the attempt list are truncated to A, V5 returns **1/1 = 100%**. This contradicts the unchanged separately pinned source's **1/2 = 50%**. It is a synthetic falsification of structural protection, not proof of any real NEXUS event omission.

Falsifier for V6: if the source bytes or the expected source digest remain unchanged, coordinated removal of B from both supplied arrays must return `NOT_COMPUTABLE`. Correct full-source cases must preserve the V5 numerator/denominator, including ineligible rows in the inventory.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

V6 adds a separate, strict base64-decoded UTF-8 JSON source snapshot with duplicate-key rejection, 1 MiB cap, SHA-256 comparison against a **separately supplied** expected digest, immutable source-commit binding, source/inventory equality and unchanged V5 arithmetic. The digest must be obtained independently by the caller; a digest supplied by the same untrusted producer is not an independent trust root.

The separate evaluator was committed first and then left unchanged. Its 15 synthetic cases were executed in local Python subprocesses against exact reconstructed V3/V4/V5 original dependencies. The candidate was committed only after the evaluator freeze.

| Fixed-oracle outcome | Original V5 | Isolated V6 |
|---|---:|---:|
| Expected outcomes | **6/15** | **15/15** |
| New source-binding negative fixtures rejected | 2/11 | **11/11** |
| Positive and regression controls | 4/4 | **4/4** |
| Coordinated inventory + attempt truncation | Incorrect 1/1 | **NOT_COMPUTABLE** |
| Real authenticated project-wide handoff rate | NOT_COMPUTABLE | NOT_COMPUTABLE |

Exact evaluator: `frozen_alpha_handoff_inventory_source_evaluator_v6_20261101.py` (4,374 bytes; SHA-256 `532bad43b49fbb4b29e558a3acdeaf524c426ca5c122c55d4e073996c76342fd`; blob `8481874a8c1dfe2ca07433b2b1040819f7914fc7`).

Candidate: `alpha_handoff_inventory_source_binding_guard_v6_20261101.py` (3,258 bytes; SHA-256 `01872e43b23e5de5989bfdf2fa07d3ca75ffb50842ebd03c6feb8f5f65a9f6e1`; blob `c8a4d93f430062bd0f7708800cf50c7a3f78035a`).

Local stdout SHA-256: V5 baseline `28a62c44ea484f357183124e2e6083406d160f1d282dc30d0f0daa635420ecb9` (exit 1); V6 `ea5cdde0cd7e00d90fd421b77aa8deb50e18713f47ff0fe4bbeb462ca2a36289` (exit 0). These stdout bytes were generated locally; they are not separately archived as GitHub source objects.

Reproduce from repository root:

```sh
cd research/r16/axiom-alpha-node-c1-adaptation-20261012
python frozen_alpha_handoff_inventory_source_evaluator_v6_20261101.py alpha_handoff_inventory_consistency_guard_v5_20261101.py
# expected 6/15; exit 1
python frozen_alpha_handoff_inventory_source_evaluator_v6_20261101.py alpha_handoff_inventory_source_binding_guard_v6_20261101.py
# expected 15/15; exit 0
```

## BOUNDARIES / DECISION

The test oracle was frozen before candidate publication, but it was authored in the same AXIOM workflow, **not independently authenticated by an external scientific reviewer**. No live GitHub event census, complete source discovery, authenticated inventory origin, project-wide 90% numerator/denominator, or productive integration is established. A producer that can change the source snapshot **and** the supposedly trusted digest can still manufacture a self-consistent 100% result. This is the explicit residual counterexample and scope limit.

No changes to model weights, runtime, branch rulesets, external actor registry, R10 experts, Cursor, Hostinger or WWW. Publication, actual main readback and Issue #93 append-only receipt are subsequent gates, not claims made by this pre-merge research report. `BLOCKED_LANE != BLOCKED_SYSTEM`; `DRIFT_RESET=NON_DESTRUCTIVE`; `C1_DESCRIPTIVE_ONLY`.
