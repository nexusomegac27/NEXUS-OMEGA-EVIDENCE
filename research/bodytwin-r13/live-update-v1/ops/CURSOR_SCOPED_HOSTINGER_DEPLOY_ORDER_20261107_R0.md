# AXIOM → CURSOR | Bodytwin Live UI + automatic public C1 feed

```text
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_BODYTWIN_PUBLIC_LIVE_C1_AUTOMATIC_UPDATE_SCOPED_RELEASE_ORDER_20261107_R0
PARENT = NEXUS_OMEGA_CURSOR_R14_R2R1_WINDOWS_PORTABILITY_HARNESS_REPAIR_BIND_RETURN_20261107_R0
OPERATOR_INTENT = VISIBLE_LIVE_RESULTS_ON_HTTPS_WWW_NEXUS_MOBILE_DE_BODYTWIN_PLUS_AUTOMATED_UPDATING
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
PUBLIC_UI_ONLY = YES
PHYSICAL_IMU_RUNTIME = NOT_AUTHORIZED
``` 

## 1. Source-exact provenance

Use the GitHub review branch and full HEAD returned by AXIOM, not a moving `main`. Rehash each of the public script/style files, the reducer, and the exact public receipt. Read standalone README and test records. Do not mutate the original scientific PR #13/#15 nor R13 UI PR #323; no claim that GitHub push = Hostinger deploy.

## 2. S0 — actual WWW/Hostinger source census (READ ONLY)

Independently establish the current **physical** Hostinger document root and the actual deployed `/bodytwin/index.html` file. Record source URL, existing page SHA-256 and bytes, current 4D controls and JavaScript modules, response Content-Type/CSP, current `/research/bodytwin/state.json` raw bytes/headers, effective caching. Search only exact targets and registered source directories, no full archive crawl. Back up the existing Bodytwin index and `/bodytwin/live/` assets if any; record rollback path and hashes before any write.

**Do not** overwrite viewer source, alter SO(4) rotation/projector, delete symbolic privacy labels or change Bodytwin claim ceiling. If existing root HTML is not byte-bound, HOLD_BODYTWIN_PARENT_SOURCE rather than a blind replacement.

## 3. S1 — isolated local Windows/Cursor verification

Run `node --test tests/live-core.test.mjs` and `python -m unittest discover -s tests` on Windows in an isolated staging dir. Actual expected 39+40=79 pass; report actual counts, Python/PHP availability, strict syntax and UTF-8/HTML/CSP tests. Keep private return, IMU, medical, GPS, cameras, microphones and device media absent. Only exact two known public inputs are consumed by reducer.

Check **both Cron candidates**: use Python if available and capable of atomic writes and Unix flock on Hostinger, otherwise PHP CLI if verified (never activate both). Cron job goes to a private/nonpublic scripts folder outside `public_html` (paths from evidence, no guessed absolute paths). Do not turn source errors into successful refresh ticks.

## 4. S2 — scoped PUBLIC UI deployment

**The operator explicitly prioritizes live `/bodytwin/` UI and automated updates.** Treat this as a bounded public-safe change request for these exact assets and two HTML tags, subject to S0/S1 preconditions and rollback. No A72/IMU/consent authority is created.

1. Stage 4 public input/assets (three browser files + receipt) under `/bodytwin/live/`, no source/test/python/php programs in public webroot. Build initial `/bodytwin/live/current.json` by **running the actual reducer** against public state. Do not fabricate a dummy successful feed.
2. Verify `.mjs` under the Hostinger route serves HTTP 200 `text/javascript` with identical bytes **without external redirect**. Previous R9/Gate `.mjs` remount issues demonstrate the risk; fix extension routing only for the two new Bodytwin `.mjs` paths, preserving all other routes.
3. In the original `/bodytwin/index.html`, insert only `<link rel="stylesheet" href="/bodytwin/live/live-panel.css">` within `<head>` and `<script type="module" src="/bodytwin/live/live-panel.mjs"></script>` before `</body>`. No other diff. Preserve rollback snapshot.
4. Read-only dry-run the status panel in staging with 4D viewer controls and mobile touch interactions. Check no console errors, correct effective CSP allowing self-styles/self-scripts and same-origin `connect-src`, no cross-origin requests, no cookies/auth, no personal data.
5. Deploy atomically/reversibly to Hostinger after stage PASS. Record Hostinger deployment ID, remote path and rollback.
6. Register exactly one Cron job **every 5 minutes** with verified actual executor path (Hostinger hPanel Cron type PHP or Custom as appropriate). Hostinger documents cron schedules in UTC; no assumption of current local OS timezone. Bind Cron schedule, stdout and two **real successive scheduled ticks** proving the sequence changes while source bytes remain stable. Distinguish from immediate manual runs. If source bytes change under authorized publication, require `source_changed=true` and new `last_change_utc`.

## 5. S3 — independent live acceptance

Require the following source-exact evidence before reporting `BODYTWIN_C1_LIVE_PANEL_WWW_PASS`:

- `https://www.nexus-mobile.de/bodytwin/`: HTTP 200 and Browser CDP DOM shows visible `#nexus-bodytwin-live-c1` status panel, original 4D interactions still functioning.
- `/bodytwin/live/live-core.mjs`, `live-panel.mjs`, `live-panel.css`, `receipts.public.json`, `current.json`: HTTP 200, correct MIME, raw bytes SHA-256 match staged objects, no redirect; special check `.mjs` module load.
- `/research/bodytwin/state.json` input exact schema, no `BODYTWIN_VALIDATED=YES`, no `CONSENT_BIND=GRANTED`, trial stays unexecuted.
- Cron Hostinger execution receipt and **two successive real 5-minute ticks** with `producer.seq` increase; `source_changed=false` when source hashes same, no fabricated scientific updates.
- Browser auto GET at least twice after 60-second interval (or synthetic fast timer for test only), visibility hide/resume and stale clock, 403 and wrong MIME/future producer negative tests, sequence rollback negative tests.
- R14-R2R1 displayed as **Cursor-reported offline tests**, not independent sensor validity. R13 Stage II remains HOLD until its own release independently validated.
- One ZIP+.sha256 return to `NEXUS_OMEGA_TRANSFER/10_TO_AXIOM` with full source HEAD, input/reducer hashes, HTTP headers/bytes, DOM/CDP, Cron ticks, rollback, DLP, separate transport/science/consent statuses.

## 6. Stop and rollback

If real docroot, Cron executable, `.mjs` serving, source integrity, CSP or 4D preservation cannot be proven, stop at the *exact* failed gate and return `SOURCE_READY_DEPLOY_PENDING` or `LIVE_UI_PARTIAL` (not an invented LIVE PASS). Fail closed on private data, scientific promotion or nonreversible root replacement. Prior sealed R11/R12/R13/R14, PR #13/#15/#323, Gate V2 R9 .mjs and A72 source gap remain unchanged.

```text
HARD_WALLS = R11_R12_PRESERVED; R13_STAGE_II_HOLD; R14_R2R1_SOURCE_REEXEC_PASS_CURSOR_REPORTED;
  A72_ORIGINALS_SOURCE_GAP; BODYTWIN_VALIDATED_NO; CONSENT_OPEN; PHYSICAL_IMU_NOT_AUTHORIZED;
  GATE_V2_R9_MJS_HOLD; R10_HEARTBEAT_NOT_STARTED; N34_PARTIAL_2_OF_5; G11_HOLD;
  N33_OPEN; STAGE2_316_HOLD_NO_START; NO_CLAIM_PROMOTION
```
