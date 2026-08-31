# AXIOM R5 formalization research lane

This lane contains independent AXIOM research and formalization work derived from the live NEXUS OMEGA repository plus public primary standards. It is intentionally separate from `research/r5/qwen-coder/`.

```text
ROLE = AXIOM_RESEARCHER_AUDITOR
CLAIM_CEILING = C1
QWEN_PRODUCER_RETURN = NOT_SUBSTITUTED
INDEPENDENT_CURSOR_VALIDATION = NOT_YET_EXECUTED
STABLE_R5_INTEGRATION = NOT_YET_AUTHORIZED
```

## Scope

The initial delta targets QWEN R5 work packages that can be independently formalized from public standards and current repository code without relying on an unavailable producer return:

- WP-B — object-role type system
- WP-C — typed digest domains
- WP-D — manifest self-binding projection
- WP-E — RFC 8785 / JCS interoperability
- WP-F — receipt type system
- WP-G — monotonic status / transition model
- WP-H — failure-code registry
- WP-I — provenance graph model
- WP-K — attestation/transparency profile
- WP-L — GitHub required-check identity, extending the already-recorded live platform audit
- WP-M — ledger concurrency and crash-consistency gap analysis

## Research-only boundary

Files in this lane are candidates. They do not change `schema/r5/`, `scripts/r5/`, `tests/r5/`, or `validation/r5/` semantics by their mere presence. Promotion to stable R5 layers requires separate implementation plus independent validation.

## Primary standards baseline

The lane uses, among others:

- RFC 8785 — JSON Canonicalization Scheme (JCS)
- JSON Schema Draft 2020-12 Core and Validation
- in-toto Attestation Framework v1.x
- SLSA v1.2 and SLSA provenance v1 predicate
- Sigstore / Rekor transparency model
- RFC 9943 — SCITT Architecture
- RFC 3161 — Time-Stamp Protocol
- GitHub Rulesets / required-status-check documentation

See `PRIMARY_SOURCE_REGISTER_20260831_R0.json` for exact source locators and research use.
