# NEXUS OMEGA · PREPILOT · THREE-LANE PILOT DECISION (ONE PAGE)

**OBJECT:** `NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_THREE_LANE_PILOT_DECISION_20261031_R0`  
**PARENT:** `NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_FINAL_REPAIR_ORDER_20261031_R0` §60  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**AUTHORITY:** `OPERATOR_ALEXANDER_VIA_AXIOM` (decision deferred to AXIOM readback)  
**CURSOR_ROLE:** prepare lanes only; no dispatch

## Lane A — Local synthetic replay (ALLOWED NOW)

| Item | Value |
|------|-------|
| Scope | Local Node/test harness; fixtures under `examples/open-neutral-checkin/fixtures/` |
| Status this bind | EXECUTED as suite `46/0` PASS (local) |
| External contact | NO |
| Public write | NO |
| Claim | LOCAL_PREPILOT_REFERENCE only; not scientific validation |

## Lane B — External read-only noncanonical (LATER)

| Item | Value |
|------|-------|
| Scope | Read-only fetch of public Agent Border / GitHub blob URLs |
| Status this bind | NOT_EXECUTED |
| May become | Noncanonical observation receipt under separate Operator order |
| Must not | POST, cookie write, or treat HTTP 200 as validation |

## Lane C — Public ACK / write (HOLD)

| Item | Value |
|------|-------|
| Scope | Any public check-in write API / Agent Border POST / external agent invite |
| Status | HOLD |
| PUBLIC_EXTERNAL_WRITE_API | HOLD |
| FIRST_AGENT_TESTS | NOT_EXECUTED |
| PR185 | OPEN_DRAFT_NO_AUTO_MERGE |

## Decision matrix (this bind)

```text
LANE_A = LOCAL_SYNTHETIC_REPLAY_ALLOWED_AND_USED
LANE_B = DEFERRED_READ_ONLY_NONCANONICAL
LANE_C = HOLD
PILOT_STIMULUS = PREPARED_NOT_DISPATCHED
RECOMMENDATION_TO_AXIOM = KEEP_LANE_C_HOLD_UNTIL_SEPARATE_WRITE_ACK
```

## Epistemic walls

```text
SUITE_46_OF_0 ≠ FIRST_AGENT_TESTS
HTTP_200 ≠ VALIDATION
STIMULUS_PREPARED ≠ DISPATCHED
PR185_DRAFT ≠ MERGED
```
