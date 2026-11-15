# NEXUS OMEGA — BODYTWIN DIRECT WWW PUBLIC C1 UPDATE / 15 NOVEMBER 2026

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_BODYTWIN_C1_PROGRESS_WWW_DEPLOY_SINGLE_PATH_20261115_R0
OPERATOR_REQUEST = USER_EXPLICIT_BODYTWIN_WWW_VISIBLE_UPDATE_20261115
SCOPE = ADDITIVE_PUBLIC_SAFE_REVERSIBLE_VISIBILITY_UPDATE_NOT_RESEARCH_LOOP
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
TARGET = https://www.nexus-mobile.de/bodytwin/
DETAIL = https://www.nexus-mobile.de/bodytwin/updates/
WWW_ACTION = ROLLOUT_REQUIRED_AFTER_TECHNICAL_GATES
MAIN_4D_VIEWER = PRESERVE_EXACT
LIVE_FEED = PRESERVE_EXACT
PHYSICAL_IMU = NOT_AUTHORIZED
OPPO_CAPTURE = NO
HOSTINGER_CREDENTIALS_IN_RECEIPTS = NO
PRIVATE_SOURCE_OR_SENSOR_DATA_PUBLICATION = NO
GITHUB_PR_MERGE = NOT_REQUIRED_FOR_HOSTINGER_SITE_FILE_DEPLOY

## 0. Why this is a release, not another paper loop

User reports September 4D site does not show the substantial work since then. Direct read-only public URL check on 15 November 2026 observed original viewer identity `NEXUS_OMEGA_BODYTWIN_VIEWER_20260914_R0` with last_verified 2026-09-12. Separately, `/bodytwin/live/current.json` returned a self-hosted producer record: run_utc 2026-11-15T07:50:02Z, seq 2150, interval 300s, source_changed false, last_change_utc 2026-11-07T20:50:02Z. This is a feed tick, NOT new science. The existing 4D viewer's source JS/CSS has NOT been independently frozen for this release; therefore this patch never rewrites it.

This release is a dated, visible C1 research-log element after the viewer plus one standalone accessible `/bodytwin/updates/` page, with machine-readable `events.json`. It is independent of the continuous feed and makes no "AUTO SCIENCE" claim. No new sensor path or BodyTwin clinical validation.

## 1. Exact-source intake (GitHub branch pinned at Cursor execution start)

Owner-only GitHub branch: `axiom/bodytwin-public-progress-20261115-c1` in `nexusomegac27/NEXUS-OMEGA-EVIDENCE`.
Site source files (relative to `research/bodytwin-r13/public-progress-20261115/site/`):
- `progress-fragment.html` — one added inline section after </main>; no script
- `progress.css` — namespaced `#nexus-bodytwin-progress-20261115`, no fixed overlays
- `updates/index.html` — independently readable without JavaScript
- `updates/events.json` — datestamped machine-readable C1 research ledger, `published_live:false` means **candidate** at creation, not false live release
Helper: `ops/apply_bodytwin_progress.py` — default dry-run, exact rollback validation, site assets before root HTML, operator ACK on apply.
Tests: `tests/test_progress.py`; any GitHub Actions result must bind exact HEAD.
NEVER guess source hashes or copy past old PR assumptions: rehash exact current branch bytes and current Hostinger index before writing.

## 2. Deploy sequence — one automatic bounded run by Cursor on existing authorized operator access

PREENTRY / NO WRITE:
1. Identify canonical web root for this domain using the existing authorized Hostinger site account or operator-approved SFTP endpoint. Do not use the guessed Windows or Hostinger path, and never print SSH credentials or keys.
2. Verify existing files `bodytwin/index.html`, five projection modes, six SO(4) controls and existing `bodytwin/live/current.json`. Record a public-safe SHA256+byte count and a sealed **nonpublic** backup of old index.html and assets. Ensure historic 4D JS/CSS is not edited.
3. Fetch exact source from the pinned GitHub branch and run `python3 -m unittest discover -s .../tests -p 'test_*.py' -v`; fail closed on any failed test.
4. On an AUTHORIZED LOCAL/STAGING COPY of the current webroot run:
   `python3 ops/apply_bodytwin_progress.py --web-root <staging-root> --site-source <source>/site`
   Verify JSON `mode=DRY_RUN`, `state=READY` or exact `ALREADY_PRESENT`. If root lacks a unique `</head>` or `</main>` closing marker or contains partial progress markers, DO NOT force a generic regex rewrite. Adapt staging under explicit original-source browser proof, never replace viewer wholesale.
5. Stage/apply the PUBLIC-SAFE delta, only after backup: set `--apply --operator-ack BODYTWIN_PUBLIC_C1_RELEASE_20261115 --backup-dir <nonpublic-existing-backup-dir>`. The user's explicit update request authorizes this reversible public-safe deployment if and only if tests, privacy scan and rollback prove safe. No approval to enable physical capture or private data.
6. If site is remote, apply/stage on approved operator working copy and upload only exactly `/bodytwin/index.html`, `/bodytwin/updates/index.html`, `/bodytwin/updates/events.json`, `/bodytwin/updates/progress.css` with exact SHA256, owner-approved deployment client, backup and atomic swap of index last. No opportunistic relaunch of the rest of website.
7. Stop on any secret/PII, syntactic, credential, unexpected changed original or destination collision. No merge is needed for this separate scoped Hostinger deploy; the evidence PR stays DRAFT for later adjudication.

LIVE ACCEPTANCE — MUST BE OBSERVED AFTER WRITE:
- HTTP(S) 200 on `/bodytwin/`, `/bodytwin/updates/`, `/bodytwin/updates/progress.css`, `/bodytwin/updates/events.json`, `/bodytwin/live/current.json`.
- Correct Content-Type for HTML/CSS/JSON; no HTML fallback returned in place of JSON/CSS.
- Browser DOM exactly **one** `#nexus-bodytwin-progress-20261115` and exactly one preexisting `#nexus-bodytwin-live-c1` if the live panel was already installed. The new progress section must follow `<main>` and not overlap the original Canvas/projection-controls.
- Existing all **five** 4D projections and **six** SO(4) plane sliders usable before/after at viewport widths 1280, 768, 390 and 320. Do not infer geometry merely from HTML text; test real controls and CSS bounding boxes.
- Read-only live feed continues with 300s cadence; no POST, camera, microphone, sensor, login, consent change, A72 promotion.
- Dated visible timeline and machine JSON contain the same 5 source events and C1 limits. Public links resolve.
- Stop and rollback if UI regression, malformed MIME, privacy leak, source drift or HTTP mismatch. Recheck restored bytes and DOM. No "success" without a real after-write browser and HTTP witness.

## 3. One return, no loop

Minimum Cursor return:
```text
OBJECT = NEXUS_OMEGA_CURSOR_BODYTWIN_C1_PROGRESS_WWW_DEPLOY_RETURN_20261115_R0
STATE = LIVE_WWW_PASS_C1 | HOLD_VERIFIED_GAP | ROLLED_BACK_FAIL_CLOSED
SOURCE_BRANCH_HEAD = <40-hex>
CURRENT_OLD_BODYTWIN_INDEX_SHA256 = <full>
NEW_BODYTWIN_INDEX_SHA256 = <full or NOT_WRITTEN>
HOSTINGER_WRITE = YES|NO
BODYTWIN_ROOT_HTTP = <code + independent bytes or NOT_OBSERVED>
BODYTWIN_UPDATES_HTTP = <code + actual bytes or NOT_OBSERVED>
MOBILE_DOM = PASS|FAIL|NOT_RUN
DESKTOP_DOM = PASS|FAIL|NOT_RUN
4D_REGRESSION = PASS|FAIL|NOT_RUN
LIVE_FEED_UNCHANGED = PASS|FAIL|NOT_RUN
BACKUP = SEALED_NONPUBLIC|NOT_CREATED
ROLLBACK = READY|EXECUTED|NOT_AVAILABLE
BODYTWIN_VALIDATED = NO
OPPO_CAPTURE = NOT_AUTHORIZED
C1_CLAIM_PROMOTION = NO
NEXT = PUBLIC_VISIBLE_CHANGE_CONFIRMED | EXACT_DEPLOYMENT_BLOCKER
```
Preserve source and negative caveats. No new analysis phase, no other Hostinger routes modified, no further Cursor instruction needed if tests pass.
