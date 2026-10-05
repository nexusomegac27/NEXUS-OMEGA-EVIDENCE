# RUN10R7 — Receiver-Side Verification Receipt

**Date:** 2026-10-05 · **Verifier:** NEXUS_OMEGA (Omega runtime) · **Claim ceiling:** C1_DESCRIPTIVE_ONLY

## Byte-Integrity Check (received MANUS PGI1 return vs. declared manifest)

| File | Size | Declared SHA-256 | Computed SHA-256 | Verdict |
|---|---|---|---|---|
| 01_METRICS_DEFINITION.md | 4103 | e927ce1b…9287110 | e927ce1b…9287110 | **BYTE_VERIFIED** |
| 02_COLLAPSE_CLASSIFIER.md | 2956 | 67b937b1…e0831e00 | 67b937b1…e0831e00 | **BYTE_VERIFIED** |
| 05_SYNTHETIC_CALIBRATION_SKETCH.md | 2390 | 434cb6e7…f6d17cc | 434cb6e7…f6d17cc | **BYTE_VERIFIED** |
| 06_MANIFEST_SHA256.json (self-hash basis: self=null + terminal newline) | 3074 | a4ec97de…14f5a36f | a4ec97de…14f5a36f | **BYTE_VERIFIED** |

Full hash values:
- 01: e927ce1bec63617358e523144606d0a7e45ff74020a8322c398e1a51c9287110
- 02: 67b937b175fa809585fa846ce5e17fc0641f430d7e20e9081387f9a2e0831e00
- 05: 434cb6e7a854cfaa84e5ecbbf7d084d86cc14ba046770dec8e29d1062f6d17cc
- 06 self: a4ec97dec8bae855929ce40ba30a74bfce0d5fc880103a6c771d588b14f5a36f

## Not received in this transport (declared in manifest, hash unverifiable receiver-side)

00_HANDSHAKE.json (731 B) · 03_NEGATIVE_FIXTURES/NF-G01..G05 (5 files) · 04_POSITIVE_FIXTURES/PF-G01..G05 (5 files) · 07_CLAIM_CEILING_RESTATEMENT.md (658 B)

Status: **NOT_RECEIVED — NO HASH WITNESS CLAIMED.** These entries remain manifest-declared only. A later transport may close this gap; until then no receiver-side verification statement exists for them (UNKNOWN, not HEALTHY).

## Method note

Hashes computed receiver-side with a self-test-verified SHA-256 implementation (FIPS 180-4 test vectors 'abc' and empty string passed). Input transport was content-addressed (base64 intermediate, byte-exact decode). One intermediate manual transcription produced a false mismatch for 02; it was resolved by a lossless re-read — documented here for error-auditability, not hidden (human-error reduction lane, order section 35).

## Verdict

BYTE_CHECK = PASS for all received files. REFERENT_CHECK = PASS (each file binds to its declared path and semantic role). Files not received remain UNKNOWN — never silently upgraded to verified.

HASH_MATCH does not establish truth of content — only transport integrity (order section 17: no HASH -> TRUTH laundering).
