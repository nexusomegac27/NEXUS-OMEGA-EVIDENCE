# AXIOM Alpha-Node — GitHub handoff source URL scope guard V1 · 2026-10-30

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_SOURCE_URL_SCOPE_GUARD_V1_20261030_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=8ceb184409c15c95ecdcf314e6209fb41bfed9bf
PREDECESSOR_PR=219
PREDECESSOR_ISSUE93_RECEIPT=6525110654
SOURCE_V1=research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_attempt_denominator_v1_20261030.py
SOURCE_V1_GIT_BLOB=9aa7501579db9e1cc1ef64648df10e8e20a7fa07
R10_PR115=OPEN_NOT_MERGED_AT_OBSERVATION
EXTERNAL_ACTOR_ALLOWLIST=EMPTY_AT_OBSERVATION
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL SOURCE / NEGATIVE HYPOTHESIS

The original V1 handoff denominator reducer was retrieved from the pinned main GitHub source and checked by Git blob ID. Its `source_ref` check accepts any string beginning with `https://github.com/` and does not bind the repository, resource kind or blob ref to `source_commit`. This is a **source-scope validation weakness**, not a demonstrated GitHub compromise or a proven manipulation of actual receipts.

Counterexample: `https://github.com/other/NEXUS-OMEGA-EVIDENCE/issues/93` passes the original prefix condition while pointing outside the governed repository. An unrelated `blob/main/...` URL also passes V1 although the row separately supplies a pinned `source_commit`. The narrower negative hypothesis is that a source-ref string may be syntactically accepted without being a canonical repository-scoped locator. Domain-spoof URLs like `github.com.evil.invalid` do **not** pass V1's exact `https://github.com/` prefix and are not claimed as a demonstrated V1 bypass.

## PINNED BASELINE / ISOLATED CANDIDATE

Baseline: one independently specified wrong-repository URL is accepted by V1's observable prefix predicate (1/1), while the original denominator evaluator contains no repository-scope negative fixture. The V1 reducer's project-wide rate remains `NOT_COMPUTABLE` because source URLs and attempt completeness are unauthenticated.

The new `alpha_handoff_source_url_guard_v1_20261030.py` is a separate **research-only preflight**, not an in-place modification of the V1 reducer. It requires exact `https://github.com` origin and exact `nexusomegac27/NEXUS-OMEGA-EVIDENCE` path, no query/userinfo/port/percent escapes/dot segments, and a restricted issue/PR/commit/immutable-blob locator. For a blob, the URL's commit must equal the independently supplied `source_commit`. It never fetches or authenticates the target resource. This restrictive syntax policy is a candidate for evaluation, not a newly imposed project-wide rule.

## INDEPENDENT TEST / FALSIFIER

The black-box evaluator `frozen_alpha_handoff_source_url_oracle_v1_20261030.py` invokes the candidate in a separate Python `-S` subprocess and does not import candidate code. It was versioned in a separate first commit before candidate publication. The local run produced **24/24 PASS**, consisting of **5/5 valid** and **19/19 negative** cases. Negatives include wrong repository, spoofed hostname, userinfo, wrong scheme, URL query/fragment, dot-segment traversal, encoded segments, noncanonical slashes, mutable blob branch, mismatched blob SHA, malformed issue ID, invalid commit SHA, control characters and noncanonical port. The original V1 wrong-repository prefix acceptance was separately asserted.

**Falsifier:** if a wrong-repository or mutable-branch blob reference passes the candidate, or a canonical pinned issue/PR/commit/blob URL fails, the proposed improvement is invalid. A future valid GitHub URL type rejected by this deliberately restrictive allowlist is also a counterexample to generalizing it without explicit scope review.

| Comparable local measurement | V1 prefix predicate | Isolated guard |
|---|---:|---:|
| Wrong-repository counterexample accepted | 1/1 | 0/1 |
| Black-box valid controls | not in V1 URL-specific oracle | 5/5 PASS |
| Black-box negative controls | not in V1 URL-specific oracle | 19/19 FAIL_CLOSED |
| Independently authenticated source bytes | NO | NO |
| Project-wide handoff attempt denominator | UNKNOWN | UNKNOWN |

## BOUNDARIES / PUBLICATION

The guard validates **URL syntax and repository scope only**. A syntactically canonical URL may still be nonexistent, edited, inaccessible, untrusted, owner-authored, semantically false or unrelated to a verified handoff. The candidate does not establish actor authentication, independent receiver ACK, R10 scientific execution, automatic operator-free handoff, publication readback or any project-wide success rate. No new scheduler, worker, CI, root, runtime, Hostinger/WWW action, evaluator override, external registration or claim promotion. Existing original files remain unchanged.

Before publication: `PR=NOT_YET_PUBLISHED`, `MAIN_READBACK=NOT_YET_PERFORMED`, `ISSUE93_RECEIPT=NOT_YET_POSTED`. A later append-only Issue #93 receipt must bind actual merge/main/CI and per-file byte/hash readback; this report must not be treated as that receipt.
