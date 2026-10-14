# NEXUS OMEGA · AXIOM Alpha-Node R36 · truthful regression accounting · 2026-10-15

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R36_TRUTHFUL_REGRESSION_ACCOUNTING_20261015_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_ALPHA_R35_ENV_INHERITANCE_GUARD_20261014_R0
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
STATE = TESTED_ISOLATED_SCAFFOLD_CANDIDATE_NOT_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Original-byte chain and negative hypothesis

Physically accessible local R35 predecessor ZIP: **541626 bytes**, SHA-256 `4028cac8a840f3f3742f75a752bdf52b1b4f1f9178b4144605dbe1574bb240ec`; **12/12** manifest children match. Embedded R34 ZIP SHA-256 `dc05ce765cc9571818f105bccc08325640850dfd43602ba508f48f9fbb16e761`, embedded R33 ZIP SHA-256 `fe0b9b5b7182043f313aeadf8de8136994bace3f15da3996831fa882c47bcf9d`. The local ZIPs are **not claimed to be present on main**. Previous R35 branch-only report is at commit `48a95b13215a68242c87b589f180c3c8468f3f2b`; no R35 merge was observed.

**Falsifiable accounting gap:** Original R35 `tests_passed` sums all tests in fully passing suites and zero from any failing suite. Thus `34/50` can be mistaken for 16 individually failed tests when only four failed. This is a reporting ambiguity, **not** an incorrect HOLD/PASS decision.

## Single bounded R36 candidate

The isolated runner preserves the original source pin, R31/R32/R33 frozen oracle identities, environment allowlist, Python `-I`, fail-closed decisions, and no-publication flags. It changes only result accounting: `tests_passed` is an exact integer only if **all suites pass**, otherwise `null`. Two new fields distinguish `tests_verified_in_passing_suites` and `tests_in_failed_or_unverified_suites`. The latter does **not** mean individually failed tests.

- Original R35 runner SHA-256: `71321ca344229f9d7b61707fc3f3ecc880a7f45bd5389d37169aac812bc53ab6`.
- R36 candidate SHA-256: `c41ee4cd64c2b06d7c86257bf3847c366293abab1c61d58450ed58c213501ef2`.
- Separately authored R36 evaluator frozen **before** candidate modification: SHA-256 `b5b1c79063a5ad6da025c3d8c1d80fb901cd4a11be570be079070aeb9731a56f`.

## Executed independent checks

| Test | Result |
|---|---|
| Original R34 positive historical replay | **50/50 PASS** |
| Original R35 positive historical replay (previously unexecuted gap) | **50/50 PASS** |
| R36 positive historical replay | **50/50 PASS**, exact `tests_passed=50` |
| R36 negative historical replay | **HOLD_SCOPED**, `tests_passed=null`, 34 tests in passing suites, 16 in failed suite |
| Unmodified R33 evaluator on controlled nonfinite-acceptance mutation | **12/16 PASS, 4 FAIL_EXPECTED** |
| Frozen R36 accounting evaluator | **9/9 PASS** |
| Unmodified R35 environment evaluator on R36 candidate | **8/8 PASS** |

**Negative fixture:** The sole code mutation removes `parse_constant=reject_nonfinite` from a copy of the R33 target. The historical R31 and R32 suites pass; R33 fails. Original R35 reports `tests_passed=34` due to suite-granular accounting, despite the independent R33 evaluator observing only four failed cases. R36 correctly reports unknown exact count and preserves HOLD. No evaluator or historical source was rewritten.

**Falsifier:** A failing suite producing numeric exact `tests_passed`, a 50/50 positive returning `null`, or loss of any historical/environment guard.

## Scope and target denominators

The historical R25 sample contains ten receipts with ten unresolved preflight-eligibility states. The actual eligible 30-day handoff denominator is **UNKNOWN**; the 90% target is **NOT COMPUTABLE**. Isolated test results are not counted as automated public handoffs. No production/runtime/Hostinger/Node/model/permissions changes, no claim promotion, and no independently verified WWW parity. Branch publication alone is not main publication or scientific acceptance.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
