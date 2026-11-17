# R33 — Pinned Lean 4 Replay and CI / Oracle Blueprint (NOT ACTIVE)

OBJECT = NEXUS_OMEGA_AXIOM_R33_PINNED_LEAN_REPLAY_AND_CI_BLUEPRINT_20261117_R0
STATE = VERSION_PINNED_DESIGN_ONLY_NOT_EXECUTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TOOLCHAIN = leanprover/lean4:v4.36.0
ORIGINAL_LEAN = sources/NEXUS_R31_GREEN.lean
EXPECTED_ORIGINAL_BYTES = 7230
EXPECTED_ORIGINAL_SHA256 = 70820997285f1bb83d211afbc3cb18f3663790f399d4bce1c506dbd910e5be16
ORIGINAL_QWEN_LOG_SHA256 = 704e4097fde88ceccc266b90801aa2de920d0ef0470131de6094c1f11a719bf7
AXIOM_CLEAN_LEAN_COMPILER_RUN = NOT_PERFORMED
ACTIVE_CI_WORKFLOW_CREATED = NO
HOSTINGER_WRITE = NO
PR_MERGE = NO

## Offline isolated deterministic replay contract

Prep A — choose an operator-authorized disposable, isolated Linux runner or Windows/WSL VM. Only known upstream lean4 version v4.36.0, elan, built-in tools; no mathlib if unused. Verify toolchain package hashes/signatures and preserve evidence before executing any downloaded binary. No code from uploaded untrusted AutoClaw or unknown archive as shell commands.

Prep B — source exact check, before replay: independently rehash original Lean code and match expected full SHA. If mismatch => HOLD; do not patch original. Record provenance of uploaded workspace3 24/24 source manifest and commit/PR head.
Prep C — run pinned Lean and capture exact version, stdout/stderr, actual exit code and walltime as output artifacts. Do not reuse the Qwen previous 379B log as a fresh R33 run. The source already has seven #print axioms calls; compare output per theorem and flag sorryAx, arbitrary axioms, and any unexpected compiler-trusted native proofs.
Prep D — repeat at least once on a clean throwaway working directory from independently re-extracted source; compare hashes and theorem names. An independent trusted checker process must have an independently observed RUN ID, not merely the same original report.
Prep E — built-in leanchecker environment pass (when .olean + Lake module build configuration actually prepared). It is a second kernel replay, NOT independently implemented checker. Different checker or alternate formalization is a separate, optional confidence enhancement.
Prep F — independently derive the finite Bool/set evaluator from the theorem statements, independently test CX1/CX2/Q-CX4/Q-CX5, positive controls, and generate a proof-obligation map. This evaluator tests the specification mapping, not real network transport.
Prep G — new corrected specification only in a separate versioned source file; no overwriting Qwen historical original. Must keep every known counterexample RED against original assumptions and explicitly reject empty B, N=0, narrowed destination set, and authenticated-but-lying recipient. A purported theorem whose premises simply assume its conclusion is not useful evidence.
Prep H — empirical runtime refinement contract in a separately authorized lab: hash-bound intent, authenticated policy, per-target MATCH/MISMATCH/UNKNOWN witness, proper timestamp/source epoch, cache and 304 semantics, unauthorized effect negatives, old CF01-CF09. Formal PASS cannot skip this gate.

## Tooling and independent CI (only when separately authorized)

Recommended minimal local runner:
  elan toolchain install leanprover/lean4:v4.36.0
  lean --version
  sha256sum sources/NEXUS_R31_GREEN.lean
  lean sources/NEXUS_R31_GREEN.lean

If the first command installs from network, run it ONLY with operator-authorized egress or a verified offline cache. This blueprint does NOT execute these commands in ChatGPT or Hostinger and does not claim the external distribution digest is currently pinned in this document. Capture distribution hash on first verified installation.

For formal-only GitHub review CI, an authorized maintainer may later enable leanprover/lean-action pinned to a vetted immutable commit. The official lean-action supports axiom-audit and built-in leanchecker; choose explicit fail-on-test-not-run rather than auto-config skips. This new PR deliberately does not create any .github/workflows file to avoid changing CI behavior just by creating a source draft.

Prevent circularity:
- Empty runner results, green lint without building, reviewer-reported screenshots or .sha256 sidecars alone cannot set AXIOM_LEAN_REPLAY=PASS.
- Non-proof statements from qwen textual report are not Lean kernel-verified; physical validity and real-world HTTP delivery always require independent trace evidence.
- An unrelated Lean theorem from another problem, including Yang-Mills, cannot be imported as evidence for our outbox/witness unless an actual checked correspondence is supplied.

## Narrow terminal result machine fields

G0_ORIGINAL_HASH, G1_PINNED_TOOLCHAIN_ID, G2_INDEPENDENT_RUN_EXIT_CODE, G3_THEOREM_AND_AXIOM_LIST, G4_INDEPENDENT_SECOND_REPLAY, G5_COUNTEREXAMPLE_BINDINGS, G6_MODEL_TO_RUNTIME_CORRESPONDENCE, G7_PRIVATE_DATA_AND_AIRGAP, G8_NO_PRODUCTION_ACTION.
Each field MUST have status PASS/FAIL/NOT_RUN/NOT_APPLICABLE with supporting exact raw proof bytes/logs and actual tester domain. G2 PASS with G6 NOT_RUN gives only SCOPED_FORMAL_PASS, no production promotion.

NEXT = OPERATOR_EXPLICIT_SCOPED_OFFLINE_REPLAY_ORDER_OR_HOLD
