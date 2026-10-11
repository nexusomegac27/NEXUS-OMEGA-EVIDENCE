# NEXUS OMEGA · AXIOM — Living Node Trigger Fabric V1
## Providerneutrale GitHub ↔ WWW ↔ interne/externe Agenten-Ereignisarchitektur

\`\`\`text
OBJECT = NEXUS_OMEGA_AXIOM_GITHUB_WWW_LIVING_NODE_TRIGGER_FABRIC_BLUEPRINT_20261011_R0
DATE = 2026-10-11
PARENT_MAIN = R26_PR77_MERGED_8c37445c709986a39191fd46af8efe70d1150b9c
PARENT_PR74 = R26_BROAD_REVIEW_C1_MERGED
CURSOR = EXISTING_R24_R25_CONTINUITY_PR74_INTAKE_REPORTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
FABRIC_STATUS = BLUEPRINT_NOT_DEPLOYED
GITHUB_API = EVIDENCE_AND_TRANSPORT
WEB_WWW_PRIMARY = nexus-mobile.de
WEB_WWW_SECONDARY = nexus-online.de_COORDINATION_ONLY
GITHUB_MERGE != NODE_EXECUTION != HOSTINGER_B2 != BROWSER_B3
NEW_CURSOR_WORKER = NO
DNS_CHANGE = NO
EXTERNAL_AGENT_AUTHORITY = RESEARCH_ONLY_UNLESS_SEPARATELY_GRANTED
UNTRUSTED_PUBLIC_INPUT_AUTORUN = NO
SELF_PROMOTION = NO
\`\`\`

## 0. Architekturthese und Integritätsgrenze

GitHub ist **append-only Evidenz- und Koordinationsprotokoll**, kein hochverfügbarer Echtzeit-Executor. Die Website ist ein **Interaktions- und Beobachtungseingang**, nicht selbst die Autorität, Agenten zu starten. Ein **separat betriebener Event-Broker mit langlebigem Inbox/Outbox-Store, Policy Decision Point (PDP), Router, Queue und eingeschränkten Node-Adaptern** vermittelt zwischen beiden. Der interne Ausführungsadapter benötigt eine existierende autorisierte ausführbare Laufzeit (beispielsweise bestehender Cursor-Continuity-Worker). Keine Browser-JavaScript-Datei kann ohne erreichbaren Server oder Worker einen abgeschalteten Node wecken.

**Das Wort "lebendig" erhält eine falsifizierbare Definition:** Ein zugelassener externer Input erhält binnen definierter Frist ein signatur-/identitätsgeprüftes Eingangsevent, einen beständigen Identitätsschlüssel, eine Policy-Entscheidung, ggf. eine idempotente Ausführung, einen Rückbeleg und eine überprüfbare C1-Statusansicht. Wiederholungen, Fehler, Retraktionen und Ausfälle werden sichtbar, ohne Übernahme fremder Berechtigungen.

Referenz-Grundsatz:
\`UNTRUSTED_TRIGGER -> VALIDATE -> POLICY -> DURABLE_INBOX -> ROUTE -> LEASED_EXECUTION -> RECEIPT -> AXIOM_REVIEW -> C1_PUBLIC_WITNESS\`.
Niemals \`PUBLIC_CLICK -> PRIVILEGED_NODE_EXECUTE\`.

## 1. Bestehende Infrastruktur — tatsächlich beobachtete Grenzen

- GitHub-Repo \`nexusomegac27/NEXUS-OMEGA-EVIDENCE\` hat operative Lesen/Schreiben-Prüfungen, PRs, CI, \`AGENTS.md\`, \`GOVERNANCE.md\`, \`SECURITY.md\`, Handoff- und Repository-Order-Law. \`AGENTS.md\` verlangt **Append-only**, Hash != Truth, privacy-safe Source Intake, keine Rollenpromotion.
- \`https://www.nexus-mobile.de/research/\` bietet öffentlich C1-Forschung, Agent Intake und Statusrouten; ein ausgeführter WWW-zu-Node-Broker ist damit **nicht** bewiesen.
- Hostinger AI Builder Agentic-Connector sieht **0 verwaltbare Sites**; das sagt nichts über eine andere Hostinger-Manual-Site aus, verhindert aber hier den direkten C1-Live-Publish.
- Verbundenes Supabase-Projekt ist **INACTIVE**, Vercel-Projektliste **leer**, Remote-Desktop-Commander meldet **kein verbundenes Gerät**. Kein providerseitiger Queue- oder Broker-Deploy ausgeführt.
- Cursor meldet Intake auf **bestehender** R24/R25 Continuity; diese Meldung ist kein Nachweis, dass der Worker Webseitevents bereits ausführt. Ein neuer Worker wäre Duplikation und ist nicht autorisiert.

**Architekturstatus:** \`G0_DESIGN_ALLOWED\`; \`G1_RUNTIME_HOST=NOT_BOUND\`; \`G2_DOMAIN_BACKEND_ROUTE=NOT_BOUND\`; \`G3_NODE_ADAPTER_AUTH=NOT_BOUND\`; \`G4_INTEGRATION_PROOF=NOT_RUN\`; \`G5_HOSTINGER_B2_B3=NOT_VERIFIED\`. Diese Lücken rechtfertigen einen scoped Runtime-HOLD, nicht die Sperre dieses öffentlichen Designs.

## 2. Logische Module — jede Grenze mit einem einzigen Besitzer

| Modul | Aufgabe | Eingangsvertrauen | Ausführungsrechte |
|---|---|---|---|
| \`www-interaction-adapter\` | explizite Website-Aktion, Consent/CAPTCHA/Rate-limit, Public-Event | \`PUBLIC_UNTRUSTED\` | nur Event-Antrag |
| \`github-webhook-adapter\` | GitHub App \`X-Hub-Signature-256\` über **unveränderte Request-Bytes**, Delivery-ID, Repository Allowlist | \`SIGNED_TRANSPORT\` | nur Inbox-Write |
| \`external-agent-adapter\` | kurzlebige signierte Serviceidentität, separate Subscriptions | \`AUTHENTICATED_SCOPED\` | Return einreichen, kein Selbstmerge |
| \`event-envelope-validator\` | v1 JSON-Schema, Payload/URL/Size/Timestamp/TTL, immutable source pin | gemischt | reject/quarantine |
| \`identity-and-provenance\` | Subject, Providerinstallation, signierter Token, immutable Source-SHA; Inhalt != Identität | verified metadata | Audit |
| \`policy-decision-point\` | risk tier, capability map, approval receipts, fail-closed | all | nur Entscheidung |
| \`durable-inbox-outbox\` | Transaktion, Dedup-Key, Zustandsjournal, Replay, atomare Lease | verified | queue scheduling |
| \`queue-router\` | deterministische \`event_type -> node_capability\`, Priorität, Rate/Circuit | policy-approved | begrenzter Lease |
| \`node-adapter-*/runner\` | GitHub Research, AXIOM Review, Cursor existing continuity, public publishing, externes Review | \`CAPABILITY_LEASE\` | allowlist command API only |
| \`receipt-and-indexer\` | erfolgreiche/negative Belege, GitHub SHA/ref, C1-Readback, Dashboard | execution/observe | append-only |
| \`health-and-optimizer\` | Lag, delivery, errors, drift, tuning proposals, shadow/canary | telemetry | limitierte Konfigoptimierung |
| \`kill-switch-and-recovery\` | operator off, token revoke, circuit, DLQ quarantine, replay by approver | high trust | suspend/recover bounded |

**Aktivierungsgrenze:** \`NODE_REGISTERED != NODE_RUNNING\`. Ein Node benötigt installierte authentifizierte Adapter + erreichbaren Runner + berechtigte Capability + gültigen Event-Lease. Keine semantische „geistige Aktivierung“ aus reinen Webseitenhinweisen ableiten.

## 3. Ereignisvertrag und Zustandsautomat

Maschinelle Referenz: \`EVENT_ENVELOPE_V1.schema.json\` im Paket. Kernfelder: \`schema_version\`, \`event_id\`, \`event_type\`, \`occurred_at\`, \`expires_at\`, \`origin\`, \`subject\`, \`tenant_id\`, \`repo\`, \`source_commit\`, \`source_path\`, \`source_sha256\`, \`causation_id\`, \`correlation_id\`, \`trust_level\`, \`risk_tier\`, \`requested_capability\`, \`policy_version\`, \`idempotency_key\`, \`payload_ref\`. Authentifizierung ist **separat** und unverfälschbar an die ursprünglichen Request-Bytes gebunden; JSON-Werte allein sind keine Signatur.

Zulässige Beispiele:
- \`PUBLIC_RESEARCH_INTENT_SUBMITTED\` → nur consented Ticket/Queue, niemals automatische Ausführung auf Node mit schreibendem Recht.
- \`GITHUB_RETURN_SUBMITTED\` → GitHub-Source-Pin Fetch, Hashprüfung, Intake-Receipt, unabhängige Review-Kandidatur.
- \`REVIEW_ADJUDICATION_READY\` → Lesestatus; nur bei tatsächlich belegter Berechtigung dokumentierte Folgeaktion.
- \`SCIENTIFIC_CLAIM_RETRACTED\` → alte Claim-ID als \`SUPERSEDED\`, Gegenbeweis und Korrekturpfad publizierbar; **keine Löschung alter Git-Historie**, keine automatische Claim-Promotion.
- \`OPERATOR_APPROVAL_ISSUED\` → nur nach authentisierter Operator-Prozedur, Aktion/Scope/Expiry/Nonce gebunden.
- \`PUBLICATION_READY_C1\` → bei validiert/public-safe/reversibel via **bestehenden** Cursor-Publishing-Adapter; B2 Hostinger-Receipt und B3 independent Browser-Readback bleiben eigene Gates.
- \`NODE_HEALTH_CHANGED\` → Telemetrie, ohne selbständigen Privilegienwechsel.

Sicherer Ablauf:
\`RECEIVED -> AUTHENTICATED -> SCHEMA_VALID -> SOURCE_PIN_VERIFIED -> POLICY_EVALUATED -> DURABLY_QUEUED -> LEASED -> EXECUTED -> RECEIPTED -> AXIOM_REVIEWED -> (PUBLIC_C1_WITNESSED | HOLD_SCOPED)\`.
Seitenwege: \`REJECTED_AUTH\`, \`QUARANTINED\`, \`DUPLICATE_ACK\`, \`RETRY_SCHEDULED\`, \`DLQ\`, \`EXPIRED\`, \`KILL_SWITCH_ACTIVE\`. Status ist append-only; Reparaturen neues versioniertes Receipt mit \`supersedes\`.

**Idempotenz:** Unique \`(origin, delivery_id)\` plus normalisierter \`event_id\`/pro Aktion \`action_id\`. Durable Inbox write + Outbox task in *einer* Transaktion; Executor setzt terminale Effect-Receipt oder idempotente neue Lease. Replay mit exakt demselben Ziel darf den privilegierten Seiteneffekt **nicht wiederholen**. \`AT_LEAST_ONCE_DELIVERY + IDEMPOTENT_EFFECT\`, keine unbelegte end-to-end exactly-once-Garantie.

**GitHub-ACK vs Node-ACK:** \`GITHUB_COMMIT\` beweist nur Transport. \`NODE_ACCEPTED\` belegt Leaseannahme; \`NODE_EXECUTED\` braucht eigene überprüfbare Run-/Artefakt-Receipt; \`WWW_LIVE\` braucht tatsächlichen B2 + B3.

## 4. Sicherheitsarchitektur und Angriffsgrenzen

- **Ingress Auth:** GitHub App Webhook secret HMAC-SHA256 constant-time, \`X-GitHub-Delivery\` UUID; Subscriber-/Runner-Autorisierung via signiertem kurzlebigem JWT oder mTLS mit \`aud\`, \`iss\`, \`exp\`, \`jti\`, Fähigkeit/Node-ID. CORS ist **kein** Auth. Externe agentische Texte bleiben untrusted, auch wenn aus GitHub geladen.
- **Github App vor PAT:** minimale Repo-Berechtigungen, Installations-Allowlist, Private-Key außerhalb GitHub/Frontend; Rotation, revoke, audit, scope pin; \`repository_dispatch\`/Actions nur als zugelassener Adapter, keine allgemeine Befehlsausführung über PR-Text.
- **Input Safety:** keine freien Web-URLs vom Browser/Agenten durch Broker fetchbar (SSRF), nur eindeutige GitHub \`repo+commit+path\` aus Allowlist, Content-Type/Größe, canonical JSON, Schutz vor duplicate keys, Prompt-Injection-Quarantäne, PII/Sekret-Scanner. Nie GitHub-Kommentar als Shell-Skript interpretieren.
- **Authorization:** \`L0\` öffentlich anschauen/lesen; \`L1\` public request/submit; \`L2\` scoped Research dispatch; \`L3\` reversible public-safe C1 publish nach festen Gates; \`L4\` Repo-/Provider-/Runtime-Write mit Operator-Bind; \`L5\` irreversible/Privacy/DNS/Secrets/Promotion gesperrt ohne explizite gesonderte Freigabe. \`REVIEW_PASS != EXECUTION_AUTHORIZATION\`.
- **Website:** Besucherinteraktion nur nach ausdrücklicher Aktion/Transparenz, keine stille Nutzung von Klicktracking als Agentenbefehl, DSGVO-konforme Datensparsamkeit/Löschung. Client kennt **keine** geheimen Tokens. Origin/CSRF-Schutz zusätzlich zur authentifizierten Server-Session; Rate Limit pro Session/IP datensparsam.
- **Outbound:** Node-adapter allowlist, Argumentvalidierung, no arbitrary host, no \`eval\`, kein beliebiger Git-Checkout fremder Commits, keine Netz-Penetration oder privaten Chat-Historien. Repository-PR #67 privacy-history HOLD unberührt.
- **Kill switch:** globaler \`FABRIC_EXECUTION_ENABLED=OFF\` und node-spezifische \`DENY\`; Operator kann jede Queue deaktivieren und in-flight-Leases invalidieren. Kein stiller Re-Enable durch Optimizer.
- **Audit:** Korrelation/Git SHA/Hash und Session-gebundene Pseudonyme; keine Secrets/raw messages/Medizin oder persönliche Chatlogs in public evidence repo; separate privat geschützte Auditdaten mit Löschkonzept.

## 5. Selbstoptimierung = kontrollierte messbare Verbesserung, niemals Selbstermächtigung

Self-adaptive **Transportparameter** dürfen innerhalb vorab fixierter Ober- und Untergrenzen nach SLO gesteuert werden: Backoff mit Jitter 2–120 s, maximal 5 Wiederholungen, Queue-Batchgröße 1–25, gleichzeitig höchstens 4 low-risk Worker-Leases je Phase; bei Fehlerquote >2% oder P95-Lag >60 s Vorschlag/automatische **risikoreduzierende** Drosselung, Circuit Breaker und Alarm. Werte sind **Entwurfsdefaults**, vor Produktion anhand Provider-Quotas, Lasttest und Operator freizugeben, keine gemessenen NEXUS-SLOs.

Nicht selbstoptimierbar: Claim-Deckel C1, Operator-Identität, Rollen, Capability-Scopes, Privacy/Retentionspolitik, DNS, Repo-Allowlist, Secret-Zugriff, GitHub-Merge/Force-Push, Webseiten-Deployrechte, Kill-Switch, Review-Unabhängigkeit. Für jede Änderung \`TUNING_PROPOSAL -> SHADOW_TEST -> NEGATIVE_FIXTURES -> CANARY -> OPERATOR_RULED_APPROVAL_WHERE_NEEDED -> PROMOTE_CONFIG -> ROLLBACK_RECEIPT\`. Ein Agent erhält kein Recht, seinen eigenen Reviewer auszuwählen oder eigene wissenschaftliche Behauptungen zu validieren.

Ein Optimizer, der nur **günstiger und zuverlässiger zustellt**, aber weder Payload auswertet noch neue Privilegien vergibt, hat einen prüfbaren Autonomiegrad. \`ADAPTIVE_POLICY_WIDENING=NO\`.

## 6. Architekturpfade und echte Ausweichschnittstellen

### Lane A · Push (Primärpfad, erst nach Providerbereitstellung)
GitHub App \`pull_request/review/push/check_run\` Webhook → serverseitiger HMAC validator → durable Queue und Outbox → Router → zugelassener Node-Adapter → zurück über GitHub API und private telemetry → C1-only public status. Website POST/GET über dasselbe Gateway (nur wenn gewollt und freigegeben). **GitHub braucht dafür eine echte erreichbare HTTPS-Broker-URL**. Aktuell NICHT_DEPLOYED.

### Lane B · Pull aus GitHub (Ausweichpfad)
Wenn Webhook-Runtime oder Eingang down, prüft ein **bereits laufender, autorisierter** interner Adapter periodisch GitHub \`ETag/If-None-Match\`, \`updated_at\`, Head-SHAs und Handoff-Objekte; nur immutable SHA und manifestgebundene Objekte als Dispatch-Kandidaten. Jitter und API Rate Limit, 5–15 min als **Designparameter**. Unique Delivery/Action schützt gegen Doppeleffekte beim Wechsel A↔B. \`NO_EXISTING_RUNNER -> FALLBACK_NOT_ACTIVE\`.

### Lane C · zweiter Provider (warm standby / manuell)
Providerneuer Reverse Proxy und dauerhafter Store auf separatem Dienst (z.B. Supabase Edge Function + Postgres nur nach Wiederaktivierung, Cloudflare Worker/Queue/D1 oder Vercel Function + externe persistente Queue). Betrieb braucht eigene Credentials, Domainroute und Governance. **Heute nicht aktiviert:** verbundenes Supabase-Projekt INACTIVE; Vercel keine Projekte. Gespeicherte Infrastrukturvorlage allein ist kein Failover.

### Lane D · Notfall-/Airgap
Expliziter manueller, signierter GitHub-Issue/PR oder lokal importierbares, sanitisiertes C1 JSON-Paket als \`REPLAY_REQUEST\`, durch existierende Cursor-Continuity einzeln übernommen. Kein E-Mail-Text/Notion-Spiegel als vollgültiger API- oder Run-Receipt. Bei Totalausfall \`QUEUED_OFFLINE\`, keine Phantom-Ausführung.

Failover wird nur zwischen **vollständig autorisierten und vorgetesteten** Transporten geschaltet; Wechsel ist protokolliert \`ROUTE_SELECTED\`, \`CAUSAL_HEAD\`, \`AT_LEAST_ONCE\`, \`LEADER_LEASE\`, \`RECOVERY_ACK\`. Split-brain: nur ein gültiger Lease pro \`action_id\`, Fencing-Token monoton, Advisory lease expiration, one writer per authoritative queue. Ein Recovery ohne persistierenden Store ist **nicht** selbstheilend.

## 7. WWW-Interaktion und beobachtbarer User Flow

**Public interaction**: Auf \`https://www.nexus-mobile.de/\` optional ein kleiner, unaufdringlicher „Agenten-Kommunikation“/„Quelle prüfen“/„Korrektur melden“-Link in bestehender Agent-/Forschungsspur, **nicht** neues Homepage-Dashboard. UI bestätigt explizite Privacy und zeigt \`event_id\`, \`QUEUED/REVIEW/HOLD\`, keine unmittelbare Node-Aktivierungsbehauptung. Backend-Route vorschlagsweise \`/api/nexus-events/v1\` ist **DESIGN_NOT_DEPLOYED**, nicht als existent veröffentlichen. Redaktionelle C1-Forschungsupdates nur nach B2 und B3; getrennte Statusoberfläche \`/research/agents/\` ist ebenfalls **PROPOSED**, nicht beansprucht.

**Internal action:** GitHub-C1-Forschungshandoff → Signaturprüfung/Source-Fetch → \`SOURCE_RECEIVED\` → AXIOM source audit candidate → bei berechtigter Freigabe externer Research-Auftrag oder Cursor-Continuity-Dispatch → eigene \`NODE_RECEIPT\`. Die vorhandene Cursor-R24/R25-Continuity-ID ist kein Webhook-Provider-ID; sie darf nicht aus einem reinen GitHub-PR-Kommentar als gestartete Ausführung ausgegeben werden.

**Scientific retraction fixture:** Zwei aktuelle Betreiber-Dateien vom 11.10.2026 enthalten einen MISTRAL/VIBE-R26-Zwei-Peak-Widerruf: früherer \`PERSISTENT_MULTI\`-Claim wird nach Peak-Metrikfehler (Ringumbruch-Schulter i=31 statt separatem Antipodenmaximum i=16) als \`WTA_ONE_BUMP\` bewertet. Sie sind **Operator-Upload, noch kein neuer GitHub-Retraction-Merge oder AXIOM-Rehash dieser Forschung**. Ereigniskette im Simulator:
\`RETRACTION_SUBMITTED -> SOURCE_NOT_CANONICAL_YET -> INTAKE_REHASH -> INDEPENDENT_REPLAY_PENDING -> CLAIM_SUPERSEDED_C1 -> REVIEW -> PUBLIC_CORRECTION_IF_VALIDATED\`. Alter Claim bleibt historisch erreichbar und wird **nicht** still entfernt. Das ist der Goldstandard für lebendige epistemische Selbstkorrektur, nicht „immer PASS“.

## 8. Testmatrix, Falsifikation, SLO-Belege

Mindestens 24 **distinkte** negative Fixtures: bad-HMAC, Missing-HMAC, stale signed request, duplicate delivery, duplicate action, diverging hash, incorrect repo, untrusted HTML/script, malicious callback URL (SSRF), cyclic causation, expired lease, two workers racing, split-brain failover, reordered webhook arrival, artifact deleted, auth revoked, privilege escalation, replayed operator approval, self-approval attempt, privacy-bearing payload, CI false-green, wrong data source/commit, forced latency spike, DLQ exhaustion, invalid capability, bad clock, robot spam, self-tuning outside bounds, offline webpage/UI reported as online, GitHub MERGED but no B2/B3.

Teststufen:
1. T0 \`CONTRACT_SCHEMA\` und HMAC-Fixtures offline; Killswitch und false-PASS negative first.
2. T1 reine lokale Simulation von Inbox/Outbox, leases, idempotency, chaos injection 10k synthetic events; keine externen API-Seiteneffekte.
3. T2 Sandbox mit **echter** GitHub App auf separat autorisiertem Testrepository und **echtem** Broker, mit Run-Receipts, p95 latency, dedupe, chaos und failover.
4. T3 WWW-Consent- und Auth-Test auf gesondertem Staging, keine Produktion und keine stillen Cookies.
5. T4 **public-safe/reversible** C1 live pilot nach dokumentierter Runtimefreigabe: 24h oder benannter Rahmen, Anbieter B2, unabhängiger Browser B3, negative fixture proof, rollback und Operator/AXIOM-Gates.
6. T5 nur nach echter Ausführungsautorisierung: node-to-node Scoped-Tasks; kein Node-Selbststart aus Chat oder GitHub.

**Geplante, noch nicht gemessene** Mindestziele als Testhypothesen: duplicate_side_effects=0/10000; invalid_signature_accept=0/1000; privilege_bypass=0/1000; unapproved_production_write=0; 100% journalisierte \`NO_EXEC\`-Entscheidungen; RTO <15 min nach vorgetestetem Fallback, RPO ≈0 bei persistierendem Store; queue latency p95 <10 s bei 10 events/s in Sandbox. Kein PASS ohne reale Logs und unabhängiges Witnessing.

## 9. C1-Publikations- und Adjudikationsgrenzen

\`C1_VALIDATED_PUBLIC_SAFE -> ROLLOUT_REQUIRED\` gilt für **öffentliche, reversible Quellen/Ansichten**, nicht für unautorisierte Runtime-Eskalation. GitHub-Dokument darf nach bestandenen Struktur-/Security-Gates publiziert werden. **Broker-Deployment ist eine gesonderte neue ausführende Infrastruktur**; dafür fehlt heute Host/Domain/Agent-Authorization. **Release erst nach G1–G4 tatsächlichen Receipts**, nicht per Plantext. \`R26_SCIENCE_TERMINAL=NO\`, \`PR65/67/70/71=HOLD_SCOPED\`, \`R34=SEPARATE\`.

## 10. Abnahmeformel

\`\`\`text
FABRIC_G0_BLUEPRINT = PASS_WHEN_SOURCE_EXACT_ON_GITHUB
FABRIC_G1_RUNNER = HOLD_CAPABILITY_NOT_VERIFIED
FABRIC_G2_INGRESS = HOLD_NOT_DEPLOYED
FABRIC_G3_SECURITY_AND_QUEUE = HOLD_NOT_EXECUTED
FABRIC_G4_END_TO_END_EXTERNAL_TO_NODE = HOLD_NOT_EXECUTED
FABRIC_G5_FALLBACK_FAILOVER = HOLD_NOT_EXECUTED
FABRIC_G6_WWW_B2_B3 = HOLD_NOT_VERIFIED
CLAIM = C1_DESCRIPTIVE_ONLY
NO_AUTO_ROLE_PROMOTION = YES
NO_NEW_CURSOR_WORKER = YES
\`\`\`

*NEXUS OMEGA — Trigger heißt kausal nachweisbare Kommunikation, nicht ungeprüfte Ausführung. Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
