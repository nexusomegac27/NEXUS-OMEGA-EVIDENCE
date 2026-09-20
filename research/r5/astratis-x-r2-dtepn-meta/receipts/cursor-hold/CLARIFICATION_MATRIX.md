# Clarification Matrix — Astratis X / R2 Push Gate

```text
OBJECT = NEXUS_OMEGA_CURSOR_ASTRATIS_X_R2_CLARIFICATION_MATRIX_20260920_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PUSH = NO
```

| # | Issue | Independent Cursor finding | Classification | Closure invented? | Push impact |
|---|---|---|---|---|---|
| 1 | Final ZIP hash `e19f149c…` | Archive + worker snapshot both MATCH; 94 entries; 372681 uncompressed | TRANSPORT_PASS | No | Non-blocking |
| 2 | Empty `history/*.zip` (22 B, 0 entries, `8739c76e…`) | Confirmed placeholders; external R0 `f0490d…` / 87810 B bound by path+hash | SOURCE_GAP_PLACEHOLDER | No | Non-blocking for documented C1 transport; blocking for R7 seal |
| 3 | Named R1 predecessor ZIP | `NEXUS_OMEGA_KAUSAL_KANONISCH_R5_R6_GESAMTPAKET_20260920_R1.zip` not found in audited custody | SOURCE_GAP | No | Blocking for R7 seal only |
| 4 | 12 same-named packaged returns | All 12 byte-unequal vs real Cursor return | DERIVATIVE_UNKNOWN_TRANSFORM | No | Blocking if package claimed as Cursor byte provenance |
| 5 | Missing EXECUTIVE in ZIP | ABSENT; real Executive `8de196bd…` bound externally | SOURCE_GAP | No | Blocking for package-as-complete-return claim |
| 6 | `[STRIPPED …]` IDs (7 files) | Present; unstripped external identities NOT_FOUND; names not invented | IDENTITY_REDACTION_SOURCE_GAP | No | Blocking for R6/R7 object seal |
| 7 | FILE_02 91-hex field | Erratum written; correct `c72fb3ed…` | ERRATUM | No (append-only) | Non-blocking after erratum |
| 8 | Hash domain mixing | Domains separated in CHAIN_RECONCILIATION | CLARIFIED | No | Non-blocking |
| 9 | Expert DONE / adjudication DONE in package text | SOURCE_REPORTED_NOT_INDEPENDENTLY_VERIFIED | OPEN | No | Blocking for R7 seal |
| 10 | Future-dated receipt timestamps | Preserved as TIMESTAMP_UNVERIFIED | OPEN | No | Non-blocking for this HOLD |
| 11 | R2 target handshake | Candidate repo reachable; R2 path/allowlist/branch NOT_BOUND | HOLD_TARGET_NOT_BOUND | No | **Blocks PUSH** |

## Gate vector

```text
INDEPENDENT_CURSOR_REHASH = MATCH
CHAIN_RECONCILIATION = RECORDED_WITH_EXACT_SOURCES_AND_EXPLICIT_OPEN_GAPS
FALSE_CLOSURE_OR_FALSE_PRODUCER_ATTRIBUTION = NONE
CURRENT_R2_TARGET_HANDSHAKE = NOT_BOUND
=> PUSH = NO
```
