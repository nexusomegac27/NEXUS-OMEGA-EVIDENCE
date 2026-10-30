# AXIOM Alpha-Node — isolated original-source byte proof V1 (2026-10-30)

OBJECT=NEXUS_OMEGA_ALPHA_SOURCE_BYTE_PROOF_V1_20261030_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=167cd7672f701bf27b67f147568ce9cee00a2d59
PREDECESSOR_PR=225
PREDECESSOR_ISSUE93_RECEIPT=6534225691
FROZEN_INDEPENDENT_ORACLE_FIRST_COMMIT=dd237e4d1ecaa11cf7c09a86b98c989b182c755a
CANDIDATE_SECOND_COMMIT=71e221fe2ed31126259a6d910fe6ffdfce9362f0

## Original bytes and negative hypothesis

Actual public original: research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py at pinned main above. GitHub returned 1452 UTF-8 bytes and Git blob 73ef222f9117f566930390e60899d571ecc77402. Independent local byte rehash: SHA-256 425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3; git hash-object --stdin independently matched the blob. Existing source URL guard: 2954 bytes, SHA-256 92fe99e09228096c976bb33537fac30d615842a5881f9023ca6c885b5007c1e2, Git blob 2b5011a574f1a24fedca98e9817381760abe68af.

NEGATIVE_HYPOTHESIS: a syntactically valid GitHub blob URL and source_commit can be paired with silently modified locally accessible bytes. The existing alpha_handoff_source_url_guard_v1_20261030.py accepts the URL without examining file bytes. The new isolated preflight must reject a same-length mutation without altering any historical source.

## One candidate and independent frozen evaluator

The candidate alpha-source-byte-proof-v1-20261030.py requires a canonical immutable same-repository GitHub blob URL, matching source_commit and relative path, exact local byte count, SHA-256 and recomputed Git blob SHA-1. It rejects malformed/duplicate-key/nonfinite JSON, foreign repositories, traversal, symlinks, oversized inputs, wrong claim ceiling and mismatched bytes. No network requests, runtime writes or actor registration. The separate evaluator was committed first, imports no candidate code, invokes the candidate in a Python -S subprocess and uses git hash-object as a second Git-blob computation.

FROZEN_ORACLE_BYTES=4843
FROZEN_ORACLE_SHA256=21b5e1444045f20638e3689e97038f1934819532b21298433e2f403c2679ede9
CANDIDATE_BYTES=4368
CANDIDATE_SHA256=5584b4c2c6c2f6d2f5cb5a4b3e9919a69e8772c2fd0305f97a4862b426d77cc8

| Fixed measurement | Old syntax guard | New byte proof |
|---|---:|---:|
| Valid canonical locator | 1/1 accepted | 1/1 accepted with matching bytes |
| Same-length source mutation rejected | 0/1 (not examined) | 1/1 |
| Frozen independent black-box checks | N/A | 23/23 PASS |
| Negative and malformed cases | N/A | 21/21 FAIL_CLOSED |
| Real source SHA-256 and independent Git blob | Not checked | 1/1 MATCH |
| Commit-tree membership | NOT_VERIFIED | NOT_VERIFIED |
| GitHub transport authentication | NOT_VERIFIED | NOT_VERIFIED |
| Project-wide handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

FALSIFIER: a same-length mutated source passes; an intact pinned source fails; symlink/path escape or a false hash/blob/commit passes; or the output claims remote authenticity, commit-tree membership or project-wide coverage.

Reproduce from the root of a checkout containing the pinned original:
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen-alpha-source-byte-proof-oracle-v1-20261030.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha-source-byte-proof-v1-20261030.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_source_url_guard_v1_20261030.py .

## Authority and R10 passive observation

Research-scoped, reversible and additive. Historical source, evaluator after freeze, repository policy, external actor registry, branch rules, productive runtime, Hostinger and WWW are unchanged. No new automation, pipeline root, external worker, independent oracle promotion or claim promotion. PR/CI and immutable main byte/hash/blob readback must pass before any publication-success statement; append an Issue #93 receipt only afterward.

R10 PR #115 observed OPEN at API head dab7c59070d67e7e2a244bd6d05db9a4d37460e3. Its detached manifest at immutable 539d4bb33d2ba2c4895713c1bc437ece0743eeea was GitHub-retrievable as blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df. All 215 observed Issue #93 comments were owner-authored; PR #115 had 0 comments, 0 reviews and 0 review threads. No new independent expert return. Manifest SHA-256 was not separately recalculated in this iteration.

PUBLIC_SEND=OBSERVED
INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED
AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED
AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED
EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE
PROJECT_ZERO_VIOLATION_CLAIM=NOT_ESTABLISHED
WWW_PARITY=NOT_ESTABLISHED
