# NEXUS OMEGA · Bodytwin LIVE C1 · P0 overlap remediation

OBJECT = NEXUS_OMEGA_AXIOM_BODYTWIN_LIVE_PANEL_OVERLAP_SCOPED_REPAIR_20261108_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
REQUEST = LIVE_/bodytwin/_PANEL_OVERLAP_REPAIR
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CURSOR_ROLE = TECHNICAL_STAGE_AND_DEPLOY_OF_REVIEWED_HOTFIX_ONLY
EXTERNAL_EXPERT_4D_VISUAL_DESIGN = STILL_EXCLUDES_CURSOR

## Confirmed exact defect in upstream source (not a pixel screenshot)
`research/bodytwin-r13/live-update-v1/site/live-panel.mjs` in public PR #324 (pinned head 93190d5ad6fa972fddd46b05ecd8f25408a7a70e) says:
`const main=document.querySelector('main')||document.body;` and `main.insertBefore(section,main.firstChild);`
This inserts the new panel into the existing 4D viewer's first layout slot. The deployed CSS has a scoped panel but does not isolate it from parent grid/flex geometry. The exact visible overlap has NOT been independently measured with a real host browser in AXIOM's current environment.

## Scoped remedial candidate
`site/layout-hotfix-r0.js` is **client-side-only**: after the existing panel appears, move that *same element* outside `main` to the immediately following sibling position. No panel reconstruction, re-fetch, new timers, changes to scripts, classes, 4D projections, host reducer or status producer. If two panels with the same ID exist, fail visible `HOLD_DUPLICATE_PANEL`, no silent deletion. If panel absent on page load, expose `HOLD_PANEL_NOT_FOUND`; do not falsify PASS.
`site/layout-hotfix-r0.css` scopes all rules to existing `#nexus-bodytwin-live-c1`, gives it its own normal-flow row (`grid-column:1/-1`, `position:relative`, max width, mobile layout), and does not style the original viewer.
Self-contained Node fake-DOM tests: 15/15 PASS under Linux Node22.16.0. Attempts to run Chromium with `file://` and local HTTP failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR`; therefore REAL_BROWSER_LAYOUT_WITNESS = PENDING and must be supplied in Cursor's authorized browser.

## Cursor execution, not discretionary design
0. Ensure latest Hostinger deployed `index.html` full original bytes/SHA and exact origin of live-panel source CSS/JS. Count actual panel IDs, script tags, main/viewer DOM. Before write, record original screenshots and per-box bounding rectangles at 320px, 390px, 768px, 1280px, viewer interactions (five projections, six plane controls), source feed seq and JSON SHA. Verify `current.json` source self-hosted and `source_changed` separation.
1. Validate preview within isolated staging with the unchanged viewer and existing panel. Load the new two assets as same-origin files; allow only 2 additive tags, **do not duplicate old source/CSS or overwrite index wholesale**:
   `<link rel="stylesheet" href="/bodytwin/live/layout-hotfix-r0.css">` within `<head>` after original live-panel.css, and
   `<script src="/bodytwin/live/layout-hotfix-r0.js" defer></script>` before `</body>` after original live-panel.js module tag.
   If old module loads after shim, MutationObserver handles insertion and disconnects after one placement.
2. Stage and run browser at desktop 1280×800, 768×1024, phones 390×844 and 320×640. Required: exactly ONE `#nexus-bodytwin-live-c1`, document root `[data-nexus-bodytwin-layout="PASS_ISOLATED_PANEL"]`, panel NOT descendant of `<main>`, panel top >= bottom of all 4D viewer geometry and rotation controls, panel left>=0 and right<=viewport; no horizontal scroll. Do not infer CSS PASS solely from DOM mutation; measure getBoundingClientRect, screenshot and inspect source map and computed styles.
3. Verify original 4D controls remain interactive (all five modes and six sliders) and live feed still GETs every 60s, Cron every 300s (NO cron changes). Actual source `seq` increment ≠ scientific change; no new devices/personal data. Verify CSP (`script-src 'self'` and `style-src 'self'`), actual MIME `.js` as JavaScript, `.css` as CSS, HTTP200, no redirects, ETag/cache and bytes SHA256. If site response has restrictive CSP headers, return HOLD and don't weaken globally.
4. Run negative fixtures: no panel, duplicate ID, delayed original module mount, muted CSS, 320px + 200% zoom, `<main>` absent, browser extensions off, reduced motion, 4D canvas visibility unchanged. If anything is wrong, stay staged.
5. Operator's latest instruction explicitly requests correcting the existing published page; treat as narrowly-scoped reversible public C1 layout hotfix, not new scientific visual design or broad Hostinger rewrite. If confirmed preview passes and rollback proven, deploy exactly two new files + exact two index insertions; preserve old index backup. Never touch `current.json`, `receipts.public.json`, reducer, Cron, R13/R14, R11/R12, Gate V2 or main merge.
6. After WWW publish, independent CDP screenshot and layout-bounding-box evidence; 60-second polling and two producer ticks can reuse prior receipts for unchanged producer but fresh feed GET must work; do not claim new 24h uptime. A failed viewer or overlapping panel triggers immediate exact rollback (restore original HTML and remove only two tags; remaining two unused assets harmless). Seal ZIP + SHA256 under NEXUS_OMEGA_TRANSFER/10_TO_AXIOM, with 00_EXEC, 10_HS, 20_WALLS, 30_RESULT, 40_MACHINE, 99_SUMS.

## R16 independent science branch: do not promote it in this hotfix
Uploaded Q0-VIE~1.JS R1 = 9116 bytes / SHA256 e03e6664c312f2f50081e6dc0fb8d03210e847ef5bf67d895688b20a10d8ebea.
Uploaded Q0-AUD~1.JS R1 = 7756 bytes / SHA256 1bb562bc87506ebed82708930d11ee36b97843e55f33cb47aa0bafe738cddbf6.
Independent Node22.16.0 replay = 17/20 (P05 cross-realm deepEqual and N07/N08 stale vm `errorState` snapshot), matching uploaded GROK report; prior 20/20 functional sandbox is not byte-identical Node testimony. Fail-closed R1 viewer is a **reconstructed reference**, NOT current production source. This P0 request DOES NOT authorize replacing user-visible 4D formulas or shipping stereographic default-pole behavior. Separate E1 mathematical decision and E3 UX after original E2 main document.

WALLS = BODYTWIN_VALIDATED_NO · PHYSICAL_IMU_NOT_AUTHORIZED · A72_SOURCE_GAP · CLAIM_CEILING_C1_DESCRIPTIVE_ONLY · NO_CLAIM_PROMOTION · NO_PR_MERGE · NO_4D_VIEWER_SOURCE_SUBSTITUTION · NO_CRON_WRITE · NO_SITE_WIDE_OVERWRITE · EXPERT_REVIEW_CURSOR_EXCLUDED.
