# R10R8 — Soft-Lineage E0.2 Gate Surface

**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`  
**State:** `PASS_WITH_MAJOR_CAVEATS_C1_R10R8_E0_2_SYNTHETIC_GATE_SURFACE_PUSHABLE_NOT_PRODUCTION`

This lane records the E0.2 synthetic gate work that follows R10R7. It is a research/validation surface only.

## What is established here

- The received outer stack is byte-readable and ZIP-integrity clean.
- Declared SHA-256 sets checked by AXIOM match for the Gate2, Gate4–Gate7, seed, Grok crossvalidation, and Manus crossvalidation materials that were independently inspected.
- Synthetic Gate2 and Gate3 non-compensation fixtures reproduce.
- Synthetic Gate4–Gate7 fixture suites reproduce.
- The Grok all-seven-gates integration fixture reproduces its declared 4/4 outcomes at the semantic level.
- AXIOM R1 adds stricter fail-closed regression cases and passes 10/10 synthetic fixtures.

## What is not established

- production readiness;
- cryptographic authority;
- semantic truth;
- external validity;
- empirical Soft-Lineage validation;
- R10R8 microscopy/vesicle-tracking performance;
- any claim promotion above C1;
- any unlock of R10R6 E2.

## Material caveat

The original all-seven-gates integration test is **not** fully fail-closed: missing GATE2/GATE3 states default to VERIFIED, and its integrated GATE4/GATE5/GATE7 checks are weaker than their standalone gate implementations. The original PASS is therefore retained as a bounded fixture result, not as proof of complete seven-gate enforcement.

See `AXIOM_VALIDATION_RECEIPT_20261005.md` and `E0_2_VALIDATION_STATUS.json`.

The full local source stack is identified by SHA-256 in the receipt; this PR intentionally publishes a curated validation capsule rather than dumping local `.work/`, duplicate Windows-path ZIP members, or unrelated transport debris.
