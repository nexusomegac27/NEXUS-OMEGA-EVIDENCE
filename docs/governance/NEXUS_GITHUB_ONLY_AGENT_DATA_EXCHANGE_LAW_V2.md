# NEXUS OMEGA · GitHub-Only Agent Data Exchange Law V2

OBJECT = NEXUS_OMEGA_OPERATOR_GITHUB_ONLY_AGENT_DATA_EXCHANGE_LAW_20261029_R0
STATE = OWNER_BRANCH_POLICY_CANDIDATE_PENDING_REVIEW_AND_MERGE
OPERATOR_DECISION = 2026-10-29
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SCOPE = ALL_NEW_MATERIAL_HANDOFFS_TO_AGENTS_WITH_VERIFIED_GITHUB_ACCESS
NATIVE_APP_R3 = HOLD
PR_BRANCH = codex/github-expert-exchange-foundation-20261029
PUBLICATION_OR_RUNTIME_AUTHORIZATION = NONE

## 1. Two channels: strict separation

**Human instruction channel:** AXIOM authors the pure work order. The Operator may manually forward only that work order to the designated agent. The work order contains immutable GitHub references (repository, full commit SHA, exact path, byte length, SHA-256), expected receipt format, role, permitted actions and required source closure. It must not embed, attach or retype evidentiary source files, packages, original returns, entire research stacks or substitute summary bytes.

**GitHub data channel:** For EVERY expert with verified GitHub access, all predecessor documents, scientific source artifacts, package manifests, test corpora, source revisions, result artifacts, machine receipts and their subsequent transfers between AXIOM/Cursor/expert travel exclusively through the operator-governed GitHub interface. Expert independently fetches ALL mandate-required inputs at pinned full commit/path and recomputes SHA-256. An URL, SHA claim, model name, issue comment, producer-side receipt, webhook arrival or local file copy is NOT recipient evidence. When independent proof is absent, classify `RECEIVER_INDEPENDENT_ACK=NOT_ESTABLISHED` and delivery `STAGED_NOT_TRANSMITTED`.

This channel rule is prospective for new work. It does not delete or relabel historical operator-supplied artifacts. No manual file hunt/ZIP copying by the Operator is a valid ordinary workflow.

## 2. Only permitted exception: scientifically necessary manual transfer

An exception is not convenience, a chat-only agent's missing connector, incomplete packaging, missing source graph, missing GitHub permission, GitHub rate limit, adapter outage or a request to save development time. Stop the affected lane and repair the GitHub route. An agent WITHOUT verified GitHub data access cannot be treated as satisfying this law.

A narrowly scoped manual data transfer may occur **only** when demonstrably indispensable for scientific integrity, reproducibility or lawful handling of a source that cannot otherwise be retrieved via the controlled GitHub interface. Before transfer, record:
`EXCEPTION_ID`, exact `OBJECT/PREDECESSOR`, source classification, independently evidenced scientific necessity, why GitHub route cannot safely support that specific object, who authorized the exception, full bytes/SHA-256 and receiver identity, consent/privacy/license review, time-limited scope, reconciliation/closure plan, and independent source hash acknowledgement. Do NOT publicly upload secrets, private sensor data, protected personal data, credentials or rights-uncleared files merely to satisfy the GitHub rule. If another secure GitHub-accessible private repository is required, it must be owner-governed and separately authorized; this policy creates none. Exceptions are append-only `MANUAL_EXCEPTION_PRESERVED`, never an implicit predecessor PASS. After the scientific constraint ends, register a GitHub evidence anchor/redacted commitment when legally permissible, without false claim that public bytes exist.

## 3. Mandatory dispatch automaton

```
ORDER_DRAFT
 -> SOURCE_GRAPH_RESOLVED
 -> REQUIRED_BYTES_AVAILABLE_AT_PINNED_GITHUB_REFS
 -> PRIVACY_AND_LICENSE_APPROVED
 -> COMPLETE_MANIFEST_INDEPENDENTLY_VERIFIED
 -> OWNER_DISPATCH_APPROVED
 -> MANDATE_READY_FOR_AGENT
 -> AGENT_GITHUB_FETCH
 -> INDEPENDENT_RECEIVER_REHASH
 -> IDENTITY_BOUND_RECEIVE_ACK
 -> WORK_AUTHORIZED_BY_SEPARATE_ORDER
 -> EXPERT_RETURN_AT_PREALLOCATED_GITHUB_SLOT
 -> OWNER_INDEPENDENT_REHASH_AND_ADJUDICATION
```

Any missing required parent/source/member, unsigned/unpinned mutable pointer, digest mismatch, unregistered actor, unauthorized write slot or policy ambiguity => `SOURCE_GAP_BLOCKED` / `AUTHORITY_HOLD`. Independent lanes may continue. Never reconstitute missing bytes from chat memory. The `latest` index is for discovery only; the full commit SHA and exact byte digest are authority for version-specific receipt.

Each expert mandate must include a **closure inventory** listing transitive required predecessors and precise source objects. A ZIP with missing declared sums MUST fail before dispatch. Seal is the graph AND its retrievability to the intended agent, not merely local packaging.

## 4. Actor permissions and trust

GitHub read access != authorization to run code or write. The existing `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` currently has `external_actor_allowlist=[]`; the law does not auto-register an actor. All direct GitHub external writes require verified GitHub principal, owner-provisioned exact create-only paths, separate least-privilege GitHub App installation or actor, protective branch rules and owner-only merge. Model branding, agent assertions and passed tests are not credentials. Untrusted PR content cannot execute in privileged CI.

The public `nexusomegac27/NEXUS-OMEGA-EVIDENCE` contains **public-safe** evidence only. Use governed private GitHub source locations if separately approved and technically supported for sensitive materials. GitHub commit/PR != publication on Hostinger/WWW.

## 5. Required technical mechanisms

Build **on** the existing `research/pipeline/` (stable snapshots), `communication/` (event/receipt ledger), `objects/` and `index/` (scientific evidence), `schema/`, `scripts/`, `tests/`, CI, and the existing github-implant view; no shadow filesystem or uncontrolled top-level directory.

- GitHub-source resolver: authenticated fetch by full commit + exact path, path/digest/size check, strict JSON, recursive predecessor DAG closure and rights/privacy classification.
- Deterministic packager/validator: exact manifest coverage, no symlinks/traversal/duplicate paths, fails hard for omissions and non-matching hashes. Reuse `scripts/nexus_expert_exchange.py` after independent test.
- Dispatcher: persistent queue, idempotent attempts, bounded retries, explicit `STAGED`, `SENT`, `RECEIVED_VERIFIED`, `FAILED` statuses; reconciles missed/failed webhooks from GitHub API. Webhooks are trigger hints, not durable evidence.
- Agent adapters: verify real GitHub read identity/capability and optional write/owner-bridge route per provider; real independent GitHub fetch receipts; no fabricated 'agent running' from a link.
- Return verifier: enforce registered slots, actor identity, independent receiver hash/bytes, causal chain and independent AXIOM adjudication.
- Dashboard: public-safe status only; no authority-sensitive secrets, source packages, or privileged hooks in public github-implant.
- Benchmark: predeclared baseline of operator manual artifact handoffs and a 90%-reduction acceptance target, with evidence of complete E01–E10 synthetic/pilot workflows. A percentage without a denominator is NOT PASS.

Current supporting GitHub PR: #185 remains **draft**, no merge, no deployment, no runtime or receiver ACK. Current Cursor return: `32/32 PASS_REPORTED`, `AUTO_GITHUB_SOURCE_FETCH=NOT_IMPLEMENTED`, `EXPERT_ADAPTERS=NOT_CONNECTED`. No `NATIVE_APP_R3` until independently verified closure and separate Operator decision.

## 6. Adoption and enforcement

This V2 record is a **reviewable policy candidate on owner-controlled branch**, not an assertion of CI enforcement on `main`. Its actual adoption requires an owner-reviewed merge, version-bound links from `docs/AI_HANDOFF_PROTOCOL.md` / `AGENTS.md`, schema and test gates in CI, and separately verified required branch checks. Until then, the Operator directive governs our task-scoping; this file alone cannot prevent a noncompliant agent from sending attachments.

Enforcement fixtures: reject attached/manual research ZIP as ordinary handoff; accept human manual pure work order with anchored GitHub references; reject missing transitive ancestor, source hash mismatch, invalid actor, URL-only receipt, partial manifest, wrong return slot, private data on public surface and unapproved manual exceptions. Positive synthetic E01→E10 pilot must independently fetch and ACK each source. Exact test evidence required.

No claim promotion, private publication, App R3, factory reset, live expert activation or WWW mutation by this document.

## 7. Primary source anchors

- GitHub App least privilege: https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app
- Failed webhook delivery handling: https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries
- GitHub webhook best practices: https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
- GitHub branch protection and rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
