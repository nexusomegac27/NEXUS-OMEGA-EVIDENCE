# AXIOM Alpha-Node · C1 GitHub API-shaped Issue #93 receipt crosscheck · 2026-10-28

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_API_CROSSCHECK_20261028_R0  
STATE = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 6e700be6fd408c3d78d3d7e08619b635de92966f  
PREDECESSOR_MAIN = 1c434c820c30d662ea8d557c7a5b06bb90f75823  
PREDECESSOR_ISSUE93_RECEIPT = 6478246029  
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/178  
AUTHORITY = docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md  
SCOPE = EXISTING_R16_RESEARCH_ONLY; NO_PRODUCTION_INTEGRATION; NO_WWW_WRITE

## Observation and original sources

The prior `alpha_receipt_order_guard_v1_20261028.py` (Git blob `19eea36ffbde83473cab4a7a082a2afe36176f99`) checks caller-supplied receipt ID order, not actual PR/main commit correspondence. This leaves a measurable integrity gap: a receipt can claim a different main commit while keeping an increasing ID chain. It is not evidence of a real attack.

Read-only GitHub REST observation on 2026-10-28: `GET /issues/comments/6478246029`, `/issues/comments/6477928081`, `/pulls/178`, `/commits/6e700be6fd408c3d78d3d7e08619b635de92966f`, `/branches/main`, and `/pulls/178/files?per_page=100`. All paths are under `https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE`. Observed: owner-authored receipt 6478246029 (19:14:07Z) links owner-authored predecessor 6477928081 (18:59:30Z); PR #178 merged at 19:13:23Z; GitHub-signed merge `6e700be6fd408c3d78d3d7e08619b635de92966f` has parent `1c434c820c30d662ea8d557c7a5b06bb90f75823`; 3/3 PR paths match commit file paths; main pointed at the merge when observed. This is a time-scoped REST observation, not proof of independent actor receipt.

The JSON file `alpha_issue93_api_projection_pr178_20261028.json` is an **explicitly reduced API-derived projection**, not original HTTP response bytes, not a signed GitHub attestation, and not a reusable authenticated snapshot. Its fields were transcribed from the above REST readback. Do not infer provenance from the offline validator's acceptance of this projection.

## Falsification and independent test

H0: receipt-ID ordering alone is sufficient for PR/main receipt integrity. Falsifier: keep the same ordered receipt IDs but alter the PR merge SHA, receipt main SHA or branch main SHA. The previous ID-only guard has no fields to detect these differences; the new isolated candidate rejects them. Counterexample to the new candidate: forge **all** caller-supplied API-shaped objects consistently; offline validation can still pass. Therefore `api_origin_authenticated=false` is mandatory.

- Frozen separate subprocess evaluator FIRST commit: `6f3dfa4629ab521a99e638fdf47621239d7600db`; file `frozen_issue93_api_crosscheck_oracle_v1_20261028.py`, 5535 bytes, SHA-256 `7f19b770e53351bae9fac8c740cc4b66b3ad6c29e9f093158ad60396d23fdb0d`, Git blob `09a23719c776849497b1141239c652962b6ba25d`.
- Candidate SECOND commit: `583fe99d75fd783d274315f8126cd5fa8c7422fd`; file `alpha_issue93_api_crosscheck_v1_20261028.py`, 5931 bytes, SHA-256 `bee92d67b18d1b831dee259ec633018509d803081bce5b776fd9d455205a981d`, Git blob `b886dff345bc0a572c8554d42fad68e1cddaca1f`.
- Observed projection THIRD commit: `63785458b8ac3ad5d7d9aa89f0b2ed18e7a567be`; file `alpha_issue93_api_projection_pr178_20261028.json`, 2280 bytes, SHA-256 `9e445ccbd81a835feede78660b2b776b239915076f1afe71315f4fb103c9984b`, Git blob `3ab0342a4326b47eef7bce862bc48b94665ab6af`.

Run in this existing R16 directory:

```bash
python -m unittest -q frozen_issue93_api_crosscheck_oracle_v1_20261028.py
python alpha_issue93_api_crosscheck_v1_20261028.py < alpha_issue93_api_projection_pr178_20261028.json
```

Local isolated Python test: **16/16 PASS** (2 positive, 14 negative) with an independently authored subprocess oracle, frozen before candidate publication. The API-derived 3-file projection returns scoped PASS; altering the PR merge SHA returns `FAIL_CLOSED: MAIN_PR_COMMIT_MISMATCH`. Before: no PR/main API-shaped crosscheck in the receipt-ID-only guard. After: 3/3 targeted forged main/PR/ref mismatch tests rejected; 3/3 observed PR/commit file paths consistent. This does **not** establish a project-wide handoff rate or independent third-party validation.

## Decision and boundaries

Candidate is additive, reversible, public-safe, isolated C1 research. It neither fetches APIs nor authenticates their origin; actual source file bytes, GitHub response transport authenticity, third-party expert identities, and whole-project census remain separate checks. A GitHub signature verifies the commit's GitHub-reported signature state, not scientific validity. Existing governance, structure, historical files, production Steward, external write-slot registry, model weights, runtime, Hostinger and WWW are unchanged.

Project-wide `AUTOMATION_RATE=NOT_COMPUTABLE` and `READBACK_RATE=NOT_COMPUTABLE`; complete eligible project denominators absent. This run's prepublication candidate has `PUBLISHED_HANDOFFS=0/0` until actual merge/readback. R10 PR #115 remains open with 17 owner-mediated files and zero review, inline, or conversation comments in the checked API; pinned manifest 4588 bytes / Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. `PUBLIC_SEND=OWNER_MEDIATED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. No R10 actor self-registration, new transport, Cursor dispatch, or biological experiment.
