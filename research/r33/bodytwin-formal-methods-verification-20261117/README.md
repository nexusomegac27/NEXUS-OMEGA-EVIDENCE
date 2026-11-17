# R33 BodyTwin Formal Methods Verification (C1 Offline Candidate)

**Object:** `NEXUS_OMEGA_CURSOR_R33_RESIDUAL_GATES_C1_OFFLINE_BODYTWIN_METHODS_COMPLETION_20261117_R1`  
**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`  
**BODYTWIN_VALIDATED:** `NO`  
**CONSENT_BIND:** `OPEN`

## Scope

Additive offline methods candidate under residual order R1:

- SOURCE_EXACT capsule + schema + contract from sealed MAXI / PR368
- Deterministic offline renderer (double-pass SHA match)
- Cursor-own Non-Lean oracle + Stage C negatives (N01–N07)
- No Lean kernel claim; no rfc8785 vendor runtime claim
- No Hostinger/www write; no PR merge from this branch alone

## Layout

- `data/` — SOURCE_EXACT inputs (capsule 8730 / `e5448d0c…`)
- `src/render_methods_offline.py` — deterministic offline renderer
- `tests/test_negatives_r1.py` — N01–N07 negatives
- `receipts/` — schema, renderer, negatives, C4 SOURCE_GAP

## Epistemic walls

```text
HASH_MATCH ≠ SCIENTIFIC_TRUTH
OFFLINE_CANDIDATE ≠ BODYTWIN_VALIDATED
NEGATIVES_PASS ≠ CLINICAL_VALIDATION
LEAN_ABSENT → NOT_RUN_TOOLCHAIN_GAP
RFC8785_WHEEL_DIGEST ≠ AUTHENTICATED_INSTALL
```
