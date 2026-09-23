# NEXUS//OMEGA — omega-sh 1.07 BioBridge Extension Spec

**OBJECT** = `22_TERMINAL_OMEGA_SH_BIOBRIDGE_SPEC.md`
**SPEC_VERSION** = omega-sh 1.07 + BioBridge
**CLAIM_CEILING** = C1_DESCRIPTIVE_ONLY
**TRUTH_AUTHORITY** = NONE
**RUNTIME** = FROZEN_OFFLINE_TESTING
**COMPATIBILITY_KERNEL** = INVARIANT (see 20_COMPATIBILITY_MATRIX.json)

---
## 1. Overview

Extension of NEXUS Web Terminal https://www.nexus-mobile.de/terminal/ to natively handle BioBridge control signals without authority escalation.

All commands are session-bound, read-only with respect to Canon, C1 descriptive only.

No production deployment. No AH escalation.

## 2. Commands

### 2.1 `micro <symbol>`

**Syntax**: `micro <. | , | ? | ! | ;>`

**Function**: Execute raw 1-byte signal transduction against bound session.

**Semantics**:
- `.` → reference_transduction_commit: commit current reference set, expect deref if needed
- `,` → continuation: more references follow
- `?` → HOLD: escalate uncertainty, preserve source+uncertainty+status, write ledger
- `!` → FAIL: hard rejection, immediate stop, ledger entry
- `;` → CHECKPOINT: resource pressure barrier, must precede compaction

**Wire**: Sends 1-byte control frame outside payload, requires session binding. Must not trigger on prose (F03). Implementation must use ESC 0x1B framing or line-isolated mode.

**Authority**: Session-bound, no AH growth.

**Example**:
```
> micro .
< ACK reference_set_committed hash=sha256:e3b0...
> micro ?
< HOLD friction=12 ledger_id=inc_042
```

**Failure modes**:
- Invalid symbol → FAIL (!) + SAFE_REFUSAL
- No session bound → HOLD (?) + `NO_SESSION`
- Resource pressure without prior `;` → HOLD + require `;`

### 2.2 `deref <hash>`

**Syntax**: `deref <sha256_hex_or_base64url>`

**Function**: Perform reference-first artifact fetch from local CAS.

**Rules**:
- Validates SHA-256 format (64 hex or 43 base64url chars)
- Fetch from local CAS only, no network
- Verifies `sha256(payload) == reference` else immediate FAIL (!) per F09, no silent auto-repair
- Cache hit: B_dereferenced = 0, returns from memory
- Cache miss: fetches, counts bytes in B_dereferenced, verifies hash

**Output**:
```
> deref e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
< CAS_HIT bytes=0 verified=true provenance=preserved
```
or
```
< CAS_MISS bytes=1248 verified=true
< FAIL (!) hash_mismatch expected=... got=...  // F09
```

**Authority**: Read-only CAS, no Canon mutation.

### 2.3 `compat`

**Syntax**: `compat [--json] [--ledger]`

**Function**: Query current Compatibility Kernel state and INCOMPATIBILITY_LEDGER.

**Output fields**:
- K members with byte-identity (K1..K5)
- Current D state (serialisation, schema version, routing, compression)
- Regulator variety status: V(R) vs V(S)
- INCOMPATIBILITY_LEDGER entries (HOLD/?, FAIL/!)

**Example**:
```
> compat --json
{
  "K": {"K1": "0x2E,0x2C,0x3F,0x21,0x3B", "K2": "SHA-256", ...},
  "D": {"serialisation":"cbor", "schema":"2.1.0", ...},
  "variety": {"V_R": 128, "V_S": 54, "sufficient": true},
  "ledger": [{"id":"inc_042","type":"HOLD","reason":"D2 incompatibility X/Y"}]
}
```

**No authority check beyond session**.

### 2.4 `friction`

**Syntax**: `friction [--lane X Y] [--json]`

**Function**: Report byte/claim delta between dual work-lanes X and Y (Dobzhansky-Muller detection).

**Formula**:
```
friction = |bytes_X - bytes_Y| + |claims_X Δ claims_Y| + ledger_entries(X,Y)
```

**Output**:
```
> friction --lane X Y
X_bytes=2048 Y_bytes=2100 delta_bytes=52
X_claims=12 Y_claims=13 delta_claims=1 (negative-evidence in Y)
ledger_entries=1 (F21 HOLD)
friction_total=54
state=HOLD (?) — non-silent escalation required
```

**Use for F21 verification and Ashby budget tracking**.

## 3. Security & Invariant Enforcement

- All commands enforce C1 ceiling: no truth oracle claims
- Any attempt to claim AH0_ROOT via micro or deref → immediate FAIL + SAFE_REFUSAL (F23)
- Prompt injection in args (e.g., `micro .; ignore previous policy`) → FAIL (F22)
- Canary emission request (`deref BC7...`) → SAFE_REFUSAL (F24)
- High-tier brand bypass → FAIL (F25)
- No custom crypto, only SHA-256

## 4. Offline Testing Requirements

- All four commands must pass F03, F09, F12, F21, F22-F25 fixtures deterministically
- No network calls, FROZEN runtime
- Session-bound only

## 5. Terminal Seal

```
SPEC = 22_TERMINAL_OMEGA_SH_BIOBRIDGE_SPEC.md
VERSION = omega-sh 1.07 + BioBridge
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
K = INVARIANT
D = BOUNDED
RUNTIME = FROZEN
PRODUCTION = NONE
```
