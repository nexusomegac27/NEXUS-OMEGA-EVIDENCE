# AXIOM Alpha-Node — Handoff Evidence-Reference Uniqueness Guard V2 — C1 — 2026-11-01

\`\`\`text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_EVIDENCE_REFERENCE_UNIQUENESS_V2_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=8f4642094aaca7a7b11c883513441b85638b38f0
PREDECESSOR_MAIN=7356cfacafadf469897b2cd920a7c76072206a5f
PREDECESSOR_PR=264
PREDECESSOR_ISSUE93_RECEIPT=6556833262
FROZEN_EVALUATOR_FIRST_COMMIT=385d66637ca0b247e87146b0507ea7dadf438bec
CANDIDATE_SECOND_COMMIT=ed662a8964419be12f297c6f5ed81d04485cc7ae
TEST_STDOUT_THIRD_COMMIT=623e913b96bd95c00307c82082cddcfe9fd6ea7e
PRODUCTION_INTEGRATION=NO
\`\`\`

## Original source and one bounded candidate

The immutable source is the V1 denominator guard at \`research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_denominator_guard_v1_20261101.py\` on main \`8f4642094aaca7a7b11c883513441b85638b38f0\`. Source identity: 3,277 UTF-8 bytes, SHA-256 \`f3e5f4d43dab8069e12090008da1e2b59046983f04d4454e663a8b2b112e3e83\`, Git blob \`34c0b23fcff0d0fe2dc63af7c984fe5c10bb013d\`. It remains unchanged.

**Negative hypothesis:** V1 deduplicates \`attempt_id\` but not \`evidence_ref\`. Two distinct claimed handoff attempts can reuse one receipt, inflating the automated numerator and denominator while still yielding \`METRIC_READY_STRUCTURAL_ONLY\`. Whitespace aliases of the same reference are likewise accepted. This is a structural false-acceptance class, **not evidence of an actual forged GitHub handoff**.

**Single candidate:** V2 requires a unique nonblank, whitespace-trimmed, attempt-level \`evidence_ref\` across all input rows. Reuse returns \`NOT_COMPUTABLE\` for the entire submitted census, including when one row is ineligible. Distinct attempt-scoped references (e.g. distinct URL fragments) remain allowed. A shared aggregate receipt can legitimately cover multiple attempts; in that situation the stricter structural contract requires distinct attempt-level evidence bindings or a separately validated aggregation scheme. This is deliberately conservative, not a universal proof of fraud.

## Frozen, separate evaluator and measured delta

The 15-fixture evaluator was authored and committed **before** the candidate file. It invokes the tested script in a fresh Python subprocess for each case. It contains fixed expected tuples independent of the candidate implementation. The evaluator was not changed after the first commit.

| Measured quantity | V1 baseline | V2 candidate |
|---|---:|---:|
| Fixed expected outcomes (15 fixtures) | 10/15 | **15/15** |
| Duplicate/aliased-reference negative fixtures rejected | 0/5 | **5/5** |
| Remaining positive and regression controls | 10/10 | **10/10** |
| Real authenticated census / production handoffs | Not available | **Not available** |

The five falsifiers are: duplicate successful receipt, leading/trailing whitespace alias, one receipt shared by success and failure, one receipt shared by eligible and ineligible rows, and tab/newline alias. If V2 accepts any of these or rejects a valid unique-reference positive control, reject this candidate. Tests are synthetic only, with no secrets or third-party original content.

Reproduce from the repository root:

\`\`\`sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_reference_uniqueness_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_denominator_guard_v1_20261101.py
# expected: exit 1, 10/15
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_reference_uniqueness_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_reference_uniqueness_guard_v2_20261101.py
# expected: exit 0, 15/15
\`\`\`

### Pre-publication local byte bindings

- Frozen evaluator: 4,279 bytes; SHA-256 \`dc6f8594cff94bf55ea54b4d62f233beb67ca1350e66564e779df15f80d78cdc\`; Git blob \`d80eed8539adab41f6b0e812f34340ad8dcd46fb\`.
- V2 candidate: 3,522 bytes; SHA-256 \`4c6e3d6dfd58988c9e234ee7235362a6ec7dcb20203481e245fd8fcad1b3f370\`; Git blob \`c00c52b17fb424062ae981f91d00ea73430076d8\`.
- V2 subprocess stdout: 2,206 bytes; SHA-256 \`047669529c5c6430086d65110d602ca880c49135a7218adb62d0769375ffedbd\`; file \`alpha_handoff_reference_uniqueness_v2_eval_stdout_20261101.jsonl\`.
- V1 subprocess stdout (local only): 2,251 bytes; SHA-256 \`c540145c7a91a6b187bcfd15776cc0824fa599ce08bc07a0a62b057f71ac5060\`.

## Scope, limitations, decision

The guard still **does not** authenticate GitHub actors, receipts, reference contents, event provenance or a complete census. The input can still falsely assert \`coverage_complete=true\`. Project-wide eligible attempts, actual automated successes and the 90% rate remain \`NOT_COMPUTABLE\`; the seven-PR historical publication cohort is not a substitute denominator. No production integration, new worker, runtime, Hostinger/WWW modification, external actor registration, Task Anchor modification, scientific promotion or change to the frozen V1 source is requested.

R10 PR #115 and the passive Issue #93 were read separately. No independent receiver ACK or expert execution evidence was observed in PR comments/reviews; owner SEND remains distinct from receiver authentication. This candidate is unrelated to R10 and does not expand its permissions.

This document is a C1 research candidate record. A publication claim requires actual PR/CI, immutable main readback, file-by-file SHA-256/blob verification and a separate append-only Issue #93 receipt. Until then: \`PUBLICATION=NOT_ESTABLISHED\`.
