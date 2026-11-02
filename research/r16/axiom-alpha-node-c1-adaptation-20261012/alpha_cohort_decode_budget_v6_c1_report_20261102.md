# NEXUS OMEGA · AXIOM Alpha-Node · V6 bounded predecode source guard · 2026-11-02 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_COHORT_PREDECODE_BUDGET_GUARD_V6_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_BRANCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=7ff9e7293c9f825716333ddbfd1a5227b2e6aa3f
PREDECESSOR_PR=288
PREDECESSOR_ISSUE93_RECEIPT=6573619590
FROZEN_EVALUATOR_FIRST_COMMIT=89dc7552ddff4abd7c57d14eb0f8c06f2af66037
CANDIDATE_SECOND_COMMIT=0bc6656c21ea336b504f8927fc1fa4bb0833dc95
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The GitHub branch `main` was read at exact commit `7ff9e7293c9f825716333ddbfd1a5227b2e6aa3f`, parent `2fbce469dc8c66d33a4be14eacb97bac3b02b938`. The immediately preceding owner-merged PR #288 and its Issue #93 receipt #6573619590 were physically retrieved. Source V5 was independently reconstructed from immutable GitHub text: **4,754 UTF-8 bytes**, SHA-256 `1c74eb1105d99e5e02b0c2bc049b92b771e270c215404c37760a1eeb2117a236`, Git blob `656cfc0ae9bcba2f9bece850aeea4bb60fe40bfc`. The historical cohort manifest remains pinned to SHA-256 `8f835b1dd27472702ee0aad0e2c5c5fc3e9d467d4d7423518ba3cb4c41e3191c`. This is an isolated C1 research lane, not a runtime or production modification.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

V5 decodes caller-supplied base64 before checking decoded byte length. A record claiming 9 source bytes but carrying 1,600,000 base64 characters is rejected eventually, **after one unnecessary base64 decode**. This creates avoidable transient CPU/allocation cost; it is not evidence of a real-world attack. The V5 baseline was executed against the independent, predeclared V6 oracle: **11/12 expected outcomes**; the one failing case returned `FAIL_CLOSED` but made **1 decode call** instead of the required 0.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The separate evaluator was committed first at `89dc7552ddff4abd7c57d14eb0f8c06f2af66037`, **3,452 bytes**, SHA-256 `d5ef4cec2015325366280dbc1d71625b9a0252fda2e8001b5976301014b7a32a`, Git blob `1430d6e5eede18aee5de068816ff61a8a202fec3`. The evaluator was not edited after the candidate was authored. V6 was committed second at `0bc6656c21ea336b504f8927fc1fa4bb0833dc95`, **5,400 bytes**, SHA-256 `517c2fc20b43d1d31fc9225bf3422c794555760a9d6ea223e7e91385717bf7a6`, Git blob `7c852a89e79f2958c98afa52cb9bb99114ddb55b`.

V6 checks exact expected canonical base64 length and string/blob type **before** decoding, and rejects a manifest with more than 8 MiB of aggregate declared source bytes. It does not claim to limit memory already allocated by the caller for input strings. The frozen evaluator executed against the actual Python V5 and V6 sources in isolated local runs:

| Fixed test metric | V5 | V6 |
|---|---:|---:|
| Expected cases | 11/12 | **12/12** |
| Oversized 1,600,000-character input: base64 decoder calls | 1 | **0** |
| Outcome of oversized input | FAIL_CLOSED | FAIL_CLOSED |
| Source-byte audit of 36 real files in this run | NOT_EXECUTED | NOT_EXECUTED |
| New verified automated handoffs | 0 established | 0 established |

V5 stdout SHA-256 `41c19a9cf9d2de6ae1f146b9b73074b2f70f84453ca099d9a6676c33887b28cb`; V6 stdout SHA-256 `5c5394bf525401859368f03d65b7aed993c5fa904d3d09a804b3e3a04e98dfbd`. These stdout hashes are local measurements, **not** independently GitHub-archived execution receipts. The frozen oracle's case labeled `coforged_anchor_falsifier` uses an ordinary valid synthetic source, so it must **not** be cited as a genuine co-forgery test. A separate explicit counterexample was executed: a fully co-forged manifest, payload, Git blob and caller-supplied trusted SHA-256 returned `PASS`. This is the actual trust-anchor falsifier and is separate from the 12/12 oracle count.

Reproduce (Python 3) from this existing R16 research directory:

```bash
python frozen_alpha_cohort_decode_budget_evaluator_v6_20261102.py alpha_cohort_original_bytes_guard_v5_20261102.py  # expected 11/12, exit 1
python frozen_alpha_cohort_decode_budget_evaluator_v6_20261102.py alpha_cohort_decode_budget_guard_v6_20261102.py   # expected 12/12, exit 0
```

## DECISION / CLAIM LIMIT

`TESTED_IMPROVEMENT_C1_ISOLATED` is limited to eliminating one unnecessary decode operation for one adversarial fixture while preserving expected source checks. V6 does **not** authenticate GitHub, the actor, the manifest anchor, scientific claims, or the provenance of source bytes. No real GitHub HTTPS E2E of the new Python code was executed. The provider and caller can still jointly forge a self-consistent record; an external independent anchor remains necessary. The 90% automation objective and project-wide publication-readback denominator remain `NOT_COMPUTABLE`; synthetic tests are not handoffs. No new pipeline, worker, runtime, Hostinger, Cursor dispatch, R10 merge, source overwrite, or C2 promotion.

R10 passive readback (not a second candidate): PR #115 remains OPEN at owner head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; original SEND head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`. PR review and discussion contain no independently authenticated expert ACK. Owner-mediated return files exist; their mere presence is not independent expert execution or scientific adjudication. `SOURCE_NOT_PRESENT` applies only to an **independent authenticated return**, not to the owner-mediated texts.

This report was authored on a branch before CI and merge. CI, any merge, exact `main` readback and Issue #93 append-only receipt must be established separately; they are not assumed here.
