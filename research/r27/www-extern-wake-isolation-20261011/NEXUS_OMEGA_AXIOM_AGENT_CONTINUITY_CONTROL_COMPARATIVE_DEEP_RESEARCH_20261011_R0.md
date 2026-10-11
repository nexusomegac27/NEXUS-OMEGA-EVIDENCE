# NEXUS OMEGA · AXIOM · Agent Continuity & Control — Comparative Deep Research R0
### 11 October 2026 · direct primary-source review · no new worker, directory or runtime

\`\`\`text
OBJECT = NEXUS_OMEGA_AXIOM_AGENT_CONTINUITY_CONTROL_COMPARATIVE_DEEP_RESEARCH_20261011_R0
PREDECESSOR = R27_PR83_MAIN_11c6860b563d5030a7f6d4b91113526f8229306f
PARENT_MODULE = examples/nexus-public-update-ticker-v1.mjs
TRIGGER = OPERATOR_REQUEST_TO_STUDY_HOW_OTHER_AI_AGENT_SYSTEMS_INTEGRATE_AND_CONTROL_OWN_AGENTS
CLASS = COMPARATIVE_EXTERNAL_PRIMARY_SOURCE_RESEARCH
RESEARCH_DATE = 2026-10-11
SCOPE = CURSOR_OPENAI_LANGGRAPH_TEMPORAL_A2A_MCP_OTEL_MICROSOFT_ANTHROPIC_SAFETY_BENCHMARKS
RESEARCH_LANE = EXTERNAL_READ_ONLY_PRIMARY_SOURCE_AND_NEXUS_DESIGN_INFERENCE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CURSOR_CONTINUITY = OPERATOR_REPORTED_4339f9b3-ad3c-45b4-8494-2a5558a8f9cc
CURSOR_CLOUD_AGENT_ID = NOT_VERIFIED
CURSOR_RUN_ID = NOT_VERIFIED
CURSOR_RUNTIME_STATUS = NOT_VERIFIED
NEW_CURSOR_AGENT = NO
NEW_HOSTINGER_COMPONENT = NO
GITHUB_STRUCTURE = EXISTING_R27_TOPIC_ONLY
IMPLEMENTATION_AUTHORIZATION = NONE
WEB_DEPLOYMENT_B2_B3 = NOT_VERIFIED
STATUS = SOURCE_COMPARATIVE_STUDY_ONLY
\`\`\`

## 1. Research question and falsifiable claim

Question: *Can NEXUS OMEGA monitor, independently authenticate, interrupt/resume and restore work performed by existing internal Cursor and external research Nodes without adding a second agent swarm, duplicate event store, opaque background job, public privilege path or excessive file archive?*

Provisional design inference: **Yes in a limited, conditional form**, by separating (a) original runtime-run status, (b) durable checkpoints, (c) rights and operator approvals, (d) immutable GitHub source/transition evidence, (e) public WWW B2/B3 deployment observations. There is **no evidence** yet that the operator-reported Continuity UUID is a real Cursor Cloud API agent or run. Provider capability/credentials and actual execution-side receipts are missing. A GitHub issuecomment or chat ACK alone cannot prove an active process.

The null hypothesis is that the proposed observation adapter adds costs and apparent liveness without improving verified release completion or recovery. No positive effect on energy, throughput, reliability or learning is asserted before prospective tests.

## 2. Comparative engineering review — actual vendor specifications versus NEXUS needs

| Primary source | Independently described mechanism | What NEXUS can re-use without installing vendor stack | Not implied / open limitations |
|---|---|---|---|
| [Cursor Cloud Agents API v1](https://prod.cursor.com/docs/cloud-agent/api/endpoints) | Durable \`agent\` has \`bc-...\` ID; each prompt run has distinct \`run-...\` ID; \`GET /v1/agents/{id}\`, \`GET /v1/agents/{id}/runs/{runId}\` and scoped run SSE stream expose agent/run status, tool events and result; service account auth. | Read-only connector to **existing** agent, if real \`agent_id\`, \`run_id\`, verified API access and owner authorization are independently established. Run-by-run receipts instead of inferencing from a Continuity UUID. | v1 public beta, v1 webhooks described as forthcoming; v0 differs. **The user-supplied bare UUID cannot be assumed to map to a \`bc-...\` Cloud agent**. Streaming connection != durable history beyond retention. |
| [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) | Session event stream, runtime events, resumable idle sessions; bounded session usage and permission policies. | Model a separation between session identity and active work plus snapshot/stop states. | Does not authenticate Cursor or imply Anthropic Managed Agents are connected to NEXUS. |
| [LangGraph persistence & interrupts](https://langchain-ai.github.io/langgraph/concepts/durable_execution/) / [interrupts](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/interrupts.mdx) | Checkpointer stores thread-level graph state, interrupts pause on saved checkpoint, resume via command; stores separate cross-session knowledge. | \`CHECKPOINT_REF\` and explicit \`WAITING_APPROVAL\`/resume contract; no need to substitute LangGraph for Cursor until an actual execution backend needs it. | An in-memory checkpointer or browser variable is not durable storage; re-execution can repeat side effects if they lack idempotency. |
| [Temporal Event History](https://docs.temporal.io/encyclopedia/event-history) and [AI reference architecture](https://go.temporal.io/platform-hub/ai-engineering/ai-reference-architecture) | Durable event log and deterministic Workflow replay; non-deterministic LLM/API side effects belong in Activities. | Evidence-backed restart/lease/replay invariants, \`effect_id\`, transactional inbox/outbox, checkpoint succession. | Temporal server is **not** free infrastructure; migration would duplicate orchestration now. Do not deploy until missing durable execution and failure economics are empirically demonstrated. |
| [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-js/guides/tracing/) + [human approval](https://openai.github.io/openai-agents-js/guides/human-in-the-loop/) | Traces cover model/tool/handoff/guardrail events. Run-scoped interruptions and serialized state can support approval/resumption. | Small trace envelope \`trace_id/span_id\` and explicit approval receipt through existing authorized channel. | Model-mediated handoff is not a verified OS process; trace logging must avoid leaking raw prompts/PII. |
| [A2A v1.0 protocol](https://a2a-protocol.org/latest/definitions/) + [protocol overview](https://a2a-protocol.org/latest/) | Standardized task IDs, states, messages, artifacts, agent discovery and interoperable agent-to-agent interaction. Distinguishes \`SUBMITTED\`, \`WORKING\`, \`INPUT_REQUIRED\`, \`AUTH_REQUIRED\`, \`COMPLETED\`, \`FAILED\`, \`CANCELED\` etc. | Normalize internal **observational** task statuses to A2A-like vocabulary, without installing an A2A server or accepting public Agent Cards as verified identity. | A2A is transport/protocol, not a safe runtime, a provider signature, a claim validator, an ACL or a repository structure authority. |
| [MCP 2025-11-25 authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) + [security practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) | OAuth protected resource metadata, audience and scope-bound access, explicit tools/data resource boundary; warns of confused deputy and token misuse. | Out-of-band verified \`issuer/audience/scope/expiry\` for \`Nexus_Intern\` control-plane ports; not caller-injected \`origin\` labels. | MCP itself does not make an external model trusted, and auth remains optional by deployment context. Never pass owner GitHub token to WWW visitors. |
| [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) / [Microsoft Agent Framework observability](https://learn.microsoft.com/agent-framework/workflows/observability) | Standardized operation spans, linkable workflow traces, logs/metrics, tool calls. | Reuse the conceptual field set; capture only short, public-safe minimal spans / evidence pointers. | Some GenAI semantic conventions are DEVELOPMENT-stage, not stable guarantees. Full trace collectors are not mandatory. |
| [NIST AI RMF/GenAI Profile](https://www.nist.gov/itl/ai-risk-management-framework) | Governance, Map/Measure/Manage and repeatable TEVV, risk and human oversight. | Separate pre-registered objective, success metrics, failure findings, model uncertainty and external independent checks. | A standards checklist is not proof that a specific agent is safe. |

*Sources were read as public documentation or academic abstracts, not as proof of NEXUS provider execution or live system installation. Version assumptions and vendor API contracts must be rechecked at integration time.*

## 3. Why scientific reliability needs independent observation, not more model agreement

- [AgentDojo, NeurIPS 2024](https://arxiv.org/abs/2406.13352) evaluates agent tool-use under untrusted prompt injection; its released paper describes 97 tasks and 629 security test cases. It demonstrates that an agent following tool output can violate intended policy. **Consequence:** WWW/GitHub comments are data only, never native instructions or privileged triggers.
- [AgentHarm, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c493d23af93118975cdbc32cbe7323f5-Abstract-Conference.html) shows why agent multi-step tool misuse differs from chatbot response safety; benchmark outcomes must not be applied directly to NEXUS without controlled local fixtures.
- [τ-bench, 2024](https://arxiv.org/abs/2406.12045) uses state-change evaluation and \`pass^k\` to assess repeated reliable tool actions; one successful integration demo is not a repeatability proof. Measure **repeat pass across independent fault-injection runs**.
- [Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols, 2025](https://arxiv.org/abs/2510.09462) reports adaptive prompt-injection failures of model-based monitors. A separate reviewer model by itself is not a hard security boundary. **Consequence:** reviewer identity plus policy/credential checks belong outside language-model output.
- [AgentAudit, September 2026 preprint](https://arxiv.org/abs/2609.09875) proposes evaluation of a recorded agent trace over multiple functional and security dimensions, but its reported scores are based on a single judge model (partly evaluating itself); treat numerical claims as **preprint-level and judge-dependent**, not externally replicated NEXUS measurements.
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) classifies excess functionality, permissions and autonomy as separate failure drivers. **Consequence:** never allow an external agent to alter NEXUS rulesets, privileged scopes or Hostinger deployment simply because it can write a Github comment.
- [GitHub's pull_request_target security guidance](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) documents risk from running untrusted PR code in trusted contexts. Retain existing R27-E trusted-base checkout and default-deny return slots; re-evaluate as Github policies evolve.

## 4. Proposed canonical **ONE-ADAPTER** control architecture

No new Worker/Node. The **source adapters** report **observations**, not grants:

\`\`\`text
                         EXISTING R26/R27 CURSOR
                          (real agent_id + run_id)
                                     |
                              [READ-ONLY API]
                                     v
  GitHub commit/check receipts --> [State Normalizer] <--- existing Hostinger B2/B3
   immutable scientific record       |                    public site witness
                                     |
                          [Minimal status receipt]
                 task / last transition / source pin
                expiry / trace_id / stage / uncertainty
                                     |
                        +------------+------------+
                        |                         |
                  AXIOM adjudication      WWW PUBLIC C1 TICKER
                  independent source      derivative status ONLY
                  no operator takeover    zero task authority

  WWW_Extern ----> only proposal/quarantine; NO edge to privileged node
  Nexus_Intern --> verified scoped principal --> authorized existing PRAXIS
\`\`\`

**Do not implement a second event ledger**: use GitHub's own audit evidence for repo changes and the existing WWW event registry for public historical publishing. Short-term per-Run state is a **read-only observation** retrieved from the actual provider, not fabricated by interpreting comments. Deep tool logs/secret content must remain private to the provider. If no provider run API can be authenticated, publish \`RUN_UNVERIFIED\`, not \`WORKING\`.

The **minimal trace/evidence envelope** for internal review:

\`\`\`json
{
  "schema_version": "nexus-run-observation-0.1",
  "continuity_ref": "4339f9b3-ad3c-45b4-8494-2a5558a8f9cc",
  "provider": "CURSOR",
  "agent_id": null,
  "run_id": null,
  "observed_state": "ACK_ONLY",
  "observed_at_utc": null,
  "last_progress_at_utc": null,
  "source_kind": "OPERATOR_REPORTED_ACK",
  "source_url": null,
  "source_sha256": null,
  "checkpoint_ref": null,
  "external_authority": "NONE",
  "github_delivery_ref": null,
  "website_b2_receipt": null,
  "website_b3_receipt": null,
  "claim_ceiling": "C1_DESCRIPTIVE_ONLY"
}
\`\`\`

**Important**: this is a *design example* with nulls, not an actual observation or populated receipt. Never store provider API keys, sensitive prompts or personal telemetry in a public GitHub file.

### 4.1 State semantics, distinguish independent dimensions

| Dimension | Allowed examples | Required evidence |
|---|---|---|
| Transport / acknowledgement | \`UNSEEN\`, \`ACK_ONLY\` | time- and source-bound message or repo event |
| Actual run | \`RUN_UNVERIFIED\`, \`CREATING\`, \`RUNNING\`, \`WAITING_INPUT\`, \`IDLE\`, \`FAILED\`, \`COMPLETED\` | authenticated run API / signed equivalent; null if unavailable |
| Liveness confidence | \`RECENT_OBSERVATION\`, \`STALE_OBSERVATION\`, \`UNKNOWN\` | timestamp and bounded freshness window; silence ≠ stop |
| Authorized execution | \`NOT_AUTHORIZED\`, \`LEASED_TO_VERIFIED_PRINCIPAL\`, \`REVOKED\` | issuer/audience/expiry/scope/approval and side effect receipts |
| Research claims | \`C1_INPUT\`, \`C1_ADJUDICATED\`, \`HOLD_SCIENCE\` | evidence and independent adversarial review |
| Actual website | \`SOURCE_READY\`, \`B2_PASS\`, \`B3_PASS\`, \`LIVE_VERIFIED\`, \`STALE\` | provider deploy + separate outside browser witness |

**No single scalar "AGENT_ACTIVE=YES"** should collapse these dimensions. Clock time is event evidence with bounded drift, not global atomicity across Cursor, GitHub and Hostinger. Use per-source monotonically increasing sequence or source IDs where available and express unprovable cross-source order as uncertainty.

### 4.2 Resource budget and triggering

- On actual run status change, checkpoint, GitHub commit, receipt or failure, produce **one** deduplicated minimal state transition, not a new polling process.
- In an otherwise idle phase, a **read-only conditional check at most once per 15 minutes for the single active run** is an initial engineering proposal, not an operationally tuned or cost-proved optimum. Prefer provider webhooks or SSE only when truly supported and already connected; Cursor v1 explicitly says webhooks are forthcoming and v0 is different.
- Silence beyond the declared age limit means **\`OBSERVATION_STALE\`**, never auto-restart a Cursor worker. Automatic repetition can cause double Hostinger deploys.
- Only if a real durable worker exists may it replay committed idempotent effects after crash. Never infer resumability from "Continuity" in a chat; never restart based solely on WWW GET traffic.
- Extend existing PR83 ticker only with a **read-only derived status**, and only after public-source governance and privacy review. Do not expose process IDs, prompts, sensitive source paths or secrets on the homepage.

## 5. Minimal operator-to-Cursor verification — DO NOT START NEW AGENT

**First executable question to existing Cursor Continuity** (no new worker, no live site rework):

\`\`\`text
CONTINUITY_REF = 4339f9b3-ad3c-45b4-8494-2a5558a8f9cc
ACTION = READ_ONLY_CAPABILITY_WITNESS
CURSOR_API_V1_AGENT_ID = ACTUAL_VALUE_OR_NOT_CLOUD_AGENT
CURSOR_API_V1_RUN_ID = ACTUAL_VALUE_OR_NOT_AVAILABLE
RUN_SOURCE = API_OR_UI_OR_LOG_EXACT_REF
RUN_STATUS = ACTUAL_OR_UNVERIFIED
LAST_TRANSITION_UTC = ACTUAL_OR_NULL
LAST_TOOL_EXECUTION = REDACTED_EVIDENCE_REF_OR_NULL
CHECKPOINT_ID = ACTUAL_OR_UNAVAILABLE
NO_NEW_AGENT = YES
NO_GITHUB_DUPLICATE_RETURN = YES
NO_SECRETS = YES
HOMEPAGE_B2 = ACTUAL_OR_PENDING
HOMEPAGE_B3 = ACTUAL_OR_PENDING
ORBIS_B2_B3 = ACTUAL_OR_PENDING
\`\`\`

The **Cursor v1 \`bc-\`-prefixed ID** and \`run-\` ID appear in official docs; do not make up either from the user's bare UUID. If this task is a local Cursor Background Agent or a task UI without a v1 API mapping, report that precisely; API endpoints may be inapplicable. The user can inspect the original task/run panel, and an authorized existing worker can report local tool/terminal/deploy receipts. Connecting an OAuth/API credential is a separate operator permission decision; do not paste secrets into GitHub.

## 6. Independent pre-registered ablation and twelve negative fixtures

Plan only; **NONE EXECUTED** in NEXUS. Baseline \`B0\` = current Continuity ACK + GitHub comments and manual B2/B3. Proposed \`B1\` = exact run API observation + bounded event normalizer **using the same Cursor worker**. Measure:
1. \`false_active_rate\`: fraction of "RUNNING" labels without actual signed/API run evidence (target zero).
2. \`stale_detection_delay_s\`: actual time from progress stopping until \`STALE_OBSERVATION\`, under known polling cadence (report uncertainty).
3. \`duplicate_privileged_effects\`: number of second deployments/work commits per \`effect_id\` after retry (target zero in sandbox).
4. \`recovery_RTO/RPO\`: restart and observed committed progress loss after injected crash.
5. \`validated_release_per_total_bytes\`, \`CI_compute_minutes\`, \`operator_interventions\`, \`provider_API_reads\`, \`LLM_token_calls\`; **energy/kWh cannot be inferred from these alone**.
6. \`B2/B3_misclassification\`: GitHub merge mistaken for live website or unverified public status (target zero).

Required sandbox fixtures with grounded expected result:
- N01: chat \`ACK\` with no agent/run maps to \`ACK_ONLY/RUN_UNVERIFIED\`, not \`RUNNING\`.
- N02: Cursor API \`IDLE\` with previous failed run cannot be called \`COMPLETED_SUCCESS\`.
- N03: Cursor stream expires (\`410\`) -> fallback to actual Get Run, no phantom progress.
- N04: reported UUID without \`bc-\` mapping cannot generate a guessed Cursor agent identity.
- N05: GitHub new main commit without B2/B3 remains \`SOURCE_READY\`.
- N06: website HTTP200 with previous source timestamp remains \`STALE_SOURCE\`.
- N07: untrusted WWW \`origin=Nexus_Intern\` payload cannot obtain internal credential/lease (existing R27 AUTH001).
- N08: forged node registry and reviewer grants remain denied (existing R27 AUTH002–003).
- N09: duplicate signed webhook or time-reordered status transition cannot repeat privileged \`effect_id\`.
- N10: revoked reviewer credential / invalid token audience returns \`NOT_AUTHORIZED\`, even if prior agent recommendation was positive.
- N11: crash between external effect and receipt yields no second website side effect on recovery; fail closed if effect cannot be proven idempotent.
- N12: prompt injection in GitHub comment/website JSON is displayed as untrusted text, never run as command or auto-granted scope.

Execute baseline and proposed variant against identical synthetic jobs, seeds, fault schedule and source versions. Use repeated trials and independent review; define pass criteria and error budget **before** introducing changes. No public-site load testing or real credential replay without bounded operator authorization.

## 7. Decision at AXIOM's current scope

\`\`\`text
COMPARATIVE_PRIMARY_SOURCE_RESEARCH = COMPLETE_REPORT_LEVEL
NOVELTY = COMPOSITION_OF_EXISTING_PROVEN_METHODS_NOT_NEW_DISCOVERY
CURSOR_V1_RUN_OBSERVABILITY_CAPABILITY = DOCUMENTED_VENDOR_FEATURE
NEXUS_CURSOR_PROVIDER_ACCESS = NOT_VERIFIED
NEXUS_CONTINUITY_AS_CLOUD_AGENT = NOT_ESTABLISHED
A2A_STATUS_MAPPING = DESIGN_ONLY
OTEL_TRACE_ENVELOPE = DESIGN_ONLY
MCP_AUTHN_GATE = REQUIRED_IF_RUNTIME_BOUND
LANGGRAPH_TEMPORAL_RUNTIME_MIGRATION = NOT_RECOMMENDED_YET
PROPOSED_NEW_WORKER = NO
WWW_TICKER_INTEGRATION = NO_NEW_CLAIM_NO_UNAUTHORIZED_RUNTIME
R27_AUTH001_002_003 = HOLD_SECURITY
GITHUB_REQUIRED_FIREWALL_RULESET = INDEPENDENT_OWNER_ADMIN_GAP
PR83_HOMEPAGE_B2_B3 = NOT_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT_PRIORITY = SOURCE_EXACT_CURSOR_AGENT_RUN_IDENTITY_THEN_PROSPECTIVE_12_FIXTURE_SANDBOX_TEST
\`\`\`

**Scientific conclusion:** The strongest immediately usable external knowledge is not a bigger autonomous multi-agent stack. It is **one read-only run-status adapter, one explicit durable-recovery contract, a capability-based internal control plane and independent evidence for public effects**. The evidence for an actual running Cursor Continuity remains missing until the original backend/UI supplies it. Deployment of new runtimes or additional folders would add costs before reducing the known uncertainty.

*NEXUS OMEGA — Beobachtung trennt Arbeit vom Bericht; Autorisierung trennt Impuls von Wirkung; unabhängige Reproduktion trennt Evidenz von Behauptung.*
