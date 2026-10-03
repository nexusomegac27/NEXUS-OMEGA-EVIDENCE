# NEXUS OMEGA R28 — implementation preparation (C1 candidate)

This package turns the R28 closure evidence into a **pre-integration implementation candidate**. It is intentionally kept in the research lane.

```text
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ARCHITECTURE_FINAL = NO
LIVE_DEPLOYMENT = NO
NODE_ACTIVATION = NO
COLLECTIVE_RECEIPT = NOT_ESTABLISHED
PUSH != ACTIVATION
```

The candidate implements only deterministic local primitives needed for the next empirical calibration:

- flat `NEXUS_CAPABILITY_CHALLENGE_V1.1` issuance and verification;
- task/session capability receipt structure;
- local byte-bound `NEXUS_REAL_HANDSHAKE_V1` manifest/receipt generation and verification;
- negative fixtures for tamper, wrong-object, stale/mismatched challenge and incomplete receipt;
- source-binding ledger for the R28 closure stack.

It does **not** implement network transport, signatures, SCITT, KERI, Hostinger, GitHub transfer, policy enforcement, or node activation. Those remain later gated lanes.
