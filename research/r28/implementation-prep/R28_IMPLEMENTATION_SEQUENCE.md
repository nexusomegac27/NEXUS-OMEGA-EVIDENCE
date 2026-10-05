# R28 implementation sequence after research closure

```text
STAGE_0 = SOURCE_BIND_AND_LOCAL_TESTS
STAGE_1 = AXIOM_ISSUED_CAPABILITY_CHALLENGE_V1_1
STAGE_2 = MULTI_SUBSTRATE_RECEIPT_COLLECTION
STAGE_3 = INDEPENDENT_RECEIPT_VERIFICATION
STAGE_4 = REAL_LOCAL_HANDSHAKE_V1
STAGE_5 = ONLINE_BACKEND_SELECTION_AND_THREAT_REVIEW
STAGE_6 = REAL_ONLINE_BYTE_HANDSHAKE
STAGE_7 = PROVIDER_REMOVAL_TEST
STAGE_8 = ONLY_THEN_INTEGRATION_DECISION
```

## Stage 0 — this pushed package

Run the candidate unit tests and preserve results as validation evidence. This stage proves only the local deterministic mechanics.

## Stage 1–3 — collective calibration

AXIOM or another non-tested issuer creates the challenge. Each agent returns a challenge-bound receipt. Self-issued pilots remain historical evidence but do not become collective issuer validation.

## Stage 4 — local real-handshake mechanics

Use one physical artifact, sender manifest, receiver recomputation, returned receipt, sender verification. The candidate script implements this local primitive.

## Stage 5 — online backend gate

Compare Hostinger-owned gate, GitHub, OCI/ORAS and at least one provider-neutral object backend. Selection must be based on measured transport capabilities, security boundary, replaceability and operator cost.

## Stage 6 — online byte handshake

`PASS` requires actual bytes to cross the selected interface and be independently rehashed by the receiver. Text acknowledgement is insufficient.

## Stage 7 — provider removal

Repeat verification after removing the chosen provider from the verification path. Artifact identity and receipt verifiability must survive.

## Hard boundaries

```text
PUSH != DEPLOYMENT
LOCAL_TEST_PASS != ONLINE_HANDSHAKE_PASS
CAPABILITY_PASS != SEMANTIC_CORRECTNESS
THREE_RECEIPTS != UNIVERSAL_REPRODUCIBILITY
SIGNATURE != TRUTH
```
