# NEXUS OMEGA — AXIOM Gate V2 Scoped Remediation + WWW Release Order (2026-11-07)
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_GATE_V2_SCOPED_REMEDIATION_AND_WWW_RELEASE_ORDER_20261107_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = AUTHORIZED_SCOPED_GATE_V2_C1_READ_ONLY_RELEASE_AFTER_GATES
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
PRIOR = NEXUS_OMEGA_AXIOM_GATE_AUDIT_ADJUDICATION_20261107_R0
CURSOR_PRIOR_RESULT = ACCEPT_CURSOR_RECEIPT_WITH_CAVEATS_C1
PRIOR_RETURN_ZIP = 4347 / b901ced243c538dce3fd90ea773112b5dcc0d48977e49080ef09dadfb7c311d6 (reported; not rehashed by this AXIOM Chat)
PRIOR_MANIFEST_LOCAL_AX_REHASH = 5/5 MATCH
PRIOR_WWW_GATE = ABSENT_404_CURSOR_WITNESSED_5_OF_5
PRIOR_404_BODY = 4511 / e7db95c97a5d45787cc3e40cbcb93b748fefc65bc14e162c746e37f979861729
SOURCE_BRANCH = axiom/gate-v2-commit-pinned-release-witness-20261107-r0
SOURCE_BASE = 200012734e9cea7156d1ef1c7e04ad50448842a0 (R11 evidence PR #320 head)
SOURCE_REPO = nexusomegac27/NEXUS-OMEGA-EVIDENCE
SOURCE_SITE = research/forum/github-implant-20261012/site/
SOURCE_DEPLOYED_ROUTE = https://www.nexus-mobile.de/forum/github-implant/gate/

## 0. Claim and custody separation
R11_STATIC_C1 = PRESERVE; R12_OFFLINE_VERIFIER = PRESERVE; R10_HEARTBEAT = NOT_STARTED.
N34_CANONICAL = PARTIAL_2_OF_5; G11=HOLD; N33=OPEN; STAGE2_316=HOLD_NO_START.
NO_R11_R12_REWRITE; NO_MAIN_BLIND_MERGE; NO_RUNTIME; NO_SECRETS; NO_CLAIM_PROMOTION; NO_GITHUB_AGENT_WRITE; NO_UNSCOPED_DEPLOY.
A C1 browser byte comparison is not an authenticated witness, an atomic clock, a cryptographic assertion of identity, or a proof of deployed CI.

## 1. Source-exact intake
Get the exact GitHub V2 branch HEAD sha (full 40 chars). Verify its parent lineage to original PR320 head and fetch all 10 allowlist files under SOURCE_SITE. Verify new gate scripts, index, CSS, parent artifacts. R11 WWW currently published source may differ from main: do NOT compare target to moving main for an acceptance decision. Do not reconstruct missing sources.
Read previous Audit Return; do not erase the prior Cursor Knowledge Bind. Only register a new scoped tip.

## 2. Static validation in disposable sandbox (must run on Cursor/Windows)
- node --check site/gate/gate-core.mjs ; node --check site/gate/gate.js
- node --test site/gate/gate.test.mjs (54 defined tests; count actual tests)
- python -m unittest tests/test_gate_release_builder.py (4 design tests if present)
- Check DLP (no tokens, credentials, private paths, raw BodyTwin). Check CSP, no inline scripts, no external JavaScript.
- Negative tests must cover stale after hidden/resume, main vs release ref divergence, missing release file, missing GitHub API, malformed base64, time of observation unverified, release manifest tampering.

## 3. Source to WWW release manifest (NO invented signer)
Run source-tree generator (without network):
python research/forum/github-implant-20261012/build_gate_release_v2.py --source-root research/forum/github-implant-20261012/site --commit <FULL_V2_GITHUB_HEAD_SHA>
Generator emits site/gate/release-v2.json (NOT signed; not a trust authority). 10 file hashes and lengths are computed from the actual post-checkout bytes. Verify all source files are present and unchanged, including R11 CSS/JS/JSON and main index; source ref points to the exact GitHub V2 head.

## 4. Scope-preserving Hostinger staging
1. Read-only discover the actual existing Hostinger deploy document root and existing R11 release receipt. DO NOT assume an unverified host path.
2. Independently HTTP-download the six parent assets specified by manifest, compare them to pinned source. If any R11 parent asset differs, HOLD_PARENT_RELEASE_MISMATCH and return evidence; DO NOT silently overwrite the already-sealed R11 public release.
3. Create isolated *staging* with the four Gate files gate/index.html, gate/gate.css, gate/gate.js, gate/gate-core.mjs plus gate/release-v2.json; do NOT publish gate.test.mjs or Python generator.
4. Validate URLs, MIME text/html and JS modules (no 404), SHA-256 of the five stage files, CSP headers/no public secrets, rollback snapshot of any overwritten Gate files. A GitHub push is NOT a Hostinger deploy.
5. Publish only the bounded Gate directory when staging/DLP/static checks PASS and parent assets match. Use atomic rename or safe reversible equivalent; keep previous 404/previous Gate assets as rollback evidence.
6. Do not modify /forum/github-implant/ parent index, JS or temporal assets in this scoped release. No overwrite of R11 or R12.

## 5. Independent WWW acceptance
Observe separately: GitHub exact source HEAD; Hostinger deployment receipt; HTTP status and full SHA-256 bytes for Gate index/css/js/core and release-v2.json; same for six parent assets; browser DOM and JS execution status. Require ten Gate browser compare rows and 10/10 MATCH and C1 marker on both indexed HTMLs, current observation device-clock-unverified. Induce synthetic/no-side-effect negatives (GitHub unavailable => HOLD_SOURCE, missing manifest => HOLD_RELEASE_BIND, mismatched bytes => DIVERGENCE, hidden tab => STALE, no WebCrypto => HOLD_CRYPTO, throttled request => HOLD; no raw site failure chaos without operator permission).
If HTTP or browser succeeds only partially, return honest PARTIAL/HOLD with exact layer. Never claim PASS_WWW_GATE_C1 from a 404-body checksum.

## 6. Return contract
Return ZIP+.sha256 in existing NEXUS_OMEGA_TRANSFER/10_TO_AXIOM with 00_EXECUTIVE,10_HANDSHAKE,20_EPISTEMIC_WALLS,30_RESULT,40_MACHINE,99_SHA256SUMS. Bind:
SOURCE_HEAD+PARENT, GATE_CODE_SHA256, STATIC_TESTS, DLP, HOSTINGER_STAGING+DEPLOY_RECEIPT, HTTP_STATUS/BYTES/HASH/HEADERS, BROWSER_WITNESS incl device clock quality and 10/10 statuses, negative fixtures, rollback object, scope preservation.
If Hostinger capability or credentials unavailable, mark HOSTINGER_EXECUTION_GAP and return SOURCE_READY_DEPLOY_PENDING. Never invent deployment.
CURSOR_ACTION = SCOPED_GATE_V2_RELEASE_AFTER_GATES (new explicit operator demand for tangible progress).
