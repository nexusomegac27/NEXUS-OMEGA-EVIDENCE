# NEXUS OMEGA · R31 BodyTwin Scientific Live + Autonomous Verified Publication · One-scoped Cursor MAXI Order

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R31_BODYTWIN_SCIENCE_LIVE_AND_AUTOPUBLISH_BOOTSTRAP_MAXI_ORDER_20261116_R0
DATE = 2026-11-16
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
GOAL = ONE_TIME_SAFE_BOOTSTRAP_THEN_NO_PER_RELEASE_MANUAL_TRIGGER_FOR_PREAUTHORIZED_C1_PUBLIC_METADATA
PARENT_R31 = NEXUS_OMEGA_AXIOM_R31_FRAMEWORK_WIDE_PUBLICATION_RECONCILIATION_20261116_R0
PARENT_PR = nexusomegac27/NEXUS-OMEGA-EVIDENCE#362
PARENT_PR_FROZEN_REVIEWED_HEAD = 35d65dd727fa0c5046f1348a13473f00c2529577
PARENT_R31_STAGING_INDEPENDENT_CUSTODY = ORIGINALS_STILL_MISSING
R30 = CLOSED_C1_PRESERVED
FRAMEWORK_RESEARCH_ROUND = NO_NEW_ROUND
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
TRUTH_AUTHORITY = NONE
OPERATOR_DIRECTIVE = SCIENTIFIC_BODYTWIN_LIVE_STAND_AND_AUTOMATIC_FUTURE_UPDATES
NO_C1_TO_C2_AUTOPROMOTION = HARD
NO_PRIVATE_RAW_SENSOR_OR_PATIENT_DATA_PUBLICATION = HARD
NO_OPPO_ADB_CAPTURE = HARD
NO_PIXEL9A_ACTIVATION = HARD
NO_AUTO_EXTERNAL_AGENT_WRITE = HARD
NO_AUTO_GITHUB_PR_MERGE = HARD
NO_AUTO_SHARED_ROOT_REWRITE = HARD
NO_UNVERIFIED_MODULE_TO_PRODUCTION = HARD
RETURN_COUNT = ONE_TERMINAL
CURSOR_AUTOSTART_BY_GITHUB_PR_CREATION = NO

## A. Why this must be delivered now; not another research or receipt loop

Direct C1 WWW content fetch on 2026-11-16:
- `/bodytwin/`: symbolic SO(4) viewer and existing progress module available.
- `/bodytwin/updates/`: five dated entries, last 2026-11-14.
- `/bodytwin/updates/events.json`: historical `published_live=false` author-time candidate flag (do not rewrite it retrospectively).
- `/bodytwin/live/current.json`: `producer.seq=2550`, `run_utc=2026-11-16T17:15:03Z`, `interval_seconds=300`, `source_changed=false`, `last_change_utc=2026-11-07T20:50:02Z`, `bodytwin.validated=NO`, `consent=OPEN`, `trial=DESIGNED_NOT_EXECUTED`.
- `/research/bodytwin/state.json`: `BODYTWIN=RESEARCH_FOUNDATION_C1`, `BODYTWIN_VALIDATED=NO`, `CONSENT_BIND=OPEN`, `TRIAL_001=DESIGNED_NOT_EXECUTED`.

**Critical source-level dependency finding:** Existing `research/bodytwin-r13/live-update-v1/site/live-core.mjs` at PR#324 HEAD `93190d5ad6fa972fddd46b05ecd8f25408a7a70e` requires exact v1 keys, the frozen R14 `source_object`, fixed source-date and 2 source digests; Python/PHP Hostinger reducer validates same fixed state/receipt schema. A naïve attempt to add R18–R31 fields or change `source_object` in `/bodytwin/live/current.json` will be REJECTED by the existing page (SCHEMA_KEYS/RESEARCH_PROVENANCE). Do NOT destroy or silently bypass this safety invariant. **Add a separate versioned scientific release lane.**

Scientific gap: R13/R16/R17/R18/R19/R20/R21 have been studied but not accurately reflected in WWW science chronology. R31 research auto-sync is offline-tested 37/37 at reviewed PR #362 commit; the separately reported SQLite staging originals are not independently in AXIOM custody, so do not claim the real framework outbox already installed.

## B. Pinned science census — provenance, classification, no false validity

Use source exactly from THIS scoped public candidate PR under `research/r31/bodytwin-science-autosync-20261116/`:
- `data/bodytwin_science_source_census_20261116_R0.json` (nine source-linked, public-safe dated events; source derived as candidate, not independently cryptographically authorized)
- `data/bodytwin_auto_publication_policy_v1.json` (two lanes and explicit versioned route allowlist; candidate policy is NOT a signed production release)
- `src/render_science_snapshot.py` (pure deterministic Python stdlib renderer; no network or website write; reads curated data)
- `tests/test_science_snapshot.py` and `.github/workflows/r31-bodytwin-science-autosync-c1.yml` (offline defensive checks)
- THIS order plus a separate research+operations crosswalk.

Mandatory C1 source distinctions:
1. R13 research bridge `SOURCE_CANDIDATE`; A72 originals gap and R13 Stage II hold preserved; 31/31 reference checks ≠ WWW success.
2. R16 reconstructed Q0 reference harness 20/20, **not** production viewer.
3. R17 OPPO-to-BodyTwin coupling architecture: 8 expert areas and 10 rounds designed, NOT actual same-day physical research returns.
4. R18 anatomical static add-on: source report of 203 skeleton/88 musculature etc, not fully integrated/rights-cleared/HTTP-GPU-verified; no use of raw image assets in science release.
5. R19 initial anatomy/biomechanical/visual research synthesis; eight expert orders do not imply eight independent completed experimental findings.
6. R20 source/legal/scientific design; BodyParts3D original/derivative license conflict remains HOLD until per-asset license/copyright provenance signed; no automatic inclusion of models.
7. R21 **later** OPPO physical trial (PR #351 inheriting reported PR #350 capture): Cursor-reported 14,018 accel+gyro events over 70,114 ms, ORIGINAL PRIVATE BYTES NOT RECEIVED/INDEPENDENTLY REHASHED HERE. Accurate public text = `PHYSICAL_CAPTURE_PRODUCER_REPORTED_NOT_SECOND_PARTY`; never `measured whole-body pose`, `clinical`, `sensor live` or `confirmed raw dataset`. PR#350 closed/superseded research mandate by PR#351 but does not erase original reported capture event; no private data/IDs/locations publicly rendered.
8. R31 source-only publication reconciliation 37/37 corrected offline tests, 9/9 checks as of HEAD 35d65dd; ZCode/GROK static adjudication report-bound, NO production outbox/witness signature/host runtime; `ALL_RECONCILED` with drift is prohibited, use `WWW_OBSERVED_METADATA_DRIFT_OPEN` when that exact condition exists.
9. Existing symbolic viewer baseline remains a historically displayed metaphor, not scientific body-anatomy truth.

To avoid a false denominator, report *verified original bytes*, *GitHub-source bytes*, *Cursor-reported measurements*, *independently executed tests*, *designs*, and *WWW-observed content* as separate fields. If a specific original is missing, show the honest C1 limitation in the public report rather than suppressing the entire topic.

## C. One-time public architecture — render once, automatically update thereafter

New stable public routes:
- `/bodytwin/science/` -> generated accessible static HTML from approved public-safe science manifest.
- `/bodytwin/science/current.json` -> corresponding generated C1 metadata content, never a fabricated publication witness.
- `/bodytwin/science/releases/<CONTENT_DIGEST>/` -> immutable archived release and raw manifest, only if host filesystem capability validated and content digest safe.
- Optional separate `/bodytwin/science/release-witness.json`: **new** independently verified witness receipt; do not modify historic `/bodytwin/updates/events.json`.

Insert ONE scoped science link/accessible panel in original `/bodytwin/` at a tested location AFTER the existing 4D controls, not inside interactive 4D coordinate layout. Prefer a permanent simple link + plain C1 status text to eliminate new CSP/script dependency. If a richer read-only component is used, enforce same-origin GET/no cookies, strict schema, stale/rollback guard, accessible no-JS link fallback. Do not rewrite the original six SO(4) controls, five projections, 4D styles, existing P0 layout hotfix, `/bodytwin/live/current.json` or its 300s cron.

Initial science snapshot is a **publication CANDIDATE**. Do not imply live until scoped Hostinger release and independent after-write witness PASS.

## D. G0 preflight: exact owner-host capability and safety

1. Cursor independently rehashes GitHub source and current Hostinger `/bodytwin/index.html`, original viewer.js, all current /updates assets and 300s current.json; source SHA256 and byte counts in machine receipt. No guessing from the Nov 15 public index hash `69f3a5cf08fe7eb4ae602c2105aa2696c378e486e9587db8ef376a4e5e395a66` if live bytes changed.
2. Check Hostinger hosting mode (VPS vs shared), available Python3/PHP CLI, Cron, locking/fsync/atomic rename, TLS, outbound GET, existing R13 feed Cron identity, dedicated nonpublic backup directory and least-privileged publish principal. No cleartext credentials in return; no assumptions about root access/systemd/webhooks.
3. Record currently running script and schedule for R13 feed. Do not create second producer or mutate existing v1 reducer. Identify conflicts with present root layout/other Cursor jobs, especially public write-surface ownership.
4. Verify snapshot source registry with actual immutable GitHub commits, public-safe text, approvals and DLP. Do NOT present the authored snapshot as independently accepted science itself; retained source-status caveats must appear in every derived format.
5. Reconcile historical PR #361 WWW release as existing public deployment. GitHub Draft/Merge state is distinct from live remote state. No automatic merge.

## E. G1 Offline science release: deterministic render, contract and XSS defense

Run `python -m unittest discover -s research/r31/bodytwin-science-autosync-20261116/tests -p 'test_*.py' -v` against exactly the installed commit. Generate the two files from `src/render_science_snapshot.py` into a disposable staging directory, twice; both raw SHA256s MUST match.

Compare rendered HTML/text with source census, check date, C1 disclaimers and all nine events; check URLs/allowlist, HTML escaping, no private data, no third-party JS, no unsafe `innerHTML`, no external fonts, no iframe, no API keys, no metadata inflation. Preserve the original snapshot and its hash as a historic candidate. The pure renderer is not a release signer or server runtime.

Any negative tests failing -> `HOLD_C1_RENDERER_SECURITY` with source-exact counterexample, not public deployment.

## F. G2 Publish FIRST version of science snapshot — one reversible scoped update

Operator's request explicitly authorizes *the goal* of a public-safe BodyTwin update; real rights/credentials must come from existing authorized Cursor/Hostinger operator scope. Only if G0/G1 PASS, perform one staged, reversible public metadata release:
- DLP-clear, freeze candidate release_id, source SHA and exact output digests and paths.
- Stage immutable release files and standalone `/bodytwin/science/index.html` + `current.json`; preserve previous good. Root `/bodytwin/` gets only the one-time, namespaced link/component. Verify previous HTML is revertible byte-for-byte; backup in nonpublic location.
- Apply via existing operator-authorized SCP/SFTP/Hostinger flow, atomic temp+rename within same filesystem and content-addressed manifest; pointer/index last. Never use `git merge` as proof.
- Independently observe response raw SHA256 and byte counts, HTTP 200, Content-Type and cache behavior for `/bodytwin/science/`, `current.json`, `/bodytwin/`, v1 `current.json`; browser acceptance of 4D viewer+live panel+science link at 320, 390, 768, 1280 and browser Back/Forward.
- If SHA/status/MIME/CSP/dom regression fails, rollback exact old root and pointer, record source-exact `ROLLED_BACK_FAIL_CLOSED`. Content-source hash != HTTP compressed representation byte hash; distinguish decompressed entity body from wire encoding/Content-Encoding.
- The old static `/bodytwin/updates/events.json` field `published_live=false` remains untouched. Instead record **new independent post-deploy receipt** with actual raw SHA/time and version to avoid false historical source rewriting.
- R13 v1 Feed must remain `validated=NO,consent=OPEN,trial=DESIGNED_NOT_EXECUTED`; feed seq advancement independent of scientific content.

A public C1 update may be deployed even while unrelated R31 private staging-original custody is pending, provided **this** bounded science-publication path has its own fully verified security, consent/privacy, rollback and independent HTTP/DOM gates. Do not convert a separate R31 outbox-source gap into an indefinite global freeze, nor misrepresent it as closure.

## G. G3 Autonomous release trigger and acceptance — NO repeated manual launch

User explicitly rejects hand-triggering each approved publication. Implement a **one-time operator-approved standing POLICY** limited to these *metadata routes and science topic*. The policy JSON in this PR is only a design candidate and NOT self-signed authority. Formal bootstrap must record a genuine owner-controlled authorization bound to: allowed routes, permitted content types, named signing and independent-review roles, expiration/revocation, max release size, rollback privileges, key lifecycle, no new Code/RAW sensor routes. After one-time authorization, each later eligible **independently reviewed** C1 public-safe science event should flow automatically without operator initiating another deploy.

Event pipeline:
```
SOURCE_ORIGINAL_HASH_BOUND
 -> INDEPENDENT_SCIENTIFIC_ADJUDICATION_C1
 -> DLP/LICENSE/PRIVACY/CLAIM_CHECK
 -> preauthorized owner-signed route policy + immutable release manifest
 -> SQLite WAL transaction: release + outbox event atomic
 -> authenticated webhook wake, de-duplicate X-GitHub-Delivery
 -> bounded 300s anti-entropy worker queries ALLOWLIST only
 -> render same source into HTML+JSON with stable content digest
 -> stage/canary + bounded tests + immutable copy + rollback
 -> exact remote post-deploy HTTP response witness by separate principal
 -> RECONCILED iff no residual drift; otherwise HOLD with alert
```

For webhook authenticity, verify GitHub `X-Hub-Signature-256` over **original raw payload bytes** (not parsed/reserialized JSON), timing-safe comparison, HTTPS, event-type and repo allowlist, delivery UUID idempotence. ACK only after durable queue commit. Retry with bounded exponential backoff+jitter; last-write/sequence conflict -> HOLD and no overwrite. CloudEvents `id+source+type+time` namespace for portable events; no unsigned self-declared model/provider identities as trust authorities.

For source trust, a public PR/draft, a green CI result or a chat phrase `VERIFIED` must NOT create an authorized release. Require actual immutable source digest, verified independent review receipt, nonexpired operator policy signature and bounded public route digest. On initial bootstrap, Cursor must implement secure signer/identity verification with an owner-controlled secret store (not hardcoded HMAC test keys), or return `HOLD_AUTHENTICATED_RELEASE_TRUST`; never silently fall back to test fixtures.

Hostinger active availability:
- Prefer **existing** Hostinger capability proven by the v1 300s producer, with an independent science worker and separate lock/DB. Never substitute GitHub Actions `schedule` for authoritative 300s durability: GitHub scheduled workflows may be delayed/disabled and run on default branch only; use GitHub Actions as optional independent read-only secondary monitor.
- Webhook optional if inbound handler cannot be securely hosted; **300s anti-entropy pull** of protected, signed release index MUST still automatically discover new authoritative events. No per-release operator trigger.
- If SQLite worker cannot be safely installed on host, use authorized Hostinger VPS relay or external secure worker meeting same contract; do not publish brittle cron scripts that blindly fetch GitHub `main`/unreviewed source.

## H. G4 Modules and dependencies — automatic integration with scoped prudence

**Two distinct deployment lanes**:
1. `SCIENCE_METADATA_C1`: after authenticated public-safe adjudication and the once-bound operator route policy, automatic publish/reconcile is the DEFAULT. A report-level finding remains labeled `CURSOR_REPORTED` or `OPEN`, not promoted to independently proven measurement. No repeated manual action for each later C1 release.
2. `VERIFIED_CODE_MODULE`: new renderer, UI widget, physics engine, Android reader or anatomy asset has a **different** pipeline: exact source/lockfile, reviewed dependencies/licensing, independent tests incl negatives, browser mobile/performance, DLP, staging/canary, rollback and explicit applicability to a preapproved code deployment allowlist. Without a preapproved reversible policy, return `HOLD_OPERATOR_SCOPE`, not a self-signed authorization. Real device/health/identity/irreversible changes always need separate explicit authorization. Preapproved low-risk modules may be released automatically only if all code gates are materially established; never infer that automatically from C1 science.

Store a clear module provenance ledger with `candidate_sha`, `tests_run`, `requirements`, `previous_good`, `observer_receipt`, `status`. No mass fanout of a BodyTwin update into Forum/ORBIS/Astra/Internal. Each target route must be allowlisted and subscribe to the event topic. Preserve Air-Gap.

## I. G5 Falsification matrix / real reliability before declaring AUTOMATED

Freeze one adversarial and positive battery before execution. Minimum:
F01 forged webhook HMAC; F02 replayed delivery UUID; F03 event reorder; F04 source SHA mismatch; F05 unsigned self-approved source; F06 expired/revoked owner policy; F07 unexpected route or topic; F08 sensitive raw OPPO sample in release; F09 changed anatomical asset license; F10 source metadata changed without source event; F11 source heartbeat advanced with no science SHA change; F12 crash between DB release and outbox insert; F13 crash after commit before HTTP ACK; F14 double Cron invocation / lock collision; F15 stale/corrupt last-good pointer; F16 200 HTTP wrong content hash/MIME/compressed-body distinction; F17 Browser regression at 320/390/768/1280; F18 independent observer report conflict; F19 remote rollback/same-seq digest equivocation; F20 unverified code module attempts auto-release.

Each test requires frozen stimulus+oracle, actual evidence+exit/HTTP/DB row, PASS/FAIL/NOT_RUN, user/security side-effect log. **The 28 renderer tests and old R31 37 synthetic reducer tests DO NOT COUNT as F01–F20 live system trials.** Run positives (legitimate append, duplicate idempotency, re-delivery, explicit rollback, manual route HOLD) in the same bounded lab.

Predeclared pilot metrics (targets only until measured):
- Coverage of eligible (event, route) pairs = 100% in controlled test corpus.
- Unauthorized public release = 0 in negative controls.
- p95 from actual authenticated adjudication to independently observed WWW = <15min in pilot (not a guarantee).
- Last real science content change separately from latest 300s worker heartbeat.
- No 4D regression; no source-v1 schema regression; no personal data or rights violations.
- Real automatic release without manually starting per-event work after one-time service authorization.

Observe at least two separately approved synthetic/public-safe metadata releases through the **full** automated pipeline, one negative and one recovery scenario; otherwise `R31_AUTOSYNC_RUNTIME_NOT_ESTABLISHED`. Test repeated real source no-op: renderer must not publish repeatedly on identical digest.

## J. G6 Reliability under degraded services

- GitHub webhook down -> polling finds missing event within configured anti-entropy window.
- Polling source unavailable -> retain last witnessed content, bounded retries, public surface displays last independent source date and `SYNC_DEGRADED`, not fake `LIVE_UPDATED`.
- All remote writes fail -> no publication promotion; queue persists with error class; page remains last good; alert without spamming.
- Observer unreachable -> `WWW_OBSERVED_PENDING`, not `RECONCILED`; independent observer catch-up later.
- Hostinger reboot/WAL recovery -> SQLite integrity check + transaction outbox and monotonic sequence, no duplicate effects.
- Renderer or schema v2 invalid -> do not compromise strict v1 feed; candidate quarantined.
- Repo/branch changes -> pinned immutable commit+source SHA enforced; never treat moving `PR362_HEAD` as a historic source commit.
- Remote publish already written but witness failed -> recheck actual bytes then rollback or classify `UNVERIFIED_SITE_LIVE`; never silently erase valid public content with an unverified historical state.

## K. G7 CI and workflow operationalization

- Existing PR#362 R31 baseline source remains pinned/frozen for its historic reviewers, not rewritten; this scoped science integration is a separate implementation PR under R31, NOT R32.
- GitHub Actions `pull_request` must prove offline renderer tests and deterministic output for the **exact new PR head**; CI has `contents:read`, no hosting secrets. A green PR check ≠ hosting activation.
- For future event triggers, use a protected authoritative release ledger/ref and least-privilege workflow dispatch to the authenticated worker. Avoid relying on PR webhooks alone because PRs do not certify scientific review.
- One owner-admin installs scoped webhook secret/worker credentials (nonpublic, rotated), starts exactly ONE outbox worker, registers scheduler/health-check in ops manifest and proves it resumes after reboot. Record service identity, process PID/job ID, schedule and revocation/kill-switch. No self-proclaimed persistent AI agent.
- GitHub scheduled workflows, if used for secondary monitoring, activate only on the DEFAULT BRANCH, may be delayed and can be automatically disabled after 60 days public-repo inactivity; not a sole automation guarantee.
- Automatic website updates must have an unambiguous typed ACK to NEXUS: `AUTOMATED_DEPLOY_STARTED`, `WWW_OBSERVED`, `RECONCILED` OR `HOLD_<CAUSE>`. Include all expected route versions and receipt digests.

Primary official specifications: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
https://slsa.dev/spec/v1.2/build-provenance
https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
https://theupdateframework.io/docs/security/
These are technical design sources, NOT certificates already possessed by NEXUS.

## L. One terminal machine return: actual delivered website + automation status separately

```text
OBJECT = NEXUS_OMEGA_CURSOR_R31_BODYTWIN_SCIENCE_LIVE_AND_AUTOPUBLISH_BOOTSTRAP_RETURN_20261116_R0
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_R31_BODYTWIN_SCIENCE_LIVE_AND_AUTOPUBLISH_BOOTSTRAP_MAXI_ORDER_20261116_R0
STATE = BODYTWIN_SCIENCE_LIVE_C1_AUTOSYNC_PILOT_PROVEN
      | BODYTWIN_SCIENCE_LIVE_C1_AUTOSYNC_GATE_PENDING
      | HOLD_VERIFIED_SECURITY_OR_SOURCE_BLOCKER
      | ROLLED_BACK_FAIL_CLOSED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R30 = CLOSED_NO_REOPEN
BODYTWIN_R13_V1_FEED = PRESERVED | REGRESSED
SNAPSHOT_CANDIDATE_RAW_SHA256 = <exact>
SOURCE_BRANCH_SHA = <40hex>
RENDERER_TESTS = <actual passed/total>
AUTOPUB_F01_F20 = <actual run/20, separate to old R31>
SCIENCE_LIVE_ROOT = 200_AND_BROWSER_PASS | NOT_OBSERVED | FAIL
SCIENCE_LIVE_CURRENT_JSON = 200_SHA_MATCH | NOT_OBSERVED | FAIL
RESEARCH_EVENTS = <actual new count>
R21_PHYSICAL_ORIGINAL = NOT_SECOND_PARTY | MATCH | NO_SOURCE
R18_ANATOMY_RIGHTS = HOLD_UNCLEARED | VERIFIED_PER_ASSET
ONE_TIME_SCIENCE_MODULE_ENTRY = PASS | HOLD
AUTO_RELEASE_OPERATOR_POLICY = INSTALLED_SCOPED_SIGNED | NOT_INSTALLED
OUTBOX_ATOMICITY = PASS_LIVE_STAGING | CURSOR_REPORTED | NOT_RUN
CRON_POLLING = ACTIVE_VERIFIED | NOT_STARTED
WEBHOOK_WAKE = AUTHENTICATED_PASS | OPTIONAL_NOT_INSTALLED | FAIL
OBSERVER = DIFFERENT_PRINCIPAL_RAW_SHA_MATCH | NOT_ESTABLISHED
SCIENCE_RELEASE_1_AND_2_AUTOMATED = PASS | NOT_RUN
CONTENT_CHANGED = YES_ONLY_IF_SIGNED_RELEASE_DIGEST_CHANGED | NO
BODYTWIN_VALIDATED = NO
CONSENT_BIND = OPEN
TRIAL_001 = DESIGNED_NOT_EXECUTED
OPPO_CAPTURE_NEW = NO
HOSTINGER_SCOPE = /bodytwin/science/* + ONE_TIME_ROOT_LINK_ONLY
GITHUB_MERGE = NO
PUBLISH_RECEIPT_SHA256 = <full or NOT_EXECUTED>
ROLLBACK = READY | TESTED | EXECUTED
NEXT = INDEPENDENT_AXIOM_C1_ADJUDICATION_NO_NEW_LOOP
```

Do not report `AUTO_RELEASE=PROVEN` after a single manual upload or after seeing the existing R13 cron ticks. A safe terminal may be `BODYTWIN_SCIENCE_LIVE_C1_AUTOSYNC_GATE_PENDING` if the publication page was verified but authentic signer/worker/outbox were not; that is useful progress with a precise remaining dependency, not a research loop.

## M. Non-compensatory last word

A valid cryptographic digest says *which bytes*; an independent scientific review says *what that evidence supports*; a release signer authorizes *where* public metadata may go; the website witness proves *what was served*; a periodic worker guarantees only *attempts* until actual uptime, recovery and coverage are observed. Never turn any one into the other.

FINAL_GOAL = ONE_C1_SCIENCE_PUBLISH_AND_PERSISTENT_AUTOMATION_PROOF_THEN_STOP
