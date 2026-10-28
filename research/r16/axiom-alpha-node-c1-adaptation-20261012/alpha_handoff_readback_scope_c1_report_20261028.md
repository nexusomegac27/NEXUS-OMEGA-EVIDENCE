# NEXUS OMEGA · Alpha-Node · readback scope guard V3 · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_READBACK_SCOPE_GUARD_20261028_R0
DECISION=PATCH_CANDIDATE_C1_ISOLATED_TESTED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=3834ef7eddf08c5b3e0cd0bb662372d8c41e29e8
PREDECESSOR_ISSUE93_RECEIPT=6467072191
SOURCE_V2=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_page_census_witness_v2_20261028.py
SOURCE_V2_BYTES=8528
SOURCE_V2_SHA256=c16806be3d00810b0e6d6ddeefc336c7428c9f6104c050c52815deb725cac8fd
SOURCE_V2_GIT_BLOB=e7882865407d2beb1b522182a86bf3351a7ef824
FROZEN_EVALUATOR_FIRST_COMMIT=acb3a62a42a7d43204814bad301438d0fdf57471
CANDIDATE_SECOND_COMMIT=8af79eeb21ab5b1d4e5a037b9736a9bb2cf153b2
PUBLICATION_MAIN_AND_RECEIPT=REQUIRE_POSTMERGE_READBACK
```

## One falsifiable change

The original V2 census accepts a synthetically complete two-page dataset with `scope.coverage=PARTIAL`, 12 observed events, and 11 caller-asserted complete public readbacks. It emits `observed_readback_sample_rate=11/11` **and** `readback_rate=11/11` despite the explicitly partial coverage. Its scoped automation rate is already `NOT_COMPUTABLE`. The second readback field can be misinterpreted as a scope-wide 100% claim.

The isolated V3 adapter imports the unchanged pinned V2 census and adds `scope_readback_rate` and `project_readback_rate`. It gates `readback_rate` and `scope_readback_rate` on `coverage=DECLARED_COMPLETE`, while preserving `observed_readback_sample_rate=11/11` for the partial sample. The project-wide rate remains `NOT_COMPUTABLE` even for a caller-declared complete synthetic scope.

## Negative hypothesis, evaluator and falsifier

- Counterhypothesis: a caller can falsely label an incomplete source `DECLARED_COMPLETE`; the adapter does **not** authenticate GitHub pagination, provenance, scope completeness or actual readback booleans.
- Frozen independent subprocess smoke evaluator committed **before** V3: 6/6 PASS on V3; original V2 lacks the new fields and fails 6/6.
- Separate local subprocess oracle: 16/16 PASS on V3; original V2 yields 1 failure and 7 errors (missing new fields and partial coverage). This larger oracle is not committed and is **not** a third-party validation.
- Local negative mutants: removing the coverage gate causes 2/16 expected failures; promoting the observed sample to a project-wide rate causes 2/16 expected failures.
- Decisive falsifier of any stronger claim: present a fabricated, internally consistent `DECLARED_COMPLETE` event set missing real GitHub events; V3 can still emit a scoped ratio. It must therefore remain caller-declared C1 only.

## Metrics and boundaries

Before: 0/1 synthetic partial-coverage negative fixtures correctly withheld from the ambiguous `readback_rate`. After: 1/1 withheld, preserving 11/11 as sample only. This is **not** a measured improvement to actual handoff automation or real project-wide readback. Real eligible denominator and authenticated source census remain unknown; `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_READBACK_RATE=NOT_COMPUTABLE`.

Exactly three additive research files in the existing R16 lane. No changes to productive Steward, original V2, existing evaluators, source objects, governance, CI, actor slots, Windows/Hostinger/WWW runtime, or claim ceiling. Owner branch/PR/CI and actual main readback are separate gates. Publication is not scientific or production integration.
