# AXIOM Alpha-Node - historical CI check-run name/app binding guard V2 - C1 - 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_NAME_APP_BINDING_GUARD_V2_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=763597cc6af4f9ff4be2faea8402b678636716f7
PREDECESSOR_PR=258
PREDECESSOR_ISSUE93_RECEIPT=6554395734
FROZEN_EVALUATOR_FIRST_COMMIT=ae55dfc440ccbd41822fb96921c42272e0d8ffd6
CANDIDATE_SECOND_COMMIT=41b76fe029eab741682954c7939df0c3ac63411b
STDOUT_THIRD_COMMIT=fe6da5a7a1f84808d898b0c3e2129c024e7041c3
NEW_PIPELINE=NO
PRODUCTION_INTEGRATION=NO
```

## Observation, original sources and counterhypothesis

The previously published V1 CI identity guard checks eight successful check runs per historical PR, unique positive numeric IDs, PR-head binding, completion and nonblank names/app slugs. It does **not** bind the actual run-name/app multiset to the historical inventory: a successful unrelated check can replace Semgrep, the structure validator, preentry or the external firewall and V1 still accepts. This is a structural false-acceptance class, not a claim of actual GitHub CI compromise.

Pinned originals on the preceding main:
- `alpha_publication_census_matrix_guard_v2_20261101.py`: 2754 bytes, SHA-256 `12bc7cb28030635fe5d07a2f54e6a17a7e86c5c5f2881ed3f1cc12fc704d9e90`, Git blob `5850473cdddb4ce8d0a32035fc9ff7e453d28132`.
- `alpha_publication_ci_run_identity_guard_v1_20261101.py`: 2410 bytes, SHA-256 `65ef7e3773a13b21abb20c7912b81587b151d49e35969be6f7a94653742e8c51`, Git blob `aa4408dc7b34f43328a6dcbe64c953aefc6d7beb`.
- `alpha_ci_real_api_metadata_hybrid_fixture_v1_20261101.json`: 22296 bytes, SHA-256 `76a5d9093e6b1e0e3174912b641c144885fcf4761bba888517018172e0a830e9`, Git blob `8e80b650700d4251e9ba6e5f226461292e00c40d`. This fixture has observed GitHub check-run metadata but synthetic non-CI success placeholders; original REST bodies were not archived.

An independent field inventory of that pinned fixture found the same name/app multiset in 7/7 PRs: four `validate/github-actions`, and one each `nexus-preentry-lab/github-actions`, `r27e-external-structural-firewall/github-actions`, `validate-repository-structure/github-actions`, `semgrep-cloud-platform/scan/semgrep-code-nexusomegac27`.

Counterhypothesis: strict multiset binding will reject legitimate repeated `validate` checks or order permutations, or still accept a missing/misidentified required check. Falsifier: reject either positive control, accept any of the ten negative mutations, or fail to reproduce the baseline V1 false acceptance.

## Frozen independent test and observed delta

The independent subprocess evaluator was committed **before** the V2 candidate. Local Python 3 executed the unchanged, source-rehashed V1 baseline and isolated V2 candidate in separate subprocesses. Its complete stdout is preserved as a fourth additive source file alongside this report.

| Test | V1 baseline | V2 candidate |
|---|---:|---:|
| Two positive inventories accepted | 2/2 | 2/2 |
| Ten targeted name/app negative fixtures rejected | 0/10 | 10/10 |
| Desired security outcomes (2 positive + 10 negative) | 2/12 | 12/12 |

Mutations: substitute an unrelated successful check for Semgrep, preentry, firewall, structure or validate; change Semgrep/validate/preentry app; change Semgrep name case; duplicate validate in place of Semgrep. Every negative retains valid unique IDs, matching heads, eight completed successes and the other synthetic positive matrix fields.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_name_app_binding_evaluator_v1_20261101.py
```

Local evaluator stdout: 1509 bytes; SHA-256 `9e5b015e5a21db4c880b02d983a039b1cc784a6c073f9f2a08cd048eb4cc3521`; 12/12 expected results. The evaluator source is 3920 bytes, SHA-256 `1143c391d66825fdf5561ce17e042aa96932a0385732d6148427e04ab71fc2f7`. The V2 candidate is 1869 bytes, SHA-256 `bf92523f502b5ca2039696e8b0cef2d5d4841a18fb41655691ddd22eb0a47b8f`.

## Limits and publication gate

This guard is **only for the frozen seven-PR cohort** (#245, #247-#252), not a general required-check policy. It does not fetch GitHub, authenticate actors or apps, verify run signatures, enforce branch rules, prove source-file hashes, or independently validate scientific claims. Name/app strings in an untrusted JSON fixture remain forgeable. Future CI configurations may legitimately differ and require a separately frozen baseline. No original file, evaluator, workflow, ruleset, write-slot registry or productive runtime was modified.

The improvement is a tested synthetic structural false-acceptance reduction, not a measured production failure-rate reduction. CI success, actual merge/main readback, exact published-file SHA-256 and Git blob checks, and the append-only Issue #93 receipt must be documented separately after publication. No GitHub-to-WWW parity, R10 expert ACK, node reset, Hostinger write or claim promotion is inferred.

`AUTOMATION_RATE_PROJECT=NOT_COMPUTABLE_DENOMINATOR_MISSING`
`PROJECT_PUBLICATION_FULL_READBACK_RATE=NOT_COMPUTABLE_DENOMINATOR_MISSING`
