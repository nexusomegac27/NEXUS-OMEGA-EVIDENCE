# R26 · GitHub-only deterministic two-sided transport handshake R0

```text
OBJECT = NEXUS_OMEGA_R26_GITHUB_ONLY_HANDSHAKE_PROTOCOL_20261010_R0
DATE = 2026-10-10
PARENT = NEXUS_OMEGA_AXIOM_R26_FUNDAMENTAL_MAXI_RESEARCH_ORDER_20261010_R0
ROOT = nexusomegac27/NEXUS-OMEGA-EVIDENCE
TRANSIT = GITHUB_CONNECTOR_API_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
AUTHORITY = OPERATOR_SCOPED
GITHUB_READ = AS_AUTHORIZED
GITHUB_WRITE = AS_AUTHORIZED_FOR_RESEARCH_BRANCH_ONLY
MERGE = NOT_AUTHORIZED_BY_THIS_PROTOCOL
PROD_DEPLOY = NO
```

## Design scope

This document is an executable **contract specification**, not proof that remote worker processes or API daemons have been deployed. It is designed for an approved external agent and AXIOM; Cursor's existing bind remains independent. Delivery, receipt and adjudication live in GitHub's API; chat only supplies lightweight human-readable notifications.

This protocol is **not** a general instruction to any agent with a token to write the repository. The Operator must scope write authorization, repository, branch, source/target and file classes; the agent must be explicitly assigned. If connector write permission is absent, the truthful return is `GITHUB_WRITE_CAPABILITY_GAP`, not a pseudo-handoff.

## Immutable object design

A `source_pin` identifies `repository_full_name`, `commit_sha`, `repo_path`, `git_blob_sha1`, `byte_count`, `sha256`, `source_role`, `source_time`, `api_readback_time` and `evidence_scope`. GitHub SHA-1 identifies the Git blob, **not** SHA-256; do not interchange them.

A `request_key` uses `OBJECT` + explicit version + named receiver + source manifest hash. Equal key + equal payload is a replay/duplicate ACK; equal key + divergent payload is `IDEMPOTENCY_CONFLICT_HOLD`. The key is not a cryptographic signature. Do not compute it before the actual manifest exists.

The `return_manifest` lists all finalized child assets, exact sizes/SHA-256, Git blob SHA-1, component verdict, whether executed and source pins. It does not contain its own hash. A final detached `send_receipt` refers to the manifest by SHA-256 and Git commit. If the detached receipt is itself an asset, publish it after the manifest and only append a hash-of-receipt in the receiving comment; avoid self-reference.

The `ack_receipt` from the recipient is a **new GitHub API comment or independent object**, acknowledging exactly the branch HEAD, commit, manifest ID and observed checks. Receipt `ACCEPTED_BYTES` does not mean `ACCEPTED_SCIENCE`.

## State machine / allowed transitions

| From | To | Required independently checkable event | Fail on |
|---|---|---|---|
| `H0_UNPINNED` | `H0_PINNED` | bootstrap governance + exact known source commits | branch name alone |
| `H0_PINNED` | `H1_ORDER_REFERENCED` | existing order + parent SHA + authorized agent identity | missing authority |
| `H1_ORDER_REFERENCED` | `H2_UPLOAD_OPEN` | authorized clean research branch API-created from inspected base | PR67 history as ancestor |
| `H2_UPLOAD_OPEN` | `H3_ASSETS_COMMITTED` | all required assets via API, read back by immutable commit and hashed | partial/inconsistent files |
| `H3_ASSETS_COMMITTED` | `H4_MANIFEST_COMMITTED` | manifest generated from observed committed file bytes; hash separately | forward references or missing file |
| `H4_MANIFEST_COMMITTED` | `H5_SENT` | branch/PR API record and detached send receipt refer to exact manifest | fake PR, stale HEAD |
| `H5_SENT` | `H6_RECEIVED` | independent recipient re-fetch, byte checks, append-only API ACK | self-ACK or hash mismatch |
| `H6_RECEIVED` | `H7_ADJUDICATED` | AXIOM explicit scoped verdict with negative evidence | borrowed authority |
| `H7_ADJUDICATED` | `H8_PUBLISHED` | separate release approval, CI and privacy/source gates | inferred merge right |
| `H7_ADJUDICATED` | `H9_SUPERSEDED` | versioned new object pointing to prior hash | silent overwrites |

`H0→H6` may be completed for a draft public-safe research handoff without merger. `H8` means authorized publication/release only; a GitHub PR does not guarantee it.

## Strict API sequence (illustrative, NOT proof of background execution)

1. Query GitHub API for `main` commit and bootstrap governance. Do not assume old `index/v1/latest.json` is current.
2. Fetch relevant parents by immutable SHA and record observed SHA-256 and Git blob ID.
3. Create `research/r26/<named-expert-or-topic>/` on an approved clean branch from main.
4. Upload candidate files through the connected GitHub file API. If a tool cannot support binary bytes, do not base64-transform a ZIP into Markdown and claim exact delivery; report capability gap.
5. Read all files back from final immutable commit; validate required asset set, actual bytes, newline normalization, utf8, line-ending acceptance, JSON keys and independent SHA256.
6. Generate and commit manifest **after** file set stable, reread and hash manifest on the resulting immutable commit.
7. Open a PR via the authorized API; include the order object, manifest SHA256 and source commit, scope `NO_MERGE_WITHOUT_AUTHORITY`.
8. Publish send receipt via API comment (public-safe only). The send receipt may also be a separate file on the research branch if immutability is preserved, with its own versioned SHA.
9. Recipient independently re-fetches by commit and emits GitHub API `RECEIVE_ACK` referencing actual hashes and errors, not opinion.
10. AXIOM adjudicates within C1, recording `PASS`, `PASS_WITH_CAVEATS`, `HOLD_SCOPED` or `FAIL` in a separate API record.
11. Future versions follow `supersedes`; do not amend past citations. Do not write to `main` until separately authorized gates pass.
12. Existing Cursor R24/R25 continuity receives an advisory only on an already existing suitable GitHub PR/comment thread, without a new worker or unrequested execution.

## Named failure states

`SOURCE_NOT_PRESENT`, `NOT_DIRECTLY_READ`, `BAD_UTF8`, `BYTE_SIZE_MISMATCH`, `SHA256_MISMATCH`, `GIT_BLOB_MISMATCH`, `JSON_DUPLICATE_KEY`, `DECODE_NORMALIZATION_CHANGE`, `HTTP_401_403_UNAUTHORIZED`, `RATE_LIMIT_RETRYABLE`, `HTTP_404_NOT_FOUND`, `STALE_HEAD_CONFLICT`, `PARTIAL_UPLOAD`, `MANIFEST_CHILD_GAP`, `DUPLICATE_SAME_HASH`, `IDEMPOTENCY_CONFLICT_HOLD`, `SELF_VALIDATION_RISK`, `PRIVACY_HISTORY_CONTAMINATION`, `WRONG_PARENT`, `AUTHORIZATION_SCOPE_FAIL`, `BROWSER_PROOF_ABSENT`.

**Retries:** ONLY for authorized recoverable GET or safe/idempotent attempt with preflight remote readback; do not retry uncertain POST/merge without readback. No implied unattended scheduling, worker persistence or secret-store entitlement. A state-dependent automation may be separately engineered and authorized; this order does not create it.

**Security:** never echo token, private conversation, account-specific information or unredacted logs into public comments. Git history is an immutable exposure domain in ordinary PR workflows; deleting current files does not remove earlier publicly visible commits. Any remediation plan for existing PR67 history requires separate privacy/security adjudication. Do not solve it with unapproved force-push.

## Minimal send receipt (append-only)

```json
{
  "object": "NEXUS_OMEGA_R26_SEND_RECEIPT_<DATE>_R0",
  "protocol": "R26_GITHUB_API_HANDSHAKE_PROTOCOL_20261010_R0",
  "repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
  "order_object": "NEXUS_OMEGA_AXIOM_R26_FUNDAMENTAL_MAXI_RESEARCH_ORDER_20261010_R0",
  "order_sha256": "TO_BE_FILLED_FROM_API_READBACK",
  "expert": "ACTUAL_ASSIGNED_EXPERT_OR_UNASSIGNED",
  "authority_scope": "RESEARCH_BRANCH_ONLY",
  "branch": "ACTUAL_EXPERT_BRANCH",
  "commit_sha": "ACTUAL_COMMIT_40_HEX",
  "manifest_path": "ACTUAL_PATH",
  "manifest_sha256": "ACTUAL_SHA256_64_HEX",
  "asset_count": 0,
  "verified_asset_count": 0,
  "parent_r25_cursor_terminal": "PENDING_ACTUAL_CURSOR_RECEIPT",
  "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
  "production_write": false,
  "new_cursor_worker": false,
  "science_verdict": "PENDING_AXIOM",
  "delivery_state": "EXAMPLE_NOT_SENT"
}
```

Use `RETURN_CONTRACT.json` for machine-specified minimum fields; literal placeholder strings in this example MUST NOT be mistaken for a valid real send receipt.

*NEXUS OMEGA — Hash identifies exact bytes; evidence decides what they show.*
