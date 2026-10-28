# NEXUS OMEGA · AXIOM Alpha-Node · C1 paginated handoff census witness · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_PAGE_CENSUS_20261028_R0
CLASS=ISOLATED_C1_RESEARCH_CANDIDATE_NOT_PRODUCTION_INTEGRATION
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PREDECESSOR_MAIN=64170faa12da85db8d2c7d5cfcf6995269ea2f8e
PREDECESSOR_ISSUE93_RECEIPT=6465851951
SOURCE_V1=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_metric_witness_v1_20261028.py
SOURCE_V1_GIT_BLOB=c98b8e9334255ad82c04788450ef1b17360f66ed
FROZEN_EVALUATOR_FIRST_COMMIT=9928e63bf27d900eaf21837d7eb19ba16bd27ba1
CANDIDATE_SECOND_COMMIT=d016a29a3fd79699ed8e2987f50f8942c06500cc
GITHUB_MAIN_MERGE=NOT_YET_EXECUTED_AT_REPORT_AUTHORING
WWW_PARITY=NOT_ESTABLISHED
```

## One bounded change

The v1 handoff metric witness accepts a caller-declared `DECLARED_COMPLETE` flat event list and reports a scoped 9/10 rate on its synthetic fixture. The source has no page count, pagination continuity or per-page source-pin checks. A truncated multi-page collection can therefore be presented as a smaller complete event list without a structural pagination error. This is a **source-inspection limitation**, not a claim of a real NEXUS missing-page incident.

The new isolated v2 witness accepts caller-supplied page records and requires: ordered 1-based pages, exact `next_page` continuity, consistent per-page `reported_total`, identical pinned source commit, unique event IDs across pages, and a complete terminal count before emitting a `DECLARED_COMPLETE` scoped rate. An incomplete partial census returns `NOT_COMPUTABLE` for scoped and project-wide rates. Unknown eligibility remains fail-closed. The four readback booleans are still caller assertions, not independently authenticated GitHub readbacks.

## Pinned independent test

- The subprocess evaluator was committed **before** the candidate, under `frozen_handoff_page_census_evaluator_v2_20261028.py`.
- Evaluator: **6,255 bytes**, SHA-256 `43032eb24cc7c4aaae798bfcbbd8cf64e8ba16b3b4966d904485d2c0e0491a6d`, Git blob `73b8a1ad805f08e56e6d7d667578e94fcd58b98d`.
- Candidate: **8,528 bytes**, SHA-256 `c16806be3d00810b0e6d6ddeefc336c7428c9f6104c050c52815deb725cac8fd`, Git blob `e7882865407d2beb1b522182a86bf3351a7ef824`.
- Local Python subprocess evaluation: **21/21 PASS**. Synthetic positive: 2 pages / 12 events / 10 eligible / 9 automated / 11 public publications / 11 complete caller-asserted readbacks. These are synthetic ratios, **not NEXUS project metrics**.
- True negative fixtures include missing final page, omitted event, conflicting or forged totals, broken page link, cross-page duplicate event, foreign commit, malformed booleans, duplicate JSON key, nonfinite number, and over-budget input.
- Targeted negative mutant without terminal total equality: **19/21 PASS, 2 expected failures**. Mutant without intermediate next-link enforcement: **20/21 PASS, 1 expected failure**. The unchanged evaluator rejects both mutants.
- Environment: isolated Linux Python subprocesses; no live API pagination or third-party validation.

## Falsifier and counterhypothesis

**Counterhypothesis:** A `DECLARED_COMPLETE` inventory can still be incomplete if a caller fabricates a smaller total, terminal marker and matching pages. This candidate cannot independently authenticate GitHub API pagination, event origin, rights or scope completeness. A real GitHub page omitted while the caller also rewrites the declared total is a decisive falsifier of any claim that this witness alone establishes complete inventory. It is intentionally **not** claimed to do so.

**Measured change:** Before: v1 has no pagination completeness check. After: the v2 synthetic frozen evaluator detects all tested omissions, count inconsistencies, page-order and next-link defects, while preserving the 9/10 synthetic arithmetic for a valid complete two-page fixture. No independent improvement to real-world handoff automation is claimed.

## Publication and boundaries

Three additive files in the existing registered R16 research lane only. No edits to v1, frozen evaluators, governance, pipeline roots, CI, external actor registry, Hostinger, WWW, runtime, model weights or system instructions. No secrets or private materials. The `CLAIM_CEILING` remains `C1_DESCRIPTIVE_ONLY`.

The project-wide eligible handoff denominator is **unknown**, so `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; 90% automation and 100% project-wide readback are **not established**. The owner GitHub branch/PR/CI/main readback and append-only Issue #93 receipt must be checked separately after publication. An isolated test is not productive integration or scientific promotion.
