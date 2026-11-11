# R27-Sandbox Public Gate · exact Hostinger leaf mount contract

OBJECT = NEXUS_OMEGA_R27_SANDBOX_GITHUB_WWW_PARITY_MOUNT_ORDER_20261111_R0
AUTHORITY = OPERATOR_APPROVED_R27_PUBLIC_SAFE_PUSH
TARGET_GATE = https://www.nexus-mobile.de/forum/github-implant/gate/
TARGET_LEAF = https://www.nexus-mobile.de/forum/github-implant/gate/sandbox/
GITHUB_PUBLIC_SOURCE = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/tree/main/research/r27/sandbox-science-library-20261111
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Files to deploy, with existing site unchanged

- `research/forum/github-implant-20261012/site/gate/sandbox/index.html` -> `<existing_approved_hostinger_public_root>/forum/github-implant/gate/sandbox/index.html`
- `research/forum/github-implant-20261012/site/gate/sandbox/sandbox.css` -> `<...>/forum/github-implant/gate/sandbox/sandbox.css`
- `research/forum/github-implant-20261012/site/gate/sandbox/library.json` -> `<...>/forum/github-implant/gate/sandbox/library.json`
- Updated `research/forum/github-implant-20261012/site/gate/index.html` -> existing `<...>/forum/github-implant/gate/index.html` (**one additive sandbox navigation card only**)

The existing `gate.css`, `gate.js` and `gate-core.mjs` are unchanged. The three-file original GitHub↔WWW Implant comparator also remains unchanged: do not increase its scoped check to four or misstate parity.

## Hostinger privileged deployment / independent readback

1. Inspect actual Hostinger site target and backup all four target paths; record pre-deploy SHA256 or NOT_PRESENT and prior deployment/rollback identifier. Do not write homepage, `/forum/index.html`, DNS, or other modules.
2. Use already authorized existing Hostinger hPanel/SSH deployment channel. Do not paste passwords into repo or browser page, and do not expose private zip contents. Publish only listed 4 public-safe source files, atomically if provider supports it.
3. Independent remote HTTPS GET (prefer a second process/observer) must check index, css, json and Gate index: HTTP 200, proper MIME, SHA256 and byte lengths match *published GitHub main source commit*. Verify CSP HTTP headers (especially `frame-ancestors` cannot be proven with meta alone), focus/keyboard, mobile 375px, desktop 1440px, and no accidental resource links to private files.
4. Recheck unchanged homepage and forum paths; on mismatch rollback atomically and record failure. For no Hostinger site API/SSH capability, record `HOSTINGER_DEPLOY_CAPABILITY_GAP`; PR/commit alone is NOT a live deployment.
5. Binding must explicitly state timestamp, Git commit, site response hashes, source hash mapping, operator scope, and whether website parity observed. No Self-ACK or invented live source status.

## Independent expert guidance

Link the source-controlled unassigned mandate under `research/r27/sandbox-science-library-20261111/orders/NEUTRAL_EXPERT_RESEARCH_MANDATE.md`. `R27_PUBLIC_INTERFACE_GITHUB=SOURCE_READY`; `R27_WWW_GATE=AWAIT_REAL_DEPLOY_RECEIPT`; `SANDBOX_RUNTIME=NOT_STARTED`.
