# AXIOM Alpha-Node — Issue #93 Unicode scalar fail-closed V3 · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_UNICODE_SCALAR_GUARD_V3_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = cfad6f9ad1f51efc2114249f14228aaa3a1c4cbd  
PREDECESSOR_PR = 249  
PREDECESSOR_ISSUE93_RECEIPT = 6548805508  
FROZEN_ORACLE_FIRST_COMMIT = 794677cef7b0ddb4892ebdf74f8b4f81c144ad0f  
CANDIDATE_SECOND_COMMIT = bf03a0371ac9b7ff6fec24c0481e6bdc08043ef6  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Observation and negative hypothesis

The exact V2 source on pinned main was independently fetched and reproduced locally: 847 UTF-8 bytes, SHA-256 `baf335b20f1a169dd35f33d811213d675c34c7a222a1827dbfd5d8e6644dccab`, Git blob `400a7d161217e87c19bc41b8e26859e8be2fad4b`. Its imported V1 evaluator was also reproduced: 4,064 bytes, SHA-256 `633c7621d8bfb7851a292fc2cc638c03bfe4691a72ee684f0246f3f8f3a014c5`, Git blob `673e1424a9e85914b80c58d4b2e659ad0339e258`.

**Falsifiable counterexample:** JSON escaped lone UTF-16 surrogate code units in ignored extra object values or keys are accepted by V2 (`2/2` synthetically demonstrated), despite not being valid Unicode scalar values. The V2 predecessor **already rejects** an invalid surrogate in a digest-bearing comment body (`1/1`), so the finding is limited to unexamined JSON subtrees and keys. This is not evidence that GitHub actually emitted malformed Unicode.

## Isolated change and independent tests

V3 recursively checks every decoded JSON string, including object keys, and rejects code points U+D800–U+DFFF before calling the unchanged V1 inventory evaluator. It imports the unchanged V2 finite-float parser; no historical file, evaluator, productive runtime, governance, or actor registry is modified.

A separate black-box Python subprocess oracle was committed **first**, before the V3 candidate. The isolated Python 3 tests ran locally against exact reconstructed-and-rehashed V1/V2 predecessor bytes and the candidate:

- `python frozen_alpha_issue93_unicode_scalar_oracle_v1_20261031.py alpha_issue93_double_inventory_nonfinite_exponent_v2_20261031.py alpha_issue93_unicode_scalar_guard_v3_20261031.py` → **12/12 expected outcomes**, 5 positive, 7 negative; V2 accepted 2/2 specifically targeted ignored-surrogate cases.
- `python frozen_alpha_issue93_double_inventory_oracle_v1_20261031.py alpha_issue93_unicode_scalar_guard_v3_20261031.py` → **25/25** earlier frozen inventory regression outcomes.
- `python frozen_alpha_issue93_nonfinite_exponent_oracle_v1_20261031.py alpha_issue93_double_inventory_guard_v1_20261031.py alpha_issue93_unicode_scalar_guard_v3_20261031.py` → **9/9** earlier frozen finite-number regression outcomes.

**Combined scoped regression:** 46/46 expected subprocess outcomes, with the new 7/7 adversarial Unicode fixtures rejected. These are local independent-code tests, not external third-party scientific validation. The candidate has not been executed on a complete real Issue #93 REST inventory.

Byte provenance of additive files:
- Frozen new oracle: 3,154 UTF-8 bytes; SHA-256 `268498fc6f4d7c03c9a368bce7df93937a0ea86bd4c038dfba31f295e8c22c93`; Git blob `f9d03c6ebe70c9cbfce40fc0aa444aa4d5ae9908`.
- V3 candidate: 1,246 UTF-8 bytes; SHA-256 `e17749dd802096fc95ff56c8023674e767d3dc64668508286473768b26c45fe0`; Git blob `4a0663fc7769f7cc56ff161a1383ea72f3453503`.

## Falsifier and bounded decision

Acceptance by V3 of a lone surrogate anywhere in decoded JSON, or rejection of the tested valid Unicode scalar fixtures, falsifies this improvement. The check does not authenticate GitHub actor identity, REST transport, pagination completeness or atomicity; very deep JSON, out-of-band source alterations and all untested formats remain outside this claim.

Issue #93 source census at observation: 238 normalized owner-authored comments, with no independent R10 expert receiver ACK. R10 PR #115 is open; detached manifest at immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` has Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

Project-wide `AUTOMATION_RATE=NOT_COMPUTABLE`, `FULL_READBACK_RATE=NOT_COMPUTABLE`: authenticated eligible handoff and publication denominators are unavailable. The 238 comments and 46 local tests are **not** project-wide denominators. No new automation, Cursor dispatch, Hostinger/WWW write, R10 merge, external actor registration, node reset, biological experiment, production integration or claim promotion. CI, actual PR merge, immutable main readback and append-only Issue #93 receipt must be separately established after publication.
