# NEXUS OMEGA — Astratis IX R3 Controlled Falsification Validation

```text
OBJECT = NEXUS_OMEGA_AXIOM_ASTRATIS_IX_R3_CONTROLLED_FALSIFICATION_VALIDATION_20260920_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_R3_AB_REFERENCE_REPRODUCED_CDE_NOT_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
IX_EXECUTION = NOT_STARTED
ACTIVATION = NO
R3_OPERATOR_PHASE_STATE = CLOSED_FOR_HANDOFF_TO_R4
```

This directory is the public-safe AXIOM derivative of the physical R3 drop `NEXUS_~3.zip`.
It preserves the useful R3-A/R3-B results, independently reproduces the minimal signed-receipt and
local authority-boundary reference, and explicitly carries unexecuted R3-C/D/E work into R4.

## Physical source bind

```text
SOURCE_ZIP_BYTES = 91584
SOURCE_ZIP_SHA256 = a61af408a88ff406f2d90aa221af210020f42d41f9c656155dbb09a808a74d38
SOURCE_ZIP_ENTRIES = 9
ZIP_CRC = PASS
PATH_TRAVERSAL = NONE_FOUND
```

The supplied R3 foundation is byte-bound at:

```text
R3_FOUNDATION_SHA256 = 89627ebb36dae43ce4e4853ef129b621959262d4d1709d140cf1239956911340
```

## Independent AXIOM reproduction

A public test-only Ed25519 fixture reproduces:

- payload SHA-256 binding;
- Ed25519 signature verification;
- previous-receipt hash linkage;
- rejection of payload tampering;
- rejection of signature tampering;
- rejection of a broken chain link.

A local, non-networked authority-boundary harness then verifies nine policy/executor cases:

- valid low-risk proposal executes;
- invalid signature is denied;
- unallowed direct-write action is denied;
- stale proposal is denied;
- high-risk proposal without human authorization is denied;
- mismatched human authorization is denied;
- expired human authorization is denied;
- valid high-risk proposal with matching authorization executes;
- executor rejects an ALLOW decision bound to another proposal ID.

Combined test suite: `13/13 PASS` on Python 3.13.5 with `cryptography==46.0.4`.

This validates only the supplied/reference software invariants. It does **not** establish production
security or complete attack resistance.

## R3-B correction

The source package describes a ZKP-vs-signed-receipt comparison, but supplies no executable ZKP
circuit, proof, proving receipt, verifier receipt or timing artifact. Therefore:

```text
SIGNED_RECEIPT_BASELINE = INDEPENDENTLY_REPRODUCED_C1
ZKP_ARM_EXECUTION = NOT_ESTABLISHED
ZKP_PERFORMANCE_COMPARISON = NOT_ESTABLISHED
```

The narrower design conclusion is retained:

```text
FOR_CURRENT_DISCLOSED_BASELINE_REQUIREMENTS:
SIGNED_RECEIPT = SUFFICIENT_REFERENCE_BASELINE
ZKP = OPTIONAL_PRIVACY_RESEARCH_LAYER
```

A zero-knowledge proof proves a formal statement under the chosen proof system; it does not by
itself establish scientific validity, human authorship or the validity of a hidden quality metric.

## R3-A source caveat

The supplied R3-A execution narrative reports `PASS=6`, but its declared `R3-A_LOG_SHA256` is a
68-hex illustrative value and no raw execution log is present in the package. The source-level
`6/6` claim is therefore **not independently established from the supplied bytes**.

The public result here is the separate AXIOM reference harness and its own execution receipt.

## R3 package provenance defect

Two byte-distinct documents share the same logical object ID:

`NEXUS_OMEGA_R3AB_CROSSVALIDATION_ORDER_TO_MISTRAL_VIBE_20260920_R0`

```text
ROOT_VARIANT_SHA256   = b33fb405df0ca493fbdf9f57042740dc8e3495fdb3598ac64cdc3a94fe8e9066
NESTED_VARIANT_SHA256 = 3f392e7eb5fedd18683ee49c121bc92f49dfcb2383766a95b84090954457ce04
```

The variants differ in issuer and substantive instructions. This is preserved as an object-identity
collision and must not be silently normalized.

## Manifest status

- `NEXUS_OMEGA_R3_AB_PACKAGE_20260920.zip`: listed objects `5/5 MATCH`, but only `5/6` non-self files are covered; README is uncovered.
- `NEXUS_OMEGA_R3AB_CROSSVALIDATED_PACKAGE_20260920.zip`: listed objects `6/6 MATCH`, but only `6/7` non-self files are covered; README is uncovered.
- `NEXUS_OMEGA_R3AB_ORDER_FOR_MISTRAL_VIBE_20260920.zip`: no internal checksum manifest.

Thus no supplied nested ZIP is promoted as a fully sealed package.

## R3-C / R3-D / R3-E

The original R3 foundation defined five tracks. In the supplied physical bytes only A and B have
execution narratives. C, D and E occur only as `NEXT` / future-work references.

```text
R3-A = REFERENCE_HARNESS_REPRODUCED_C1
R3-B = SIGNED_RECEIPT_BASELINE_REPRODUCED_C1_WITH_ZKP_EXECUTION_GAP
R3-C = NOT_EXECUTED_IN_SUPPLIED_PACKAGE
R3-D = NOT_EXECUTED_IN_SUPPLIED_PACKAGE
R3-E = NOT_EXECUTED_IN_SUPPLIED_PACKAGE
R3_FULL_5_TRACK_COMPLETION = NO
```

The operator may close R3 as a phase and move the unresolved tracks to R4, but the missing execution
must remain explicit.

## Publication boundary

Published:

- physical package and nested-package identities;
- manifest-coverage audit;
- object-ID collision;
- independent signed-receipt reference implementation and receipt;
- independent local authority-boundary reference implementation and receipt;
- primary-source scope corrections;
- open gaps for R4.

Not published/promoted:

- raw third-party agent transcripts;
- source-package claims lacking raw execution receipts;
- any claim that ZKP was benchmarked;
- any claim that R3-C/D/E executed;
- an activated IX agent or production security assertion.

```text
PUSH != ACTIVATION
REFERENCE_HARNESS_PASS != PRODUCTION_SECURITY_PASS
MULTI_AGENT_AGREEMENT != INDEPENDENT_EXPERIMENT
```
