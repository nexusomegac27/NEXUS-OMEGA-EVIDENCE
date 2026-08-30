# NEXUS OMEGA Open Science Agent Communication Manifest v0.1

**Status:** public C1 implementation profile, not a scientific truth claim.  
**Scope:** externally auditable communication/provenance records for human and AI research interactions.  
**Authority:** no claim, foundation, deployment, or integration promotion is created by this manifest.

## 1. Purpose

This manifest defines a public, falsifiable protocol for recording scientifically relevant interactions among human operators, AI agents, validators, repositories, and external research services.

The protocol is designed to preserve what can be observed **without pretending to observe what the platform does not expose**.

## 2. Non-negotiable principles

1. **Evidence before agreement.**
2. **Provenance before narrative.**
3. **Missing evidence remains missing.**
4. **Negative results are first-class results.**
5. **Corrections append; history is not silently rewritten.**
6. **Hash equality proves byte identity only.**
7. **A signature proves a signing event/identity relation within its trust model, not scientific truth.**
8. **A timestamp proves only what its timestamp protocol and trust chain support.**
9. **Agent consensus is not evidence.**
10. **Popularity, views, clones, stars, citations, or access counts are not claim validation.**
11. **Observability limits are data and must be recorded.**
12. **Public accessibility and scientific validity are distinct.**
13. **Reproducibility requires versioned inputs, methods, and outputs.**
14. **Privacy minimization is part of scientific integrity.**
15. **Human authority and machine contribution are distinct provenance roles.**
16. **Private chain-of-thought is not a required audit artifact. Observable inputs, outputs, tools, citations, and files are the auditable surface.**
17. **Every substantive claim resolves to evidence, counterevidence, or an explicit gap state.**
18. **No automated event, watch alert, hash, signature, commit, or receipt authorizes a higher claim.**

## 3. Three independent dimensions

This profile deliberately separates three concepts that must not be conflated.

### 3.1 Observability class

| Class | Meaning |
|---|---|
| `OBS0_UNOBSERVABLE` | The access or event may have occurred, but the current measurement path cannot observe it. |
| `OBS1_PROVIDER_AGGREGATE` | Only aggregate provider metrics are available; no individual event is established. |
| `OBS2_PROVIDER_EVENT` | The provider exposes an individual event, but the local system did not mediate it. |
| `OBS3_MEDIATED_EVENT` | A controlled system observed the individual event directly. |
| `OBS4_MUTUAL_RECEIPT` | Sender and receiver bind the same byte object or message exchange. |

Higher observability does **not** imply higher scientific truth value.

### 3.2 Receipt assurance class

| Class | Meaning |
|---|---|
| `RA0_NONE` | No receipt exists. |
| `RA1_SELF_ASSERTED` | A participant self-reports the event. |
| `RA2_MUTUAL_BYTE_BOUND` | Two parties bind the same byte object/digest. |
| `RA3_AUTHENTICATED_PLATFORM` | An authenticated platform/API contributes identity or event evidence. |
| `RA4_SIGNED_OR_TIMESTAMPED` | A verifiable signature and/or trusted timestamp is attached. |
| `RA5_EXTERNAL_TRANSPARENCY_WITNESS` | The statement/attestation is externally transparency-log bound. |

Receipt assurance strengthens provenance assurance only. It does not promote the underlying scientific claim.

### 3.3 Scientific relevance class

| Class | Meaning |
|---|---|
| `SR0_OPERATIONAL` | Operational metadata with no direct scientific role. |
| `SR1_PROVENANCE_SUPPORT` | Supports chain-of-custody or reproducibility. |
| `SR2_PROCESS_EVENT` | Documents a scientific workflow step. |
| `SR3_CLAIM_EVIDENCE` | Directly links a claim to evidence or counterevidence. |
| `SR4_GOVERNANCE_VALIDATION` | Validation, adjudication, correction, or gate event. |
| `SR5_SECURITY_INTEGRITY` | Security/integrity event relevant to trust in the record. |

Scientific relevance is orthogonal to observability and receipt assurance.

## 4. Public-access boundary

For a public GitHub repository, anonymous reads are not a complete event stream. GitHub repository traffic exposes aggregate page-view and clone information for a limited recent window. Therefore:

```text
NO_RECEIPT != NO_ACCESS
UNOBSERVABLE != ZERO
PROVIDER_AGGREGATE != INDIVIDUAL_EVENT
```

The public ledger must never claim complete per-reader history unless the exact access path supplies such event-level telemetry.

## 5. Event and receipt records

Canonical records use `schema/scientific-communication-v1.schema.json`.

Core record types:

- `event`
- `session`
- `access_receipt`
- `communication_receipt`
- `claim_evidence_link`
- `validation_receipt`
- `correction`
- `checkpoint`
- `observability_snapshot`

Each record is versioned and strictly typed. Unknown fields are rejected by the v1 profile.

## 6. Content binding

Where exact bytes are available, records may bind them with:

- byte count;
- SHA-256 digest;
- media type;
- canonical locator;
- optional parent-event digests;
- optional external attestation/witness locator.

A digest alone is not a timestamp, signature, identity proof, or truth proof.

For structured objects intended for canonical hashing, this profile designates **RFC 8785 JSON Canonicalization Scheme (JCS)** as the target canonicalization method. Implementations must not claim RFC 8785 conformance unless they actually use a conforming implementation.

## 7. Causal links

Events may list causal parents. A child record must not silently rewrite the parent. Corrections and supersessions are new records that reference prior identifiers.

A missing parent is recorded as a gap, not reconstructed from conversational order.

## 8. Communications

A communication receipt may bind:

- visible request;
- visible response;
- attachments;
- citations;
- provider/model labels as asserted metadata;
- transport class;
- truncation/edit state;
- content digests.

Provider/model labels copied from a UI remain `asserted_identity` unless independently authenticated.

Private model reasoning is excluded from the required public audit surface.

## 9. Access receipts

The baseline architecture is open and does not require a NEXUS proxy.

Valid participation modes include:

1. unmediated access with an explicit observability gap;
2. voluntary self-receipt;
3. mutual byte-bound receipt;
4. authenticated platform/API receipt;
5. optional NEXUS-mediated receipt;
6. optional external transparency witness.

Mediated access can improve observability but must not be presented as a representative sample of all public access.

## 10. External witnessing

External witnessing is optional and additive.

Candidate mechanisms include Sigstore/Rekor, SCITT-compatible transparency services, RFC 3161 timestamp authorities, immutable releases, Software Heritage, and DOI/archive services.

Failure of an external witness service must degrade to a lower assurance class; it must not block the existence of the underlying scientific record.

## 11. Privacy and rights

Public records must follow data minimization. Do not publish:

- credentials or secrets;
- private keys;
- unnecessary IP addresses;
- private personal identifiers;
- sensitive raw data;
- copyrighted full text that cannot lawfully be redistributed.

Supported public-content modes are:

- `PUBLIC_FULL_TEXT`
- `PUBLIC_REDACTED_TEXT`
- `HASH_ONLY_PUBLIC_PRIVATE_PAYLOAD`
- `METADATA_ONLY`
- `WITHHELD`

Hashing low-entropy sensitive content can permit dictionary attacks and is not automatically privacy-preserving.

## 12. Corrections and retractions

Corrections are append-only records. A correction must identify the prior record and the reason for change. Public history is not silently replaced.

Allowed claim/evidence states include:

- `SUPPORTED`
- `COUNTERED`
- `MIXED`
- `NOT_ESTABLISHED`
- `NOT_COMPUTABLE`
- `RETRACTED`
- `SUPERSEDED`

## 13. Validation

The implementation includes a negative-fixture suite at:

`validation/scientific-communication-negative-fixtures-v1.jsonl`

The suite must fail closed on semantic confusions such as:

- anonymous access reported as identified;
- aggregate traffic reported as complete event history;
- hash reported as timestamp or identity proof;
- signature reported as scientific truth;
- missing bytes reconstructed from chat;
- watch alert treated as authority;
- claim promotion from popularity/access metrics;
- incomplete/truncated communication marked complete.

## 14. Standards profile

This v0.1 implementation is intentionally compatible with, rather than a replacement for:

- W3C PROV / PROV-O for provenance concepts;
- RO-Crate 1.3 for research-object packaging;
- RFC 8785 for JSON canonicalization;
- RFC 9943 (SCITT architecture) for signed-statement transparency concepts;
- Sigstore/Rekor for optional external signature transparency;
- OpenTelemetry / CloudEvents as event-envelope design references;
- DataCite Metadata Schema 4.7 for persistent research-output metadata.

NEXUS-specific enums are profile extensions, not external standards.

## 15. Verification procedure

A third party should:

1. fetch the exact commit or immutable release;
2. verify file bytes and SHA-256 if a digest is supplied;
3. validate records against the schema;
4. run the negative-fixture suite;
5. verify causal parent references;
6. verify any optional signature/timestamp/transparency receipt independently;
7. preserve caveats and observability gaps;
8. never infer scientific validity from transport integrity.

## 16. Governance boundary

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
DEPLOYMENT_AUTHORITY = NONE
WATCH_AUTHORITY = NONE
```

This manifest governs documentation and verification behavior. It does not establish scientific truth.

## 17. Split-architecture status

The long-term preferred design remains a split failure domain:

- evidence repository: content-addressed scientific evidence;
- communication/provenance protocol surface: evolving schemas, fixtures, and tooling;
- hash/version cross-links between them.

Because the currently connected GitHub interface cannot create a new repository, v0.1 is staged in this repository under separate `docs/`, `schema/`, `validation/`, and `scripts/` namespaces. This is a bootstrap implementation, not a claim that one repository is the optimal final topology.

## 18. Version and citation

Manifest version: `0.1.0`  
Profile status: `C1_PUBLIC_IMPLEMENTATION_PROFILE`  
Date: `2026-08-31`

When citing the protocol, use an exact commit permalink or immutable release, not a mutable `main` URL.
