# Receiver ACK Harness Plan · 20261030 R0

**OBJECT:** `NEXUS_OMEGA_RECEIVER_ACK_HARNESS_PLAN_20261030_R0`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_INDEPENDENT_RECEIVER_PILOT_READINESS_20261030_R0`  
**PARENT_ORDER_SHA256:** `dd0874f8a1ad112fd1ea824558436d4d957df3433c3aa2cd8b5fcde2e909618f`  
**SCHEMA:** `RECEIVER_INDEPENDENT_ACK_SCHEMA_V1.json`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**LIVE_PILOT:** `NOT_AUTHORIZED_THIS_ORDER`  
**DATA_ROUTE:** `GITHUB_ONLY`

---

## Goal

Define the exact fetch → rehash → ACK cycle a distinct authenticated GitHub principal must execute. No live enrollment and no ACK_PASS claim from this readiness package alone.

---

## Disposable PUBLIC-SAFE source package (pilot target)

```text
PACKAGE_OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_RECEIVER_PILOT_READINESS_ORDER_20261030_R0
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PINNED_COMMIT = 7bc257103f3923dbfd633bc1f43ccb73de1b59bc
PATH = research/communication/github-only-exchange-enforcement-20261029/AXIOM_CURSOR_GITHUB_RECEIVER_PILOT_READINESS_ORDER_20261030_R0.md
BYTES = 6512
SHA256 = dd0874f8a1ad112fd1ea824558436d4d957df3433c3aa2cd8b5fcde2e909618f
CLASS = PUBLIC_SAFE_ORDER_TEXT
HOSTINGER = OUT_OF_SCOPE
```

Alternate disposable pin (Expertenkodex V1):

```text
CODEX_COMMIT = b17d38266777bad61178e608d09e41726b9f4769
CODEX_PATH = docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md
CODEX_BYTES = 15388
CODEX_SHA256 = adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab
```

---

## Exact cycle (receiver-side)

1. **Auth** — Sign in as a GitHub principal with `distinct_from_producer=true` (not `nexusomegac27` / Cursor producer session). Auth route must be one of: OAuth App · GitHub App installation · collaborator session (least privilege). Document login + numeric user id.
2. **Fetch** — Prefer `GET /repos/{owner}/{repo}/contents/{path}?ref={commit}` (GitHub Contents API) or git blob by SHA. Do not use Hostinger/www. Record HTTP status and request ref.
3. **Decode** — Base64-decode content if Contents API; keep raw bytes for hash.
4. **Measure** — `BYTES = len(raw_bytes)`; `RECEIVER_OBSERVED_SHA256 = SHA256(raw_bytes)` (hex lowercase).
5. **Compare** — Match against declared `SOURCE_SHA256` and `BYTES`.
6. **Fill ACK** — All required fields from `RECEIVER_INDEPENDENT_ACK_SCHEMA_V1.json`.
7. **Return** — Publish ACK JSON (or equivalent structured comment) on GitHub only: PR #185 comment preferred; issue comment or PR file commit allowed per return-channel plan.
8. **Verdict** — `ACK_PASS` only if schema match rules hold. Otherwise use explicit FAIL/HOLD enum. Never promote producer self-rehash to `EXTERNAL_RECEIVER_ACK`.

---

## Suggested local command recipe (receiver machine)

```text
# PowerShell — receiver-controlled session only
$owner = "nexusomegac27"
$repo  = "NEXUS-OMEGA-EVIDENCE"
$ref   = "7bc257103f3923dbfd633bc1f43ccb73de1b59bc"
$path  = "research/communication/github-only-exchange-enforcement-20261029/AXIOM_CURSOR_GITHUB_RECEIVER_PILOT_READINESS_ORDER_20261030_R0.md"
$raw   = gh api "repos/$owner/$repo/contents/$path?ref=$ref" --jq .content
$bytes = [Convert]::FromBase64String(($raw -replace "`n",""))
$sha   = [System.BitConverter]::ToString(
           [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
         ).Replace("-","").ToLower()
"BYTES=$($bytes.Length)"
"SHA256=$sha"
```

Python equivalent:

```text
# python - uses gh stdout; receiver auth only
import base64, hashlib, json, subprocess
owner, repo, ref = "nexusomegac27", "NEXUS-OMEGA-EVIDENCE", "7bc257103f3923dbfd633bc1f43ccb73de1b59bc"
path = "research/communication/github-only-exchange-enforcement-20261029/AXIOM_CURSOR_GITHUB_RECEIVER_PILOT_READINESS_ORDER_20261030_R0.md"
body = subprocess.check_output(["gh","api",f"repos/{owner}/{repo}/contents/{path}?ref={ref}"])
content = json.loads(body)["content"]
raw = base64.b64decode("".join(content.split()))
print(len(raw), hashlib.sha256(raw).hexdigest())
```

---

## Fail-closed gates (F10–F12 preserved)

```text
F10 = LF/CRLF or path normalization must not invent MATCH
F11 = Expertenkodex header absent → fail closed (dispatch path unchanged)
F12 = empty grants[] + DEFAULT_DENY; authenticated:true alone ≠ grant
ACK harness MUST NOT invent legacy grants or mutate register
```

---

## Synthetic offline demo (this package)

```text
CLASS = SYNTHETIC_NOT_EXTERNAL
ACTOR = CURSOR_PRODUCER_LOCAL_REHASH
MAY_EMIT = local MATCH receipt labeled SYNTHETIC_NOT_EXTERNAL
MAY_NOT_EMIT = EXTERNAL_RECEIVER_ACK / ACK_PASS as external
See RECEIPT_SYNTHETIC_OFFLINE_RECEIVER_DEMO_20261030_R0.json
```

---

## Disposition

```text
HARNESS = DESIGN_BOUND_C1
LIVE_EXECUTION = NOT_AUTHORIZED_THIS_ORDER
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
NEXT = OPERATOR_CONTROLLED_RECEIVER_ENROLLMENT_THEN_LIVE_CYCLE
```
