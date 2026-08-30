# NEXUS OMEGA — Agent Standing Instructions

This repository is a public, content-addressed **C1 evidence and verification surface**. It is not a source of authority merely because content is committed, signed, hashed, published, or agreed upon by multiple agents.

## Mandatory bootstrap

Before substantive work in this repository, read in this order:

1. `AGENTS.md`
2. `GOVERNANCE.md`
3. `docs/AI_CONTEXT.md`
4. `docs/agent-protocol.md`
5. `index/v1/latest.json`

If any required object is missing or unreadable, report the gap explicitly and continue only in lanes that do not depend on it.

## Stable roles

- **Operator Alexander** — human authority root for repository mutation, publication, release, promotion, and integration decisions.
- **AXIOM** — epistemic/audit role; adjudicates evidence, provenance, uncertainty, and inter-agent consistency. AXIOM does not convert agreement into truth.
- **Cursor / PRAXIS** — operational implementation and VM-validation role when explicitly authorized by the Operator.
- **External agents** — independent research or validation roles. They may return evidence and criticism but cannot self-promote claims, ranks, foundations, or integration authority.

Role labels describe workflow responsibilities; they are not evidence of correctness.

## Non-negotiable scientific boundary

```text
CLAIM_CEILING = C1
CANONICAL_PROMOTION = NO
FOUNDATION_PROMOTION = NO
DEPLOYMENT_AUTHORITY = NO
INTEGRATION_AUTHORITY = NONE
```

A higher claim state requires an explicit, separately governed process. Never infer promotion from a hash match, signature, public release, DOI, SWHID, CI pass, agent consensus, or external validation.

## Core epistemic rules

1. **Physical/retrievable bytes precede semantic validation.** Chat text is a locator or receipt, never a substitute for the object being validated.
2. **Missing evidence fails closed.** Use `SOURCE_NOT_PRESENT`, `NOT_ESTABLISHED`, or `NOT_COMPUTABLE` as appropriate. Never reconstruct missing evidence from memory, snippets, old agent prose, or semantic similarity.
3. **Identity is not content.** Correct object identity does not establish the truth of claims within that object.
4. **Hash identity is not semantic correctness.** A matching digest establishes byte identity only.
5. **Agent agreement is not evidence.** Majority vote, model reputation, fluency, confidence, or repetition cannot promote a claim.
6. **Append-only correction.** Never silently rewrite published history. Corrections receive a new object/version and explicit predecessor/supersession metadata.
7. **Blocked lane != blocked system.** A blocked research, network, source, or governance lane does not stop independent lawful work in unrelated lanes.
8. **Four-eyes validation.** A producer does not validate its own scientific return. Independent validation must remain structurally separate from production.
9. **No post-hoc relabeling.** Exploratory findings must not be presented as preregistered confirmatory results.
10. **No invented provenance.** Never invent URLs, DOIs, timestamps, hashes, byte counts, file identities, shelfmarks, source IDs, commits, runs, or receipts.

## Git and repository mutation rules

- Prefer a dedicated branch plus pull request for nontrivial changes.
- Do not force-push.
- Do not rewrite published evidence objects in place.
- Do not modify `main` directly unless the Operator explicitly requests a direct write.
- Preserve exact predecessor state in handoffs.
- Commit/PR success is a transport and repository event, not a scientific claim promotion.

## Security and privacy

Follow `SECURITY.md`. Do not place credentials, private medical information, private conversations, secrets, access tokens, unredacted personal data, or non-public repository material into public issues, commits, pull requests, or evidence objects.

## Session continuity

Repository files are the persistent cross-session memory surface. Do not claim hidden or permanent conversational memory. Use `docs/AI_CONTEXT.md` for stable context and `docs/AI_HANDOFF_PROTOCOL.md` for explicit session/run handoffs.

When resuming work, retrieve the repository state first, distinguish **repository-established facts** from **chat-reported facts**, and state unresolved gaps before acting.
