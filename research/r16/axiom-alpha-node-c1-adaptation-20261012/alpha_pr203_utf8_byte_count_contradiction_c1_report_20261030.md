# AXIOM Alpha-Node — PR #203 UTF-8 byte-count receipt contradiction · 2026-10-30

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_PR203_UTF8_BYTE_COUNT_CONTRADICTION_20261030_R0
DECISION = CONTRADICTION_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 91b0a6d800bce25208c1137fb087c25e1846e089
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/203
PREDECESSOR_ISSUE93_RECEIPT = 6509926493
HISTORICAL_SOURCE_REWRITE = NO
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Source-exact observation and provenance

On 2026-10-30, the owner-authenticated GitHub connector returned the current `main` at the pinned SHA above, the merged PR #203 at that same merge SHA, the unchanged historical Issue #93 receipt `6509926493`, and three file objects at the pinned commit. The source report was retrieved as UTF-8 text and independently re-encoded to bytes; a separate GitHub contents directory response reported the same physical byte count. A separate SHA-256 implementation (JavaScript) independently hashed the fetched UTF-8 bytes; GitHub provided the Git blob SHA-1. This is **source-identity checking**, not scientific validation.

| File at pinned main (under `research/r16/axiom-alpha-node-c1-adaptation-20261012/`) | Receipt byte count | Actual UTF-8 bytes | Independently computed SHA-256 | Git blob SHA-1 | Byte-count result |
|---|---:|---:|---|---|---|
| `alpha_handoff_denominator_guard_v3_20261029.py` | 5664 | 5664 | `5fc12dbf825e9b0ab0057e393bc6a644512e8ffce9bf04a239b5385c445c7f1c` | `407b6eea176d23a6d8cdbe8a4b9d19cf9db23638` | MATCH |
| `frozen_handoff_safety_qualified_oracle_v3_20261029.py` | 5775 | 5775 | `b143a3f6c9d4adacc0947b57b2b94b65939b1601378a5932014b15e7e7944c2f` | `ba2484285c0f07e492d66013e266a21911682192` | MATCH |
| `alpha_handoff_safety_qualified_v3_c1_report_20261029.md` | **6078** | **6081** | `bdb5c95d4b3ba6acd033ba18dec1dcf49556fc47e19e8f3e8e7a513608a85ee7` | `e07bbc9f199cd50d36a561e50c3f22c6fc8efec2` | **MISMATCH (+3 bytes)** |

The actual report is 6,078 JavaScript UTF-16 code units and 6,081 UTF-8 bytes. The receipt field `REPORT_BYTES=6078` equals the character/code-unit count, not the physical UTF-8 count. A character-versus-byte confusion is a **plausible explanation**, not an established reconstruction of the historical producer's algorithm. The report file itself and its Git blob remain unchanged; the discrepancy is in **receipt metadata**. The historical `MAIN_FILE_BLOB_READBACK=3/3_MATCH` is a blob claim and does not itself assert three correct receipt byte counts. Do not rewrite that historical receipt.

## Negative hypothesis, independent evaluator, and falsifier

**Negative hypothesis:** A receiver that checks `len(decoded_text)` rather than the byte length can accept a false physical size for non-ASCII UTF-8 files. For a synthetic 6,078-character fixture consisting of 6,076 ASCII `a` characters followed by U+2014 and U+00B7, the naive count is 6,078 while UTF-8 contains **6,081 bytes**. A correct byte-bound witness must reject `bytes=6078` and accept `bytes=6081` only when the SHA-256 and Git-blob IDs also match.

The independent, **pre-existing** witness `alpha_receipt_file_digest_witness_v1_20261028.py` was retrieved at the pinned main and locally reconstructed with **4,899 bytes** and matching Git blob `5523bea43be23d96b37432b7147183818ab58c81` before the synthetic evaluation. It is an unchanged earlier oracle, not candidate-controlled acceptance logic. The new frozen regression evaluator `frozen_alpha_receipt_utf8_byte_count_oracle_v1_20261030.py` runs this witness in separate Python subprocesses.

- Local isolated evaluation: **12/12 PASS**, covering ASCII and Unicode positive controls, character-count false acceptance, incorrect byte count, same-length content mutation, SHA-256 mismatch, Git-blob mismatch, duplicate JSON key, invalid Base64, Boolean size, non-additive status, and missing original bytes.
- The key negative fixture returns `FAIL_CLOSED: BYTE_COUNT_MISMATCH` for claimed 6,078 bytes. The corrected 6,081-byte fixture returns `PASS_CALLER_SUPPLIED_FILE_BYTES_C1`.
- **Falsifier:** The pinned report's actual bytes equal 6,078; the independent hash differs from the recorded report digest; the unchanged prior witness accepts the false 6,078-byte claim; or the same fixture with the correct 6,081-byte count and matching digests fails.
- Regression evaluator: 4,599 UTF-8 bytes, SHA-256 `fa611e49524a5991247665eb0113046048d5064864eb20699a22f4e5099efcf6`, Git blob `09a17464a0f9865426d5b4020818ccf7153b1400` (local prepublication values, requiring GitHub readback).

The **real GitHub source** was independently measured through connected GitHub reads and a JavaScript SHA-256 implementation; the **isolated Python witness** was executed against synthetic fixtures, not a full local GitHub checkout. This separation must not be obscured.

## Bounded before/after metric and decision

Before this iteration, the latest Issue #93 receipt reported all three PR #203 file byte fields without a recorded mismatch. Source-exact rechecking identifies **1 mismatch among 3** receipt byte fields: **2/3 MATCH**, not 3/3. After applying the already versioned byte-count witness to the synthetic negative fixture, the false character-count claim is rejected **1/1** and the corrected count is accepted **1/1**. This is a test of a pre-existing safeguard and a correction to the evidence ledger, **not** proof of a new production integration or an increase in project automation.

The correction is append-only: `REPORT_BYTES_CORRECTED=6081`, `REPORT_SHA256=bdb5c95d4b3ba6acd033ba18dec1dcf49556fc47e19e8f3e8e7a513608a85ee7`, `REPORT_GIT_BLOB=e07bbc9f199cd50d36a561e50c3f22c6fc8efec2`, with `SUPERSEDES_RECEIPT_BYTE_FIELD=6509926493:REPORT_BYTES`. Preserve the original receipt and original report. The future receipt writer should use raw byte length and reject a discrepancy before claiming byte-complete readback; that integration is **not** performed here.

## Limits and R10 passive lane

`PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. The full authorized handoff population and failed-attempt denominator are not independently authenticated. The bounded 2/3 ratio is **receipt metadata accuracy for PR #203**, not a project-wide rate. No unauthorized write, source overwrite, actual safety breach, or scientific claim promotion follows from this metadata mismatch.

R10 PR #115 remains open, with no independent receiver comments, review submissions or review threads in the checked GitHub sources. The pinned R10 detached manifest at commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was independently measured at 4,588 UTF-8 bytes and SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc` (MATCH). `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. No external actor registration, Cursor dispatch, Hostinger write, biological experiment, new worker or R10 merge.

`BLOCKED_LANE != BLOCKED_SYSTEM`; `DRIFT_RESET=NON_DESTRUCTIVE`; `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`.
