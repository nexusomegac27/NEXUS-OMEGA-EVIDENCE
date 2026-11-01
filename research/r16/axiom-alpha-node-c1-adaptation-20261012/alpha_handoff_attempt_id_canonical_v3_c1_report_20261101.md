# AXIOM Alpha-Node — Canonical Attempt-ID Guard V3 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_ATTEMPT_ID_CANONICAL_GUARD_V3_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=cb2653eac6c40fe24e246ca19981de4e21f664f5
MAIN_PARENT=8f4642094aaca7a7b11c883513441b85638b38f0
PREDECESSOR_PR=265
PREDECESSOR_ISSUE93_RECEIPT=6557177847
FROZEN_EVALUATOR_FIRST_COMMIT=f81d30ce93296d6061fa16c5e6af9442e4d2f1e1
CANDIDATE_SECOND_COMMIT=9302f2349e71fccff5a8ffb6e468f03466bb6027
TEST_STDOUT_THIRD_COMMIT=f6287e9e5564fc8e69a53df7bf1f194c3f7b4c63
PRODUCTION_INTEGRATION=NO
```

## Original bytes, negative hypothesis, and isolated candidate

The immutable V2 baseline is `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_reference_uniqueness_guard_v2_20261101.py` at the pinned main. Its 3,522 bytes have SHA-256 `4c6e3d6dfd58988c9e234ee7235362a6ec7dcb20203481e245fd8fcad1b3f370` and Git blob `c00c52b17fb424062ae981f91d00ea73430076d8`. This source was independently reconstructed byte-for-byte and was not changed.

**Negative hypothesis:** V2 compares raw `attempt_id` strings. Distinct spellings of one identifier (leading/trailing whitespace, NFC/NFD Unicode aliases, invisible control/format characters) can be counted as separate attempts despite sharing a semantic identifier. This can inflate the denominator and automated numerator in an untrusted submitted census. This is a structural vulnerability, not an observed fraudulent real-world handoff.

**Single V3 candidate:** require every attempt ID to be nonempty, already whitespace-trimmed, in Unicode NFC, and free of `Cc`/`Cf` characters. Reject noncanonical IDs and duplicate canonical IDs with `NOT_COMPUTABLE`; retain case sensitivity and valid composed Unicode. Evidence-reference uniqueness and all prior eligibility arithmetic remain unchanged. Conservative rejection may require upstream ID normalization; no runtime integration is authorized.

## Independent evaluator, baseline and falsifier

The independent 16-fixture Python subprocess evaluator was authored and committed before the candidate. The frozen oracle contains 7 positive/regression cases and 9 new negative cases; the candidate did not modify it.

| Measurement | V2 | V3 |
|---|---:|---:|
| Expected outcomes | 7/16 | 16/16 |
| New ambiguous-ID negatives rejected | 0/9 | 9/9 |
| Positive and regression controls | 7/7 | 7/7 |
| Authenticated project-wide handoff census | Not available | Not available |

Negative fixtures include ASCII whitespace aliases, tab/newline, nonbreaking spaces, NFC/NFD aliases, zero-width format, embedded NUL, a single padded ID, and a single decomposed ID. **Falsifier:** if any of these is accepted, or if the valid case-sensitive/NFC positive controls fail, reject V3. The test is synthetic and evaluates only structural parsing and arithmetic.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_attempt_id_canonical_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_reference_uniqueness_guard_v2_20261101.py
# expected: exit 1, 7/16
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_attempt_id_canonical_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_attempt_id_canonical_guard_v3_20261101.py
# expected: exit 0, 16/16
```

## Exact isolated file bindings

- Frozen evaluator: 3,941 bytes; SHA-256 `54ed76d8ab929ef26068b50b137d79038f6bd7a0d1c833dd4a123fc37d0d2a7e`; Git blob `9c8b2a33f67bcc0dfb9a98640d2cb99a357c9cdc`.
- V3 candidate: 3,920 bytes; SHA-256 `297b26d3d2eb9164459ad3fa31333acd52fb0ed8c1f70e64f1241808b90fcd11`; Git blob `b79b70e92771700afba4f5c860471da09c2775ed`.
- V3 evaluator stdout: 2,391 bytes; SHA-256 `75958278e29741de950eb4ff9f8c0ab4fcb729fcd968bd26c44555e3e5b7745a`; Git blob `e30a2f8d222e124143f6f05be9286544d8dff569`.

## Scope and release boundary

`METRIC_READY_STRUCTURAL_ONLY` is **not** a real 90% automation measurement. The complete independently authenticated project-wide numerator and denominator remain `NOT_COMPUTABLE`. The guard does not authenticate GitHub actors, evidence contents, source completeness, receipts, or expert returns. R10 PR #115 has no newly authenticated independent expert receipt in the checked PR comments/reviews and Issue #93; owner-authored SEND remains separate. No new automation, external write slot, worker, Cursor/Hostinger/WWW change, evaluator auto-approval, or claim promotion is permitted.

Publication is conditional on PR/CI, exact immutable main readback, all file byte/SHA-256/blob matches and an append-only Issue #93 receipt. A branch or this report alone is not proof of main publication.
