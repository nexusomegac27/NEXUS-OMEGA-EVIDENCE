# AXIOM Alpha-Node — bounded cohort middle-edge anchor V3 · 2026-11-02 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_COHORT_MIDDLE_EDGE_ANCHOR_V3_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PREDECESSOR_PR=285
PREDECESSOR_MAIN=ccfd6c4168f989bc372fe87227fd9218a77da6ff
PREDECESSOR_ISSUE93_RECEIPT=6569227849
FROZEN_EVALUATOR_FIRST_COMMIT=4c183b4569cbb1ef4e38685148f7dd7c97985703
CANDIDATE_SECOND_COMMIT=211d1de26c5499fbe685472805c4beb9b347c872
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## Authority, scope and original provenance

The Operator's standing C1 direct-publication rule, `AGENTS.md`, `GOVERNANCE.md`, Task Anchor Norm V1, Repository Order Law V1 and the R16 Alpha-Node adaptation contract govern this isolated, append-only research. No new directory, worker, evaluator replacement, branch-protection override or source rewrite.

Source manifest: `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_cohort_census_274_283_20261102.json` at immutable main `ccfd6c4168f989bc372fe87227fd9218a77da6ff`; Git blob `2f4dbfa8b05a073d5fd939b5fc779a2734f65fdd`, 19,301 ASCII/UTF-8 bytes observed via GitHub Contents read. The historical 36/36 source-byte checks belong to the preceding cohort report, not a newly repeated 36-file rehash.

Baseline original V1 evaluator: 4,662 bytes, SHA-256 `f4cdd6da100891164a734dd81ef2873f4726c33fc28cfeb77cbfa305733d05e3`, Git blob `3a046d603991e369319cdf7d0305d3b2f3329f8e`. Baseline V2 guard: 1,216 bytes, SHA-256 `3ec701e63d61fcb09b387bad02f65f8f62aeeb220ffe97c5663f06bdfcc2df48`, Git blob `cebce85f00598c97251e01017f6eb3360f12a22e`. Both originals were reconstructed locally with matching byte size, SHA-256 and Git blob, not inferred from chat.

The ten PR #274–283 parent-to-merge pairs were read separately via GitHub compare API against pinned commit IDs; each returned `ahead_by=1`, `behind_by=0`, with expected file count (5,5,5,3,3,3,3,3,3,3). This is a provider-scoped history check, not an external signature or authenticity proof.

## Negative hypothesis and frozen independent oracle

**Hypothesis:** V2 binds the first PR boundary and final main, but permits an attacker to change one intermediate `merge_commit` together with the next `parent_commit` while keeping the internal chain coherent. Such an altered manifest can falsely pass V2.

Before candidate creation, the frozen V3 evaluator was committed as `4c183b4569cbb1ef4e38685148f7dd7c97985703`. It contains an independent expected merge chain derived from the ten pinned GitHub compare reads, a positive fixture, eight co-forged middle-edge negatives, four prior regression negatives, and one deliberately accepted residual falsifier. The candidate did not edit this oracle.

- Frozen evaluator: 3,185 bytes; SHA-256 `4c886dc65a476e8149b0067bb3e1d1d670150cecbea955fae323828912b48349`; Git blob `68f12e61c6cd6508bc11360923dd8c1e8aaaa5d7`.
- V3 candidate: 1,553 bytes; SHA-256 `f166a82bfbb9c27e67f92850014ab9fa0d754834357a93063dd26a6d883533ef`; Git blob `1ffc190d0b49bc11b38baf27aefb3f3a8ea16d13`.
- The independent test oracle imports the frozen V1 and V2 predecessors; V3 imports V2 only. No production code, governance, CI or runtime is changed.

## Executed evidence and measurable delta

Local Python 3 subprocess replay using exact byte-matched V1/V2 modules and the previously committed V3 oracle:

| Metric | V2 baseline | V3 candidate |
|---|---:|---:|
| Frozen oracle expected outcomes | 14/14 PASS | 14/14 PASS |
| Co-forged middle-edge fixtures rejected | 0/8 | **8/8** |
| Positive fixture accepted | 1/1 | **1/1** |
| Four prior regression negatives rejected | 4/4 | **4/4** |
| Deliberate source/hash co-forgery still accepted | 1/1 | **1/1** |

Baseline stdout: 1,744 bytes, SHA-256 `ae965e17dd6b7f001117d971740121480513b3f3e60b2f1267c80b740b5a947d`.
Candidate stdout: 1,667 bytes, SHA-256 `b3e8704509528a7ad8c451e57335a005de9dc5f37b88690111b6c897367d0606`.

Separate JavaScript checker over the **actual fetched 19,301-character manifest**, independent of the Python V3 implementation: 1/1 real manifest accepted, 8/8 injected middle-edge co-forgeries rejected, 1/1 deliberate co-forged file hash still accepted (10/10 expected). This JS check does not constitute execution of the frozen Python oracle against the actual manifest; that exact cross-check remains `NOT_EXECUTED`.

**Falsifier:** Co-forging a file's SHA-256 and both Git blob fields remains accepted by the structural guard. An attacker who can change the trusted expected chain or the upstream provider data can also defeat this fixed-reference check. The candidate is therefore **not** proof of authentic GitHub history, independent expert identity, scientific correctness, or full real-event census.

## Reproduction and scientific decision

From a checkout containing the unchanged V1/V2 source modules and the two new V3 files:

```bash
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_cohort_middle_edge_evaluator_v3_20261102.py baseline
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_publication_cohort_middle_edge_evaluator_v3_20261102.py candidate
```

Run in the research directory or add it to `PYTHONPATH` so sibling imports resolve. No network calls are made by the candidate. No secrets or private data used.

This candidate repairs the documented V2 middle-chain false-acceptance class on the eight predeclared fixtures. It remains an **isolated C1 scaffold**, not an integrated validator or a claim about the 90% automation target.

Project-wide `AUTOMATION_RATE=NOT_COMPUTABLE` and `FULL_READBACK_RATE=NOT_COMPUTABLE`: authenticated global numerators and denominators are not established. The historical ten-PR cohort is explicitly bounded, not project-wide.

R10 is a separate read-only observation, not a second candidate: PR #115 open; original detached manifest still present; owner-mediated expert text and an asserted ACK exist, but no independently authenticated GitHub expert actor or scientific adjudication was established in this run. No R10 merge or write.

Publication is only complete after actual merged `main` readback and an append-only Issue #93 receipt. Until then, this document records a tested **branch candidate**, not a published main success.
