# C1 addendum · bounded GitHub Checks API census for PR #274–283

This is an **append-only supplement**, not a rewrite of the prior report. After the first-page workflow-only census (50/50 completed-successful), the approved GitHub REST `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/{PR_HEAD_SHA}/check-runs?per_page=100` endpoint became available through the connected GitHub read path.

For **each** of PR #274–283, GitHub returned `total_count=8`, eight enumerated check runs, and all eight with `status=completed` and `conclusion=success`, including `semgrep-cloud-platform/scan`. **80/80 check runs**, with immutable PR head SHA, check ID, name, app and conclusion recorded in `alpha_publication_census_check_runs_274_283_20261102.json`.

This closes the earlier **bounded PR-head check-run inventory gap only**. It does not authenticate GitHub beyond the connected API transport, audit the whole repository, prove post-merge main CI, prove scientific correctness, or measure actual automated artifact handoffs. The bounded selected-cohort commit/source/PR-head-check/owner-receipt readback is **10/10** on the declared provider-evidence criteria; the **project-wide** full-readback denominator remains `NOT_COMPUTABLE`.

Source-byte census remains 36/36, 153,329 bytes; ten adjacent commit comparisons, ten owner receipts and 80 PR-head checks are distinct evidence layers. `C1_DESCRIPTIVE_ONLY`; no production or WWW claim.
