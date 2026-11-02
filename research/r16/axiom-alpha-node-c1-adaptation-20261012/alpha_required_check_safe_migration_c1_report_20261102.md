# NEXUS OMEGA | AXIOM Alpha-Node | Required-check collision: source-pinned migration candidate | 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_REQUIRED_CHECK_SAFE_MIGRATION_CANDIDATE_20261102_R0
DECISION=PATCH_CANDIDATE_C1_TESTED_ISOLATED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=94ea6517cc7a9f98a53cc8c4fb5f6a3d6fd9c6f8
PREDECESSOR_PR=300
PREDECESSOR_ISSUE93_RECEIPT=6588842440
FROZEN_EVALUATOR_FIRST_COMMIT=ee2bd02a75b042153c369389397ff02f23e01f5d
CANDIDATE_SECOND_COMMIT=03d4a14b8274b796b618ca1f336943f2076850b6
WORKFLOW_MUTATION=NO
RULESET_MUTATION=NO
GITHUB_MERGE_BYPASS=NO
PRODUCTION_PROTECTION_ESTABLISHED=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The previous PR #300 / Issue #93 receipt documented a real ambiguity in active GitHub ruleset `21252293`: one required context `validate`, GitHub Actions integration `15368`, but four different successful check-runs and four different workflows at the pinned predecessor main. That earlier detection scaffold did **not** repair the required-check configuration. This run selected exactly one successor candidate: a reproducible, **read-only and non-applying migration proposal**.

Current ruleset was fetched from `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293` and showed `enforcement=active`, `refs/heads/main`, strict required checks, and only `(validate,15368)`. Four original workflow YAMLs were fetched by immutable main SHA and Git blob:

| Workflow | Original bytes | Git blob SHA-1 | Proposed job ID | Proposed bytes |
|---|---:|---|---|---:|
| `.github/workflows/validate-anchor.yml` | 1138 | `3ab2bfecc4949cf23bc9ea1eafeb65c342cf0b0e` | `validate-anchor` | 1145 |
| `.github/workflows/validate-scientific-ledger.yml` | 919 | `787cc06380be6b3981ba2ab0fd20e53cb13881b4` | `validate-scientific-ledger` | 937 |
| `.github/workflows/validate-scientific-communication.yml` | 1126 | `082979fd7531b22873f0a93a8418a5e7d5b6693a` | `validate-scientific-communication` | 1151 |
| `.github/workflows/validate-a83-framework-hardening.yml` | 2078 | `b03b029f7c168ac80ae42f3a40a3ad9481c367a7` | `validate-a83-framework-hardening` | 2102 |

Each proposed YAML differs only in the `jobs.validate` mapping key. No source YAML was edited in the repository. The target required-check set is the four distinct names above, each with integration ID `15368`. This is a **proposed future target**, not a claim that GitHub will actually expose those exact names or enforce them.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

Hypothesis: A safe migration requires (a) all four original validation bodies preserved and (b) four uniquely identifiable required contexts, not merely a successful check named `validate`. The current observed baseline is **four jobs / one repeated required context**. Proposed isolated state is **four jobs / four distinct contexts**; live GitHub remains at baseline.

Crucial counter-hypothesis: changing the four job IDs immediately while the existing ruleset still requires `validate` may strand future PRs, since the old required check would disappear. The candidate therefore **must not be directly applied**. A separately authorized staged migration should first expose and verify new unique check contexts while retaining old checks, then require all four unique checks in the ruleset, only then retire the legacy `validate` requirement and jobs. This sequence needs separate owner review, actual GitHub check-run evidence, and rollback planning. It was **NOT_EXECUTED** here; duplicating validators temporarily has cost and potential drift.

## ISOLATED CANDIDATE / FROZEN INDEPENDENT TEST

The independent evaluator `frozen_alpha_required_check_safe_migration_evaluator_v1_20261102.js` was committed **before** the candidate, at `ee2bd02a75b042153c369389397ff02f23e01f5d`. The candidate `alpha_required_check_safe_migration_candidate_v1_20261102.js` followed at `03d4a14b8274b796b618ca1f336943f2076850b6`. Neither makes network calls or changes workflows, branch rules, source objects or permissions.

The evaluator was re-fetched from the branch and executed as a separate frozen JavaScript module against the re-fetched candidate in an isolated V8 test. Result: **16/16 PASS**, including **15/15 negative fixtures** (missing/duplicate workflows, blob mismatch, missing/duplicate YAML anchor, wrong app, wrong ref, inactive ruleset, extra required check, malformed/duplicate/unapproved target, malformed input). An additional real-source test fetched all four immutable workflow YAML files and confirmed **4/4** proposed replacements differ **only** in the job ID; original and proposed byte lengths match the table. This is independent test-code separation and time-order freezing, **not** independent human scientific peer review.

Versioned source identities:
- Frozen evaluator: 4172 UTF-8 bytes; SHA-256 `190ae62a9ebb81819145a4908d5b273c0682b76f7a4857ed207d2a73c82e5de7`; Git blob `e9d9304b99ea2b702bd7f0240ff4b276b0816cc0`.
- Candidate: 2946 UTF-8 bytes; SHA-256 `7697d434cd557fddee2cc4bbf7528394e7feaf042764f0c1f1e9df519b41a386`; Git blob `b35923fdbf115452b6614b66c38c1aa1267bf616`.

Reproduce after checkout of this candidate branch:

```bash
node -e "const e=require('./research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_required_check_safe_migration_evaluator_v1_20261102.js'); const c=require('./research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_required_check_safe_migration_candidate_v1_20261102.js'); console.log(e.runTests(c.proposeRequiredCheckMigration))"
```

**Falsifiers and boundaries:** a jointly forged `sha` metadata field and altered `content` can pass the planner; it does not calculate cryptographic source hashes internally or authenticate GitHub API transport. If actual GitHub Actions check-run names differ from the proposed job IDs, the target ruleset cannot be considered validated. If any validation job is omitted from an enforced target rule, or if a migration PR becomes unmergeable, the operational plan fails. Neither scenario was experimentally tested on live branch protection. A full platform-level migration requires explicit authorization and independent post-change negative testing.

## DECISION / MEASURABLE DELTA

`PATCH_CANDIDATE_C1_TESTED_ISOLATED`: before, no concrete source-pinned four-job migration artifact was established; after, one reproducible candidate generates **4/4 minimal job-ID-only patches** and a **4/4 required-context target**, with frozen evaluator **16/16 PASS**. This is a research/preflight gain only. **Production collisions fixed: 0/4.** No actual new unattended handoff, CI ruleset repair, or scientific validation is claimed.

Project-wide 90% handoff automation: `NOT_COMPUTABLE` (eligible authenticated numerator and denominator absent). Project-wide 100% publication readback: `NOT_COMPUTABLE` (complete authenticated publication population absent). No private/local unavailable returns enter a success numerator.

## R10 PASSIVE HANDSHAKE / SEPARATE TRUST DOMAIN

PR #115 remains open, with no PR discussion/review comments returned at observation. Original immutable R10 head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` yielded detached manifest 4588 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, independently calculated SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`. The 282 Issue #93 comments read before this publication were owner-authored; no independent authenticated R10 expert receiver was observed. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`.

No new automation, worker, Cursor dispatch, R10 merge, biological experiment, GitHub ruleset/CI change, Hostinger/WWW write, secret, or C1 claim promotion.
