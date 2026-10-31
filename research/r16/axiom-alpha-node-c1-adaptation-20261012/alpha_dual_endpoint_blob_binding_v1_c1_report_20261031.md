# AXIOM Alpha-Node — dual-endpoint/original-byte blob cross-binding · 2026-10-31

```text
OBJECT=NEXUS_OMEGA_ALPHA_DUAL_ENDPOINT_BLOB_BINDING_V1_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=e8b4fbaac62f269504cce62b20e5a064af3cb602
PREDECESSOR_PR=242
PREDECESSOR_ISSUE93_RECEIPT=6544982173
FROZEN_ORACLE_FIRST_COMMIT=25f05fe08daded8c678fdc8e88bca92a4c12a313
CANDIDATE_SECOND_COMMIT=ab38df2859e09b2f4405e5772e79c248b7a37f80
PUBLICATION_MAIN=NOT_ESTABLISHED_AT_REPORT_CREATION
```

## Observation, counterhypothesis and original-byte provenance

The prior dual-endpoint guard `alpha_pr_dual_endpoint_census_guard_v1_20261031.py` checks that PR-file and compare-API path sets match, but only checks the PR-file Git blob identifier's *format*. A forged 40-hex blob identifier can pass even if the filename sets are unchanged. This is a caller-supplied source-integrity gap, not evidence that GitHub itself was compromised. The prior original file was independently reconstructed byte-for-byte from pinned main for the local test: **5,183 bytes**, SHA-256 `210c19082277fdc98e05fb91509eec91e3e1cd8f17e51fdcef493b5f3033f603`, Git blob `9000a7a9afab83a35b3082347c6ca0e9064f60d2`.

Negative hypothesis: agreement of PR file paths and compare paths does **not** imply agreement of the actual original file bytes and the claimed Git blob IDs. The candidate composes the unchanged prior guard with an independent original-byte inventory, validates canonical base64, size, SHA-256 and Git blob for each listed file, and requires the recomputed Git blob to equal the PR-file API blob. It imports the existing published guard and does not edit it.

## Independent frozen evaluator and measured delta

The evaluator was locally written and run as a separate Python subprocess before the candidate was pushed, and its exact bytes were committed on the dedicated branch **before** the candidate. No post-candidate oracle edit.

- Frozen evaluator: `frozen_alpha_dual_blob_binding_oracle_v1_20261031.py` — **4,274 bytes**, SHA-256 `b9537bd995f4f091d3812e83c118a137aa11de30c74d8998cc58fab9a58429a0`, Git blob `f5d2499ea9590357ea807e879d8677c84a2a5e6c`.
- Candidate: `alpha_pr_dual_endpoint_blob_binding_v1_20261031.py` — **3,672 bytes**, SHA-256 `4e4a559ccbe0512ab988244655afeed478838c50393bc516eb874d16fb656edf`, Git blob `8c4b0857b66107ccb3571948f35fa96adbbcbc7d`.
- Reproduce from the existing R16 directory: `python frozen_alpha_dual_blob_binding_oracle_v1_20261031.py alpha_pr_dual_endpoint_blob_binding_v1_20261031.py alpha_pr_dual_endpoint_census_guard_v1_20261031.py`.
- Actual isolated Python 3 subprocess execution: **14/14 assertions PASS**, including **10/10 deliberately corrupted source/metadata mutants rejected**; the old guard accepted **1/1** syntactically valid forged blob fixtures, whereas the candidate rejected **1/1**. The oracle deliberately confirmed that a *jointly forged* file set, API listings and source bytes still passes; this is a disclosed residual falsifier, not a PASS for transport authenticity.

These are synthetic fixture results. No real PR was falsely attributed to this synthetic fixture, and no project-level throughput improvement was measured. The source-set completeness and GitHub API actor/transport are **not authenticated** by this validator. A jointly fabricated input may still pass. Source sizes are limited to 1 MiB per file and the prior guard's additive/linear/1–100-file scope remains.

## Scope and project targets

All new files are additive under the existing R16 research lane. No historical overwrite, evaluator self-approval, new pipeline root, runtime, worker, Hostinger, WWW, branch-rule, external actor registration or claim promotion. Existing GitHub CI and exact main/receipt readback must be verified separately before reporting publication.

Handoff target >=90%: `NOT_COMPUTABLE` because the authenticated complete eligible-attempt denominator and numerator including failures are missing. Project-wide publication full-readback target 100%: `NOT_COMPUTABLE` because the complete authenticated publication denominator is missing. Zero unauthorized writes remains a target, not a globally verified result. A local 14/14 test result is not a handoff success rate.

R10 secondary read-only: PR #115 open; pinned detached manifest SHA-256 is a reference, not an independent expert acknowledgment. Issue #93 contained 232 owner-authored comments at intake; no independently authenticated R10 expert return was identified. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.
