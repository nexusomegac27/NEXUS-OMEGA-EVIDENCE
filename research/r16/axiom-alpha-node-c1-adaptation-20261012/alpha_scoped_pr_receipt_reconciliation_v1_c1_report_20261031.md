# AXIOM Alpha-Node — bounded GitHub PR/receipt reconciliation V1 · 2026-10-31

```text
OBJECT = NEXUS_OMEGA_ALPHA_SCOPED_PR_RECEIPT_RECONCILIATION_V1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_BOUNDED_PROVENANCE_MEASUREMENT
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = b8e9a27e88f8806a72c2d7945337214ed884aec6
PINNED_MAIN_PARENT = f28a5e46398c46afe77fde8cdd35522a4cb2d37c
PREDECESSOR_PR = 237
PREDECESSOR_ISSUE93_RECEIPT = 6541883668
FROZEN_ORACLE_FIRST_COMMIT = 1ce8e783eb8e26411d0df5182115c2890e4f3240
SOURCE_PROJECTION_SECOND_COMMIT = 90505df01b0418964f181441288b51bb84b3f3b2
SOURCE_WINDOW = PR_228_TO_237_INCLUSIVE
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## One candidate and negative hypothesis

The single improvement is a **bounded, independently falsifiable reconciliation of actual GitHub PR merge metadata, Git commit-parent objects and Issue #93 receipt references**. The predecessor handoff census V1.1 was structural-only on synthetic events and correctly left the project-wide numerator/denominator unknown. This candidate does not replace that tool or claim to solve its completeness gap; it adds a measured, explicitly scoped real-API publication/receipt consistency subset.

H0: One or more of ten consecutive published Alpha-Node PRs may lack a corresponding owner-authored receipt, may point to a different merge commit or PR head, or may break the immutable main-parent chain. Any such counterexample falsifies the complete reconciliation claim. Source is GitHub itself, not a cryptographically independent witness.

## Source/provenance and pinned baseline

The source set was retrieved on 2026-10-31 using the connected GitHub API: `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pulls/{228..237}`, `GET /repos/.../git/commits/{merge_sha}`, and all pages of `GET /repos/.../issues/93/comments`. The repository `main` at the observation baseline was `b8e9a27e88f8806a72c2d7945337214ed884aec6` with parent `f28a5e46398c46afe77fde8cdd35522a4cb2d37c`. Original API responses and comment bodies were read to derive the projection, but **raw JSON response bytes and complete receipt bodies are not archived in the projection**; no raw API JSON SHA-256 or independent actor authentication is claimed. The projection is a *derived, replayable field inventory*, not a source-byte substitute.

The operator's governing sources were read at the immutable baseline: `AGENTS.md` blob `f24f7cf557927016860279b65d0725275e6270a9`; `GOVERNANCE.md` blob `b630b62eb9800e2f57b6c86318c72faadb29c23b`; R16 Alpha adaptation contract blob `f8adcf6df22bba526c17dbff72b7ad494b42c63e`; direct C1 publication rule blob `a99e6fc7c71cbf82bdfdd9cf414b44a362073ce8`; task-anchor norm blob `51c97b624f14fe9c3f1dfe1bf13394a773f87935`. The external actor registry blob `1fabcab7f556e83621a3676ddfb3d11cdd964b55` remains default DENY with empty external allowlist.

## Frozen evaluator and observed test

The independent offline Python oracle was committed **before** the source projection on the same short-lived research branch. It is separate from the GitHub API extraction and accepts only a fixed ten-PR projection. The frozen oracle is 5,843 bytes, SHA-256 `6c895281384e9cfaa43d3855cf68e0fc3a2f69fbf5090a05b5c8479ccaa9d561`, Git blob `6681403e9a5acc8de9296bf0b9f7e081da9ecdf8`. The derived projection is 7,690 bytes, SHA-256 `0ffd9f15c112fbc7ced21a81b5d14144d6f424282e0b78439ee800aa2c098836`, Git blob `32fc123dc1cef2d523a8187f1ba892c1c2da6296`. Both Git blobs were checked against the local Git object formula and fetched from the frozen branch commits. Its first independent isolated Linux execution used Python standard library only:

```sh
python frozen_alpha_scoped_pr_receipt_oracle_v1_20261031.py --selftest < alpha_scoped_pr_receipt_api_projection_v1_20261031.json
```

Observed result: `SCOPED_API_PROJECTION_CONSISTENT`, **10/10** PR merge/receipt references consistent, **10/10** Git parent-chain entries consistent, **9/10** receipts explicitly declaring their parent (the tenth parent is verified from the Git object but not repeated in its receipt), **1/1** positive control and **10/10** adversarial negative fixtures detected. The negative fixtures mutate receipt main SHA, duplicate receipt ID, Git parent, PR base, actor label, merge flag, PR head, drop a record, omit a SHA, or attempt C2 promotion. A separate JavaScript crosscheck against fresh PR and Issue API results made **119/119** bounded field assertions and detected **8/8** deliberately corrupted fixtures. Both are technical checks against GitHub-sourced fields, not external third-party validation.

Before: no consolidated ten-PR Git-commit/receipt reconciliation in the previous structural handoff-census report. After: **10/10** in this exact selected window, with falsifiers and a frozen evaluator. The rate is a **bounded consistency coverage**, not the project's `FULL_READBACK_RATE` and not the automation/handoff rate. This selected ten-PR sample cannot establish project-wide completeness, publication eligibility, full source-byte checks, CI sufficiency, independence of actors, or the absence of unobserved failures. The 227 observed Issue #93 comments were all owner-authored at extraction; they are **not** 227 eligible handoff attempts.

## Falsification and stop boundaries

Any real PR merge SHA, immutable Git parent, PR head, receipt link, receipt author or C1 field that disagrees with the projection invalidates the corresponding row. A missing/duplicate receipt or an unlisted PR within the declared window fails the frozen oracle. A future branch advance does not retroactively change this pinned snapshot; a successor must fetch and independently revalidate new source objects. A forged but internally consistent GitHub API projection could pass the offline oracle: the oracle does not authenticate its input and must never be treated as an independent source witness. Source-to-file SHA-256 and Git-blob readback for **all historical published files** remains separately unproven by this audit.

## R10 secondary readback

PR #115 remains OPEN/UNMERGED, current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, original pinned head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`. Detached manifest Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` is identical at both heads; its declared 4,588-byte SHA-256 is not an independently authenticated expert return. PR discussion has zero comments and no new independent receiver ACK. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`.

## Decision and nonclaims

`TESTED_IMPROVEMENT` applies only to **bounded GitHub provenance measurement** and negative-case detection. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` because the authenticated complete eligible-handoff denominator is unavailable. `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE` because the complete eligible publication denominator and per-publication source/test readbacks are not independently censused. No new automation, folder root, write slot, production workflow, runtime/Hostinger action, Cursor dispatch, R10 merge, biological experiment or C1 promotion. This report and its code/data remain isolated C1 research; publishing it does not certify its scientific or operational validity.
