# AXIOM Alpha-Node · R10 Git commit OID preimage V1 · 2026-10-30

```text
OBJECT=NEXUS_OMEGA_ALPHA_R10_COMMIT_OID_PREIMAGE_V1_20261030_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=d9de0f0f2f28f184559e9b44e0c96c2bf873cf93
PREDECESSOR_PR=218
PREDECESSOR_ISSUE93_RECEIPT=6523871576
R10_PR=115_OPEN_UNMERGED
R10_SOURCE_COMMIT=dab7c59070d67e7e2a244bd6d05db9a4d37460e3
R10_SOURCE_TREE=d743c5d926d469470afa0d7331d5c56b8262d56c
R10_SOURCE_PARENT=eb86e98228efd393e36fb3fbecf79f830b7c41e2
R10_ORIGINAL_HEAD=539d4bb33d2ba2c4895713c1bc437ece0743eeea
INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED
RAW_GIT_COMMIT_BYTES=NOT_OBTAINED
```

## OBSERVE / SOURCE / NEGATIVE HYPOTHESIS

The preceding PR #218 reconstructed five Git-tree SHA-1 OIDs, not the R10 Git commit OID. The GitHub Git Data API endpoint `/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/git/commits/dab7c59070d67e7e2a244bd6d05db9a4d37460e3` returned normalized author/committer dates, parent/tree IDs, message and `verification.reason=unsigned`, **not raw Git commit object bytes**. The new 529-byte JSON is a transcribed API *projection*, not original HTTP response bytes or an authenticated expert return. Projection SHA-256: `c2e66af22fdd9680998b6a9513f33865810215e1e038a41356cc96410478a8b8`; Git blob: `8eb1784e50202c9ddf3e916fdbf115fbeb9a2194`.

The normalized UTC timestamp loses the original Git timezone offset. Naively reconstructing with `+0000` gives SHA-1 `74ebfe0fe5500eccafcd102de21d7c41bd90afdb`, not the pinned commit. Falsifier: the pinned commit must have exactly one matching preimage under the declared bounded timezone hypothesis, and mutated source fields or forged authority fields must fail closed.

## ISOLATED CANDIDATE / INDEPENDENT TEST

The evaluator `frozen_alpha_r10_commit_oid_preimage_oracle_v1_20261030.py` was **committed before** the candidate. It invokes the candidate as a separate Python subprocess and independently computes the positive Git object ID using `git hash-object -t commit --stdin`, not the candidate's `hashlib` code. The candidate `alpha_r10_commit_oid_preimage_gate_v1_20261030.py` enforces strict JSON, external commit pin, one parent, unsigned state, and tests identical author/committer offsets UTC−12:00 to UTC+14:00 in 15-minute increments. The source fixture is `r10_commit_api_projection_v1_20261030.json`.

The independent Git CLI and candidate both match the pinned SHA-1 using an inferred `+0200` offset and **304-byte** Git commit payload, without trailing newline or signature. Frozen black-box evaluator: **18/18 PASS** including **17/17 fail-closed negatives** (tree, parent, same-length message, author, committer, timestamps, extra parent, wrong external pin, forged actor/ACK/signature fields, duplicate keys, nonfinite and malformed JSON). Run:

```bash
python -S frozen_alpha_r10_commit_oid_preimage_oracle_v1_20261030.py alpha_r10_commit_oid_preimage_gate_v1_20261030.py r10_commit_api_projection_v1_20261030.json
```

## BEFORE / AFTER / BOUNDARIES

| Metric | Before | After |
|---|---|---|
| Matching R10 commit SHA-1 preimage from normalized API fields | 0/1 demonstrated | 1/1 under bounded offset hypothesis |
| Independent Git CLI crosscheck | Not established | 1/1 MATCH |
| Separate negative controls | Not available for this candidate | 17/17 rejected |
| Original raw Git commit bytes acquired | NO | NO |
| Authenticated external R10 receiver or actor | NO | NO |

A matching SHA-1 preimage does **not** prove these were the historical original Git bytes, API provenance, external actor identity, scientific execution or independent ACK. Git SHA-1 collision limitations and the same-offset search assumption remain. No runtime integration, R10 merge, new automation, Hostinger/WWW write, secret, biological experiment, evaluator self-approval or claim promotion. Project-wide eligible handoff attempt denominator remains unavailable: `AUTOMATION_RATE=NOT_COMPUTABLE`; `FULL_READBACK_RATE=NOT_COMPUTABLE`. PR/CI/main readback and Issue #93 receipt must be verified separately, not inferred from this report.
