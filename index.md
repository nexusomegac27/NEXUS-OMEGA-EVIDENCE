---
title: NEXUS OMEGA Evidence
---

# NEXUS OMEGA Evidence

This site is a discovery surface for public, content-addressed C1 evidence. It is not a truth oracle and grants no promotion or deployment authority.

## Machine-readable entry points

- [Latest object](index/v1/latest.json)
- [Append-only object inventory](index/v1/objects.jsonl)
- [Anchor manifest schema](schema/anchor-manifest-v1.schema.json)
- [External-agent return schema](schema/agent-return-v1.schema.json)
- [Agent verification protocol](docs/agent-protocol.md)
- [Open Science Agent Communication Manifest](docs/OPEN_SCIENCE_AGENT_COMMUNICATION_MANIFEST.md)
- [Scientific communication implementation profile](docs/SCIENTIFIC_COMMUNICATION_IMPLEMENTATION_PROFILE_V0_1.md)
- [Scientific communication record schema](schema/scientific-communication-v1.schema.json)
- [Negative fixture suite](validation/scientific-communication-negative-fixtures-v1.jsonl)
- [Communication ledger head](communication/index/v1/latest.json)
- [Communication ledger inventory](communication/index/v1/records.jsonl)
- [Communication ledger protocol](communication/README.md)

Every consumer must retrieve the referenced bytes, verify their SHA-256 and length, preserve all caveats, and independently validate any semantic claim.
