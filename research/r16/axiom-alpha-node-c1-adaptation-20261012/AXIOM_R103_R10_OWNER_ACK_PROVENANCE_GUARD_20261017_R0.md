# NEXUS OMEGA · AXIOM R103 · Owner-asserted receiver ACK provenance guard · 2026-10-17

```text
OBJECT = NEXUS_OMEGA_AXIOM_R103_R10_OWNER_ASSERTED_RECEIVER_ACK_GUARD_20261017_R0
STATE = CONTRADICTION_APPEND + TESTED_ISOLATED_PATCH_CANDIDATE_C1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
R10_ORIGINAL_HEAD = 539d4bb33d2ba2c4895713c1bc437ece0743eeea
R10_READBACK_HEAD = dab7c59070d67e7e2a244bd6d05db9a4d37460e3
R10_R1_MANIFEST_SHA256 = 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc
```

## Observe / source exactness

PR #115 remains open and unmerged. Its head is nine owner-authored commits ahead of the immutable original. The R1 manifest remains Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. All 35 Issue #93 comments are by the owner; PR reviews and PR comments: zero. The new owner-archived files are actual GitHub bytes, not independently authenticated external actors.

Independent UTF-8 byte readback and recomputed SHA-256/Git-blob-SHA-1 (cross-checked against GitHub blob metadata):

| File in `research/r10/biocomputing-independent-experts-20261016/returns_20261016/` | Bytes | SHA-256 | Git blob |
| --- | ---: | --- | --- |
| `R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt` | 4380 | `60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5` | `4e31f92be1f673f49a2c27e570b5849e754cca78` |
| `GROK_R10_INDEPENDENT_REPORT_20261016.txt` | 10086 | `4880fb234c94575b976c5cdf0c6ecefe4759a158feb31af25b217d56a7881c57` | `4841076e18c65645a0bc96028a01dbd95ad7818f` |
| `KIMI_R10_ORIGINAL_REPORT_20261016.txt` | 10636 | `dc1b875df367730d286c4ea29697b588386f236da204781d3ca86ac6e4364079` | `cd5912d327189531e8b865dd73d44dad42d82685` |
| `R10_GITHUB_INDEPENDENT_VERIFICATION_20261016.md` | 17375 | `6ff4fd59b54f148b7412d98f20e5069e195e64b0f1dfbaf1549dac69ff792c01` | `88570a979e92d1dee5232d3592b6f7598ec6a210` |

The ACK file claims `EXTERNAL_RECEIVE_ACK = THIS_RECEIPT` and expert execution in a previous turn. The same source says no registered external actor and no independent return commit. **Claimed ACK is not authenticated ACK.** This is an internally conflicting source assertion, not hidden source tampering: the existing R10 terminal register already correctly labels it `EXPERT_ASSERTED_ACK_UNAUTHENTICATED`.

## Negative hypothesis / one isolated machine candidate

A naive parser can mistake an expert-named file or `EXTERNAL_RECEIVE_ACK` string for a real H5 return. A proposed stdlib-only guard requires independently verified bytes, blob, commit, exact manifest reference, registered authenticated GitHub actor distinct from owner, and substantive source-specific acknowledgement before classifying an independent receiver ACK. It does not itself authenticate actors, execute expert research, adjudicate science or authorize writes.

Pinned synthetic evaluator was written and SHA-256-frozen **before** implementation: `frozen_evaluator.py` SHA-256 `e1a79bbeee4ef71b2adc58a8b0e7e5fe65f124456f36553943be696804b13f48`; fixture JSON SHA-256 `97a3849d23d1616532e334886b6bb93dd02b2d361a12f7a512dbab17f51b63b4`. Candidate SHA-256 `5131da519074ab27faab46f8da8317cf22bcc760343877d3ddfb01028b623000`.

| Test comparator | Frozen synthetic cases |
| --- | ---: |
| Naive claim-string baseline | 2/20 correct |
| Isolated guard | **20/20 correct** |
| Deliberately weakened owner/provenance mutant | 15/20 correct |

The actual owner-uploaded R10 ACK metadata classifies `SOURCE_EXACT_OWNER_ASSERTION_NOT_ACK`. The pre-existing human R10 source register **already correctly rejected** that promotion: no actual improvement over the human register is claimed. This is a tested *machine enforcement candidate*, not independently accepted production code. Falsifier: any authenticated, allowlisted, exact-source substantive ACK falsely rejected, or any owner-mediated assertion accepted.

## Decision

```text
PUBLIC_SEND = CONFIRMED_OWNER_GITHUB_BRANCH
INDEPENDENT_RECEIVER_ACK = SOURCE_NOT_PRESENT_AUTHENTICATED
AUTHENTICATED_GITHUB_ACTOR = OWNER_ONLY_OBSERVED
AXIOM_SCIENTIFIC_ADJUDICATION = NOT_ESTABLISHED
EXPERT_RESEARCH_ACTUALLY_EXECUTED = NOT_ESTABLISHED_BY_GITHUB_ACTOR_EVIDENCE
R10_MAIN_MERGE = NO
R103_RUNTIME_INTEGRATION = NO
CLAIM_PROMOTION = NO
HANDOFF_30D_NUMERATOR = UNKNOWN
HANDOFF_30D_ELIGIBLE_DENOMINATOR = UNKNOWN
HANDOFF_TARGET_90_PERCENT = NOT_COMPUTABLE
```

The branch publication of this research report does not authorize R10 merge, new worker, actor self-registration, Hostinger or Cursor execution. Any later public change requires exact commit/blob/readback. Sources: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/115 ; https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93 ; https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/dab7c59070d67e7e2a244bd6d05db9a4d37460e3
