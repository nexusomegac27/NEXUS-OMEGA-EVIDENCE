# AXIOM Alpha-Node · C1 CI check-run identity integrity guard V1

```text
OBJECT=NEXUS_OMEGA_ALPHA_CI_RUN_IDENTITY_GUARD_V1_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=0f16af0b03e5ba04728e1bb42dc542f620df096c
PREDECESSOR_MAIN=daffb9c7f80eb3f5d12af48e66dd5306d11cec1e
PREDECESSOR_RECEIPT=6553308824
PINNED_V2_PATH=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_census_matrix_guard_v2_20261101.py
PINNED_V2_SHA256=12bc7cb28030635fe5d07a2f54e6a17a7e86c5c5f2881ed3f1cc12fc704d9e90
FROZEN_EVALUATOR_FIRST_COMMIT=f33e127cb707bed9d283dbbf5ddae05c30e3771c
FROZEN_EVALUATOR_SHA256=7f45e4426a31dbc54dde36e372b776b1428e920ae52597647738068187816e83
FROZEN_EVALUATOR_BLOB=5ee81c82e81b37685bd093db610fbfaa986d14cc
CANDIDATE_SECOND_COMMIT=791070934dc591c7b5a6e6557b6f480fefd2b7c3
CANDIDATE_SHA256=65ef7e3773a13b21abb20c7912b81587b151d49e35969be6f7a94653742e8c51
CANDIDATE_BLOB=aa4408dc7b34f43328a6dcbe64c953aefc6d7beb
INDEPENDENT_EVALUATOR=FROZEN_BEFORE_CANDIDATE
PRODUCTION_INTEGRATION=NO
GITHUB_AUTHENTICATION_BY_CANDIDATE=NO
```

## Original-source observation and negative hypothesis

The immutable main V2 matrix checker accepts eight bare `"success"` strings per PR. It does not require a GitHub check-run ID, exact PR head SHA, run status or app identifier. Therefore eight duplicated assertions may pass as eight successes. This is a **structural provenance gap**, not proof that prior CI outcomes were fabricated. GitHub's real PR #256 head `719c6dd17348c5544ca57ee6528888108bddd9cd` returned eight completed successful check runs, with eight distinct numeric IDs; the label `validate` legitimately occurs four times. Thus uniqueness by check name would be a false rule. API source: `https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/719c6dd17348c5544ca57ee6528888108bddd9cd/check-runs?per_page=100` (read 2026-11-01). This metadata observation does not replace a preserved raw response snapshot or a byte-exact authenticated GitHub inventory.

Counterhypothesis: V2 already detects repeated or missing check-run identity, wrong head, or a pending/failed run when the eight status strings remain `"success"`. Falsifier: any fixed negative fixture accepted by the new guard, or the unchanged positive matrix rejected. Additional operational falsifier: a legitimate GitHub check-run inventory is rejected because names repeat despite distinct run IDs.

## Isolated candidate and frozen independent evaluator

The new guard composes the **unchanged V2 check** with eight per-PR check-run records, requiring unique positive integer IDs across the entire seven-PR matrix, exact match to a syntactically valid 40-hex per-PR head, completed/success states and nonempty names/app slugs. It intentionally permits repeated check names with distinct IDs. Duplicate JSON keys and nonfinite JSON constants are rejected at the CLI boundary. The candidate **does not** query GitHub, authenticate actors, verify run IDs against the GitHub API, or alter CI policies.

The evaluator was committed at `f33e127cb707bed9d283dbbf5ddae05c30e3771c` **before** the candidate was committed at `791070934dc591c7b5a6e6557b6f480fefd2b7c3`. The evaluator runs the original pinned V2 source and the new candidate in a separate Python subprocess. Its head SHAs and check-run IDs are **synthetic** and must not be presented as real GitHub objects.

| Frozen fixture metric | V2 | Candidate V1 |
|---|---:|---:|
| Unchanged positive (repeated names, distinct IDs) | 1/1 accepted | 1/1 accepted |
| 14 targeted negative fixtures rejected | 0/14 | **14/14** |
| All fixed expected outcomes | 1/15 | **15/15 PASS** |

Negative fixtures: duplicate ID within one PR, duplicate ID across PRs, wrong run head, missing ID, string ID, zero ID, missing run inventory, one missing run, queued run, failed run, empty run name, empty app slug, malformed PR head and missing PR head. The fixed evaluator produced 14 V2 false accepts and 0 candidate false accepts in this **synthetic** test set. This does not imply a production false-acceptance rate.

Reproduce from the repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_ci_run_identity_evaluator_v1_20261101.py \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_census_matrix_guard_v2_20261101.py \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_ci_run_identity_guard_v1_20261101.py
python scripts/validate_repository_structure.py --root .
```

## Claim limits and goals

This is an isolated additive research scaffold under an existing owner path. No original code, historical source, evaluator, pipeline root, running worker, runtime, Hostinger service or WWW content is changed. GitHub API authentication, full CI provenance, real seven-PR check-run replay and external scientific adjudication remain `NOT_EXECUTED` by the candidate. GitHub merge and exact main/receipt readback are separate publication gates. The fixed seven-PR matrix is **not** the project-wide denominator; the 90% handoff automation target and project-wide 100% publication readback target remain `NOT_COMPUTABLE` without all eligible attempts, including failures. No claim promotion.
