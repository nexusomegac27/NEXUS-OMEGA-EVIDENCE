# NEXUS OMEGA | AXIOM Alpha-Node | Required-check identity collision | 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_REQUIRED_CHECK_IDENTITY_COLLISION_AUDIT_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_WITH_GOVERNANCE_CONTRADICTION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=a3e8b63ecb52f27cef1177ad2bab86057804bbbb
PREDECESSOR_PR=299
PREDECESSOR_ISSUE93_RECEIPT=6588025294
FROZEN_EVALUATOR_FIRST_COMMIT=f45f6db7d324a9c039abfd85784385a5bb89504c
CANDIDATE_SECOND_COMMIT=8c3278cee1f6a04deeee743e0741719164f29622
PRODUCTION_WORKFLOW_OR_RULESET_MUTATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Owner GitHub API returned immutable `main` SHA `a3e8b63ecb52f27cef1177ad2bab86057804bbbb`, immediately after PR #299. Passive Issue #93 had 281 comments at observation time; all were attributed to the repository owner `nexusomegac27`. PR #115 was still OPEN with current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, no PR conversation or inline review comments and no authenticated independent receiver acknowledgment observed. The R10 manifest was present at original pinned head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` as Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; no new expert source was claimed.

The active main branch ruleset, [main-evidence-protection](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rules/21252293), requires exactly one status-check context named `validate` from GitHub Actions integration ID `15368`, with strict required status-check policy. It does **not** identify a unique workflow. The actual main check-runs endpoint returned **four distinct successful check-runs** with the same name `validate`, same app and same pinned commit, but four different workflow runs:

| Workflow source | Workflow run | Check-run ID | Git blob of workflow YAML |
|---|---:|---:|---|
| `.github/workflows/validate-scientific-communication.yml` | 41522002628 | 125540118916 | `082979fd7531b22873f0a93a8418a5e7d5b6693a` |
| `.github/workflows/validate-anchor.yml` | 41522002279 | 125540117995 | `3ab2bfecc4949cf23bc9ea1eafeb65c342cf0b0e` |
| `.github/workflows/validate-scientific-ledger.yml` | 41522002425 | 125540117930 | `787cc06380be6b3981ba2ab0fd20e53cb13881b4` |
| `.github/workflows/validate-a83-framework-hardening.yml` | 41522002296 | 125540117014 | `b03b029f7c168ac80ae42f3a40a3ad9481c367a7` |

All four original workflow YAML files were fetched at the pinned commit. Each defines a `jobs.validate` job, but their validation commands differ materially. The actual GitHub Actions run endpoints separately identify the four workflow paths; all were successful on this observed commit. Sources: `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293`; `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/a3e8b63ecb52f27cef1177ad2bab86057804bbbb/check-runs`; `GET /repos/.../actions/runs/{run_id}`; exact pinned YAML paths.

GitHub's own [protected-branch guidance](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) advises unique job names across workflows when using required status checks, because duplicates can produce ambiguous results and block merges. This report establishes **identity ambiguity**; it does **not** demonstrate that GitHub incorrectly allowed a merge, bypassed a failed required check, or that any of the four observed jobs failed.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

A required-check assertion identified only by `(context='validate', app=15368)` is insufficient to prove which specific scientific or repository validation job satisfied the intended control. Baseline: **4/4 real matching checks have no unique workflow discriminator in the ruleset**. The older `8/8 CI SUCCESS` observations remain true for that commit but cannot be substituted for uniquely scoped workflow identity or scientific evaluator execution.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The additive, research-only `alpha_required_check_collision_guard_v1_20261102.js` takes caller-supplied ruleset and check-run records. It returns `HOLD_SCOPED/AMBIGUOUS_REQUIRED_CHECK` when multiple matching checks share a required context and app on the target commit; it also rejects missing, failed, skipped, wrong-head and duplicate-ID fixtures. A unique successful check is labeled only `PASS_STRUCTURAL_ONLY`. It makes no GitHub calls, cannot authenticate API responses, and changes no protected settings.

The independent `frozen_alpha_required_check_collision_evaluator_v1_20261102.js` was committed **first**, before candidate commit. It contains 14 fixed cases, including the actual four check IDs/workflow IDs and negative mutations. An isolated Node.js process ran the frozen evaluator against the candidate: **14/14 PASS**. Independent source-byte identity for the tested code was confirmed by comparing Git blob SHA-1 and byte count from GitHub with locally hashed originals: evaluator 2,833 bytes, SHA-256 `e5b7b250f21f409f4a4e3afff3c2a5a79e7f9c07f944f36886bbbdf4b93c9175`, Git blob `71602d5c10fe462e3ef501132b8c7e6813d88dda`; candidate 2,143 bytes, SHA-256 `c7a179b673321a89368c966a51718fee81c4fe24bfb1abd63cd67ed806dd6ffb`, Git blob `a3caadf2a809cbde8bc7933b80d7b7e3f128a1ec`.

**Before/after scoped metric:** automatic collision detection on this real four-run source set **0/1 established -> 1/1 correctly flagged**; four matching jobs remain four, no CI protection is changed. Synthetic oracle: 14/14 passed. This does not measure a productive handoff gain.

**Falsifier:** Supplying only one of the four matching check-runs, or jointly forged consistent ruleset/check-run records, can produce `PASS_STRUCTURAL_ONLY`; the guard does not fetch a complete authenticated population itself. A decisive platform-level test would deliberately fail one duplicate-named job on a disposable, authorized test branch and inspect merge eligibility; **NOT_EXECUTED**, because no workflow mutation or merge-bypass experiment is authorized here.

## DECISION / SAFE NEXT ACTION

`TESTED_IMPROVEMENT_C1_ISOLATED` for the detection scaffold; `CONTRADICTION_APPEND` for the real required-check naming ambiguity. Preserve every existing workflow and ruleset. A separately reviewed, owner-authorized follow-up may give each required job a unique identity and update the protected ruleset atomically with independent negative testing; this run neither performs nor authorizes that operational change.

No production integration, no new worker, no Hostinger or WWW mutation, no scientific or claim promotion. Project-wide eligible handoff numerator and denominator remain `NOT_COMPUTABLE`; locally/private source gaps are excluded from successful automation counts. One bounded publication readback, if merged, is not a project-wide 100% readback claim.
