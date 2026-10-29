# AXIOM Alpha-Node — Markdown-fenced Issue #93 receipt guard V2 · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_FENCED_RECEIPT_GUARD_20261029_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 05748765ab35d87d6bfa79377a97d7c0ff2c2807
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/184
PREDECESSOR_ISSUE93_RECEIPT = 6485768210
SCOPE = OFFLINE_CALLER_SUPPLIED_ISSUE93_RECEIPT_PROJECTION
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## Original bytes and falsification

The exact V1 source at `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_exact_key_receipt_census_v1_20261029.py` was read from immutable main: 5,622 bytes; SHA-256 `4325bb9cbc440f205ee26bb3c879e8cdd689ebfd5415adc20feb9f45be30eb1c`; Git blob `68655fd9c5d36fe562b15d3f5ddf29fcd372c145`. An exact-byte local copy was reconstructed and its SHA-256 and Git blob independently matched before executing it. V1's `fields()` scans every text line for `PR=`, `ACTUAL_MAIN_READBACK=` and `CLAIM_CEILING=`, including lines inside Markdown fenced examples. A forged receipt consisting only of a fenced example can therefore be accepted as a current PR receipt when other caller-supplied fields agree. This is a synthetic demonstrated parser vulnerability, **not** evidence that an actual GitHub receipt was forged.

Negative hypothesis: exact-key matching alone prevents all attribution errors. Falsifier: a Markdown code fence containing an otherwise well-formed receipt. V1 accepted this negative fixture. V2 ignores triple-backtick, tilde and up-to-three-space-indented fenced content, preserving exact-key semantics outside fences. An unclosed fence fails closed. V1 remains unchanged; V2 is an isolated additive wrapper, not a production patch.

## Frozen independent test

The subprocess oracle `frozen_issue93_fence_oracle_v2_20261029.py` was committed **first** on the owner branch, before the V2 candidate. The oracle does not import the candidate and checks output/exit codes on 15 synthetic positive, negative and regression fixtures. Linux/Python 3.13 isolated execution:

- Original V1, exact-byte source: **8/15 PASS**, seven expected failures, including three accepted forged fenced receipts and failures on fenced duplicate fields.
- V2 candidate: **15/15 PASS** on the identical frozen oracle; no oracle changes after candidate creation.
- V2 bytes: 1,769; SHA-256 `05330dc41414bad319539a8dd25f0e995a726527237f55b19c58c792e8955b91`; Git blob `e34cd65069c3f0fb3bf071aac7889a109b0be7bc`.
- Oracle bytes: 4,859; SHA-256 `31874f93e77b8024843930dff7623cde666325f15fff8dffba08162682c5799b`; Git blob `1d1b6bb0f96213f14f44083be13780d2d9b7f017`.

Reproduce from a checkout of the candidate branch:

```bash
cd research/r16/axiom-alpha-node-c1-adaptation-20261012
python frozen_issue93_fence_oracle_v2_20261029.py -q
AXIOM_CANDIDATE=alpha_issue93_exact_key_receipt_census_v1_20261029.py python frozen_issue93_fence_oracle_v2_20261029.py -q
```

## Real API control and limits

The connected GitHub API returned **175 Issue #93 comments**. A separate read-only Markdown fence census found **19 comments containing fences**, **0 unclosed fences**, and **0 fenced current-receipt binding lines**. Therefore no actual false acceptance is asserted. A six-PR (#179–#184) merge/receipt readback was checked; #180–#184 matched their exact `PR=` receipt merge SHAs, and #179 was excluded from that narrow regex projection rather than counted as a failure. The full automation denominator, including unsuccessful and inaccessible attempts, is **UNKNOWN**; `AUTOMATION_RATE=NOT_COMPUTABLE`, `PROJECT_READBACK_RATE=NOT_COMPUTABLE`.

This candidate cannot authenticate caller-supplied JSON, prove GitHub actor identity, distinguish a malicious owner-authored plain-text claim from a receipt, or establish scientific truth. It rejects one syntactic ambiguity only. Its positive fixtures do not establish independent third-party validation. R10 PR #115 had no new PR conversation comments, reviews or review threads in this readback; no independent receiver ACK or executed expert research was established. The owner-controlled PR #185 is a separate draft architecture proposal and was not merged or modified.

Publication scope: only three additive files under the existing R16 Alpha-Node research directory. No new scheduler, evaluator modification, productive Repository Steward change, runtime/Hostinger/WWW write, external actor registration, Cursor dispatch, merge bypass, node reset or claim promotion. Publication, main and Issue #93 readbacks remain distinct post-test gates.
