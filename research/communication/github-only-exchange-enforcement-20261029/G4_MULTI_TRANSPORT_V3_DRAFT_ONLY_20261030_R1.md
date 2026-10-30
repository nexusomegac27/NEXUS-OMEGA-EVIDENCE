# G4 Multi-Transport V3 · DRAFT ONLY · 20261030_R1

OBJECT: `NEXUS_OMEGA_G4_MULTI_TRANSPORT_V3_DRAFT_ONLY_20261030_R1`  
STATE: `DRAFT_ONLY`  
IMPLEMENTATION_SHIP: `NO`  
CLAIM_CEILING: `C1_DESCRIPTIVE_ONLY`

## Modular receive channel (shipped now)

Loopback HTTP POST `/checkin` + append-only ledger. Optional future cryptographic signature field reserved as:

```text
signature_alg = OPTIONAL_FUTURE
signature_b64 = OPTIONAL_FUTURE
public_key_ref = OPTIONAL_FUTURE
```

Not required for STAGED_UNTRUSTED. Unsigned anonymous check-ins remain valid as observation.

## V3 draft transports (not activated)

| Transport | Status |
|-----------|--------|
| Loopback HTTP | ACTIVE_LOCAL_STAGING |
| GitHub comment return channel | DESIGNED · EXTERNAL_PRINCIPAL=NOT_ESTABLISHED |
| Hostinger public write API | HOLD |
| Signed envelope V3 | DRAFT_ONLY |

## Law

```text
MULTI_TRANSPORT_V3 = DRAFT_ONLY
DRAFT ≠ SHIPPED
OPTIONAL_SIGNATURE ≠ REQUIRED_FOR_CHECKIN
NO_PARALLEL_FRAMEWORK
```
