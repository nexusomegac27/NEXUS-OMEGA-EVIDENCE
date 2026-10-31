# AXIOM Alpha-Node — PR-scoped CI path-filter eligibility audit V1 (2026-10-31)

OBJECT = NEXUS_OMEGA_ALPHA_CI_PR_PATH_FILTER_ELIGIBILITY_V1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 56c383b6675d47b61d1b35bb543d24a2d36de512
PREDECESSOR_PR = 233
PREDECESSOR_ISSUE93_RECEIPT = 6539717530
PREDECESSOR_REPORT = research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_static_required_context_audit_v1_c1_report_20261031.md
FROZEN_ORACLE_FIRST_COMMIT = eb4406362a2ab89560c987a36ee7e856cad0dd95
CANDIDATE_SECOND_COMMIT = 567a6203ffa292ef61ff78a85de4295271f3556b
RUNTIME_INTEGRATION = NO
RULESET_MODIFICATION = NO

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The active main branch was read as immutable commit 56c383b6675d47b61d1b35bb543d24a2d36de512. Governing files AGENTS.md, GOVERNANCE.md, the R16 adaptation contract, operator direct C1 publication rule, task-anchor norm, repository order/structure, and external actor registry were read. Issue #93 contained 223 owner-authored comments; the latest predecessor receipt was 6539717530. R10 PR #115 was OPEN with no independently authenticated expert receipt.

The predecessor's immutable workflow inventory covers 17 GitHub Actions YAML files, 12 definitions with effective job name validate, and 18 job IDs total. Source workflow commit: b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9. Inventory commit: 56c383b6675d47b61d1b35bb543d24a2d36de512; inventory Git blob: 66a330dddee79726c2384421ec2ac940a53f1225. This iteration fetched all 17 actual YAML contents at the pinned source commit and checked each GitHub-reported blob SHA-1 against the predecessor inventory: 17/17 MATCH. The new JSON projection records original path, reported Git blob, byte length, parsed job IDs/effective names, pull_request trigger and paths filters.

The concrete runtime comparison is PR #231, head a6a04f775d620e1e94cb1fd0ebcd16dfa4518c4d, whose three actual changed paths all reside in research/r16/axiom-alpha-node-c1-adaptation-20261012/. Its GitHub API check-runs contain eight completed successes, four named validate. GitHub ruleset 21252293 requires context validate; this is an ambiguity inventory, not a branch-protection exploit.

## NEGATIVE HYPOTHESIS / BASELINE

H0: All twelve statically identified validate job definitions are simultaneously eligible for this R16-only pull request. The previous static census did not evaluate pull_request path filters, so 12/17 is a repository-wide potential-source count, not a PR-specific denominator.

Falsification on the pinned PR: exactly four validate definitions have unfiltered pull_request triggers, and eight other validate definitions have paths filters that do not match any of PR #231's three changed files. Thus 4/12 are statically eligible, 8/12 statically excluded. The independently fetched GitHub runtime snapshot also reports four validate check-runs among eight total checks. Matching counts do not prove GitHub's internal required-check enforcement semantics or the precise workflow-to-check-run mapping.

## ISOLATED CANDIDATE / INDEPENDENT TEST

- Frozen independent Node.js black-box subprocess evaluator, committed BEFORE the candidate: frozen_alpha_ci_pr_path_filter_oracle_v1_20261031.js, 3392 bytes, SHA-256 e7c981d85756345f698b08c74816cdba52369867fb34b5d828891441fd519a2d, Git blob 57f192dd62b26ca912c568cf6826fdeb0e770bb7. Local separate-process result: 20/20 PASS, including 16 negative/invalid fixtures FAIL_CLOSED.
- Isolated candidate: alpha_ci_pr_path_filter_audit_v1_20261031.js, 3615 bytes, SHA-256 0cc5a0d332cfc524582da4a64525a9fecd5df8434756e3a8b4a1bf4cd952e645, Git blob 7d0614759d472cb980809fbbce618556fb02531f.
- Source-derived projection: alpha_ci_pr_path_filter_projection_v1_20261031.json, 8685 bytes, SHA-256 9aad5e271db570dc13b5ad2e7d8a3fbd9bc3db4de2e4b13b96390614dbf2c0fd, Git blob 5da248602def62f7d34c926ccc21bf59ec944bcb.
- The actual pinned projection was also evaluated using the exact candidate source fetched back from the branch in an isolated JavaScript evaluation: PASS, 17 workflows, 12 validate definitions, four eligible, eight excluded. The complete actual projection was NOT executed by the separate Node.js subprocess oracle; the oracle instead used independently specified positive and adversarial synthetic fixtures.

Reproduce in this existing research directory:

    node frozen_alpha_ci_pr_path_filter_oracle_v1_20261031.js alpha_ci_pr_path_filter_audit_v1_20261031.js
    node alpha_ci_pr_path_filter_audit_v1_20261031.js < alpha_ci_pr_path_filter_projection_v1_20261031.json

| Metric | Prior static census | PR-specific candidate |
| --- | ---: | ---: |
| Workflow sources inventoried | 17/17 | 17/17 |
| Static validate definitions | 12 | 12 |
| PR #231 statically eligible validate definitions | NOT_EVALUATED | 4/12 |
| PR #231 excluded by paths filters | NOT_EVALUATED | 8/12 |
| Observed runtime validate checks | 4/8 | 4/8 (unchanged) |
| Frozen separate-process oracle | NOT_PRESENT | 20/20 PASS |
| Negative/invalid fixtures | NOT_PRESENT | 16/16 FAIL_CLOSED |
| Productive workflow, ruleset or runtime mutations | 0 | 0 |

Falsifier: any original pinned YAML trigger/job name or blob diverging from the projection; any PR #231 changed path matching an excluded workflow's path filter; an independent evaluator returning different eligibility for the specified fixtures; or an API snapshot showing different completed check names at the pinned PR head. A different PR with research/fundus changes can legitimately activate more than four validate definitions. The classifier deliberately supports only literal paths and prefix/** filters for relevant validate jobs, rejecting unsupported patterns. It is not a general GitHub minimatch/YAML parser, GitHub trust-root authenticator or required-check bypass tester.

## DECISION / BOUNDARIES

This is a source-bound, isolated, falsifiable quality improvement in diagnostic specificity, not a security repair or productive integration. The static 12 count remains correct for the entire repository; the 4 count is specific to PR #231. Full independent YAML-parser equivalence, independent cryptographic rehash of every original YAML source, actual Node subprocess replay of the full 8685-byte projection, and adversarial GitHub merge-policy testing are NOT_EXECUTED. No branch protection, workflow, external actor registration, Hostinger, WWW, node runtime or scientific claim was changed.

Project-wide handoff automation and publication readback rates remain NOT_COMPUTABLE without complete authenticated denominators including failed eligible attempts. This PR-specific 4/12 is not a Handoff denominator. R10 PUBLIC_SEND is observed; INDEPENDENT_RECEIVER_ACK, AUTHENTICATED_EXTERNAL_ACTOR, AXIOM_SCIENTIFIC_ADJUDICATION and EXPERT_RESEARCH_ACTUALLY_EXECUTED remain NOT_ESTABLISHED. GitHub PR merge, actual main readback and append-only Issue #93 receipt are separate post-publication gates.
