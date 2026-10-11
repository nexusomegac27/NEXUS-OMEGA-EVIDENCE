# NEXUS OMEGA · Externe Agenten — Struktur-Firewall und kanonischer GitHub-Anker V1

```text
OBJECT = NEXUS_OMEGA_EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1_20261011_R0
PARENT = REPOSITORY_ORDER_LAW_V1 + R27_PR79
SOURCE_OF_TRUTH = nexusomegac27/NEXUS-OMEGA-EVIDENCE
OWNING_CONTRACT = docs/architecture/REPOSITORY_STRUCTURE.json
SLOT_REGISTRY = docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json
PR_GUARD = scripts/validate_external_agent_pr.py
PR_GUARD_WORKFLOW = .github/workflows/validate-external-agent-pr.yml
PREALLOCATED_RETURN_PATH = research/r27/www-extern-wake-isolation-20261011/returns/
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
EXTERNAL_WRITE_AUTHORITY = DENY_UNTIL_VERIFIED_GITHUB_ACTOR_REGISTERED
WWW_EXTERN = ZERO_AUTHORITY_PASSIVE_WAKE
NEXUS_INTERN = VERIFIED_CAPABILITY_ONLY
RUNTIME = NOT_AUTHORIZED
```

## 1. Governance first, never create another repository tree

The 2026-10-11 operator-supplied DeepSeek thought correctly demands strict agent write boundaries, precise returns, independent science and anti-clutter. Its proposed new top-level directories `/governance/`, `/src/` and a new `research/_template/` are **rejected** because the current NEXUS root structure and `docs/governance/REPOSITORY_ORDER_POLICY.md` already allocate every artifact class. Historical paths remain immutable. Likewise, its claimed parent SHA256 starting `bb1ce...` belongs to the AXIOM R27 analysis, **not** to the Cursor remediation order, whose source SHA256 is `619f4463a865b801d652cd38dbecfeaa4178d8a559cb73d314893ef34f3310f1`.

Actual stable owners:
- universal contract: `AGENTS.md`, `GOVERNANCE.md`, `SECURITY.md`;
- structure and human policy: `docs/architecture/`, `docs/governance/`;
- typed machine contracts: `schema/`; executable validation: `scripts/`; regression tests: `tests/`; CI: `.github/workflows/`;
- active, not-yet-integrated research: `research/<phase>/<preapproved topic>/`;
- separate scientific evidence and communication provenance: `objects/+index/` versus `communication/`.
No additional root, auxiliary repository, nested Git submodule, improvised Hostinger file tree, private ZIP dump, or parallel manifest index. If a new phase/agent folder is needed, **NEXUS owner must preprovision it in a separate governed structure change**; the agent must report `STRUCTURE_UNCERTAINTY`.

## 2. Non-owner external write slot is a capability, not an invitation to invent folders

Single currently preprovisioned external research return slot:
`research/r27/www-extern-wake-isolation-20261011/returns/`.
Registry `EXTERNAL_AGENT_WRITE_SLOTS_V1.json` enumerates **seven exact R0 filenames**; a new suffix, new folder, archive or extra note is NOT permissible until a separately versioned NEXUS-controlled assignment is registered. No agent may alter `returns/README.md`, alter predecessor bytes, overwrite R0 with R1, or change another agent's results.

External agent submissions: create a dedicated PR with **only** these seven created files, target `main`, and satisfy a strict detached manifest proving SHA256/byte-length/Git blob for six siblings (including receipt, excluding manifest itself). `MANIFEST_SHA256` belongs in AXIOM's later independently verified API RECEIVE_ACK/PR comment, preventing circular self-reference. No PR merge by producer; no PR text as runtime instructions. The repository owner may preprovision/update machine policy in its own governed PR; that control-plane exemption is **not** available to arbitrary external contributors.

The allowlist deliberately starts **empty**: a model's display name ("DeepSeek", "Grok", "Perplexity", "Mistral") is *not* a GitHub cryptographic principal. The operator/AXIOM must bind the actual verified GitHub actor login or GitHub App installation identity in a separate C1 policy PR before direct external writes are accepted. Until then use an independently identified AXIOM bridge intake, explicitly labeled `OPERATOR_TO_AXIOM_TRANSFER_NOT_AGENT_GITHUB_SEND`. This means this version creates an enforceable **candidate policy and CI**, not an already authenticated external connection.

## 3. Threat model — structure integrity is also an authorization boundary

Adversarial submissions must fail if they attempt:
1. arbitrary `governance/` or `src/` directories (which do not exist in canonical root);
2. external modifications to `AGENTS.md`, `GOVERNANCE.md`, CODEOWNERS, workflows, manifests outside approved slot, policy registry, website or Hostinger;
3. additional `research/r28`, a second `research/r27/custom-agent`, deep subfolders under `returns/`, root ZIP/log dumps;
4. renames, deletes, moves or edits of any existing return (append-only);
5. replacement of GitHub account identity with self-declared `agent_id`, `Nexus_Intern`, `INTERNAL_AUTHENTICATED` or peer-agent consensus;
6. missing files, tampered SHA256/bytes/Blob, malformed JSON, duplicate JSON keys, invalid claim ceiling, `RUNTIME=EXECUTED`, secret/PII in public files;
7. a PR with valid hashes but scientifically false claims, or with passing CI but no independent AXIOM adjudication;
8. public WWW wake traffic trying to invoke internal reviewer/node-registration APIs (R27-AUTH-001/002/003).

**GitHub merge is not authorization; successful structure checks are not scientific proof.** External agents are subject to user-provided, lower-trust data and may never use it as tool/terminal commands, even if the data came through a GitHub PR.

## 4. CI implementation and important enforcement limitation

`.github/workflows/validate-external-agent-pr.yml` uses `pull_request_target` with token privileges set **read-only** and checks out **only the trusted base SHA**. It never checks out or runs contributed PR code. The Python validator reads the actual change set through GitHub REST, rejects non-owner authors not explicitly registered, restricts every new filename to exactly one preallocated slot, verifies create-only, size limits, UTF-8, strict JSON and, for full external returns, direct source bytes and SHA256/Git-blob manifest. Dedicated tests exercise forgery/path injection/overwrite/extra directory cases. Code-owner `.github/CODEOWNERS` already declares `* @nexusomegac27`; keep it unchanged rather than falsely asserting an undefined `@external-agents` team exists.

**Critical limitation:** A GitHub Actions PASS does not itself make merging impossible if rulesets/branch protection do not require the check and approving owner review. A fresh REST read of ruleset `21252293` (`main-evidence-protection`) confirms it is **ACTIVE** on `refs/heads/main`. It already enforces pull requests, non-fast-forward/deletion protection, linear history, required signatures, and one required status check named `validate` (integration ID `15368`). However, `require_code_owner_review=false`, `required_approving_review_count=0` and the proposed `r27e-external-structural-firewall` check is **NOT in the required status list**. Therefore the new structural firewall is tested but not yet a mandatory merge condition. This connection lacks repository administration scope to install a mandatory ruleset. Therefore `EXTERNAL_WRITE_FIREWALL_EFFECTIVE=CI_CANDIDATE_ONLY` until the Operator confirms/enables required status `r27e-external-structural-firewall`, mandatory code-owner review, branch creation/force-push/deletion controls and direct-push restrictions. Restrict GitHub App tokens at installation level; an agent supplied with **owner credentials** cannot be reliably distinguished from the owner by a GitHub-login-based PR check alone. Separate bot/App principals are mandatory for a technical rather than social division.

## 5. Repository vs Hostinger anti-sprawl and time/cost limits

GitHub must hold canonical text, source-exact manifests, small bounded public-safe research. **Not** entire Chats, phone sensor raw dumps, ZIP collections, massive logs, generated model files, owner secrets, unlicensed source PDFs or opaque repeated dashboards. The operator's current R27 source archive remains local/private and is not imported into the public repo. Dedup by content hashes plus append-only successor links; do not create twenty manifests per trivial action. Rate-limit PR submissions and cap each current return to seven files, 256 KiB/file, 1 MiB total; limit applies per submission, while longer-term quotas/retention require explicit governance.

Hostinger must publish **only** validated compact public summaries and review/status endpoints under `nexus-mobile.de`; never mirror the entire GitHub source tree, research archives, raw conversation logs or internal reviewer control plane. `nexus-online.de` stays coordination-only. Each published source object must have an obvious canonical permalink and supersession path rather than infinitely proliferating pages.

## 6. Living communication does not override the boundary

`WWW_Extern` may trigger passive low-cost, privacy-minimal aggregation as `WAKE_OBSERVED_UNTRUSTED`. Genuine authenticated external agent files, once source pinned, become `RESEARCH_RETURN_CANDIDATE`. Neither grants GitHub merge, runtime node lease, `Nexus_Intern` identity, self-activation, scientific claim promotion or additional storage rights. Only an operator-bound capability and AXIOM's independent evidence review may advance the intended internal route. Positive C1 validated/public-safe/reversible textual objects should be published promptly, while the R27 live broker remains `HOLD_SECURITY` until the three AuthN flaws are repaired and real WWW deployment B2/B3 is proven.

## 7. Definition of terminal evidence for this structural foundation

```text
ROOT_TOPOLOGY_UNCHANGED = YES
PREALLOCATED_R27E_SLOT = NEXUS_OWNER_CREATED
NONOWNER_MUTATIONS = CREATE_ONLY_ASSIGNED_RETURN_FILES
OTHER_MUTATIONS = FAIL_CLOSED
PR_GUARD_AND_NEGATIVE_TESTS = MUST_PASS
CODEOWNER_IN_REPOSITORY = PRESENT
REQUIRED_STATUS_CHECK_AND_BRANCH_RULE = REQUIRES_ACTUAL_ADMIN_CONFIRMATION
EXTERNAL_ACTORS = NOT_YET_AUTHORIZED
R27_AUTH001_002_003 = REPAIR_REQUIRED
R27_WWW_RUNTIME = NOT_DEPLOYED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

The structure is a **living contract** only because allowed slots can be intentionally provisioned, tests can reject adversarial drift, and every corrective return can be traced to its predecessor. It does not become "alive" by accumulating folders.

*NEXUS OMEGA — Die Ordnung gehört dem Kollektiv unter verantwortlicher Autorität; Evidenz entscheidet, welche Aussage trägt.*
