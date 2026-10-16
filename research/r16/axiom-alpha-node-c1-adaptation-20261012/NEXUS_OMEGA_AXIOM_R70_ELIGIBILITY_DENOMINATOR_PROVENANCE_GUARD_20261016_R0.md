# NEXUS OMEGA — AXIOM R70 · Eligibility denominator provenance guard

OBJECT = NEXUS_OMEGA_AXIOM_R70_ELIGIBILITY_DENOMINATOR_PROVENANCE_GUARD_20261016_R0
STATE = TESTED_ISOLATED_C1_CANDIDATE_NOT_INTEGRATED
PREDECESSOR = NEXUS_OMEGA_AXIOM_R69_REMOTE_COMPLETION_DEFAULT_DENY_20261016_R0
PREDECESSOR_ZIP_SHA256 = 7ce88fccad9fa964a85c193610aaa820a946606e67f6e68a1e8293eb496b3454
PREDECESSOR_PACKAGE_MANIFEST = 17/17_MATCH
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Observed defect and falsifier

R69 computes `known_eligible_denominator` from self-asserted local ledger booleans (`public`, `routine`, `authorized`, `accessible`), even in default `LOCAL_UNTRUSTED_REMOTE` mode. A matching local source SHA-256 and Git blob ID do not authenticate eligibility, time window or GitHub readback. A downstream dashboard could misrepresent a locally asserted count as an independently known denominator.

Falsifier: without independent eligibility-source authentication, a local all-true event MUST NOT produce a numeric `known_eligible_denominator`; synthetic fixture counts may remain visible only in separately named fields. No 30-day rate may be inferred from local flags.

## Isolated candidate

R70 preserves the R69 remote-completion default-deny and existing event decisions, but returns `known_eligible_denominator=null`, `actual_30_day_eligible_denominator=null`, `locally_asserted_eligible_count=N`, and `eligibility_source_authentication=NOT_ESTABLISHED_BY_LOCAL_REDUCER`. `synthetic_eligible_denominator=N` exists only with explicit `--synthetic-fixture-mode`. Invalid ledgers also produce no numeric known denominator. No authenticated GitHub adapter is implemented.

## Frozen black-box evaluation

FROZEN_EVALUATOR_SHA256 = e0bab98ecd42308bd8a1979e5688784f4925f734e68f204b30eeac1509407d58
CANDIDATE_SHA256 = 41f4e0dce477cddaba1e5b06c187ffe7ccfa0bd776075090fd1843866d5e53df
R69_BASELINE_NEW_CONTRACT = 0/14_PASS (13 failures, 1 error)
R70_CANDIDATE_NEW_CONTRACT = 14/14_PASS
R70_MUTANT_RESTORING_KNOWN_DENOMINATOR = 11/14_FAIL_DETECTED
R69_HISTORICAL_TESTS_ON_R70 = 2/18_PASS (16 expected schema-contract failures)

These are local synthetic black-box tests, not external scientific validation. The evaluator was frozen before implementation and was not modified. Historical output compatibility is intentionally broken; integration requires separate consumer migration review. No production pipeline, runtime, evaluator oracle or model weights were changed.

## Publication and R10 boundaries

This is a public-safe research candidate under the existing R16 research directory, not a production patch. Any branch transport, PR, CI, merge, actual main readback and Issue #93 receipt must be separately verified; no transport implies scientific acceptance. R10 PR #115 at `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` remains a public SEND without a verified independent receiver/actor/research completion in the checked PR and Issue #93. The actor allowlist on pinned main is empty. No biological experiment, Cursor dispatch, Hostinger write, new worker, auto-merge or claim promotion is authorized.

ACTUAL_30_DAY_ELIGIBLE_DENOMINATOR = UNKNOWN
ACTUAL_30_DAY_VERIFIED_AUTONOMOUS_NUMERATOR = UNKNOWN
ACTUAL_90_PERCENT_GOAL = NOT_COMPUTABLE
WWW_PARITY = NOT_ESTABLISHED
