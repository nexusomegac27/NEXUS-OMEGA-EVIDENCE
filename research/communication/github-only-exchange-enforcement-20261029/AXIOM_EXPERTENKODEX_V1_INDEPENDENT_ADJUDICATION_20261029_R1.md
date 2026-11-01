# NEXUS OMEGA · AXIOM Independent Adjudication — Expertenkodex V1 R1

```text
OBJECT = NEXUS_OMEGA_AXIOM_EXPERTENKODEX_V1_INDEPENDENT_ADJUDICATION_20261029_R1
PARENT = NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0
EVIDENCE_COMMIT = c5a1b26e9a736d0fd643b4451fc56da32729920e
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
PR = 185
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_SOURCE_AND_CI_VERIFIED
TERMINAL_PASS = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
MANUAL_OPERATOR_DATA_TRANSFERS = PROHIBITED_BY_DEFAULT
NATIVE_APP_R3 = HOLD
DEVICE_INSTALL = PAUSED
CI_REQUIRED_ON_MAIN = NOT_ESTABLISHED
LIVE_EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
ADAPTER_NOT_CONNECTED = PRESERVED
```

## Independent source and integrity evidence

AXIOM fetched the actual files from GitHub pinned to `c5a1b26e9a736d0fd643b4451fc56da32729920e` and independently SHA-256 hashed UTF-8 payloads. A second raw-byte base64 GitHub API fetch corroborated the discrepant Task Anchor size.

| File | Observed bytes | Observed SHA-256 | Cursor-declared | Verdict |
|---|---:|---|---|---|
| `RESULT_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0.md` | 4272 | `f292d7c8a8b50853c47613cf5eb9e1076565e5a25ec80e9a11b6f9ebeb1b4a51` | 4272 / same | MATCH |
| `scripts/nexus_expertenkodex_validator.py` | 17321 | `ff465ba0989e03eba8aed0013d9738c454d93d37cf53b7091133cce720403173` | 17321 / same | MATCH |
| `tests/test_nexus_expertenkodex_v1.py` | 12258 | `22130de6663d162680628020adf6a5b78486749e2f17825e14140fc5bce7a824` | 12258 / same | MATCH |
| `.github/workflows/validate-repository-structure.yml` | 2936 | `02e89b11ccf24465c9700125faaa92c30691ee9fbe873a3800e8e5fa02bda045` | 2936 / same | MATCH |
| `.github/workflows/validate-anchor.yml` | 1608 | `9f217c3d43a7981bfcba27cff4f768fe31f6edb55a8aedc1cd59eee84c53b76c` | 1608 / same | MATCH |
| `NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_V1_ENFORCEMENT_20261029_R0_TASK_ANCHOR.json` | **2661** | **`92fc6aa510faa22c0023e400d5228eecfa2127fd414b098cbffa9742cbe5133b`** | **2720 / `aca0ae992a2d27849f7ba626ec6c73defc639968ee90fa417a71a921ede5b4f8`** | **MISMATCH_F10** |

**F10: Task Anchor declared identity mismatch**. GitHub's immutable source at the asserted commit differs from the reported anchor byte length and hash; this is an evidence mismatch, not proof of malicious modification. Do not repair original receipts retroactively; append an explicit discrepancy witness and a new correctly bound successor receipt, including exact source version and explanation when available.

## Independently verified GitHub CI

GitHub Actions workflow runs for exact commit `c5a1b26e9a736d0fd643b4451fc56da32729920e`:

- `validate-anchor` run `40953511346`, job `123727525759`: status `completed`, conclusion `success`, steps passed.
- `Validate repository structure` run `40953511183`, job `123727524733`: `completed / success`.
- GitHub job log for `123727524733` explicitly reports `Ran 40 tests ... OK` for `tests.test_nexus_github_exchange_chain` and `Ran 33 tests ... OK` for `tests.test_nexus_expertenkodex_v1`.

This is independently checked **GitHub-hosted CI execution evidence**, not a local AXIOM rerun and not proof of source semantics, external expert receipt, or required-branch-check enforcement. The combined commit-*status* endpoint returned no status entries, as GitHub Actions normally reports **check runs**, not legacy commit statuses (GitHub Docs: https://docs.github.com/en/pull-requests/reference/status-checks).

## F11: Mandatory codex dispatch bypass (code-observed)

At the same pinned commit, the implementation of `DispatchValidator` in `scripts/nexus_github_exchange_chain.py` runs `ExpertenkodexHeaderValidator().validate(...)` ONLY under this conditional:
```python
nested = manifest.get("expertenkodex") or manifest.get("expertenkodex_header")
has_top = any(k in manifest for k in ("EXPERTENKODEX", "CODEX_COMMIT", "CODEX_PATH", "CODEX_BYTES", "CODEX_SHA256"))
if nested is not None or has_top:
    ...validate(...)
```

When an incoming **new expert task manifest omits all codex fields**, the mandatory header check is skipped. Passing tests of the validator in isolation does not establish that the dispatch endpoint always calls it. This contradicts prospective universal law for new GitHub-capable expert orders. Historical task manifests may be exempt only via explicit authenticated, versioned, policy-defined legacy classification; **never** infer legacy status from absent codex fields. Add direct G2 dispatch tests with no codex keys and a full source manifest and require fail-closed `MISSING_EXPERTENKODEX_HEADER`.

## Remaining critical external preconditions

- The live external actor allowlist remains `DEFAULT_DENY`; no model display name constitutes an authenticated GitHub principal.
- No independently authenticated external-agent fetch/rehash/ACK was established; synthetic same-process results do not count.
- PR #185 remains DRAFT, not merged or enforced on `main`. A successful workflow run may be optional until verified branch rulesets require its check and owner review. No auto-merge or new permission grants from this adjudication.
- Operational 90-percent manual-transfer reduction not measured with real independent receipts.
- NEXUS App R3 remains HOLD until explicit later operator decision following the interface's actual end-to-end gate.

## Next narrow Cursor assignment

Perform one owner-controlled PR #185 scoped **follow-up**:
1. **F10** diagnose discrepancy (reported anchor 2720 bytes vs actual 2661 bytes), bind both versions with full SHA-256 and evidence, append correction witness and new return receipt; do not silently overwrite.
2. **F11** enforce mandatory codex header at the actual G2 dispatcher for **all new GitHub-capable expert mandates**. Add fail-closed bypass fixture and explicit authenticated grandfathering only where authorized. Do not break lawful historical returns by treating all old packages as new.
3. Preserve and independently verify the 40+33 existing cases, add new negative cases; use GitHub Actions run + job IDs tied to the exact new head.
4. Identify one actual independently authenticated external GitHub receiver candidate, but **do not grant rights, install apps, create principal or start live pilot** without a separate operator decision. If no authorized receiver: `ADAPTER_NOT_CONNECTED`, scoped hold.
5. Return **only** full Git commit, path, byte count, SHA-256, actual CI run IDs, true external ACK and remaining source gaps; do not request any file transfer from Operator.

Source rules: `AGENTS.md`, `GOVERNANCE.md`, `docs/AI_HANDOFF_PROTOCOL.md`, GitHub-only Law V2, Expertenkodex V1, Task Anchor Norm V1 and existing structural firewall have precedence. No new top-level folder, no R27-E slot reuse, no Hostinger/WWW write, no App R3 or installation, no auto-merge or claim C2+. Claim ceiling C1 only.

## Terminal

```text
DECISION = CURSOR_SCOPED_F10_F11_HARD_REMEDIATION
NATIVE_APP_R3 = HOLD
GITHUB_ONLY_DATA_ROUTE = REQUIRED
RECEIVER_INDEPENDENT_ACK = NOT_ESTABLISHED
TERMINAL_PASS = NO
NEXT = CURSOR_F10_F11_REPAIR_AND_INDEPENDENT_EXTERNAL_RECEIVER_CAPABILITY_CENSUS
```
