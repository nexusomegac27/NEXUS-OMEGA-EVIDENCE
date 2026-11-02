# NEXUS OMEGA · Alpha-Node · GitHub API source readback V10 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_GITHUB_API_SOURCE_READBACK_V10_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_OFFLINE_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=4e22d346006b67de332bfeb1f0ea68db8412fd70
MAIN_IMMEDIATE_PARENT=c1aee5da5015e1108ceab049c7031180978c109d
PREDECESSOR_PR=281
PREDECESSOR_ISSUE93_RECEIPT=6566413038
FROZEN_EVALUATOR_FIRST_COMMIT=791b98a5b4583bf3ef2293e24314b2a85dba5c16
CANDIDATE_SECOND_COMMIT=d1acde6f03aead02da98c792cd65575da1796e24
PRODUCTION_INTEGRATION=NO
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

At the pinned `main`, V9 original `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_independent_git_blob_guard_v9_20261102.py` was fetched and independently reconstructed at **3,463 bytes**, SHA-256 `e848bf157ac56ae75fcb978ca4180836da4bab1067916614873152118617e18f`, Git blob `a2ba4c03cc824169c754c982bfe2b394e5258ef2`. V9 requires a supposedly independent trusted blob from its caller; if the producer controls both this argument and the source envelope, V9 cannot distinguish a jointly forged input. The predecessor's own report explicitly documents this limitation. No predecessor bytes were modified.

The current authority is `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha-Node contract, operator direct-publication rule, Task Anchor Norm, Repository Order Law and existing owner GitHub branch/PR/CI path. No new root or external actor write slot is used. Public-safe source code and synthetic fixtures only.

## NEGATIVE HYPOTHESIS / ONE ISOLATED CANDIDATE

**Hypothesis:** An attacker can jointly replace source bytes, SHA-256 and the purportedly trusted Git blob, causing V9 to accept a forged source. V10 removes the *caller-provided trusted blob* as the decisive reference. Its live path requests the exact `https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/contents/<path>?ref=<40hex-commit>` via read-only HTTPS, and cross-checks returned `path`, `type`, `size`, `encoding`, content bytes, Git blob and producer envelope SHA-256. Missing or divergent data fail closed. No user-provided API host or repository is accepted. The commit/path **must still be pinned independently of the producer**.

A separate explicit `--offline-fixture-test --fixture-response <file>` mode enables deterministic tests and returns only `FIXTURE_BOUND_C1_BYTES_ONLY`, never the live API status. This prevents offline fixture acceptance from being reported as authenticated GitHub retrieval. V10 neither authenticates the producer/actor nor proves branch ancestry, event-census completeness, source license or scientific truth. Git SHA-1 is a Git object identity check, not a standalone collision-security claim.

## PINNED EVALUATOR / INDEPENDENT TEST

Frozen evaluator was committed **before** the candidate at `791b98a5b4583bf3ef2293e24314b2a85dba5c16`; bytes **5,765**, SHA-256 `67536a0eb045561004663d684f04d1309a92c1b01a670048438290101d41d941`, Git blob `e61eb45de10f276a3736cf7d2942dc0ac67f4926`. Candidate at second commit `d1acde6f03aead02da98c792cd65575da1796e24`; bytes **6,327**, SHA-256 `4ba4e969cf0d8643915185bf5f05ca4ae93acde01854ba7ebc170683dc8ca39a`, Git blob `906614086b2e014e198b2324fe26669cc425607a`. The frozen evaluator was not modified after candidate creation. Both GitHub blobs were read back and matched the independently prepared local originals.

Reproduce (same directory):

```sh
python frozen_alpha_handoff_api_source_evaluator_v10_20261102.py alpha_handoff_github_api_source_guard_v10_20261102.py alpha_handoff_independent_git_blob_guard_v9_20261102.py
```

**Observed local result: 25/25 expected outcomes PASS**, stdout SHA-256 `fa9772663645f6db1b5a4de3df30294360e1e73ca33a50a4cb33d7e3ec86d360`. Of the 24 V10 cases, 22 were negative input/API-mismatch cases returning `NOT_COMPUTABLE`, one was the positive original fixture, and one was a deliberately co-forged offline API fixture accepted as a **falsifier**. The 25th case replayed V9 with a co-forged trusted blob and source and observed V9 acceptance as predicted. Each test runs the target in a separate Python subprocess. The evaluator is independent source code, but not independent external peer review.

A separate GitHub-source control read `index/v1/latest.json` at immutable `4e22d346006b67de332bfeb1f0ea68db8412fd70`: **871 bytes**, Git blob `4e957f463eda19734c1ab42c51bb4bb6cfa073d7`, SHA-256 `e186fec20065b9e774fc71bdbdc369f6e7ee8b40f48fb3ddc762e0ffd06b6961`. An offline fixture constructed from these verified source bytes passed; a modified source with newly computed SHA-256 and blob, compared against the unchanged independently pinned fixture, returned `NOT_COMPUTABLE`. The fixture wrapper was **locally constructed** and is not an original HTTP response.

| Measurable scoped criterion | V9 | V10 |
|---|---|---|
| Co-forged producer bytes + digest + caller trusted blob | 1/1 falsely accepted in replay | 0/1 accepted against fixed independent API fixture |
| Independent frozen subprocess evaluation | V9 baseline co-forgery replayed | 25/25 expected outcomes, offline |
| Genuine GitHub source bytes in offline control | Prior V9 original source known | 1/1 positive, 1/1 altered-source rejection |
| GitHub HTTPS live-mode E2E | NOT_EXECUTED | NOT_EXECUTED (local network unavailable) |
| Authenticated real handoff event census | NOT_COMPUTABLE | NOT_COMPUTABLE |

## FALSIFIER / DECISION / GOVERNANCE

A jointly forged **offline API fixture** and producer envelope are accepted (`FIXTURE_BOUND_C1_BYTES_ONLY`). This explicitly falsifies any claim that V10 can authenticate offline fixtures. In live mode, compromise of GitHub/TLS, a wrong operator-selected commit, or a legitimately committed malicious file could still yield matching bytes without establishing authorization or scientific validity. The real HTTPS path was **not executed** in this run; no production E2E or project-wide automation improvement is claimed. This candidate improves the isolated trust-boundary *design* and tested mismatch rejection, not the real 90% handoff metric.

R10 PR #115 remains open at head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; original detached manifest at `539d4bb33d2ba2c4895713c1bc437ece0743eeea` is 4,588 bytes, blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`. The current Issue #93 inbox census has 261 owner-authored comments, PR discussion 0 and reviews 0: no independently authenticated expert return observed. `PUBLIC_SEND` does not imply `INDEPENDENT_RECEIVER_ACK` or `EXPERT_RESEARCH_ACTUALLY_EXECUTED`.

No runtime/Hostinger/WWW write, new worker, merge-gate mutation, external actor registration, private transfer, original overwrite, model change or claim promotion. A main publication, if performed, requires separate CI, merge, immutable main byte readback and an append-only Issue #93 receipt. `BLOCKED_LANE != BLOCKED_SYSTEM`.
