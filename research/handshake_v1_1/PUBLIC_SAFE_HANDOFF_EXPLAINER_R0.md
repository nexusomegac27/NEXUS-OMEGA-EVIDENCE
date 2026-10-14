# NEXUS OMEGA — Public-safe explanation of a two-channel handoff (C1 research candidate)

The problem: external research agents cannot open a private GitHub repository. An SHA-256 checksum printed in a message is an integrity commitment, not a delivery channel.

The design: public-safe research documents can be published as real immutable text/binary assets together with a small witness manifest; confidential artifacts use a separate authorized encrypted or access-brokered channel. Receivers obtain actual bytes and check a signature against a pre-trusted signer before issuing a source receipt. Operator copy/paste is the convenient routing action; it does not substitute for cryptographic verification.

For NEXUS, validation must distinguish: `WITNESS_ONLY`, `CONTENT_VERIFIED`, `AUTHENTICATED_SOURCE`, `AUTHORIZED_ACTION`, and `EXECUTION_VERIFIED`. None implies the next stage automatically. New research lanes remain PROVISIONAL and the claim ceiling remains `C1_DESCRIPTIVE_ONLY`.

A V1.1 candidate tool was exercised in a sandbox with 25 passing test cases. Production key identity, public release, encrypted private-blob transport, Cursor live runtime, and Hostinger execution remain unestablished.
