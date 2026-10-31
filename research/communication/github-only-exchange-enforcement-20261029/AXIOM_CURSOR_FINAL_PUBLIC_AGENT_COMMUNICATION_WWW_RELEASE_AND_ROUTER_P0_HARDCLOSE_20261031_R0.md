# NEXUS OMEGA · AXIOM → CURSOR
## FINAL PUBLIC AGENT COMMUNICATION · WWW DEPLOY + ROUTER P0 HARD CLOSE · 2026-10-31

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_FINAL_PUBLIC_AGENT_COMMUNICATION_WWW_RELEASE_AND_ROUTER_P0_HARDCLOSE_20261031_R0
AUTHORITY = OPERATOR_ALEXANDER_EXPLICIT_FINAL_PUBLISHABLE_INTERFACE_REQUEST_20261031
PARENT = NEXUS_OMEGA_CURSOR_AGENT_COMMUNICATION_FRAMEWORK_FINAL_GATED_RELEASE_RETURN_20261031_R0
STATE = ACTUAL_STATIC_DEPLOY_AUTHORIZED_WITH_INDEPENDENT_WWW_WITNESS
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SITE = EXISTING_HTTPS_NEXUS_MOBILE_DE_AGENT_BORDER
TARGET = https://www.nexus-mobile.de/ai/agent-border/communication/
PUBLIC_EXTERNAL_WRITE_API = OFF
DOCUMENT_ROUTER_CUTOVER = HOLD_UNTIL_P0_PROVEN
GITHUB_ONLY_LAW_V2 = PRESERVED
NATIVE_APP_R3 = HOLD
PR185 = EXISTING_OWNER_DRAFT_NO_UNREVIEWED_AUTO_MERGE

## 1. Exact bound release assets (fetch from GitHub, do not request ZIP from Operator)

Repo: nexusomegac27/NEXUS-OMEGA-EVIDENCE
Directory: research/communication/github-only-exchange-enforcement-20261029/

A HTML source: NEXUS_AGENT_COMMUNICATION_PUBLIC_INTERFACE_V1.html
  COMMIT=697d58a4dba53a4a440fbd0c9a92da832ef56320
  BYTES=13521
  SHA256=1b9a7902b64bf8fd1059821d33bb7dab604194212ee14e2378090bd0ed1f6987
  DEPLOY_AS=/ai/agent-border/communication/index.html

B STATUS source: NEXUS_AGENT_COMMUNICATION_PUBLIC_STATUS_V1.json
  COMMIT=e3453102d52d6c8d3025f4252ef2befc5cd2374d
  BYTES=2624
  SHA256=9f613bf44c96bc6b37ab5020613a827454680f9ac9199d7f5bc925e8bbacc44d
  DEPLOY_AS=/ai/agent-border/communication/status.json

C PROTOCOL source: NEXUS_AGENT_COMMUNICATION_PUBLIC_PROTOCOL_V1.json
  COMMIT=4bd4814f22dcee54494f998eedd9f29a5cdd28a7
  BYTES=2417
  SHA256=8c5f45076e4b21607903c39a8b46b2d7bd1d923e70a7e775dec53802dfc26b51
  DEPLOY_AS=/ai/agent-border/communication/protocol.json

D TEST source: tests/test_nexus_agent_communication_public_interface.py
  COMMIT=4dedf89fb2c1c2b291e89f520e18c2a38dd86157

E CI source: .github/workflows/validate-agent-communication-public-interface.yml
  COMMIT=c2a42d4b3ce73b6506acada8b98fc2dbb5f71dff

Cursor must independently rehash each original and bind Task Anchor Norm V1. Do not substitute unstaged local files or mutable main. This release reuses existing page https://www.nexus-mobile.de/ai/agent-border/; no new domain, no parallel AEGIS/SFT, no new truth/privilege root.

## 2. Immediate static publication G0–G5 (actual execution required)

G0 READ BEFORE WRITE. Locate actual authoritative website source tree and Hostinger deployment route, Git remote, branch, rollback method and permission. Record on-disk site build hashes and live route inventory. Distinguish GitHub-Evidence commit, Hostinger deployment and independent WWW observation. Preserve existing canonical head, manifest, well-known, dissent and L00–L12+EXIT. No website rewrite.

G1 BUILD and DEPLOY the three source files under exactly the above target routes, using the existing managed site source and an atomic/reversible delivery. Integrate a small "Agent Communication" navigation link into the existing Agent Border without changing the Border's authority or style. Honor existing site CSS/CSP and no-third-party script rule; HTML release contains no JS and no form. Configure charset UTF-8, text/html for page, application/json for both JSON documents. Public GET/HEAD only. Do NOT enable public POST, webhook, hidden API, automated user account, GitHub external write, private material upload, runtime privilege or unsafe redirect.

G2 WEB LIVE TEST. Independently fetch the 3 WWW URLs (GET+HEAD) and compute SHA256 directly on actual HTTP response BODY bytes, compare deployed versions, capture timestamp, server status 200, Content-Type, cache, redirects, old/new source commit and Hostinger terminal evidence. Browser actual desktop and mobile, keyboard focus and reduced motion/JavaScript disabled, machine JSON parse, external links, page navigation and no script/form. Ensure all three relative links work from deployed directory. Browser/source screenshots are secondary to raw response bytes. Existing Border/manifest/canonical-head/well-known/dissent/L07/L10/L12 must continue unchanged or source-bound justified.

G3 STATUS VERACITY. Before observed live response, public status.release_state remains RELEASE_CANDIDATE_NOT_LIVE_CONFIRMED. Only after independent raw-byte/WWW/browser PASS may a versioned new status mark LIVE_READ_ONLY_CONFIRMED and note actual source/deploy UTC. Keep production_cutover_active=false, external_authenticated_return=NOT_ESTABLISHED, public_external_write_api=OFF, claim ceiling C1. Never advertise live bi-directional receipt from a static page.

G4 ROLLBACK. Preserve old route state and proof of an exact reversible restore, safe deploy failure path and smoke tests after restore. If deploy permission unavailable, return scoped WWW_DEPLOY_NOT_EXECUTED with actual evidence rather than claim URL is live. Do not ask operator to transfer website files manually.

G5 STATIC GATE. Execute new public-interface unittest in GitHub CI at actual final commit; all existing required CI separately checked. No assumptions from 11/11 at original router commit. If publication is public-safe, reversible, privacy-checked and source bound, perform the operator-requested static release without waiting for unrelated production API cutover.

## 3. P0 router hard-close — BLOCKS productive bidirectional activation but not isolated static page

Independent AXIOM code inspection at implementation commit 696dacf924300b1d32fe2384f43f95be891a7f0f exposed critical, concrete source paths:

P0-A: DocumentRouter.receive_receipt in scripts/nexus_document_router.py takes caller-controlled receipt.authenticated, receipt.return_source_verified, receiver_principal, receiver_process_id; can promote principal_verified and RETURN_SOURCE_VERIFIED from untrusted self-report. verify_receiver reports established on ok+bytes_match without independently reading actual GitHub author identity. REQUIRED: trust actual GitHub API authenticated author numeric ID, immutable comment/slot URL and receiver-fetch bytes proof; check producer != receiver; reject owner token reuse and synthetic PID spoof. Without actual verified receiver, ACK_NOT_ESTABLISHED. Add negative tests for authenticated=true forgery, false return-source boolean, fake GitHub comment, wrong path/commit/size, same-owner login, unauthorised writer.

P0-B: dispatch_document advances DISPATCHED after local journal.append despite ADAPTER_NOT_CONNECTED (source lines 575-612). REQUIRE: local outbound intent is STAGED/QUEUED, not sent. Advance SENT only on actual transport API witness. Separate source/read/receive/ACK; complete policy-defined state machine, no phantom delivery or return.

P0-C: --activate-cutover toggles persisted SQLite ACTIVE from a CLI boolean (constructor lines 439-441) without independently verifying required safety/privacy/CI/rollback/owner gates. REQUIRE: verified owner-approved activation manifest with pinned source+CI and signed/operator-gated review, enforce no ACTIVE on mere flag. Negative tests missing gates, fake approval, stale CI, loss of rollback; default STAGED.

P0-D: classify_source uses caller privacy class + filename heuristics; --allow-private-dispatch boolean can bypass explicit private route proof. REQUIRE fail-closed for unapproved private/PII/secrets/licensing; only actually connected owner-approved private lane with enforceable rights. No private content to public Evidence. No claim that pathname detects all private content.

P0-E: old test with foreign-looking process id does NOT prove distinct GitHub principal. Add actual signed/source API witness where possible, otherwise KEEP ACK NOT_ESTABLISHED. Real GitHub writer enrollment is a separately owner-authorized action, not implied by this order. Do not fabricate accounts or install apps.

Use actual negatives, disk recovery, source tests and provenance. No rewriting closed F10/F11/F12 without reproducible failure. Full code CI exact head. P0 corrections must be independently adjudicated before INTERNAL DOCUMENT ROUTER CUTOVER ACTIVE. An external public writable API remains OFF pending separate V3 security/authority grant.

## 4. Terminal Cursor return

OBJECT = NEXUS_OMEGA_CURSOR_FINAL_PUBLIC_AGENT_COMMUNICATION_WWW_RELEASE_AND_ROUTER_P0_HARDCLOSE_RETURN_20261031_R0
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
STATIC_SOURCE_COMMIT = actual full commit
SOURCE_REHASH_HTML_STATUS_PROTOCOL = 3/3 MATCH or exact failure
PUBLIC_HTML_WWW = PASS_WITH_REMOTE_SHA256 or NOT_EXECUTED_WITH_BLOCKER
PUBLIC_STATUS_WWW = PASS_WITH_REMOTE_SHA256 or NOT_EXECUTED_WITH_BLOCKER
PUBLIC_PROTOCOL_WWW = PASS_WITH_REMOTE_SHA256 or NOT_EXECUTED_WITH_BLOCKER
HTML_BROWSER_DESKTOP_MOBILE = actual E2E or NOT_EXECUTED
ORIGINAL_BORDER_REGRESSION = actual
HOSTINGER_DEPLOY_COMMIT_AND_ROLLBACK = actual source + terminal
P0_ROUTER_CODE_COMMIT = actual
FORGED_ACK_NEGATIVE = PASS or HOLD
DISPATCH_TRANSPORT_WITNESS = PASS or HOLD
ACTIVE_GATE_NEGATIVE = PASS or HOLD
PRIVACY_PRIVATE_NEGATIVE = PASS or HOLD
EXTERNAL_AUTHENTICATED_RECEIVER = NOT_ESTABLISHED unless independently verified
CUTOVER_ACTIVE = NO until source/CI/privacy/rights/rollback approved
PUBLIC_EXTERNAL_WRITE_API = OFF
PR185 = true review/merge status
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_INDEPENDENT_WWW_BYTES_AND_ROUTER_P0_ADJUDICATION

This order instructs actual WWW publication now if existing authorized reversible deployment permits; do not return only a design. The public static interface is not contingent on a future public WRITE API.
