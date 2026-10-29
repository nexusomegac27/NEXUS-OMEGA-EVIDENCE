# NEXUS OMEGA — AXIOM Alpha-Node — F0 source identity collision guard V2 — 2026-10-29

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_F0_SOURCE_IDENTITY_COLLISION_V2_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=8b7ac2a34175f520f7fd9c1fe738cb902f0e6c41
PINNED_MAIN_PARENT=09f517e544056c7217a800f1f596cedb356db2c2
PREDECESSOR_ISSUE93_RECEIPT=6487895710
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/188
BASELINE_PATH=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_source_graph_closure_f0_v1_20261029.py
BASELINE_BYTES=5274
BASELINE_SHA256=c39208bffdc60ef8072cc7fb82a8aead459870f840e4ff7c9a0e4f79a59e051b
BASELINE_GIT_BLOB=0a156f3b0044b1f389237e53e8a3175f13f2483a
FROZEN_ORACLE_FIRST_COMMIT=9fd63e94f25f43b4f9ed709734a3966650f9c6dd
CANDIDATE_SECOND_COMMIT=86aa500a7452b8f38bed89d2b4d8dc94122082bd
PRODUCTION_INTEGRATION=NO
EXTERNAL_DISPATCH=NO
WWW_PARITY=NOT_ESTABLISHED

## Observe, original bytes and negative hypothesis

The source-graph F0 V1 from PR #188 was retrieved at the immutable main commit and locally reconstructed with an exact 5,274-byte SHA-256 match and Git-blob match. Its source-node IDs are unique, but two different IDs can declare the same full commit SHA and repository path with different bytes, each individually passing SHA-256 and Git-blob verification. This is an internally contradictory source identity for a Git tree, regardless of whether external GitHub origin is authenticated.

**Negative hypothesis:** A graph is reported locally byte-consistent despite two reachable source nodes naming identical (commit,path) and incompatible content. A receiver relying only on V1 can mistake inconsistent aliases for a closed source inventory.

**Falsifier:** Any accepted conflicting (commit,path) pair fails the V2 hypothesis. Valid aliasing of identical content at the same (commit,path) must remain accepted. Revisions of the same path on different commits and distinct paths on one commit must remain accepted.

## Pinned baseline, frozen evaluator, isolated candidate

Only additive files are proposed in the existing R16 Alpha-Node research lane; no baseline or governance files are edited.

- Frozen black-box oracle: frozen_source_graph_identity_f0_oracle_v1_20261029.py, 4,982 bytes, SHA-256 0026fcd56ec479b2381838c86353b0c75b34e9e3ff27b04df8834cafe6921056, Git blob 07b75d0fa10a8fc04036c18c6e2606aa6e7c409b; committed FIRST.
- V2 candidate: alpha_source_graph_identity_f0_v2_20261029.py, 2,318 bytes, SHA-256 766e13749445d8193ab5402fa518d2eebefb456445b8ca23452287a05af1579a, Git blob 88b0247a0be609c6e40c7ddb9ce39c7bfd9da2c8; committed SECOND.
- V2 executes the existing V1 byte/graph checks from the locally pinned, SHA-256-verified source and then requires one consistent byte binding per (commit,path). V1 is not changed. Its source is compiled in memory without a Python bytecode cache write.

**Independent local subprocess evaluation:** Same frozen 18-case evaluator with V1 as candidate: **14/18 PASS**, four conflicting-identity negative fixtures incorrectly accepted. With V2: **18/18 PASS**, all four rejected. Five positive controls remain accepted; nine other negative controls retain fail-closed behavior. The evaluator does not import candidate logic or modify itself. An additional V1-source-drift fixture (altered local baseline file) was rejected with BASELINE_SOURCE_DRIFT, exit 2. A mutant skipping the new identity comparison reverts to the observed 14/18 result. These are local synthetic tests, not external third-party replication.

Reproduction in this directory, with the first command expected to report four failed tests and the second expected to pass:

1. AXIOM_CANDIDATE=alpha_source_graph_closure_f0_v1_20261029.py python frozen_source_graph_identity_f0_oracle_v1_20261029.py -q
2. python frozen_source_graph_identity_f0_oracle_v1_20261029.py -q

## Decision and hard limits

**Before/after metric:** Four out of four targeted source-identity contradictions were falsely accepted by V1 and rejected by V2; complete frozen suite 14/18 to 18/18. This is a bounded synthetic validator improvement, not a measured decrease in operator effort or live handoff success-rate improvement.

Input bytes, declared commit IDs, paths, rights flags and provenance remain caller-supplied. A coherent but forged (commit,path,bytes) pair remains an explicit counterexample to authenticated origin. Neither V1 nor V2 performs an authenticated GitHub receiver fetch, authorizes READY_FOR_EXPERT, establishes independent receiver ACK, executes expert research, publishes to WWW or changes any runtime. No self-approved oracle change, model-weight change, external actor registration, new scheduler or pipeline.

Project-level 90% handoff and 100% readback rates remain NOT_COMPUTABLE because the authenticated complete eligible numerator and denominator, including failed attempts, are unavailable. The scoped C1 result must not be generalized beyond the frozen synthetic fixtures.
