# AXIOM Alpha-Node · C1 receipt-order chronology guard · 2026-10-28 R0

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_ORDER_CHRONOLOGY_20261028_R0
STATE = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 1c434c820c30d662ea8d557c7a5b06bb90f75823
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/177
PREDECESSOR_ISSUE93_RECEIPT = 6477928081
AUTHORITY = docs/governance/NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0.md
WRITE_SCOPE = OWNER_RESEARCH_ONLY_EXISTING_R16_DIRECTORY
PRODUCTION_INTEGRATION = NO
EXTERNAL_ACTOR_REGISTRATION = NONE
WWW_DEPLOY = NO

## Observation and pinned original

The physically fetched V2 and V5 sources on pinned main expose an integrity gap: the V2 receipt-chain audit verifies positive receipt IDs, uniqueness among supplied records, and that each predecessor matches the preceding record, but does not require a child GitHub issue-comment ID to be strictly greater than its predecessor. V5 extends commit-acyclic checks without changing that receipt rule.

- V2 path: research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_receipt_chain_reconciler_v2_20261028.py; Git blob 9dc125ed90be9f875e698a6189d3007787394f7e.
- V5 path: research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_receipt_chain_reconciler_v5_20261028.py; Git blob 4f3dc94e61a12b34141aa6f0ce178c39056818ad.
- Pinned source: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/tree/1c434c820c30d662ea8d557c7a5b06bb90f75823/research/r16/axiom-alpha-node-c1-adaptation-20261012
- Issue #93 readback at observation: 167 comments; latest receipt 6477928081. R10 PR #115 remains open with no independent review or conversation receipt in this readback.

## Negative hypothesis, falsifier and scope

H0: receipt-parent equality and within-list uniqueness suffice for chronological integrity. A self-referential initial receipt (parent ID = child ID) or backward child ID falsifies H0 for a purported append-only GitHub issue-comment chain. The chronology guard rejects any receipt_id <= receipt_predecessor_id, preserving exact linkage.

This is an orthogonal isolated guard, NOT a replacement for V5. It does not call GitHub APIs, authenticate GitHub actors, prove raw comment-byte identity, validate Git commit graphs, or establish scientific claims. An internally consistent forged increasing sequence is an explicit counterexample: it passes without proving provenance.

## Independent frozen black-box evaluation

Evaluator committed FIRST on owner branch: 18f84cd741fb3fe2be2399f94c135ed433c6ccbd.
- frozen_receipt_order_oracle_v1_20261028.py
- 4283 bytes; SHA-256 01614236a06a163697fd573d7ecbb5c40b4d238ea988ab70db36333ae2de22de; Git blob ef9170ba34d7689a5a0b1ea29c617aa9ceb2752a.

Candidate committed SECOND: 63670ad643b3ecf599d94e7fa60a52a40c4d8bb8.
- alpha_receipt_order_guard_v1_20261028.py
- 2823 bytes; SHA-256 ca04bf21025f7aac77eef522240cd4bf9940bdb86f640a7233059f3468245793; Git blob 19eea36ffbde83473cab4a7a082a2afe36176f99.

Reproduction in the existing research directory:
python -m unittest -v frozen_receipt_order_oracle_v1_20261028.py

Local Linux/Python sandbox: 15/15 PASS (3 positive, 4 chronology-negative, 8 additional invalid-input checks). Four chronology-negative fixtures include initial self-reference, initial backward link, later self-reference, later backward link. A negative mutant with the chronology condition disabled fails 4/15 tests as expected (remaining 11 pass). The evaluator uses a separate subprocess and does not import candidate code.

Before: V5 source has no strict chronological issue-comment ID check (source-inspection observation; exact V5 code was not locally executed in this run). After: isolated guard rejects 4/4 targeted chronology-negative fixtures and accepts 3/3 positive fixtures. No project-wide rate or production improvement is claimed.

## Decision and limits

TESTED_IMPROVEMENT for the isolated guard only. No existing source or independent oracle modified. Public-safe, additive, reversible, C1-only, existing R16 research lane. External third-party validation and authenticated GitHub API integration unestablished. AUTOMATION_RATE=NOT_COMPUTABLE; PROJECT_READBACK_RATE=NOT_COMPUTABLE; no private handoffs counted. No WWW parity asserted.

R10 remains separate: PUBLIC_SEND=OWNER_MEDIATED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED. R10 manifest pinned to 539d4bb33d2ba2c4895713c1bc437ece0743eeea; no new R10 claim promoted.
