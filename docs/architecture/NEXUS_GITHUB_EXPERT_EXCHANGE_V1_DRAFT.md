# NEXUS OMEGA · GitHub Expert Exchange V1 (C1 candidate)

OBJECT = NEXUS_OMEGA_AXIOM_GITHUB_EXPERT_EXCHANGE_FOUNDATION_20261029_R0
STATE = OWNER_BRANCH_DESIGN_CANDIDATE_NOT_DEPLOYED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
APP_R3 = HOLD
EXTERNAL_DISPATCH = NOT_ESTABLISHED
CLAIM_PROMOTION = FALSE

## Purpose

Eliminate operator-mediated file hunting by making source-exact expert mandates discoverable through GitHub. Extend, do not replace, existing `research/pipeline/`, `communication/`, `objects/`, `index/`, `docs/governance/`, `schema/`, `scripts/`, `tests/` and `.github/workflows/` infrastructure. The existing `research/pipeline/POLICY.md`, `docs/AI_HANDOFF_PROTOCOL.md`, repository order policy, task-anchor norm, structural firewall and actor write-slot registry remain authoritative.

A GitHub link, CI PASS, hash MATCH or webhook delivery is not evidence of expert receipt, execution, scientific truth, merge, production deployment or external agent capability.

## Canonical handoff graph

```
OWNER_SOURCE_CENSUS
  -> PREDECESSOR_GRAPH_CLOSURE
  -> SOURCE_CLASSIFICATION_PUBLIC_SAFE
  -> REPRODUCIBLE_MANIFEST_SEAL
  -> OWNER_REVIEW
  -> IMMUTABLE_GIT_COMMIT_AND_SHA256
  -> GITHUB_EXPERT_DISPATCH
  -> EXPERT_FETCH_AND_INDEPENDENT_REHASH
  -> RECEIVER_IDENTITY_BOUND_ACK
  -> BLIND_INDEPENDENT_REVIEW
  -> OWNER_CONTROLLED_RETURN_INTAKE
  -> AXIOM_ADJUDICATION
  -> OPERATOR_DECISION
```

The dispatcher MUST NOT label a task `READY_FOR_EXPERT` unless all **required** parent objects and input bytes are retrievable at full immutable commit/ref, exact path, size and independent SHA-256 by the intended receiver. An inaccessible private source, a dangling manifest file, an unpinned `latest` path or a mismatched digest produces `SOURCE_GAP_BLOCKED` / `FAIL_CLOSED`, never implicit reconstruction.

Manifest records must identify exact `OBJECT`, `PREDECESSOR`, `AUTHORITY`, `CLAIM_CEILING`, effective errata, lane / return namespace, policy version, commit SHA, path, byte length, SHA-256, source classification and actual recipient. ZIP checksums are complete for contained payload paths, excluding only the checksum manifest itself. Detached container hash and receiver hash are independently recomputed; no claim of remote verification from producer-side sums.

## Security / governance

- Public GitHub branches and draft PRs are public. Only public-safe, rights-cleared descriptions or source references enter the public evidence repository. Raw phone/GPS/IMU data, private host paths, secrets and unlicensed payloads are excluded.
- External-agent registry currently defaults DENY. A model name is not a GitHub principal; an external write requires operator-registered GitHub actor/App installation and owner-preallocated create-only slot. Never reuse owner tokens for external agents.
- GitHub Apps: minimum required read/write scopes, expiring installation tokens and dedicated key custody. No embedded private signing keys.
- Webhook receivers must verify GitHub HMAC over raw payload, scope event/action, persist idempotent event processing, quickly queue work and reconcile periodically via GitHub API. GitHub does not automatically retry failed deliveries.
- No privileged `pull_request_target` job executes PR-provided code. Verify trusted-base policy and enforce required branch checks + code-owner review before external write activation. Do not merge, install or deploy from this candidate alone.
- Keep blind expert first passes isolated and return claims typed `DIRECT_BYTES`, `PUBLIC_PRIMARY_SOURCE`, `EXECUTION_OBSERVED`, `CURSOR_REPORTED`, `INFERENCE`, `SOURCE_NOT_PRESENT`.
- GitHub Actions run artifacts expire under retention rules; Git commit references or suitably governed immutable releases are the evidence anchors, and independently rehashed receivers remain mandatory.

## Staged rollout

F0: offline fail-closed archive verifier with synthetic positive/negative tests and a real operator-provided missing-path regression. **F0 is local evidence, not deployed in this PR.**

F1: owner-controlled draft PR integrating the verifier into the existing `scripts/` + `tests/` domains, versioned dispatch contract in `schema/`, and existing repository policy CI. Do not create another root or repository.

F2: one **synthetic** authorized expert lane with pinned GitHub fetch, source closure, independent receiver SHA-256 + identity ACK and owner-controlled return. External provider runtime must actually exist and be authorized; chat-only agents without adapter remain `ADAPTER_NOT_CONNECTED`.

F3: expand to E01–E10 only after per-lane receipts, recovery from failed webhook, source privacy review and verified branch protection. Native App R3 still needs a separate operator decision.

## Measurable acceptance

All required files present at declared paths; 0 accepted mismatches; 0 unauthorized external writes; 0 public private-data leaks; independently fetched bytes/commit/sha256 on every counted receiver ACK; no fake completion from a URL; recovery from lost webhook; measured reduction in operator file hunts versus a declared baseline (90% is a target, not a result).

## Source anchors

- GitHub App authentication: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app
- Webhook best practices and non-automatic redelivery: https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks and https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries
- GitHub Actions untrusted PR safety: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- Immutable releases: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
- Artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations

Status: **DESIGN_ONLY; NOT DEPLOYED; NO EXTERNAL EXPERT DISPATCH; C1_ONLY.**
