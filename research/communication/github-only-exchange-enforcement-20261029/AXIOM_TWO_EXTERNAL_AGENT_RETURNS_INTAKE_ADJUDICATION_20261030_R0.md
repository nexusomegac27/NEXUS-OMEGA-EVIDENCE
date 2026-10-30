# NEXUS OMEGA · AXIOM · Two external agent reports · independent intake adjudication 2026-10-30 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_TWO_EXTERNAL_AGENT_RETURNS_INTAKE_ADJUDICATION_20261030_R0
PARENT_ORDER = NEXUS_OMEGA_AXIOM_EXTERNAL_EXPERT_INDEPENDENT_GITHUB_RECEIVER_PILOT_ORDER_20261030_R0
EXPERTENKODEX = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_GITHUB_COMMUNICATION_20261029_V1
SOURCE_PR_HEAD = af6d0fc8a031cfc1272bf4bb2a3da9e25cd998bd
PR = 185 OPEN_DRAFT_NOT_MERGED
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_TWO_REPORTED_SOURCE_REHASHES_NO_EXTERNAL_ACK
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
OPERATOR_UPLOADS = NON_CANONICAL_CHAT_INTAKE
EXTERNAL_DATA_CHANNEL_RETURN = NOT_OBSERVED
RECEIVER_ACK = NOT_ESTABLISHED
NATIVE_APP_R3 = HOLD
AUTO_MERGE = NO
```

## 1. Intake provenance and exact operator-upload hashes

The Operator supplied three files as **manual conversation attachments**, which is not the required GitHub-only data return route. AXIOM independently calculated SHA-256 of these received original file bytes. Their filenames are untrusted upload names; bytes/hashes are evidence identities only. Do **not** convert these attachments into authenticated GitHub delivery simply by re-uploading them, and do not falsely classify this as a scientifically necessary/manual-transfer exception.

| Report source / upload basename | Bytes | Operator-upload SHA-256 | Source class |
|---|---:|---|---|
| `NEXUS_~1(10).JSO` | 20610 | `5763189e6348ef9dd02b389889fec6aaefa07929b2b88c8310e76ede69f0482e` | Z.ai GLM process JSON, operator-supplied |
| `NEXUS_~1(20261030-152833).MD` | 12586 | `e50d4479bf400ac8a1efdac71150f26dafec318d27670508350ab1a236c3b378` | Z.ai GLM process documentation, operator-supplied |
| `NEXUS-~1(20261030-152834).MD` | 17721 | `b437a2c0f8fbc2010bdcdecbc84d7fa7505298dfc7af13334ea42064b000ca73` | Mistral/Vibe report, operator-supplied |

No external-authenticated Github comment/PR/file receipt exists for these reports at review time. This adjudication is an **AXIOM-derived metadata record** of observed chat intake and independent GitHub readback, not a replacement for direct external data return.

## 2. Z.ai GLM · precise outcome (from supplied JSON + markdown)

- Agent reports own independent Linux sandbox, anonymous Git clone at exact commit and `raw.githubusercontent.com` second fetch route, six obligatory objects **6/6 declared bytes/SHA256 MATCH**: Order 11023, anchor 7933, codex 15388, Source01 6512, Source03 7137, Source04 5256.
- JSON and markdown agree on `IDENTITY_HOLD_PRODUCER_OR_UNVERIFIED`: no independently authenticated GitHub login/ID, no token or Github CLI. Anonymous access is sufficient to fetch public source bytes but **not** to satisfy distinct authenticated receiver requirement.
- Local negative controls reported one bit flip and one byte truncation, both detected. Additional six adjudication-linked references reported match.
- `ACK_FAIL_AUTH_NOT_ESTABLISHED`; draft ACK objects kept local, no Github return location, no `ACK_PASS`; `ACK_HOLD_RETURN_CHANNEL_NOT_AUTHORIZED`.
- Raw.githubusercontent.com and Git clone are two retrieval paths to the same GitHub-hosted source, not independent platforms or authenticated receiver identities. A GitHub HTTP 403 via an anonymous rate-limited API is not evidence of access entitlement.

## 3. Mistral/Vibe · precise outcome (from supplied report)

- Reports own TypeScript SHA-256 including known-answer tests and six mandatory pinned source bytes/hash MATCH; two local one-byte negative controls detected.
- GitHub connector session principal is **`nexusomegac27`**, reportedly numeric ID 281316431; this equals producer/owner identity. No distinct authenticated external receiver principal.
- Correctly declines to use Owner connector as external PR-185 comment author; `ACK_FAIL_PRINCIPAL_NOT_DISTINCT` and `ACK_HOLD_RETURN_CHANNEL_NOT_AUTHORIZED`.
- Its source access and hash calculation are reported as independently executed work, but account identity remains **owner-mediated**. A model name ≠ a separate authenticated GitHub principal.
- No PR-comment return; draft ACK is present only in chat-uploaded report and is not a canonical GitHub receiver receipt.

## 4. AXIOM independent GitHub source readback

At `af6d0fc8a031cfc1272bf4bb2a3da9e25cd998bd` the GitHub connected API currently confirms:
```text
PR185 = OPEN_DRAFT_NOT_MERGED
HEAD = af6d0fc8a031cfc1272bf4bb2a3da9e25cd998bd
CHECK_RUNS = 9_OF_9_COMPLETED_SUCCESS
PR_ISSUE_COMMENTS_COUNT = 0
PR_REVIEWS_COUNT = 0
ORDER_BLOB_SHA1 = 53794a34b61eb2f49728fd9a8a35d82a7d845295
TASK_ANCHOR_BLOB_SHA1 = b14cdef99ed20a8efc09d275f0174251c9ebdbe8
```

The original order (Git commit `5246032a11e32f97ff23e39b461125f52e145093`) and anchor (Git commit `af6d0fc8a031cfc1272bf4bb2a3da9e25cd998bd`) are accessible directly from GitHub with the pinned Git blob identities. Prior AXIOM independent SHA256 checks for original order, anchor, codex and sources remain valid. **Published original source byte identity != third-party report provenance.**

## 5. Joint comparative adjudication

- `SOURCE_INTEGRITY_CONFLICT=NONE_OBSERVED`: two reported, materially different receiver environments reproduce the same pinned public source hashes and local mutation detection. This supports *reported methodological reproducibility*, not independent GitHub-authenticated delivery.
- `GH_AUTHENTICATED_RECEIVER=0_OF_2`; `GITHUB_RECEIVER_ACK=0_OF_2`; `GITHUB_RETURN_DELIVERY=0_OF_2`.
- Both agents correctly fail closed instead of promoting themselves to ACK_PASS. Z.ai has no authenticated GitHub principal; Mistral uses the Owner principal.
- The in-chat attachments are **not** a compliance exception and cannot count toward `GITHUB_ONLY_DATA_TRANSFER_COMPLETE` or operational >=90% manual reduction.
- No claim C2+, no external write slot registration, no model consciousness/identity promotion.
- No broad replay of existing F10/F11/F12 test suites necessary absent a new defect.

## 6. Next authorized stage (operator-controlled separate permission)

One distinct, authenticated external Github principal must be bound to the actual expert runtime with lawful least-privilege commenting/return capability. The owner must explicitly authorize the identity/permission arrangement; neither external model label nor Cursor Owner session grants it. Where feasible, a **separate existing account** with current PR comment rights is preferable to new secret distribution; a GitHub App with separate installation identity may be considered by owner, with source-exact run identity and non-producer execution proof.

A PR-185 comment must be authored under that distinct Github principal and carry the nonce-bound source exact rehash witness. Then AXIOM must independently verify the actual author, object IDs, hashes and execution context. Do not equate an asserted comment field with actual authentication. No new GitHub accounts, tokens, app installs, invites, ruleset changes, merging or WWW writes are authorized by this audit.

```text
TERMINAL = SCOPED_CAPABILITY_HOLD_REAL_RECEIVER_NOT_ENROLLED
ZAI_GLM = SOURCES_MATCH_REPORTED_IDENTITY_HOLD
MISTRAL_VIBE = SOURCES_MATCH_REPORTED_OWNER_PRINCIPAL_HOLD
GITHUB_COMMENTS = ZERO
GITHUB_EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
EXPERTENKODEX = SOURCE_BOUND_V1
PR185 = OPEN_DRAFT
NATIVE_APP_R3 = HOLD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = OPERATOR_ENROLL_DISTINCT_GITHUB_PRINCIPAL_THEN_REPEAT_ONLY_REAL_RECEIVER_STEP
```
