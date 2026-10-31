# NEXUS OMEGA · AXIOM · Independent WWW Remote Bytes + Router P0 Adjudication · 2026-10-31 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_AGENT_COMMUNICATION_WWW_LIVE_REMOTE_BYTES_AND_ROUTER_P0_INDEPENDENT_ADJUDICATION_20261031_R0
PARENT = NEXUS_OMEGA_CURSOR_FINAL_PUBLIC_AGENT_COMMUNICATION_WWW_RELEASE_AND_ROUTER_P0_HARDCLOSE_RETURN_20261031_R0
SOURCE_COMMIT = de25a94c361514a896b8a1c1cc33cd04f17cb33f
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_WWW_READ_ONLY_REMOTE_BYTES_VERIFIED_ROUTER_P0_PARTIAL_NOT_FINAL
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
WWW_PUBLIC_READ = CONFIRMED_3_OF_3_REMOTE_BYTES_SHA256_MATCH
DOCUMENT_ROUTER_P0_FULL_SECURITY_SEAL = NOT_ESTABLISHED
CUTOVER_ACTIVE = NO
EXTERNAL_AUTHENTICATED_ACK = NOT_ESTABLISHED
PUBLIC_WRITE_API = OFF
PR185 = OPEN_DRAFT_NOT_MERGED
NATIVE_APP_R3 = HOLD
```

## A. Independent evidence

Primary GitHub repository: nexusomegac27/NEXUS-OMEGA-EVIDENCE. PR185 source HEAD `de25a94c361514a896b8a1c1cc33cd04f17cb33f` (at first intake), actual parent `ac4d9e680956d787ba1933463181490b6d208ddf`; 11/11 GitHub check-runs completed SUCCESS at that exact commit, including Semgrep, static public interface, structural validation, research-pipeline validation, Check-in and R27E structural firewall.

Github source result: `research/communication/github-only-exchange-enforcement-20261029/RESULT_FINAL_PUBLIC_AGENT_COMMUNICATION_WWW_RELEASE_AND_ROUTER_P0_HARDCLOSE_20261031_R0.md` at pinned commit. It reports Hostinger scoped SCP deployment, rollback rehearsal PASS, desktop browser PASS and remote WWW hashes. This report is Cursor source evidence, not AXIOM's own Hostinger terminal readback.

**Independent web view:** public rendered HTML, `status.json`, `protocol.json` accessible via external read-only extraction; first web.open and local container DNS lacked capability, not evidence of HTTP 404. A second independent vantage was created via GitHub Actions runner:
- new first-party verification code `.github/workflows/verify-agent-communication-www-remote-bytes.yml` commit `174a3e226cd5962c275aaf29379b6dacfbb0e2e0`
- GitHub run `41224585554`, job `124605976802`, SUCCESS.
- actual remote HEAD and GET witnessed at 2026-10-31T17:27:09–11Z, `www.nexus-mobile.de`, status HTTP 200 for all 3, content types text/html/application/json:
  - `/ai/agent-border/communication/`: 13521 bytes; SHA256 `1b9a7902b64bf8fd1059821d33bb7dab604194212ee14e2378090bd0ed1f6987`; MATCH immutable HTML original.
  - `/ai/agent-border/communication/status.json`: 3230 bytes; SHA256 `3e6d6d46297a46fa11e1b7de08ec8ab66af0eddc8aac48e8d58389da6fe62707`; MATCH live status from Cursor return.
  - `/ai/agent-border/communication/protocol.json`: 2417 bytes; SHA256 `8c5f45076e4b21607903c39a8b46b2d7bd1d923e70a7e775dec53802dfc26b51`; MATCH immutable protocol original.
- raw HTTPS witness is an independently executing GitHub-hosted CI runner, still not a separate trusted human auditor, browser screenshot proof or pen test. Its GET/HEAD assertions and JSON invariants pass.
- `status.json` declares `release_state=LIVE_READ_ONLY_CONFIRMED`, `production_cutover_active=false`, `public_external_write_api=OFF`, `external_authenticated_return=NOT_ESTABLISHED`. Protocol also explicitly denies POST, PUT, PATCH and DELETE. Never infer actual security from a declaration alone.
- dedicated `router-p0` source workflow `.github/workflows/validate-agent-communication-router-p0.yml` commit `a179752df020fa4fc819258ce6c0497aa1cffe9f`, run `41224663584` job `124606210140`, SUCCESS, logs `Ran 22 tests in 0.306s` and `OK`. This validates the existing unit tests on a real GitHub Actions checkout, not all untested adversarial conditions.

## B. Positive Router P0 improvements evidenced in exact source

At original Cursor commit, `scripts/nexus_document_router.py`:
- `receive_receipt` ignores untrusted plain `receipt.authenticated` and `receipt.return_source_verified` booleans, and requires a separate `github_api_witness` data object to mark principal status.
- `dispatch_document` correctly records `OUTBOUND_QUEUED` for local journal-only intent, and leaves `ADAPTER_NOT_CONNECTED` marked not delivered in regular cases.
- `--activate-cutover` cannot set ACTIVE without a syntactically valid activation manifest (explicit boolean alone fails).
- `OWNER_GOVERNED_PRIVATE` cannot pass solely through `--allow-private-dispatch`; an additional `private_lane_proof` structure is required.
- 22 unit checks pass; positive contribution ACCEPTED_C1 at code level.

## C. Residual critical P0 findings: original code inspection, not a production exploit

**F1 — receiver identity remains SELF-ASSERTED in witness data.** `verify_github_receiver_witness` lines approx 271-352 solely checks fields supplied in `receipt.github_api_witness`: `author_id`, `author_login`, `immutable_url`, `observed_sha256`, `observed_bytes`, and the literal `api_attestation == GITHUB_REST_VERIFIED`. It does NOT call GitHub REST API, query the immutable comment/author, verify receiver-side byte fetch independent of submitter, or compare author ID against an authorized rights register. A fabricated witness containing the correct known source SHA/length and non-owner-looking author can satisfy the code's `principal_verified`. Adding string `return_source_commit` + `return_source_sha256` can mark RETURN_SOURCE_VERIFIED without retrieval or path-binding. This is a concrete deterministic code-path vulnerability, NOT evidence of an actual attacker or external agent POST. Keep all external actor/ACK promotions HOLD until a trusted independent GitHub API verifier is integrated. In a local isolated test with a fake GitHub client, reject a forged self-authenticated witness.

**F2 — verify_receiver still elevates hash only.** `verify_receiver` lines approx 1011-1040 assigns `ESTABLISHED_REPORT_LEVEL` when stored receipt `ok` and `bytes_match` are true, even if `principal_verified=False`, `return_source_verified=False`, `github_witness.ok=False`. This contradicts new `receive_receipt`'s stricter status and creates inconsistent representations. Fix both to use the same trusted, source-bound verifier; never use a duplicated heuristic.

**F3 — cutover manifest attests its own approval.** `validate_cutover_activation_manifest` lines approx 235-268 checks user-provided `owner_approval:true`, four values `PASS`, a 40+ char commit and a syntactically valid 64hex order SHA. It does NOT independently check these values against true owner authorization, GitHub CI source commit, privacy review or rollback witness. Any local caller with access to CLI can craft a formally passing manifest; if cutover is an operator-only local command this is not itself a public remote exploit, but the advertised irreversible production authority gate remains unsigned/unverified. Real cutover remains OFF. Require source-pinned approved owner receipt, API-checked repository protection/CI and verified gate manifest before activation.

**F4 — private lane proof attests its own rights.** `_valid_private_lane_proof` lines approx 170-202 checks caller-provided `proof_kind`, `owner_approved:true`, `connected:true`, and an allowed `rights_scope` string. It does not resolve the actor/lane against trusted owner registry or validate the actual configured private transport. Filename heuristics and caller-declared privacy class are not sufficient to classify sensitive data. Therefore owner-governed private automated handoff still requires a trusted route registry and source/rights review; do not put private bytes in public GitHub.

**F5 — transport/API witness itself currently looks caller supplied.** `dispatch_document` checks `transport_witness.api_attestation == TRANSPORT_API_VERIFIED` and bytes/hash against prior source, but does not independently read provider API delivery within that method; also needs `adapter_status != ADAPTER_NOT_CONNECTED`. Under future untrusted input, this permits an asserted transport witness; until actual provider API evidence, OUTBOUND_QUEUED is the reliable state. A retrievable public GitHub source is different from dispatched delivery.

**F6 — WWW published copy contains a minor status-text mismatch.** status.json now declares LIVE_READ_ONLY_CONFIRMED, while protocol.json still says RELEASE_CANDIDATE_NOT_WWW_VERIFIED and HTML text still speaks of being a release candidate. This is public metadata drift, not a blocker to basic read-only access. Cursor should update immutable site source + deploy versioned, rehash and retest in the next scoped static update; do not silently edit live with no new hash.

## D. Adjudication

WWW RELEASE / PUBLIC READ = C1_CONFIRMED_ACTUAL_REMOTE_BODY_SHA_MATCH for 3 routes, no accounts. Old Agent Border entry remains a separate first-party route; full browser viewport or Hostinger terminal rollback independently by AXIOM still not witnessed and retains report-level caveat. No need to undo public static deployment because an internal document router is not yet proven.

DocumentRouter P0 = PASS_WITH_MATERIAL_CAVEATS_SOURCE_AND_UNIT_TESTS, **NOT P0_FINAL_SEALED**. There is a clear difference between blocking simple self-attested fields and authenticating an actual GitHub writer. The latter requires independent fetch of actual GitHub return artifact plus rights-bound verified principal. Full document transport CUTOVER remains STAGED. Public writable API remains OFF. Prior MISTRAL/VIBE and GLM/Z.ai returns remain operator-mediated scientific observations, not independent authenticated AGENT_ACK.

Recommended next: one narrow owner-governed Cursor repair that connects true GitHub REST author/comment/source bytes verifier, consolidates receipt status, binds activation approvals to trusted owner/CI/rollback and private lane to trusted registry; rerun negative fixtures. Static status metadata drift can be repaired in parallel, with actual WWW deploy receipt and matching new remote bytes. Then AXIOM independent review. No new worldwide architecture, new agent accounts, public POST or V3 enactment.

```text
WWW_READ_ONLY = CONFIRMED_REMOTE_SHA256_3_OF_3
WWW_GET_HEAD = HTTP_200_3_OF_3
PUBLIC_STATUS = LIVE_READ_ONLY_CONFIRMED
PR185_ORIGINAL_CURSOR_HEAD_CI = 11_OF_11_SUCCESS
CURSOR_P0_UNIT_SUITE = 22_OF_22_GITHUB_ACTIONS_PASS
DOCUMENT_ROUTER_P0_FULL_CLOSURE = HOLD_F1_TO_F5
PUBLIC_TEXT_VERSION_DRIFT = CAVEAT_F6
CUTOVER_ACTIVE = NO
EXTERNAL_ACK = NOT_ESTABLISHED
PUBLIC_EXTERNAL_WRITE_API = OFF
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = CURSOR_TARGETED_TRUSTED_SOURCE_P0_CLOSE_AND_DYNAMIC_RETEST
```
