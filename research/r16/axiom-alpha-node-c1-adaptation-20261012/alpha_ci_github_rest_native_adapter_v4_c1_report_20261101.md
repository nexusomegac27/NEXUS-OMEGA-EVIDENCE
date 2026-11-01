# AXIOM Alpha-Node — REST-native CI inventory adapter V4 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_GITHUB_REST_NATIVE_ADAPTER_V4_20261101_R0
DECISION=TESTED_ISOLATED_C1_RESEARCH_SCAFFOLD
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=964fe47c4bdbad599e0689b132ff73c0822f3518
PREDECESSOR_PR=273
PREDECESSOR_ISSUE93_RECEIPT=6560962256
FROZEN_EVALUATOR_FIRST_COMMIT=715f0ceb00031c2e995f25e1c210e2da9c8c1477
CANDIDATE_SECOND_COMMIT=b10bf86124c4d5bcc72d10d94e483afb54e8e9d3
PRODUCTION_INTEGRATION=NO
RULESET_MUTATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The pinned V3 guard requires manually normalized `ruleset`, `check_runs`, and `inventory.ids_by_page`. GitHub's native REST shape instead has nested `rules[].parameters.required_status_checks` and `check_runs[].app.id`. Therefore V3 rejects valid raw REST-shaped snapshots until manually transformed. This is a reproducibility/handoff-friction issue, **not a security bypass**.

V3 original: `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_checkrun_inventory_completeness_guard_v3_20261101.py`; 2,944 bytes; SHA-256 `5e63313d88feb181b5255309b6d7b51065e84700a59c72585aa1621225b60422`; Git blob `a792dc1e81491d42fae74466a6b50edcffdc3f8a`.

Read-only GitHub REST fields observed on 2026-11-01, not archived as independently hashed HTTP response bytes:

- `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/branches/main`: immutable head `964fe47c4bdbad599e0689b132ff73c0822f3518`.
- `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/rulesets/21252293`: active main ruleset, one required context `validate` with app `15368`.
- `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/964fe47c4bdbad599e0689b132ff73c0822f3518/check-runs?per_page=100&page=1`: `total_count=8`, eight returned runs, four named `validate` and four named `build`, `deploy`, `report-build-status`, `validate-repository-structure`; all completed/success.

The API-source *field replay* with these eight run IDs returned `GAP_OBSERVED`, `observed_checks=8`, `required_contexts=1`, duplicate `validate` count 4. It was reconstructed from observed fields; it is **not** an original-byte REST E2E.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

Counter-hypothesis: V3 already handles unmodified REST-shaped snapshots. The independently frozen evaluator, committed before V4, falsifies this for three valid/observable raw-shaped cases. It also fixes thirteen malformed/negative cases without importing the candidate as an oracle.

| Metric | V3 | V4 |
|---|---:|---:|
| Expected outcomes | 13/16 | **16/16** |
| Valid raw REST-shaped classifications | 0/3 | **3/3** |
| Negative/malformed cases rejected | 13/13 | **13/13** |
| Manual normalization for the one-page shape | required | not required |
| HTTP-header/Link/authenticated REST E2E | NOT_EXECUTED | NOT_EXECUTED |
| Production merge enforcement | UNCHANGED | UNCHANGED |

## ISOLATED_CANDIDATE / FALSIFIER

V4 is additive and imports V3/V2 unchanged. It accepts raw REST-shaped nested ruleset and check-run objects in a bounded envelope, validates exact repository/commit URL, `page=1`, `per_page=100`, no declared next page, `1 <= total_count <= 100`, exact count, pinned SHA, active main ruleset ID `21252293`, required-status-check shape, and nested GitHub app IDs. It derives V3's inventory internally. It rejects multi-page inventories rather than claiming completeness.

Falsifier: a complete raw-shaped positive must return `OBSERVED_CONTEXTS_COVERED`; an additional `build` run must yield `GAP_OBSERVED`; mismatched count, stale SHA, missing page, invalid app ID or failed run must yield `NOT_COMPUTABLE`. These are frozen expectations in the separate evaluator.

**Limits:** The input and `fetch.next_page` are caller-supplied, not cryptographically authenticated or verified HTTP Link headers. An attacker can forge both response and metadata. V4 does not fetch GitHub itself, validate source signatures, establish complete historical CI provenance, prove a required gate was bypassed, or modify branch rules. `GAP_OBSERVED` is a structural comparison only.

## INDEPENDENT_TEST / REPRODUCIBILITY

The evaluator was first committed at `715f0ceb00031c2e995f25e1c210e2da9c8c1477`; the candidate followed at `b10bf86124c4d5bcc72d10d94e483afb54e8e9d3`. Separate Python subprocesses executed locally. From repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_rest_native_evaluator_v4_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_checkrun_inventory_completeness_guard_v3_20261101.py
# expected 13/16, exit 1
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_rest_native_evaluator_v4_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_github_rest_native_adapter_v4_20261101.py
# expected 16/16, exit 0
python scripts/validate_repository_structure.py --root .
# NOT_EXECUTED_LOCALLY against full repository; check GitHub CI separately
```

| Source / output | Bytes | SHA-256 |
|---|---:|---|
| Frozen evaluator | 4313 | `cf54b496b861f02ae468cc342e096e145899b93278a14cf30e56445d9b7fb952` |
| V4 adapter | 4462 | `17e81cb944bd0a79fc616e5bbb4ad79962190d2b800a96d79b9a3590221dacd3` |
| V3 baseline stdout | 1698 | `487da0577af796b09f3bae4383ec6b483287e9d92cb33be3c0b28ce682e62b67` |
| V4 candidate stdout | 1702 | `e3b74814a2cc1595e9a73c1535ea7b43ab9632fbc09158e1ba81329664ad2b36` |

## DECISION / NEXT GATES

Exactly one additive C1 research candidate under the existing R16 directory. No old files changed, no new pipeline, external agent/worker, rights, secrets, node reset, Cursor dispatch, Hostinger/WWW action, biological experiment, ruleset mutation, or claim promotion. Publication requires actual PR/CI, immutable main source readback and an append-only Issue #93 receipt. Project-wide 90% automation and 100% publication-readback metrics remain `NOT_COMPUTABLE` without authenticated total denominators. R10 PR #115 is read-only: owner SEND is not independent expert ACK.
