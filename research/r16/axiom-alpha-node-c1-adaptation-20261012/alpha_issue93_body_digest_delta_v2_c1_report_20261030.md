# AXIOM Alpha-Node — Issue #93 body-digest append-only delta V2 · 2026-10-30

```text
OBJECT=NEXUS_OMEGA_ALPHA_ISSUE93_BODY_DIGEST_DELTA_V2_20261030_R0
DECISION=KNOWLEDGE_APPEND_C1_SNAPSHOT_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=e726697213b2d637d42f2929c98a8c0f5f63a477
PREDECESSOR_PR=220
PREDECESSOR_ISSUE93_RECEIPT=6526826821
PREDECESSOR_DIGEST_SHA256=69787c3cf2e59401eb9ea52048f8c0f0ba4cf928040f1095a8b4c99986e0f4fb
PREDECESSOR_DIGEST_GIT_BLOB=a7e8314a9742c2eeb04e98f8ba02deddbd16e92c
ORACLE_FIRST_COMMIT=3c9dabea1ecae6769d432fd164c589b158491f9d
DELTA_SECOND_COMMIT=abf5162c21c34690b30570a7523d79db5422bea8
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL BYTES / NEGATIVE HYPOTHESIS

The pinned V1 inventory has 201 ordered body pins, cutoff ID 6516343927, SHA-256 69787c3cf2e59401eb9ea52048f8c0f0ba4cf928040f1095a8b4c99986e0f4fb, Git blob a7e8314a9742c2eeb04e98f8ba02deddbd16e92c. A fresh GitHub connector issue-comment census returned 210 ordered unique comments, all API-attributed to the owner, with last ID 6526826821. A second API census returned the same 210 IDs and order.

The V1 pins were independently compared to the first 201 API-returned comment-body strings using a standalone JavaScript SHA-256 implementation (tested on empty string and `abc` known vectors): **201/201 body SHA-256 and UTF-8 byte lengths MATCH**, 620299 bytes. Nine newer comment bodies add **28394 UTF-8 bytes**. Their nine SHA-256/byte pins are in the append-only V2 delta; no full body text is published. The newly covered cutoff total is **210/210**, 648693 UTF-8 body bytes. This is coverage of a specific issue snapshot, not a complete project handoff-attempt census.

Negative hypothesis: a fixed 201-row inventory can be mislabeled as covering the current 210-row issue, leaving nine newer receipt bodies outside the frozen provenance population. The V2 delta is anchored to the V1 SHA-256, blob, last ID, exact path and pinned main, rather than silently replacing V1.

## PINNED BASELINE / MEASURABLE DELTA

| Measurement at 210-comment cutoff | Before V2 | V2 candidate |
|---|---:|---:|
| Comment bodies with versioned digest pins | 201/210 | 210/210 |
| Unpinned newer comment bodies | 9 | 0 at cutoff |
| Previously pinned body mismatches on fresh API read | 0/201 | 0/201 |
| Newly pinned body bytes | 0 | 28394 |
| Authenticated independent actor | NOT_ESTABLISHED | NOT_ESTABLISHED |
| Project-wide eligible handoff denominator | UNKNOWN | UNKNOWN |

The nine rows have IDs 6517745738 through 6526826821 and strictly increase. The V1 source remains unmodified. Any later Issue #93 receipt necessarily lies **after** the V2 snapshot cutoff and must not be counted as V2-covered.

## ISOLATED EVALUATION / FALSIFIER

A separate Python structural oracle was written and executed **before** publication of the candidate delta, then committed first as `alpha_issue93_digest_delta_v2_oracle_20261030.py`. It does not import the candidate, query GitHub, or authenticate the source. The oracle accepted the positive V2 data and rejected **17/17** negative/malformed fixtures: wrong repository, commit, predecessor digest/blob/path, missing or reordered/duplicate IDs, invalid digest/bytes, boolean byte count, wrong census/last ID, extra authentication claim, wrong historical cutoff, duplicate JSON keys and NaN. **18/18 PASS** in a local Python execution. It is an independently separated test implementation, not independent external third-party review.

Falsifier: any of the 201 previously pinned bodies changing while retaining the same V1 pins, or any of the nine new bodies changing while retaining V2 pins, must be detected on a fresh body-to-pin comparison. A missing/reordered ID or an altered predecessor binding must fail the structural oracle. Joint modification of body and pins or compromised API origin is not prevented by these checks. The Python oracle alone does not verify actual body hashes; the JS byte comparison and Python structural oracle are distinct evidence layers.

## MATERIAL IDENTITIES / REPRODUCTION

- Frozen oracle: 4574 UTF-8 bytes; SHA-256 `183d31d0a904d7ac2f348699d91395c497dbe91626096a89dd43c9c3f0d6d610`; Git blob `2a3e84d42c2c9aa98fe6f92f11eab01fc0103fac`.
- Delta JSON: 1897 UTF-8 bytes; SHA-256 `e83aa5f19d1882e56291ab21bb4685710d57fd5809f7b90fc6d2079f7d44079f`; Git blob `0f6d5f73f8b219d39f31e03b12cc555866b01d23`.
- Reproduce structural tests from this directory: `python alpha_issue93_digest_delta_v2_oracle_20261030.py alpha_issue93_body_digest_delta_v2_20261030.json`.
- Original comment text is not in the repository delta. Reproduction of actual body hashes requires a fresh paginated API read and comparison to the fixed V1 and V2 pins. A GitHub API response is not an independently authenticated cryptographic witness.

## PASSIVE R10 / GOVERNANCE

R10 PR #115 remains OPEN at observation, with head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, no submitted reviews, no review threads and no independent PR conversation return. The pinned original manifest was fetched from `539d4bb33d2ba2c4895713c1bc437ece0743eeea`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. The owner-mediated expert ACK claim remains unauthenticated; the external actor registry allowlist is empty. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED; SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

No new scheduler, worker, transport, Cursor dispatch, R10 merge, external actor registration, secrets, original-source overwrite, Hostinger/WWW write, model change, production integration or claim promotion. `AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE` because the complete authenticated eligible-attempt denominator is unknown. The V2 data is a C1 provenance snapshot, not a scientific or automation performance claim.

## PUBLICATION GATE

This report records a pre-PR candidate. PR/CI/merge, actual immutable main readback and append-only Issue #93 receipt must be verified separately. `MAIN_PUBLISHED=NOT_YET_ESTABLISHED` at report authoring.
