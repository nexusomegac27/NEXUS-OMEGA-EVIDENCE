# R28 local reference candidate

This directory contains a **pre-integration local reference candidate** for the R28 capability and byte-handshake primitives.

## Scope

Implemented:

- issue and verify `NEXUS_CAPABILITY_CHALLENGE_V1.1`;
- produce and verify capability receipts;
- build and self-check a byte-bound handshake manifest;
- receiver rehash + receipt;
- sender-side receipt verification;
- local-directory transport test double;
- eight positive/negative fixtures.

Not implemented:

- real online transport;
- authentication/authorization;
- digital signatures;
- SCITT/KERI;
- Hostinger/GitHub/OCI backend adapters;
- node activation;
- architecture finalization.

## Local validation

```bash
cd research/r28/implementation-prep/candidate
python -m unittest -v test_nexus_r28_reference.py
```

The local-directory transport exists only to exercise the transport boundary deterministically.

```text
LOCAL_TRANSPORT_TEST_DOUBLE != REAL_ONLINE_HANDSHAKE
TEST_PASS != ARCHITECTURE_FINAL
PUSH != ACTIVATION
```
