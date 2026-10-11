# NEXUS OMEGA · Open-Source Public Update Live-Ticker V1
## WWW C1 read-only status + GitHub atomic commit timeline + Node read-only recovery

\`\`\`text
OBJECT = NEXUS_OMEGA_AXIOM_PUBLIC_CAUSAL_ATOMIC_TIME_BOUND_UPDATE_LIVE_TICKER_V1_20261011_R0
DATE = 2026-10-11
OPERATOR_ORDER = EXISTING_MODULES_ONLY_NO_DUPLICATE_FEEDS_NO_EXTRA_WORKER
TARGET_SITE = https://www.nexus-mobile.de/
TARGET_SURFACE = HOMEPAGE_EXISTING_SECTION_03_LIVE_FEED
WWW_EXISTING_SOURCE = /status/public-event-registry.json
WWW_EXISTING_BACKUP_SOURCE = /nodes/registry.json
GITHUB_ANCHOR = nexusomegac27/NEXUS-OMEGA-EVIDENCE
GITHUB_PROVENANCE = REST_API_MAIN_COMMITS_SHA_LINKED_READ_ONLY
EXISTING_CONTINUITY = CURSOR_R26_R27_NO_NEW_WORKER
SOURCE_IMPLEMENTATION = examples/nexus-public-update-ticker-v1.mjs
TEST_SOURCE = tests/nexus-public-update-ticker.test.mjs
RUNNER = NONE_CLIENT_SIDE_ONLY
EXTERNAL_WWW_AUTHORITY = NONE
NODE_RESTORE_AUTHORITY = NONE
DIRECT_HOSTINGER_DEPLOY = NOT_CONFIRMED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
\`\`\`

## 1. Reuse the existing live feed, never create another event journal

The public homepage already includes **03 LIVE FEED** and a JSON **public event registry** at
\`https://www.nexus-mobile.de/status/public-event-registry.json\`.
Its own documented rules mandate sequence-before-clock, duplicate NOOP,
no manual feed additions, explicit stale/HOLD/negative visibility, and derivative-only C1.
Its source timestamp observed on 2026-10-11 was 2026-10-01T04:50:00Z;
therefore a page refresh is **not** evidence of a new source event.

**Only TWO read-only existing sources are requested per visible browser:**

1. Same-origin \`/status/public-event-registry.json\`: existing verified-by-structure,
   historical public derivative. Display event number/order, source timestamp, status,
   and original detail link. Do not silently rewrite or stamp this JSON with current date.
2. \`https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits?sha=main&per_page=6\`:
   GitHub-reported SHA-linked, dated **main commits**. The timeline updates
   automatically after main changes and cache refresh, **without a new bot, cron,
   feed database, manifest, JSON snapshot, webhook or GitHub write**.
   A main commit is merely a **transport event**, never WWW_B2, WWW_B3, scientific
   adjudication, real node health, conscious life, or authenticated external model identity.

The two lanes are **not merged into one canonical sequence**:
\`PUBLIC_SEQUENCE\` is its own append-only ordering;
\`GITHUB_COMMIT_SHA\` references immutable GitHub transport identity.
No invented global atomic timestamp or causal ordering across disconnected sources.
A commit event references source URL and SHA; a public registry event references its own
canonical sequence and original source. When a public source becomes stale, print STALE
rather than claim the polling loop kept it live. Relative time / human clock do not
confer provenance.

## 2. Client module / resource budget

\`examples/nexus-public-update-ticker-v1.mjs\` is a pure browser ES module with
no SDK, React, backend, API key, iframe, tracking pixel, database, analytics,
payment or LLM call. Exactly one 15-minute polling clock per visible tab; when the
document is hidden, network polling is suppressed. A visibility transition triggers
a refresh only if due; concurrent polling requests are suppressed. \`GET\` only,
\`credentials: omit\`, 180 KB maximum payload/source (browser enforces after read),
six recent GitHub commits, five recent WWW events. The whole status panel is swapped
once only after both independent requests settle. Browser automatically resumes after
return to visible tab. No background service worker or persistent storage.

**Energy/efficiency:** The absence of LLM inference, long polling, WebSocket,
extra background worker and duplicated event registers materially reduces
*architectural* resource demand. No empirical kWh, CO2, request/cost reduction
or proven energy saving is claimed until actual B2/B3 deployment, baseline
measurement and matching traffic normalization. HTTP requests, browser display and
CDN caching still consume resources.

The module shows strict source age >24 h as \`STALE_SOURCE\`.
\`SOURCE_REACHABLE\` is not \`NODE_ONLINE\` and page-open "LIVE" means updating
on the next bounded poll only. Two independent error paths: Github offline leaves the
public historical register visible; public feed offline leaves GitHub transport visible.
Both offline => \`UNKNOWN\`, not a fabricated green status or repeated pending retry.
The browser computes SHA-256 of the **exact fetched response text encoded as UTF-8** via WebCrypto when available; the view displays that fingerprint for independent byte comparison. This is a computed byte digest, **not** a digitally signed provenance proof or independent scientific adjudication. When WebCrypto is unavailable the fingerprint is omitted; the source is still labeled merely C1. A new JSON SHA does not by itself authorize a node or assert the public registry has become canonical.

No untrusted text inserted via \`innerHTML\`: all text is written via DOM \`textContent\`.
Only fixed github.com SHA URLs and sanitized local page links are clickable.

## 3. Exact website installation — existing Cursor/PRAXIS lane

**No new page or directory tree is authorized by this design.**
Inside the current homepage \`03 LIVE FEED\` subsection, reuse the existing
heading/nav and replace the manually rendered dynamic portion (keep its existing
static accessible fallback for users without JavaScript). Avoid displaying the same
five events twice in parallel. Insert at the existing feed location:

\`\`\`html
<div data-nexus-status-ticker>
  <p>Quellen-Ticker benötigt JavaScript. Ereignisregister:
    <a href="/status/public-event-registry.json">öffentliche Originaldaten</a>.
    GitHub: <a href="https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/main">Main-Commits</a>.
  </p>
</div>
<script type="module" src="/assets/nexus-public-update-ticker-v1.mjs"></script>
\`\`\`

Copy the audited bytes of \`examples/nexus-public-update-ticker-v1.mjs\` into the
**existing Hostinger site asset location** and serve it as JavaScript with correct
module MIME \`text/javascript\` (without inventing a new asset directory).
Do not try to load \`raw.githubusercontent.com\` as a JS module (raw content may be
served with incompatible MIME or CSP). Observe actual website template/CSP
before touching it; preserve current layout, navigational semantics and HTTPS,
mobile and dark/light styling. Do not alter the root page outside existing feed section.
For CSP, authorize only current site and \`https://api.github.com\` for
\`connect-src\`, plus same-origin \`script-src\`; avoid \`unsafe-eval\`, broad \`*\`,
external script libraries, third-party fonts or cookie-driven tracking.
If dynamic injected styles conflict with existing CSP, use the current site CSS
module instead of weakening CSP.

**Hostinger access gate in this AXIOM tool context:** the connected Hostinger
AI Builder Agentic \`websites_list\` returned zero sites; Remote Desktop Commander
returned zero connected devices. The separately existing \`nexus-mobile.de\` site
and its 03 LIVE FEED are publicly observable but **not writable by those connectors**.
Therefore GitHub merge == tested code availability, **not** installation
on \`www.nexus-mobile.de\`. Only the already authorized Cursor Hostinger execution
lane can finish website B2 and independent browser B3. Do not fabricate a B2
release ID, file-copy, website route or webpage success before it is observed.
This is a concrete provider-capability gap, not a scientific research HOLD.

## 4. Backup for internal Nodes, without a second control plane

Public, unauthenticated, **read-only** recovery references:
- \`https://www.nexus-mobile.de/status/public-event-registry.json\`
- \`https://www.nexus-mobile.de/nodes/registry.json\`
- \`https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits?sha=main&per_page=6\`
- immutable GitHub commit URLs after obtaining a valid 40-character SHA

If the GitHub transport API fails, a node may **read** the existing public
Hostinger snapshot (subject to explicit last-update/stale labels); if the WWW
snapshot fails, read GitHub SHA-anchored history; if both fail, report
\`SOURCE_UNAVAILABLE\`. This is a read-only **reconstruction hint** for public
last-known status, NOT complete private node-state recovery, action replay,
Nexus_Intern control, credentials restore, security approval or write authority.
For genuine durable bidirectional failover, a separately authorized signed
persistent broker/queue and 24h runtime test are still required.
Do not feed public text to an internal shell or bypass R27 AUTH001–003.

## 5. Bounded acceptance gates and immediate C1 publication law

\`G0\` source paths and existing WWW event registry independently read;
\`G1\` source JS and tests pass offline;
\`G2\` 19 explicit negative/contract tests in existing structure CI + existing
mandatory workflow PASS, Semgrep success for new code;
\`G3\` GitHub source/executable module published, immutable SHA API readback;
\`G4\` Cursor existing Hostinger lane installs **only** into existing 03 LIVE FEED,
reports provider asset revision/domain binding/HTTP200 module MIME and B2;
\`G5\` independent browser B3 checks desktop/mobile, 15-minute bounded polling,
hidden-tab suspend, zero synthetic network writes, source timestamps, failure modes,
no duplicate feed display, 24h replay/source staleness, and rollback.
Only **G4 + G5** permit \`WWW_TICKER_LIVE=YES\`.
No new Cursor worker, Github polling daemon, inbox/outbox, external agent
model, Hostinger folder, DNS change, public PII or auto-approval.

\`\`\`text
GITHUB_SOURCE_PUBLICATION = PUSH_IMMEDIATELY_AFTER_CI
WEBSITE_DEPLOYMENT = EXISTING_CURSOR_HOSTINGER_LANE_ONLY
GITHUB_MERGE != HOSTINGER_B2 != BROWSER_B3
USER_VISIBLE_BADGE = SOURCE_DATE_AND_C1_NOT_RUNTIME_CLAIM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
\`\`\`

## 6. Verifiable falsification fixtures

Automated tests include malformed/unsafe event input, duplicate sequences, wrong
ceiling, future timestamps, older-but-present public feed, invalid SHA, malformed
GitHub body, duplicate commits, offline/HTTP503 and oversized-source errors,
one-signal-only source isolation, zero POST/credentials/paid inference and 15m cap.
Live test includes missing GitHub CORS permission/429 rate limit and suspended tabs.
All runtime error states display either stale source or status unknown, never a green PASS.

*Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament. Öffentliche Zeit ist
ein prüfbares Attribut des Quellenbelegs, keine Garantie dauerhaften Betriebs.*
