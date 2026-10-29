# NEXUS OMEGA — AXIOM Alpha-Node — Handoff denominator and publication-readback guard V1 — 2026-10-29

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_DENOMINATOR_GUARD_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=1208a338714c78951371fa431e13261726c6b590
PINNED_MAIN_PARENT=8b7ac2a34175f520f7fd9c1fe738cb902f0e6c41
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/189
PREDECESSOR_ISSUE93_RECEIPT=6489031228
ORACLE_FIRST_COMMIT=3f8563a255159d2cebba4a761c8b99cfb4b7bd87
CANDIDATE_SECOND_COMMIT=7c7be95911df7107c51a7c47d801a058878b796b
PRODUCTION_INTEGRATION=NO
AUTOMATIC_GITHUB_DISCOVERY=NO
WWW_PARITY=NOT_ESTABLISHED

## OBSERVE / source provenance

At pinned main, the predecessor F0 V2 research report explicitly states that project-wide 90% handoff automation and 100% publication readback are NOT_COMPUTABLE because an authenticated complete numerator/denominator, including failed attempts, is unavailable. AGENTS.md, GOVERNANCE.md, the operator direct-publication rule, Task Anchor Norm, research/pipeline/POLICY.md, external write-slot registry and Issue #93 were read at pinned main. This candidate is a bounded response to a real accounting gap, NOT a claim that an exhaustive historical handoff inventory has been discovered.

## NEGATIVE HYPOTHESIS / falsifier

A partial inventory can falsely show 100% if failed eligible handoffs are omitted, inaccessible private returns are counted as successes, or an unauthorized publication is excluded from the readback denominator. A naive eligibility-filter-first mutant omits an unauthorized publication from the readback denominator. It fails the independent frozen test that requires all declared publications to remain in that denominator.

Falsifier: a duplicate handoff ID, missing required flag, string in place of boolean, duplicate JSON key, unknown flag, missing input, or false readback flag must not yield a complete success claim. A candidate that produces a project-wide success rate from caller-declared data alone is rejected.

## PINNED BASELINE / isolated candidate / separate evaluator

- Existing project-wide measured automation rate: NOT_COMPUTABLE; project-wide published-change readback rate: NOT_COMPUTABLE. No complete, authenticated population was identified in this run. This is a source gap, not a numeric zero baseline.
- Frozen black-box evaluator committed FIRST: research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_handoff_accounting_oracle_v1_20261029.py; 4919 bytes; SHA-256 f0320314d5a2e465a236b1c2ac7043896484f3d25cd5a07926c4c36e87e99d14; Git blob 7cb54abe2b8e80f108f0ac6d118c6a3cdaa6c1b3.
- Isolated candidate committed SECOND: research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_denominator_guard_v1_20261029.py; 3343 bytes; SHA-256 0f88904c3d7c75a1b334508d7ac6aa9a66ebbacfb3813c28c077bba519616b0b; Git blob e146e4efcd7d48bf4b56c7b8e6972f8ea4e6c235.
- The evaluator launches the candidate in a separate subprocess; it does not import candidate code. Both artifacts are pure local synthetic research, not production instrumentation. The evaluator was authored within this AXIOM run and is NOT externally third-party certified.
- Executed in a local isolated Python process: python frozen_handoff_accounting_oracle_v1_20261029.py -q -> 17/17 PASS.
- Negative mutant (NOT published): moving publication counting after eligibility filtering -> 16/17 PASS, one expected failure on unauthorized publication exclusion.
- Positive synthetic example: 3 eligible handoffs, only one both automated and delivered -> declared sample automation 1/3; 3 declared publications with all four readback flags -> declared sample readback 3/3.
- Adversarial example: 2 declared publications, one unauthorized with missing receipt readback -> 1/2 declared readback, unauthorized_publications=1; no inferred project-wide zero violations.

## DECISION / limits

The improvement is a reproducible accounting safeguard: eligible handoff denominator requires accessible AND routine AND public AND authorized; automated numerator requires automated AND delivered; publication-readback denominator includes ALL declared published changes, including ineligible or unauthorized ones. The validator rejects duplicate IDs/JSON keys, missing/unknown fields, nonboolean flags and invalid JSON. Zero denominators remain NOT_COMPUTABLE. Its output always labels project-level rates NOT_COMPUTABLE and source provenance NOT_AUTHENTICATED.

Before/after test metric is a scoped mutation check (naive mutant 16/17 vs candidate 17/17), not a measured change in live automation percentage, operator interventions or repository steward runtime. Inputs are caller-declared, no GitHub API receipt authentication, no completeness attestation, no independent external evaluator and no observed live handoff reduction. A fabricated but internally coherent inventory remains a counterexample. Only a separately authenticated, complete population can establish the 90%/100% project metrics.

No modification of baseline sources, evaluator, model, production scripts, worker, external actor registry, permissions, WWW or Hostinger. No R10 expert dispatch or scientific claim promotion. BLOCKED_LANE != BLOCKED_SYSTEM.
