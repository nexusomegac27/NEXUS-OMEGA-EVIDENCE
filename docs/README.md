# Documentation domain

`docs/` owns stable human-readable repository documentation.

## Stable bootstrap surface

The files at `docs/` root are intentionally stable public entry points used by agents and existing handoffs. They are not moved merely to achieve cosmetic nesting.

## Subdomains

- `artifact-handoff-protocol.md` - GitHub Inbox -> Validate -> Bind -> Relay -> Ack protocol for external agent returns.
- `artifact-rollout-protocol.md` - separate Prepare -> Validate -> Package -> Authority-Gate -> Ack protocol for rollout readiness packages.
- `architecture/` — repository/system architecture and machine structure contract.
- `governance/` — durable operational laws and placement policy.
- `phase2/` — historical path-bound A83/A84 evidence; location is frozen by published artifact bindings.
- `r5/` — R5 architecture/protocol documentation as it becomes integration-grade.

New phase-specific documentation should use the mirrored phase slug used by schemas, tooling, tests, validation, examples, and research.
