# G13 — A2A / MCP INTEGRATION BOUNDARY (Lane 1)

CLAIM_CEILING: C1_DESCRIPTIVE_ONLY · LAST_VERIFIED 2026-10-05 · Sources in `G01_part_lane1.csv`.

## 1. Pinned versions (verified)

| Protocol | Version to cite | Evidence | Note |
|---|---|---|---|
| A2A | **Protocol version 1.0**. The spec page says "Latest Released Version 1.0.0". The latest GitHub release is **v1.0.1 (2026-05-28T11:34:36Z = 13:34 Berlin)**. v1.0.0 was released 2026-03-12T16:34:41Z (17:34 Berlin, CET). | L1-004, L1-005, L1-006 | Spec §3.6: versions are Major.Minor and patch numbers MUST NOT be used in negotiation. Clients send an `A2A-Version` header. Governance: a Linux Foundation project (donated by Google), TSC of 8 companies. **Not an SDO standard.** The words "stable / production-ready" are UNVERIFIED (MA-L1-06). |
| MCP | **2026-07-28** (current); previous 2025-11-25 | L1-007..L1-010 | The 2026-07-28 revision is stateless: no initialize handshake, no sessions, protocolVersion sent per request in `_meta`, `server/discover`, tasks moved to an extension, Roots/Sampling/Logging deprecated. Authorization builds on the OAuth 2.1 **Internet-Draft** (MCP cites -13; -16 is current [L1-052]). |

## 2. What each layer already solves (do not re-implement)

| Concern | A2A 1.0 | MCP 2026-07-28 | Consequence for NEXUS |
|---|---|---|---|
| Agent discovery / capability advertisement | AgentCard; optional JWS signatures over RFC 8785-canonical JSON; keys via kid/jku or trusted store; expired/revoked keys MUST NOT be used (§8.4) | `server/discover`; tool listing | NEXUS consumes these. An AgentCard signature authenticates the card's publisher; it does **not** prove the agent's claims are true. |
| Transport bindings | JSON-RPC, gRPC, HTTP/REST | stdio, Streamable HTTP | Out of NEXUS scope. |
| Authentication | securitySchemes (OAuth2 incl. device code/PKCE, mTLS, API key, OIDC) | OAuth-based; RFC 9728 metadata; RFC 8707 resource indicators; client MUST validate `iss` | NEXUS should not define a new authN scheme. |
| Per-request authorization | Implementation-specific (§7.5); servers MUST authorize every request and scope results (§13.1); in-task `TASK_STATE_AUTH_REQUIRED` (§7.6) | Servers MUST validate token audience; token passthrough forbidden; consent before tool invocation; annotations untrusted | NEXUS policy can be the **policy decision point** that these hooks call. That is where Capsule V2 (G11) would plug in. |
| Task lifecycle | Tasks, status, artifacts, streaming, push notifications | Tasks only as an extension | NEXUS records the lifecycle as evidence; it does not control it. |
| Security posture | Enterprise auth hooks | "MCP itself cannot enforce these security principles at the protocol level"; attack catalogue (confused deputy, token passthrough, SSRF, state handle hijacking, local server compromise) | NEXUS must assume a hostile tool/server and treat tool outputs as untrusted inputs to epistemic gates. |

## 3. Boundary statement (normalized)

- A2A and MCP are **interaction/transport layers**. NEXUS sits **above** them (as an evidence and claim-governance layer) or **alongside** them (as a policy decision point invoked by their authorization hooks). It **does not replace** them.
- Allowed claim: "NEXUS records A2A/MCP interactions as signed, optionally transparency-registered evidence and evaluates them against NEXUS claim ceilings."
- Not allowed:
  - "A2A/MCP provide governance or truth guarantees";
  - "NEXUS secures A2A/MCP";
  - "an A2A AgentCard signature or MCP OAuth token authorizes a NEXUS claim".

## 4. Integration gates (sec. 35 format)

### G-I01 PROTOCOL_VERSION_PIN
- INPUT: observed `A2A-Version` header / MCP `_meta.protocolVersion`.
- PREDICATE: the value is in an allow-list (A2A "1.0"; MCP "2026-07-28").
- PASS: listed. FAIL: unlisted. UNKNOWN: header absent.
- RECOVERY: record as UNKNOWN_PROTOCOL and do not admit evidence above NAC-0.
- FALSE_POSITIVE_RISK: rejecting a compatible newer minor version. FALSE_NEGATIVE_RISK: a version string spoofed by the counterparty, since it is self-declared.

### G-I02 TOKEN_NOT_AUTHORITY
- INPUT: OAuth/MCP access token or A2A credential present on the request.
- PREDICATE: the NEXUS decision does **not** use the token as proof of NEXUS scope. A separate Capsule V2 AUTHORIZED predicate is required.
- PASS: a separate predicate is evaluated. FAIL: the token alone is treated as authorization. UNKNOWN: the code path cannot be audited.
- RECOVERY: deny the NEXUS-level action.
- FALSE_POSITIVE_RISK: a duplicate authorization burden. FALSE_NEGATIVE_RISK: token passthrough or confused deputy (MCP best practices [L1-010]).

### G-I03 AGENTCARD_SIGNATURE_SCOPE
- INPUT: A2A AgentCard plus its JWS signatures.
- PREDICATE: the signature verifies over RFC 8785 JCS bytes with a key from a pinned store (not only from jku).
- PASS: verified and pinned. FAIL: invalid. UNKNOWN: unsigned card. The spec makes card signing optional: clients SHOULD verify at least one signature *if present*.
- RECOVERY: treat an unsigned card as NAC-0 evidence.
- FALSE_POSITIVE_RISK: JCS edge cases in numbers or Unicode. FALSE_NEGATIVE_RISK: treating a valid card signature as a validity claim about the agent's capabilities.

### G-I04 TOOL_OUTPUT_UNTRUSTED
- INPUT: MCP tool result or annotation.
- PREDICATE: the result enters NEXUS only as an observation, never as a verified fact. Annotations are treated as untrusted (MCP Tools [L1-009]).
- PASS: tagged as an observation. FAIL: promoted to a claim without a gate. UNKNOWN: provenance of the tool server is unknown.
- RECOVERY: hold (UNKNOWN → deny promotion).
- FALSE_POSITIVE_RISK: friction for trusted internal tools. FALSE_NEGATIVE_RISK: semantic laundering through a chain of tools (the term is from draft-bondar-wca-00 [L1-003], an expired draft).

## 5. Exact gaps
- No NEXUS↔A2A/MCP adapter exists in the repos (none found in the main tree). Everything here is a boundary design.
- The A2A "production-ready" wording is unverified. MCP's dependency on an OAuth 2.1 draft is a moving target.
- SAFE DEFAULT: pin the versions above, treat all protocol-level credentials as authentication only, and route NEXUS authority through G11's predicate.
- WHAT WOULD CHANGE THIS: a new A2A minor version (1.1) or MCP revision, or A2A/MCP adding a delegation-attenuation primitive.
