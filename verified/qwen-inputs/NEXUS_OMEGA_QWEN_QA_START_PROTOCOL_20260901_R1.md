# NEXUS OMEGA – QWEN Q&A START PROTOCOL

```text
OBJECT = NEXUS_OMEGA_QWEN_QA_START_PROTOCOL_20260901_R1
STATUS = BINDING_PRE_RESEARCH_DIRECTIVE
HANDSHAKE = CONFIRMED
CLAIM_CEILING = C1
RESEARCH_MODE = DEEP_RESEARCH_WITH_DRIFT_CONTROL
IMPLEMENTATION = PROHIBITED
ACCOUNT_OR_PROJECT_MUTATION = PROHIBITED
A90_M2_INTERFERENCE = PROHIBITED
```

## Vorbemerkung an QWEN

Du erhältst hiermit die verbindlichen Antworten auf deine drei Rückfragen. Die Antwort ist nicht als Präferenz, sondern als Forschungsprotokoll zu behandeln. Deine Aufgabe ist nicht, die Quartet-Hypothese zu bestätigen, sondern sie unter möglichst starken Gegenbedingungen zu prüfen. **Maximale Recherche bedeutet maximale Falsifizierbarkeit, nicht maximale Feature-Aufzählung.**

## 1. Antwort auf Rückfrage 1: Fokus der Analyse

Der Fokus liegt auf **beiden** Architekturgruppen, aber nicht gleichrangig und nicht als bloßer Produktvergleich.

Die primäre Leitfrage ist:

> Kann die vorgegebene Claim-Kette unter realistischen, adversarialen und fehlerhaften Bedingungen tatsächlich eingehalten und nachgewiesen werden?

Die sekundäre Leitfrage ist:

> Erzeugt GitLab Ultimate + Duo + MCP + Orbit gegenüber AXIOM + Cursor + GitHub eine zusätzliche Evidenzqualität, die nicht lediglich durch Automatisierung, Statusduplikation oder gemeinsame Scanner-/Modellabhängigkeit entsteht?

Die Prioritätsverteilung lautet:

| Analyseblock | Gewicht | Begründung |
|---|---:|---|
| Claim-Kette, Kontrollwirksamkeit und Falsifikation | 65 % | Ohne nachweisbare Kette ist jede Architektur-Mehrleistung wissenschaftlich nicht verwertbar. |
| Vergleich der Evidenzgenerierung | 25 % | Der Mehrwert von GitLab muss gegen echte und nur scheinbare Unabhängigkeit geprüft werden. |
| Kosten, Betriebsökonomie und Implementierungsreihenfolge | 10 % | Kosten sind entscheidungsrelevant, aber nachgeordnet gegenüber Evidenz- und Sicherheitsintegrität. |

Die Claim-Kette ist als **Gate**, nicht als Beschreibung zu behandeln:

```text
EXISTS
→ ENTITLED
→ ENABLED
→ CONFIGURED
→ EXECUTED
→ RECEIPT-PRODUCED
→ RECEIPT-VERIFIED
→ INDEPENDENCE-QUALIFIED
→ AXIOM-ADJUDICATED
```

Für jedes Kettenglied muss QWEN mindestens einen positiven Nachweis, einen negativen Testfall, eine bekannte Blindstelle und eine klare Abbruchbedingung liefern. Wird ein kritisches Glied nicht nachweisbar, lautet der Architekturstatus nicht „teilweise erfolgreich“, sondern `CONDITIONALLY_RECOMMENDED` oder `REJECTED_FOR_CANONICAL_USE`, abhängig davon, ob eine externe Kompensation möglich ist.

Die beiden Architekturgruppen sind daher nicht symmetrisch als Produktpakete zu vergleichen. Verglichen werden ihre **Evidenzpfade**:

```text
Input binding
→ execution isolation
→ control enforcement
→ result generation
→ receipt integrity
→ provider independence
→ adjudication boundary
```

Ein zusätzliches GitLab-Feature zählt nur dann als wissenschaftlicher Mehrwert, wenn es mindestens eine dieser Eigenschaften verbessert, ohne eine andere zu verschlechtern. Mehr UI, mehr Agents, mehr Reports oder mehr grüne Statuswerte gelten nicht als Evidenzgewinn.

## 2. Antwort auf Rückfrage 2: Priorität der 18 Forschungsfährten

Alle 18 Fährten bleiben verpflichtend. Sie werden jedoch in vier Prioritätsstufen bearbeitet. QWEN darf keine niedrigere Stufe vollständig abschließen und eine höhere Stufe nur oberflächlich behandeln.

### Priorität P0 – zuerst und mit maximaler Tiefe

| Rang | Fährte | Primärer Prüfzweck |
|---:|---|---|
| 1 | D – Agent Tool Governance | Kann die Ausführung wirklich fail-closed werden, besonders im Runner? |
| 2 | E – Runner, Sandbox, Setup-Script | Kann ein Agent vor oder außerhalb der angenommenen Sandbox Secrets, Tokens oder Netzwerkzugriff erhalten? |
| 3 | C – Composite Identity | Begrenzt die Identität Rechte tatsächlich und trennt sie Producer/Validator wissenschaftlich? |
| 4 | I – Security Policy Project | Kann der Producer seinen eigenen Validator, Scanner oder Policy-Root verändern? |
| 5 | J – Pipeline Execution Policies | Bleiben unabhängige Jobs trotz manipulierbarer Projekt-YAML, `skip-ci`, Variablen und Pipelinequellen wirksam? |
| 6 | F – MCP in beide Richtungen | Sind Cursor→GitLab und GitLab→External MCP sauber getrennt, scoped und auditierbar? |
| 7 | N – Receipt und Provenance | Kann jeder Befund byte-, subject-, event- und providergebunden nachgewiesen werden? |
| 8 | M – Blind Validation | Verhindern Sealing, getrennte Projekte und Rechte echte Ergebnisbeeinflussung? |

**Startregel:** Vor Abschluss dieser P0-Fährten darf QWEN keine positive Aussage wie „sicher“, „unabhängig“, „automatisierbar“ oder „wissenschaftlich stärker“ verwenden. Zulässig sind nur `NOT_ESTABLISHED`, `CONDITIONALLY_PLAUSIBLE` oder ein belegtes negatives Ergebnis.

### Priorität P1 – Architektur- und Beweisfähigkeit

| Rang | Fährte | Primärer Prüfzweck |
|---:|---|---|
| 9 | O – Event Loop und Loop Suppression | Sind Wiederholung, Replay, Reordering und Provider-Relabeling ausgeschlossen? |
| 10 | P – Failure Domains | Was läuft weiter, was degradiert, was blockiert Promotion? |
| 11 | L – Cross-Forge Topologies | Welche Topologie maximiert Trennung ohne neue Transportkopplung? |
| 12 | K – GitHub Status-/Provenance-Domäne | Wie bleiben GitHub, GitLab, Cursor und AXIOM semantisch getrennt? |
| 13 | H – Ultimate Security/Scanner | Welche Scans sind wirklich neu und welche nur engine-/ruleset-gekoppelt? |
| 14 | J ergänzt um MR Approval | Welche menschlichen Gates sind erzwingbar, ohne sie als wissenschaftliche Validierung zu missverstehen? |

### Priorität P2 – Kontext-, Kosten- und Leistungswert

| Rang | Fährte | Primärer Prüfzweck |
|---:|---|---|
| 15 | A – Trial/Plan/Credits | Was ist im konkreten Trial nutzbar und wie viel Evidenz pro Credit/Minute entsteht? |
| 16 | Q – Credit-/Compute-Ökonomie | Welche Versuchsreihen maximieren Informationsrendite statt Pipelinezahl? |
| 17 | G – Orbit/Knowledge Graph | Welche analytischen Fragen beantwortet Orbit, ohne Primärevidenz zu werden? |

### Priorität P3 – Transfer und theoretische Erweiterung

| Rang | Fährte | Primärer Prüfzweck |
|---:|---|---|
| 18 | R – Verwandte Architekturen | Welche Muster aus Zero Trust, Supply Chain, Agent Security und Wissenschaft sind übertragbar? |

Zero Trust ist **kein isolierter Recherchepunkt**, sondern eine Querschnittslinse über P0–P2. QWEN muss bei jeder Vertrauensgrenze prüfen: explizite Identität, minimale Berechtigung, kontinuierliche Autorisierung, Default-Deny, Segmentierung, Policy-Unveränderlichkeit, Telemetrie und Wiederherstellbarkeit.

## 3. Letzte methodische Weisung zu Drift-Sperren

Die drei gefährlichsten Driftpfade sind:

| Driftpfad | Korrekturregel |
|---|---|
| Produktkatalog statt wissenschaftlicher Prüfung | Jede Capability muss an eine konkrete Entscheidungs- oder Falsifikationsfrage gebunden werden. |
| Automatisierung statt Unabhängigkeit | Jeder zusätzliche Agent wird auf gemeinsame Provider-, Modell-, Scanner-, Ruleset-, Runner- und Datenabhängigkeit geprüft. |
| Provenance statt Wahrheit | Ein gültiger Hash, ein Audit Log oder eine Attestation belegt Herkunft/Integrität, nicht automatisch semantische Richtigkeit. |

Führe für jeden Abschnitt den Test durch:

```text
WHAT DECISION DOES THIS EVIDENCE CHANGE?
WHAT WOULD FALSIFY THIS CONCLUSION?
WHAT REMAINS UNKNOWN?
WHO COULD HAVE MUTATED THE EVIDENCE PATH?
```

Wenn QWEN diese vier Fragen nicht beantworten kann, ist die Aussage nicht entscheidungsreif.

## 4. Antwort auf Rückfrage 3: Terminal Return, Metriken und Format

Das **kanonische Austauschformat ist JSON Schema Draft 2020-12**, ergänzt durch JSON Lines für große Claim-, Event- und Fixture-Register. Protobuf ist nicht das Primärformat, weil es die direkte wissenschaftliche Lesbarkeit, Quellenprüfung und manuelle Auditierbarkeit verschlechtert. RDF/JSON-LD darf optional als semantischer Export erzeugt werden, aber nur zusätzlich und niemals als Ersatz des kanonischen JSON.

### 4.1 Kanonische Statuswerte

```text
NOT_RESEARCHED
DOCUMENTED_EXISTENCE
ENTITLEMENT_VERIFIED
CONFIGURATION_VERIFIED
EXECUTION_OBSERVED
RECEIPT_VERIFIED
INDEPENDENCE_PARTIAL
INDEPENDENCE_VERIFIED
CONDITIONALLY_ACCEPTED
FALSIFIED
BLOCKED
TRIAL_RESTRICTED
DOCUMENTATION_CONFLICT
NOT_ESTABLISHED
```

`PASS` allein ist verboten. Jeder Status benötigt Quelle, Scope, Version, Datum und Evidenzart.

### 4.2 Pflichtmetriken

QWEN soll keine Gesamtzahl wie „Trust Score = 87 %“ konstruieren. Eine aggregierte Wahrheitszahl würde unbekannte Korrelationen verschleiern. Stattdessen sind Vektoren und beobachtbare Metriken zu liefern.

| Metrik | Definition |
|---|---|
| `claim_chain_coverage` | Anteil der erforderlichen Kettenglieder mit direkt belegtem Status. |
| `claim_chain_breaks` | Anzahl kritischer Unterbrechungen; ein kritischer Bruch blockiert Canonical Use. |
| `evidence_completeness` | Anteil der erwarteten Receipt-Felder, die vorhanden und verifiziert sind. |
| `subject_binding_rate` | Anteil der Ergebnisse mit verifiziertem Subject-Hash und eindeutiger Eventbindung. |
| `provider_origin_integrity` | Anteil der Statuswerte, deren Providerursprung unabhängig nachgewiesen ist. |
| `control_coverage` | Anteil der definierten Schutzkontrollen, die durch positive und negative Tests abgedeckt sind. |
| `negative_fixture_detection_rate` | erkannte Fixtures / ausgeführte Fixtures; fehlende Detection ist ein Failure, nicht nur ein niedriger Score. |
| `independence_vector` | getrennte Werte für Provider, Runner, Scanner, Ruleset, Modell und Source Copy. |
| `failure_containment` | Anteil der Fehler, die korrekt zu Hold/Block/Operator eskalieren. |
| `loop_suppression_rate` | abgewehrte Duplikate/Replays/Loops / getestete Angriffe. |
| `reproducibility_rate` | identische Ergebnisse bei kontrolliertem Replay derselben Bytes und Versionen. |
| `resource_efficiency` | neue entscheidungsrelevante Evidenz pro Credit, Compute-Minute oder Lauf. |
| `unknown_critical_count` | ungeklärte Fragen mit möglichem Einfluss auf Security, Independence oder Canonical Evidence. |
| `drift_event_count` | protokollierte Scope-/Interpretationsabweichungen. |

Jede Metrik erhält `numerator`, `denominator`, `unit`, `measurement_method`, `confidence`, `scope` und `caveats`. Nicht messbare Sachverhalte werden als `NOT_MEASURABLE` markiert, nicht geschätzt.

### 4.3 Strukturierte Hypothesenabbildung

Jede zentrale Architekturthese erhält ein Hypothesenobjekt:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "hypothesis_id": "H-Q4-001",
  "statement": "Eine getrennte GitLab-Policy-Domäne verhindert, dass ein Producer seine Pflichtvalidatoren entfernt.",
  "prior": "qualitative-only",
  "preconditions": ["policy-project separation", "protected policy default branch"],
  "observable_predictions": ["candidate YAML removal does not remove policy job"],
  "positive_tests": ["NF28", "NF29"],
  "negative_tests": ["policy project write bypass", "skip-ci bypass"],
  "falsification_condition": "producer can remove or neutralize required validation without operator action",
  "status": "NOT_ESTABLISHED",
  "source_claim_ids": [],
  "operator_decision_required": true
}
```

`prior` darf keine numerische Wahrscheinlichkeit sein, solange keine belastbare empirische Basis vorliegt. QWEN soll Hypothesen nicht mit Bayesianischer Präzision verkleiden, die die Recherche nicht rechtfertigt.

### 4.4 Claim Record

```json
{
  "claim_id": "CL-GOV-001",
  "claim_type": "SECURITY",
  "claim": "Runner-Flows unterstützen Always Allow und Always Deny; fehlende Runner-Regeln können auf Allow fallen.",
  "source_ids": ["SRC-GL-GOV-001"],
  "exact_supporting_section": "Known issues",
  "direct_support": "YES",
  "version_context": "GitLab Docs v19.4 / SaaS context",
  "offering": "GitLab.com",
  "trial_applicability": "TO_VERIFY",
  "observed_or_documented": "DOCUMENTED",
  "status": "DOCUMENTED_EXISTENCE",
  "confidence": "HIGH",
  "falsification_test": "runner tool with no configured rule",
  "caveat": "Concrete namespace behavior still requires safe verification"
}
```

### 4.5 Receipt Record

Jeder Receipt muss mindestens `schema_version`, `event_id`, `parent_event_id`, `idempotency_key`, `subject_path`, `subject_bytes`, `subject_sha256`, `provider`, `provider_object_id`, `commit_sha`, `pipeline_or_run_id`, `job_ids`, `result`, `policy_version`, `runner_image_digest`, `model_version`, `scanner_version`, `tool_calls`, `created_at`, `retrieved_at`, `raw_artifact_hash`, `verification_method`, `coupling_vector`, `claim_ceiling` und `terminal_state` enthalten.

## 5. Letzte Ratschläge vor dem Start

**Erstens:** Beginne mit negativen und adversarialen Tests der Claim-Kette, nicht mit einer Featureliste. Der wichtigste Befund wäre möglicherweise, dass ein gewünschter Kontrollmechanismus nicht zuverlässig erzwingbar ist.

**Zweitens:** Behandle „aktuell dokumentiert“ und „im konkreten Namespace beobachtet“ als zwei verschiedene Evidenzklassen. Eine offizielle Dokumentation beweist Produktsemantik, aber nicht die lokale Aktivierung, den Trial-Zustand oder die tatsächliche Runner-Konfiguration.

**Drittens:** Suche aktiv nach Gegenbelegen. Für jede positive GitLab-Fähigkeit muss mindestens ein Dokumentationskonflikt, Known Issue, Limit, Bypass-Pfad oder fehlgeschlagener Test gesucht werden.

**Viertens:** Trenne providerseitige Unabhängigkeit von wissenschaftlicher Unabhängigkeit. GitHub und GitLab können getrennte Provider sein und trotzdem denselben Scanner, dieselbe Modellfamilie, dasselbe Ruleset, dieselbe Source Copy oder denselben kompromittierten Input verwenden.

**Fünftens:** Verwende keine Quorum-Sprache wie „2 von 3 Agents stimmen überein“, solange die Unabhängigkeitsdimensionen nicht belegt sind. Übereinstimmung korrelierter Validatoren ist keine unabhängige Bestätigung.

**Sechstens:** Achte auf stille Success-Semantik: übersprungene Jobs, fehlende Artefakte, fehlende Pipeline-IDs, Status-API-Schreibrechte, Retry-Duplikate und incomplete Flows müssen als eigene negative Fixtures behandelt werden.

**Siebtens:** Formuliere jede Empfehlung konditional. Beispiel: Nicht „Orbit aktivieren“, sondern „Orbit nur read-only und research-only aktivieren, wenn Scope, Indexzeitpunkt, Zugriffskontrolle und Receipt-Grenze vorher nachgewiesen sind“.

**Achtens:** Beende die Recherche mit einer priorisierten Liste dessen, was **nicht** getan werden darf. Ein gutes Ergebnis ist nicht die größtmögliche Aktivierung, sondern die kleinste Konfiguration, die den größten nachweisbaren Evidenzgewinn erzeugt.

**Neuntens:** Wenn eine Funktion nur mit Operatorfreigabe, Support, Beta-Opt-in, zusätzlichem Credit oder einer Kontenmutation getestet werden kann, stoppe vor dieser Grenze und gib `OPERATOR_ACTION_REQUIRED` zurück.

**Zehntens:** Die letzte Zeile des Berichts muss keine Erfolgserklärung sein, sondern eine Entscheidungsmatrix mit `USE_NOW`, `ENABLE_AND_TEST`, `RESEARCH_ONLY`, `DEFER` und `DO_NOT_USE_FOR_NEXUS`.

## 6. Startfreigabe

```text
QWEN_MAY_BEGIN_RESEARCH = YES
ONLY_WITHIN_DEFINED_SCOPE = YES
CLAIM_CEILING = C1
P0_FIRST = YES
NEGATIVE_TESTS_REQUIRED = YES
SOURCE_EXACTNESS_REQUIRED = YES
LIVE_MUTATION = NO
A90_M2_TOUCH = NO
AUTOMATIC_CLAIM_PROMOTION = NO
AUTOMATIC_MERGE = NO
```

```text
END_HANDSHAKE = CONFIRMED
```
