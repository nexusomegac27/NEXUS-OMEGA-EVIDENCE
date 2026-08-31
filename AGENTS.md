# NEXUS OMEGA — Agent Standing Instructions

This repository is a public, content-addressed **C1 evidence and verification surface**. It is not a source of authority merely because content is committed, signed, hashed, published, or agreed upon by multiple agents.

## Mandatory bootstrap

Before substantive work in this repository, read in this order:

1. `AGENTS.md`
2. `GOVERNANCE.md`
3. `docs/AI_CONTEXT.md`
4. `docs/agent-protocol.md`
5. `docs/architecture/REPOSITORY_STRUCTURE.md`
6. `index/v1/latest.json` when the task depends on current evidence state

If any required object is missing or unreadable, report the gap explicitly and continue in independent lanes when reasonable.

## Stable roles

- **Operator Alexander** — human authority root for repository mutation, publication, release, promotion, and integration decisions.
- **AXIOM** — epistemic/audit role; adjudicates evidence, provenance, uncertainty, inter-agent consistency, and repository-order compliance.
- **Cursor / PRAXIS** — operational implementation and VM-validation role when explicitly authorized by the Operator; also enforces repository-order compliance on implementation intake.
- **External agents** — independent research, implementation-candidate, or validation roles. They may return evidence and criticism but cannot self-promote claims, foundations, or integration authority.

Role labels describe workflow responsibility; they are not evidence of correctness.

## Non-negotiable scientific boundary

```text
CLAIM_CEILING = C1
CANONICAL_PROMOTION = NO
FOUNDATION_PROMOTION = NO
DEPLOYMENT_AUTHORITY = NO
INTEGRATION_AUTHORITY = NONE
```

Never infer promotion from a hash match, signature, public release, DOI, SWHID, CI pass, agent consensus, or external validation.

## Core epistemic rules

1. Physical/retrievable bytes precede semantic validation when byte identity is material.
2. Missing material evidence is labeled explicitly; noncritical uncertainty is not automatically a system-wide stop condition.
3. Identity is not content; hash identity is not semantic correctness.
4. Agent agreement is not evidence.
5. Corrections append; published history is not silently rewritten.
6. `BLOCKED_LANE != BLOCKED_SYSTEM`.
7. A producer does not independently validate its own scientific return.
8. No post-hoc relabeling of exploratory results as confirmatory.
9. Never invent provenance, hashes, byte counts, commits, receipts, URLs, or source identities.

## Repository Order Law V1 — permanent trigger

Before creating, moving, importing, or integrating any file:

1. classify its artifact class and owning directory;
2. consult `README.md` and `docs/governance/REPOSITORY_ORDER_POLICY.md`;
3. place active research only under `research/<phase>/<agent-or-topic>/`;
4. use mirrored phase paths across `docs/`, `schema/`, `scripts/`, `tests/`, `validation/`, and `examples/` when work becomes implementation-grade;
5. never dump generated returns, patches, archives, receipts, or experiments into repository root;
6. do not relocate path-bound historical evidence merely for appearance;
7. update the structure README and machine structure contract in the same change whenever structure changes;
8. run `python scripts/validate_repository_structure.py --root .` before handoff or PR.

AXIOM and Cursor/PRAXIS MUST treat repository order as an intake invariant. If a new artifact is misfiled, route it to the correct domain before canonical continuation. This is risk-adaptive: ordinary placement mistakes should be corrected without halting unrelated lawful research; path changes that would break evidence bindings require explicit migration treatment.

## Git and repository mutation rules

- Prefer a dedicated branch plus pull request for nontrivial changes.
- Do not force-push.
- Do not rewrite published evidence objects in place.
- Preserve exact predecessor state in handoffs.
- Commit/PR success is a transport and repository event, not scientific claim promotion.

## Security and privacy

Follow `SECURITY.md`. Do not place credentials, private medical information, private conversations, secrets, access tokens, unredacted personal data, or non-public repository material into public repository content.

## Session continuity

Repository files are the persistent cross-session memory surface. Use `docs/AI_CONTEXT.md` for stable context and `docs/AI_HANDOFF_PROTOCOL.md` for explicit session/run handoffs.

When resuming work, retrieve repository state first, distinguish repository-established facts from chat-reported facts, and preserve unresolved gaps without inventing continuity.
