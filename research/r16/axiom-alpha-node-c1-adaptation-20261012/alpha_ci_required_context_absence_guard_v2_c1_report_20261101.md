# AXIOM Alpha-Node — Required CI Context Absence Guard V2 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_REQUIRED_CONTEXT_ABSENCE_GUARD_V2_20261101_R0
STATE=TESTED_ISOLATED_C1_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=63b2fd39a909eef6492344d944a5df0034f585d0
PREDECESSOR_PR=271
PREDECESSOR_ISSUE93_RECEIPT=6559691677
ORACLE_FIRST_COMMIT=8f9e7113068ce2338794082b634a8f8c2a076219
CANDIDATE_SECOND_COMMIT=e95b0f491c93e2daaacbad40df201d73cd96de5e
PRODUCTION_INTEGRATION=NO
RULESET_MUTATION=NO
```

## Observation and negative hypothesis

At pinned main, the existing read-only V1 ruleset-coverage witness only computes `observed_check_contexts - required_contexts`. It does **not** compute the reverse difference `required_contexts - observed_check_contexts`. A synthetically modified active ruleset requiring both `validate` and `semgrep`, paired with a single successful `validate` check-run, therefore incorrectly produces `OBSERVED_CONTEXTS_COVERED` even though `semgrep` is absent. The inverse-name/app fixtures also fail to identify the absent required pair.

The counter-hypothesis was that the existing V1 witness already detects absent required contexts. It is **falsified on the declared synthetic fixtures**, not on a real failed GitHub merge. Actual current ruleset #21252293 requires only `validate` (app 15368); this is a *prospective structural guard* and does not claim a new production breach.

Source references: immutable [main commit](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/63b2fd39a909eef6492344d944a5df0034f585d0), [original V1 code](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/63b2fd39a909eef6492344d944a5df0034f585d0/research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_coverage_guard_v1_20261101.py), and [read-only ruleset endpoint](https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293). The mutable ruleset is time-scoped; GitHub API payload completeness/authentication is not inferred from supplied fixture JSON.

## Single isolated candidate

V2 preserves the V1 read-only input contract and output fields, adds `absent_required_contexts` as sorted `{name,app_id}` records, and changes the decision to `GAP_OBSERVED` when any required pair is absent, any unrequired observed pair exists, or duplicate observed contexts exist. V1 is unmodified. The legacy `missing_required_names` field actually describes *observed but unrequired* contexts; V2 preserves it for compatibility rather than silently changing its meaning.

The frozen evaluator was committed first, before V2. It uses independent expected outcomes and runs both programs as separate Python subprocesses; the candidate cannot modify its oracle. No third-party or human-independent scientific validation is claimed.

| Metric | V1 | V2 |
|---|---:|---:|
| Frozen expected outcomes | 9/12 | **12/12 PASS** |
| New absent-required negative fixtures correctly resolved | 0/3 | **3/3** |
| Existing positives/regressions correctly resolved | 9/9 | **9/9** |
| Authenticated production API E2E | NOT_EXECUTED | NOT_EXECUTED |
| Ruleset or workflow configuration changed | NO | NO |

**Falsifier:** If a required `(name, app_id)` pair is absent from a nonempty otherwise valid normalized inventory yet V2 emits `OBSERVED_CONTEXTS_COVERED`, the repair fails. If a complete matching unique positive inventory emits a gap, the repair also fails. Future authentic GitHub API replay must additionally validate completeness of the check-run inventory and its source provenance.

## Exact original-byte bindings

| Object | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| Pinned V1 original | 3727 | `0ec91a70ed9e4091e6261cab9bc2c91a8457722669d51ccc81a4733609fdf26a` | `8562bdbb51d7b09f3850050a718c0cfc67f89756` |
| Frozen evaluator (first commit) | 4722 | `3a22f823306ac8cbe9718150d7577e00a2d4d25a48152750cbf84d871e464b50` | `87acdbc364e3f37f75dc3aee5b20bddb29d1920d` |
| V2 candidate | 3948 | `0eeaf689ea0ef956d3f1bc7ee8ed0307b51b4d8d99b112abd2f5e52d060b216d` | `5eca7f4fccabb15bdcd9980a5d54b91074933a5b` |
| V1 evaluator stdout | 1668 | `68161121efd6dd8be02cf5aa1f882ef956aec4fd4c57a6186798acffb9de897f` | `d38babeb02487ec74281fd8b0de487ec038ab21f` |
| V2 evaluator stdout | 1698 | `b8bdf16d1f0727151ed85d8acce8847581cd28fa37088da6e8de31288d22f41a` | `6cafa2327b74ae05dbb544c9622c7d0c84f33219` |

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_required_absence_evaluator_v2_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_coverage_guard_v1_20261101.py
# expected exit 1; 9/12 (deliberate negative baseline)
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_required_absence_evaluator_v2_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_required_absence_guard_v2_20261101.py
# expected exit 0; 12/12
python scripts/validate_repository_structure.py --root .
```

## Scope and limits

One candidate, four new files plus this report, all in the pre-existing R16 research path. No historical overwrite, new root, new worker, secret, private source, Cursor dispatch, Hostinger/WWW write, external actor registration, GitHub ruleset change, evaluator self-approval, biological experiment, or claim promotion. The 90% handoff automation and 100% project-wide publication-readback targets remain **NOT_COMPUTABLE** without a complete authenticated denominator. The per-iteration publication-readback rate can be reported only after actual PR merge, main readback and append-only Issue #93 receipt. R10 PR #115 remains a separate passive read-only observation lane.
