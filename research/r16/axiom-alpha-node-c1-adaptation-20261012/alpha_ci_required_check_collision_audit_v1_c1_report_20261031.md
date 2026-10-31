# AXIOM Alpha-Node — required-check name collision audit V1 (2026-10-31)

\`\`\`text
OBJECT=NEXUS_OMEGA_ALPHA_CI_REQUIRED_CHECK_NAME_COLLISION_AUDIT_V1_20261031_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=830dfd18dc30f3a8dc878418f09faf128b1ad7e3
PREDECESSOR_MAIN=5df8953165087fabf50aba52eb15e3668f50d940
PREDECESSOR_PR=231
PREDECESSOR_ISSUE93_RECEIPT=6538543672
FROZEN_EVALUATOR_FIRST_COMMIT=90c361a01d5dd51f2b8dfeee4ecc6afcaae3aa4f
CANDIDATE_SECOND_COMMIT=46914957a88f1215a7436d5786c60c29bca4558d
NORMALIZED_SNAPSHOT_THIRD_COMMIT=f98a20b70d2f947ca43d2cfc3004e78452767181
PRODUCTION_INTEGRATION=NO
\`\`\`

## OBSERVE → ORIGINAL_BYTES / PROVENANCE

At pinned GitHub main, read AGENTS.md, GOVERNANCE.md, the R16 adaptation contract, the operator C1 research-publication directive, task-anchor norm, repository order policy, research/pipeline, the external actor registry, and Issue #93. The latest prior receipt was #6538543672, owner-authored. R10 PR #115 was OPEN; its PR discussion, reviews and review threads had no new independently authenticated expert return. The owner-controlled external actor registry remains empty.

Independently queried the **live GitHub REST API** for:
- active ruleset: https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293
- immutable PR #231 head check-runs: https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/a6a04f775d620e1e94cb1fd0ebcd16dfa4518c4d/check-runs

Ruleset ID 21252293, active for refs/heads/main, requires exactly **one named status-check context**: \`validate\`, GitHub Actions app/integration 15368. The same ruleset also contains PR, signature, linear-history, no-deletion and non-fast-forward rules. These are distinct from the single required status-check context. The classic branch-protection endpoint returned HTTP 403 through the connected GitHub App; this does not negate the independently readable active ruleset.

The PR head had **8 completed successful check runs**. Four distinct job IDs shared the same required \`validate\` name and app ID 15368. The remaining four job names (\`nexus-preentry-lab\`, \`r27e-external-structural-firewall\`, \`validate-repository-structure\`, \`semgrep-cloud-platform/scan\`) were **not named** in that ruleset's required-status-check list. This does **not** prove those four checks can be bypassed, nor how GitHub internally resolves duplicate required check names. It disproves the inference that 8/8 successful check runs means eight independently named, ruleset-required checks.

The committed \`alpha_ci_ruleset_check_snapshot_pr231_v1_20261031.json\` is a **normalized projection** of those API responses, not original API response bytes or an externally signed snapshot. Its 1,744 UTF-8 bytes have SHA-256 \`107540b22bbbe49a5536b83330d33581900adb976a7dce56a104f16d3eceaddf\` and Git blob \`8089de6a5f0c1c1491d5f609cd2f19a82519a3e6\`. Live rulesets are mutable; this observation is not a permanent statement about future enforcement.

## NEGATIVE_HYPOTHESIS → PINNED_BASELINE

H0: a green aggregate of CI check runs is insufficient to infer unambiguous required-check coverage. A required name repeated across several workflows may make provenance ambiguous; an unlisted successful check cannot be called individually required on the basis of its success.

Baseline PR #231: 8/8 green; 1 required named context; 4/8 check runs match the required \`validate\` name; 4/8 do not. Before this iteration, this particular snapshot had **0 machine-generated required-name-collision diagnostics**. The observed risk is **classification ambiguity**, not a demonstrated branch-protection bypass or unapproved merge.

## ISOLATED_CANDIDATE → INDEPENDENT_TEST

One additive, read-only Python diagnostic accepts a strictly validated ruleset/check-run projection. It reports duplicate matches to a required (name, integration_id) pair and distinguishes all-green CI from proven hard-gate coverage. It cannot edit GitHub rulesets or approve its own oracle.

- Frozen black-box evaluator, committed **before** candidate: \`frozen_alpha_ci_required_check_collision_oracle_v1_20261031.py\`; 4,279 UTF-8 bytes; SHA-256 \`21db5a4ac15470686f9287d9f4cbec790a0a5a69dbb29be8df2b8d95cdf650c0\`; Git blob \`e80c7f4ff267324ea10f6a8a150ab1351925a765\`.
- Candidate: \`alpha_ci_required_check_collision_audit_v1_20261031.py\`; 4,792 UTF-8 bytes; SHA-256 \`a1ac7c7d567d867e06e77b0177d0ebec037785593507271416c727e703902f53\`; Git blob \`af699272f8d7372afff1e8028e07116dcadf171e\`.
- Local Python \`-S\` subprocess oracle: **21/21 PASS**, including **18/18 negative fixtures FAIL_CLOSED**. The three positive controls are the real normalized collision snapshot, a unique required check, and a missing required check. Negative fixtures include inactive ruleset, wrong branch, missing/duplicate required contexts, duplicate check-run IDs, malformed states, invalid pins, wrong repository, duplicate JSON keys and nonfinite JSON.
- Real committed snapshot passed the isolated candidate: \`REQUIRED_CHECK_NAME_COLLISION_OBSERVED\`; 8/8 green; \`validate:4\`; 4 not named as required; \`hard_gate_coverage=NOT_PROVEN_BY_API_SNAPSHOT\`.

| Metric | Before | After |
| --- | ---: | ---: |
| Machine-identified duplicate required-check names for this snapshot | 0/1 | **1/1** |
| Independently frozen subprocess oracle | Not present | **21/21 PASS** |
| Negative fixtures fail closed | Not present | **18/18** |
| PR #231 observed successful check runs | 8/8 | 8/8 (unchanged) |
| GitHub ruleset / production CI changes | 0 | **0** |
| Project-wide handoff automation / publication readback rate | NOT_COMPUTABLE | **NOT_COMPUTABLE** |

**Falsifier:** the diagnostic labels the four distinct \`validate\` jobs as unambiguous, reports all eight checks as separately required, accepts an inactive/wrong-branch ruleset, accepts a duplicate job ID, or fails to accept a unique valid control. Any such result disproves the respective diagnostic claim.

## DECISION / GOVERNANCE BOUNDARY

\`TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE\`. The observed CI-name collision is a substantive **governance-quality finding**. No ruleset, workflow, branch protection, evaluator, production validator, external actor registry, model weights or runtime was changed. Changing required contexts or renaming CI jobs would require a separate scoped authorization and independent verification; it is not silently performed here.

No claim of a GitHub security exploit, branch-rule bypass, full GitHub transport authentication, scientific validity, or WWW parity. R10 remains \`PUBLIC_SEND=OBSERVED\`, \`INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED\`, \`AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED\`, \`AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED\`, \`EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED\`. The full authenticated denominator of eligible handoff attempts, including failures, is unavailable; synthetic tests are not project success counts.

Reproduce from a repository checkout:

\`\`\`sh
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_required_check_collision_oracle_v1_20261031.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_required_check_collision_audit_v1_20261031.py
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_required_check_collision_audit_v1_20261031.py < research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_check_snapshot_pr231_v1_20261031.json
\`\`\`

PR CI, actual merge/main readback, per-file bytes/hash/blob readback and Issue #93 append-only receipt are **pending** at report creation; no publication success is inferred from this text.
