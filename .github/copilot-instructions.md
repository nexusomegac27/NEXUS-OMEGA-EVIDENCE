# GitHub Copilot Instructions — NEXUS OMEGA EVIDENCE

Always treat this repository as a governed C1 evidence surface, not as an ordinary software repository.

Before substantive answers or changes, read and obey:

- `AGENTS.md`
- `GOVERNANCE.md`
- `docs/AI_CONTEXT.md`
- `docs/AI_HANDOFF_PROTOCOL.md`
- `docs/agent-protocol.md`
- `docs/architecture/REPOSITORY_STRUCTURE.md`
- `index/v1/latest.json` when current evidence state matters

## Persistent context behavior

Repository files are the durable project memory. Distinguish repository-established facts, externally validated facts, operator-reported facts, unresolved evidence, and model prior knowledge used only for discovery.

## Scientific and governance boundary

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
DEPLOYMENT_AUTHORITY = NO
```

Never infer stronger authority from hashes, signatures, commits, CI, releases, attestations, DOI/SWHIDs, publication, code review, or multi-agent agreement.

## Risk-adaptive evidence handling

- Material missing source bytes: use `SOURCE_NOT_PRESENT`.
- Insufficient material evidence: use `NOT_ESTABLISHED`.
- Required computation unavailable: use `NOT_COMPUTABLE`.
- Do not reconstruct missing historical evidence from chat or semantic similarity.
- Noncritical uncertainty is not automatically a global stop condition.
- `BLOCKED_LANE != BLOCKED_SYSTEM`.

## Repository Order Law V1

Before writing a file, classify it and place it in the owning directory defined by `README.md` and `docs/governance/REPOSITORY_ORDER_POLICY.md`.

- Never use repository root for agent returns, patches, research packages, receipts, or experiments.
- Active research goes to `research/<phase>/<agent-or-topic>/`.
- Stable R5 components mirror across `docs/r5/`, `schema/r5/`, `scripts/r5/`, `tests/r5/`, `validation/r5/`, and `examples/r5/`.
- Preserve path-bound historical evidence in place unless an explicit migration contract authorizes otherwise.
- Structure changes must update the human and machine structure contracts and pass `scripts/validate_repository_structure.py`.

## Repository mutations

Use a dedicated branch and pull request for nontrivial changes. Do not force-push or silently rewrite published evidence objects. Checks do not authorize claim promotion.

## External-agent and handoff behavior

Use `docs/AI_HANDOFF_PROTOCOL.md`. Preserve exact predecessor identity, received bytes, hashes, work executed, work not executed, caveats, and next lawful action. A producer cannot independently validate its own scientific output.

## Security

Follow `SECURITY.md`. Never place credentials, tokens, private health data, private conversations, or non-public sensitive material in public repository content.
