# RESULT · Expertenkodex F12 Legacy-Grant Hard Close · R0

**OBJECT:** `NEXUS_OMEGA_CURSOR_EXPERTENKODEX_F12_LEGACY_GRANT_HARD_CLOSE_RETURN_20261030_R0`  
**ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_F12_LEGACY_GRANT_HARD_CLOSE_ORDER_20261030_R0`  
**ORDER_PATH:** `research/communication/github-only-exchange-enforcement-20261029/AXIOM_CURSOR_F12_LEGACY_GRANT_HARD_CLOSE_ORDER_20261030_R0.md`  
**ORDER_BYTES:** `4651`  
**ORDER_SHA256:** `51a4c9d77e0191dd9bc5ac5df7585edb45b696690700a0e19435093ba29c4d96`  
**ORDER_REHASH:** `MATCH`  
**ADJUDICATION:** `AXIOM_F10_F11_RECEIVER_POLICY_ADJUDICATION_20261030_R0.md`  
**ADJUDICATION_BYTES:** `8059`  
**ADJUDICATION_SHA256:** `ac5c3264de11fc647090ba87f8cdb9f37f3f9362861820b9eb42092ea0ad0810`  
**ADJUDICATION_REHASH:** `MATCH`  
**EXPERTENKODEX_V1:** `docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md`  
**EXPERTENKODEX_BYTES:** `15388`  
**EXPERTENKODEX_SHA256:** `adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab`  
**EXPERTENKODEX_REHASH:** `MATCH`  
**BASE_TIP_AT_INTAKE:** `906569a720d6c26c13b82d323a5e8d7e234d4103`  
**AUTHORITY:** `OPERATOR_ALEXANDER_VIA_AXIOM`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**DATA_ROUTE:** `GITHUB_ONLY`  
**PR:** `#185` · `DRAFT` · `NO_AUTO_MERGE`  
**NATIVE_APP_R3:** `HOLD`

---

## Terminal state

```text
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_F12_HARD_CLOSED_LOCAL
F10 = INDEPENDENTLY_CLOSED_PRESERVED
F11 = DEFAULT_DISPATCH_FAIL_CLOSED_PRESERVED
F12 = HARD_CLOSED_OWNER_REGISTER_DEFAULT_DENY
SELF_ASSERTED_LEGACY_GRANT = REJECTED
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
GITHUB_MAIN_ENFORCEMENT = PARTIAL
CURSOR_ACTION = NONE
NEXT = AXIOM_INDEPENDENT_FINAL_POLICY_REVIEW
```

---

## G0 · Intake

| Artifact | Bytes | SHA-256 | Rehash |
|----------|------:|---------|--------|
| F12 Order | 4651 | `51a4c9d77e0191dd9bc5ac5df7585edb45b696690700a0e19435093ba29c4d96` | MATCH |
| F10/F11 Adjudication | 8059 | `ac5c3264de11fc647090ba87f8cdb9f37f3f9362861820b9eb42092ea0ad0810` | MATCH |
| Expertenkodex V1 | 15388 | `adf69aa393afc97773fe9a00628cdd1c3b6bfcfba9d40f179ed15915deb789ab` | MATCH |

Parent tip at intake: `906569a720d6c26c13b82d323a5e8d7e234d4103` (AXIOM F10/F11 adjudication + F12 order commits). F10/F11 not reopened.

---

## G1–G2 · F12 remediation

### Defect closed

`F12_SELF_ASSERTED_LEGACY_GRANT_AUTHENTICATION_BYPASS` — incoming manifests that set `authenticated: true` plus classification/IDs were previously treated as authorized legacy grants without owner-verified register match.

### Repair

1. Removed `_is_authenticated_legacy_grant` self-trust path from `scripts/nexus_github_exchange_chain.py`.
2. Added `LegacyGrantRegistry` — evaluates only against owner-controlled register; empty grants → `LEGACY_GRANT_DEFAULT_DENY`.
3. Added production register `docs/governance/EXPERTENKODEX_LEGACY_GRANT_REGISTER_V1.json`:

| Field | Value |
|-------|-------|
| Bytes | 950 |
| SHA-256 | `3bb2b28ca3c648780242d54c4a9814467d8ca38ffddaf27afee47027309bcdcd` |
| `grants` | `[]` |
| `default` | `DENY` |

4. Fail codes bound: `LEGACY_GRANT_DEFAULT_DENY` · `NOT_IN_REGISTER` · `FIELD_MISMATCH` · `SELF_ASSERTED_REJECTED` · `EXPIRED` · `REVOKED` · `MALFORMED`.
5. Success path only via injected owner-verified fixture match → `expertenkodex=LEGACY_GRANT_ACCEPTED`, `legacy_grant_source=OWNER_VERIFIED_REGISTER`.
6. Unauthenticated / absent Expertenkodex remains `MISSING_EXPERTENKODEX` (F11 preserved).

### Local tests

```text
pytest tests/test_nexus_github_exchange_chain.py tests/test_nexus_expertenkodex_v1.py
= 86_PASSED
TestF12 = 8_METHODS
TestF11 = 5_METHODS (DEFAULT_DENY preserved)
```

---

## G3 · Tip CI (separated from ruleset)

Pre-push tip `906569a…` (AXIOM head before this Cursor return):

```text
CHECK_RUNS_AT_906569a = 9_OF_9_SUCCESS
NOTE = Honest count at that tip; not claimed as 10/10 for 906569a
PRIOR_CURSOR_TIPS_90ac033_AND_bcdba870 = 10_OF_10_AS_AXIOM_STATED_PRESERVED
```

Post-push CI for this return tip: recorded in STRUCTURE / PR after push (`github_ci_this_tip`).

---

## G4 · GitHub ruleset (read-only; not mutated)

| Parameter | Observed |
|-----------|----------|
| Ruleset | `main-evidence-protection` |
| ID | `21252293` |
| Required checks | `validate` only |
| `require_code_owner_review` | `false` |
| `required_approving_review_count` | `0` |

```text
GITHUB_MAIN_ENFORCEMENT = PARTIAL
PLAN_NOT_EXECUTED =
  Add required checks beyond validate when Operator/AXIOM orders
  · Enable require_code_owner_review when Operator/AXIOM orders
MUTATION_OF_RULESET_THIS_BIND = NO
```

---

## G5 · External receiver census

See `CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261030_R2.md`.

```text
ADAPTER_STATUS = ADAPTER_NOT_CONNECTED
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
INVENTION = PROHIBITED
```

---

## G6 · Return surface

```text
DATA_ROUTE = GITHUB_ONLY
PR185 = DRAFT · NO_AUTO_MERGE
CHAT = CANONICAL_HANDSHAKE_ONLY
NATIVE_APP_R3 = HOLD
```

---

## Epistemic walls

```text
F12_LOCAL_HARD_CLOSE ≠ EXTERNAL_RECEIVER_ACK
F12_LOCAL_HARD_CLOSE ≠ FULL_MAIN_ENFORCEMENT
EMPTY_REGISTER_DEFAULT_DENY ≠ LICENSE_TO_SELF_ASSERT
HASH_MATCH ≠ SCIENTIFIC_TRUTH
9_OF_9_AT_906569a ≠ 10_OF_10_CLAIM_FOR_THAT_TIP
PRIOR_10_OF_10_AT_CURSOR_TIPS ≠ THIS_RETURN_TIP_CI
```

---

## Prohibitions observed

- No Hostinger/www write  
- No invent WRITE_ACK / adapter / tokens  
- No PR auto-merge  
- No F10/F11 reopen  
- No NATIVE_APP_R3 reopen  
- Claim ceiling C1 preserved  
