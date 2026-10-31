# G7 — GitHub Implant Path / 404 Analysis

**OBJECT:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_ONLY_EXCHANGE_ENFORCEMENT_20261029_R1`  
**GATE:** `G7`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**STATE:** `PASS_WITH_CAVEATS_C1_MOUNT_CONTRACT_CLARIFIED_NO_WWW_WRITE`

## Live HEAD probes (report-level)

Base: `https://www.nexus-mobile.de/forum/github-implant/`

| URL | HTTP |
|---|---:|
| `/forum/github-implant/` (index) | 200 |
| `/forum/github-implant/assets/github-implant.js` | 200 |
| `/forum/github-implant/assets/github-implant.css` | 200 |
| `/forum/github-implant/github-implant.js` (bare, non-canonical) | 404 |
| `/forum/github-implant/github-implant.css` (bare, non-canonical) | 404 |

## Source contract

Checkout file `research/forum/github-implant-20261012/site/index.html` references:

```text
./assets/github-implant.js
./assets/github-implant.css
```

## Root cause (bounded)

Prior “JS/CSS 404” reports conflated **non-canonical bare filenames** with the **mounted `/assets/` paths**. Canonical relative refs under `/assets/` resolve live HTTP 200. Bare paths without `/assets/` are expected 404 under current mount.

## Repair design (isolated; not deployed)

1. Keep index refs as `./assets/…` only.
2. Document mount contract: implant assets must be published under `/forum/github-implant/assets/`.
3. Optional defensive redirect/alias for bare filenames — **requires separate Hostinger/www write ACK** (not granted this bind).

## Explicit non-actions

```text
HOSTINGER_PRODUCTION_WRITE = NO
WWW_PRODUCTION_WRITE = NO
IMPLANT_REDEPLOY = NO
WRITE_ACK_INVENTED = NO
```

## Verdict

`G7 = PASS_WITH_CAVEATS_C1_MOUNT_CONTRACT_CLARIFIED_NO_WWW_WRITE`
