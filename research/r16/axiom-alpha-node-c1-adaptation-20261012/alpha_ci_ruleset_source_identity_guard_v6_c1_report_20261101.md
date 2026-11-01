# NEXUS OMEGA · AXIOM Alpha-Node · Ruleset source identity guard V6 · C1

```text
OBJECT = NEXUS_OMEGA_ALPHA_CI_RULESET_SOURCE_IDENTITY_GUARD_V6_20261101_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BASE_MAIN = 3fef33f230f5cfbec75167811d0a12787f1847db
BASE_PARENT = 3cc35487e8cae54aeac95377b6a8c376f412dc4f
FROZEN_EVALUATOR_COMMIT = 4d27e0390c306ef8b7105b7de6fbc6aa2fedff9b
CANDIDATE_FIRST_COMMIT = 69e89b9a482e89dbfd01622f30d1ec672916ef51
PRODUCTION_INTEGRATION = NO
RULESET_MUTATION = NO
EXTERNAL_ACTOR_REGISTRATION = NO
WWW_WRITE = NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Pinned GitHub `main` and the actual repository ruleset API were read separately. The active ruleset `21252293` returns `source=nexusomegac27/NEXUS-OMEGA-EVIDENCE`, `source_type=Repository`, and canonical `url=https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293`. Existing V5 checks ruleset ID, target, active enforcement, include/exclude and bypass, but ignores these three source identity fields. A foreign/missing source can therefore be accepted on synthetic input even if the rest of the object looks identical. This is a **structural source-misbinding counterexample**, not evidence that GitHub actually supplied a foreign ruleset.

Predecessor source files were retrieved at immutable main and independently reconstructed with exact Git-blob matches (not inferred from chat): V2 `5eca7f4fccabb15bdcd9980a5d54b91074933a5b` / 3948 bytes; V3 `a792dc1e81491d42fae74466a6b50edcffdc3f8a` / 2944 bytes; V4 `4806d9fbb8086b25b345ddef6452d6a6ed0d5968` / 4462 bytes; V5 `ac9b226447448c090b2fb4e7744f5a7fae090841` / 2837 bytes. All predecessors remain unchanged.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

Counter-hypothesis: V5 already rejects a ruleset whose `source`, `source_type`, or canonical ruleset URL is missing or inconsistent with the owner repository. A separately committed fixed-expectation evaluator refuted this on 12 negative fixtures: V5 accepted 12/12 malformed source identities; its expected-outcome score was **4/16**. Four valid/coverage-gap controls passed.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

V6 is an additive fail-closed wrapper around unchanged V5. It requires exact `source`, `source_type=Repository`, and canonical ruleset API URL before calling V5. A missing, foreign, null, case-drifted, whitespace-extended or wrong-type identity yields `NOT_COMPUTABLE`. The frozen evaluator was committed before the candidate (`4d27e039...` before `69e89b9a...`); the candidate did not edit the evaluator. Every fixture was run in a separate Python subprocess using byte-matched predecessor modules. V6 produced **16/16** expected outcomes, including **12/12** negative rejections and **4/4** positive/gap controls. This is independently frozen test logic, not external scientific peer review.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_ruleset_source_binding_evaluator_v6_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_effective_scope_guard_v5_20261101.py
# 4/16; exit 1 (expected baseline counterexample)
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_ruleset_source_binding_evaluator_v6_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_source_identity_guard_v6_20261101.py
# 16/16; exit 0
python scripts/validate_repository_structure.py --root .
# full repository structure check is a separate GitHub CI gate; not run in local isolated directory
```

| Additive research file (same R16 Alpha directory) | Bytes | Git blob SHA-1 | SHA-256 |
|---|---:|---|---|
| `frozen_alpha_ci_ruleset_source_binding_evaluator_v6_20261101.py` | 4011 | `fc5b44c1a63947fe0c150dcadd1ef26e2cfc82f6` | `bce18a4aa02b3c0081fa6f0b046418041e180fb908236a2d143c1bf24839f1f7` |
| `alpha_ci_ruleset_source_identity_guard_v6_20261101.py` | 2035 | `9713b07537dfd4577fa087e3c6f38231cca7490d` | `f3f4e8a740752a77046b171508c4141329e09bf258aaa4f1be8e760e0dde3564` |
| `alpha_ci_ruleset_v5_source_baseline_stdout_20261101.jsonl` | 1919 | `a89d8174d35aa7e80e96ac05f495e616fb4e0fe4` | `f9f0644a24bb94cf38df76803237b5379407cd89c15aa62c49944af9f32cf11a` |
| `alpha_ci_ruleset_v6_source_candidate_stdout_20261101.jsonl` | 1776 | `5ee0a3e92999ec33b0db5dc7d48b3de8e0c69bb0` | `b2064fd3ca470c8c41c91df9671a5e8ac1d992daebe520e70c85da501ed7b910` |

## FALSIFIER / LIMITS / DECISION

Falsifier: any of the 12 source-misbinding fixtures produces `OBSERVED_CONTEXTS_COVERED` or `GAP_OBSERVED` under V6; or one of the four valid/gap controls changes its expected status. Exact source spelling is intentionally conservative; case-insensitive repository aliases can be rejected. Structural crosschecks do **not** authenticate GitHub HTTP bytes, detect a fully forged self-consistent payload, prove live branch protection, or make a required status check enforceable. The V5 exclusion/bypass conservative limitation remains.

No actual productive CI integration, ruleset mutation, model-weight change, worker activation, Hostinger/WWW publication, Cursor dispatch, R10 expert-ACK claim, or C1 promotion. The project-wide authenticated handoff denominator and exhaustive publication-readback denominator remain unavailable: both project-wide target rates are `NOT_COMPUTABLE`; the 16 tests are synthetic, not real handoff attempts. Publication, CI, merge, main readback and append-only Issue #93 receipt must be established separately by their actual API results.
