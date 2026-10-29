# AXIOM Alpha-Node — root-path symlink provenance preflight V3 · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_ROOT_PATH_SYMLINK_PREFLIGHT_V3_20261029_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = cc6cae5a81667c5fbb1b1bddb5013b2c6c337af7  
MAIN_PREDECESSOR = 2b3e27383d7d86e9742af00d39e8c6e2e70c59f1  
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/200  
PREDECESSOR_ISSUE93_RECEIPT = 6506861787  
FROZEN_EVALUATOR_FIRST_COMMIT = 2e07b7aa63922d9288e2a4850f636a3d6e8f30d7  
CANDIDATE_SECOND_COMMIT = 12416ef15312ce15daacef0979a3f00526700cfc  
PRODUCTION_INTEGRATION = NO  
WWW_PARITY = NOT_ESTABLISHED

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

GitHub returned `main=cc6cae5a81667c5fbb1b1bddb5013b2c6c337af7`, with one additive three-file commit after `2b3e27383d7d86e9742af00d39e8c6e2e70c59f1`; Issue #93 returned 190 comments and last receipt `6506861787`. The previous V2 source at the pinned main was fetched as 4,397 UTF-8 bytes, SHA-256 `e224c42beced1c23748f241532b467b4a8ef9ef097e69c95d74e67a667748312`, Git blob `c3d451b9eb59dc5f45d8299602d2ea145aeca216`. The local reconstruction independently matched that SHA-256 and Git blob. Governance, the R16 adaptation contract, root placement policy, pipeline README and external write-slot registry were read. Owner GitHub identity was `nexusomegac27`; external actor allowlist was empty.

## NEGATIVE_HYPOTHESIS / FALSIFIER

V2 rejects a symlink at each expected leaf filename, but `Path(root).is_dir()` follows a symlinked **root** or **ancestor** directory. With a synthetic real directory containing byte-exact expected files, V2 returned `MATCH` even when the supplied root path traversed a symlink. This is a path-provenance ambiguity, not a demonstrated SHA-256 collision, a GitHub compromise or an unauthorized data disclosure.

Falsifier: if V3 still returns `MATCH` for either a symlinked root or a symlinked ancestor in the same fixture, or rejects an ordinary physical directory, the proposed fix fails. The frozen evaluator also tests a same-size byte mutation, a missing file, a leaf symlink, unsafe names, an empty manifest, unchanged pinned inventory/claim ceiling, and a POSIX FIFO. Any failed test rejects the candidate.

## PINNED_BASELINE / ISOLATED_CANDIDATE / INDEPENDENT_TEST

- V2 original: 4,397 bytes, SHA-256 `e224c42beced1c23748f241532b467b4a8ef9ef097e69c95d74e67a667748312`, Git blob `c3d451b9eb59dc5f45d8299602d2ea145aeca216`.
- Frozen independent evaluator, committed **before** V3: `frozen_issue93_root_path_symlink_oracle_v1_20261029.py`, 5,032 bytes, SHA-256 `a72e5548a76b893af381e30e0324b95562266d3804ff1670cb418dcdf1f7cb4a`, Git blob `7f643e8d4b02ec85c19b6a84b364b055446a6bb6`.
- Additive V3: `alpha_issue93_v7_dependency_fixity_preflight_v3_20261029.py`, 4,749 bytes, SHA-256 `6b23c4daa11232fe62e9749c9f91b0b9aae5b0f5ba0acf94b217b23892c7b6e4`, Git blob `50b55aef69b20835c275d978989044c953c5fd6d`.
- V3 uses `Path(root).absolute()` without resolving symlinks, rejects a symlink at root or any ancestor, and retains the existing leaf `O_NOFOLLOW`, `O_NONBLOCK`, `fstat`, length and SHA-256 checks. Existing V1/V2 source files and frozen oracles are unchanged.
- Command: `python frozen_issue93_root_path_symlink_oracle_v1_20261029.py -v` in the existing R16 research directory. Local isolated POSIX Linux result: **10/10 PASS**, including two differential symlink fixtures and the positive control.

| Observable fixture | V2 before | V3 after |
|---|---|---|
| Byte-exact file under symlinked root | `MATCH` (incorrect path acceptance) | `SYMLINK_ROOT_REJECTED` |
| Byte-exact file under symlinked ancestor | `MATCH` (incorrect path acceptance) | `SYMLINK_ROOT_REJECTED` |
| Ordinary real directory | `MATCH` | `MATCH` |
| Same-size byte mutation | `SHA256_MISMATCH` | `SHA256_MISMATCH` |
| POSIX FIFO | `NONREGULAR_FILE` | `NONREGULAR_FILE` |

This is a synthetic path-fixity hardening test, **not** a race-free directory capability. Symlink replacement races, hardlinks, and GitHub checkout authentication are outside the test. Legitimate symlinked workspace roots will be rejected by design; compatibility impact is not assessed. No production integration, complete real-checkout CLI test, Windows validation, external third-party evaluation, runtime change, or WWW publication was performed.

## R10 PASSIVE AUXILIARY READBACK

PR #115 remained open with 0 discussion comments, 0 reviews, 0 review threads. The originally pinned immutable commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` is an ancestor of the current PR head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` (GitHub compare: 9 ahead, 0 behind). Nine additive files include owner-uploaded historical expert-labelled reports and a receive-ACK assertion; they do **not** establish an authenticated independent GitHub actor, a new expert receipt in this check, or independently executed expert research. The detached original manifest at the pinned commit remains 4,588 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. R10 remains `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.

## DECISION / TARGET METRICS

This candidate improves two explicitly tested path-fixity negative fixtures, but does not change the measured project-wide automation rate. The previously scoped PR #184–#199 receipt census reported 15/15 metadata matches, not a complete handoff denominator. Eligible public handoff attempts, failures, and full source/test readback population remain unknown: `AUTOMATION_RATE=NOT_COMPUTABLE`, `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. The local test covers 10/10 synthetic fixtures, not 100% of runtime scenarios. No unauthorized writes, secret disclosures, source overwrites, actor self-registration, model-weight changes, claim promotion or Hostinger writes were performed in this iteration.

`BLOCKED_LANE != BLOCKED_SYSTEM`  
`DRIFT_RESET = NON_DESTRUCTIVE`  
`CLAIM_CEILING = C1_DESCRIPTIVE_ONLY`
