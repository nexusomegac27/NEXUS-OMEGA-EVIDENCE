# AXIOM Alpha-Node · C1 handoff byte-binding falsification (isolated research)

OBJECT = NEXUS_OMEGA_ALPHA_HANDOFF_BYTE_BOUND_RECEIPT_FALSIFICATION_20261020_R0
PREDECESSOR = NEXUS_OMEGA_ALPHA_HANDOFF_SAFETY_FLAGS_RECEIPT_20261020_R0
SOURCE_MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = TESTED_IMPROVEMENT_ISOLATED_C1
INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## Question and negative hypothesis

Can a metadata-only handoff reducer count a complete publication without any independently checked original source bytes? Yes: a synthetic observation with all boolean readback flags set to true produces a metadata-only 1/1 success, even when no GitHub source bytes, test bytes, or Issue #93 receipt bytes are available. The flags alone are assertions, not verified transport evidence.

## Candidate and independent test

The isolated additive candidate `alpha_handoff_byte_binding_v3.py` preserves the V2 metadata reducer and introduces `measure_bound(records, proofs, observed_main_sha)`. It independently recomputes SHA-256, Git blob SHA-1 with the canonical `blob <size>\\0` prefix, exact source byte count, test digest, JSON receipt binding, and commit identity. Missing or divergent proof is flagged rather than counted as byte-bound.

Frozen evaluator `frozen_evaluator_handoff_byte_binding_v1.py` was established before candidate implementation and is unchanged. Synthetic baseline (V2) 0/16 because the new entry point does not exist; candidate 16/16; historical independent regression suites 14/14 and 18/18; a source-digest-bypass mutant fails 1 of 16 as expected. These are local, isolated Python tests, **not** GitHub authentication, external validation, or deployed runtime evidence.

Candidate original local bytes: 9,420; SHA-256 `b9c13303b740a2862395b3b16d485c331f0539c52c3fc7b55a122926a926682e`.
Frozen evaluator original local bytes: 4,300; SHA-256 `9d6e24398707e3378a7302c3affb4aef2f4636f22b3ae26a0bce3d2dba3bacd9`.
These local source files are **not** represented as GitHub-published files by this report.

## Falsifiers and limitations

Falsify the candidate if a tampered source, forged digest, forged Git blob ID, mismatched commit, duplicate JSON receipt key, missing Issue ID, or missing proof is counted as byte-bound; or if prior denominator/safety suites regress. This local proof checker does **not** authenticate a GitHub actor, GitHub API response, branch rules, independent scientific expert, or actual main publication. Accordingly `project_handoff_numerator` and `project_handoff_rate` remain null even for a synthetic locally valid proof. The project-wide eligible denominator is not established.

## Governance

Owner-directed public-safe C1 research only, under existing R16 lane. No historical file modification, new pipeline, external write-slot registration, evaluator rewrite, merge permission, Hostinger change, runtime update, or claim promotion. Original authority: `AGENTS.md`, `GOVERNANCE.md`, `docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md`, and `research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_NODE_C1_CONTINUOUS_SELF_MODIFICATION_R0.md` at pinned main.

This report is a research candidate and cannot serve as its own independent receipt. Only an actual immutable GitHub commit/file readback can establish its publication; Issue #93 ACK and main merge must be checked separately.
