# AXIOM Alpha-Node C1 — PR #196–#197 original-byte extension and bounded PR/receipt census · 2026-10-29

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_PR196_197_INCREMENTAL_BYTE_CENSUS_20261029_R0
DECISION=KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=076d763dc8bb9aae26a8507aae0e7567eac9ee3e
PINNED_MAIN_PARENT=959cfe7e13db98735e4b3d7ec26d2d0ce7d5cbe7
PREDECESSOR_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/197
PREDECESSOR_ISSUE93_RECEIPT=6503078382
PREVIOUS_CENSUS_PR=https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/196
FROZEN_EVALUATOR_FIRST_COMMIT=213c605b22d3a9cc234636550272a9b7df222ec1
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / immutable source provenance

The GitHub connector directly retrieved the current `main` commit `076d763dc8bb9aae26a8507aae0e7567eac9ee3e`, its PR #197, the prior PR #196 and Issue #93's 187 available comments. The authenticated GitHub actor is `nexusomegac27` with repository owner permissions. The R16 Alpha contract, AGENTS.md, GOVERNANCE.md, operator direct-publication rule, task-anchor norm, repository order, research/pipeline policy and external actor write-slot registry were read at pinned main. External actor allowlist is empty. No new pipeline root or existing file modification is proposed.

The preceding additive census covered **31/31** source files from PR #184 and #186–#195, totaling **137,572 bytes** in earlier separate audits. Those 31 files were **not rehashed during this iteration**. This iteration independently fetched and hashed the four newly added original files from PR #196 and #197 at immutable main, using a separately implemented JavaScript SHA-256 and Git blob SHA-1 calculator. SHA-256 empty-string, `abc` and SHA-1 `abc` reference vectors passed. Git blob calculation used `SHA1("blob " + decimal_byte_length + NUL + raw_bytes)`, independently compared with GitHub's file blob IDs.

| PR | Exact filename under `research/r16/axiom-alpha-node-c1-adaptation-20261012/` | UTF-8 bytes | Independently calculated SHA-256 | Independently calculated Git blob SHA-1 |
|---|---|---:|---|---|
| 196 | `alpha_pr191_195_incremental_original_byte_census_c1_report_20261029.md` | 8,858 | `b0b855923a3a692da70652b05735fa88251fcfdd1cb8d7e5fadb4372d15d2fc1` | `59d576395d428d63d192ebaa543c1c88df041ed1` |
| 197 | `alpha_issue93_v7_dependency_fixity_preflight_c1_report_20261029.md` | 5,603 | `38fbeabb2b4421d754877b72f9c50ab3a306889bdfd2211427179a481d22cae3` | `33a819d59018db4770ce7985dc7a38ace72a43af` |
| 197 | `alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py` | 4,194 | `0fb4f5408d4c61d3a2e4c9bd160cc63afe68b077febbdd288e757b0fb324af23` | `80ed3eee7bf66c8076ce4f06c1eac5e9904ded48` |
| 197 | `frozen_issue93_v7_dependency_fixity_oracle_v1_20261029.py` | 4,938 | `249e51a98d810bf5ddc37f0b9de22195706c9591ae20ad6eb64c678f3c47023b` | `9534bc535643b73c732644177236db24b3f6a313` |

**New original bytes: 23,593; independently calculated SHA-256: 4/4; Git blob matches: 4/4.** Prior + new cumulative coverage: **35/35 files, 161,165 bytes**, explicitly an *incremental* rather than single-run independent rehash of all 35.

## NEGATIVE HYPOTHESIS / cohort denominator

A partial or corrupted cohort can falsely appear complete when PR #185 is counted as merged, a PR receipt is omitted, an owner comment binds the wrong merge SHA, a Git blob differs, or the earlier 31-file cumulative count is silently substituted for an independently rehashed 35-file count.

The bounded observable cohort consists of **13 merged PRs**: #184 and #186–#197. Direct GitHub PR metadata identified all 13 as merged and the exact merge SHAs. The GitHub comparison from #184 merge `05748765ab35d87d6bfa79377a97d7c0ff2c2807` to #197 merge `076d763dc8bb9aae26a8507aae0e7567eac9ee3e` returned **ahead=12, behind=0**. Each PR has one exact-key `PR=` owner comment in Issue #93 with `ACTUAL_MAIN_READBACK` equal to that PR's merge SHA and `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`: **13/13 metadata receipt matches**. Last receipt: `6503078382`. PR #185 was checked separately and remains **open/unmerged**; it is a real negative control, not a missing merged publication.

This is **13/13 owner-reported receipt-to-merge metadata matches**, NOT 13 independently executed scientific validations, NOT 13 fresh source-byte rehashes, and NOT a project-wide handoff denominator. A self-reported owner receipt alone does not establish independent test execution.

## PINNED BASELINE / separate frozen evaluator / falsifier

- Before: 31/31 previously source-checked files, 137,572 bytes. After: 35/35 cumulatively source-checked files, 161,165 bytes; newly checked 4/4, 23,593 bytes. The incremental delta is +4 source files and +23,593 independently processed bytes.
- The separately authored, isolated Python metadata evaluator was executed locally before publication: `python alpha_pr196_197_census_oracle_short_20261029.py -q` → **12/12 PASS** (one positive, eleven negative controls). Its on-disk SHA-256 was `bb7f4f8459a52917d41fbe35d5187496a42da3f2f8b3bde290790ee028360efb`, 4,115 bytes. Its source was committed first, before this report, as `frozen_alpha_pr196_197_census_oracle_v1_20261029.py`. It checks a pinned *caller-supplied* inventory, not original GitHub bytes or authenticated identity.
- Negative fixtures: wrong SHA-256, wrong independently computed blob, mismatched API blob, missing source, duplicated source, missing receipt, wrong receipt main, untrusted actor, PR #185 falsely marked merged, wrong ancestry count and wrong cumulative byte total. **11/11 rejected**. The positive pinned inventory was accepted 1/1.
- Falsifier: any one of these 4 source SHA-256 or Git blob identities differs on an independently fetched immutable commit; any one of 13 PR merge SHAs differs from its exact-key Issue #93 receipt; PR #185 is actually merged; or a frozen evaluator negative fixture is accepted. Such evidence invalidates the relevant scoped result.

The evaluator is a different Python implementation from the JavaScript byte hasher, but both are authored in this AXIOM run; **external third-party validation is NOT_ESTABLISHED**. The evaluator's constants reflect this pinned cohort and do not establish completeness of all project handoffs.

## R10 passive side readback

PR #115 remained open, with zero PR discussion comments, zero reviews and zero review threads in the fresh GitHub API read. The Issue #93 comments inspected yielded no newly independently authenticated R10 expert receiver return; owner SEND descriptions are not independent receiver authentication. `PUBLIC_SEND=HISTORICALLY_OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`. The historical detached manifest is not newly rehashed here because no new receiver original was discovered.

## DECISION / claim boundaries

`KNOWLEDGE_APPEND` for the newly verified 4-file source extension and the 13/13 bounded owner PR/receipt metadata census. **Project-wide automation rate = NOT_COMPUTABLE; project-wide publication full-readback rate = NOT_COMPUTABLE**, because the authenticated complete eligible/failed handoff population is missing. No claim of 90% automation, 100% project readback, external expert research, production integration, WWW parity, or claim promotion. No model, runtime, Hostinger, actor registry, governance, prior source, evaluator oracle, or path-bound history is modified.

`BLOCKED_LANE != BLOCKED_SYSTEM` · `DRIFT_RESET=NON_DESTRUCTIVE` · `C1_DESCRIPTIVE_ONLY`.
