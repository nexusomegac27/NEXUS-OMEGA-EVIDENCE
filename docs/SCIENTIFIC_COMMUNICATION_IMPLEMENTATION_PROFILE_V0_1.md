# Scientific Communication Implementation Profile v0.1

## Decision

This implementation adopts a **split-by-namespace bootstrap** inside `NEXUS-OMEGA-EVIDENCE` because the currently connected interface cannot create a second repository.

The long-term topology remains a separate communication/provenance protocol surface cross-bound to the evidence repository.

## Verified standards baseline (2026-08-31)

- W3C PROV-O: W3C Recommendation, 30 Apr 2013.
- RO-Crate 1.3: Recommendation, published 22 Jun 2026.
- RFC 9943: IETF Standards Track / Proposed Standard architecture for trustworthy and transparent digital supply chains.
- DataCite Metadata Schema 4.7: released 3 Mar 2026.
- GitHub repository traffic: views/clones are aggregate metrics for the last 14 days; not a complete individual-reader log.
- Sigstore Rekor: optional append-only/tamper-resistant transparency layer; not a scientific truth oracle and not a mandatory dependency.

## Corrective decisions from independent review

1. Observability, receipt assurance, and scientific relevance are separate axes.
2. Higher observability does not imply higher scientific relevance.
3. The Gateway is optional.
4. Rekor/SCITT witnessing is optional; absence degrades assurance rather than invalidating the base record.
5. The previous architecture-score inconsistencies are not used as implementation logic.
6. Uncurated auto-collected reference lists are not imported.
7. The unrelated D0/D2 mathematical witness material is not part of this communication protocol implementation.

## Implementation stage

Implemented now:
- public manifest;
- strict schema;
- semantic validator;
- >=36 executable negative fixtures;
- CI workflow;
- public discovery links.

Not implemented yet:
- RFC 8785 canonical hashing engine;
- live append-only ledger writer;
- cryptographic signing;
- RFC 3161 timestamping;
- Rekor/SCITT submission;
- controlled access gateway;
- DOI/RO-Crate publication.

Those later components require separate implementation and validation gates.
