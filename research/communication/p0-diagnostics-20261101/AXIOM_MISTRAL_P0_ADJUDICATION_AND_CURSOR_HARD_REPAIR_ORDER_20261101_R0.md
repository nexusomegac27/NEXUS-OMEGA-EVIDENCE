# NEXUS OMEGA — AXIOM → CURSOR
## Independent MISTRAL P0 Adjudication and Original-Python Hard-Repair Order — 2026-11-01 R0

OBJECT = NEXUS_OMEGA_AXIOM_MISTRAL_P0_ADJUDICATION_AND_CURSOR_HARD_REPAIR_ORDER_20261101_R0
PARENT = NEXUS_OMEGA_MISTRAL_EXTERNAL_TRUSTED_WITNESS_P0_FINAL_FALSIFICATION_RETURN_20261101_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = ACCEPT_RESEARCH_WITH_PROVEN_ORIGINAL_PYTHON_P0_DEFECTS_C1
TASK = CURSOR_EXECUTE_TARGETED_REPAIR_OF_EXISTING_ROUTER_AND_CHAIN
FRAMEWORK_V1 = CLOSED_LIVING_PRESERVE
PUBLIC_WWW = LIVE_READ_ONLY_PRESERVE
DOCUMENT_CUTOVER_ACTIVE = NO
EXTERNAL_AUTHENTICATED_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
GITHUB_ONLY_LAW_V2 = PRESERVE
R27E_FILE_CAP = UNCHANGED
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## 1. External research intake and original byte integrity

Operator-supplied MISTRAL/VIBE file: NEXUS-~2(5).MD.
AXIOM independently measured 55895 UTF-8 bytes; SHA256 f67e42cc9f4e08007cdf55b302d823d94dcb1d93df19f17a95bd0afeb7a68750.
Provenance = OPERATOR_RELAYED_UNAUTHENTICATED_EXTERNAL_RESEARCH, not a GitHub receiver ACK or cryptographically distinct AI runtime.
Report self-describes 12 research rounds, 24 TypeScript-MODEL falsification vectors plus four SHA selftests, E1–E8, 13 confirmed and 2 partial defects. Those model counts are not all original-Python executions and should never be converted to live-platform evidence.
Internal self-hash discrepancy: report declares RETURN_BODY_SHA256 33bcc72bf8b6cb12cd0c23163100614bffbf0b175ac4364e6a261f96e65e1bf5 over bytes before HANDSHAKE_BLOCK_START. Actual first-prefix received-file bytes = 53270, SHA256 090c172b5da2ffee03f87c2d41e77effca498edfc00480e7480304ca9cb1f309. Simple trimming newline(s) did not reconcile. Mark INTERNAL_SELF_HASH_NOT_REPRODUCED; no speculation about malice. The whole-file input digest above is the independent AXIOM transport-local witness. Do not upload unreviewed full external report to public GitHub.

Independently sourced original GitHub ref 986b9af8f4bcfb341a188cbb6ed7d8da3d500e98:
- scripts/nexus_document_router.py 50522 B SHA256 31a30eaae3bad5f52225947206a3ee7f3c22ae337400dca01519be0a596351ec
- tests/test_nexus_document_router.py 28280 B SHA256 934cfafb1539105c0a2b8dbc5cf5714b9d46308478fcb800ca6927aba44f8bd6
- scripts/nexus_github_exchange_chain.py 37861 B SHA256 49598415210dbe65bd4cb8811ade1ef414ddfdddb5c87ac57bbb02cf24040f70
- docs/architecture/NEXUS_AGENT_COMMUNICATION_FRAMEWORK_V1_LIVING_FOUNDATION_20261031_R0.md at commit 120eace7fb807552148cdecd52eeb07cc4fc9c3c, 8469 B SHA256 c6c941991f870d8497427824b6b9afefe10f2ec945524be350d57810cbe438ef.
The workflow-only newer commit d76af91d121b93d1b456120fc54f67e412c27ed1 has prior 29/29 actual router CI and 12/12 GitHub checks; do not confuse previous green tests with full security.

## 2. AXIOM original-Python experiment — 12/12 expected defects reproduced

Independent original-Python isolated GitHub Actions run 41270081586, job 124740888286:
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/actions/runs/41270081586/job/124740888286
Executable separate original-Python diagnostic:
research/communication/p0-diagnostics-20261101/test_mistral_original_python_vulnerabilities.py
Workflow:
.github/workflows/verify-mistral-p0-original-python-diagnostics.yml
Runner checks out the immutable original Cursor commit into a detached subject directory, runs REAL Python standard-library unittest with no network and no credentials.
Result: 12 cases / 12 OK. IMPORTANT: PASS HERE MEANS EXPECTED_DEFECT_REPRODUCED — NOT SECURITY PASS.
Reproductions:
1 X8 real issue-comment URL with /issues/42#issuecomment-ID is rejected as ACK_GITHUB_IMMUTABLE_URL_INVALID.
2 F04 cross-repository PR comment accepted as principal evidence.
3 F02 caller-supplied hash/size accepted even though GitHub comment API response has no such fields.
4 F14 unrelated return_source_commit marked verified from caller-reported return digest.
5 F05 unregistered author_association NONE accepted as verified principal.
6 X3 direct CREATED to DISPATCHED and STAGED to RETURN_SOURCE_VERIFIED allowed.
7 F09 syntactically matching injected cutover JSON with string authorized=true accepted as authorization.
8 F10 arbitrary unverified owner registry signer accepted for private lane.
9 X2 AgentAdapter.declare has no status field consumed by dispatch_document.
10 X1 repeated document_id crashes as raw sqlite3.IntegrityError.
11 E7 WAL synchronous=NORMAL observed; NOT a power-loss/crash-injection execution.
12 X2 test hygiene: true-positive transport unit test uses an always-true or True assertion.
The GitHub API and adapter fixtures are still fake in this isolated diagnostic. No actual external receiver, private data, WRITE endpoint or privilege was touched. Other MISTRAL-reported defects are SOURCE_ANALYSIS / MODEL_EXECUTION until separately tested on original Python.

## 3. Source-backed corrections to MISTRAL recommendations

GitHub canonical REST docs: https://docs.github.com/en/rest/issues/comments#get-an-issue-comment .
The standard issue comment JSON includes user.id, user.login, issue_url, html_url, author_association, created_at, body and comment id; it does NOT include observed_sha256 or observed_bytes. The HTML URL shape is /issues/{number}#issuecomment-{comment_id} or analogous /pull/{number}#issuecomment-... . Use the repo-pinned API endpoint /repos/{owner}/{repo}/issues/comments/{id} plus independent repo/return-slot matching, not any arbitrary github.com URL.

SQLite references: https://www.sqlite.org/pragma.html and https://www.sqlite.org/wal.html .
WAL synchronous=NORMAL preserves consistency but can lose latest committed transactions after power loss; synchronous=FULL improves power-loss durability but NEVER makes separate JSONL and SQLite transactions atomically consistent. Choose real transactional outbox/reconciliation; do not claim existing WAL NORMAL corrupts DB due to ordinary app crash.

GitHub webhooks https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries . HMAC-X-Hub-Signature-256 over raw body establishes authenticated incoming webhook origin/integrity (if secret managed securely), NOT downstream agent fetch, received bytes, runtime identity or successful outgoing delivery.

An actual API-fetched comment by a real GitHub user proves an attributable GitHub ACCOUNT authored a claim. A self-declared model/runtime string is not identity. The body claiming a source fetch is still a REPORT by that account; independently downloading the original source verifies source availability and bytes, not a proof that a particular autonomous model actually fetched it. Do not promote RECEIVER_FETCH_INDEPENDENTLY_ATTESTED without a separately justified independent witness. author_association is informative, not automatically an access grant; use trusted owner-approved receiver registry by stable numeric user IDs, rights/slot checks, not login substrings.

## 4. CURSOR: immediate bounded repair, no architectural redesign

Priority A — FIRST FIX WITNESS TRUTH AND DEAD DELIVERY PATH (M7/M1/M2/M9).
- Remove the vacuous or True assertion in original tests; establish real fail-first expected-delivered tests. AgentAdapter.declare remains DECLARATION, not transport readiness. Only transport provider proof with real request/delivery identifier and exact route may yield DISPATCHED; no connected provider => OUTBOUND_QUEUED. A local echo of source digest is not provider acceptance. Retain C1 no phantom dispatch.
- Implement verifier-owned GitHub REST fetch with pinned repository, exact issue or PR return slot, comment ID, actual issue_url/html_url grammar, authenticated numeric user ID and rights/owner registry. Reject foreign repository, unauthorized principal, owner token/account substitution and stale/replayed comments. A registered GitHub account is NOT a verified AI runtime.
- Treat all caller witness fields as untrusted hints only; no fallbacks for observed_sha256/observed_bytes/return_source_commit/return_source_sha256. Independently retrieve exact original commit/path blob and return artifact original bytes and recompute BOTH digests. Parse GitHub comment body into a structured signed-by-account **claim**, not as GitHub-provided independent byte witness. Bind task reference, nonce, source and return refs, origin and consent/rights.
- Make receiver status an evidence-labeled state machine: RECEIPT_SUBMITTED -> ACCOUNT_COMMENT_API_VERIFIED -> SOURCE_BYTES_INDEPENDENTLY_REHASHED -> RETURN_SOURCE_INDEPENDENTLY_REHASHED -> RECEIVER_REPORT_EVALUATED. Distinguish independent receipt of an account-authored claim from unproved actual runtime fetch. Do not move RECEIVED_BYTES_VERIFIED from caller data. Fix arbitrary forward jumps, replay/dedup, timestamp and contradictory newest-receipt status.

Priority B — TRUSTED OWNER / PRIVATE / DURABILITY (M3–M6, M8).
- Cutover requires actual source-pinned owner authority, platform-verified exact code CI/security/privacy/rights/rollback, and real transport capability. Never trust syntactically matching injected booleans/dictionaries, string true, or an unsigned free-text signer. On reboot recheck persisted ACTIVE and fail closed if stale.
- Private lanes require independently verified owner registry origin, real connected permitted private transport and content/rights classification; untrusted signer and filename heuristic cannot authorize raw private upload. Missing evidence = HOLD. Preserve public GitHub nonprivate-only lane.
- Repair duplicate-document idempotent replay rather than throwing sqlite3.IntegrityError; atomic receipt/state SQLite transaction, durable outbox/recovery of separate JSONL and SQLite, SIGKILL injection at every boundary and explicit reconciliation. Source/version/ID collisions must fail-closed, distinct from identical idempotent retries.
- Add real original-Python post-fix regression tests (F01–F15, X1–X8) whose PASS means the DEFECT IS FIXED, unlike this historical diagnostic suite; preserve both as distinct version-scoped artifacts. Run Windows/PowerShell plus Linux CI parity and negative mutations. No weakened R27E, no hidden owner token reuse, no unreviewed merge.

Priority C — actual independent receiving when legitimate capability exists.
- Test owner-governed GitHub code+slot with a distinct pre-authorized principal, verifying API response, linked exact refs, full byte witnesses and caller-nonce/replay. If no legitimate external receiver is installed, report EXACT_CAPABILITY_GAP, do not create new account, do not claim ACK ESTABLISHED, do not turn on Hostinger public POST.
- Keep STATIC WWW read-only live; V1 closed living. Public web route and document-router cutover are distinct.

## 5. Release thresholds and return

Minimum blocking negatives: forged self-claims cannot be promoted; foreign/missing/old comments rejected; actual GitHub issue-comment URL supported; unregistered/owner accounts cannot become independent; fake cutover or private registry fails; outbox/SQLite replay and fault injection have correct outcomes; DISPATCHED reachable only with actual verified provider acceptance, or accurately remains queued; return ref/bytes are independently rehashed; synthetic test fixtures never masquerade as live proof.

Do not reactivate the previously closed V1 architectural phase. This order is an **implementation execution mandate** scoped to the existing router and exchange chain, in governed PRs under the unchanged 100-file R27E cap. Return source-pinned implementation SHA, original bytes/sha, full test count, independent GitHub CI job IDs, actual authorized receiver/slot tests or clearly scoped gap, security/rollback evidence, source-only privacy review and Task Anchor Norm V1. No manual ZIP source ferry.

CURSOR_RETURN_OBJECT = NEXUS_OMEGA_CURSOR_MISTRAL_P0_ORIGINAL_PYTHON_HARD_REPAIR_RETURN_20261101_R0
SOURCE_ORIGINAL_COMMIT = 986b9af8f4bcfb341a188cbb6ed7d8da3d500e98
DIAGNOSTIC_RUN = 41270081586
DIAGNOSTIC_JOB = 124740888286
REPAIRED_NEGATIVE_TESTS = ACTUAL_COUNTS_AND_RESULTS
GITHUB_PRINCIPAL = ACTUAL_VERIFIED_ACCOUNT_OR_NOT_ESTABLISHED
REAL_AGENT_RUNTIME_IDENTITY = NOT_INFERRED_FROM_ACCOUNT
ACTUAL_SOURCE_BYTES = VERIFIER_REHASH_OR_NOT_ESTABLISHED
ACTUAL_RETURN_BYTES = VERIFIER_REHASH_OR_NOT_ESTABLISHED
CUTOVER_ACTIVE = NO_UNTIL_SEPARATE_OWNER_RELEASE_AND_EVIDENCE
EXTERNAL_AUTHENTICATED_ACK = NOT_ESTABLISHED_UNTIL_REAL_VERIFICATION
PUBLIC_WRITE_API = OFF
FRAMEWORK_V1 = CLOSED_LIVING
WWW_READ_ONLY = PRESERVE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_INDEPENDENT_REAL_P0_CODE_AND_RECEIVER_E2E_ADJUDICATION

This is a decisive code-and-tests repair task, not another free-standing research dossier. Execute all locally safe corrections and report precise unavailable capabilities only where actual external authorization is missing.
