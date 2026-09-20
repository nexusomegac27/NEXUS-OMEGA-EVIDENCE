# R3 primary-source crosscheck

Audit date: 2026-09-20.

## Ed25519 / EdDSA

RFC 8032 specifies EdDSA and the Ed25519 instantiation and provides implementation-oriented details
and test vectors.

- https://www.rfc-editor.org/info/rfc8032/

NEXUS use: cryptographic signature primitive for the public reference receipt. Signature validation
is not treated as proof of human identity, authorship or scientific truth.

## Zero-knowledge proof scope

NIST defines a zero-knowledge proof as a cryptographic scheme in which a prover convinces a verifier
that a statement is true without revealing additional information beyond that fact.

- https://csrc.nist.gov/glossary/term/zero_knowledge_proof

NEXUS use: optional privacy/selective-disclosure research for precisely formalized predicates.

## Cedar

Cedar is an authorization policy language/engine. Its reference documentation separates policy
semantics and authorization decisions from application business logic and documents formal
verification work for validation soundness.

- https://docs.cedarpolicy.com/
- https://docs.cedarpolicy.com/policies/validation.html
- https://docs.cedarpolicy.com/other/security.html

NEXUS use: authority-boundary research candidate only. The public R3 reference harness is a small
local deterministic policy model; it is **not** a Cedar execution claim.

## NVIDIA MAIW authority boundary

The public Multi-Agent Intelligent Warehouse architecture states that the model/agent does not
receive the write path directly; typed proposals are evaluated by deterministic governance before a
bounded executor reaches write capabilities.

- https://github.com/NVIDIA-AI-Blueprints/Multi-Agent-Intelligent-Warehouse

NEXUS use: open architectural precedent, not evidence of NEXUS production security.
