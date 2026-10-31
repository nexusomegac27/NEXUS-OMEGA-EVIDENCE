# AXIOM Alpha-Node — four-hop R16 source Git-tree OID closure (2026-10-31)

```text
OBJECT=NEXUS_OMEGA_ALPHA_R16_SOURCE_GIT_TREE_OID_CLOSURE_V1_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=1abc0f06dd43553113c0eb1f3099e5e39cfb2879
PREDECESSOR_MAIN=209ae5f11c0bda7c4b5336fe51cb19c683758299
PREDECESSOR_PR=227
PREDECESSOR_ISSUE93_RECEIPT=6535556174
FROZEN_ORACLE_FIRST_COMMIT=24e1326fa4205d61b96a85816819b0310f6d6bf2
ISOLATED_CANDIDATE_SECOND_COMMIT=e260e5e1a7a75b823bffd3bb11634ab943624365
REAL_API_PROJECTION_THIRD_COMMIT=89ed47f638b494a20f7f0a009ac56a010707857e
SOURCE_COMMIT=167cd7672f701bf27b67f147568ce9cee00a2d59
SOURCE_ROOT_TREE=60b0fddfe38708d4de486e0355ff684e8eb12b98
SOURCE_LEAF_BLOB=73ef222f9117f566930390e60899d571ecc77402
SOURCE_PATH=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read the current immutable GitHub main, original repository governance, the latest Issue #93 append-only receipt, and the R10 PR/inbox channels. The preceding V2 trusted-pin report explicitly labeled commit-tree membership `API_PROJECTION_MATCH_NOT_CRYPTOGRAPHICALLY_RECONSTRUCTED`. Its independent pin was API-derived, not an authenticated root of trust. That narrower caveat is preserved.

The source at immutable commit `167cd7672f701bf27b67f147568ce9cee00a2d59` was read through the GitHub connector: **1,452 UTF-8 bytes** and Git blob `73ef222f9117f566930390e60899d571ecc77402`. The existing pinned SHA-256 is `425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3` (pin V2; not an independent external signature). GitHub's Git Data commit API supplied root tree `60b0fddfe38708d4de486e0355ff684e8eb12b98`. Four nonrecursive Git tree API responses were fetched and normalized without changing their path/mode/type/SHA tuples. This is an API-derived projection, not raw server tree-object bytes or an independently authenticated GitHub channel.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

**H0:** A source blob plus an API-asserted tree entry does not establish that all intervening Git tree object IDs are internally consistent with the claimed root. A substituted parent/child entry or forged tree projection may pass a projection-only check.

Before this iteration: **0/4 Git tree object IDs independently reconstructed for this R16 pinned source**. The earlier V2 test proved source-byte binding to a pinned witness, not full tree-object reconstruction.

## ISOLATED_CANDIDATE / SEPARATE_EVALUATOR

The independent black-box Python evaluator was committed first, before the candidate. It uses the external `git hash-object -t tree --stdin` CLI as its OID reference and executes the candidate in a separate `python -S` subprocess. The candidate never imports or edits the evaluator. The evaluator was run locally on synthetic Git-tree fixtures, not claimed as external third-party validation.

- `frozen_alpha_source_tree_closure_oracle_v1_20261031.py`: 4,789 bytes, SHA-256 `06c4691c36ecfc780ba1b4d397ec7ffabe22a009e188df2603ba06152c18ab53`, Git blob `40709274207ceac66ffcc41b9aee633bf0419b56`.
- `alpha_source_git_tree_closure_v1_20261031.py`: 4,634 bytes, SHA-256 `41ba3417f2f5c52e81722d60dabc89a85da41c380880ae228716fc166abff8d1`, Git blob `1b4f58153ce0d6a9e4fd86ee980ce57981dbb1eb`.
- `alpha_source_git_tree_api_projection_v1_20261031.json`: 43,911 UTF-8 bytes, SHA-256 `6a72bcb7c8aaeedf1ef12efacadff2e39f1ed24b4d9dd2d7bf2bedbbd4146a9e`, Git blob `d0023443aca38399d809dba0941af3df0b173b46`. This is the full normalized 4-level projection for reproducibility, not original API response bytes.

Local frozen evaluator: **27/27 PASS**, including **26/26 negative/malformed fixtures FAIL_CLOSED**, using the independent Git CLI reference on four synthetic tree objects. The negative controls include substituted intermediate/leaf SHA, wrong root, wrong path, wrong blob, truncated tree, duplicate entries, symlink leaf, mode/type mismatch, missing/extra hop, invalid hash, malformed/duplicate-key/nonfinite JSON, and invalid Unicode. The frozen oracle's exact committed bytes were checked against the local tested file.

Separately, an independent JavaScript Git-object encoder and SHA-1 implementation reconstructed **all four real Git tree IDs** from the normalized live GitHub API responses and then from the committed projection. SHA-1(`abc`) and SHA-256(`abc`) were checked against standard known-answer vectors. The committed projection's SHA-256 and Git-blob SHA-1 were computed independently from its retrieved UTF-8 bytes. This real-data verification is independent of the Python candidate implementation but not independent of the GitHub API as a source.

| Hop | Reconstructed Git tree SHA-1 | Entries | Raw tree bytes | Result |
| --- | --- | ---: | ---: | --- |
| root → research | `60b0fddfe38708d4de486e0355ff684e8eb12b98` | 23 | 848 | MATCH |
| research → r16 | `2f477f51a0fcbae6fd904aec608f0e087d3dd1c0` | 21 | 668 | MATCH |
| r16 → alpha-node directory | `91c065df8ac166dbd429f45fc51833e91a01fc51` | 4 | 226 | MATCH |
| alpha-node directory → source blob | `a57d5ad50bf1b3ec163bc5284fb5a9a693138ced` | 271 | 21,658 | MATCH |

The final leaf is regular `100644` blob `73ef222f9117f566930390e60899d571ecc77402`. Each fetched tree reported `truncated=false`. The candidate verifies Git-canonical directory-aware sorting, full object SHA-1 reconstruction, four parent-child links and the externally supplied root/leaf pins; it does not accept a producer's root/leaf from the projection as independent authority.

**FALSIFIER:** change one entry SHA or mode, omit a tree entry, change root/leaf/path pins, introduce duplicate paths or truncation; the candidate must reject it. The valid unmodified projection must pass. A real-data Python end-to-end invocation of the committed 43,911-byte projection was **not executed in this run**; the actual-data OID reconstruction was independently executed in JavaScript. This distinction must remain explicit.

## BEFORE / AFTER / DECISION

| Metric | Before | After |
| --- | ---: | ---: |
| Real R16 source Git tree object IDs reconstructed | 0/4 | **4/4 MATCH** (independent JS) |
| Isolated Python black-box checks | Not applicable | **27/27 PASS** |
| Negative/malformed fixtures | Not applicable | **26/26 FAIL_CLOSED** |
| Actual R16 Python candidate + real projection end-to-end | 0/1 | **NOT_EXECUTED** |
| Authenticated GitHub transport / independent trust root | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Productive integration / WWW parity | NO | NO |

**Decision:** `TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE`, specifically stronger Git tree object internal-consistency evidence than API tree entry projection alone. This does not prove raw historical commit bytes, GitHub API transport authentication, collision resistance beyond Git SHA-1 semantics, an independently governed root pin, scientific truth, expert identity, independent R10 receipt, or operational integration. The historical V2 pin and original source remain unchanged.

Reproduce on a checkout with Python and Git installed:

```bash
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_source_tree_closure_oracle_v1_20261031.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_source_git_tree_closure_v1_20261031.py
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_source_git_tree_closure_v1_20261031.py 60b0fddfe38708d4de486e0355ff684e8eb12b98 research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py 73ef222f9117f566930390e60899d571ecc77402 < research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_source_git_tree_api_projection_v1_20261031.json
```

## R10 passive watch / goal metrics

R10 PR #115 remained OPEN and unmerged at observation. PR conversation: 0 comments; reviews: 0; review threads: 0. The detached R10 manifest at immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was retrievable as 4,588 UTF-8 characters and Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. The 217 Issue #93 comments observed were all authored by the owner GitHub login. No new independent authenticated expert receiver return was observed. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`.

The 90% handoff automation and 100% project-wide readback targets remain `NOT_COMPUTABLE`: the full authenticated denominator of eligible routine public handoff attempts and all publications, including failures, is absent. Local synthetic tests are excluded from these numerators. This research is not production-integrated. No new automation, pipeline root, external actor, evaluator self-approval, Hostinger/WWW change, Cursor dispatch or claim promotion. PR checks, exact main readback and append-only Issue #93 receipt are required before any `MAIN_PUBLISHED` statement.
