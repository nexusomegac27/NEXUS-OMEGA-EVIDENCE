# NEXUS OMEGA · Alpha-Node · Independent Git-blob source anchor V9 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_INDEPENDENT_GIT_BLOB_ANCHOR_V9_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=c1aee5da5015e1108ceab049c7031180978c109d
MAIN_IMMEDIATE_PARENT=9e5110ce84f2bd63bad1882d80a7ee6a219b448d
PREDECESSOR_PR=280
PREDECESSOR_ISSUE93_RECEIPT=6565584811
FROZEN_EVALUATOR_FIRST_COMMIT=bc3085aeae6c4540421f1370e5cb3a584c03c3f6
CANDIDATE_FIRST_COMMIT=82bc7d8ce42fac930f6d1c314a971fee638257d6
CANDIDATE_PRE_PR_SYNTAX_REPAIR=7f8cc28165fb382933885ed01b7464365d2039d8
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The prior V8 source at pinned `main` was independently fetched: `alpha_handoff_coverage_state_source_binding_guard_v8_20261102.py`, 3,837 UTF-8/ASCII bytes, SHA-256 `6f95502177a7be45c8b655485505f949ee66589e8be823237e62a26229d742b8`, Git blob `30abeb0bf47bf53f96f8446ae6e3dfdc4128dd30`. V8 checks a caller-provided SHA-256 against caller-provided source bytes, but does not independently bind those bytes to the immutable GitHub commit/path/blob. Its report explicitly preserves this joint-forgery limitation. No predecessor was modified.

## NEGATIVE HYPOTHESIS / ONE CANDIDATE

A producer can replace source bytes and recompute the accompanying SHA-256; a SHA-only structural validator may accept this internally consistent forgery. V9 is a **separate research-only precheck** requiring a trusted immutable commit, repository path and Git blob SHA-1 obtained independently of the producer envelope. It computes the actual Git object ID as `SHA1(b"blob " + decimal_byte_length + b"\0" + raw_bytes)` and independently computes SHA-256. Both must match; missing, malformed, path-traversal and inconsistent values fail closed to `NOT_COMPUTABLE`.

This is not a GitHub API client, authentication oracle, SHA-1 collision resistance proof, event-census completeness proof, or productive V8 integration. The caller MUST obtain and pin the trusted reference independently, including checking that the GitHub path belongs to the intended commit. Merely copying the producer's claimed blob into `--trusted-blob` defeats the purpose.

## FROZEN EVALUATOR / INDEPENDENT TEST

The evaluator was committed first at `bc3085aeae6c4540421f1370e5cb3a584c03c3f6`, Git blob `62829fd646b004a3d7d8cc44df702a139a643b49`, local SHA-256 `1a9e2066c4efe7c4f3fccd46879b7221259f64019ba301687aa56600905f0508`. The candidate's final byte-identical version is Git blob `a2ba4c03cc824169c754c982bfe2b394e5258ef2`, local SHA-256 `e848bf157ac56ae75fcb978ca4180836da4bab1067916614873152118617e18f`. An initial one-character missing parenthesis in the unmerged candidate was corrected on the same branch before the PR; no bound source or `main` file was overwritten. The frozen evaluator remained unchanged.

Run `python frozen_alpha_handoff_git_blob_evaluator_v9_20261102.py alpha_handoff_independent_git_blob_guard_v9_20261102.py`. Sixteen subprocess cases: **16/16 expected outcomes**, including **15/15 negative/edge cases rejected** and **1/1 positive accepted**. Local stdout SHA-256 `43af2ec725c87fc552cb170496ea496f511f622edda25c39b3392edbce2d68a9`. This is a local independent frozen-fixture test, not external peer review or production evidence.

A second source-exact control used GitHub's immutable `main` `c1aee5da5015e1108ceab049c7031180978c109d`, `index/v1/latest.json`: **871 original bytes**, Git blob `4e957f463eda19734c1ab42c51bb4bb6cfa073d7`, SHA-256 `e186fec20065b9e774fc71bdbdc369f6e7ee8b40f48fb3ddc762e0ffd06b6961`. The independently fetched original passed the V9 cross-check. A changed `A0_LOCAL_STAGING` value with its SHA-256 recomputed to `ffaefe846f522daea2b63f8b53eca7b7fcd5979249edfde238b1aa74df48e449`, while retaining the independently pinned original Git blob, returned `NOT_COMPUTABLE`.

| Scoped measure | SHA-only baseline / V8 | V9 isolated |
|---|---|---|
| Jointly altered source bytes and claimed SHA-256 | Structurally unprotected (V8 source inspection; V8 runtime replay NOT_EXECUTED) | 1/1 independently anchored forgery rejected |
| Frozen V9 evaluator | Not applicable | 16/16 expected results |
| Real GitHub original byte control | Not tested against V8 here | 1/1 bound to independent Git blob |
| Authenticated project-wide handoff automation | NOT_COMPUTABLE | NOT_COMPUTABLE |

## FALSIFIER / LIMITATIONS / DECISION

A deliberately co-forged **trusted** Git blob argument, changed bytes and changed SHA-256 were accepted by V9 (`BOUND_C1_BYTES_ONLY`): this falsifies any stronger claim that the guard authenticates its own trusted reference. The result is only a byte-level cross-check against an independently supplied immutable Git object identity. GitHub REST authenticity, branch ancestry, actor authentication, exhaustive handoff event enumeration and source license/semantic validity remain separate gates. The 90% target numerator and denominator remain unavailable; synthetic cases are not eligible handoffs.

No existing GitHub ruleset, runtime, worker, Hostinger deployment, WWW artifact, external actor registry, GPT model or scientific claim ceiling was changed. Publication through the existing owner branch/PR/CI path is permitted only if checks pass; main and append-only Issue #93 receipt require separate post-merge readback.
