# AXIOM Alpha-Node — dual-endpoint PR filename census V1 · 2026-10-31

```text
OBJECT=NEXUS_OMEGA_ALPHA_PR_DUAL_ENDPOINT_CENSUS_GUARD_V1_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_PENDING_GITHUB_PUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=f9a34220ae351efc24114c4bbe48c3042097ebf6
PREDECESSOR_PR=241
PREDECESSOR_ISSUE93_RECEIPT=6544134604
FROZEN_ORACLE_FIRST_COMMIT=9f9938afb6c12675a956a3c03a878e7b07ddb163
CANDIDATE_FINAL_COMMIT=756c8b5a7f58475b41ab095de1dd8ff1aa881382
```

## One bounded improvement and counterhypothesis

Prior guard `alpha_pr_filename_census_crosscheck_v1_20261031.py` accepted a self-consistent but forged two-file listing for PR #240 even though the actual PR changed three files. The prior guard explicitly disclaimed API authentication. Its original source was fetched from pinned main and independently re-created byte-identically for the test: 3,423 B, SHA-256 `bf611fdfcf2bd87eddd53cbc5e5dd8516f84b9cdcaa30dd7f3cdd857254db04f`, Git blob `b289511f14a14c3a946a54dc81b32a57883005ec`. An actual subprocess with a two-file forged `api_file_listing`, `pr.changed_files=2`, and matching local declaration returned exit 0 and `API_FILENAME_CENSUS_MATCH_UNAUTHENTICATED_PROJECTION` (2 files). This is a **source-projection trust gap**, not a demonstrated GitHub compromise.

Negative hypothesis: a single caller-supplied PR file listing and completion flag can be self-consistent yet omit a real file. The additive V1 candidate compares the file set against a separately obtained GitHub compare endpoint, binds both to exact PR base/head and a linear merge-base, and rejects mismatched file sets. It deliberately supports only additive PRs with 1–100 files and two explicit paginated requests (page 1 plus empty page 2); other shapes fail closed. It does not authenticate the two caller-supplied endpoint projections, transport, actor, CI, original file bytes or actual pagination. If an adversary forges both endpoint projections consistently, the candidate may still accept: **this is the residual falsifier**. A real GitHub PR with 101+ files, renamed/modified files, or non-linear ancestry is outside this candidate's positive scope.

## Original API observations (read-only, pinned)

GitHub PR #240: `base_sha=0e32161a7599291ff581b8c8c1b072c37d2d99ec`, `head_sha=0af4961cec47093e8e99de8811b593fe167e661f`, `changed_files=3`. GitHub REST `GET /pulls/240/files?per_page=100&page=1` returned 3 added files and blob IDs; page 2 returned an empty list. Independent `compare_commits(base,head)` returned `ahead_by=3`, `behind_by=0`, `status=ahead`, `merge_base=base` and the same three filenames:

- `alpha_publication_full_readback_preflight_v1_20261031.py` — blob `4ffbc155a6c20eb6b08bf41a167e85d6ba9cf6a0`
- `alpha_publication_full_readback_preflight_v1_c1_report_20261031.md` — blob `9b7fdb089147bad8fb76f441ad821aa2c958811f`
- `frozen_alpha_publication_readback_oracle_v1_20261031.py` — blob `a4c98d74fac66c47fd1b46abf011cc258e13ceea`

All are under `research/r16/axiom-alpha-node-c1-adaptation-20261012/`. The API data was projected into a frozen synthetic test envelope; full original HTTP response bodies and response headers were not independently archived. The oracle's local-preflight success field is synthetic and does not constitute a new independent source-byte readback of PR #240.

## Independent test and measured delta

The independent black-box oracle was physically written, SHA-256/Git-blob checked and committed **before** the candidate. The candidate was tested in isolated Python subprocesses; test expectations were not changed after candidate creation.

- Frozen evaluator: `frozen_alpha_pr_dual_endpoint_oracle_v1_20261031.py`, **6,358 bytes**, SHA-256 `ae05484acc6f643025c7a92ea95f0437070f79b49b8558ec814a1d68d4832545`, Git blob `3258bd5b573776b7d24a098ea10166b87d0ca38f`.
- Final candidate: `alpha_pr_dual_endpoint_census_guard_v1_20261031.py`, **5,183 bytes**, SHA-256 `210c19082277fdc98e05fb91509eec91e3e1cd8f17e51fdcef493b5f3033f603`, Git blob `9000a7a9afab83a35b3082347c6ca0e9064f60d2`.
- Reproduction from the same directory: `python frozen_alpha_pr_dual_endpoint_oracle_v1_20261031.py alpha_pr_dual_endpoint_census_guard_v1_20261031.py`.
- Actual local outcome: **33/33 PASS**, including 4 positive assertions and **29/29 adversarial/invalid negative cases FAIL_CLOSED**; subprocess exit 0. Forged PR-file omission with locally reduced count: predecessor accepted **1/1** attack fixture; new guard rejected **1/1**. This is a bounded fixture-detection improvement, not an operational Handoff success rate.
- A pre-publication GitHub candidate commit `7a8e00ee60e22c05e955db9bedec9ef391e46004` differed from the locally tested source (one missing parenthesis and two extra backslashes). The discrepancy was detected by the Git-blob readback and corrected **on the unpublished branch** in commit `756c8b5a7f58475b41ab095de1dd8ff1aa881382`. The original oracle commit was not modified. The final Git blob matches the tested source exactly. This failed pre-publication transfer is retained as negative provenance, not concealed.

## Governance and measurement boundary

Only additive isolated research files under the existing R16 directory. No new root, historical source overwrite, actor registration, runtime/Hostinger/WWW write, CI/ruleset modification, Cursor dispatch, worker or claim promotion. Independent technical evaluator != external third-party scientific adjudication. GitHub-API agreement != authenticated response bytes. GitHub->WWW parity remains `NOT_ESTABLISHED`.

Target `>=90%` eligible public handoffs: **NOT_COMPUTABLE** (complete authenticated numerator and denominator including failed attempts absent). Target `100%` published full readbacks: **PROJECT_RATE_NOT_COMPUTABLE**; one run's complete publication may be reported only after actual main and receipt readback. Zero unauthorized writes is a target, not a proof of global absence. Synthetic 1/1 fixture detection is not a project KPI.

## R10 secondary read-only check

PR #115 is open, current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, original pinned manifest head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`. The manifest at the pinned original head is retrievable (4,588 UTF-8 characters, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`); its recorded SHA-256 is `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, not independently recomputed in this run. PR #115 has zero comments. All 231 observed Issue #93 comments were owner-authored; no authenticated independent expert return was found. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.

Publication status when this report was authored: PR/CI, merge, actual main and Issue #93 append-only receipt **PENDING**. Any subsequent claim requires separate GitHub API readback.
