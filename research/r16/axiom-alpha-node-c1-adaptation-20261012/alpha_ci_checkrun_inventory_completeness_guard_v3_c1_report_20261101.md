# AXIOM Alpha-Node — Check-run Inventory Completeness Guard V3 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_CHECKRUN_INVENTORY_COMPLETENESS_GUARD_V3_20261101_R0
DECISION=TESTED_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=97c30b3b3eab5881c8b77970c1d3d6787b5104e9
PREDECESSOR_PR=272
PREDECESSOR_ISSUE93_RECEIPT=6560315145
FROZEN_EVALUATOR_FIRST_COMMIT=7fde2a50c2ad84e3e5e4129a7706bebae270ad83
CANDIDATE_SECOND_COMMIT=6bb6a47633e7fb31f2a5b7af2a0c21f8d3775897
PRODUCTION_INTEGRATION=NO
GITHUB_RULESET_MUTATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read from immutable main `97c30b3b3eab5881c8b77970c1d3d6787b5104e9`: the unchanged V2 read-only required-context guard validates each supplied check run but has no check-run inventory count, pagination, or page-ID reconciliation. A supplied proper subset can therefore yield `OBSERVED_CONTEXTS_COVERED`. The previous V2 report explicitly marked inventory completeness as not proven. The V2 source is 3,948 UTF-8 bytes, SHA-256 `0eeaf689ea0ef956d3f1bc7ee8ed0307b51b4d8d99b112abd2f5e52d060b216d`, Git blob `5eca7f4fccabb15bdcd9980a5d54b91074933a5b`.

This is a structural source-completeness issue, **not** evidence that GitHub actually omitted a check run, that GitHub API data was forged, or that any required check was bypassed. No full raw REST response body is archived in this candidate.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

Counter-hypothesis: V2 already rejects incomplete or mismatched pagination metadata. Falsified on 12 newly targeted synthetic negative fixtures; V2 ignores the additional `inventory` envelope and accepts their valid check-run subset. The independent evaluator was committed first and runs both programs as separate Python subprocesses. It uses fixed expected statuses, not the candidate's own oracle.

| Metric | V2 original | V3 candidate |
|---|---:|---:|
| Frozen expected outcomes | 4/16 | **16/16** |
| New malformed/incomplete inventory fixtures rejected | 0/12 | **12/12** |
| Existing positive and regression controls | 4/4 | **4/4** |
| Real authenticated REST pagination E2E | NOT_EXECUTED | NOT_EXECUTED |
| Productive CI/Ruleset enforcement | UNCHANGED | UNCHANGED |

## ISOLATED_CANDIDATE / FALSIFIER

V3 is a new additive Python wrapper that imports V2 unchanged. Before delegating to V2, it requires an explicit `inventory` object: source API label, identical head SHA, integer `total_count`, page size 1–100, positive page count, exact per-page ordered run IDs, consistent page sizes and count, `next_page=null`, and `complete=true`. Incomplete, malformed, mismatched or unprovided inventory yields `NOT_COMPUTABLE`, never a positive coverage claim.

**Falsifier:** supply a snapshot with `total_count` larger than the actual check-run list, or with a non-null `next_page`; if V3 returns `OBSERVED_CONTEXTS_COVERED`, the candidate is disproven. A complete matching inventory must remain accepted. The 16-case frozen evaluator checks both.

**Epistemic limitation:** The metadata envelope is caller supplied, **not authenticated**. Even a structurally complete envelope can be dishonest, omit entire events with a forged `total_count`, or represent a stale ruleset. This scaffold does not fetch GitHub REST, verify HTTP Link headers, establish complete historical CI provenance, or change merge gates. Its positive result is structural only.

## INDEPENDENT_TEST / REPRODUCIBILITY

From the repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_inventory_completeness_evaluator_v3_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_ruleset_required_absence_guard_v2_20261101.py
# expected exit 1; 4/16
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_inventory_completeness_evaluator_v3_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_checkrun_inventory_completeness_guard_v3_20261101.py
# expected exit 0; 16/16
python scripts/validate_repository_structure.py --root .
```

The isolated Python subprocess replay was executed locally; the repository-wide structure command was **not** executed locally against the full repository. GitHub CI must be checked independently before publication.

| Source / output | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| Frozen evaluator | 4065 | `75ee823a84a16641aea5797e3828b6a1b4808163fa3e77638c0af29499b51a6b` | `cc410be862adba3bd1331eef702bb59a17460a62` |
| V3 candidate | 2944 | `5e63313d88feb181b5255309b6d7b51065e84700a59c72585aa1621225b60422` | `a792dc1e81491d42fae74466a6b50edcffdc3f8a` |
| V2 baseline stdout | 1906 | `0db84d100806527413390775055000a45402dfaabb3c5eacd5a7ae26a04d1b25` | `5b5432a7695e592a2a67195c03ff7095e291d3f0` |
| V3 candidate stdout | 1763 | `b6b0356aef7cf2e6a67cc4ef6a1e962b9702e753bce81511ecdaa9d55a3e9c88` | `8124fdc86a1dc6463102d7149ca782265314534b` |

## DECISION / LIMITS

One candidate, five additive files in the existing R16 research lane; no historical edits, new pipeline, external actor registration, secrets, Cursor dispatch, Hostinger/WWW changes, runtime integration, evaluator self-approval, ruleset mutation, biological work, or claim promotion. Publication requires an actual PR merge, immutable main readback, CI checks, and append-only Issue #93 receipt. The project-wide 90% automation and 100% publication-readback goals remain `NOT_COMPUTABLE` without complete authenticated denominators. R10 PR #115 is read-only; no independent expert receiver ACK is inferred from owner SEND.
