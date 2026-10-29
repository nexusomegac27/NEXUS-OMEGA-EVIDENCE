# AXIOM Alpha-Node · Issue #93 exact-key receipt attribution · 2026-10-29

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_20261029_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 623ac73ae19f7000cabb050066667e0eff49e5a8
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/183
PREDECESSOR_ISSUE93_RECEIPT = 6484213521
SOURCE_INBOX = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93
SCOPE = PR_164_TO_183_ONLY
PRODUCTIVE_REPOSITORY_STEWARD_MODIFIED = NO
WWW_PARITY = NOT_ESTABLISHED

## Observation and real falsifier

The connected GitHub API returned 174 Issue #93 comments. Twenty PRs (#164–#183) were independently read from the GitHub PR API and reported merged, with twenty exact-key PR= receipt lines. All twenty ACTUAL_MAIN_READBACK= values in their corresponding comments matched the PR API merge-commit SHAs. This is a bounded, selected *published-PR/receipt mapping*, not a census of attempted handoffs or full commit/source/test/readback success.

A naive substring filter searching for PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/182 matched **two** comments: receipt 6483629858 (correct) and receipt 6484213521 (incorrect). The second comment contains **PREDECESSOR_PR=.../pull/182**, whereas its exact current PR= field points to #183. An exact whole-line key comparison matched only receipt 6483629858. Thus, actual API observations falsify the assumption that substring PR= search uniquely attributes receipts. No historical published receipt was incorrect; the defect was in the ad hoc scanner.

## Isolated candidate and independent evaluation

The new alpha_issue93_exact_key_receipt_census_v1_20261029.py accepts a caller-supplied, explicitly scoped GitHub-API-shaped JSON projection. It parses **exact field names at the beginning of a line**, not substrings; rejects duplicate receipt fields, duplicate PR receipts, absent expected receipts, mismatched merge commits, non-owner claimed actors, nonmonotonic receipt IDs and C1 promotion. PREDECESSOR_PR= and quoted > PR= lines are not current-PR bindings. It neither fetches nor authenticates GitHub, and it does not infer any project-wide rates.

The separate frozen_issue93_exact_key_census_evaluator_v1_20261029.py was published on the owner branch **before** the candidate. Its subprocess tests do not import candidate functions. Locally on Linux/Python 3.13, **14/14 PASS**, including positive controls and single-defect negative fixtures. A deliberately mutated scanner that falls back from absent PR= to PREDECESSOR_PR= scored **12/14 PASS**, with two expected failures. This is implementation-independent black-box testing within the same AXIOM environment, **not** third-party validation.

| Metric | Naive scanner | Exact-key method |
|---|---:|---:|
| Real API matches for current PR #182 | 2 (one false attribution) | **1 (correct)** |
| Correctly attributed PRs in bounded #164–#183 set | Not a unique mapping for #182 | **20/20** |
| Synthetic frozen subprocess oracle | Mutation: 12/14 | **14/14 PASS** |
| Project-wide automated handoff denominator | Unknown | **Unknown** |

Falsifier of stronger authenticity claims: a caller can supply internally consistent, fabricated user.login, PR metadata and receipt bodies; the isolated candidate would accept them. Actual GitHub API provenance and complete attempt enumeration remain separate, necessary inputs. A successful merge is not a fully independently checked source or a proof of a 90% automation rate.

## Receipt mapping from the bounded live API projection

| PR | Issue #93 receipt |
|---:|---:|
| 164 | 6460634584 |
| 165 | 6461898518 |
| 166 | 6462252014 |
| 167 | 6463634536 |
| 168 | 6464324854 |
| 169 | 6465851951 |
| 170 | 6467072191 |
| 171 | 6469264130 |
| 172 | 6470285817 |
| 173 | 6472047244 |
| 174 | 6473538115 |
| 175 | 6474399729 |
| 176 | 6476336042 |
| 177 | 6477928081 |
| 178 | 6478246029 |
| 179 | 6480022471 |
| 180 | 6481362322 |
| 181 | 6482166560 |
| 182 | 6483629858 |
| 183 | 6484213521 |

## Limits, safety and disposition

The live census used connected API response objects, not a separately archived original HTTP response byte stream. The candidate tests used synthetic data, while the live 20/20 mapping was independently computed from retrieved GitHub API objects. Neither the candidate nor the local tests establish GitHub identity from user-supplied JSON, detect all unseen failures, or prove project-wide completeness. Source and receipt provenance are not semantic scientific validity. The project-wide automation numerator/denominator and full-readback numerator/denominator remain **UNKNOWN/UNKNOWN** and NOT_COMPUTABLE; private/local unavailable returns are not successes.

Exactly three additive files in the already registered R16 Alpha-Node research directory. No historical file changes, evaluator rewrites, external actor registration, new scheduler, productive Steward integration, runtime/Hostinger/WWW write, node reset, Cursor dispatch or claim promotion. GitHub branch/PR/CI/main/Issue #93 publication receipts are separate required post-test gates.

R10 PR #115 remained open in the connected API check; zero PR conversation comments, reviews and review threads were returned. The immutable R10 manifest was fetched at 539d4bb33d2ba2c4895713c1bc437ece0743eeea (4,588 text characters, Git blob 0c2ca57a40f519da45ce60b565e8aadb4c9b95df). No new independent expert return was found: PUBLIC_SEND=OBSERVED, INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED, EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED, AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED.
