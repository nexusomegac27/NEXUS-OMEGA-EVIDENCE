# AXIOM Alpha-Node · Variable additive-file receipt-chain audit · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_CHAIN_VARIABLE_INVENTORY_20261028_R0
DECISION=TESTED_C1_ISOLATED_CANDIDATE_PENDING_MAIN_READBACK
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=c0f69e9fcd2ff54243ffa1bf3aa9d90ce2bda62d
PINNED_MAIN_PARENT=a56c7a8eb4d922df543b534d7d90a5c0ada5bf3a
PREDECESSOR_ISSUE93_RECEIPT=6472047244
FROZEN_EVALUATOR_FIRST_COMMIT=5fdc3ca63729906962f069f78143545a0435607c
CANDIDATE_SECOND_COMMIT=9bfa1811088c9cb16d87f1ecf639bd54728d390e
REAL_FIXTURE_THIRD_COMMIT=8efa9550442994ace02dd8decd68c93482abfc2c
PRODUCTION_INTEGRATION=NO
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_READBACK_RATE=NOT_COMPUTABLE
```

## One bounded source-exact contradiction and successor

The pinned V1 reconciler at `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_receipt_chain_reconciler_v1_20261028.py` is 4,797 bytes, SHA-256 `b38125d20729cad52a0c40a59589dafe144ef80ccc620f734974a2aea16729ba`, Git blob `f7614d8a134066bf74f52544342bd7e03f31a7a3`. It requires `(ahead,behind,files_added,files_modified,files_deleted)==(1,0,3,0,0)` for *every* record. This is correct for its explicitly scoped nine-PR sample #164–#172 but cannot represent the immediate next legitimate public PR #173, which added four files. This is a **scope/extension limitation**, not a historical failure or a false claim about the original nine.

GitHub API readback at pinned main `c0f69e9fcd2ff54243ffa1bf3aa9d90ce2bda62d` establishes PR #173 merged at that commit, parent `a56c7a8eb4d922df543b534d7d90a5c0ada5bf3a`, compare ahead=1 behind=0, four added files, no modified/deleted files. Issue #93 receipt `6472047244` is owner-authored, points to the same main and predecessor receipt `6470285817`. Four exact file paths and statuses were retrieved from `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pulls/173/files`. These are observed API metadata, not cryptographically signed raw JSON retained in the fixture.

**Negative hypothesis:** hardcoding a three-file compare tuple falsely excludes a valid four-file PR, while merely relaxing the count without checking the inventory permits fabricated count claims. **Falsifier:** a legitimate four-file record must pass; a missing inventory entry, inflated compare count, duplicate path, modification, path traversal or broken predecessor must fail closed.

## Isolated V2 candidate and independent oracle

The frozen subprocess oracle was committed first at `5fdc3ca63729906962f069f78143545a0435607c`, before candidate commit `9bfa1811088c9cb16d87f1ecf639bd54728d390e`. The oracle imports no candidate code. Local Python execution yielded **16/16 PASS**, including a synthetic 3+4-file positive case, a one-PR four-file positive case, and 14 negative/format checks. The real API-derived PR #173 fixture returned `records_checked=1, files_checked=4, metadata_chain_match=1/1`; mutating only `files_added` from 4 to 3 returned exit 2 `FAIL_CLOSED: COMPARE_INVENTORY_MISMATCH`.

V2 checks `files_added==len(files)`, all file statuses `added`, unique safe paths inside the existing R16 research directory, exact predecessor receipt and main hash chain, no modifications/deletions, strict JSON key/number types and bounded input. It preserves V1 unchanged and is **not a productive Steward integration**.

| Scope metric | V1 | V2 isolated |
|---|---|---|
| Four-file PR #173 representable | 0/1 | 1/1 |
| PR #173 four added paths cross-checked against API | not representable | 4/4 in caller-supplied fixture |
| Frozen black-box oracle | not applicable to V1 schema | 16/16 local PASS |
| Injected mismatch (four files vs three declared) | rejects all four-file records by fixed contract | rejects contradictory inventory |
| Project-wide eligible handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

## Reproduction and evidence limits

From `research/r16/axiom-alpha-node-c1-adaptation-20261012/`:

```bash
python frozen_receipt_chain_variable_inventory_oracle_v2_20261028.py -v
python alpha_receipt_chain_reconciler_v2_20261028.py < alpha_receipt_chain_pr173_observed_fixture_v2_20261028.json
```

The offline candidate does **not** authenticate its caller-supplied API fixture or verify PR file bytes, actor identity, CI, or scientific truth. An internally consistent forged input can pass. The evaluator is separately frozen and executed locally, but **external independent third-party validation is NOT_ESTABLISHED**. Neither 90% project automation nor 100% project-wide readback is measurable from this sample. This work adds no runtime, Hostinger, WWW, actor registration, worker, external transport, claim promotion or change to existing source paths. Public branch/PR publication and immutable main/Issue #93 receipt readback are separate gates, not preclaimed here.
