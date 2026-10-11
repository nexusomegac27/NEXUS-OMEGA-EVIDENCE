# NEXUS OMEGA — R28 Trusted-Base Pre-Entry Laboratory V1
## C1_DESCRIPTIVE_ONLY · Automated GitHub PR intake, not a WWW/Internal runtime ingress gateway

```text
OBJECT = NEXUS_OMEGA_AXIOM_R28_TRUSTED_BASE_GITHUB_PREENTRY_SANDBOX_LAB_V1_20261011_R0
PARENT = R27_PR84_MAIN_63945da53de7789315d79fe759e32eb6197b9fb7
OPERATOR_INPUT = NEXUS-~1.TXT + 3TCUB5~1.ZIP
CANONICAL_ENTRY_SCOPE = GITHUB_PULL_REQUEST_BEFORE_MERGE
NOT_YET_GATED = WWW_HTTP_INGRESS_AND_NEXUS_INTERN_RUNTIME
IMPLEMENTATION = EXISTING_R27E_WORKFLOW_AND_STRUCTURE_CI_PLUS_ONE_SCRIPT_AND_TEST_MODULE
GH_WORKFLOW = .github/workflows/validate-external-agent-pr.yml
UPSTREAM_CHECK = r27e-external-structural-firewall
NEW_CHECK = nexus-preentry-lab
NEW_STANDALONE_WORKFLOW = NO
NEW_TOP_LEVEL_DIRECTORY = NO
NEW_CURSOR_WORKER = NO
HOSTINGER_DEPLOY = NO
R27_AUTH001_002_003 = HOLD_SECURITY
CURSOR_CONTINUITY_RUN_ID = NOT_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## 1. Input adjudication

The supplied TXT is a multi-proposal source: a candidate GitHub Actions runner, an R28 external-agent MAXI order, external reference claims (OpenShell / CERN / Sigstore), and a proposal to add new `governance/`, `src/`, `research/_template/` trees. **Do not import its sample workflow verbatim**: its first sketch references absent `tests/sgp4-position.test.mjs`, `src/cli-selfcheck.mjs` and root `governance/RETURN_SCHEMA.json`, plus `npm ci` and unrestricted default runner networking; it would be nonreproducible against the actual canonical tree. Its examples also confuse GitHub Actions source testing with genuine inline HTTP ingress enforcement, and call hash receipts "forgery-proof" without a separately validated signing identity.

The ZIP is a **separate front-end demonstration application**, not the GitHub repository or an authenticated runtime. Physical inspection of `3TCUB5~1.ZIP` shows `src/lib/ledger.ts` implements a browser-only receipt ledger stored in `localStorage` and signs with an HMAC key **hard-coded inside the shipped browser module**: `nexus-broker-seal-v1-SIMULATED-NOT-PRODUCTION`. The sequence visualisation in `src/components/lab.tsx` advances using staged timer delays. These visuals may explain a workflow, but **cannot provide tamper resistance, authenticated agent identity, trusted timestamps, broker separation, independent signing, external runner isolation or a true pre-entry guarantee**. The ZIP also contains built Vercel outputs, many third-party packages and prior attachments. None is imported into the canonical GitHub repository, uploaded to Hostinger or passed to a runtime. Use only the original author's conceptual insight.

External reference: [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) documents genuine out-of-process runtime restrictions and secret brokering; it **is not installed in this GH workflow**. GitHub [pull_request_target hardening](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) warns never to execute untrusted PR content with a trusted base token. GitHub [artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) need trusted `id-token:write` and `attestations:write`. Neither of these permissions is delegated to external PR code in V1.

## 2. Actual automatically executing pipeline — reuse existing enforcement

```text
EXTERNAL OR OWNER PR TO MAIN
       |
       v
R27-E existing trusted-base firewall
  [GitHub authenticated actor; NEXUS-owned exact preallocated slots;
   pristine base checkout; live PR contents API; hashes/manifest/size;
   reject owner-incomplete returns and all unauthorized external edits]
       | success only
       v
R28 trusted-base ephemeral preentry lab (GitHub-hosted runner)
  [no PR-head checkout; contents:read; persist-credentials:false;
   no self-hosted nodes or secret input;
   19 independent synthetic negative tests that reuse R27-E source;
   existing R19 ORBIS manifest & SGP4 bridge native Node tests;
   bounded CLI-generated SHA256 input-binding receipt]
       | source test PASS_C1
       v
NORMAL REPO PR VALIDATIONS
       |
       v
OWNER/ADMIN GITHUB RULESET CHECK
       |
       v
MERGE *ONLY IF REQUIRED CHECKS ENFORCED*

NEITHER SUCCESS NOR MERGE ACTIVATES:
WWW_Extern HTTP control | Nexus_Intern privileged action |
Hostinger deployment | Cursor run | AUTH001/002/003 remediation.
```

This approach does not duplicate R27-E content validation, directory policy, or user identities. The existing script `scripts/validate_external_agent_pr.py` and the owner-controlled `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` remain the single enforcement source; the new `scripts/nexus_preentry_lab.py` uses only fixed offline commands and emits an informational receipt into the existing CI log. No PR comment bot, independent database, redundant feeds or extra persistent service.

## 3. Security truth table

| Feature | V1 state |
|---|---|
| GitHub PR-triggered ephemeral runner | Implemented in existing workflow (post-merge active for future PRs) |
| Trusted base / no PR-head code execution in privileged validator | Enforced in `pull_request_target` jobs |
| GitHub actor, paths, owner-approved file allowlist | Reused from R27-E validator |
| 19 synthetic adversarial input negatives | Executed by existing unprivileged structure CI on introduction, by trusted-base PR job after merge |
| R19 orbital *software contract* tests | Executed on base for future PRs, no observation-based orbit certification |
| Standalone signed tamper-proof receipt | NOT_IMPLEMENTED; SHA256 of input bytes is a digest, not signing |
| Network egress default-deny | **NOT_ENFORCED** by default GitHub-hosted runner; no false "airgap" claim |
| Full arbitrary-untrusted-binary runtime sandbox | NOT_IMPLEMENTED; no untrusted PR code executed |
| Inline WWW/Node ingress interception | NOT_IMPLEMENTED; HTTP traffic still has no inline supervisor |
| Required-merge enforcement via Ruleset 21252293 | **ADMIN_ACTION_REQUIRED** |
| Runtime AUTH001–003 | HOLD_SECURITY |
| N01–N12 Cursor run/resume tests from PR84 | DESIGN_ONLY, distinct from new PR preentry fixtures |
| Autonomous agent activation / operator privilege | NONE |

**Scope precision:** The public `pull_request_target` trigger checks GitHub API content with a privileged but strictly read-only token (read repository metadata and exact text). `persist-credentials:false` reduces token exposure in checked-out repository files, but the GitHub Actions platform still supplies an ephemeral job token to trusted steps. The separate preentry job has no own code needing a GitHub token, inherits no secret, and does no dynamic dependency installation. The hosted runner has outbound network connectivity: it must NOT be described as egress-denied. Avoid executing arbitrary incoming binaries, npm scripts, PR test shell code, `curl | sh`, unpinned third-party egress plug-ins or self-hosted runners in this lane. The PR author's ability to submit untrusted Markdown/JSON does not grant command execution.

## 4. What actually counts as a pre-entry gate

A newly added GitHub check is only **informational** until the operator or repository admin makes it *required* in existing ruleset `main-evidence-protection` ID `21252293`, alongside `r27e-external-structural-firewall` and CODEOWNERS review. At last AXIOM direct API readback, only `validate` was required, `required_approving_review_count=0` and `require_code_owner_review=false`. This is a concrete admin gap, not a research HOLD. Never declare `ENFORCED_BEFORE_MERGE` from a green check alone. The new job depends on R27-E success and fails closed if R27-E fails. For future zero-trust WWW entry, a separately authorized, out-of-process **runtime** gateway/sandbox (for example a pinned OpenShell-style supervisor or equivalent) is required. It must reject `origin`, `reviewer`, `trust` claims from user input and prove the R27 AUTH negative tests reject.

## 5. Acceptance and follow-up

- Main implementation can be **publicly merged under C1** once original GitHub PR workflows, 19 new sandbox fixtures, Node R19 tests, structure test suite and Semgrep succeed.
- In the first **future PR after main merge**, the `nexus-preentry-lab` status check must appear and contain an actual `NEXUS_ENTRY_LAB_RECEIPT_JSON` in its CI log; base hash / run id and SHA256 input bindings must be retrievable. This is an execution witness, unlike merely merging a workflow file.
- The operator's single existing Cursor Continuity remains focused on Homepage Ticker B2/B3 and then ORBIS P0. No launch of a new Cursor Agent, no new app/site, no additional folder or external return slot.
- Future *runtime ingress* implementation is a distinct scoped authorization and separate sandbox demonstration, not a claim from GH Actions CI. No publication of fake agent identities or private node state on WWW.

**C1 conclusion:** A GitHub-hosted pre-entry validation laboratory can be built immediately and automatically reused with the existing firewall at low incremental cost. It is not an always-on security daemon or total isolation, and does not replace authenticated real-world ingress control.

*NEXUS OMEGA — Beweise vor Rechten. Isolation am tatsächlichen Eintritt, nicht im erklärenden UI.*
