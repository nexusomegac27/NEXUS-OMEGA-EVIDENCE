# AXIOM Alpha-Node — R10 receiver ACK source-channel contradiction (C1)

OBJECT = NEXUS_OMEGA_ALPHA_R10_RECEIVER_ACK_CHANNEL_BINDING_CONTRADICTION_20261019_R0
STATE = CONTRADICTION_APPEND_C1_RESEARCH_ONLY
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
R10_PINNED_HEAD = 539d4bb33d2ba2c4895713c1bc437ece0743eeea
R10_MANIFEST_PATH = research/r10/biocomputing-independent-experts-20261016/R10_GITHUB_NATIVE_DETACHED_SOURCE_MANIFEST_20261016_R1.json
R10_MANIFEST_BYTES = 4588
R10_MANIFEST_SHA256 = 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc
R10_MANIFEST_GIT_BLOB = 0c2ca57a40f519da45ce60b565e8aadb4c9b95df
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Negative hypothesis and actual finding

The previously isolated local R10 receiver provenance guard V1 accepts a synthetically constructed ACK in the wrong GitHub source channel. Its accepted URL set is the union of PR #115 and Issue #93 issuecomment permalinks regardless of whether the normalized input row comes from `pr_comments`, `issue_comments` or `reviews`. Therefore the source-channel label is not independently bound to the permalink.

This is an **isolated synthetic failure**, not evidence of a real forged expert ACK. The repository's actual external actor allowlist remains empty, so no real independent receiver ACK is established.

## Frozen independent test before V2 implementation

- Frozen oracle SHA-256: `6db29e125bb0ef2fa624f2d46e26635f7f13cd253751bad084da1df4a23c5fe5`.
- Predecessor guard V1 SHA-256: `4d394443e0118db2137bb8d63ffe4895394df52b1c3e20a0981d9501f68dd019`.
- Isolated V2 candidate SHA-256: `ae54c829dd7be503abcd2df752b993b93b31a77e7645b84272bf6fd2e83b6a04`.
- New independent channel-binding oracle: predecessor **8/12**, V2 **12/12**, deliberate channel-unbound mutant **8/12**. Four negative fixtures target swapped PR/Issue permalinks and review-object masquerading.
- Historical frozen R10 V1 oracle: predecessor **20/20**, V2 **19/20**. The failed historical test `test_17_issue_comment_valid_ack` constructs an `issue_comments` record using a **PR permalink** and expects acceptance.
- Thus the historical oracle contradicts the newly explicit source-channel binding invariant. Do not rewrite either frozen oracle or integrate V2 until an independent, operator-governed compatibility adjudication is completed.

## Decision and falsifier

DECISION = CONTRADICTION_APPEND_C1
INTEGRATION = HOLD_SCOPED_INDEPENDENT_ORACLE_CONFLICT
REAL_R10_INDEPENDENT_RECEIVER_ACK = SOURCE_NOT_PRESENT_AUTHENTICATED
EXPERT_RESEARCH_ACTUALLY_EXECUTED = NOT_ESTABLISHED
PRODUCTION_RUNTIME_CHANGE = NO
HOSTINGER_WRITE = NO
MAIN_MERGE_AUTHORIZATION = NO

FALSIFIER: show a documented, authenticated GitHub API object whose source collection legitimately differs from its canonical issuecomment permalink while retaining reliable GitHub actor and comment identity. If found, source-channel matching must be re-specified rather than blindly enforced.

No external model identity, scientific acceptance, WWW parity or new authorization is inferred from these tests.
