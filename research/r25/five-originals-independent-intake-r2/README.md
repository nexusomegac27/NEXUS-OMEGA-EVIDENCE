# R25 Five Originals Independent Intake R2 (C1)

**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`  
**Claim promotion:** `NO`  
**Truth authority:** `NONE`

## What this is

Public-safe custody publication of five GROK R25 original deliverables plus the Cursor R2 independent-intake return capsule.

This path is a **clean Evidence publication from `main`**. It does **not** merge open PR `#65` or `#67`.

## Bound state (report-level)

| Token | Value |
|---|---|
| `R25_FIVE_ORIGINALS` | `PASS_SOURCE_EXACT_5_OF_5` |
| `R25_SOURCE_TRANSPORT_GAP` | `CLOSED` (these five only) |
| `R25_FULL_MAXI_RETURN` | `PARTIAL_COMPLIANCE` |
| `R25_EXPERIMENTS` | `NOT_EXECUTED` |
| `R25_TERMINAL` | `NO` |
| `R24` | `CLOSED_ADMINISTRATIVE` |
| `PR65_MERGE` | `HOLD_SCOPED` (unchanged) |
| `PR67_PRIVACY_HISTORY` | `HOLD_NO_MERGE` (unchanged) |

## Five originals (LF-normalized SHA-256)

| File | Bytes | SHA-256 |
|---|---:|---|
| `R25-00_EXECUTIVE_ADJUDICATION_BRIEF.md` | 5297 | `38c2efcc6a5edda5021198d9e81ba9b58422fd6d546cbb03da3254c63dc92b2a` |
| `R25-03_RING_AND_ORBIT_ERROR_MODEL.md` | 4811 | `e7eabdf30eff378ea54766f1220fa7aa9b6f6ec634c72b9b10ccb411e8058b1b` |
| `R25-05_E1_E2_CAUSAL_AUDIT.md` | 4084 | `f627e23875eaff52795c550a46cc6a9cd876d9b32cd3abceca472ecafd72880f` |
| `R25-07_ADVERSARIAL_REVIEW.md` | 4134 | `ca2fa0cbf00cbd02150ccbd962faee7a4c43ebd978696b1afdb19b0aec9c959a` |
| `R25-09_RETURN_MANIFEST.json` | 3103 | `33bbf4b101b42888fdb60f40a22384b4780936a60b640112e1de80db248c21a4` |

## Cursor R2 return capsule

| File | Bytes | SHA-256 |
|---|---:|---|
| `CURSOR_R2_EXECUTIVE.md` | 5982 | `3ad821edb310b039f02b79ba057a8f188cb38035713615d4200a25e1228ffe5b` |
| `CURSOR_R2_HANDSHAKE.md` | 1198 | `3edc4269b8896bce5bfa8fd3429739e8fcafa22202568ebeeac3435bed6c105a` |
| `CURSOR_R2_EPISTEMIC_WALLS.md` | 768 | `fc48f8477afb5152068f22405c9a998125bccdc3b8e51e0e52db8e36662ba47f` |
| `CURSOR_R2_SHA256SUMS.txt` | 243 | `9ec94c24b005b5c4451152185809f49aafd0f1daffdfddf0c7ae3f377e58f03b` |

## Epistemic walls

```text
PASS_SOURCE_EXACT_5_OF_5 ≠ R25_TERMINAL
PASS_SOURCE_EXACT_5_OF_5 ≠ FULL_MAXI_RETURN
HASH_MATCH ≠ SCIENTIFIC_TRUTH
GITHUB_PUSH ≠ WWW_DEPLOY ≠ LIVE_HOSTINGER_PASS
PR67_PRIVACY_HISTORY_HOLD ≠ LIFTED_BY_THIS_PUBLICATION
```

## Prohibitions preserved

- No merge of PR `#65` / `#67` from this publication.
- No Hostinger / www write claimed by this package.
- No claim promotion beyond C1 descriptive custody.
