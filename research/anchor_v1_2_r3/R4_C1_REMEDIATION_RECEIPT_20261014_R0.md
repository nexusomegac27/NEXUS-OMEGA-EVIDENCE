# NEXUS OMEGA — R4 C1 Remediation Receipt

**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`  
**Classification:** public-safe, reversible research evidence; not a production release

## Executed evidence

- The private R1 source bundle was read from an authenticated native Git checkout and independently rehashed at **154,785 bytes**. ZIP CRC validation passed for all 17 entries.
- The R3 source inventory contains **11 bound input objects**. Source provenance classes remain separated: original bytes, externally reported execution, static review, reconstruction, and not observed.
- Anchor V1.2 delta suite: **16/16 passed** in an isolated no-network sandbox. The source-bound compatibility result of **25/25** remains reported from the prior isolated run. Operator signer, production downloader, DNS/redirect/rebinding perimeter, and Hostinger deployment remain unprovisioned or untested.
- The untrusted R1 baseline reproduced **6/6** documented defects (F01–F06).
- A separate C1 hardening candidate rejected **6/6** adversarial cases and passed positive/idempotency, history-preservation, durable-queue restart, and C1-claim regression fixtures. This is a sandbox candidate, not a production-signed implementation.

## Boundaries and non-claims

- No private R1 ZIP, credentials, secrets, or private source code are published here.
- No Hostinger, production, main-branch, or website-root write was performed.
- No automatic start, claim promotion, operator-signing authority, or live SSRF/redirect security proof is implied.
- This receipt does not constitute an authentic Cursor-agent receiver ACK; it records the executor's own evidence only.

## Public branch scope

This file is published on the existing `codex/nexus-r3-public-safe-anchor-v12-20261014` research branch only. It is not a merge to `main` and not a deployment.
