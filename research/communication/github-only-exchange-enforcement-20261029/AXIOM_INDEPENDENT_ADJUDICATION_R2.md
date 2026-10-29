# NEXUS OMEGA · AXIOM Independent GitHub Exchange Adjudication R2

OBJECT = NEXUS_OMEGA_AXIOM_GITHUB_EXCHANGE_ENFORCEMENT_ADJUDICATION_20261029_R2
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_ONLY_EXCHANGE_ENFORCEMENT_20261029_R1
CURSOR_SOURCE_COMMIT = 952951f0e38f703865dba305a47b183faa6b1798
SOURCE_PATH = research/communication/github-only-exchange-enforcement-20261029/RESULT.md
SOURCE_BYTES = 3193
SOURCE_SHA256 = 0e9b321216e697b181534ec78e049f5484c7cd090d12d757993d96a0343ca951
SOURCE_REHASH = AXIOM_INDEPENDENT_GITHUB_FETCH_AND_SHA256_MATCH
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
DECISION = CONTINUE_CURSOR_EXCHANGE_REPAIR; NATIVE_APP_R3_HOLD
STATUS = PASS_WITH_MATERIAL_CAVEATS_C1_REPORT_AND_SOURCE_AUDIT
DRAFT_PR = 185
RUNTIME_DISPATCH = NOT_ESTABLISHED
EXTERNAL_INDEPENDENT_ACK = NOT_ESTABLISHED
MAIN_ENFORCEMENT = NOT_ESTABLISHED

## Source-exact evidence audited

From commit 952951f0...:
- `RESULT.md` direct independent GitHub readback, exact UTF-8 3193 bytes, SHA256 match above.
- `scripts/nexus_github_exchange_chain.py`, `tests/test_nexus_github_exchange_chain.py`, `G8_SYNTHETIC_CYCLE_RECEIPT.json`, `G9_EFFICIENCY_RECEIPT.json`, `G6_CI_GOVERNANCE.md`, `G7_IMPLANT_ANALYSIS.md`, `.github/workflows/validate-repository-structure.yml` read independently via GitHub.
- GitHub PR 185 OPEN/DRAFT/NOT_MERGED at source commit, changes include new validator, synthetic tests, CI step and previously operator-bound communication law.
- 22/22 is producer-reported test execution; source test definitions inspected, not independently rerun in this adjudication.
- GitHub combined *commit-status* API returns empty array for commit, which is NOT proof that no GitHub Actions check runs exist; independent required-check enforcement still NOT_ESTABLISHED.

## Material observations / required repairs

**F01 — Critical provenance gap in SourceResolver (source code observed).** `_fetch_blob()` first accepts `checkout_root / ref.path` if it exists, explicitly even if the requested commit does not match checkout HEAD. Its SHA256 check then confirms bytes but NOT claimed repository/commit provenance. A local file with matching bytes and a fabricated/nonexistent commit can be accepted. Enforce exact full commit (40-hex), verified repository identity, path confinement and source fetch at the pinned commit (e.g. `git show <verified_commit>:<safe_path>` or API pinned ref). No worktree fallback as provenance proof; test same bytes + false commit and wrong repo -> DENY.

**F02 — Claimed actor identity is not authenticated.** `AgentAdapter.prove()` checks a local allowlist and sets `github_read=True` as a fixed value; `github_login_bound` is true whenever a caller passes a nonempty login, with no remote GitHub principal verification. This is a policy fixture, not GitHub capability proof. Distinguish `DECLARED`, `REGISTRY_MATCH`, `GITHUB_AUTHENTICATED`, `PERMISSION_TESTED`; deny assumed rights and use separate least-privilege credentials.

**F03 — The synthetic receiver creates its own ACK.** `run_synthetic_cycle()` calls the same process's `DeliveryJournal.independent_ack(artifact_bytes=outbound_bytes,... receiver_id="synthetic...")`. It is a valid unit test but not independent receiver fetch, identity, GitHub upload, or detached receiver attestation. Require distinct authenticated receiver and recipient-produced ACK bound to source commit/path/bytes/hash, identity, and time.

**F04 — Journal is not yet a durable append-only delivery ledger.** `DeliveryJournal.append()` loads and rewrites a JSON object without transactional locking, atomic commit/fsync or crash recovery; `reconcile()` checks event-type presence, not independently verified event provenance/authorization. Concurrency, torn-write and spoofed ACK fixtures required; implement durable event identity, replay-safe idempotency and crash consistency in a bounded local transactional store.

**F05 — G9 95% is a synthetic test datum, not operational impact.** The receipt compares fabricated `100` baseline manual handoffs with `5` observed manual and `95` claimed receipts. `LOCAL_METRIC_PASS` only, never `90PCT_OPERATIONAL_PROVEN`. Record real transfers and unique receiver ACKs with independent denominator.

**F06 — E01–E10 COMPLETE is fixture metadata.** G8 synthetic receipt lists 10 COMPLETE statuses in a fixture, no real external expert received source bytes or returned work. Pilot with a separately registered, authorized GitHub principal and source-exact lane; do not recycle the R27-E external return slot for this assignment.

**F07 — Main CI gate and PR still pending.** Tests wired in draft branch; no observed required status/CodeOwner rule binding on main. Commit status lookup alone is inconclusive; obtain ruleset/check-run/branch protection evidence. Do not merge or promote without owner authorization.

**F08 — Implant mount partially analyzed.** Cursor found /assets/ JS/CSS HTTP 200 and bare paths 404, but no browser E2E fetch UX witness or WWW deployment. Preserve no-WWW-write and keep implant a public-safe read/status view, never privileged source authorizer.

**F09 — Source closure cannot depend solely on self-declared `parent_refs`.** The resolver traverses whatever parents are explicitly listed, but a missing mandatory ancestor in an incomplete manifest cannot be inferred. Bind task anchor and required-source inventory, derive closure deterministically, detect cycles/aliases/paths/rights/secret-class gaps, and report all non-present required objects before `READY_FOR_EXPERT`.

## Next Cursor execution scope (separate pure manual order)

Continue existing PR #185 only, owner-controlled draft; repair F01-F09 using negative tests and audited primary GitHub documentation. Preserve original evidence and add append-only successor, no force-push, no unapproved external writes, no GitHub runtime credentials in public content. Avoid another archive transfer via Operator. Return only repository + exact full commit + exact return path + bytes + SHA256 + gate states. If independent external principal/adapters remain unavailable, report blocked lane rather than pretending success.

## Primary external evidence (current official GitHub documentation)

- Webhook security and X-GitHub-Delivery: https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
- HMAC-SHA256 validation and constant-time compare: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
- Failed webhook redelivery/reconciliation (not automatic): https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries
- GitHub App identities and installation access tokens: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app
- Ruleset effective enforcement: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Untrusted pull_request_target controls: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

## Terminal

NATIVE_APP_R3 = HOLD
EXTERNAL_AGENT_WRITE_ALLOWLIST = UNCHANGED_DEFAULT_DENY
GITHUB_MERGE = NO
WWW_WRITE = NO
DEVICE_INSTALL = NO
CLAIM_PROMOTION = NO
NEXT = CURSOR_SOURCE_PROVENANCE_AND_RECEIVER_ACK_REMEDIATION_ON_PR185
