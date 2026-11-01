# Return Channel · Least Privilege Plan · 20261030 R0

**OBJECT:** `NEXUS_OMEGA_RETURN_CHANNEL_LEAST_PRIVILEGE_PLAN_20261030_R0`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_INDEPENDENT_RECEIVER_PILOT_READINESS_20261030_R0`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**LIVE_ENROLLMENT:** `NOT_AUTHORIZED_THIS_ORDER`  
**DATA_ROUTE:** `GITHUB_ONLY`

---

## Preferred return channels (ranked)

| Rank | Channel | Privilege | Notes |
|------|---------|-----------|-------|
| 1 | PR #185 review comment or issue comment on same PR | `pull_requests: write` or comment capability on open draft PR | Preferred: no branch write; ACK as comment body + optional gist/CAS pointer |
| 2 | Dedicated GitHub Issue under Evidence repo (exchange lane) | `issues: write` | Use if PR comment policy blocks; still GitHub-only |
| 3 | Commit of ACK JSON on a receiver-owned fork branch + PR | fork write + PR create | Higher privilege; only if operator explicitly chooses |
| 4 | Hostinger / www / email / chat attach | — | **PROHIBITED** for this lane |

Manual Operator chat remains `PURE_WORK_ORDER_TEXT_ONLY` (pointer/handshake), not ACK custody.

---

## Least-privilege principal matrix

```text
PRODUCER (current) = nexusomegac27 (User) — Cursor session / owner
RECEIVER (required) = DISTINCT GitHub principal
RECEIVER ≠ PRODUCER
RECEIVER ≠ Cursor agent identity alone
```

### Candidate auth modes (operator chooses later)

1. **Outside collaborator (read + comment)** — Invite with Triage or Write scoped to commenting; no admin; no ruleset mutation.
2. **GitHub App installation** — App with `contents: read` + `pull_requests: write` (comments) on Evidence only; short-lived tokens; no org-wide admin.
3. **OAuth App (user-to-server)** — User scopes minimal: `public_repo` or fine-grained `Contents: Read` + `Pull requests: Read & Write` (comments).
4. **Fine-grained PAT** — Repository-scoped; expiration ≤ 90 days; Contents Read + Pull requests Write; never repo Admin.

```text
NO_NEW_AGENT_RIGHTS_FROM_CURSOR = REQUIRED
NO_RULESET_PATCH_FROM_CURSOR = REQUIRED
NO_CODEOWNERS_MUTATION_FROM_THIS_ORDER = REQUIRED
GRANT_REGISTER_REMAINS_EMPTY_UNTIL_OPERATOR_ENROLLMENT = REQUIRED
```

---

## ACK return payload location (canonical)

```text
PREFERRED_PATH_ON_SUCCESS =
  PR185 comment containing JSON conforming to RECEIVER_INDEPENDENT_ACK_SCHEMA_V1
OPTIONAL_FILE_PATH =
  research/communication/github-only-exchange-enforcement-20261029/RECEIPTS/RECEIVER_ACK_<UTC>_<principal>.json
FILE_COMMIT = only after OPERATOR Freigabe for receiver-authored commit
```

---

## Privilege escalation stop rules

```text
WENN Cursor invents collaborator invite / App install / PAT,
DANN FAIL — TYPE_C / OPERATOR only.

WENN Receiver ACK uses Hostinger or chat as custody,
DANN FAIL — DATA_ROUTE=GITHUB_ONLY.

WENN Producer self-ACK is labeled EXTERNAL_RECEIVER_ACK,
DANN FAIL — distinct_from_producer required.

WENN Legacy grant register is mutated for pilot without Freigabe,
DANN FAIL — F12 empty grants preserved until enrollment order.
```

---

## Disposition

```text
PLAN = BOUND_C1
ADAPTER = NOT_CONNECTED
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
NEXT = OPERATOR_SELECTS_AUTH_MODE_THEN_ENROLLS_DISTINCT_PRINCIPAL
```
