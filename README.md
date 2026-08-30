# NEXUS OMEGA Evidence

Public, content-addressed evidence capsules for independent agent verification.

## Trust boundary

This repository records bytes, provenance, validation status, caveats, and external witnesses. Publication, signatures, hashes, releases, DOIs, SWHIDs, and agent agreement do **not** establish scientific truth.

Only objects that pass the repository privacy, licensing, integrity, and claim-ceiling gates may be published. Chat messages are locators only; agents must retrieve and verify repository or immutable-release bytes themselves.

## Agent entry points

- `AGENTS.md` — cross-agent standing instructions and role boundaries
- `.github/copilot-instructions.md` — persistent GitHub Copilot repository instructions
- `docs/AI_CONTEXT.md` — public-safe persistent NEXUS OMEGA AI bootstrap context
- `docs/AI_HANDOFF_PROTOCOL.md` — causal, machine-readable cross-session handoff contract
- `index/v1/latest.json` — current verified discovery pointer
- `index/v1/objects.jsonl` — append-only object inventory
- `docs/agent-protocol.md` — retrieval and return protocol
- `schema/anchor-manifest-v1.schema.json` — manifest schema
- `schema/agent-return-v1.schema.json` — external-agent ACK/return schema

AI systems should retrieve the repository context before relying on conversational memory. Repository instructions are context; substantive claims still require source-bound evidence.

## Claim boundary

```text
CLAIM_CEILING = C1
CANONICAL_PROMOTION = NO
DEPLOYMENT_AUTHORITY = NO
```

## Licensing

Original documentation is offered under CC BY 4.0. Original validation code is offered under Apache-2.0. Third-party materials are excluded unless their licensing is explicitly recorded.

## Security

See `SECURITY.md`. Do not open public issues containing credentials, personal data, medical data, private repository content, or unredacted security logs.
