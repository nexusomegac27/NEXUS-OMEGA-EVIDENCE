# AXIOM Alpha-Node — PR filename census crosscheck V1 (2026-10-31)

OBJECT: NEXUS_OMEGA_ALPHA_PR_FILENAME_CENSUS_CROSSCHECK_V1_20261031_R0
DECISION: TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING: C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE: 8414fad60c646c3970ec52d870f30bb7bc2c417a
PREDECESSOR: PR #240; Issue #93 comment 6543650224
FROZEN_ORACLE_FIRST_COMMIT: 332d93935b97d191a36eced7e87066568aa4fa3c
CANDIDATE_SECOND_COMMIT: f1d761b8519411d9dbf11b4c6a2eb6914d326f92

## One candidate and falsifier

The preceding byte-preflight checks only a caller-declared changed-file count. It can accept a self-consistent 2/2 declaration even if a real PR changed three files; its source does not contain a paginated GitHub filename census. This is a completeness gap, not proof of a security exploit.

The additive isolated guard compares an all-pages GitHub PR filename projection with the local preflight file set, API changed-file count and pinned PR head. It fails closed on missing, extra, duplicate or invalid paths, wrong counts/head, incomplete pagination, invalid preflight status and C2 promotion. Falsifier: any such adversarial mutation passes, or a complete reordered set fails. A forged caller-supplied API pagination flag remains an unresolved stronger falsifier.

## Original sources and test

Pinned main was physically read with AGENTS.md, GOVERNANCE.md, R16 Alpha contract, Operator C1 direct-publication rule, Task Anchor Norm, repository order, research/pipeline, Repository Steward V1 and external write-slot registry (default DENY; allowlist empty). PR #240 is merged; immutable head 0af4961cec47093e8e99de8811b593fe167e661f, GitHub changed_files=3. The connector's paginated PR listing returned the three existing R16 filenames: alpha_publication_full_readback_preflight_v1_20261031.py, alpha_publication_full_readback_preflight_v1_c1_report_20261031.md and frozen_alpha_publication_readback_oracle_v1_20261031.py. This projection is not an independently authenticated page transcript.

The evaluator was committed and Git-blob read back before the candidate existed. Original UTF-8 bytes were independently SHA-256/Git-blob hashed and matched the connector's pinned Git blobs:

- frozen_alpha_pr_filename_census_oracle_v1_20261031.py: 4744 bytes; SHA-256 3a5ddb2bd2e5fbf91746c67d7374b7f6b8bbfc2af083f4a90ec7477d18645648; Git blob 8fee521673b0f926ea96f7dd5e1aa28c122adddb
- alpha_pr_filename_census_crosscheck_v1_20261031.py: 3423 bytes; SHA-256 bf611fdfcf2bd87eddd53cbc5e5dd8516f84b9cdcaa30dd7f3cdd857254db04f; Git blob b289511f14a14c3a946a54dc81b32a57883005ec

Reproduction: python frozen_alpha_pr_filename_census_oracle_v1_20261031.py alpha_pr_filename_census_crosscheck_v1_20261031.py
Observed: 23/23 PASS, subprocess exit 0 (4 positive assertions; 19 adversarial/invalid-input cases). The real PR #240 filename projection matched 3/3 in the isolated fixture; removing one local file and reducing the declared count to 2 yielded FAIL_CLOSED/file_set_mismatch, exit 2. Before: no PR-file-set comparison; after: one omission detected. No original PR #240 bytes were newly rehashed by this guard, and its local-preflight-success input is synthetic.

## Limits and decision

Output is API_FILENAME_CENSUS_MATCH_UNAUTHENTICATED_PROJECTION, not authenticated GitHub readback. Caller-supplied API flags, page completeness, preflight success and actor identity remain untrusted; this is not a full CI/receipt/source authentication system. PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE; PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE; authenticated denominators including failed attempts absent. No productive integration or GitHub ruleset/Hostinger/WWW change.

R10 secondary check: PR #115 OPEN, head dab7c59070d67e7e2a244bd6d05db9a4d37460e3; pinned R10 manifest at 539d4bb33d2ba2c4895713c1bc437ece0743eeea is 4588 bytes, Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df; prior SHA-256 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc. PR #115 has no comments; all 230 Issue #93 comments at observation owner-authored. PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED.

Publication state at report creation: PR CI, merge, actual main readback and append-only Issue #93 receipt PENDING. No new worker, Cursor dispatch, external actor registration, biological experiment, node reset or claim promotion.
