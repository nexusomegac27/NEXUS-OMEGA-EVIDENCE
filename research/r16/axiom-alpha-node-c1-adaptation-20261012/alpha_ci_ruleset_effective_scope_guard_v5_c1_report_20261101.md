# NEXUS OMEGA · AXIOM Alpha-Node · Ruleset effective-scope guard V5 · C1

```text
OBJECT = NEXUS_OMEGA_ALPHA_CI_RULESET_EFFECTIVE_SCOPE_GUARD_V5_20261101_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BASE_MAIN = 3cc35487e8cae54aeac95377b6a8c376f412dc4f
BASE_PARENT = 964fe47c4bdbad599e0689b132ff73c0822f3518
FROZEN_EVALUATOR_COMMIT = cc2f7592d16665e2549ee2fbf5e3fd1a5f9ec312
CANDIDATE_COMMIT = d2d541d76ed3a4250670bdf4308ba2c8d80b1682
PRODUCTION_INTEGRATION = NO
RULESET_MUTATION = NO
WWW_WRITE = NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The predecessor V4 REST-shaped adapter checked that `refs/heads/main` was *present* in the ruleset `include` field but did not validate the field's JSON type, `exclude`, or `bypass_actors`. Its inherited V2 check also used membership without validating the type. Thus a ruleset-shaped payload with main excluded or a bypass principal could be classified `OBSERVED_CONTEXTS_COVERED`. This is a **structural false acceptance on synthetic input**, not proof of an actual bypass of GitHub rules.

Original immutable main `3cc35487e8cae54aeac95377b6a8c376f412dc4f`, immediate parent `964fe47c4bdbad599e0689b132ff73c0822f3518`. Source files were independently retrieved and locally reconstructed byte-identically, verified by `git hash-object` against GitHub blob IDs:

| Pinned predecessor | Bytes | Git blob SHA-1 | SHA-256 |
|---|---:|---|---|
| `alpha_ci_ruleset_required_absence_guard_v2_20261101.py` | 3948 | `5eca7f4fccabb15bdcd9980a5d54b91074933a5b` | `0eeaf689ea0ef956d3f1bc7ee8ed0307b51b4d8d99b112abd2f5e52d060b216d` |
| `alpha_ci_checkrun_inventory_completeness_guard_v3_20261101.py` | 2944 | `a792dc1e81491d42fae74466a6b50edcffdc3f8a` | `5e63313d88feb181b5255309b6d7b51065e84700a59c72585aa1621225b60422` |
| `alpha_ci_github_rest_native_adapter_v4_20261101.py` | 4462 | `4806d9fbb8086b25b345ddef6452d6a6ed0d5968` | `17e81cb944bd0a79fc616e5bbb4ad79962190d2b800a96d79b9a3590221dacd3` |

Read-only GitHub ruleset API on 2026-11-01 reported active ruleset `21252293` with `include=["refs/heads/main"]`, `exclude=[]`, `bypass_actors=[]`, and only required status context `validate` / integration `15368`. These API fields were **not archived as independently hashed HTTP response bytes**. The real ruleset was not observed to contain the synthetic negative configurations.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

Counter-hypothesis: V4 already fails closed on an excluded branch, a bypass actor, missing fields, or non-list `include`. The separate fixed-expectation evaluator refutes this on its bounded matrix: V4 yielded **4/17 expected outcomes**, with **13/13 new negative fixtures falsely accepted**. The four valid/gap controls remained correct.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

V5 is a small additive wrapper that imports V4 unchanged and rejects type-ambiguous/duplicate `include`, any nonempty or missing `exclude`, and any nonempty or missing `bypass_actors`. A nonempty `exclude` for an unrelated branch is intentionally rejected because this bounded profile has no independently verified GitHub pattern matcher; this is conservative, not a general semantic verdict about all valid GitHub rulesets.

The evaluator was committed **before** the V5 candidate (`cc2f7592...` precedes `d2d541d7...`); the candidate did not edit the evaluator. Each fixture is executed in a separate Python subprocess. Local observed result: V4 **4/17**, V5 **17/17**, with **13/13 negative fixtures rejected** and **4/4 positive/gap controls preserved**. This is a separately frozen evaluator, **not an external independent scientific review**.

Reproduce from the repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_ruleset_effective_scope_evaluator_v5_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_github_rest_native_adapter_v4_20261101.py
# expected 4/17, exit 1
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_ruleset_effective_scope_evaluator_v5_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_effective_scope_guard_v5_20261101.py
# expected 17/17, exit 0
python scripts/validate_repository_structure.py --root .
# full-repository execution not performed locally; inspect GitHub CI separately
```

| Published research object | Bytes | Git blob SHA-1 | SHA-256 |
|---|---:|---|---|
| `frozen_alpha_ci_ruleset_effective_scope_evaluator_v5_20261101.py` | 4695 | `6676e61a812e27f67b1bd1699319eaadbf220dc7` | `b8e282e8a11083bd5245c0775b962c7f98e5be0d3df6376b1ce6c7b513924ff8` |
| `alpha_ci_ruleset_effective_scope_guard_v5_20261101.py` | 2837 | `ac9b226447448c090b2fb4e7744f5a7fae090841` | `afd7e905e95f41a48fbbaf577584acabb35e90fd36491b24be9e094ba016de35` |
| `alpha_ci_ruleset_v4_baseline_eval_stdout_20261101.jsonl` | 2056 | `22cddca61851c4bdd468e240cbdcd2016e9b96e9` | `c8c7b31a5cbe254a4c6b2fa0d780d5f9d83084091f71303afbf104119b1999b1` |
| `alpha_ci_ruleset_v5_candidate_eval_stdout_20261101.jsonl` | 1901 | `e00f420019281d2a9689788c280df43c115a813c` | `0c71eda936458878d342556df502322eaec415ad01e6c55c57094db744f1b99a` |

## FALSIFIER / DECISION / LIMITS

Falsifier: any of the thirteen malformed/ambiguous ruleset fixtures yields a result other than `NOT_COMPUTABLE`, or any of the four positive/gap controls changes its expected status. Additional counterexample: a legitimately excluded *unrelated* ref that is provably safe for main will still be rejected by V5; this is an acknowledged scope/availability cost, not a correctness claim.

V5 does not fetch or authenticate HTTP, verify GitHub `Link` headers, interpret arbitrary GitHub ref-pattern semantics, attest current branch protection, authenticate external experts, or alter CI/rulesets. Structural output does not establish actual enforcement or a security incident. No GPT self-modification, production integration, new worker, Hostinger/WWW mutation, external actor registration, biological experiment, or C1 promotion.

Project-wide Handoff automation rate and complete-publication-readback rate are `NOT_COMPUTABLE` without exhaustive authenticated attempt/publication denominators; local/private inaccessible returns are not successes. One isolated C1 candidate only. Actual PR CI, main merge and append-only Issue #93 receipt require separate physical verification; do not infer them from this report.
