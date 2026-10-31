# AXIOM Alpha-Node — static required-context workflow census V1 (2026-10-31)

OBJECT = NEXUS_OMEGA_ALPHA_CI_STATIC_REQUIRED_CONTEXT_WORKFLOW_CENSUS_V1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9
PREDECESSOR_PR = 232
PREDECESSOR_ISSUE93_RECEIPT = 6539206004
FROZEN_ORACLE_FIRST_COMMIT = 02dd68ee4d892135fd61d51d1e225947c5ecf77a
CANDIDATE_SECOND_COMMIT = 61d94828574093bba4ab65f394fd51d27e9c954d
INVENTORY_THIRD_COMMIT = 096173abae691315bdba3d3dc737c7d7abc0a17b
PRODUCTION_INTEGRATION = NO

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read pinned main, AGENTS.md, GOVERNANCE.md, docs/AI_CONTEXT.md, docs/agent-protocol.md, repository structure/order, R16 adaptation contract, operator C1 publication rule, task-anchor norm, external actor registry, and research/pipeline directory. Issue #93 contained 222 comments, all owner-authored; latest prior receipt #6539206004. R10 PR #115 remained OPEN without independently authenticated expert receipt. External actor allowlist was empty.

Predecessor PR #232 established an API snapshot of **4 distinct successful check-runs named validate among 8 total**. The active ruleset 21252293 requires one status context validate with GitHub Actions integration 15368. That predecessor did not inventory all workflow source definitions.

This iteration fetched the GitHub directory listing and **all 17 actual workflow YAML source contents** on immutable main b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9, recording GitHub-reported blob SHA-1 values and extracting top-level jobs keys. The resulting JSON is a **normalized projection**, not the 17 original YAML files and not an independently authenticated GitHub witness.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

H0: The four validate check-runs observed for PR #231 are only a triggered subset of a larger static naming collision; four green jobs do not imply only four workflow definitions share the name. A complete source census can falsify this.

Baseline: PR #232's runtime snapshot covers 8 check-runs, 4 named validate; **0 of 17** workflow definitions were inventoried in a static source census. This is a coverage comparison, not a claim that the predecessor tried and failed to parse YAML.

Pinned static census: **17/17** workflow files inspected; **12/17** contain a top-level job ID validate (12 matching definitions, 18 total job definitions). These are potential same-named check sources, not 12 simultaneously executed jobs or 12 independently required checks. Workflow events and path filters can prevent execution. The four observed runtime jobs and twelve static definitions have different denominators.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The read-only Python validator rejects malformed or ambiguous normalized inventories and counts duplicate required-context job names. All files are additive research. No workflow, ruleset, CI requirement, registry, external slot, runtime or production validator changed.

- Frozen subprocess oracle: frozen_alpha_ci_static_required_context_oracle_v1.py, **3,492 bytes**, SHA-256 6e0efd5de278e997448bfc1fe9a65416b9cc550fcdc7b72d2abb24862c7548e5, Git blob 1133968fe518a50eee4b6a742a4444144eee56d8. Committed first at 02dd68ee4d892135fd61d51d1e225947c5ecf77a.
- Candidate: alpha_ci_static_required_context_audit_v1.py, **3,097 bytes**, SHA-256 fae58d67c8dad8ba47ed0462d153220a4ad54bb340520be508e6f743e009e527, Git blob 411cbd3275ca4269a08f97b2b3d049b072ac0546.
- Projection: alpha_ci_workflow_static_inventory_v1.json, **3,473 bytes**, SHA-256 9cecb89515d8f081161e53b3d083927cd1ca451338c0ccd6a808ec0c7444c60c, Git blob 66a330dddee79726c2384421ec2ac940a53f1225.
- Local independent Python -S subprocess oracle: **15/15 PASS**, including **12/12 negative controls FAIL_CLOSED** (foreign repository, mutable commit, duplicate path, invalid blob, empty/duplicate/nonstring jobs, path escape, empty inventory, invalid context, extra field, duplicate JSON keys). Three positive controls: pinned 12-match inventory, unique context, absent context.

Reproduction, from the directory containing these files:

    python -S frozen_alpha_ci_static_required_context_oracle_v1.py alpha_ci_static_required_context_audit_v1.py alpha_ci_workflow_static_inventory_v1.json
    python -S alpha_ci_static_required_context_audit_v1.py alpha_ci_workflow_static_inventory_v1.json

| Metric | Predecessor | New isolated candidate |
| --- | ---: | ---: |
| Pinned workflow definitions inventoried | 0/17 | **17/17** |
| Static definitions named validate identified | NOT_EVALUATED | **12/17** |
| Runtime PR231 jobs named validate | 4/8 | 4/8 (unchanged) |
| Independent subprocess oracle | NOT_PRESENT | **15/15 PASS** |
| Negative controls rejected | NOT_PRESENT | **12/12** |
| Production workflow/ruleset changes | 0 | **0** |

**Falsifier:** If any pinned workflow has a different top-level job ID than its projection, the pinned tree lacks a listed path/blob, the candidate misses a duplicate, or it accepts a negative fixture, the relevant claim is false. The candidate checks schema and supplied blob-ID syntax, **not** raw YAML byte-to-blob cryptography, source-to-JSON semantic fidelity, YAML parser equivalence, or live GitHub enforcement. The projection was manually cross-checked against fetched source text; a separate full raw-byte/YAML-parser audit remains NOT_EXECUTED.

## DECISION / LIMITS

TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH. New source-scope observation and falsifiable static inventory diagnostic. No branch-protection bypass, automatic enforcement failure, scientific truth, production integration or WWW parity established. GitHub CI, PR merge, actual main readback and Issue #93 receipt require separate verification after publication.

Project-wide handoff automation and publication readback rates remain NOT_COMPUTABLE: authenticated denominators including failures are unavailable. This static workflow count is not the Handoff denominator. R10: PUBLIC_SEND observed; INDEPENDENT_RECEIVER_ACK, AUTHENTICATED_EXTERNAL_ACTOR, AXIOM_SCIENTIFIC_ADJUDICATION and EXPERT_RESEARCH_ACTUALLY_EXECUTED not established.
