# NEXUS OMEGA · AXIOM R27 — WWW_Extern Wake / Nexus_Intern Isolation / Immediate C1 Push

\`\`\`text
OBJECT = NEXUS_OMEGA_AXIOM_R27_WWW_EXTERN_FREE_WAKE_STRICT_INTERNAL_ISOLATION_AND_IMMEDIATE_C1_ROLLOUT_20261011_R0
DATE = 2026-10-11
PREDECESSOR = NEXUS_OMEGA_AXIOM_GITHUB_WWW_LIVING_NODE_TRIGGER_FABRIC_BLUEPRINT_20261011_R0
PREDECESSOR_GIT_MAIN = d49f8e959b3aac61f9b7ef0621d7293908b2791e
CHANGE_TYPE = NEW_OPERATOR_DIRECTIVE_AND_ADVERSARIAL_SOURCE_VALIDATION
PRIMARY_DOMAIN = nexus-mobile.de
SECONDARY_DOMAIN = nexus-online.de_COORDINATION_ONLY
WWW_EXTERN = OBSERVATION_TRIGGER_ONLY_NOT_AUTHORITY
NEXUS_INTERN = INDEPENDENT_AUTHENTICATED_CONTROL_PLANE
FREE_WAKE = ZERO_LLM_TOKEN_AND_ZERO_PAID_EXTERNAL_AGENT_CALL_PER_PUBLIC_HIT_BY_DEFAULT
ZERO_TOTAL_INFRASTRUCTURE_COST = NOT_ESTABLISHED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
LOCAL_BASELINE_TESTS = PASS_13_OF_13
LOCAL_SECURITY_ADVERSARIAL_CASES = FAIL_3_OF_3_ACCEPT_UNAUTHENTICATED_INTERNAL_CLAIMS
G2_RUNTIME_AUTHORIZATION = HOLD_SECURITY
G3_DURABLE_BROKER = NOT_IMPLEMENTED
G4_WWW_BRIDGE = NOT_DEPLOYED
G5_FAILOVER = NOT_EXECUTED
NEW_CURSOR_WORKER = NO
CURSOR_R27_CONTINUITY = OPERATOR_REPORTED_4339f9b3-ad3c-45b4-8494-2a5558a8f9cc
CURSOR_FOLDER_X = READ_ONLY
CURSOR_AX_BODY_DELIVERY_DEFECT = OPERATOR_REPORTED_AFTER_COLON
IMMEDIATE_PUBLIC_SAFE_GITHUB_PUSH = REQUIRED_AFTER_SOURCE_AND_CI_VALIDATION
LIVE_WEBSITE_RUNTIME_PUSH = ONLY_AFTER_SECURITY_RUNTIME_PROVIDER_B2_B3_EVIDENCE
\`\`\`

## 1. Normative R27 operator decision

**Jede von außen sichtbare Interaktion** mit der WWW-Forschungsoberfläche soll, sofern ein Gateway erreichbar ist, **als äußerer Wake-Reiz interpretierbar** sein — nicht bloß ein absichtlich ausgefülltes Formular. Das gilt insbesondere Navigation/Seitenaufrufe, Link-/Quellenöffnungen, Suche, ausdrückliche Forschungseingaben, Korrekturmeldungen und signierte Integrationsereignisse. Eine interaktionsfreie Offline-Sitzung kann keinen Online-Trigger erzeugen. Technisch "kostenlos" bedeutet: kein LLM-/Agent-Call und kein kostenpflichtiger externen Workflow pro ungeprüfter Rohinteraktion; Server-, Netzwerk-, Speicher- und Hostingkosten bleiben real und müssen budgetiert werden.

Ein roh beobachteter Hit ist **nur ein schwaches Signal, nicht valide Identität, menschlicher Wille, Trainingsdatensatz, Zustimmungsnachweis oder Beschäftigungsauftrag**. Wenn ein Bot 1000 Requests erzeugt, zählen sie höchstens als aggregierte Eingangslast, nicht als 1000 Lernbeweise oder 1000 Node-Aufträge. Ein expliziter signierter/consented Forschungs-Return bleibt von passivem Traffic getrennt.

\`\`\`text
WWW_RAW_OBSERVATION
 -> BOUNDED_FREE_WAKE_COUNTER_OR_BUCKET (NO_MODEL_RUN)
 -> OPTIONAL_DEDUPED_PUBLIC_RESEARCH_SIGNAL
 -> SOURCE_AND_POLICY_TRIAGE
 -> PROPOSED_RESEARCH_ITEM
 --- TRUST_BOUNDARY (NO DIRECT EDGE) ---
 -> AUTHENTICATED_INTERNAL_REVIEW
 -> AUTHORIZED_NODE_LEASE
 -> VERIFIED_RESULT_RECEIPT
 -> AXIOM_C1_ADJUDICATION
 -> GITHUB_C1_PUSH / WWW_B2_B3_IF_ACTUALLY_DEPLOYED
\`\`\`

**Asymmetrie:** Internes Lernen/Retrieval darf bekannte public-safe externe Impulse als Forschungsprioritäten auswerten, aber externe Texte können weder \`Nexus_Intern\` vortäuschen noch Credential/Node-Registry/GitHub-Writes/Runtime/DNS/WWW-Deploy triggern. Für kontinuierlichen Model-Weight-Trainingprozess fehlt sowohl Trainingsfreigabe als auch Datengrundlage: \`WAKE_SIGNAL != MODEL_TRAINING\`. Die "Lebendigkeit" ist zunächst kausal bestätigte adaptive Forschungspriorisierung, kein behauptetes Bewusstsein oder permanentes eigenständiges Denken.

## 2. Striktes Drei-Klassen-Ingress-Design

### E0: Passive WWW observation (jedes Außenereignis, ohne Consent-/Tracking-Bypass)

Gateway auf \`nexus-mobile.de\` kann Anfragen lokal als zeitgebundene minimalistische Buckets mitzählen: \`route_family\`, \`utc_window\`, \`event_kind\`, \`coarse_count\`, \`ingress_health\`. Für V1 **keine IP, keine Fingerprints, keine Nutzerprofile, keine Cookie-ID, keine User-Agent-Speicherung, keine Nachrichtentexte, keine externen Agent-Runs** in öffentlicher Evidenz. Exakte Datenschutzeinordnung und Hosting-Telemetrie sind vor Realbetrieb durch die verantwortliche Stelle zu prüfen. Rate limiting/cost caps gelten auch für E0; Bucket-Verdichtung schützt gegen Spam, unendliche Queue-/GitHub-Kosten und Missbrauch. **Jeder Hit kann das Aggregat beeinflussen, nicht jeder Hit produziert einen persistierten Job.**

\`E0 → WAKE_OBSERVED_UNTRUSTED\` — keine Signatur vom Browser verlangt; der vertrauenswürdige **serverseitige Gateway** signiert ggf. seinen eigenen aggregierten Beobachtungs-Receipt. Browser-JavaScript erhält **niemals** ein HMAC-Secret. Ein reiner Static-HTML-Host kann ohne Backend/Serverless-Eingang die behauptete serverseitige Beobachtungskette nicht liefern.

### E1: Explicit public research / corrections

Öffentliche Eingabe mit transparenter Interaktion, Datenschutz-Information, Rate Limit, Missbrauchsschutz und strukturiertem Submit-Receipt. Prüfung und Persistierung in **eigener externer Quarantäne**: \`PENDING_EXTERNAL_WAKE\`. Public payload ist *untrusted data*, nicht Werkzeugbefehl. Kontextsensitive Signaturen/CSRF/Auth, sofern sessions oder Benutzerkonten beteiligt sind. \`E1 → PROPOSED_EXTERNAL_RESEARCH\` nur nach sicheren Grenzen und Relevanzfilter. Ohne validierte externe Quelle \`NO_C1_CLAIM\`.

### E2: Authenticated GitHub / agent bridge

Github-App-signierter Webhook auf **unveränderte Request-Bytes** und korrekte \`X-Hub-Signature-256\`, zusätzlich \`X-GitHub-Delivery\`, Installation/Repo/branch/commit Allowlist; legitime Agenten über eigene signierte kurzlebige scoped credentials. Keine gemeinsame Browser-Signatur mit GitHub; bestehende "x-nexus-signature" ist **kein** vollwertiger Ersatz für GitHub App HMAC. Nach Verify: source exact \`repo+commit+path+SHA256\`, dedupe and policy → Proposal, nicht automatischer Produktionseffekt.

## 3. Nexus_Intern als getrennte Sicherheitszone

**Abgelehnt:** \`{origin:"Nexus_Intern", trust:"INTERNAL_AUTHENTICATED"}\` als Authentisierung. Ein Objekt kann diese Zeichenketten frei setzen. Auth muss über eine **vom Event nicht kontrollierte** Identität stammen (serverseitige verifizierte Session, mTLS, scoped tokens durch separaten trusted adapter, Workload Identity, oder eine nicht über öffentliches API erreichbare capability). Der Internal-Control-Plane-Adapter erzeugt die Claims erst **nach** erfolgreichem Auth-Nachweis; der Public-Port exponiert niemals \`ingestInternal\`, \`registerNode\`, \`approveProposal\` oder \`runTask\`. Ein privater Funktionsname oder eine Code-Property ist kein Security Boundary, wenn der Außenadapter dasselbe Objekt frei exportiert.

**Minimaler sicherer Vertrag:**
- Transport: two processes/isolated service principals preferred, separated databases/collections and network ACLs. Least-privilege per adapter.
- AuthN/AuthZ: \`verifiedPrincipal\`, \`issuer\`, \`aud\`, \`scope\`, \`expiry\`, \`jti\`; admin approval has action-specific nonce and explicit source, reviewer != proposer != producer.
- Work: durable inbox/outbox, idempotency \`effect_id\`, lease and fencing token, immutable source-pin, rights-bound target, result receipt.
- Public never can register internal node, select internal reviewer, change scopes, approve themselves, turn off kill switch, force GitHub merge, call the OS, or declare deployment.
- Legitimate internal decisions \`Nexus_Intern\` require an audited authenticated **control-plane** and are not created by mere replay/import of public data.

## 4. Baseline ZIP review and three new failures

Local Operator-delivered R11 ZIP: **64,055 bytes**; evaluated read-only in isolated local directory (ZIP itself deliberately **not** added to public GitHub: includes nested chats and additional source archives). \`node --test test/*.test.js\` on Node v22.16.0 returned \`13/13 PASS\` (8 original ingress + 5 coordinator). This establishes that the tests match the authors' declared intent in isolated circumstances, not a secure boundary.

Independent adversarial checks, using actual exported functions:
- \`R27-AUTH-001\`: \`broker.ingestInternal\` accepted a caller-created \`origin=Nexus_Intern\`, \`trust=INTERNAL_AUTHENTICATED\` object, without any real identity credential or capability check. Observed \`accepted=true\`. **FAIL_AUTHN**.
- \`R27-AUTH-002\`: \`coordinator.registerNode\` accepted an analogous forged \`INTERNAL_AUTHENTICATED\` node claim, and the external proposal router offered that node. Observed \`accepted=true\`. **FAIL_NODE_REGISTRY_AUTHZ**.
- \`R27-AUTH-003\`: \`coordinator.approveProposal\` accepted a forged \`reviewer_id\` + matching \`Nexus_Intern\` labels and recorded \`APPROVED_INTERNAL\`. Observed \`accepted=true\`. **FAIL_REVIEW_AUTHZ**.

These are **library API trust-boundary defects**, not verified internet exploits: no HTTP server or deployment exists in the provided ZIP. They are nevertheless production-blocking because any future public adapter that exposes one of these methods could escalate authority. Do not publish a vulnerable running facade or promote \`G2_SECURITY_PASS\` from \`13/13\` intent tests. Static inspection alone does not prove absence of further defects.

Additional scoped caveats: signed external ingestion currently expects an HMAC made with broker secret, which a public visitor cannot possess; it therefore needs a server-side E0/E1 ingress adaptor instead of distributing secrets. Queue/Dedupe/Rate-Limit are in memory, reset after restart, not durable or interprocess safe; no 24h proven operation/failover. \`drain\` removes event from queue before verified receipt; at-least-once delivery is not guaranteed across crash. There is no actual WWW endpoint, GitHub App signature verification, broker provider host, or real node runner.

## 5. Release / immediate push rule (risk-adaptive)

**Immediately push:** validated, privacy-safe, reversible source objects (this correction, event model, test-fixture spec, scoped remediation order) to GitHub once structure and Security/CI checks pass. Existing policy \`C1_VALIDATED_PUBLIC_SAFE -> ROLLOUT_REQUIRED\` applies to these C1 documents. Emit source-exact API receipt and immutable main-readback.

**Do NOT immediately expose:** executable Node API / public wake-up path that still accepts spoofed internal approval/registration. Until AuthN fix and adversarial regression tests demonstrably reject forged callers, classify \`EXECUTOR_RELEASE=HOLD_SPECIFIC_AUTHZ_FAILURE\`. This is a concrete integrity/security HOLD, not indiscriminate philosophical delay. Independent safe design/research remains unblocked.

**Website push distinction:** GitHub Main API push is not Hostinger B2 and Browser B3; no \`WWW_LIVE=PASS\` absent provider deployment and actual public readback. User's R27-Continuity statement reports intake to \`4339f9b3-ad3c-45b4-8494-2a5558a8f9cc\` but also \`Chat-AXIOM-Body fehlt nach dem Doppelpunkt\`. A GitHub file and PR comment remedies **artifact availability**, not verified Cursor tool-read/ACK.

## 6. Ordered remediation and test proof

**H0 SECURITY FIRST**: Source exact ZIP baseline + compile 13 baseline tests + add three adversarial tests to previously defined offline suite. Refactor ingress into **public ingress port, authenticated internal port, separate operator control port**. Verify scope against out-of-band credential context; reject all forged object labels, even when \`event.payload_sha256\` matches. Prove no public code path accesses internal factory/registrar/reviewer grant; run a black-box HTTP adapter test using only public endpoints.

**H1 PASSIVE WAKE**: implement E0 edge counter/buckets without per-view API cost, per-event content, fingerprint or persistent high-cardinality identifier. Every technically observed WWW request increments at most one bounded observation sample, preserving design semantics while preventing excessive paid work; bucket quota/expiry and anti-bot distinction documented. Test 10k synthetic mixed requests yields no external model calls and no \`Nexus_Intern\` event. Implement E1 explicit research submission as separate path.

**H2 REAL DURABILITY**: provider-neutral event-store interface + transactional inbox/outbox + unique dedupe and fencing locks. Retry/dlq/recovery after crash and split-brain race tests. In-process queues are insufficient. No new Node worker; inspect existing reported Cursor-Continuity control plane and reuse only if demonstrably authorized.

**H3 PROVIDER / WWW**: independently establish Hostinger write/deploy B2, server-side Gateway route on \`nexus-mobile.de\`, GitHub App webhook receipt and browser B3. No hidden DNS changes or customer data capture. \`nexus-online.de\` coordination only.

**H4 SELF-OPTIMIZATION**: transport retries/batching/polling/power budgets only within signed operator policy; simulator can compute recommendations without auto-grant. Internal knowledge modification only as versioned reviewed C1 evidence and source-specific learning proposals; model-weight training not authorized. Protected kill switch/role permissions immutable to optimizer.

**H5 NEGATIVE TESTS**: 28 previously designed Fabric V1 policy cases **plus** R27-AUTH-001..003 and public passive traffic, mixed bot/staleness, browser no-HMAC, secret exfiltration, cold start/retry, authorization token expiry, race and malicious payload fixtures. Distinguish \`TEST_DESIGNED\` from \`TEST_EXECUTED\`; gate flags require actual scripts and raw logs.

## 7. Causal status

\`\`\`text
R27_OPERATOR_DIRECTIVE = BOUND_C1
WWW_PASSIVE_OBSERVATION = POLICY_ACCEPTED_DESIGN
WWW_REQUEST_COST = ZERO_LLM_PAID_INFERENCE_PER_UNTRUSTED_HIT_DEFAULT
EXTERNAL_AUTHORITY = NONE
NEXUS_INTERNAL_AUTHN = REQUIRE_OUT_OF_BAND_VERIFICATION
ZIP_G2_ORIGINAL_FUNCTION_TESTS = PASS_13_OF_13
ZIP_G2_PRIVILEGE_BOUNDARY = FAIL_3_REPRODUCED
SOURCE_ZIP_RUNTIME = LOCAL_ONLY_NO_WWW_SERVER
R27_CODE_PRODUCTION_RELEASE = HOLD_SECURITY
R27_PUBLIC_SAFE_DOCS = PUSH_AFTER_VALIDATION_REQUIRED
CURSOR_WORKER_REFERENCE = OPERATOR_REPORTED_ONLY
CURSOR_CHAT_BODY_DELIVERY = GAP_CANONICAL_GITHUB_BODY_REQUIRED
FOLDER_X = READ_ONLY
WWW_B2_B3 = NOT_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
\`\`\`

*NEXUS OMEGA — Jeder äußere Kontakt darf Beobachtung auslösen. Nur intern authentifizierte Freigabe darf interne Wirkung auslösen. Quelle ist nicht Wahrheit; Prüfung bleibt das Fundament.*
