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

## R27-E external-agent structural firewall (operator directive 2026-10-11)

External agents MUST treat `docs/governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md` and `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` as mandatory before any repository write. They may **only create** the exact return files in a preallocated, ACTIVE authorized slot. No agent may create directories/namespaces, rename/edit historical assets, modify code/workflows/governance, import chats or ZIP archives, or declare a deployment. A model's name or `Nexus_Intern` field is not GitHub or runtime identity. The verified GitHub actor must be operator-registered; the default actor allowlist is empty. Unavailable authorization ⇒ `WRITE_IDENTITY_NOT_AUTHORIZED`, not a guessed path. The owner-controlled CI check runs against trusted base code, but it becomes a hard merge gate only when branch rulesets and CODEOWNERS approval are actually enforced. GitHub evidence, external WWW wake signals, and internal privileged execution remain separate trust domains.

## Standing expert documentation and hash handoff · operator directive 2026-10-11

Every **new substantial expert research order**, without exception, must physically repeat the operative repository structure and write boundaries inside the order itself, rather than supplying only a casual hyperlink. Reuse the verified authoritative root and existing governance documents; do not issue standalone directory schemes, unsolicited return namespaces, or a second repo.

An order is **incomplete** unless it binds: exact `OBJECT` and prior `PREDECESSOR`; immutable parent GitHub commit, source paths, SHA256 and bytes; a recognized expert role explicitly separated from GitHub authentication; the full `REPOSITORY_ORDER_LAW_V1` owner paths and exact allowed/prohibited mutations; `C1_DESCRIPTIVE_ONLY`; required falsification and negative evidence; scientific assumptions, sources, methods, reproducibility commands/seeds/raw outcomes, data licenses, privacy exclusions; executed vs not executed; expected versioned output files and a detached child manifest; exact `NEXUS_OPERATOR_AXIOM` receiver and a pending, independently earned ACK.

**Canonical passive inbox:** `https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93` (`NEXUS_OPERATOR_AXIOM`). For this lineage, the owner-approved example assignments and complete rules are in `research/r26/collective-expert-handoffs-20261011/` at PR #94 / main commit `206381c880770954865c67d9075c401efd2295f0`. General detached manifest schema: `schema/expert-hash-handshake-v1.schema.json`; byte-only verifier: `scripts/verify_expert_hash_handshake_v1.py`. Those tools report only byte integrity, not authentication or science validity.

Existing R27-E `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` remains decisive for permissions. Its external actor allowlist is empty; **no direct expert PR write** without operator-issued exact slot, registered real GitHub/App actor, and independently enforced rules. Otherwise require honestly labeled operator-mediated bridge. An issue comment alone is neither a GitHub sender identity nor an always-on ChatGPT trigger. Private/sensitive inputs use approved private transport, never public issue text.

Future experts must carry this policy in every scoped research order, independent of model identity or prior conversation memory. **Receiver rehash and scientific adjudication remain separate gates; no producer-issued AXIOM ACK.**

## TASK ANCHOR NORM V1 — binding non-destructive DRIFT_RESET task-format trigger (operator 2026-10-11)

For each **new substantial** AXIOM, Cursor/PRAXIS or external-expert order, apply `docs/governance/NEXUS_OMEGA_TASK_ANCHOR_NORM_V1.md`. The order MUST bind its originating authority, exact predecessor bytes/path/immutable commit, delegated role and scope, allowed/prohibited actions, negative evidence and falsifiers, receiver hash handshake and append-only continuity. The machine-readable `TASK_ORDER_ANCHOR` envelope follows `schema/task-anchor-norm-v1.schema.json`; the offline check is `scripts/validate_task_anchor_norm_v1.py`; the exemplar is `examples/task-anchor-v1.example.json`.

```text
TASK_FORMAT = NEXUS_OMEGA_TASK_ANCHOR_NORM_V1
STATUS = NEXUS_INTERNAL_BINDING_TECHNICAL_SPECIFICATION
DIN = DIN_SPEC_92001_1_INSPIRED_NOT_DIN_ISSUED_NOT_CERTIFIED
ANCHOR = TASK_ORIGIN_ROLE_AUTHORITY_CONTINUITY_NOT_PERSONHOOD
DRIFT_RESET = RELOAD_VERIFIED_ANCHOR_AND_APPEND_DIFFERENCE_WITNESS
DRIFT_RESET_IS_NODE_RESET = FALSE
PRESERVE = ORIGINAL_EVIDENCE + HISTORY + NEGATIVE_RESULTS + CHECKPOINTS + NODE_STATE
PREDECESSOR_SOURCE_GAP = HOLD_SCOPED_NO_CHAT_RECONSTRUCTION
SCIENTIFIC_SUCCESSOR = APPEND_ONLY_NOT_AUTOMATIC_DRIFT
AUTHORITY_ESCALATION = DENY
NEW_CURSOR_OR_NODE_RUNTIME_AUTHORITY = NONE
EXTERNAL_GITHUB_ACTOR_POLICY = EXISTING_DEFAULT_DENY_UNCHANGED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

This trigger is **prospective**, does not reformat old source-bound orders, and does not mean the ChatGPT platform has persistent agent memory or privileged pre-inference injection. DIN-like internal format discipline is not DIN accreditation or certification. A valid schema/CI check means structural conformity only; every source rehash, actor authentication, scientific adjudication and execution authorization is a separate gate. When a new assignment's source is missing, preserve a scoped HOLD instead of replacing it with chat order. No non-owner external writer may alter this norm or invent return slots.
