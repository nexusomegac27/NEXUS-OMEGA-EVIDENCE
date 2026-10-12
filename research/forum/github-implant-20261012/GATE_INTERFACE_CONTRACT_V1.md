# NEXUS OMEGA · GitHub↔NEXUS Security & Science Interface Gate V1
2026-10-12 · SPDX-License-Identifier: MIT

```text
OBJECT = NEXUS_OMEGA_GITHUB_NEXUS_INTERFACE_GATE_C1_20261012_R0
PREDECESSOR = NEXUS_OMEGA_FORUM_GITHUB_IMPLANT_LIVE_READONLY_C1_20261012_R0
PURPOSE = BRIDGE_OBSERVABILITY_ONLY_SECURITY_AND_SCIENCE
ROOT = https://www.nexus-mobile.de/forum/github-implant/gate/
SOURCE = nexusomegac27/NEXUS-OMEGA-EVIDENCE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
WRITE_AUTHORITY = NONE
SCIENCE_PROMOTION_AUTHORITY = NONE
```

## Small scope, not an approval pipeline

**Scope is fixed to three original public interface assets**:
`research/forum/github-implant-20261012/site/index.html`,
`site/assets/github-implant.css`, and
`site/assets/github-implant.js`.

Browser retrieves each GitHub original via `GET /repos/{owner}/{repo}/contents/{file}?ref=main` and its own separately delivered HTTPS copy via `GET /forum/github-implant/{file}`, hashes exact decoded bytes with WebCrypto SHA-256 and compares both the digest and byte length. It also checks that the main HTML still displays `C1_DESCRIPTIVE_ONLY`. Source GitHub HEAD is a *separately observed* metadata stamp, not an immutable link binding to the 3 fetched sources in a concurrent-commit race; a returned source content SHA is a git blob field, not an independently trusted authority.

Known status vocabulary: `MATCH_C1`, `DIVERGENCE`, `HOLD_SOURCE`, `HOLD_WWW`, `HOLD_SCOPE`, `SCIENCE_WARN`, `HOLD_CRYPTO`. On `MATCH_C1`, all **three scoped bytes** matched at observation time; this does not imply all GitHub content has been copied to Hostinger, that a real scientific result is valid, or that signature/owner identity has been proved.

This is an **observability gate**, not a server-side request interceptor, content blocker, malware scanner or independent scientific adjudicator. Never claim it prevents distribution, validates GitHub's cryptographic signatures, certifies licenses/privacy on all repo files, or verifies hidden runtime dependencies. All operation is read-only HTTPS GET; no token, secrets, site mutation, event tracking, external JavaScript, inline HTML injection, agent roles, gate promotion, or automatic writes.

The browser monitor automatically checks at most once every 30 minutes while the tab is visible, with a 60-second manual cooldown. Existing Alpha-Node may run separate source-level research independently, not as a prerequisite for this status panel.

## Visual picture-in-picture (PiP) research

Verified sources: [MDN Document Picture-in-Picture API](https://developer.mozilla.org/en-US/docs/Web/API/Document_Picture-in-Picture_API) (HTTPS, user gesture, limited browser support);
[Floating UI](https://github.com/floating-ui/floating-ui) (MIT, open-source floating element/positioning primitives, *not itself native Document PiP*);
[react-rnd](https://github.com/bokuweb/react-rnd) (draggable/resizable React panel; unsuitable extra React dependency for existing vanilla page).

Selected implementation: no third-party libraries; fixed draggable status dock works on desktop and mobile, and the native Document PiP window opens on user click where supported. Otherwise dock fallback remains. PiP displays **only local gate status text**, not a foreign GitHub iframe or live external HTML. Close and keyboard controls remain available; no automatic new window.

## One-shot public WWW mount (existing Hostinger site only)

Already-deployed GitHub_Implant leaf URL is the source parent. Copy only the *new* four gate assets:
```text
site/gate/index.html        -> <existing-public_html>/forum/github-implant/gate/index.html
site/gate/gate.css          -> <existing-public_html>/forum/github-implant/gate/gate.css
site/gate/gate.js           -> <existing-public_html>/forum/github-implant/gate/gate.js
site/gate/gate-core.mjs     -> <existing-public_html>/forum/github-implant/gate/gate-core.mjs
```

The updated `site/index.html` adds exactly one small `Interface Gate` navigation link. **Do not overwrite unrelated Forum V0/index files or the homepage**. The existing Hostinger hPanel login path previously used for GitHub_Implant is the correct site-deploy channel when available to the authorized agent; AXIOM itself has no browser login or Hostinger file-manager token. Preserve backup and previous source blob; verify HTTP 200/MIME for all gate assets, source digests, mobile/desktop, visible network status and absence of unplanned homepage/forum changes. To claim `NODE_LIVE_VERIFIED`, provide a fresh receiver HTTP + SHA-256 receipt for gate assets and one actual browser check, not just a GitHub merge.

## Independent testing

`node --test research/forum/github-implant-20261012/tests/test_gate.mjs`

The contract checks 13 cases: fixed allowlist, base64 source decoding and length guards, hold behavior, divergence, C1 marker, URL safety, SHA256 known-answer. The API fetch/Hostinger HTTP pair is not simulated by those tests; real-browser smoke must follow live mount.

## Runtime independence

A recurring owner-level **read-only interface monitor** can run hourly without Hostinger credentials, performing only the same scoped three-source comparison and reporting material deviations; no gateway server, webhook, new external-agent slot, dedicated repository or GitHub Action workflow is necessary.

```text
NODE_RESET = NO
GITHUB_WRITE = NO
HOSTINGER_WRITE = NO
SCIENTIFIC_CLAIM_PROMOTION = NO
R19_INTERFERENCE = NO
```
