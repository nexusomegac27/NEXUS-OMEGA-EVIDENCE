# AXIOM Alpha-Node — Issue #93 receipt-body source binding (C1, 2026-10-30)

```text
OBJECT=NEXUS_OMEGA_ALPHA_ISSUE93_RECEIPT_BODY_PIN_BINDING_V1_20261030_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=97838201eb9e435e3d2690752133b96d02368953
PREDECESSOR_PR=222
PREDECESSOR_ISSUE93_RECEIPT=6531007357
EXTERNAL_ACTOR_ALLOWLIST=EMPTY
PRODUCTION_INTEGRATION=NO
```

## Observe / original bytes / provenance

GitHub `main` was pinned to `97838201eb9e435e3d2690752133b96d02368953` before this candidate. The previously published ten-PR audit (`alpha_issue93_pr_receipt_chain_v1_20261030.json`, Git blob `7fe4b9256411695829d0fe9e1144252bcd35bd03`, SHA-256 `a16f417851d6af8d3a95c4b15a6eb3b2028874776cba4f45b3dec4e1e5fd0c22`) linked PRs #212–#221 to ten Issue #93 receipt IDs. The older body-digest delta (`alpha_issue93_body_digest_delta_v2_20261030.json`, Git blob `0f6d5f73f8b219d39f31e03b12cc555866b01d23`, SHA-256 `e83aa5f19d1882e56291ab21bb4685710d57fd5809f7b90fc6d2079f7d44079f`) contained only the first nine of these ten receipts. This is a *source-byte binding gap*, not proof that the tenth receipt was false.

The existing GitHub connector fetched the 212 actual public Issue #93 comment bodies. A separately implemented JavaScript SHA-256 (checked against empty-string and `abc` standard vectors) computed UTF-8 byte counts and SHA-256 of all ten selected original API body strings. Nine matched the predecessor digest delta exactly. The tenth, receipt `6527434004` for PR #221, had **2,699 UTF-8 bytes**, SHA-256 `fd602eda80fc9f505dedd146aa3beec28815eb7e96fc528a85df2a53497b037a`. All ten receipt IDs matched the separately fetched PR-audit JSON. These observations authenticate neither the GitHub transport nor the human identity behind the API actor field; raw HTTP wire bytes were not acquired.

## Negative hypothesis / one candidate / pinned baseline

A fixed PR/receipt audit may report `10/10` metadata consistency even though one of its referenced receipt bodies has no pinned byte digest. An edited same-length receipt could then evade that particular *cross-source body-fixity* check. The isolated successor adds exactly one append-only digest supplement, preserving both predecessor JSON files unchanged, plus a frozen fixed-sample oracle. It does not silently relabel the 10-row sample as the project-wide handoff population.

| Fixed sample metric | Before | After |
|---|---:|---:|
| PR-to-Issue receipt ID links | 10/10 | 10/10 |
| Receipt bodies with source-checked digest pins | **9/10** | **10/10** |
| Newly pinned source bytes | 0 | **2,699** |
| Local frozen independent subprocess checks | Not established for this specific supplement | **20/20 PASS** |
| Negative and malformed fixtures | Not established for this specific supplement | **19/19 rejected** |
| Project-wide eligible handoff denominator | UNKNOWN | **UNKNOWN** |

The independent Python oracle was committed **before** the candidate JSON and executed locally as a separate process. It rejects a wrong repository or pinned main, changed predecessor digest, fabricated project scope/authentication, omitted or duplicate new pin, wrong receipt ID/PR, a same-byte-length SHA-256 mutation, incorrect UTF-8 count, fake actor field, extra fields, duplicate JSON keys and nonfinite JSON. The oracle checks a frozen *known-source* digest and identity; it does not fetch GitHub, independently authenticate the source, or validate all historical receipts. No external third-party evaluator was used.

**Falsifier:** independently refetch Issue #93 comment `6527434004` and show that its UTF-8 byte count or SHA-256 differs from the new pin; or mutate the new pin's SHA-256 without changing its byte count and observe an oracle PASS. Either result defeats the claimed fixed-sample binding. Coordinated alteration of both frozen oracle and candidate or compromise of the GitHub API remains outside this isolated test.

## Reproduction and boundary

From the existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` directory:

```sh
python frozen_alpha_issue93_receipt_body_pin_oracle_v1_20261030.py alpha_issue93_receipt_body_pin_supplement_v1_20261030.json
```

The predecessor source bytes and their digest pins remain immutable at the pinned main. The new JSON is digest-only and contains no copied comment body. This is an isolated C1 research candidate; it does not change the production handoff counter, validator trust roots, CI workflows, repository structure, live runtime, Hostinger, WWW, model weights, external actor registration or claim ceiling. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE` because the complete authenticated eligible-attempt population, including failures, is unavailable. Local/private inaccessible returns are never credited as successful automated handoffs.

## Passive R10 status

PR #115 remained open and unmerged. Its immutable detached R10 manifest at commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was freshly fetched and rehashed: 4,588 UTF-8 bytes, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. PR discussion, reviews and review threads contained no new independent receiver return; all 212 Issue #93 comments observed were owner-authored. `PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

## Publication condition

This report records the **pre-merge candidate**. GitHub PR creation and successful CI alone are not `main` publication. Only after the existing required checks pass, an authorized merge is observed, exact `main` and file bytes are read back, and a new append-only Issue #93 receipt is verified may `MAIN_PUBLISHED` be reported. `BLOCKED_LANE != BLOCKED_SYSTEM`.
