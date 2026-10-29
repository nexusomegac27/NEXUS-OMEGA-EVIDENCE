# AXIOM Alpha-Node C1 — V1–V7 Issue #93 dependency-fixity preflight (2026-10-29)

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_V7_DEPENDENCY_FIXITY_PREFLIGHT_20261029_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=959cfe7e13db98735e4b3d7ec26d2d0ce7d5cbe7
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/196
PREDECESSOR_ISSUE93_RECEIPT=6500402037
FROZEN_ORACLE_FIRST_COMMIT=7d0279f5e4761b7bcca616f5d366608b2ed66c19
CANDIDATE_SECOND_COMMIT=e082caad82513df2855cd0eddd0c3258d28cdbb6
PRODUCTION_INTEGRATION=NO
R10_EXPERT_RETURN=SOURCE_NOT_PRESENT_IN_CHECKED_PR_INBOX
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / original source and authority

The latest physically read `main` at the start of this run was `959cfe7e13db98735e4b3d7ec26d2d0ce7d5cbe7`, parent `1a824816506b917bac5027291f47edb9ff228fc1`. Owner Issue #93 last receipt `6500402037` was read via the GitHub API. The R16 Alpha-Node rule, AGENTS.md, GOVERNANCE.md, direct-publication directive, task-anchor norm, repository order, research pipeline policy and empty external actor registry were checked. The connected actor was `nexusomegac27` with repository write permission. No external actor registration or runtime authority was inferred.

The current V7 Issue-#93 receipt parser dynamically imports V5, which imports earlier parser modules. Source code dependency bytes are not intrinsically authenticated by that import. The new preflight is **read-only** and never executes or imports any of those source modules; it verifies a separately pinned inventory before any optional later parser use. It is a research scaffold, not an installed execution gate.

At immutable `main`, the seven V1–V7 source files under `research/r16/axiom-alpha-node-c1-adaptation-20261012/` were independently fetched and SHA-256 hashed by a separate JavaScript SHA-256 implementation (standard `abc` and empty-string reference vectors passed). All **7/7** SHA-256 values matched the earlier owner receipts; aggregate source bytes: **24,528**. Git blob identities were recorded separately from GitHub API responses, not independently recomputed as Git SHA-1 in this source census.

## NEGATIVE HYPOTHESIS / falsifier

A naive preflight that checks only whether all seven filenames exist can silently accept a same-byte-length mutation to a historical Python dependency. In a separate synthetic test, the existence-only baseline accepted the mutated file (1/1 false acceptance); the new digest-checking preflight rejected it (1/1 correct rejection). This is a **synthetic falsification** of an existence-only baseline, not an observed compromise of the public repository.

Falsifier: a same-size one-byte mutation, a missing or truncated dependency, a symlink, a forged expected digest, or an unsafe manifest filename must never return `MATCH`. A valid, exactly matching synthetic inventory must return `MATCH`. A future actual GitHub source mismatch or a failure of the independent frozen oracle invalidates the candidate's scoped acceptance.

## PINNED BASELINE / isolated candidate / independent evaluator

- Baseline: the existing V7 parser has no standalone pre-execution dependency SHA-256 gate. The project-wide automation and readback rates remain `NOT_COMPUTABLE` because the complete authenticated handoff population and failed attempts are not available.
- Frozen evaluator **committed first**, before the candidate: `frozen_issue93_v7_dependency_fixity_oracle_v1_20261029.py`, **4,938 bytes**, SHA-256 `249e51a98d810bf5ddc37f0b9de22195706c9591ae20ad6eb64c678f3c47023b`, Git blob `9534bc535643b73c732644177236db24b3f6a313`.
- Candidate **committed second**: `alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py`, **4,194 bytes**, SHA-256 `0fb4f5408d4c61d3a2e4c9bd160cc63afe68b077febbdd288e757b0fb324af23`, Git blob `80ed3eee7bf66c8076ce4f06c1eac5e9904ded48`.
- Local isolated execution: `python frozen_issue93_v7_dependency_fixity_oracle_v1_20261029.py -v` → **15/15 PASS**, including positive synthetic inventory, same-size mutation, missing/truncated files, symlink, path traversal, invalid manifest, and a fail-closed CLI on a directory lacking the actual seven sources.
- The evaluator is a separate versioned file, committed before the candidate; it imports the candidate function for testing but does not let candidate code rewrite the evaluator. Both were authored in this AXIOM iteration. **External third-party validation: NOT_ESTABLISHED.**
- The actual seven GitHub source files were independently SHA-256 checked via the GitHub API in this run, but the new Python preflight CLI was **not** executed against a local clone of those seven files. Its end-to-end real-source behavior remains `NOT_EXECUTED`.

## DECISION / scope and exclusions

This isolated, additive preflight improves the ability to detect source substitution in a seven-file historical dependency chain. It does **not** authenticate GitHub actors, receipts, scientific findings, or project-wide handoffs. It does not eliminate all filesystem time-of-check/time-of-use races, is not a sandbox against malicious code, and does not run or modify the parser. The pinned manifest must be updated only through a separately verified append-only successor if a legitimate dependency changes.

No production integration, external worker, R10 expert dispatch, runtime or Hostinger write, WWW parity claim, source overwrite, governance change, evaluator self-approval, or claim promotion. `BLOCKED_LANE != BLOCKED_SYSTEM`; `DRIFT_RESET=NON_DESTRUCTIVE`; `C1_DESCRIPTIVE_ONLY`.
