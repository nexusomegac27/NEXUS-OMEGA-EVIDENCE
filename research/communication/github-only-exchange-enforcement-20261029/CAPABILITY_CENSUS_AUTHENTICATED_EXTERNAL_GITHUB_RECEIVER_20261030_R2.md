# Capability Census · Authenticated External GitHub Receiver · R2

**OBJECT:** `NEXUS_OMEGA_CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261030_R2`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_F12_LEGACY_GRANT_HARD_CLOSE_ORDER_20261030_R0`  
**PARENT_ORDER_SHA256:** `51a4c9d77e0191dd9bc5ac5df7585edb45b696690700a0e19435093ba29c4d96`  
**PREDECESSOR_CENSUS_R1:** `CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261029_R1.md`  
**AUTHORITY:** `OPERATOR_ALEXANDER_VIA_AXIOM`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**MODE:** `READ_ONLY_CENSUS`  
**DATE_UTC:** `2026-10-30`

---

## Purpose

G5 of the F12 hard-close order requires a read-only census of what is still needed for a genuine independent external ACK cycle after F12 closes the self-asserted legacy-grant bypass. This document does not invent adapters, tokens, or WRITE_ACK.

---

## Required capability for EXTERNAL_RECEIVER_ACK = ESTABLISHED

| # | Capability | Required | Observed (this bind) | Gap |
|---|------------|----------|----------------------|-----|
| 1 | Authenticated GitHub identity of a distinct external receiver (not Cursor producer, not Operator-only) | YES | NOT_ESTABLISHED | No separate authenticated receiver actor bound |
| 2 | Scoped read (and optional comment) access to PR #185 / Evidence paths without Hostinger | YES | Producer Cursor can read; independent external receiver path absent | ADAPTER_NOT_CONNECTED |
| 3 | Deterministic receipt: path + bytes + SHA-256 of ACK artifact on GitHub | YES | Producer returns exist; independent ACK artifact absent | EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED |
| 4 | Fail-closed Expertenkodex header on inbound dispatch (F11) | YES | PASS_LOCAL (DEFAULT_DISPATCH_FAIL_CLOSED) | Closed for standard dispatch |
| 5 | Fail-closed legacy grant path (F12) | YES | PASS_LOCAL (empty owner register → DEFAULT_DENY) | Closed for production path this bind |
| 6 | Branch protection / required checks on `main` covering Evidence integrity | PARTIAL | Ruleset `main-evidence-protection` (id `21252293`): required check = `validate` only; `require_code_owner_review=false`; `required_approving_review_count=0` | GITHUB_MAIN_ENFORCEMENT = PARTIAL |
| 7 | Hostinger / www write for ACK cycle | NO | Not required for GitHub-only route | Out of scope |

---

## Disposition

```text
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
ADAPTER_STATUS = ADAPTER_NOT_CONNECTED
ADAPTER_INVENTION = PROHIBITED
TOKEN_INVENTION = PROHIBITED
WRITE_ACK_INVENTION = PROHIBITED
NEXT_FOR_ACK_CYCLE =
  OPERATOR_OR_AXIOM_MUST_BIND_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER
  · THEN_INDEPENDENT_ACK_ARTIFACT_ON_GITHUB
  · THEN_AXIOM_INDEPENDENT_FINAL_POLICY_REVIEW
```

---

## Epistemic walls

```text
F12_LOCAL_PASS ≠ EXTERNAL_RECEIVER_ACK
CURSOR_GITHUB_READ ≠ INDEPENDENT_EXTERNAL_RECEIVER
EMPTY_LEGACY_REGISTER ≠ EXTERNAL_ACK
RULESET_VALIDATE_ONLY ≠ FULL_MAIN_ENFORCEMENT
ADAPTER_NOT_CONNECTED ≠ LICENSE_TO_INVENT_ADAPTER
```

---

## Terminal census state

```text
STATE = HOLD_C1_ADAPTER_NOT_CONNECTED
F10 = INDEPENDENTLY_CLOSED
F11 = DEFAULT_DISPATCH_FAIL_CLOSED
F12 = HARD_CLOSED_LOCAL_OWNER_REGISTER_DEFAULT_DENY
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
