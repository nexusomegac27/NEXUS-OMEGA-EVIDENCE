# AXIOM Alpha-Node - Issue #93 UTF-8 receipt byte preflight V1 - 2026-10-30

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_RECEIPT_BYTE_PREFLIGHT_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = c57b255c983f30674ca037c6f6fe703b8552a1b8
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/204
PREDECESSOR_ISSUE93_RECEIPT = 6511131571
FROZEN_EVALUATOR_FIRST_COMMIT = aaee237498c4690e518e91a9bda27c995a06e85b
CANDIDATE_SECOND_COMMIT = 364da94ec32256645c46302179328c4b2fab6369
RUNTIME_INTEGRATION = NO
```

## Source and decision

The GitHub connector retrieved the pinned main commit, `AGENTS.md`, `GOVERNANCE.md`, R16 Alpha-Node adaptation contract, direct C1 research publication rule, task-anchor norm, repository structure and external actor registry. The last Issue #93 receipt (#6511131571) documents the PR #203 metadata contradiction: the original report has 6,078 text code units but 6,081 UTF-8 bytes, whereas its historical receipt claimed `REPORT_BYTES=6078`. PR #204 preserved the source and appended a correction. The existing October 28 byte-digest witness detects this mismatch when used, but there was no source-derived preflight at the receipt authoring boundary in this lane.

**One selected candidate:** an isolated, read-only, strict-JSON receipt byte preflight under the existing R16 research directory. It computes byte length, SHA-256 and Git blob SHA-1 from supplied Base64 original bytes; requires a caller-supplied API blob SHA-1 match; rejects contradictory claimed counts, digests, duplicates, malformed input, non-additive status and noncanonical paths. It never opens a network connection, writes repository files, posts an Issue comment, approves its own evaluator, or claims GitHub authentication. The input commit and API blob identities remain caller supplied, not independently authenticated by the CLI.

## Negative hypothesis and falsifier

**Negative hypothesis:** a receipt writer using `len(text)` can produce false byte metadata for non-ASCII UTF-8 text. The frozen synthetic fixture uses 6,076 ASCII characters plus U+2014 and U+00B7: `len(text)=6078`, `len(text.encode('utf-8'))=6081`. A naive character-count baseline would accept 6,078 as a size. The new preflight must reject a declared 6,078 with `BYTE_COUNT_MISMATCH`, derive 6,081 when no count is claimed, and accept 6,081 with matching hashes.

**Falsifier:** a frozen test that accepts the false 6,078-byte declaration, rejects the true 6,081-byte declaration, accepts a wrong Git blob, or permits duplicate source paths disproves the candidate's stated behavior. A real GitHub source mismatch would separately disprove any claimed API provenance; the preflight explicitly does not authenticate GitHub bytes or actor identity.

## Isolated test and before/after metric

The independent evaluator was committed first at `aaee237498c4690e518e91a9bda27c995a06e85b`; the candidate was committed second at `364da94ec32256645c46302179328c4b2fab6369`. Local source Git blob IDs were checked against the fetched GitHub blobs at those exact commits. The evaluator uses Python subprocesses, not candidate-owned assertions. It was rerun after both commits using the same locally hashed source bytes.

| Bounded measure | Baseline | Candidate |
|---|---|---|
| Synthetic Unicode incorrect declared size | 6,078 falsely accepted by naive text length | `BYTE_COUNT_MISMATCH` |
| Synthetic Unicode actual size | 6,081 UTF-8 bytes | 6,081 derived from raw bytes |
| Frozen independent subprocess tests | N/A | 20/20 PASS |
| Explicit duplicate path, invalid Base64, wrong blob | Not guaranteed by naive text length | Rejected in isolated fixtures |
| Actual project-wide handoff automation | NOT_COMPUTABLE | NOT_COMPUTABLE |
| Full authenticated source/test readback rate | NOT_COMPUTABLE | NOT_COMPUTABLE |

The synthetic oracle covers 20 positive/negative tests including Unicode, SHA-256, Git blob, duplicate JSON keys, duplicate paths, wrong repository/commit, path traversal, Boolean byte count and missing files. The candidate is not integrated into the existing receipt writer, so it does not retroactively repair earlier receipts and does not establish a production prevention rate. The 20/20 ratio is test coverage of this isolated suite only.

## Source-bound material inventory

- Frozen evaluator: `frozen_alpha_issue93_receipt_preflight_oracle_v1_20261030.py`, 5,303 bytes, SHA-256 `755fa24eddd4ebed9e946d3c4289d0cde54b99d458a151ac99a5d07db922c574`, Git blob `67892849e9cc8a6d524b40da7185f68fc65cfc59`.
- Candidate: `alpha_issue93_receipt_byte_preflight_v1_20261030.py`, 4,439 bytes, SHA-256 `8491e09f04d4a0046d4f66ecfdf80b16fb25ce5cc76d5b6cc31270014c05c8e2`, Git blob `3d9a9e65969cc78ed4ad0f6f16f91df4398204ca`.
- Both are under `research/r16/axiom-alpha-node-c1-adaptation-20261012/`; no existing source, evaluator or governance file was modified.

## R10 passive check and limits

R10 PR #115 was still open when checked. Its comment, review and review-thread collections returned no independent expert return. The historical detached manifest was read at immutable commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` with the recorded Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; prior independent UTF-8 byte and SHA-256 check is documented in PR #204. No new independent receiver ACK, authenticated external actor or actually executed expert research is established. The external actor registry remains empty. The R10 lane is observational only and is not a second improvement candidate.

`PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; the eligible complete event population and failed-attempt denominator are not authenticated. `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`; a complete publication denominator with independent source/test readbacks is absent. No source overwrite, rights change, runtime/Hostinger/WWW write, Cursor dispatch, worker creation, biological experiment or claim promotion is authorized or performed.

`BLOCKED_LANE != BLOCKED_SYSTEM`; `DRIFT_RESET=NON_DESTRUCTIVE`; `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`.
