# AXIOM Alpha-Node — Real Issue #93 comment-body digest inventory V1 (C1, 2026-10-30)

```text
OBJECT = NEXUS_OMEGA_ALPHA_ISSUE93_REAL_BODY_DIGEST_INVENTORY_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 06eee8d929c3bf6877cd01767aeea82e3f9e01bf
PREDECESSOR_PR = 211
PREDECESSOR_ISSUE93_RECEIPT = 6516343927
SOURCE = nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93
EXTERNAL_ACTOR_AUTHORIZATION = NONE
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Observable gap, source and baseline

The predecessor body-pin preflight V1, from pinned main above, detects changed comment text **only when independently retained per-ID body pins are supplied**. Its predecessor report explicitly states that zero actual Issue #93 body digests were independently anchored at that time. The earlier complete Issue #93 census was metadata-only (199 comments at its cutoff). No real body edit was established.

This run fetched the GitHub connector's paginated Issue #93 comment population twice, obtaining **201/201 ordered unique comment IDs** at the digest snapshot cutoff (first 6111816879, last 6516343927). The comment-body source comprised **620,299 UTF-8 bytes**. The generated inventory contains only ID, UTF-8 byte count and SHA-256, not original comment texts or user data. Its 201 rows were rechecked against a fresh API read: **201/201 digest and byte-count matches**. The API connector is the transport source; neither API actor metadata nor source transport is independently cryptographically authenticated.

## Candidate, independent evaluator, falsification

A new offline Python builder validates the declared source, pinned main, ordered population, duplicate IDs, exact row fields, body types, and strict JSON. It emits a digest-only inventory. The new independent Python evaluator was committed on the owner branch before the candidate and executed locally as a separate subprocess, without importing or modifying the candidate: **14/14 PASS**, including **13/13 fail-closed negative/malformed fixtures** (missing/extra comments, duplicate/reordered IDs, invalid source/main SHA, booleans, non-string body, duplicate JSON keys, NaN and malformed JSON). A Unicode control distinguishes code points from UTF-8 bytes.

Negative hypothesis: a changed body under fixed historical pins is detectable, but a changed body with simultaneously recomputed pins is not. The previously published body-pin preflight supplies the fixed-pin comparison. **Falsifier:** any future body whose ID and fixed digest differ but passes the unchanged preflight invalidates the detection claim; a deleted or reordered pinned ID must likewise fail. The new builder alone is not a tamper detector, and cannot authenticate the origin of its own pins.

### Scoped before/after (not project-wide metrics)

| Metric | Baseline | This candidate |
|---|---:|---:|
| Real Issue #93 comment bodies with immutable *digest-only inventory* | 0/201 demonstrated | 201/201 pinned on PR branch; main pending |
| Fresh API body-to-pin comparisons | 0/201 demonstrated | 201/201 MATCH |
| Independent subprocess oracle | Not applicable | 14/14 PASS |
| Negative/malformed fixtures | Not applicable | 13/13 expected rejection |
| Authenticated, complete project handoff denominator | UNKNOWN | UNKNOWN |

The source inventory is a reproducible **snapshot**, not a proof that GitHub comments never change, that all historical comments existed, or that GitHub authenticated the origin. Snapshot consistency is not external third-party scientific validation.

## Exact research artifacts

- `frozen_alpha_issue93_digest_inventory_oracle_v1_20261030.py`: **2,823 UTF-8 bytes**, SHA-256 `65b4fee828f42a0def3f40accbf892b8b6b2c7abfe6b237f378e65a2b5e7ce64`, Git blob `baf10ff978e1c582327efe7bf6380e13059135d7`.
- `alpha_issue93_digest_inventory_v1_20261030.py`: **2,528 UTF-8 bytes**, SHA-256 `021d0b109d3b5a722fcf3d6189b16de6aa11a304386059ab20937295f03524f4`, Git blob `a995dbf40981ed2f1596f560a49862fb293677a1`.
- `alpha_issue93_real_body_digest_inventory_v1_20261030.json`: **28,739 UTF-8 bytes**, SHA-256 `69787c3cf2e59401eb9ea52048f8c0f0ba4cf928040f1095a8b4c99986e0f4fb`, Git blob `a7e8314a9742c2eeb04e98f8ba02deddbd16e92c`.

Reproduce the synthetic oracle using `python frozen_alpha_issue93_digest_inventory_oracle_v1_20261030.py alpha_issue93_digest_inventory_v1_20261030.py` in the same research directory. For real-source regeneration, supply an independently fetched ordered `{"source":...,"main_sha":...,"declared_count":...,"comments":[{"id":...,"body":...}]}` JSON payload to the offline builder via stdin; do not commit raw bodies. Compare the emitted pins to the committed inventory, and preserve exact cutoff IDs.

## R10 passive parallel readback

PR #115 is OPEN, with no PR discussion comments, submitted reviews or review threads in this run. The immutable detached manifest at commit `539d4bb33d2ba2c4895713c1bc437ece0743eeea` was freshly read: **4,588 bytes**, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` MATCH. No new independent expert return or authenticated receiver ACK is established. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`.

## Publication gates

The current branch is a reversible, public-safe C1 research-only candidate. No changes to existing source objects, workflows, external actor registry, runtime, Hostinger, WWW, or GPT internals. Branch/PR CI, actual merge, immutable main readback and append-only Issue #93 receipt are distinct required events and are **NOT claimed by this premerge report**. `AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`: the authenticated project-wide handoff population is unknown.
