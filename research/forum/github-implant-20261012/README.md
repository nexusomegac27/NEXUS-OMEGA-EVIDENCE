# GitHub_Implant · NEXUS Forum · 2026-10-12 R0

**Object:** `NEXUS_OMEGA_FORUM_GITHUB_IMPLANT_LIVE_READONLY_C1_20261012_R0`  
**Authority:** OPERATOR_DIRECT_C1_PUBLICATION; AXIOM implementation; Cursor/PRAXIS may publish to the *existing* official Hostinger forum root with its established runtime controls.  
**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`.  
**Scope:** Public-safe GitHub repository representation. **Not a separate GitHub UI proxy; not a 100% persistent duplicate of all Git blobs.**

## Output / architecture

The production-ready standalone static site is `site/index.html` with only two local assets `site/assets/github-implant.css`, `site/assets/github-implant.js`.

- Responsive mobile-first refinement: spacious editorial typography, restrained emerald/gold status markers, dark surface, accessible contrast, visible keyboard focus, reduced-motion support, tablist navigation.
- Official public GitHub REST endpoints, read-only: `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits?sha=main&per_page=15`, `GET /pulls?state=all`, `GET /contents/<path>?ref=main`. This includes repository navigation, individual plain-text file previews up to 150kB and direct original links; larger/binary files link to the original.
- No GitHub token in browser, no third-party script, no API write, no external tracking, strict CSP. Browser CORS is supported by GitHub API; 60 unauthenticated requests per hour per originating IP; cached ETags, five-minute interval and per-request cooldown.
- Fails visibly for quota exhaustion, network failure, rate-limited APIs and unverified freshness. The interface never claims GitHub commit validity equals scientific truth.

## Actual website integration (existing site only)

The exact new route is `https://www.nexus-mobile.de/forum/github-implant/`. Copy three static files from `site/` **without renaming, modifying or wrapping them** into the existing Hostinger site document root:

```text
<EXISTING_FORUM_WWW_ROOT>/github-implant/index.html
<EXISTING_FORUM_WWW_ROOT>/github-implant/assets/github-implant.css
<EXISTING_FORUM_WWW_ROOT>/github-implant/assets/github-implant.js
```

In the existing `/forum/` navigation add one small, semantically labeled subtab `GitHub Implant` pointing to `/forum/github-implant/`. **Do not replace the existing forum page or homepage.** Retain its current navigation hierarchy, visual tokens when available and responsive behavior. When style conflict exists, revise the new leaf module, never overwrite the established homepage. Link back to Forum and original GitHub is already included.

If the forum is not served as static files, adapt into its pre-existing templating/router mechanism and preserve the same URL, CSS scoping and read-only API rules. Do not create a new Hostinger project or DNS/subdomain.

Before calling WWW LIVE verify HTTP status, correct page title, 200 responses for JS/CSS, usable mobile at 375px and desktop at 1440px, tab keyboard navigation, GitHub API origin and visible source status; inspect Content-Security-Policy **HTTP response header** (the current page includes meta CSP but frame-ancestors must be set server-side). Record public status/HTTPS/deployment time and original/source SHA-256; if no host access, report `HOSTINGER_DEPLOY_CAPABILITY_GAP` and do not invent a live WWW claim.

## "Everything published on GitHub must appear on www"

Two separate mechanisms, do not conflate:

1. **Live readable view** (implemented above): public GitHub main-commit timeline, Pull Requests, browsable full public directory tree and file text views. Browser requests originate at GitHub; those bytes are **not** independently archived on NEXUS hosting.
2. **Host-resident file mirror** (offline builder implemented, host deployment pending): `tools/mirror_public_git.py --source <CLEAN_CHECKOUT> --output <NEW_STAGING_PATH>` makes a deterministic, exact-byte public-safe snapshot with manifest, SHA-256, source commit ID, excluded-file list and no hidden Git metadata. No secrets/private paths are blindly duplicated. Test: `python -m unittest discover -s tests -p 'test_*.py' -v`.

When the existing Hostinger deployment credential / authorized Cursor site workspace is available, the **existing** site-sync workflow should atomically place that staging snapshot under `/forum/github-implant/mirror/<commit>/`; after server-side hash readback and HTTPS check the rendered forum may display its published completeness state. GitHub-public content does not bypass license, privacy, GDPR and secret checks. A proof of 100% original mirror requires `complete_unfiltered_mirror=true` plus HTTP verification for all expected safe bytes; otherwise report scoped exclusions. The manifest is itself immutable per commit. Old published snapshots are append-only and remain addressable.

## Independent source research

Verified open-source option: [peterbenoit/RepoWidget](https://github.com/peterbenoit/RepoWidget), MIT, no mandatory dependencies. Considered but not vendored since the first-party API implementation has a smaller trust surface and supports the actual NEXUS file explorer. No dependency redistribution necessary.

Official references: GitHub REST commits, pulls and Contents docs, CORS guidance and REST rate-limit docs. Do not proxy/scrape copyrighted GitHub UI. GitHub API representation is an interface, not a repository backup.

## Verification status

```text
GITHUB_EVIDENCE_SOURCE_PUBLICATION = PENDING_PR_MAIN
SOURCE_JS_PARSE = PASS_LOCALLY_IN_AXIOM_V8_CHECK
SITE_HOSTINGER_DEPLOY = NOT_EXECUTED_NO_CONNECTED_SITE
LIVE_WWW_HTTPS_CHECK = NOT_ESTABLISHED
C1_SCIENTIFIC_CLAIMS = DESCRIPTIVE_ONLY
GITHUB_ALL_BYTES_HOST_MIRROR = NOT_ESTABLISHED
```

## GitHub↔NEXUS Security & Science Gate (additive 2026-10-12)

The existing Implant now links to a narrow, **read-only interface monitoring Node** under `site/gate/`. It verifies only the three canonical deployed Implant file bytes against GitHub main using WebCrypto SHA-256, recognizes the C1 marker and shows material source/WWW discrepancies. The [Gate scientific/technical contract](GATE_INTERFACE_CONTRACT_V1.md) describes scoped PASS/HOLD states, bounded source assumptions, rate limits and the PiP design; the [Hostinger one-shot mount](SITE_GATE_ONE_SHOT_MOUNT.txt) uses the existing public Hostinger site channel. Native Document-PiP is progressive enhancement; a draggable on-page floating status card works as fallback, without importing any third-party scripts. [13 local Node tests](tests/test_gate.mjs) passed in the receiver research environment, their source exactness must be rechecked after GitHub readback. Site live-mount and browser network test remain separate from source publication. This Node observes transport integrity; it is not a publishing blocker or scientific truth certifier.
