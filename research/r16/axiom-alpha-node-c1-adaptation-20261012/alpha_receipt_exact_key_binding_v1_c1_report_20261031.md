# AXIOM Alpha-Node — exact-key Issue #93 receipt attribution · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_RECEIPT_EXACT_KEY_BINDING_V1_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 5b5ecbd1cf320e139cd0e43a64a9c9f11c857301  
PREDECESSOR_PR = 243  
PREDECESSOR_ISSUE93_RECEIPT = 6545317836  
FROZEN_ORACLE_FIRST_COMMIT = 40824fe08e902a4180885cc73044957a51a80bd9  
CANDIDATE_SECOND_COMMIT = ed54bfc31a3f6553b8b5bce166b8fd651e99c826  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Negative hypothesis and observed defect

Issue #93 receipts contain PREDECESSOR_PR before PR. An unanchored first-match PR=(digits) regex matches the suffix of PREDECESSOR_PR and assigns a receipt to its predecessor. On the real bounded 16-receipt window PR #228–243, **16/16 naive unanchored first matches were wrong**. This is a defect of the deliberately naive extraction baseline, **not** evidence that the prior curated ten-PR oracle or production systems used this regex. Counterhypothesis: exact line-anchored binding keys with aliases and expected merge-SHA checks prevent this attribution error. Falsifier: a wrong PR binding accepted as positive.

## Source-exact bounded GitHub observation

Connected GitHub API: 233 Issue #93 comments, all observed authors nexusomegac27. Exactly 16 scoped receipts for PR #228–243. PR field aliases: PR 15/16; OWNER_PR 1/16. Main aliases: ACTUAL_MAIN_READBACK 12/16, ACTUAL_MAIN 3/16, MAIN_AFTER 1/16. Independent GitHub PR metadata requests confirmed **16/16 merged PR and merge-SHA matches** against the receipt projection. Strict scoped field extraction matched **16/16** PR, predecessor, C1 ceiling and owner labels. This is bounded GitHub-origin consistency, not independent authentication, completeness of all publications or project-level throughput.

An overly strict first idea would have rejected the legitimate #234 receipt (Issue #93 comment 6540138304), which repeats the ancillary SOURCE_REPORT field with different meanings. The candidate enforces uniqueness only on binding-critical fields. Original receipts remain unchanged.

## Frozen technical evaluator, measured delta and original bytes

Frozen black-box Python subprocess oracle committed FIRST, before candidate code. Command from existing R16 research directory: python frozen_alpha_receipt_exact_key_oracle_v1_20261031.py alpha_receipt_exact_key_binding_v1_20261031.py

Actual local Python 3 result: **4/4 positive PASS; 14/14 adversarial negative FAIL_CLOSED**, exit code 0. Negative cases cover forged PR/main, duplicate IDs/PR/critical fields, forged predecessor, wrong actor label, C2, conflicting main aliases, missing/forged URL and missing actor. The oracle is technically separate but not an external third-party evaluator.

- Frozen oracle: **3,803 bytes**, SHA-256 102a9d5909195b0243855cdbd31ace41b4b934fc43e31952e88285c3d0df7972, Git blob f91e2c5bdfa9a5501735895fadd0b3854e614a04.
- Candidate: **3,619 bytes**, SHA-256 813784d62d929e5097270ba62adbe16f0d2edc0f5c94a605f97893f18cd244f3, Git blob 3118576790a72e687e5b94bf676eae60adbaaaa8.

## Limits and decision

The candidate reads caller-supplied GitHub projections. It does NOT authenticate API transport, actor identity, original source bytes, completeness of eligible handoffs or all publications. Nonbinding repeated fields are ignored and grant no authority. Additive C1 research only under the existing R16 lane; no historical overwrite, new worker, pipeline, automation, production integration, branch-rule change, Hostinger/WWW write, Cursor dispatch, R10 merge or claim promotion.

Project AUTOMATION_RATE and FULL_READBACK_RATE = NOT_COMPUTABLE: complete authenticated denominators including failures are missing. The 16/16 is only a bounded receipt/merge consistency measurement.

R10 secondary read-only: PR #115 OPEN; detached manifest at original 539d4bb33d2ba2c4895713c1bc437ece0743eeea and current dab7c59070d67e7e2a244bd6d05db9a4d37460e3 had identical 4,588-character UTF-8 content and Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df. PUBLIC_SEND observed; independent receiver ACK, authenticated external actor, scientific adjudication and executed expert research NOT_ESTABLISHED.
