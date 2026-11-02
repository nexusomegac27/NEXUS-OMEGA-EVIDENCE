# NEXUS OMEGA · AXIOM Alpha-Node · Bounded publication readback census 274–283 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_COHORT_CENSUS_274_283_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_BOUNDED_PROVENANCE_CENSUS_NOT_PROJECT_WIDE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=7961026bf0f630aee160e083122c2900744d2da1
PREDECESSOR_PR=283
PREDECESSOR_ISSUE93_RECEIPT=6567407508
FROZEN_EVALUATOR_FIRST_COMMIT=4fab92dfe8ce98e3d6e690fb6072b16d4c5c3764
FROZEN_EVALUATOR_GIT_BLOB=3a046d603991e369319cdf7d0305d3b2f3329f8e
FROZEN_EVALUATOR_BYTES=4662
FROZEN_EVALUATOR_SHA256=f4cdd6da100891164a734dd81ef2873f4726c33fc28cfeb77cbfa305733d05e3
MANIFEST_CANDIDATE_COMMIT=03e6b1bef18a00ea6f8a3d5503d0d945b9892bb1
SOURCE_SHARDS=34623f297e6a6234dcddec598aa455b060c8ac8f;3cd6dcc60f42c8fddafb21e5226cadf24a1faf4c;87894644cda8c26ff45ac8b9c0b6a62993bcb485
WORKFLOW_READBACK_COMMIT=6b000f5c8c8c138ea1530635855be1f947b0edc7
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PINNED_BASELINE

The preceding per-iteration Issue #93 receipts repeatedly stated **1/1 publication readback** without an independently consolidated cross-run denominator. That is not a project-wide rate. This iteration defines a **deliberately bounded, non-exhaustive** cohort: merged PRs #274 through #283, ten consecutive merge commits from `964fe47c4bdbad599e0689b132ff73c0822f3518` to `7961026bf0f630aee160e083122c2900744d2da1`. Each adjacent GitHub compare returned **ahead=1, behind=0**. All ten PRs were observed merged. The last main ref was read as the latter SHA.

The readback retrieved each of the 36 changed text files from immutable `main` at that SHA using GitHub's Contents API in base64 form, decoded the returned bytes, recomputed SHA-256 and Git blob SHA-1 independently, and compared the Git blob against the API's blob ID. **36/36 file-byte comparisons matched; 153,329 source bytes total.** The full per-file paths, byte lengths, SHA-256 and blob IDs are in the canonical JSON census, with three append-only source shard records.

The ten exact Issue #93 owner receipt IDs are: `6561672055`, `6562253845`, `6562668295`, `6563701606`, `6564141672`, `6564862176`, `6565584811`, `6566413038`, `6567269097`, `6567407508`. Each was retrieved and contained the corresponding merge commit. They are **owner-authored receipt evidence**, not an independent external actor or scientific ACK.

For the ten PR head SHAs, GitHub returned five completed-successful PR-triggered workflow runs each: **50/50 observed successful workflow runs**, with run IDs and names in `alpha_publication_census_workflow_274_283_20261102.json`. This API exposes only a first-page workflow subset and does not prove that the full GitHub Checks/Semgrep inventory was retrieved.

## NEGATIVE HYPOTHESIS / ONE CANDIDATE / METRICS

Hypothesis: aggregating the last ten published C1 scaffolds may reveal a missing source, noncontiguous merge, absent receipt, or failing workflow even when individual receipts claim 1/1. The one candidate is a versioned **bounded publication-census scaffold**, not a new scheduler, worker, pipeline, or productive validator.

| Metric | Before this iteration | Observed after |
|---|---|---|
| Independently consolidated cross-run source-byte cohort | Not established | 10 PRs; 36/36 files; 153,329 bytes |
| Contiguous immutable commit chain | Not consolidated | 10/10 adjacent comparisons ahead=1/behind=0 |
| Owner Issue #93 receipts bound to merge SHAs | Not consolidated | 10/10 found |
| PR-triggered workflow subset | Not consolidated | 50/50 completed-successful |
| Full GitHub Checks/Semgrep readback | NOT_COMPUTABLE | NOT_COMPUTABLE |
| Project-wide eligible handoff automation numerator/denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |
| Project-wide complete publication readback numerator/denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

## FROZEN EVALUATOR / INDEPENDENT TEST / FALSIFIER

The frozen structural Python evaluator was created **before** the source-census candidate, and its original 4,662 bytes were independently rehashed locally; SHA-256 and Git blob matched the GitHub file. Executed Python selftest: **10/10 PASS**, including missing PR, missing file, duplicate receipt, broken chain, false byte-check flag, blob mismatch, C2 promotion, scope swap and last-main mismatch. A **separate JS structural evaluator** fetched the actual candidate manifest from the GitHub branch and obtained **11/11 PASS** (one positive, ten adversarial mutations, including duplicate path). The Python frozen evaluator was **not** executed against the full actual manifest; this distinction is preserved. The original file-by-file SHA-256 and Git-blob checks were performed separately against the fetched original bytes.

Falsifier/limitation: a jointly forged API response and fabricated receipt metadata can remain internally consistent; this census does **not** authenticate an adversarial GitHub transport, verify independent external receiver identity, establish the full Checks/Semgrep census, or infer project-wide rates. The selected ten PRs are a convenience cohort, not a random sample and not all NEXUS handoffs. An omitted eligible event outside #274–283 would falsify any attempt to promote the cohort to the project-wide denominator. Negative fixtures test structural fail-closed behavior, not scientific correctness.

## DECISION / PUBLICATION BOUNDARY

Publish only as additive, public-safe C1 research in the existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` directory. Historical sources and validators are untouched. No new root, runtime, Hostinger, WWW, agent registration, R10 merge, biological experiment, credential, node reset, claim promotion, or new automation. GitHub PR/CI, actual main SHA and append-only Issue #93 receipt must be checked **after** publication; until then this is a tested C1 candidate, not `MAIN_PUBLISHED`.

R10 side-readback at immutable PR #115 head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`: detached manifest **4,588 bytes**, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; no independently authenticated expert return in the inspected PR discussion/reviews or 263 prior Issue #93 owner comments. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. No R10 write.
