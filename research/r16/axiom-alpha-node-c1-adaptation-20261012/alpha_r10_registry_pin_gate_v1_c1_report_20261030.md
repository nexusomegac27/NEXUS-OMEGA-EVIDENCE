# AXIOM Alpha-Node — R10 pinned-registry provenance gate V1 (C1, 2026-10-30)

OBJECT: NEXUS_OMEGA_ALPHA_R10_PINNED_REGISTRY_GATE_V1_20261030_R0
DECISION: TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING: C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE: a04d9874f19a04101d8e106809c6b0f6d58feb0b
PREDECESSOR_PR: 214
PREDECESSOR_ISSUE93_RECEIPT: 6519349549
R10_PR115_MERGE_AUTHORITY: NONE
PRODUCTION_INTEGRATION: NO

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

GitHub API main was read as a04d9874f19a04101d8e106809c6b0f6d58feb0b. The immutable R10 detached manifest at 539d4bb33d2ba2c4895713c1bc437ece0743eeea was fetched as 4,588 UTF-8 bytes, Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df; a separate JavaScript SHA-256 implementation, checked against the abc vector, returned 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc (MATCH).

The current actor registry at pinned main path docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json was fetched as 2,178 UTF-8 bytes, Git blob 1fabcab7f556e83621a3676ddfb3d11cdd964b55, independently computed SHA-256 d257be3faef8336e30f688d440758b051d93dd2a29ece693882af4ed8e463e7c; default is DENY, owner is nexusomegac27 and external_actor_allowlist is empty. This pin is a baseline, not authority to edit the registry.

R10 PR #115 remains OPEN, unmerged, head dab7c59070d67e7e2a244bd6d05db9a4d37460e3, with zero PR discussion comments, zero reviews and zero review threads at this cutoff. The later owner-mediated ACK assertion has source path research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt, Git blob 4e31f92be1f673f49a2c27e570b5849e754cca78, 4,380 bytes, previously reported SHA-256 60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5. No new independent expert return was established.

## NEGATIVE_HYPOTHESIS / BASELINE

The predecessor alpha_r10_ack_provenance_preflight_v1_20261030.py accepts external_actor_allowlist and source-rehash booleans from the same caller-supplied claim object. Its frozen synthetic positive controls can report ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION if a caller supplies a hypothetical external actor and matching hypothetical allowlist. This is a limited eligibility classification, not a demonstrated production bypass or authenticated ACK.

Falsifier: an untrusted claim must not supply or modify the authoritative actor allowlist without detection. The current pinned empty registry must prevent external-review eligibility even when a claim asserts an API actor. A separately pinned future registry may support review eligibility only, never an authenticated ACK or scientific adjudication.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

The new offline read-only candidate alpha_r10_registry_pin_gate_v1_20261030.py accepts two local JSON files and externally supplied immutable pins. It verifies the registry file's SHA-256 against the expected pin, enforces default=DENY, repo and owner identity, rejects caller-injected allowlist fields, checks the claim source identity against separate commit/SHA-256/bytes/blob pins, and rejects duplicate JSON keys, nonfinite JSON, malformed fields and ambiguous numeric types. Actor eligibility reads the allowlist only from the pinned registry file. The candidate writes no files.

The separate frozen subprocess evaluator frozen_alpha_r10_registry_pin_oracle_v1_20261030.py was committed first. Its local Python execution on the exact candidate bytes returned 20/20 PASS, including forged allowlist, unpinned registry edit, forged external actor, source mismatch, duplicate JSON keys, nonfinite JSON and a synthetic future allowlisted-actor positive control. The positive control returns ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY. All outputs retain independent_receiver_ack=NOT_ESTABLISHED, authenticated_github_actor=NOT_ESTABLISHED, scientific_adjudication=NOT_PERFORMED.

| Comparable synthetic measure | Previous preflight | New pinned-registry preflight |
| --- | --- | --- |
| Actor allowlist supplied inside claim | Accepted as input | Rejected as invalid claim field |
| Registry SHA-256 independently pinned | No | Required and checked |
| Claim source identity compared to external CLI pins | No | Yes |
| Actual external actor authentication | Not established | Not established |
| Separate subprocess evaluation | 16/16 in predecessor report | 20/20 locally in this iteration |

Local file bindings:
- Evaluator: 6,501 UTF-8 bytes, SHA-256 ea05d94b5a48d0158d6ecac338f2e88ed76af99a87925e7fce985fd36a5e6fb8.
- Candidate: 5,691 UTF-8 bytes, SHA-256 f057c6a2985ef989f8121ff68b56fc4f8783513ef7df7c3477ee4692fcb96cae.

Reproduce from this research directory: python frozen_alpha_r10_registry_pin_oracle_v1_20261030.py alpha_r10_registry_pin_gate_v1_20261030.py

The evaluator fixtures are synthetic. Actual registry bytes were independently read and hashed for the provenance pin, but the candidate was not run end-to-end against that actual registry in the local evaluator. CLI pins and caller-supplied actor_origin, source_bytes_rehashed and source_blob_rehashed flags are not independent GitHub authentication. This remains an isolated research candidate, not a production security control.

## DECISION / PUBLICATION BOUNDARIES

Only three additive files under existing research/r16/axiom-alpha-node-c1-adaptation-20261012/. Preserve all prior evidence and validators. No external actor registration, Task Anchor publication, PR #115 merge, R10 source mutation, CI-oracle change, new worker, Hostinger/WWW write, model modification or claim promotion. Project-wide handoff and publication-readback denominators remain unknown; 90% and 100% project goals are not established.

PR: PENDING_AT_REPORT_CREATION
ACTUAL_MAIN_READBACK: NOT_YET_PERFORMED
ISSUE93_APPEND_ONLY_RECEIPT: PENDING_AT_REPORT_CREATION
