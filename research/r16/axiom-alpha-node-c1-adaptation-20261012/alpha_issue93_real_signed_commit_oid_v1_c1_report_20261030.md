# AXIOM Alpha-Node — real signed Git commit OID reconstruction · 2026-10-30

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_REAL_SIGNED_COMMIT_OID_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 3ce61de8adaa7257fbf281b869b6b097439b03e3
PREDECESSOR_PR = 207
PREDECESSOR_ISSUE93_RECEIPT = 6513702443
TARGET_COMMIT = b76994d0e431949e03e37d32ea45e179034550f8
TARGET_PARENT = 8ce99dd243c6d3450ddaa7308a0fc4c5d52c71cc
TARGET_TREE = 3a2e8300090345a1fa6ac6b4263431247af42bab
RAW_GIT_OBJECT_DIRECT_FETCH = NOT_ESTABLISHED
API_DERIVED_RECONSTRUCTION = TESTED_MATCH
PGP_SIGNATURE_INDEPENDENT_VERIFICATION = NOT_EXECUTED
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED

## 1. One bounded falsifiable gap

PR #207 independently reconstructed four actual GitHub tree objects and one file blob, but explicitly left the signed commit object's SHA-1 reconstruction untested. This iteration selects only that gap. It does not alter any historical tree validator, existing oracle, CI, registry, running service or website.

Negative hypothesis: the GitHub API's verification.payload and verification.signature cannot be reassembled into a Git signed-commit object whose Git SHA-1 equals the advertised commit OID. Any mismatch or an accepted one-byte corruption would falsify the scoped improvement.

## 2. Original API source and reconstruction

Source: https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/git/commits/b76994d0e431949e03e37d32ea45e179034550f8

At the immutable commit, the GitHub API provided a 460-byte unsigned payload, 801-byte PGP signature text, verification.verified=true, root tree 3a2e8300090345a1fa6ac6b4263431247af42bab and parent 8ce99dd243c6d3450ddaa7308a0fc4c5d52c71cc. The exact payload and signature strings are in the new additive JSON witness.

The reconstruction inserts the multiline gpgsig header before the header/body separator, prefixing every continuation line with a space (including the terminal newline continuation). Reconstructed commit content: 1,285 bytes. Git object framing: ASCII "commit 1285", a NUL byte, then those content bytes. Independently computed SHA-1: b76994d0e431949e03e37d32ea45e179034550f8 — MATCH.

Two separate implementations agree: JavaScript SHA-1 checked against the standard "abc" test vector, and Python hashlib.sha1 in the isolated frozen evaluator. A trimEnd() reconstruction of the signature does not match the expected OID, demonstrating the importance of exact serialization.

This is an API-derived reconstruction, not an independently fetched raw Git object, independent PGP signature verification, GitHub actor authentication or scientific adjudication.

## 3. Frozen evaluator and negative evidence

The additive frozen_alpha_issue93_real_signed_commit_oracle_v1_20261030.py was committed before the witness. It imports neither the previous tree validator nor its evaluator and was tested in a local isolated subprocess.

- Synthetic selftest: 12/12 PASS (one positive, eleven negative, including duplicate JSON key, changed commit/tree/parent/message/signature, missing signature, CRLF, invalid envelope/OID).
- Actual API-derived witness: 1/1 MATCH, 1,285 reconstructed bytes.
- Four real-witness mutations (signature character, expected parent, expected tree, message): 4/4 FAIL_CLOSED with the expected diagnostic.
- Actual witness subprocess outcomes: 5/5 PASS (one positive, four negative).

Reproduction, after fetching the two exact immutable GitHub files:

    python frozen_alpha_issue93_real_signed_commit_oracle_v1_20261030.py --selftest
    python frozen_alpha_issue93_real_signed_commit_oracle_v1_20261030.py < alpha_issue93_real_signed_commit_witness_v1_20261030.json

## 4. Before / after and project metrics

| Scoped measurement | Previous PR #207 | This candidate |
|---|---|---|
| Actual signed commit OID reconstructed and rehashed | 0 | 1/1 MATCH |
| Reconstructed commit bytes | Not established | 1,285 |
| Real signed-commit negative fixtures | 0 | 4/4 rejected |
| Separate Python synthetic selftest | Not available for this case | 12/12 PASS |
| Direct raw Git object fetch | Not established | Still not established |
| Independent PGP verification | Not established | Still not established |
| Production integration | No | No |

The complete authenticated denominator of accessible, routine, public, authorized handoff attempts, including failures, is absent. AUTOMATION_RATE=NOT_COMPUTABLE; PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE. No private/local handoff counts as automated success.

Owner-governed additive C1 research publication only. No new root, path migration, external write slot, Cursor dispatch, R10 merge, Hostinger or runtime change, evaluator self-approval, history overwrite, or claim promotion. Merge, main and Issue #93 receipt must be separately read back.

## 5. R10 passive readback

PR #115 remains open, API head dab7c59070d67e7e2a244bd6d05db9a4d37460e3, with 0 PR comments, 0 reviews and 0 review threads in the queried GitHub surfaces. The immutable historical head is 539d4bb33d2ba2c4895713c1bc437ece0743eeea. Owner-authored updates are not independent expert returns.

PUBLIC_SEND=OBSERVED; INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED; AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED; AXIOM_SCIENTIFIC_ADJUDICATION=NOT_ESTABLISHED; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED.
