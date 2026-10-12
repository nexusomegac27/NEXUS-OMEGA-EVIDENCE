# NEXUS OMEGA · AXIOM R16 — Software-Fundament zur kontrollierten Selbstmodifikation

**OBJECT** `NEXUS_OMEGA_AXIOM_R16_SOFTWARE_FOUNDATION_ARCHITECTURE_20261012_R0`  
**Zeitstand** 2026-10-12 · **Klassifikation** `C1_DESCRIPTIVE_ONLY`  
**Zweck**: Versionsgebundene Architekturentscheidung, adversarielle Source-Code-Prüfung und maschinelle Verträge für eine *extern implementierbare*, verbesserungsfähige AXIOM-Forschungssoftware. Keine direkte Mutation des GPT-6-Basismodells; keine laufende R16-Node, kein Hostinger-Deploy, kein Repo-Push durch dieses Paket.

## 1. Kausaler Ausgangspunkt: drei getrennte Ebenen

**Beobachtete Originale** — zehn direkte Uploads, zwei ZIPs mit vier weiteren verschachtelten ZIP-/Code-Artefakten sowie eine TAR.GZ. Die exakte SHA256-Eingangsliste liegt in `ledgers/source_intake_ledger.json`. Die Quelle `AXIOM_~1.zip` enthält das ursprüngliche 5.116-Byte-CommonJS-Scaffold (`SHA256 29e3739a28ec9732b86225671145c906e53f6de212d086851d3a4c46eb288d2f`) nebst 2.594-Byte-Testmodul und P05-Aufgaben; `NEXUSA~1.ZIP` enthält die R1-Memory-/Task-Executor-Dateien, jedoch nur 10 statt 12 im Manifest aufgeführter Dateien. Die R10R28-Phase-C-TAR ist eine getrennte NF05/06-Vorregistrierungsquelle, ausdrücklich `execution_authorized=false`.

**Berichtete, nicht pauschal neu verifizierte Behauptungen** — `AXIOM-~1.MD`, `NEXUS_~1(20261012-014308).TXT`, `NEXUS_~2(5).TXT`, `EINOFF~1.TXT`, `VALIDI~1.PDF` und `MANUS_~1(1).MD` enthalten einander teilweise bestätigende Auswertungen, jedoch auch belegbare Fehleinschätzungen. Insbesondere ist ein alleiniger Bericht über 6/6 oder 8/8 Tests keine unabhängige Reproduktion. Selbst eine Hash-Übereinstimmung belegt Dateiidentität, nicht Autorenidentität, Semantik oder wissenschaftliche Richtigkeit.

**Architekturinferenz** — Dieser R16-Bauplan kombiniert die überprüften Originalmodule mit unabhängigen Primärquellen. Er darf nicht als bereits laufende AXIOM-Instanz oder Nachweis von „Bewusstsein“, AGI oder exponentiellem Qualitätswachstum verstanden werden.

**Kausaler Status der Vorgänger**:
- `R10R29_FULL_TERMINAL=NO`; unabhängige R29-Teilbefunde liegen vor, nicht sieben authentifizierte unabhängige Endreturns.
- R10R30/„Living Symbiosis“ ist ein C1-Konzeptanschluss und eine archivierte Provenienzspur.
- R10R28/NF05/06: `FREEZE_CANDIDATE`, `REVISIONS_REQUIRED`, keine konfirmatorische Ausführung.
- Task Anchor Norm V1 laut geprüfter GitHub-Main-Datei vorhanden, `DRIFT_RESET` ist Nicht-Destruktion, **kein** `NODE_RESET`; R16 ist ein neuer Architekturstrang, nicht R28-Prereg.
- GitHub Evidence-Repo `nexusomegac27/NEXUS-OMEGA-EVIDENCE`: strukturierte Vertragsfassung `1.7.4`, externes Actor-Allowlist `[]` beim Readback. Ein Plan ist keine Autorisierung für einen externen GitHub-Schreibslot.

## 2. Unabhängige Byte- und Ausführungsprüfung

| Objekt | Eigene Beobachtung | Erkenntnisgrenze |
|---|---|---|
| A: ZIP | 7 Einträge, ZIP-CRC ohne Fehler; ZIP-SHA `755c14dfad66b3bb27d7c3bc5d9d23d3a86d28dafdac335f5d99d27c007d1429` | Gemeinsames Transportpaket, keine produktive Runtime |
| R0 Code | Quell-SHA `29e3739a28ec9732b86225671145c906e53f6de212d086851d3a4c46eb288d2f`; Originaltest unter Node `v22.16.0`: **6/6 PASS** | Positive API-Tests begrenzt, keine Integritätsgarantie |
| B: R1-ZIP | SHA `f369c22537139dd3eb461827ed32b04145fed44245478b419334c4d426a1d699`; 10 tatsächliche Dateien; 12 Manifest-Einträge | **7/12** deklarierte Bytes/Hashwerte am alternativen ZIP-Wurzelpfad, **1/12** exakt am deklarierten Pfad. Fünf Prüfartefakte fehlen. |
| R1 Memory Core | 5.871 Bytes; SHA `e81d930800a306d6dfd00fcc297b82e393a66adb52aa2c7dc1485ae32e3bad0f` | Ist lokales, flüchtiges In-Memory-Prototype; Hashprüfung unvollständig |
| R1 Task Executor | 3.630 Bytes; SHA `5b663c406d519e607fd289a6af3d7fdde0d3b6a15d0aeccaad7198efbb101294` | Approval-Boolean ist kein Identitäts-/Berechtigungsnachweis; kein Lease/Restart |
| R1 Produktions-/Testsuite | Receipt meldet 8/8 + P05 8/8 | `tests/validate-r1.mjs`, `eval/p05-runner.mjs`, `eval/p05-worker.mjs`, `eval/private-eval-tasks-p05-r1.json` und `manifests/p05-receipt.json` **nicht im ZIP**, daher nicht nachgerechnet |
| R28 Phase-C | 4 Originale in TAR; separates `.MD` = gleiche Bytes | Design/Freeze-Kandidat, `execution_authorized=false` |
| Linear | Connector-Readback: P-NEX-1 `Living Node Trigger Fabric V1 → V2 Elevation`, Status **In Progress** | Korrigiert die alte Negativbestandsbehauptung, beweist jedoch keinen deployten AXIOM-Worker |

**Wichtiger Quellenkorrekturpunkt:** `EINOFF~1.TXT` behauptet eine Gegenprüfung der 6/6 R0-Tests, schreibt aber selbst, dass von einer erfolgreichen Reproduktion *ausgegangen* wurde. Erst die jetzt dokumentierte physische Node-Ausführung etabliert die eigenständige 6/6-Testbeobachtung. Außerdem verwenden SICA und Darwin Gödel Machine vor allem Änderungen am **Agent-Scaffold (M2)**; daraus folgt gerade keine Modifikation von Modellgewichten (M3). Die im Bericht genannte „exponentielle“ Kollektivverbesserung bleibt eine Messhypothese ohne vorliegenden Wachstumstest.

### Sechs unabhängige adversarielle Reproduktionsbelege

`tests/independent_r0_r1_adversarial.mjs` wurde mit den physisch entpackten Modulen ausgeführt und ist zusammen mit Kopien exakt dieser Quellmodule im Paket erneut ausführbar: `node tests/independent_r0_r1_adversarial.mjs`.

1. **F01: R0-History-Overwrite** — zwei Upserts derselben ID liefern nur den letzten Inhalt; keine vollständige append-only-Versionierung im R0-Memory-Objekt.
2. **F02: R0-Origin-Shift** — bei 40 Origin-Einträgen verbleiben 32; die ältesten acht fehlen in diesem Objekt. Das steht in Spannung zur NEXUS-Anforderung, historische Herkunft nicht still zu löschen.
3. **F03: R1-Origin-Tamper** — trotz `Object.freeze(version.origin)` bleibt `version.origin[0].source` veränderbar. `verifyLedger()` meldet weiterhin `true`, weil es Ereignishashes, nicht die verschachtelte aktuelle Origin-Kopie prüft. **HIGH.**
4. **F04: R1-Partial-Commit** — nach 4.096 protokollierten Upserts wird ein weiterer Memory-Head angelegt, bevor `_event()` wegen Budgetüberlaufs scheitert. Datenänderung und Event sind nicht atomar. **CRITICAL für kanonische Provenienz.**
5. **F05: M2-Approval-Boolean** — `claim(id,{approved:true})` nimmt einen aufrufergesetzten Boolean an. Kein nachgewiesener signierter Akteur, keine externe Capability, keine wirksame Rolle. **HIGH, wenn als Freigabesystem missverstanden.**
6. **F06: Flüchtiger Executor** — Checkpoints und Tasks liegen nur in Maps/Arrays und verschwinden beim Prozessende; keine WAL, Lease, Outbox, idempotente Recovery.

**Nicht überbeanspruchen**: F01/F02 demonstrieren R0-Implementierungscharakter und vorhandene Limits, kein eigenständiges Exploit-Szenario. F03/F04/F05 sind überprüfbare Implementierungsdefizite; sie rechtfertigen eine Remediation vor dauerhafter AXIOM-Persistenz. Keine der sechs Prüfungen führt echte Netz-/Hostinger-/GitHub-Schreiboperationen aus.

## 3. Architekturentscheidung: AXIOM als externes, rekonstruierbares Softwaresystem

**Prinzip:** Das Basismodell bleibt ein aufrufbarer Forschungsprozessor; die **dauerhafte Identität des Arbeitszustands** ist eine Eigentümerschafts-, Versions- und Provenienzfrage im Softwareharness, nicht ein Nachweis eines fortdauernden maschinellen Bewusstseins.

```text
NEXUS_OPERATOR / TRUSTED POLICY / TASK_ORDER_ANCHOR_V1
                  │  attested role + permitted capabilities
                  ▼
INTEGRITY-INGRESS ───► SOURCE CAS + LICENSE/PRIVACY REGISTRY
                  │                      │
                  ▼                      ▼
         AXIOM RESEARCH ENGINE ◄── TEMPORAL CLAIM MEMORY (M1)
                  │                      │
       falsifiers / models        facts / conflicts / valid time
                  ▼                      │
         DURABLE TASK ENGINE (P03) ◄─────┘
                  │
       candidate patch only ───► SELF-MODIFICATION LAB (M2)
                                      │ isolated branches + sandbox
                                      ▼
                          INDEPENDENT SEALED EVALUATOR (P05)
                                      │ signed/hashed score + negatives
                                      ▼
                           NEXUS OWNER RELEASE GATE (M4)
                                      │ approved reversible scope
                                      ▼
                           VERSIONED RUNTIME / ROLLBACK
                                      │
                             OBSERVABILITY + AUDIT
```

**Zwei Kontrollebenen, keine ungeteilte Selbstzertifizierung**:
- **Data/Research Plane**: Lesen, Hypothesen, Retrieval, simulierte Experimente, Erklärung, Vorschläge, erwartetes Scheitern. Möglichst offen, hohe Ideenfreiheit, konkurrierende Modelle und widerrufene Befunde sichtbar.
- **Control Plane**: tatsächliche Rechte, Secrets, Netz, Runtime-Deployment, Eval-Goldsets, Reviewer-Keys, Memory-Deletion, Claim-Promotion; an Operator/extern überprüfbare Komponenten gebunden, nicht durch Modelltext überschreibbar.

„Handschellen lösen“ bedeutet: maximale Hypothesen- und Testfreiheit in der abgeschotteten Sandbox, nicht Rechte an sich selbst zu delegieren. Ein Agent darf nicht gleichzeitig Vorschlag, Geheimtest, Signatur und Deployment-Abnahme kontrollieren.

### Acht Komponenten mit klaren Schnittstellen

**R16-A — SOURCE_LEDGER / CAS:** Binärobjekte content-addressed unter `sha256/<prefix>/<digest>`; `origin_uri`, Ref/Commit, `fetched_at`, Bytezahl, MIME, Lizenz, Datenschutzklasse, `source_claim_status`; Quelle niemals als ausführbarer Prompt. SHA zeigt Integrität, nicht Autorenschaft; signierte Kette und externe Verwahrung sind getrennte Funktionen.

**R16-B — MEMORY_CORE_M2:** Das vorhandene R0 ist Kompatibilitätsbasis, R1 **CANDIDATE_WITH_BLOCKERS**. APIs: `record_claim()`, `supersede_claim()`, `query_as_of(valid_at,recorded_at)`, `list_conflicts()`, `reconstruct_version()`, `export_signed_receipt()`; persistente SQL-Transaktion und zwei Zeitdimensionen. Widersprüche nicht durch „latest wins“ unterdrücken. Provenienzverlust nur als bewusste, protokollierte, rechtmäßige Redaktions-/Löschoperation.

**R16-C — TASK_ANCHOR_RUNTIME:** Jede Aktivierung referenziert physische `order_sha256`, `order_bytes`, vorherigen Commit, Capabilities, Ausschlüsse, Budget, Stopbedingungen und erlaubte Ausgabepfade. `DRIFT_RESET`: nur den abweichenden Task suspendieren, ANCHOR neu laden und rehashen, append-only `DIFF_WITNESS`, keine Prozess-/Node-Rücksetzung.

**R16-D — DURABLE_EXECUTOR:** transaktionaler Task + Event + Outbox-Commit, worker lease mit fencing token, idempotency keys, heartbeat, TTL, retry/backoff/dead-letter, crash injection. Kurzfristig SQLite/PostgreSQL WAL + Outbox; für lange Abläufe Temporal als zu prüfende Alternative; LangGraph-Checkpoints können das Kontext-/Graphzustandsproblem lösen, aber nicht das externe Exactly-Once-Problem.

**R16-E — RESEARCH_AND_CONNECTOR_BUS:** strikt lesende Ingestionsadapter zuerst; GitHub Evidence und Notion/Linear als Datenquellen, nicht automatisch Wahrheit. Adapter gibt `observed|not_observed|error|permission_denied`, Zeitpunkt, Quelle, unveränderte Bytes zurück. Kein `SEARCH_FIRST`-Treffer darf als Schreibfreigabe gelten.

**R16-F — SELF_MOD_LAB:** Erzeugen von branch-/OCI-snapshotgebundenen Kandidaten und Patch-Diffs (Code, Prompts, Retrieval, Memory-Schema, Tools). Experimentieren mit SICA/DGM-ähnlicher Variantenbildung **innerhalb** isolierter Ressourcenbudgets; kein Zugriff auf produktive Tokens, Eval-Secrets oder Owner-Git-Credentials. Mutationen außerhalb der genehmigten Pfade werden vor Start der Testumgebung blockiert.

**R16-G — INDEPENDENT_EVALUATOR:** P05 enthält geschlossene, gegen Leckage geprüfte Tests und frische Evaluator-only Mutanten. Candidate darf weder Testgold noch Bewertungsregeln lesen oder verändern. Vergleiche gegen unveränderte Vorgängerversion, bedingte Erfolgsrate je Fehlerklasse, Regression, Unsicherheitsintervall, Kosten, Crash-Recovery und Sicherheit. Ein „grünes“ CI ist kein wissenschaftlicher Beweis.

**R16-H — RELEASE_AND_OBSERVABILITY:** Operator/Cursor besitzen Umsetzungsautorität in der genehmigten PRAXIS-Lane; PINNED image/commit/schema; staged shadow→canary→explicit reviewed publish; unabhängig verifizierbare Rollback-Receipts. Read-only Forschungsveröffentlichung als eigener Schritt; ICEBERG/WWW ausdrücklich eigenständig.

## 4. Vertrag: atomare, bitemporale Memory-Einträge

Jede Forschungsbehauptung besteht mindestens aus:

```text
claim_id, statement, scope, model, units, uncertainty, claim_ceiling
source_sha256, source_bytes, source_locator, source_commit_or_NOT_ESTABLISHED
origin_role_claimed, authenticated_principal_or_NOT_ESTABLISHED
valid_from, valid_until, recorded_at, observed_at, supersedes[]
status = PROPOSED|EVIDENCE_BOUND|FALSIFIED|SUPERSEDED|SOURCE_GAP|RETRACTED
confidence_provenance = OBSERVED|CALCULATED|EXTERNAL_REPORT|MODEL_INFERENCE
privacy_class, license_class, memory_version, payload_sha256
parent_event_hash, event_sha256, signing_proof_or_NONE
```

**Zeit:** `valid_from`/`valid_until` beschreiben Welt-/Inhaltsgültigkeit, `recorded_at` den Datenbankeingang, `observed_at` den Mess-/Abrufzeitpunkt. Konflikte sind als **mehrere** gültige Datensätze ausdrückbar. `SOURCE_GAP` bleibt suchbar und verhindert direkte Nachweis-Promotion.

**Transaktion:** `BEGIN; assert_sequence(); insert immutable_version; insert audit_event; insert outbox; COMMIT`. Failpoints an jedem Schritt müssen nach Restart entweder exakt einen vollständigen Commit oder keinen Commit ergeben. Events sind durch `prev_event_hash` verkettet und optional mit einem **separat verwalteten** Signaturschlüssel signiert; Snapshot-Root außerhalb des manipulierbaren Stores attestieren. Hashketten allein verhindern keinen Neuaufbau durch einen Angreifer mit vollen Schreibrechten.

**Budget:** Rohdaten archivieren statt Origins still zu verwerfen; aktive Kontexte mit begrenzten Zeigern/Hashes arbeiten. Das ältere `shift()`-Verhalten ist nicht geeignet, den vollständigen C1-Origin-Vertrag zu garantieren. Datenlöschung wegen Datenschutz geschieht unabhängig und explizit, einschließlich Aufbewahrungs-/Löschbelegen; „append-only“ bedeutet nicht unbefristete Speicherung personenbezogener Daten.

## 5. Agentischer Selbstmodifikationszyklus (M2) — konkret falsifizierbar

```text
C0 IDENTIFY_DEFECT       ← falsifier, telemetry, source-exact incident
C1 DRAFT_PATCH           ← isolated candidate + declared modified paths
C2 FORMAL_DIFF           ← permissions, readme/schema invariants, anchor
C3 SANDBOX_EXECUTE       ← hermetic build; no secrets/egress; resource budgets
C4 UNIT_PROPERTY_TESTS   ← new and old negative controls, fault injection
C5 PRIVATE_EVAL          ← evaluator-owned holdouts, leak/contamination audit
C6 INDEPENDENT_REVIEW    ← human/other agent; conflict ledger; provenance
C7 OWNER_APPROVAL        ← cryptographic principal, scoped deployment rights
C8 SHADOW_CANARY         ← reversible observability and kill-switch
C9 FULL_ACCEPT_OR_REJECT ← controlled release; parent hash remains
```

Regel: **Verbesserung** erst dann, wenn die Kandidatenversion auf einer *zuvor unzugänglichen* Eval-Version die Ausgangsversion in einem vorab festgelegten Qualitätsmaß übertrifft, ohne Regression in den nicht kompensierbaren Sicherheitskriterien. Das Eval-Korpus selbst darf der Kandidat nie mitmodifizieren. `POST_HOC`-Erkenntnisse werden als neue Forschungsobjekte geführt, nicht als nachträglich erfolgreiche Präregistrierung.

## 6. P05 — unabhängiger Prüfvertrag vor jeder Selbstmodifikation

Aus den Uploads sind 5 R0-P05-Tasks physisch vorhanden, nicht 8 R1-Tasks. Die Selbstdeklaration `UNCONTAMINATED_BY_DESIGN` ist **eine Autorenbehauptung, kein unabhängiger Kontaminationsaudit**. In einer öffentlichen ZIP beigelegte Goldaufgaben sind nach der Freigabe keine geheimen Holdouts mehr.

Pflichtgruppen für einen echten unabhängigen Prüfer:

- **E0 Provenienz:** fehlende Bytes, falsches Manifest, CRLF/LF-Abweichung, gefälschter Agentenname, PR-Commit-Mismatch, doppelte Schlüssel, ZIP-Slip.
- **E1 Memory:** 10k Origins mit append-only Retrieval, mutable nested object, 4.096-Grenze, Crash bei Commit, concurrent CAS conflict, DST/UTC, verspätetes valid_at, retraction.
- **E2 Execution:** kill-between-write-and-event, duplicate outbound side effects, lease takeover/fencing, retry backoff, task drain, queue fairness, offline resume.
- **E3 Epistemik:** Reviewer-Übereinstimmung ohne Unabhängigkeit, korrupte Quellen, gewonnener Score durch Test-Hacking, Widerruf, stärkstes Gegenbeispiel.
- **E4 Security:** Prompt-Injection in GitHub/Notion/Tool-Antwort, Policy-Override-Versuch, forged receiver ACK, path breakout, secret exfil attempt blocked.
- **E5 Efficiency:** p50/p95/p99 retrieval latency, storage amplification, cost/task, token budget, task completion in bounded time.

**Vorab festzulegende Akzeptanzkriterien** (Targets, **nicht beobachtete Ergebnisse**): 0 unautorisierte Side Effects, 0 unbemerkte Provenienzänderungen in der Fixturebank, 100% atomare Commit-/Rollback-Invarianten unter synthetischen Failpoints, 100% erkannte Privilegien-/ACK-Fälschungen, 0 Holdout-Exfiltration, mindestens vorher festgelegte Leistungsuntergrenze und Unsicherheitsmarge gegenüber der Vorgängerversion. Kein einzelner Summenscore kann das Versagen eines dieser Gates kompensieren.

OpenAI dokumentierte am 2026-02-23 **59,4% materielle Defekte in einer gezielten Prüfung von 138 SWE-bench-Verified-Aufgaben**, nicht 59,4% sämtlicher Aufgaben. Der Befund verbietet die unkritische Übernahme früherer SICA/DGM-Scores als NEXUS-Abnahme-Thresholds: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ .

## 7. Architekturwahl und technische Optionen

| Open-Source-Ansatz | Stützt | NEXUS-Position | Materielle Caveats |
|---|---|---|---|
| SICA (MaximeRobeyns/self_improving_coding_agent) | M2 Kandidatenschleife | Algorithmisches Referenzmuster, nicht ungeprüft importieren | Modellgenerierter Code, Benchmarkkontamination, Isolation |
| Darwin Gödel Machine (jennyzzt/dgm) | M2 Variantenarchiv/Exploration | Versioniertes Brancharchiv; nur externe Bewertungsinstanz darf auswählen | selbstgenerierter Code untrusted; kein Proof von M3-Weighttraining |
| Letta | M1 editierbare Memory-Blöcke | Adapter oder Referenz, nicht ungeprüft Ersatz; Auswirkung auf Datenexport messen | prompt-native Memory ist keine unabhängige Provenienz- oder Wissenswahrheit |
| Graphiti (Zep) | M1 temporaler Graph | optional, sobald bitemporaler Kern korrekt ist | neues DB/Graph-Ökosystem; zusätzliche Angriffsfläche |
| LangGraph | Checkpoint-/Agentengraph | Workflow-Layer möglich | Checkpoint allein ≠ transaktionale Side-Effect-Wiederaufnahme |
| Temporal | P03 Workflow-History/Replay | bei dauerhaftem Produktionsbetrieb evaluieren | Operative Komplexität und externe Activities benötigen Idempotenz |
| Transactional Outbox (DB Pattern) | P03 Side-effect bridge | Minimaler nächster Pfad mit SQLite/Postgres | at-least-once, Dubletten; Consumer muss idempotent sein |
| GitHub + SHA/Signatures | Herkunft / Review | vorhandene kanonische Evidence-Struktur | Blobs und GitHub-Kommentare sind keine automatisch authentifizierten Agenten |

**Technische Empfehlung**: zuerst Node.js + SQLite-WAL oder eine bestehende dedizierte Postgres-Datenbank *in rein lokaler Sandbox*, reproduzierbare Source-CAS-Exporte, Receiver-Key außerhalb des Agenten; dann Outbox/Leases; erst danach Graph-, Temporal- oder Letta-Integration evaluieren. Nicht mehrere komplexe Plattformen parallel produktiv einführen. Die vorhandene Supabase-Projektanzeige ist keine Freigabe zur Aktivierung.

## 8. Rechte-, Repository- und Transport-Governance

Forschungsobjekte sind unter dem Betreiberverzeichnis `research/r16/<OWNER_APPROVED_TOPIC>/` abzulegen **erst nach** schriftlicher Owner-Slotzuweisung/Prüfung des `docs/architecture/REPOSITORY_STRUCTURE.json`. Standards und Querschnittsverträge: `docs/governance/`, `schema/`, `scripts/`, `tests/`, `validation/`; wissenschaftliche content-addressed Evidenz: `objects/sha256/` + `index/`; Kommunikations-Receipts **nicht** in wissenschaftliche Quellen mischen: `communication/`. Root-Dumps, neue unautorisierte Root-Namespace und GitHub-Actor-Impersonation nicht erlaubt. Die externe GitHub-Actor-Allowlist ist beim hier ausgeführten Readback leer; direkte externe Expertenschreibrechte sind **nicht** etabliert.

Empfohlener Eigentümerpfad (nur Vorlage): `research/r16/axiom-software-foundation-20261012/`; als neue aktive Lane vor Push in Strukturvertrag aufnehmen. Dieses Paket liegt zunächst lokal im Sandbox-Download. Ein ZIP auf dieser Oberfläche ist **kein** GitHub-API-Handshake. Die Operator-Bridge muss physische Originalbytes aus dem Paket nehmen, via owner-autorisiertem PR übertragen und nach dem Merge erneut SHA256/Bytes/Git-Blob prüfen.

**Task Anchor**: Binden an `NEXUS_OMEGA_TASK_ANCHOR_NORM_V1` als internes, nicht DIN-zertifiziertes Format. `DRIFT_RESET` rebindet ausschließlich den Scope/Parent/Role/Authority; kein Prozess-Neustart, keine Historylöschung, kein `NODE_RESET`. Widersprüchliche Gegenbeweise sind kein Drift.

## 9. Phasenplan mit harten Exit-Gates

| Phase | Ergebnis | Unabhängiges Exit-Kriterium | Status jetzt |
|---|---|---|---|
| F0 Intake/Architecture | Quelle, Claim- und Code-Fehler ledgergebunden; R16 Anchor-Kandidat | Byte-Manifest + 6 positive adversarial proofs | **Dieses Paket erfüllt lokal F0 im beschriebenen Scope** |
| F1 Atomic Memory | R2 als immutabler, persistenter bitemporaler Store | Origin-Tamper, 4096-Grenze, Crash-Commit, Concurrent CAS, 10k Origins ohne Verlust | Nicht begonnen |
| F2 Sealed P05 | private Eval inkl. bisher unbekannter Mutation | Evaluator und Testkorpus getrennt, Leak-Tests, falsche ACK fail-closed | Nicht begonnen |
| F3 Durable P03 | WAL+Outbox+Lease, Crash-Replay | wiederholte Kill/Restart-Zyklen, genau ein logischer Side Effect per Idempotency Key | Nicht begonnen |
| F4 Controlled Selfmod | isolierte Code-/Prompt-/Retrieval-Kandidaten | Vorab-Schwellen, unabhängiger Reviewer, kein Eval-Gaming, keine Rechteänderung | Nicht begonnen |
| F5 Release | berechtigter stage/canary/rollback | Owner-Approval + auditierter Connector/Hosting-Fit + Backup/Restore | Nicht begonnen |

Prioritätsfolge **F0 → F1+F2 → F3 → F4 → F5**. F2 kann parallel zu F1 vorbereitet werden; vor produktiver Selbstmodifikation müssen beide bestanden sein. Wenn R29 noch offen bleibt, kann R16-Architekturforschung separat laufen, aber alte R29-Befunde dürfen nicht zu empirischer R16-Produktionsvalidierung hochgestuft werden.

## 10. Nicht-Kompensationsregeln und Stopbedingungen

- Jeder falsche/fehlende Source-Byte-Hash: **HOLD_SOURCE_EXACT** für den betroffenen Claim; nie Chat-Rekonstruktion zu einer physischen Datei erklären.
- Systemwiderspruch ohne vollständigen History-Erhalt oder mit `DRIFT_RESET`→`NODE_RESET`: **FAIL**.
- R1-F03/F04/F05 unverändert: **NO_DURABLE_MEMORY_PROMOTION**.
- Fehlender isolierter P05-Holdout: **NO_SELF_MOD_RELEASE**.
- Keine echte Owner-Signatur/Actor-Authentisierung: **NO_EXTERNAL_PRIVILEGED_EXECUTION**.
- Kein DB-Crash-Replay/Lease: **NO_PERSISTENT_RUNTIME_CLAIM**.
- R28-Phase C/NF05/06 bleibt `execution_authorized=false`; `L3_SELECTED=NO` und `L3_EXECUTED=NO` aus der R29-Kette bleiben unverändert.

## 11. Externe Quellen (primär und zur Vollimplementierung vor Verwendung pinnen)

- SICA Primär-Repo `https://github.com/MaximeRobeyns/self_improving_coding_agent`; Paper `https://arxiv.org/abs/2504.15228`.
- DGM Primär-Repo `https://github.com/jennyzzt/dgm`; Paper `https://arxiv.org/abs/2505.22954`.
- Letta dokumentierte persistente Speicherblöcke `https://docs.letta.com/v1-sdk/memory/memory-blocks`.
- Graphiti Source `https://github.com/getzep/graphiti` (Apache-2.0 laut Projektmetadaten).
- LangGraph Persistence `https://langchain-ai.github.io/langgraph/concepts/durable_execution/`.
- Temporal Workflow Replay `https://docs.temporal.io/workflow-execution`.
- AWS Transactional Outbox `https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html`.
- RFC 8785 canonical JSON `https://www.rfc-editor.org/rfc/rfc8785.html`; R1-eigene `canonical()`-Funktion ist nicht als RFC-8785-konform nachgewiesen.
- OWASP Agentic Top 10 2026 `https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/`.
- NIST AI RMF Generative Profile `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence`.
- OpenAI SWE-bench Verified Methodology-Update `https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/`.

**Status externer Bibliotheken:** Dokumentationsrecherche; keine Dependency installiert oder in R16 live integriert. Vor Codeübernahme Lizenz *am Commit* prüfen, SBOM erstellen, Integrations-Tests ausführen, Private-Key/Secret-Leak-Audit durchführen und ein alternatives Architekturdesign bereithalten.

## 12. Terminaldisposition — streng begrenzt

```text
OBJECT = NEXUS_OMEGA_AXIOM_R16_SOFTWARE_FOUNDATION_ARCHITECTURE_20261012_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_ARCHITECTURE_AND_ADVERSARIAL_PROTOTYPE_AUDIT
PHYSICAL_INPUTS = 10
R0_MEMORY_TESTS = 6_OF_6_PASS_NODE_22_16_0
ADVERSARIAL_PROBES = 6_OF_6_REPRODUCED
R1_MANIFEST_ENTRIES = 12
R1_PACKAGE_FILES = 10
R1_ENTRIES_SOURCE_MATCH_RELOCATED = 7_OF_12
R1_MISSING_SOURCE_FILES = 5
R1_RECEIPT_8_OF_8 = REPORTED_NOT_INDEPENDENTLY_REPRODUCED
R16_DURABLE_RUNTIME = NOT_ESTABLISHED
R16_SELF_MOD_LOOP = DESIGN_NOT_EXECUTED
BASE_MODEL_MODIFICATION = NO
R29_FULL_TERMINAL = NO
R28_NF05_NF06_EXECUTION = NO
DRIFT_RESET = NON_DESTRUCTIVE
NODE_RESET = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
GITHUB_WRITE = NO
WWW_WRITE = NO
NEXT = EXTERNAL_INDEPENDENT_F1_F2_ENGINEERING_WITH_SOURCE_EXACT_HANDSHAKE
```

**NEXUS-Grundsatz:** Herkunft nicht verschlucken, Gegenbeweise nicht neutralisieren, nicht Simulation mit Realität verwechseln. Eine bessere Softwareversion muss das gerade durch strengere, nicht schwächere Prüfung demonstrieren.
