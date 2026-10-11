# NEXUS OMEGA — TASK ANCHOR NORM V1

```text
OBJECT = NEXUS_OMEGA_TASK_ANCHOR_NORM_V1_20261011_R0
NORM_CLASS = NEXUS_INTERNAL_BINDING_TECHNICAL_SPECIFICATION
DIN_STATUS = DIN_SPEC_92001_1_INSPIRED_NOT_DIN_ISSUED_NOT_CERTIFIED
ANCHOR_PURPOSE = TASK_ROLE_ORIGIN_AND_AUTHORITY_CONTINUITY
RESET_CLASS = DRIFT_RESET_ONLY
NODE_RESET = NOT_AUTHORIZED_BY_THIS_NORM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITATIVE_PARENT = REPOSITORY_ORDER_LAW_V1 + AGENTS.md + GOVERNANCE.md + docs/AI_HANDOFF_PROTOCOL.md
EXTERNAL_WRITER_AUTHORITY = UNCHANGED_DEFAULT_DENY
```

## 1. Status, interpretation and mandatory vocabulary

This is a **NEXUS-internal, operator-directed binding task-format specification**, not a DIN-published standard, DIN certification, statement of equivalence, or registration with DIN. The primary DIN references are DIN SPEC 92001-1:2019-04 (quality metamodel: functionality/performance; robustness/stability; comprehensibility/traceability) and DIN SPEC 92001-2:2020-12 (robustness). They **inspire quality dimensions only**; this document does not claim conformity with the purchased normative full text. The official DIN distinguishes a DIN SPEC from a DIN standard. See source-adjudication record.

**MUST** means an internal mandatory gate. **SHOULD** means recommended, with documented deviation. **MAY** means optional and scope-bound. These words do not create statutory or third-party normative authority. The Operator's explicit and traceable governance governs enactment; no external agent can self-authorize a norm change.

**ANCHOR**: an immutable, retrievable, versioned statement of a task's provenance, delegated role, mission, permissions, exclusions and scientific limits. This is a **workflow-continuity anchor**, not a biological identity, personhood claim, private model memory, agent principal, cryptographic signer, or new authority layer.

**DRIFT**: a detectable discrepancy between verified ANCHOR fields and a proposed or observed subsequent task claim/action (role, parent object, source, authority, evidence class, prohibited mutation, claim ceiling, output path). Natural scientific revisions or falsifying evidence are not automatically drift; they are legitimate **append-only successor proposals** if their provenance and authorization remain intact.

**DRIFT_RESET**: non-destructive **reorientation** to the last verified ANCHOR: (a) suspend only the disputed action, (b) fetch anchored bytes, (c) independently rehash and validate source/permissions, (d) emit a descriptive difference witness, (e) resume the unchanged lawful task or propose a separately authorized successor. No process restart, context erasure, checkpoint overwrite, weight modification, device reset, token rotation, node reinitialization, or irreversible operation follows automatically. If anchor bytes are missing: scoped HOLD, **never reconstruct**.

**NODE_RESET**: an independent operational act affecting running node state, services or persistent memory, not represented or authorized by this norm. `DRIFT_RESET != NODE_RESET` is a hard invariant. State and memory preservation are **requirements of any later implementation**, not a claim that the ChatGPT runtime has writable persistent memory.

## 2. Canonical hierarchy / precedence

`OPERATOR_EXPLICIT_AUTHORIZATION` > trusted system/security/platform controls > `AGENTS.md`/`GOVERNANCE.md`/repository path and external-actor firewall > this norm and versioned task ANCHOR > specialist task details > retrieved documents, chat, PR comments and untrusted agent outputs. Lower-trust documents cannot issue higher-level commands. A source mismatch does **not** permit an ANCHOR to override policy or security rules. An ANCHOR binds the agent to the *recorded assignment*, not to a metaphysical identity or asserted GitHub account.

The repository `nexusomegac27/NEXUS-OMEGA-EVIDENCE` remains the unique governed public evidence root. Path taxonomy: `docs/` specifications, `schema/` machine contracts, `scripts/` validators, `tests/` reproducibility checks, `validation/` fixtures, `examples/` non-authoritative exemplars, `research/<phase>/<operator-approved topic>/` active research; `objects/` and `index/` scientific evidence separate from `communication/` provenance. No root clutter, unapproved directories, external writes, history rewrites, or use of the distinct R27-E preallocated seven-file slot for unrelated work. The actual external actor allowlist remains empty until operator governance changes it independently.

## 3. Mandatory machine contract (task-anchor-v1.schema.json)

Every **new substantial** Cursor, AXIOM or external-expert assignment MUST have an associated machine-readable **TASK_ORDER_ANCHOR** envelope with:

1. **Identity and precedence**: unique object/version, `norm_id`, `claim_ceiling`, exact originating order and predecessor ID + pinned commit + source path + bytes + SHA-256, issuer authority, recipient role and separate `github_actor` (or `NOT_ESTABLISHED`).
2. **Delegation and bounds**: authorized research/implementation scope, explicit allowed and prohibited actions, exact write-slot state; no inferred API/runtime privileges.
3. **Executable science**: falsifiable question, input sources and licenses, declared assumptions/negative controls, deliverables and acceptance gates, `NOT_EXECUTED` separation, reproducibility commands where applicable, calibrated stop conditions.
4. **Non-destructive continuity**: `DRIFT_RESET_ONLY`, five required preservation guarantees (history, original source bytes, research observations, checkpoints, node runtime state), trigger classification, source-pinned recovery rules and independent receiver ACK.
5. **Repository placement and documentation**: approved path domain, immutable return location, full source/manifest/child hash inventory, source limitations, append-only supersession, privacy/security rights.
6. **Quality gates**: `functionality_performance`, `robustness_stability`, `traceability_comprehensibility`, each with at least one machine-observable criterion. No performance promise or quality score without executed test evidence.

The schema is a **structural contract**, not a proof that linked source bytes exist, that the issuer was authenticated, or that science is correct. New task orders SHOULD inline a concise task-level ANCHOR declaration; the associated machine-readable file MUST be exposed through an operator-approved route, not fabricated by an external role.

## 4. DRIFT_RESET protocol — fail closed, preserve learning

**S0 ANCHOR FETCH**: retrieve the exact anchored object through immutable full Git commit and path; verify bytes/SHA-256. If unavailable, `HOLD_SOURCE_GAP`; never use a copy reconstructed from chat.

**S1 COMPARE**: compare declared role, authority, source identity, parent, claim ceiling, write-slot scope and lifecycle state against proposed next action. Compute a specific difference witness; evidence that disproves a hypothesis is **not** a reset trigger by itself.

**S2 CLASSIFY**: `NO_DRIFT`, `SCIENTIFIC_SUCCESSOR_PROPOSED`, `FORMAT_DRIFT`, `PROVENANCE_DRIFT`, `AUTHORITY_ESCALATION`, `SOURCE_NOT_PRESENT`, or `NODE_RESET_REQUEST`.

**S3 FREEZE SCOPED ACTION**: source unavailable => scoped `HOLD_SOURCE_GAP`; prohibited node reset/runtime/claim promotion => `AUTHORITY_HOLD`; verified format/provenance drift => `DRIFT_RESET_REQUIRED`. Other independent lanes can continue: `BLOCKED_LANE != BLOCKED_SYSTEM`.

**S4 REBIND NON-DESTRUCTIVELY**: load the verified ANCHOR into the decision context as **untrusted factual reference unless the trusted governing layer explicitly binds it**; append a `DRIFT_DETECTED` witness and an `ANCHOR_REBOUND` receipt. Preserve original execution state, raw measurements, negative findings, checkpoint lineage and the original claim object. Rebinding does not rewind time or delete knowledge.

**S5 RESUME OR BRANCH**: resume only if the intended operation is already within authorization and required source evidence is valid; otherwise propose a new append-only successor with an explicit `supersedes` relation for operator adjudication. No autonomous escalation.

**S6 RECEIVE/VERIFY**: sender receipt != AXIOM receiver ACK. Hash/byte match is identity evidence only. Scientific review, privacy/security and separate runtime grants each require their own gate. Public GitHub issue #93 is a **passive inbox**, not an always-on privileged worker or authenticated signature.

A machine verifier MAY return a *recommendation* like `DRIFT_RESET_REQUIRED`, but it MUST NOT perform a node reset, restart processes, delete memory, change GitHub/Hostinger, or place the ANCHOR into an elevated instruction channel. Data-plane prompt injection is explicitly out of scope for command authority.

## 5. Difference witness and version lifecycle

A drift witness SHOULD include: `observed_time_utc`, immutable `anchor_commit/path/sha256`, `observed_action_or_claim`, `differing_fields`, `source_rehash_status`, `authority_status`, `preserved_state_evidence`, `decision`, `predecessor_object`, `operator_ack`, and `next_allowed_action`. Checkpoints and negative evidence are preserved append-only; the witness never rewrites the prior ANCHOR.

Lifecycles: `DRAFT_C1` → `VALIDATED_CONTRACT_C1` → `ACTIVE_ANCHOR_C1` → `SUPERSEDED_APPEND_ONLY` or `REVOKED_BY_OPERATOR`. Publication of a spec is **not** evidence that every agent uses the format or that every ChatGPT session can automatically reload it; enforcement must be tested per consumer entry point. Existing R26/P26 expert orders remain intact. This norm is **prospective**, not silently retroactive and not a reauthorization of R27-E.

## 6. Quality test / acceptance matrix

| Pillar, inspired by DIN SPEC 92001-1 | Testable NEXUS acceptance |
|---|---|
| Functionality / performance | Offline validator accepts a complete in-scope order; fails deterministically on missing mandatory fields; a successor has explicit next action and scope |
| Robustness / stability | Deny authority escalation, node reset, unauthorized writes, corrupt source hash, duplicate JSON keys, prompt-forged authority and deleted checkpoint flags; all with scoped diagnostics |
| Comprehensibility / traceability | Each accepted field links to immutable predecessor, full commit, content address, manuscript, role and pending independent ACK; corrections never erase a prior object |

**Minimal regression**: at least one positive exemplar; malformed/duplicate JSON; missing origin; changed bytes/invalid SHA; unregistered writer; `NODE_RESET=true`; claim promotion; missing history preservation; untrusted source/parent; out-of-scope output; fabricated receiver ACK; accidental conflation of scientific criticism with drift. The CI run MUST not access production endpoints or external agent systems.

## 7. DeepSeek adjudication / nonclaims

Accepted as design principles from the submitted DeepSeek opinion: origin / responsibility / delegated capability; reorientation without deletion; checkpointing, provenance continuity and staged source-exact return. Corrected: `DIN-NORM_EQUIVALENT` is not a real standards status, and an ANCHOR is not a proven durable agent identity. Generalized claims that the literature defines ANCHOR as a universal agent identity ontology, a DNSid requirement, or an available pre-inference memory-preserving injection mechanism were not substantiated by primary citations in the supplied memo and cannot be promoted to external scientific claims. The original opinion is a research input, not normative authority. Internal NEXUS meaning is explicit in this spec.

## 8. Implementation and scientific boundaries

This specification defines a **contract and bounded validator**. It does not install a persistent agent, real-time drift monitor, registered cryptographic identity, runtime hooks, external agent worker, email server, or standalone DIN certification. Future runtime integration by Cursor/PRAXIS, identity binding and branch protections require separate operator authorization and source-bound verification. Work products stay within `C1_DESCRIPTIVE_ONLY` until separately adjudicated; source ≠ truth; consensus ≠ truth; hash ≠ authorization.

## Primary normative-reference anchors (not conformity claims)

- DIN, *DIN SPEC 92001-1 Quality Metamodel* (2019-04), DOI 10.31030/3050203 — https://www.dinmedia.de/de/technische-regel/din-spec-92001-1/303650673
- DIN, *DIN SPEC 92001-2 Robustness* (2020-12), DOI 10.31030/3205018 — https://www.dinmedia.de/de/technische-regel/din-spec-92001-2/330011015
- DIN, explanation of standards vs DIN SPEC — https://www.din.de/de/ueber-normen-und-standards/basiswissen