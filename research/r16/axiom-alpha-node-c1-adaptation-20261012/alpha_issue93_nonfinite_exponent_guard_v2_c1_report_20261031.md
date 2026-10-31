# AXIOM Alpha-Node — Issue #93 nonfinite-exponent JSON fail-closed · 2026-10-31

OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_NONFINITE_EXPONENT_GUARD_V2_20261031_R0  
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
PINNED_MAIN_BEFORE = 8036ffdb2985c688705f2d29f594b8dd757a5f55  
PREDECESSOR_PR = 248  
PREDECESSOR_ISSUE93_RECEIPT = 6548115987  
FROZEN_ORACLE_FIRST_COMMIT = 1ec0253cd5a74f9f4d69c45a5272f0da013a21b0  
CANDIDATE_SECOND_COMMIT = c0d34dbe05b00a36a2385b2eee221c9ac5f1c727  
PUBLICATION_MAIN = NOT_ESTABLISHED_AT_REPORT_CREATION

## Observation and negative hypothesis

The exact V1 source at pinned main was fetched as Git blob `673e1424a9e85914b80c58d4b2e659ad0339e258`, 4,064 UTF-8 bytes, SHA-256 `633c7621d8bfb7851a292fc2cc638c03bfe4691a72ee684f0246f3f8f3a014c5` (independently rehashed local exact copy). Its `json.loads` rejects `NaN`/`Infinity` through `parse_constant`, but default `parse_float` converts `1e999` and `-1e999` to nonfinite Python floats. When these are in an ignored extra JSON field, V1 returns `DOUBLE_INVENTORY_STABLE_NOT_ATOMIC` with exit 0. Thus the broad nonfinite-JSON fail-closed expectation is falsified for two syntactically valid extreme exponents. This is a parser-scope integrity issue; it does not establish that GitHub ever emitted such a field.

## Isolated change and reproducible independent test

V2 preserves the pinned V1 evaluator and adds only `parse_float=finite_float`, rejecting values where `math.isfinite(float(token))` is false. No original code, independent evaluator, production runtime or repository governance was modified.

A separate black-box Python subprocess oracle was committed **before** the V2 candidate. It was executed locally with Python 3 against the exact V1 source and V2. From the R16 research directory, run:

`python frozen_alpha_issue93_nonfinite_exponent_oracle_v1_20261031.py alpha_issue93_double_inventory_guard_v1_20261031.py alpha_issue93_double_inventory_nonfinite_exponent_v2_20261031.py`

Observed: **9/9 expected V2 outcomes** (4 positives, 5 negatives), exit 0. The two extreme-exponent negatives are **2/2 false accepts on V1** and **2/2 structured FAIL_CLOSED on V2**. Positives: empty stable inventory, finite fractional extra field, finite large exponent, Unicode scalar. Negatives: positive and negative overflow exponent, NaN, Infinity, duplicate JSON key. Existing 25-case V1 frozen oracle was not re-executed against V2 in this run; full regression and real REST payload execution remain unproven.

Byte provenance:
- Frozen oracle: 1,912 UTF-8 bytes, SHA-256 `247df4df9fa47edbc9ebb15d8585c36ab8aec6776a3332cd2c7f9ef29df58ec5`, Git blob `7982186d629feec53a0ab173cf55dac8ad410911`.
- Isolated V2: 847 UTF-8 bytes, SHA-256 `baf335b20f1a169dd35f33d811213d675c34c7a222a1827dbfd5d8e6644dccab`, Git blob `400a7d161217e87c19bc41b8e26859e8be2fad4b`.
- V1 unchanged: 4,064 UTF-8 bytes, SHA-256 `633c7621d8bfb7851a292fc2cc638c03bfe4691a72ee684f0246f3f8f3a014c5`.

## Falsifier, scope and decision

A V2 acceptance of `1e999` or `-1e999` anywhere in the JSON payload, or rejection of finite valid positive fixtures, falsifies the stated improvement. The oracle does not authenticate REST transport, prove atomicity, establish actor identity or validate a real full Issue #93 inventory. The current source-census is 237 normalized owner-labeled comments; this is not the project handoff denominator. `AUTOMATION_RATE=NOT_COMPUTABLE`, `FULL_READBACK_RATE=NOT_COMPUTABLE` project-wide. No production integration, additional automation, worker, Cursor dispatch, Hostinger/WWW write, external actor registration, R10 merge, biological experiment, or claim promotion.

R10 PR #115 is open; its independent expert return remains `SOURCE_NOT_PRESENT` for an authenticated receiver ACK. The detached R10 manifest was fetched at original head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` with Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, 4,588 UTF-8 bytes. No new independently authenticated expert receipt was identified in the inspected PR discussion and Issue #93. Scientific expert adjudication and executed independent expert research remain unestablished.

CI, merge, actual immutable main readback and append-only Issue #93 receipt must be separately verified after publication.
