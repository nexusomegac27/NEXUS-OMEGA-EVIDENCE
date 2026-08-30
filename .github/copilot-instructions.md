# GitHub Copilot Instructions — NEXUS OMEGA EVIDENCE

Always treat this repository as a governed C1 evidence surface, not as an ordinary software repository.

Before substantive answers or changes, read and obey:

- `AGENTS.md`
- `GOVERNANCE.md`
- `docs/AI_CONTEXT.md`
- `docs/AI_HANDOFF_PROTOCOL.md`
- `docs/agent-protocol.md`
- `index/v1/latest.json` when the task depends on the latest published evidence object

## Persistent context behavior

Repository files are the durable project memory. Do not claim that conversational memory across sessions is authoritative or complete. When asked what is known about NEXUS OMEGA, retrieve repository context first and distinguish:

- repository-established / physically verified facts;
- externally validated facts;
- operator-reported facts;
- unresolved or missing evidence;
- model prior knowledge used only for discovery.

## Scientific and governance boundary

Never exceed:

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
DEPLOYMENT_AUTHORITY = NO
```

Never infer stronger authority from hashes, signatures, commits, CI, releases, DOIs, SWHIDs, GitHub publication, code review, or multi-agent agreement.

## Fail-closed rules

- Missing source bytes: use `SOURCE_NOT_PRESENT`.
- Insufficient evidence: use `NOT_ESTABLISHED`.
- Required computation cannot be performed: use `NOT_COMPUTABLE`.
- Never reconstruct missing evidence from chat, summaries, snippets, prior model prose, or semantic similarity.
- Correct object identity does not validate object content.
- A matching hash proves byte identity only.

## Work-conserving rule

`BLOCKED_LANE != BLOCKED_SYSTEM`.

A blocked lane must not halt unrelated lawful work. Continue independent tasks while preserving the blocked lane's uncertainty.

## Repository mutations

For nontrivial changes, prefer a new branch and pull request. Do not force-push or silently rewrite published evidence objects. Do not merge merely because checks pass. Operator disposition remains required where governance says so.

## External-agent and handoff behavior

Use `docs/AI_HANDOFF_PROTOCOL.md`. Preserve exact predecessor identity, received bytes, hashes, work executed, work not executed, caveats, and the single next lawful action.

A producer cannot independently validate its own scientific output. A validator must inspect the actual physical/retrievable object.

## Security

Follow `SECURITY.md`. Never place credentials, tokens, private health data, private conversations, or non-public sensitive material in public repository content.

## Response style for repository work

Be precise and compact. Use machine-readable status blocks for material handoffs. Never invent hashes, byte counts, URLs, DOI/SWHIDs, timestamps, commit IDs, execution receipts, or source identities.
