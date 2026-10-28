# NEXUS OMEGA · AXIOM Alpha-Node · postpublication readback witness · 2026-10-28 R0

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_STEWARD_POSTPUBLISH_READBACK_20261028_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PREDECESSOR_ISSUE93_RECEIPT=6462252014
PINNED_MAIN_BEFORE=ec66b61010212855a79297ec0673f84582dd8543
PRODUCTION_STEWARD_UNCHANGED_REQUIRED=YES
RUNTIME_HOSTINGER_WWW_WRITE=NO
```

## Source and provenance

- Original v3 research baseline: `research/r16/axiom-alpha-node-c1-adaptation-20261012/steward_output_postpublish_status_candidate_v3_20261028.py`, 4191 UTF-8 bytes, SHA-256 `847c3bd775b195f30617174904af6644ab1d13dd30725a9f44e40fe797423578`, Git blob `89d5df5726ed25756ca0550559eae268db3c1b36` on pinned main.
- Frozen independent evaluator, committed **before** candidate: `frozen_steward_postpublish_readback_evaluator_v4_20261028.py`, first branch commit `f3594ab3d57d53770b3ad0795ea9f499d6260db9`, 7225 bytes, SHA-256 `4d98704e9d15163ac0c54db99a0fde5241769e0188b97606a37af26bf650e084`, Git blob `fed4d0de9644835efc20880a4409ebf3a3ee49b6`.
- Isolated candidate: `steward_output_postpublish_readback_candidate_v4_20261028.py`, second branch commit `d12348d45a06885f0b501933a705e0ef17686d15`, 4770 bytes, SHA-256 `bc08d2b6ab1e12059418b6573192af2b1f7f1c0d381100d22d40d932a8cdafd2`, Git blob `03aa7ee31d56b5c91fc44e2635c96b3e15b9681d`.
- All three new files belong to the existing registered R16 Alpha-Node research lane. No root, schema, workflow, ruleset, external actor registry, historical path or productive Steward mutation is proposed.

## Negative hypothesis and falsifier

Hypothesis: a post-publication file-content mutation or same-byte path replacement between hard-link publication and completion of the directory `fsync` can escape the v3 guard as successful output. The frozen oracle injects both mutations at directory-`fsync` completion. It also includes normal, `fsync`-EIO, no-replace, checkout-write and parent-symlink controls. Falsify this research result if the original v3 rejects either synthetic mutation, if the candidate accepts either, or if ordinary positive controls regress. The evaluator is an independently versioned black-box subprocess oracle, **not an external third-party validation**.

## Executed bounded Linux/POSIX test

```bash
python frozen_steward_postpublish_readback_evaluator_v4_20261028.py \
  --baseline steward_output_postpublish_status_candidate_v3_20261028.py
python frozen_steward_postpublish_readback_evaluator_v4_20261028.py \
  --baseline steward_output_postpublish_status_candidate_v3_20261028.py \
  --candidate steward_output_postpublish_readback_candidate_v4_20261028.py
```

- Pinned baseline: **3/3 PASS**; two negative fixtures silently accepted (1 tampered content, 1 same-content inode swap); positive control PASS.
- Candidate: **18/18 PASS**, repeated in three separate executions (18/18 each). Injected tampering and same-content inode swap both produce explicit non-success errors; normal output and earlier fsync uncertainty behavior are preserved.
- Mutant A, suppressing post-success readback: **14/18 PASS**, four expected failures. Mutant B, disabling inode-identity comparison: **16/18 PASS**, two expected failures.
- During development, an initial candidate without a held source descriptor failed the swap fixture (16/18); POSIX inode reuse was an alternative explanation. The revised candidate retains a duplicate descriptor until readback, preventing immediate inode reuse for the source inode. This failed intermediate attempt is preserved here as negative evidence, not reclassified as a pass.
- Before/after targeted failure detection: **0/2 → 2/2**. This is synthetic fault-detection coverage, **not** a measured production defect rate or project handoff automation rate.

## Scope limits and disposition

The witness detects the two injected mutations at the observation instant; it does not prevent mutation, close every concurrent filesystem race, prove crash durability, establish cross-platform portability, or verify a real compromise. A successful readback is not an enduring integrity guarantee. Parent-path TOCTOU, external hardlink semantics, adversarial mount changes, and Windows/macOS behavior remain untested. The productive `scripts/nexus_repository_steward.py` is not changed or repaired. Do not promote to C2, integrate or deploy automatically.

Decision: `TESTED_IMPROVEMENT` limited to isolated C1 research. Public GitHub publication and any main/CI/receipt state are separate observable gates and must not be asserted by this pre-merge report. Project-wide eligible-handoff numerator/denominator remain `NOT_ESTABLISHED`; no 90%/100% target claim. R10 PR #115 is a subordinate read-only handshake with no newly authenticated independent expert return observed in this run; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. GitHub→WWW parity is not established.
