# Capability Census · Authenticated External GitHub Receiver · R3

**OBJECT:** `NEXUS_OMEGA_CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261030_R3`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_INDEPENDENT_RECEIVER_PILOT_READINESS_20261030_R0`  
**PARENT_ORDER_SHA256:** `dd0874f8a1ad112fd1ea824558436d4d957df3433c3aa2cd8b5fcde2e909618f`  
**PARENT_ORDER_COMMIT:** `7bc257103f3923dbfd633bc1f43ccb73de1b59bc`  
**PREDECESSOR_CENSUS_R2:** `CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261030_R2.md`  
**F12_ADJUDICATION:** `AXIOM_EXPERTENKODEX_F12_FINAL_POLICY_ADJUDICATION_20261030_R0.md` · `8966b6b7…` · 7832 / `c6632b91…`  
**AUTHORITY:** `OPERATOR_ALEXANDER_VIA_AXIOM`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**MODE:** `READ_ONLY_CENSUS`  
**DATE_UTC:** `2026-10-30`  
**LIVE_PILOT:** `NOT_AUTHORIZED`  
**NEW_EXTERNAL_PRINCIPAL:** `NOT_AUTHORIZED`

---

## Purpose

P1 of the Independent Receiver Pilot Readiness order: identify a *real existing* external GitHub principal distinct from `nexusomegac27` / Cursor producer, or document `ADAPTER_NOT_CONNECTED`. No invitations, app installs, tokens, or write slots.

---

## Observed principal surface (this bind)

| Probe | API / method | Result |
|-------|--------------|--------|
| Authenticated actor | `GET /user` | `login=nexusomegac27` · `id=281316431` · `type=User` |
| Collaborators | `GET /repos/…/collaborators` | `length=1` · only `nexusomegac27` · `permission=admin` |
| Invitations | `GET /repos/…/invitations` | `length=0` |
| Outside collaborators | org/user outside-collaborators | `404` / not available (user-owned repo) |
| GitHub App installation JWT | installation token route | `401` / not bound for this census |
| Distinct external login | — | **ABSENT** |

```text
PRODUCER_PRINCIPAL = nexusomegac27
CURSOR_PRODUCER = SAME_OWNER_ACCOUNT_SURFACE
DISTINCT_EXTERNAL_RECEIVER_LOGIN = NOT_ESTABLISHED
INVITATION_PENDING = NO
ADAPTER_STATUS = ADAPTER_NOT_CONNECTED
ADAPTER_INVENTION = PROHIBITED
TOKEN_INVENTION = PROHIBITED
WRITE_ACK_INVENTION = PROHIBITED
ACCOUNT_CREATE = PROHIBITED
APP_INSTALL = PROHIBITED
ACCESS_INVITATION = PROHIBITED_THIS_ORDER
```

---

## Required capability matrix (pilot readiness)

| # | Capability | Required | Observed | Gap |
|---|------------|----------|----------|-----|
| 1 | Authenticated GitHub identity ≠ `nexusomegac27` / Cursor producer | YES | NOT_ESTABLISHED | No distinct login bound |
| 2 | Proven auth route (OAuth App / GitHub App / collaborator with least privilege) | YES | NOT_ESTABLISHED | Provider not connected |
| 3 | Read access to PR #185 / exchange paths without Hostinger | YES | Producer only | External path absent |
| 4 | Comment or create-only return ability for that principal | YES (pilot) | NOT_PROVEN | Actor permission unknown until enroll |
| 5 | Independent fetch + SHA-256 rehash witness | YES | Schema prepared; live witness absent | EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED |
| 6 | F10 / F11 / F12 fail-closed preserved | YES | CLOSED (no regression observed) | No re-repair |
| 7 | `main` ruleset beyond generic `validate` | PARTIAL | Ruleset `21252293` · check=`validate` only | See owner decision packet |
| 8 | Hostinger / www for ACK | NO | Out of scope | — |

---

## Delta vs R2

```text
R2 = HOLD_C1_ADAPTER_NOT_CONNECTED (F12 parent order)
R3 = HOLD_C1_ADAPTER_NOT_CONNECTED (pilot-readiness parent)
DELTA =
  · Bound to PINNED_COMMIT 7bc257… and readiness order dd0874f8…
  · Collaborators / invitations re-probed this bind (still owner-only)
  · Explicit NEW_EXTERNAL_PRINCIPAL / LIVE_PILOT = NOT_AUTHORIZED
  · Pointer to ACK schema + ruleset decision packet (this package)
NO_FALSE_PROGRESS = REQUIRED
REPETITION_WITHOUT_MATERIAL_DELTA ≠ NEW_EVIDENCE
```

---

## Disposition

```text
STATE = HOLD_C1_ADAPTER_NOT_CONNECTED
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
EXTERNAL_PRINCIPAL = NOT_ESTABLISHED
GITHUB_MAIN_ENFORCEMENT = PARTIAL
F10 = CLOSED_PRESERVED
F11 = CLOSED_PRESERVED
F12 = CLOSED_EMPTY_REGISTER_DEFAULT_DENY_PRESERVED
NEXT_FOR_ACK_CYCLE =
  OPERATOR_CONTROLLED_RECEIVER_ENROLLMENT
  · THEN_DISTINCT_AUTHENTICATED_FETCH_REHASH
  · THEN_GITHUB_RETURN_ARTIFACT
  · THEN_AXIOM_INDEPENDENT_READBACK
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

---

## Epistemic walls

```text
CENSUS_R3 ≠ EXTERNAL_RECEIVER_ACK
CURSOR_GITHUB_READ ≠ INDEPENDENT_EXTERNAL_RECEIVER
OWNER_ADMIN_ONLY ≠ RECEIVER_CONNECTED
ADAPTER_NOT_CONNECTED ≠ LICENSE_TO_INVENT_ADAPTER
F12_CLOSED ≠ COMMUNICATION_INFRASTRUCTURE_TERMINAL
```
