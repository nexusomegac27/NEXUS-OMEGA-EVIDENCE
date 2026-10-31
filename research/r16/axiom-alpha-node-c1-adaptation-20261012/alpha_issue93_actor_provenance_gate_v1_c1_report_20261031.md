# AXIOM Alpha-Node — Issue #93 GitHub actor provenance gate V1 (2026-10-31)

```text
OBJECT=NEXUS_OMEGA_ALPHA_ISSUE93_ACTOR_PROVENANCE_GATE_V1_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=7500742672bca68c5c84e524a1262f9b786a7aef
PREDECESSOR_MAIN=5805c4ed63e3d0aad4dffc26cf47d7c1112c39cb
PREDECESSOR_PR=229
PREDECESSOR_ISSUE93_RECEIPT=6537004391
FROZEN_EVALUATOR_FIRST_COMMIT=0e2b10051e92eee000b15efd91fb9262bcbc66ee
CANDIDATE_SECOND_COMMIT=051a1d6f28e51bd72aae9a8b7d6b15ca7b690562
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read the immutable main commit, AGENTS.md, GOVERNANCE.md, Alpha-Node adaptation contract, direct-publication directive, task-anchor norm, repository order, research/pipeline README, Issue #93 and R10 PR #115 through the connected owner GitHub API. Current Issue #93 snapshot: **219/219 GitHub comments authored by owner `nexusomegac27`**, last ID `6537004391`; R10 PR #115 is OPEN/UNMERGED, with zero PR conversation comments and zero submitted reviews. The R10 detached source manifest was physically retrievable at original head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`, 4,588 UTF-8 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. Its previously reported SHA-256 is not independently recalculated in this iteration. External write-slot register blob `1fabcab7f556e83621a3676ddfb3d11cdd964b55` declares `external_actor_allowlist=[]`. API metadata is not an independently authenticated expert identity.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

H0: A comment body claiming `INDEPENDENT_RECEIVER_ACK=MATCH` or a complete-looking handshake can be misclassified as an independently authenticated expert return even when the GitHub author is the owner or an unregistered actor. A GitHub user login is not the identity of an expert model, and a return candidate is not a byte-verified ACK.

Before: the observed 219 comments were checked for author origin in prior readbacks, but no pinned, isolated, deterministic actor-gate test existed in this iteration's test lane. After: **219/219 current comments machine-classified in one bounded read-only pass**; **0/219 independently authenticated receiver ACKs established**, matching the source metadata. This is a reproducibility/guard improvement, **not** an improvement in expert-return delivery rate.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The independent black-box oracle was committed first and then left unchanged. It invokes the JS candidate in a **separate Node.js subprocess** and checks exit status, machine-readable output, and stderr. The candidate was committed later. The actual GitHub file blobs matched separately computed local Git blob IDs.

- Frozen oracle: `frozen_alpha_issue93_actor_gate_oracle_v1_20261031.js`; 3,079 UTF-8 bytes; SHA-256 `aa6d16124981f72f9aef638611b76c3ddda8f225bc13628e5f59dbcd0b1473d0`; Git blob `eab641a452574002fc7a3ce10619a7050ac77508`.
- Candidate: `alpha_issue93_actor_provenance_gate_v1_20261031.js`; 3,444 UTF-8 bytes; SHA-256 `efb132f95e7b1e7fa5062e762a964835ecf3f59925313779acf6b5ee627e5a90`; Git blob `71c06ae01a0d8f4e7f4238413d78a82cd980c44b`.
- Local independent black-box evaluation: **21/21 PASS**, including **8/8 fail-closed invalid-input/duplicate-ID cases**, eight malformed handshake cases denied independent ACK, owner-spoof control, unregistered-actor control, registered-actor candidate with source bytes explicitly unverified, and empty/mixed census controls.
- Real GitHub API metadata test: **219/219 classified as `OWNER_AUTHORED_NOT_INDEPENDENT_RECEIVER`**, 0 non-owner comments, 0 established independent ACK, 0 source bytes validated by this classifier. This test used the actual fetched candidate JS from the pinned branch and the actual fetched GitHub comment metadata.

The classifier deliberately **never** returns an independent receiver ACK. A registered actor with syntactically complete handshake is only `REGISTERED_ACTOR_RETURN_CANDIDATE_BYTES_UNVERIFIED`, pending separate physical byte/hash, actor scope, privacy, scientific and authority checks. It does not query external systems, change permissions or merge R10.

**FALSIFIER:** an owner-authored forged ACK or an unregistered actor yields an independent ACK; duplicate comment IDs or malformed records are silently accepted; or a registered actor's unverified manifest is promoted to byte-verified/scientifically adjudicated. Any such result disproves the scoped guard claim.

## DECISION / GOAL METRICS

`TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE`. No new pipeline root, evaluator self-approval, productive integration, external actor registration, R10 merge, Hostinger/WWW write, Cursor dispatch, runtime change, or claim promotion. GitHub PR/CI, main and append-only Issue #93 publication receipt require separate actual readback after publication.

Project-wide `AUTOMATION_RATE=NOT_COMPUTABLE` and `FULL_READBACK_RATE=NOT_COMPUTABLE`: the complete authenticated denominator of eligible routine handoff attempts and all publications, including failures, is not present. The 219 comments are **not** the handoff denominator. The isolated tests are not operational handoff successes.

`PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`.

Reproduce on a checkout with Node.js:

```bash
node research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_issue93_actor_gate_oracle_v1_20261031.js research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_actor_provenance_gate_v1_20261031.js
```
