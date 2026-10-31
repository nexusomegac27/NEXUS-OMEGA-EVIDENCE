# F10 · Task-Anchor Discrepancy Witness (append-only)

**OBJECT:** `NEXUS_OMEGA_F10_TASK_ANCHOR_DISCREPANCY_WITNESS_20261029_R1`
**PARENT:** `NEXUS_OMEGA_AXIOM_EXPERTENKODEX_V1_INDEPENDENT_ADJUDICATION_20261029_R1`
**ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1`
**AUTHORITY:** `OPERATOR_ALEXANDER_VIA_AXIOM`
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`
**CREATED_UTC:** `2026-10-29T21:20:00Z`
**ERASE_HISTORICAL:** `NO`

## Scope

Bind BOTH reported Task-Anchor identities without deleting either.
Do not treat mismatch as proven manipulation. Do not invent a third identity.

**PATH:**
`research/communication/github-only-exchange-enforcement-20261029/NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0_TASK_ANCHOR.json`

**SCHEMA:** `NEXUS_TASK_ORDER_ANCHOR_V1`

## Identity A — historical Cursor / worktree handshake (CRLF)

| Field | Value |
|-------|-------|
| CLASS | `HISTORICAL_CURSOR_HANDSHAKE_CRLF` |
| BYTES | `2720` |
| SHA-256 | `aca0ae992a2d27849f7ba626ec6c73defc639968ee90fa417a71a921ede5b4f8` |
| LINE_ENDING | `CRLF` (`\r\n`) — inferred from +59 B vs LF identity |
| STATUS | `PRESERVED_AS_HISTORICAL_HANDSHAKE_RECEIPT` |
| ROLE | Explains prior Cursor-reported bytes/hash; not erased |

AXIOM Independent Adjudication R1 table binds Identity A as Cursor-reported and Identity B as independent GitHub readback. This witness does not erase A.

## Identity B — canonical GitHub / git blob / restored worktree (LF)

| Field | Value |
|-------|-------|
| CLASS | `CANONICAL_GITHUB_GIT_BLOB_LF` |
| BYTES | `2661` |
| SHA-256 | `92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b` |
| LINE_ENDING | `LF` (`\n` only; `CR_COUNT=0`) |
| GIT_BLOB_OID | `e07dd75679a476a3ee079a8e375796c58b7f75d5` |
| STATUS | `MATCH_AXIOM_INDEPENDENT_GITHUB_READBACK` |
| ROLE | Source-exact identity for future closures |

## Reconciliation (C1 descriptive)

```text
DELTA_BYTES = 2720 - 2661 = 59
LIKELY_CAUSE = CRLF_CHECKOUT_ON_WINDOWS (core.autocrlf=true)
  OR PIPELINE_CONTAMINATION_OF_CURSOR_HANDSHAKE_BYTES
NOT_ESTABLISHED = CONTENT_TAMPERING
NOT_ESTABLISHED = SILENT_REWRITE_OF_JSON_SEMANTICS
CANONICAL_FOR_NEXT_CLOSURE = Identity_B (2661 / 92fc6aa5…)
HISTORICAL_HANDSHAKE_A = PRESERVED_DO_NOT_ERASE
```

## Independent Cursor rehash this remediation turn

| Source | Bytes | SHA-256 | CR_COUNT |
|--------|------:|---------|----------|
| Worktree after LF restore | 2661 | `92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b` | 0 |
| `git cat-file -p` blob | 2661 | `92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b` | 0 |
| AXIOM F10 reported GitHub readback | 2661 | `92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b` | — |

**VERDICT_F10_BYTES:** `CANONICAL_IDENTITY_BOUND_BOTH_HISTORIES_PRESERVED_C1`

## Epistemic walls

```text
HASH_MATCH ≠ SCIENTIFIC_TRUTH
CRLF_HANDSHAKE ≠ CONTENT_TAMPER_PROOF
IDENTITY_B_CANONICAL ≠ LICENSE_TO_ERASE_IDENTITY_A
WITNESS_WRITTEN ≠ TERMINAL_PASS
```

## Prohibitions observed

- No deletion of historical Task-Anchor receipt text elsewhere in the lane
- No rewrite of AXIOM Independent Adjudication R1
- No Hostinger / www write
- Claim ceiling remains `C1_DESCRIPTIVE_ONLY`
