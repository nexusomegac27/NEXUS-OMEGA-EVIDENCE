# AXIOM Alpha-Node R25 — C1 handoff denominator falsification candidate (2026-10-14)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R25_HANDOFF_DENOMINATOR_FALSIFICATION_20261014_R0
DECISION = TESTED_SCAFFOLD_CANDIDATE_NOT_INTEGRATED
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR = R24_UNINDEXED_EVENT_JSON_CENSUS_20261014
PREDECESSOR_ZIP_SHA256 = 86030e105f248622d86098c047009390f007c85fa0cb0363677c5ce7f11ce748
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RUNTIME_AND_MODEL = UNCHANGED
```

## New falsifiable finding

R15–R24 local transport receipts repeatedly report an undefined 0/0 *eligible* end-to-end handoff ratio, while each documents an attempted public handoff. Undefined is mathematically appropriate if preflight accessibility is unknown, but omitting attempt-stage counts conceals where the failures occurred. **Eligibility must be pinned from evidence available before the attempt**; a failed write cannot be removed retroactively from an already verified eligible denominator.

A read-only source-hash-verified census of ten physically mounted R15–R24 local receipt files gives: **10 reported public handoff attempts; 9 blocked file writes; 1 branch-content-only handoff (R19); 0 main publications; 0 preflight-proven eligible attempts; 10 unknown-preflight attempts.** The 90% eligible ratio remains **UNDEFINED_0_OVER_0**, not 0% or 100%. This is not a complete 30-day population.

The R19 branch-only case was separately checked against actual GitHub commit `cfeb0b4fd2d77ad3e129c0358e0e943070807f67`, file blob `b9f2add1d57026ea33dab039794991400798e592`; the file is absent from the pinned main. GitHub Issue #93 currently has 19 comments; last receipt `6137726458`. These are narrower live cross-checks, **not** independent attestation of all ten local receipts.

## Isolated candidate and falsifier

A stdlib-only offline stage-funnel classifier rehashes each source receipt and distinguishes attempted / blocked write / branch only / main publication / main readback / Issue receipt, plus preflight PASS/FAIL/UNKNOWN. It rejects duplicate keys, nonfinite JSON, duplicate IDs, tampered source bytes, malformed hashes and incomplete main receipts. The separate black-box evaluator was written and SHA-256 frozen **before** candidate implementation.

- Evaluator SHA-256: `063bbf52bc03d035f8541011c39293343a1d5e5f90893a0a4bf05fb9ec4c155e`.
- Candidate SHA-256: `9086eb07d0796e4630a66b082339bd22bf16ee6d6b08363cb687aca0b57de646`.
- Synthetic evaluator: **15/15 PASS** in an isolated local run; no third-party scientific acceptance.
- Prior baseline: ten receipts had no unified machine-executable funnel or preflight coverage measure. Do **not** describe the old implementation as 0/15; it did not exist.
- Source ZIP (local, not GitHub-published): SHA-256 `b0f78ee26bb77e8a5d603ca49b98b7e6ffbe741367828a4d071c593e6b09f983`; manifest 22/22 matched.

**Negative fixture:** a handoff with verified PASS preflight but a blocked write MUST remain in the eligible denominator and MUST count as unsuccessful. A private/nonroutine handoff is excluded before the attempt; unknown preflight stays unknown. Any violation falsifies the classifier.

## Boundary and decision

This is a **measurement/scaffold candidate**, not a claim of improved transfer success. Source receipt bytes and runnable evaluator are presently local, so external reproduction from this GitHub note alone is **NOT_ESTABLISHED**. No historical evaluator, production pipeline, Hostinger, Windows node, external actor registry, model weights or permissions were changed. No main publication or WWW parity is claimed without exact main/WWW readback.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
