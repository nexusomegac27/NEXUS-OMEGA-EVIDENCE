# NEXUS OMEGA · AXIOM Alpha-Node R10 raw-resource binding · 2026-10-19

OBJECT = NEXUS_OMEGA_ALPHA_R10_RAW_RESOURCE_TYPE_BINDING_20261019_R0
STATE = TESTED_IMPROVEMENT_ISOLATED_C1
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR_BRANCH_COMMIT = 6fda0910e4702edce884f9d827fde2266fc938d5
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## One falsifiable quality improvement

The previous isolated issue-comment guard trusts a caller-supplied `is_pull_request` Boolean, rather than deriving PR-versus-issue classification from the raw GitHub Issues API resource's `pull_request` field. A faulty normalizer can forge the Boolean. This is a synthetic input-integrity defect, NOT evidence of a forged real expert receipt.

An isolated new guard derives type from the raw Issues API object, binds `resource.url`, `resource.html_url`, `pull_request.url` and `pull_request.html_url`, and checks the comment parent, API comment ID, permalink, and numeric actor ID. This is a structural check only: the caller must independently fetch the source-exact REST objects.

## Frozen evaluator and falsification

Independent 26-case Python oracle was written and hashed before the candidate implementation.

| Subject | Pass | Total |
| --- | ---: | ---: |
| Original guard with legacy normalization adapter | 14 | 26 |
| Isolated raw-resource candidate | 26 | 26 |
| Deliberate hint-trusting mutant | 23 | 26 |
| Original guard on its historical frozen suite | 22 | 22 |

Three mutant non-passing cases include both contradictory type hints and malformed PR metadata. The old frozen oracle was not changed. A separately implemented JS readback of actual GitHub REST Issue #93/comment 6111816879 and PR #122/comment 6251483782 checked 16/16 metadata relationships. The full raw live HTTP response bytes were not archived; no atomic snapshot or external third-party validation is claimed.

Candidate Python: 3014 bytes; SHA-256 `8c7a2923bad7d17c50f77f482f9e6125c0c1cd2f84bf7f5f9f50271fc107f2a8`.
Frozen evaluator: 5378 bytes; SHA-256 `f0cde9236dbbc54b9c00f99978936f1e169aa2001123b1b2d61e1810e213f2b5`.
Legacy comparator adapter: 945 bytes; SHA-256 `4ee09d41d255e11a7a05b3b826876f0d0d1a32a85417cd959211e3b920d8c2f6`.

FALSIFIER = A legitimate, independently sourced GitHub REST issue-comment object whose canonical resource and permalink relationship contradicts the candidate rule.

## Publication and authority boundary

R10 pinned manifest at commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` remains Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; the previously verified SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc` was not independently recomputed in this iteration.

INDEPENDENT_RECEIVER_ACK = SOURCE_NOT_PRESENT_AUTHENTICATED
EXPERT_RESEARCH_ACTUALLY_EXECUTED = NOT_ESTABLISHED
EXTERNAL_ACTOR_ALLOWLIST = EMPTY
INTEGRATION = HOLD_SCOPED_FULL_REPOSITORY_REGRESSION_NOT_EXECUTED
PRODUCTION_RUNTIME_WRITE = NO
HOSTINGER_WRITE = NO
MAIN_MERGE = NO
CLAIM_PROMOTION = NO

This append-only C1 research note does not change the existing oracles, authorization, or source-bound historical paths.
