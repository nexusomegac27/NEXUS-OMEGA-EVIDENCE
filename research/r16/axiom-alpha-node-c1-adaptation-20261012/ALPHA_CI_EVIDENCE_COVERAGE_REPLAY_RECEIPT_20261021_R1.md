# AXIOM Alpha-Node — PR #124 Public Replay Evidence Closure R1 (C1)

OBJECT = NEXUS_OMEGA_ALPHA_PR124_PUBLIC_REPLAY_EVIDENCE_CLOSURE_20261021_R1
PREDECESSOR = NEXUS_OMEGA_ALPHA_PR124_CI_EVIDENCE_COVERAGE_AUDIT_20261021_R0
PREDECESSOR_RECEIPT_SHA256 = 4677a143ab901b80eec461af44f34b65d33ff137426022a606074db0a58a3c81
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
PR_PARENT_HEAD = 5fb35be25870e3a8785f0b41a82bcba652b43088
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = TESTED_IMPROVEMENT_ISOLATED_C1_NOT_CI_NOT_MAIN

## Single candidate: public replayability of the existing CI-evidence guard

Before this append-only change, PR #124 contained 2/2 narrative reports but **0 runnable frozen evaluators and 0 runnable guard scripts**; successful generic CI could not reproduce the claimed CI-evidence-classification tests. This candidate publishes the *previously locally tested* read-only guard and separately frozen evaluator, together with one machine-readable local replay result. No historical file is overwritten; all additions remain in the existing research/r16/axiom-alpha-node-c1-adaptation-20261012/ directory.

Pinned source scripts (unchanged from isolated predecessor):
- Guard: 3066 bytes, SHA-256 `27e4ea850b63b234275e6a8b2bf89c87e47685bd8d8fc760f801a7f998f7ca9c`, Git blob `96b22aa303ebd5c16edcc5c8a8e29efb4b5fc7ee`.
- Frozen evaluator: 3706 bytes, SHA-256 `3911141a004ab407b829129e9e42999fead0994277573f098b34b7856885c324`, Git blob `0f622a973e17d4c7c63f08e220221492d82ba7fc`.

## Reproduce (offline, isolated, no production/API calls)

From the repository root:

```bash
python research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_CI_EVIDENCE_COVERAGE_FROZEN_EVALUATOR_V1_20261021.py research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_CI_EVIDENCE_COVERAGE_GUARD_V1_20261021.py
```

This evaluator synthesizes its 20 fixtures and executes the guard in temporary directories. In an isolated subprocess rerun on 2026-10-21, unchanged candidate + unchanged frozen evaluator returned 20/20 correct classifications, exit 0 (1 positive, 19 negative). A deliberate mutation that bypasses the same-head named replay CI requirement returned 17/20, failing three expected negative cases: missing/stale/failed replay CI. The independent oracle is a separately fixed script, **not an authenticated third-party scientific validation**.

Before/after measurable public artifact completeness (subject to immutable GitHub readback): runnable scripts 0/2 -> 2/2; machine-readable local result 0/1 -> 1/1. These are public *replayability* metrics, not automation handoff success, and no claim is made that GitHub Actions actually executed this evaluator.

## Negative hypothesis and falsifier

Negative hypothesis: ordinary green CI is insufficient to establish execution of the frozen evaluator at the same immutable PR head. Falsifier: the guard accepts absent/mismatched evaluator, fixture or result evidence, a stale/failed/missing dedicated replay check, or rejects a complete structurally valid positive case. The supplied synthetic fixture suite checks these classes. The guard checks supplied metadata structure only; it does not authenticate GitHub API responses or independently fetch raw source bytes.

## Decision and hard boundaries

PUBLIC_BRANCH_REPLAYABLE_CANDIDATE if and only if all added bytes and Git blobs are independently read back at the actual new branch commit. `alpha-evidence-replay` is **not** an installed/observed CI job; no new workflow, privileged worker, runtime, Hostinger action, merge, external actor, biological experiment, or claim promotion. PR remains DRAFT until independent gates and actual operator governance are satisfied. GitHub main remains separate. Eligible project-wide handoff denominator UNKNOWN, no 90% attainment claim, GitHub->WWW parity NOT_ESTABLISHED.

R10 passive observation (not a second candidate): PR #115 contains owner-published `returns_20261016/` reports including a text asserting `EXTERNAL_RECEIVE_ACK`; its own terminal source register labels that asset `EXPERT_ASSERTED_ACK_UNAUTHENTICATED`. Owner-mediated source bytes are not a registered external GitHub actor, independent receive ACK, or proven biological research execution. Issue #93 has no new independent external comment at this observation.
