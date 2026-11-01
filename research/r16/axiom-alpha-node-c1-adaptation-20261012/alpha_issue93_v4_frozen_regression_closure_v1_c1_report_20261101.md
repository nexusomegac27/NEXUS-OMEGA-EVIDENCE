# AXIOM Alpha-Node — Issue #93 V4 frozen regression closure · 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_ISSUE93_V4_FROZEN_REGRESSION_CLOSURE_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_QUALITY_EVIDENCE_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=ec887632a4f1659a29c01f4db8bbf1cc79c30ae6
PREDECESSOR_PR=251
PREDECESSOR_ISSUE93_RECEIPT=6549786500
PRODUCTION_INTEGRATION=NO
```

## One candidate and counter-hypothesis

The prior V4 report (PR #251) explicitly marked the previously frozen 46-case V1–V3 regression as **not rerun against V4**. The negative hypothesis is that V4's bounded stdin and recursion handling may have regressed older inventory, finite-number or Unicode-scalar behavior despite passing its own 15-case oracle.

This iteration changes **quality evidence**, not validator code or independent test oracles. Eight original Python files were fetched at the immutable parent `main`, reconstructed as UTF-8 bytes in an isolated local workspace, and matched to their Git blob IDs. SHA-256 was computed independently from the reconstructed bytes. The companion JSON binds all eight byte counts, SHA-256 and Git blobs, exact reproduction commands, stdout byte counts and SHA-256, and expected terminal markers.

## Actual frozen black-box execution

Four pre-existing, unchanged subprocess oracles were run on the same V4 source and its pinned dependencies using Python 3.13.5, without network access.

| Frozen oracle | Actual outcomes | Positive | Negative |
|---|---:|---:|---:|
| V1 two-inventory consistency | 25/25 PASS | 3 | 22 |
| V2 nonfinite exponent | 9/9 PASS | 4 | 5 |
| V3 Unicode scalar | 12/12 PASS | 5 | 7 |
| V4 bounded JSON | 15/15 PASS | 6 | 9 |
| **Total** | **61/61 PASS** | **18** | **43** |

**Before → after:** 15/61 previously executed on V4, with 46/61 explicitly `NOT_RERUN`; now **61/61 executed expected outcomes**. These are suite-level synthetic assertions, not 61 unique incidents, production defect rates, independently sampled trials or scientific claim validations.

A separate local manifest verifier checked physical source lengths/SHA-256 and captured stdout SHA-256/terminal markers: **1/1 positive**. Four modified source/oracle hash declarations and one modified stdout hash declaration were rejected: **5/5 negative fixtures**. This additional checker is not an adopted or frozen repository oracle. The four pre-existing frozen black-box oracles are the independent technical evaluators.

**Falsifier:** a source/oracle hash mismatch, nonzero oracle exit, missing expected terminal marker, or different classification under the pinned environment refutes this scoped result. Captured raw stdout logs are not published; only their byte counts and SHA-256 are preserved, so independent replay remains necessary.

## R10, denominator and authority boundaries

At observation, `main=ec887632a4f1659a29c01f4db8bbf1cc79c30ae6`, Issue #93 had 240 owner-authored comments and latest receipt `6549786500`. R10 PR #115 remains open; no new independent expert return was present in the PR discussion. The pinned detached R10 manifest was retrievable as 4,588 bytes with Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. The pinned external GitHub actor allowlist is empty.

`PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_EXPERT_ACTOR=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

`AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`. Complete authenticated eligible attempt denominators including failures are unavailable. The 61 test outcomes and 240 comments are **not** eligible handoff denominators.

No old file, oracle, workflow, external write slot, model, runtime, Hostinger/WWW state or claim ceiling is changed. No GitHub→WWW parity is asserted. This is one additive C1 research-quality candidate under the existing R16 lane.

**Publication is not pre-asserted:** PR checks, merge, immutable main readback and Issue #93 append-only receipt require separate actual verification after creation.
