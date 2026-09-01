# NEXUS OMEGA GitLab Parallel-Forge Policy V1

Status: RESEARCH/FOUNDATION C1
Date: 2026-09-01

## Purpose

GitLab is a second, independent forge and CI/provenance failure domain alongside GitHub. It is not a cosmetic mirror and does not automatically inherit authority from GitHub.

## Core invariants

- CLAIM_CEILING = C1 unless separately promoted.
- GITHUB_SUCCESS != GITLAB_SUCCESS.
- GITLAB_SUCCESS != GITHUB_SUCCESS.
- CROSS_FORGE_MATCH requires independently observed byte/content digests or explicitly defined Git-object equivalence.
- Provider-native Git object IDs are provenance locators, not the canonical scientific digest domain.
- Canonical byte binding uses SHA-256.
- PR/MR comments are transport; canonical evidence is immutable repository content plus validated receipts/events.
- SOURCE_OBJECT_SUBSTITUTION = PROHIBITED.
- HISTORICAL_REWRITE = PROHIBITED.
- FORCE_PUSH_FOR_RECONCILIATION = PROHIBITED.
- BLOCKED_FORGE != BLOCKED_SYSTEM.

## Forge roles

### GitHub

Current public evidence/communication forge and active PR #11 transport surface.

### GitLab

Independent secondary forge used for:

1. clean-room reproduction of validators;
2. independent CI execution;
3. cross-forge byte/digest reconciliation;
4. independent branch/MR review history;
5. provider-failure-domain testing;
6. future SLSA/in-toto/Sigstore-compatible provenance experiments;
7. research-object metadata and archival export preparation.

Neither forge is declared universally authoritative. Authority is object- and receipt-specific.

## Replication states

- NOT_REPLICATED
- CONTENT_REPLICATED_UNVERIFIED
- CONTENT_REPLICATED_SHA256_MATCH
- GIT_GRAPH_REPLICATED
- CI_REPRODUCED
- SEMANTIC_VALIDATION_REPRODUCED
- CROSS_FORGE_DIVERGENCE
- SOURCE_NOT_PRESENT

A higher state does not imply a lower-level scientific claim promotion.

## Required cross-forge record

Each promoted cross-forge record SHOULD bind:

- source forge/repository/ref/commit;
- destination forge/repository/ref/commit;
- file/object role;
- byte count where available;
- SHA-256 digest;
- provider-native object ID where useful;
- CI run/pipeline identity;
- validator version;
- timestamp evidence;
- actor/producer;
- independent validator;
- discrepancy classification.

## CI independence

The same validator may run on both forges, but one provider's passing result is not imported as the other's result. GitLab must execute its own pipeline and preserve its own job/pipeline receipt.

## Attestations

Target model:

artifact -> SHA-256 -> SLSA provenance -> in-toto statement -> signature/identity -> transparency/archival witness.

GitLab-native provenance attestations are currently treated as experimental/additive. They must not replace local SHA-256 manifests, independent replay, or external archival witnesses.

## Scientific object layer

For research software and evidence bundles, future stable packages SHOULD support FAIR4RS-oriented metadata and RO-Crate export. Software Heritage SWHIDs may be added as independent intrinsic archival identifiers after public archival is established.

## Merge/deploy boundary

This GitLab foundation authorizes research branches, validators, CI, receipts, and draft merge requests. It does not authorize production deployment, claim promotion, destructive synchronization, force push, or automatic merge to either forge.
