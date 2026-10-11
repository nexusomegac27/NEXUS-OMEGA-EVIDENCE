# NEXUS OMEGA — ICEBERG V1 · WWW C1 Publication / Pipeline Closure
## Operator-directed source-to-site integration · 2026-10-11

```text
OBJECT = NEXUS_OMEGA_AXIOM_ICEBERG_V1_C1_FULL_WWW_PIPELINE_RELEASE_ORDER_20261011_R0
PARENT = NEXUS_OMEGA_CURSOR_WWW_HOME_NAV_FORUM_FEED_ORBIS_MAXI_ROLLOUT_RETURN_20261011_R0
PARENT_EXECUTIVE_SHA256_REPORTED = 038d449ec157560f5f4c61b85bb58779539014647f072975484d5621dce5b0a5
WWW_EVIDENCE = PR83_COMMENT_6109548565 + PR54_COMMENT_6109551341
DESIGN_REFERENCE = https://www.palantir.com/ (GENERAL_EDITORIAL_PRINCIPLES_ONLY)
CONTENT_ORIGIN = NEXUS_OMEGA_ORIGINAL_BRAND_COPY_AND_EXISTING_SITE_C1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PUBLICATION_RULE = C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE_ROLLOUT_REQUIRED
EXECUTION = EXISTING_AUTHORIZED_CURSOR_HOSTINGER_PRAXIS
ACTUAL_SITE_SOURCE = NOT_AVAILABLE_TO_AXIOM_MCP
AXIOM_SITE_DEPLOY = NOT_EXECUTED
NODE_BUS = NOT_MODIFIED
NEW_WORKER = NO
```

## I. Decision: iceberg, not a copied corporation

Inspired only by *general* design traits observed on Palantir's public website and editorial reviews (https://www.palantir.com/ and https://fudge.design/share/palantir.com-design): restrained navigation, generous negative space, quiet typography, subtle rules, disciplined lower layers. **Do not copy Palantir's logo, typography files, imagery, text, code, product taxonomy, brand-specific animations, icons, proprietary materials or trade dress.** NEXUS has its own values and content.

Above the fold: NEXUS omega identity; four grounded nav destinations (Research, ORBIS, Forum, Evidence); existing strong headline `Wissen braucht Herkunft.`; one uninflated explanatory sentence; two links. No hero status-card grids, counters, hype, simulated satellites, artificial node vitality or excessive Living-Node-Sky animation.

Below fold (iceberg): three research surfaces and the full C1 evidence system. Preserve original source-bound pages. Do not destroy existing research archive, historical public index, current `03 LIVE FEED` or the actual Forum/ORBIS implementations merely to minimize the hero.

### Delivered working code and scope
- `examples/nexus-omega-iceberg-homepage-v1.html`: self-contained original HTML/CSS reference, with accessible desktop/mobile navigation, source links, ORBIS illustration explicitly labeled NOT MEASURED, and C1 explanatory labels. This is a deployable **design reference** not a drop-in replacement for unknown Next.js site source.
- `tests/nexus-omega-iceberg-homepage.test.mjs`: 12 offline tests for truthful links/claims, no duplicate feed, no injected worker or third-party assets, C1 boundaries, accessibility.
- Existing canonical live-feed executable remains `examples/nexus-public-update-ticker-v1.mjs` on main, PR83 merge `11c6860b563d5030a7f6d4b91113526f8229306f`. **Reuse this source** instead of implementing another feed or inventing fresh source timestamps.

### Strict Next.js site integration
Before any host edit, Cursor must inspect the **actual local website repository** and the `676fa4e3e942e39a` stylesheet identity that was missing in the Oct 11 return, plus current router layout and deployed HTML/CSS hashes. A new template in the EVIDENCE repo is not the site's actual code. Map this reference's `nxo-` styles onto a component/section under current site source, without overwriting global CSS, changing source-managed metadata, or breaking existing routes. Preserve existing event ticker's own mount as a SINGLE instance: the example only *links to* `/#live-feed` and does not duplicate live events. Keep no-JS fallback, reduced motion, focus order, tab sequence, 320/375/768/1440 px, 200% zoom, and no horizontal overflow.

## II. One pipeline; scope-specific releases

| Lane | Most recent source-bounded status | Execute and publish next | Terminal witness |
|---|---|---|---|
| W0 Root + visual layer | 2026-10-05 homepage accepted operator status; Cursor 2026-10-11 index 69,282 B SHA256 `3d935f8f…3c90`; source Next CSS still unbound | Bind actual Next source, adapt ICEBERG header/hero, preserve accepted HOME + content lower down | B2 site source/build revision + independent B3 desktop/mobile screenshot |
| W1 Existing LIVE FEED | Cursor reports public module 11,682 B SHA256 `ef501002…766f5`, byte-match PR83; 2026-10-01 source time retained | **Do not reupload the same bytes**; preserve original C1 feed and existing public event registry; test new layout doesn't suppress it | Existing Cursor readback rechecked after W0 release |
| W2 Main navigation | Cursor found `/orbis/` and `/forum/` both HTTP200 yet root links missing | Add exactly the verified accessible routes to existing header/menu, preserve other validated routes | Actual click/keyboard/mobile/404 scan + B2/B3 |
| W3 Forum | HTTP200 route source-reported; R10 RC identity UNBOUND | Surface navigational link immediately, public-safe forum view only; source-bind RC `out-v849-rc-r10-forum-full` separately before claiming RC release | Route UI and provenance checked independently |
| W4 ORBIS | `/orbis/` public; manifest D01 fixed, 248 B SHA256 `d6edb363…d6b4`, `satellites:[]`, jsonschema Draft2020-12 errors 0, reported | Link ORBIS now. Preserve illustrative surface; ensure directory/details render truthful zero-state. D02 SGP4 conversion only after exact model/source/date/license proof | Public manifest + browser marker count 0 (until real admission) |
| W5 Research index C1 | `/research/` currently indexed public C1 scientific claims, source page | Prominent accessible link; keep per-object C1, source, caveats, no canonical promotion | Page loads + click-through + source provenance |
| W6 R14 public gate | `/ai/r14-gate/` publicly indexed, 34 primary sources with open gaps | Keep existing C1 route discoverable in evidence area, no fabricated new validation | HTTP/browser + checked source date |
| W7 R15 and other validated public research | FSM-v2 original 9,101 B SHA256 `647a3b16…8acfd65` and Cursor local 41 PASS; not live-integrated | Publish **public-safe descriptive research only** after sanitization, source/rights check and correct data binding; no claim of active node runtime | C1 object page + source hash and independent browser |
| W8 Node registry / Living Memory | Public registry snapshot older; Living-Memory JSON missing `LIVE_TRIGGER` in current return | Show as historical C1/source-dated; do not invent live state or change LIVE_TRIGGER by inference | Exact JSON fields and source age |
| W9 GBAC | `/gbac/` HTTP404, source gap | Keep out of primary menu; recover existing GBAC source or show truthful hold on existing research index. Do NOT make up a page solely to pass 200. | Source-bound RC + origin 200 when safely restored |
| W10 Website operations | Hostinger identity `u310432914` and `public_html` from Cursor report; no new B2 upload in last run | Use only existing authorized PRAXIS; versioned backup, bounded actual source edit, HTML/JS/CSS readback; rollback. Hostinger Builder list empty in AXIOM environment. | Provider B2 (new asset hash) + independently observed B3 |

Do not mark a pipeline item `CLEAR` because a PR, design preview or GitHub CI succeeded. Record `CLEAR_SITE` only with source/deploy/public proofs appropriate to the item. Existing W1 is `PUBLIC_MATCH_SOURCE_REPORTED`, not an excuse to upload again. D02, GBAC and R10 lineage gaps are **component-specific**, never a global HOLD.

## III. Cursor execution — no paper loop

P0 (single read-only inventory): resolve existing real source, Next layout/CSS hash, navigation component, already installed ticker, deployed ORBIS/Forum, rollback/backup. Use existing worker/continuity only.
P1: implement restrained hero + 4-link header in actual **site source**. Restore navigation to existing /orbis/ and /forum/; keep all deeper existing C1 page content, no generic rebrand.
P2: verify existing feed and index; no needless identical reupload. Move visual/dense site status material below fold or onto research pages **without deleting source or altering epistemic statuses**.
P3: deploy W0/W2 via existing Hostinger scope if safe/reversible; secure before-and-after HTML/CSS/JS hashes. Independent B3 across 375/mobile, desktop, keyboard, slow/JS-disabled, true focus behavior and active hrefs.
P4: independent parallel Forum provenance and ORBIS D02; publish other C1-safe research without halting W0/2; site route updates source-bound.
P5: close W0–W10 each as `CLEAR_SITE`, `PRESERVED_PUBLIC`, `HOLD_SOURCE_GAP_<exact>` or `NOT_ATTEMPTED` with precise next action. **Return visible, actual website changes and screenshots/URLs, not only another spec.**

## IV. Release invariants

- `C1_DESCRIPTIVE_ONLY`; source ≠ truth; no invented observational data; 0 real satellites still honest.
- Site is not an authenticated NexusIntern command channel. No WWW-to-node write.
- No external assets copied from Palantir. No font redistribution. No duplicate event registry, DOM ticker, forum database, worker or API.
- Site deploy authority requires real authorized Hostinger route; an EVIDENCE-repo PR cannot establish deploy.
- No disruption of R13, nine-node legacy event records, Continuity/Watchdog, accepted forum source, R21 private archive.
- Privacy/license/CSP respected. Standalone errors scoped to failing route.
- Source-specific rollback must be demonstrated before high-visibility homepage change.

## V. Return contract

For every W0–W10 line, return: `lane, predecessor, local_site_source_path, source_SHA256, changed_commit, source_test_result, deployed_assets, provider_B2, browser_B3_URL_and_timestamp, desktop/mobile proof, rollback, exact_open_gap, terminal_state`. Protected private data remains in Hostinger/Cursor and public receipts must be sanitized. AXIOM records a report-level ACK until exact bytes independently available.

```text
OPERATOR_INTENT = DRAIN_ALL_PUBLIC_SAFE_C1_WWW_PIPELINE
DESIGN = NEXUS_ICEBERG_ORIGINAL_NOT_PALANTIR_CLONE
PUBLIC_SAFE_VALIDATED = RELEASE_REQUIRED
W0_W2 = PRIORITY_VISIBLE_CHANGE
W1 = DO_NOT_DUPLICATE
W3_W4 = PARALLEL_SOURCE_BOUND
CLAIM_PROMOTION = NO
NEXT = EXISTING_CURSOR_REAL_SOURCE_INTEGRATION_AND_SITE_B2_B3
```
