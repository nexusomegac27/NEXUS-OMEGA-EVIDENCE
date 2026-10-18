# NEXUS OMEGA — R18 unabhängige wissenschaftliche Tiefenrecherche und Fundament R1

**Stand:** 18. Oktober 2026 · **Geltung:** `C1_DESCRIPTIVE_ONLY` · **Forschungsmodus:** `EXTERNAL_RESEARCH_ONLY`, keine produktive Implementierung.

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_INDEPENDENT_DEEP_RESEARCH_AND_INTEGRITY_FOUNDATION_20261018_R1
PARENT = R17_C1_FINAL_RESEARCH_CLOSURE_20261018_R0
SOURCE_INTAKE = NINE_OPERATOR_SUPPLIED_R18_FILES_SHA256_MANIFEST
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_FOUNDATION_ESTABLISHED
R18_R0 = IMMUTABLE_HISTORICAL_PARENT
R18_R1_47_CONDITIONS = DRAFT_PENDING_OPERATOR_RATIFICATION
R18_SHADOW_LOOP = HOLD_NO_START
R18_RUNTIME = FROZEN
R18_EMPIRICAL_VALIDATION = NOT_PERFORMED
R18_PRODUCTION_COMPONENT_SELECTION = NOT_ESTABLISHED
R18_SOURCE_BODY_K7 = PARTIAL_NOT_HTTP_BYTE_VERIFIED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
```

## 1. Gegenstand, Eigentümerschaft und Quellenscope

Die Forschungsfrage ist **nicht**, wie ein Kollektiv automatisch Wahrheit produziert, sondern: *Welche nachprüfbaren Eigenschaften ermöglichen die kontrollierte Zusammenarbeit von Generatoren, Prüfern und menschlichen Entscheidern bei fehlerhaften, korrelierten oder aktiv manipulierten Agentennachrichten, ohne unzulässige Autoritätsübertragung?*

Neun tatsächlich bereitgestellte Dateien wurden physisch gelesen, Größe und SHA-256 unabhängig bestimmt; sie stehen in `ORIGINAL_INTAKE_SHA256.json`. Quellenhierarchie:

- **Operatorvermittelte Dokumente**: `R18-P0~1.TXT` (metaphorischer CWEIP-Entwurf mit eingebetteter Kritik); `QWEN_R~1.TXT` und identisch thematisches PDF; GROK/QWEN-Handshake; Perplexity Erstkritik, konkreter Korrekturauftrag, überarbeiteter Perplexity-R1-Bericht und GROK-Korrektur-Handshake; R18 Physical-Control-Analogy. Ihre Textaussagen sind **Quellen über Behauptungen**; keine authentisierte Expertensignatur, kein NEXUS-Messergebnis, keine R18-Ratifizierung.
- **Externe Primärliteratur**: Lee et al., *Robust Multi-Agent LLMs under Byzantine Faults*, arXiv **2605.09076v1** und **v2**; Zheng et al., *Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance*, arXiv **2511.10400v2**. Autorenprojekte unter versionierten GitHub-Commits. Standards: SLSA **v1.2**, in-toto, Sigstore; wissenschaftliche Kalibrierungs-, BFT- und Risikomethodik.
- **Eigene Arbeit**: Recherche, exakter lokaler Byte-Intake, Versionsvergleich, arithmetische Kontrolltabelle, abstrakter Kontrollfluss und 42 synthetische Falsifikations-Tests; keine reale Replikation von SAC/CP-WBFT oder NEXUS-Experiment.

Einige QWEN-/Perplexity-Dateien enthalten zeitlich begrenzte, signierte Drittanbieter-Dateilinks. Diese werden **nicht erneut veröffentlicht** und nicht als belastbare Langzeit-Referenz betrachtet.

**Exaktheitsregel:** Physische SHA-256-Matches an den neun Anlagen belegen nur die Identität der eingegangenen Dateien. Für externe URLs wurde der Text aus arXiv-/Projektseiten geprüft, jedoch kein vollständiges K7-Audit mit HTTP-Status, Headern, abgerufenem Rohkörper und dessen unabhängiger SHA-256 geführt. Externer Quellenstatus bleibt `CONTENT_SCOPED_ONLY / K7_PARTIAL`.

## 2. Finaler Primärquellenvergleich: v1 vs. v2, Metrikidentität

### 2.1 Versionsverwechslung aufgelöst — Nicht gleiches Experiment

| Kriterium | arXiv:2605.09076v1 (9. Mai 2026) | arXiv:2605.09076v2 (29. Juni 2026) |
|---|---|---|
| Closed-source-MATH Hauptvergleich | **30** Level-4-Aufgaben | **100** Level-4-Aufgaben |
| Closed-source-Commonsense Hauptvergleich | **30** | **30** |
| MATH-Kompositions- und Skalierungsablation | 30 | 30 |
| Hauptvergleich Tabelle 1 | v1-Tabellen, eingeschränkter n-Aufgabensatz | v2-Tabelle 1 mit anderen Ausgangs-/Endgenauigkeiten |
| Modellmix | MATH: starke `gpt-4o-mini`, schwache `gpt-3.5-turbo`; Commonsense: starke `gpt-5`, schwache `gpt-4o` | In den jeweils benannten Hauptkonfigurationen analog; weitere open-weight-Experimente zusätzlich |
| Typisches Netzwerk | n=7, 4 starke ehrliche, 2 schwache ehrlich-fehlerhafte, 1 absichtlich adversariell; F=3, robustheitsgebundene Graphen | Analog für Hauptvergleich; zusätzliche Topologien-/n=9-Analysen |
| Autoren-/Versionseintrag | v1 enthält zusätzlich Hyeonho Oh | v2 listet vier Autoren |

**Neu verifizierter Kernkonflikt:** Die Perplexity-R1-Rekonstruktion transkribiert den v1-MATH-Hauptvergleich mit MATH 30 und z. B. `CP-WBFT/MERG IAA 55,2 -> FAA 44,8 => BFTI −10,4 pp`; im v2-Hauptvergleich steht für dieselbe Methoden-/Topologienbezeichnung `52,3 -> 43,6 => −8,7 pp` bei **100** MATH-Aufgaben. Beides sind historisch verschiedene Ergebnisobjekte, keine austauschbaren Zahlen. Die arXiv-Abstraktseite zeigt v1/v2; eine behauptete dritte arXiv-Version ist im gegenwärtig abgerufenen Versionsverzeichnis **nicht bestätigt** (`v3 = NOT_VERIFIED`, kein Nichtexistenzbeweis).

**Konfigurationspflichtfelder für jede Zahl:** `paper_id`, `version`, `table_id`, `dataset`, `task_count`, `topology`, `n`, `strong_n`, `weak_n`, `intentional_attacker_n`, `F_local`, `round`, `metric`, `group_scope`, `attack_model`, `model_versions`, `raw_traces_available`, `replication_status`.

### 2.2 Metrikidentität

Bei `D` Tasks, `V` Agenten und Round t ist `Acc(V,t)` der Mittelwert korrekter Agenten-Antworten über **D×V** Beobachtungen. `IAA=Acc(V,0)` und `FAA=Acc(V,T)`, `BFTI=FAA−IAA` in **Prozentpunkten**. Das ist weder ein relativer Prozentsatz noch Strong-Group-Preservation. `RA` bezeichnet den Anteil korrekter Mehrheitsantworten aller n Agenten; `H-Majority` bezieht sich auf die ehrlichen Agenten allein. `S_IAA→S_FAA` und `W_IAA→W_FAA` sind gruppenspezifische Genauigkeiten. Bei sechs ehrlichen Agenten müssen Stimmengleichstände in einem Replay ausdrücklich geregelt werden.

Die folgende *unabhängig arithmetisch kontrollierte Transkription* aus arXiv-v2-Tabelle 1 **beansprucht keine Laufwiederholung**:

| Datensatz | Methode | Graph | IAA % | FAA % | BFTI pp | H-Majority % | Strong IAA→FAA % |
|---|---|---|---:|---:|---:|---:|---|
| MATH100 | CP-WBFT | MERG | 52,3 | 43,6 | −8,7 | 38,0 | 79→48 |
| MATH100 | CP-WBFT | Complete | 52,7 | 42,3 | −10,4 | 49,0 | 81→50 |
| MATH100 | CP-WBFT | Erdős–Rényi | 52,6 | 35,1 | −17,5 | 42,0 | 80→41 |
| MATH100 | SAC | MERG | 50,1 | 53,1 | +3,0 | 79,0 | 77→80 |
| MATH100 | SAC | Complete | 53,7 | 54,1 | +0,4 | 78,0 | 81→78 |
| MATH100 | SAC | Erdős–Rényi | 53,3 | 55,0 | +1,7 | 78,0 | 81→77 |
| Commonsense30 | CP-WBFT | MERG | 69,5 | 37,1 | −32,4 | 26,7 | 83→39 |
| Commonsense30 | CP-WBFT | Complete | 69,0 | 14,3 | −54,7 | 16,7 | 85→17 |
| Commonsense30 | CP-WBFT | Erdős–Rényi | 69,0 | 20,5 | −48,5 | 23,3 | 83→23 |
| Commonsense30 | SAC | MERG | 68,6 | 66,7 | −1,9 | 80,0 | 83→78 |
| Commonsense30 | SAC | Complete | 69,5 | 69,5 | +0,0 | 83,3 | 83→82 |
| Commonsense30 | SAC | Erdős–Rényi | 69,0 | 66,2 | −2,8 | 76,7 | 84→78 |

**Falsifier gegen Claim-Absolutismus:** SAC/MATH100/Complete verschlechtert die starke Gruppe 81→78 %, SAC/Commonsense30/MERG 83→78 %. Die Kurzform „bewahrt starke Agenten“ ist ohne Toleranzkriterium zu pauschal. Selbst SAC erzeugt im gezeigten Commonsense30-Datensatz negative BFTI-Zeilen. R18 darf aus der Überlegenheit zur angegriffenen Baseline kein „nie schlechter“ ableiten.

### 2.3 Primärquellen-kontextuelle Schwächen

- Der SAC-Score `φ_i(x, r_j)` wird im Original **vom empfangenden LLM selbst** per Verification-Prompt erzeugt. Empfängerkontrolle gegen Sender-Selbstbewertung ist **nicht** das Vorhandensein eines unabhängigen deterministischen Prüfers, einer fremden Prozessidentität oder fehlerfreien Referenzlabels.
- Die `(F+1)`-Robustheitsbedingung wird als graphentheoretische Garantie unter **statischer, zeitinvarianter**, F-lokal begrenzter Umgebung hergeleitet; sie validiert nicht automatisch die Semantik des LLM-Scores, beherrscht nicht beliebige dynamische Graphen und zertifiziert keine NEXUS-Topologie.
- CP-WBFT nutzt eigenständige Confidence Probes, seine konkrete Auswertung und das Angreifermodell müssen je Studie getrennt werden. Der SAC-Angriff mit **falsifizierter Selbstkonfidenz 1,0** zeigt eine spezifische Angriffsfläche – weder die allgemeine Unsicherheit aller Probevarianten noch eine universelle BFT-Faustrate.
- v1-Tabellen enthalten potenzielle interne Konflikte, z. B. v1 SAC/Complete-H-Majority des MATH-Hauptlaufs vs. bestimmte Ablationszellen und v1 Commonsense/Complete Hauptgruppe vs. Rundenangabe. Diese verbleiben als `SOURCE_CONFLICT` bis Autoren-Rohdaten/Laufzuordnung vorliegt.
- v1-Risikokennzahlen, v2-Ergebnisse, AIME/HMMT-Angaben und die externe Zahl **85,7 %** CP-WBFT stammen aus **unterschiedlichen Experimenten**; sie dürfen nicht zu einer einzigen Erfolgstabelle zusammengesetzt werden.

## 3. Unabhängige Gegenforschung zur Auswahl von Open-Source-Komponenten

### 3.1 BFT / kollektiv-kooperative Auswertung

**SAC** (offizielles Autorenrepo `daniel-eai/Robust-Multi-Agent-LLMs-under-Byzantine-Faults`, `2ef7061590d0968ea4bd19f82b8d7ddde8f2bb89`) implementiert den Forschungsalgorithmus; Basis stammt aus `Z1ivan/Byzantine-Fault-Tolerance-in-LLM-MAS`, Commit `7f7464dc0415f415182f25e99b71738730a87408` (MIT laut GitHub-Metadaten). **Im überprüften Repositoryroot des SAC-Autorenprojekts wurde keine LICENSE-Datei gefunden, und GitHub meldet keine Lizenz.** Der Quellcode ist öffentlich sichtbar, aber direkte Integration/Kopie ist wegen nicht nachgewiesener Lizenz **HOLD_LICENSE_SOURCE_GAP**. Auch Abhängigkeiten und Unterlizenzen sind ungeprüft. Die Forschungsbeschreibung darf mit Link zitiert werden.

**CP-WBFT**: Paper `arXiv:2511.10400v2`; offizielles Baseline-Repo wie oben. Die publizierte 85,7-%-Angabe ist ein **spezifisches experimentelles** Ergebnis, keine pauschale garantierte Fehlertoleranz eines realen NEXUS-Kollektivs. Insbesondere ist „Mehrheit der Agenten stimmt zu“ keine hinreichende Regel für epistemische Richtigkeit.

**Einzelagent und unabhängige Mehrheitsvoten** gehören als Baselines zu jedem zukünftigen methodischen Vergleich; sonst ist ein Mehr-Agenten-Nutzen nicht isolierbar. SAC und CP-WBFT sind C1-Untersuchungskandidaten, nicht technische Projektentscheidungen.

### 3.2 Ledger / Tamper Evidence: zwei unterschiedliche Vertrauensmodelle

`Aperintelligence/nexuscone` (SHA `45b51e7a987d97a23d279f6f2c57e12d231b6201`, Apache-2.0 metadata): lokale SQLite-SHA256-Kette, optionale Ed25519-Einträge und optionale RFC3161-/OpenTimestamps-Anker. Ein gültiger Hash beweist keine vollständige Erfassung der Ereignisse und keinen unabhängigen Beobachter; Ankerbelege und Schlüsselrollen separat prüfen.

`OgenticAI/ogentic-audit` (SHA `bd994be094f4c468054873027712091600f32fc6`, Apache-2.0 metadata): HMAC-SHA256-Kette, Crash-Recovery, dokumentierte Golden-Vektoren. Die eigene Projektdokumentation stellt klar: Wer HMAC-Schlüssel und Log besitzt, kann das gesamte Log **neu verketten**; ein unabhängig verwahrter, authentifizierter Checkpoint ist erforderlich, um historische Neuschreibung zu erkennen. Ein veröffentlichter Court-Defensibility-Brief **ist keine unabhängige Gerichtszertifizierung oder formale Sicherheitsprüfung**. Er sagt nichts über die tatsächliche Zulässigkeit oder Beweiskraft im konkreten Rechtsverfahren.

Für NEXUS bleibt die Minimalarchitektur: lokal write-once/append-only Eventlog (keine Verfälschung von source-of-record), unabhängiger Checkpoint/Receipt-Reader, zwei getrennte Authentisierungsdomänen und testbare Negativfixtures `edit`, `truncate`, `rechain`, `key-compromise`, `checkpoint-compromise`, `silent-omission`. **Keine automatisierte Retention-, Lösch- oder Schlüsselrotation ohne eigene Operatorfreigabe.**

### 3.3 Kalibrierung / Judge-Qualität

`judgekit` ist identifizierbar als `mohammadi-hadi/judgekit`, Git SHA `ae2603488ba257f29873162bc2ff58ee8b18bd3f`, Lizenz MIT. Es testet Position-, Verbosity-, Selbstpräferenz-, Stabilitäts- und Kalibrierungs-Bias gegen gelabelte Testfälle; der Betreiber nennt konkrete synthetische und lokale Ollama-Beispiele. Diese **Repository-Demowerte sind keine NEXUS-Validierung**. Kalibrierung setzt unabhängig verifizierbare Referenzlabels und repräsentative, gesperrte Daten voraus. Für `calikit` wurde in dieser Runde keine eindeutige, versioniert auflösbare Projektidentität aus dem bloßen Namen festgestellt; deshalb **NOT_SELECTED / SOURCE_IDENTITY_GAP**. Weder `judgekit` noch ein Brier-/ECE-Paket ersetzt einen deterministischen sachlichen Validator.

Brier/Expected Calibration Error messen Wahrscheinlichkeitsgüte nur bezüglich definierter Outcomes und verlässlicher Zielereignisse. Brier ist ein proper scoring rule, ECE hängt u. a. von Bin-Auswahl und Stichprobengröße ab. „Calibrated Truth Index (CTI)“ aus R18-P0 ist kein etabliertes Maß; der Quotient `Wisdom=(Calibration×Resilience)/(Drift×Susceptibility)` ist ohne Variablen-, Nullstellen-, Einheit- und Schätzdefintion **nicht operationalisierbar**. Als Metapher archivierbar, **nicht als Messlatte**. Mythologische Salomo-Motive gehören in eine explizit separierte Erklärungs-/Ethikschicht, nicht als quantitative Wissenschaftsevidenz.

### 3.4 Software-Supply-Chain

SLSA **v1.2** besitzt Build- und Source-Track. SLSA Build L3 beschreibt einen gehärteten Build-Prozess mit Provenienz/Isolation; es verlangt **nicht automatisch** vollständige Bit-Reproduzierbarkeit. SLSA-eigene FAQ unterscheidet reproduzierbar von unabhängig verifiziert-reproduzierbar und benennt weitere nicht gedeckte Bedrohungen. in-toto strukturiert attestierte Aussagen; Sigstore/Cosign signiert und bindet Identitäten, Rekor führt Transparenz-Logs. **Signatur/Attestation ≠ sachliche Korrektheit des erzeugten Inhalts** und beweist keine LLM-Promptkette vor der erfassten Source/Build-Grenze. Vor-Commit-Prompt-/Modell-Provenienz bleibt `OPEN_RESEARCH` mit Privacy/Secret-Exfiltrationsrisiko.

### 3.5 Optionaler Konfigurationssuchalgorithmus

PL-NSGA-II und vergleichbare Pareto-/lexikographische Verfahren sind höchstens **Suchverfahren für Kandidatenräume**. Bei kleinem, bereits erfasstem Satz entscheidet eine deterministische Pareto-Filterung nach harten Zulässigkeits-Gates ohne zusätzlichen genetischen Algorithmus. Kein Score darf `CORRECTNESS=FAIL` oder `INTEGRITY=FAIL` mit geringerer Latenz verrechnen.

## 4. R18-Architektur: harte Trennung von vier Prüflevels

| Level | Leitfrage | Mindestartefakt | Evidenzstatus 2026-10-18 |
|---|---|---|---|
| L1 Quellen | Existiert eine benannte, versionierte Quelle für einen scoped Claim? | URL, Version, Abschnitt/Tabelle, Inhaltsreadback, K7-Rohkörper-Receipt sobald verfügbar | `PARTIAL`, für SAC/CP-WBFT Inhaltsprüfung, K7 nicht geschlossen |
| L2 Transferabilität | Tragen F-local, Ground Truth, Rollen, Graph, Datenverteilung und Angreiferfähigkeit im NEXUS-Ziel? | Exaktes Bedrohungsmodell + Gegenhypothesen | `DESIGN_ONLY` |
| L3 Implementierung | Erfüllt eine eingefrorene, getrennt autorisierte Implementierung die Spezifikation? | Source/Build/Sandbox Pins, unabhängige Tests, Negativmutation | `NOT_PERFORMED` für reale BFT/Integrator |
| L4 Empirie | Wie verhält sich das integrierte System unter gepaartem adversarialem Versuch? | gesperrte Korpora, Rohtraces, unabhängige Metrik-Checks, Konfidenzintervalle | `NOT_PERFORMED` |

### 4.1 Zulässigkeitskontrollfluss (nur Forschungsvertrag)

```text
SOURCE_URI + VERSION + CONFIGURATION
  -> if missing/conflicted: HOLD_SOURCE
TASK_OBJECTIVE + ORACLE + PROOF_LEVEL
  -> if incorrect: REJECT_CORRECTNESS
  -> if unknown: HOLD_CORRECTNESS
EVALUATOR_IDENTITY + BUILD_PIN + INPUT_BOUNDARY + AUDIT_RECEIPT
  -> if integrity fails: REJECT_INTEGRITY
  -> if missing: HOLD_INTEGRITY
THREAT_MODEL + TOPOLOGY_CERTIFICATE + F_LOCAL_BUDGET
  -> if unsupported: HOLD_SCOPE
RESOURCES_VECTOR (latency, bytes, error_budget, compute, energy)
  -> PARETO_FRONTIER_DESCRIPTIVE_ONLY
OPERATOR_AUTHORITY (named, authenticated, case-bound)
  -> HUMAN_CHOICE / HOLD / NOGO

NO BRANCH IMPLIES RUNTIME OR SCIENTIFIC CLAIM PROMOTION.
```

**VETO > OPTIMIERUNG:** Korrektheit und Integrität sind kategoriale Bedingungen; niedrigere Kosten kompensieren sie nicht. `NO_CANDIDATE -> EXIT_NOGO` muss ein eigener nicht automatisch neustartbarer Zustandsübergang sein. HOLD darf nicht durch Timeout automatisch verschwinden.

### 4.2 Evaluator-Unabhängigkeit (L1–L5, nicht bloß Rollenetiketten)

L1 Code: unabhängiger, unveränderlicher Prüforakel-Source-Pin, Dependency-/Build-Hash und Rechteprüfung, keine Schreibrechte für den Generator. L2 Prozess: eigenständige Ausführungsidentität und Geheimnisse, getrennte Laufzeitgrenzen. L3 Input: eingefrorene Aufgaben-/Bewertungsspezifikation; generierte Inhalte sind **Daten**, niemals neue Evaluator-Instruktionen. L4 Replay: identische Input-/Umgebungsversion muss denselben **strukturierten** Entscheid ergeben (floating-point-/plattformabhängige Textvarianten gesondert). L5 Kanal: Prüfrückgaben und Negativentscheidungen unveränderbar und unabhängig beobachtet. **Ein deterministischer LLM-Prompt bei Temperatur 0 genügt keiner dieser fünf Anforderungen allein.**

### 4.3 R18 47-Bedingungen und K7–K18

Ein R18-47-Bedingungen-Draft wird in den Artefakten wiederholt benannt, jedoch **sein eigenständiger vollständiger Katalog ist nicht unter den neun aktuellen Uploads**. Die historische Vollständigkeit `C01–C47` wird deshalb hier nicht neu eigenständig zertifiziert. Seine Ratifizierung bleibt `PENDING_OPERATOR_RATIFICATION`; kein GROK-/QWEN-/MISTRAL-Status kann die Operatorentscheidung ersetzen. K7 (Primärquelle), K8 (Unabhängigkeit), K9 (Fail-Closed), K10 (Rollen), K11 (Ledger), K12 (Niedrigqualitätsquellen) sowie K13–K18 (Authority-Korrektur) werden **als geprüfte Forschungsanforderungen**, nicht als bereits in Kraft gesetztes Gesetz, behandelt.

Die R18 Physical-Control-Analogie bleibt eine anschauliche, nicht gemessene Darstellung von isolierten, direkten Signalwegen. Aus CRT- oder Strahlungsdemonstrationen wird keine konkrete NEXUS-Verzögerungs-, Energie- oder Strahlenhärtezahl übertragen.

## 5. Eigenständig durchgeführte, begrenzte Falsifikationsprobe

Die Datei `test_r18_frozen_oracle.py` wurde **vor** der separaten Python-Referenzfunktion `r18_research_gate.py` verfasst. Im isolierten Standard-Python-Lauf wurden **42/42** synthetische Vertragsfälle erfolgreich geprüft: Versions-/Nennerbindung, Status-Trennung, Korrektheit/Integrität als harte Vetos, Ressourcen-Nan/negative Werte, Pareto-Dominanz, BFTI-Arithmetik, K7-Inhalts-/Bytegrenzen, externer Checkpoint und Ausschluss einer automatischen Runtime-Autorisierung. Eine bewusst geschwächte Kopie ohne Integritäts-Veto versagt erwartungsgemäß an **3 von 42** Fällen, darunter der Anreiz zur Ressourcenkompensation. Alle Protokolle und Originalskripte liegen im Artefaktpaket.

**Unbedingt beachten:** Diese Tests zeigen nur, dass die vorgeschlagene vereinfachte Kontrollflussregel die ausgewählten synthetischen Beispiele erfüllt. Sie beweisen **nicht**, dass externe Quellen lückenlos erfasst, ein echtes BFT-Netzwerk sicher, ein Evaluator prozessisoliert, oder das NEXUS-Kollektiv verlässlich ist. Kein Entwickler-fremder unabhängiger wissenschaftlicher Validator oder eingefrorenes fremdes Abnahmeorakel war beteiligt. Tester und Kandidat wurden in derselben AXIOM-Forschungssitzung erstellt.

## 6. R18 Pilotexperiment — präregistrierbar, aber nicht ausgeführt

**Haupt-Frage:** Reduziert SAC bei identischer Ausgangsqualität und festem Angriff die Verschlechterung *starker ehrlicher Agenten* gegenüber (a) Einzelagenten, (b) unabhängiger Mehrheitswahl, (c) CP-WBFT mit manipuliertem Sendervertrauen und (d) CP-WBFT mit separat kalibrierter, manipulationsresistenter Probe, falls ein solcher Pfad tatsächlich vorliegt?

**Versuchsplanung:**

1. Zunächst ein reines **Topologie- und Schema-Prototyping ohne LLMs** (synthetische, beschriftete Nachrichten; Generator ≠ Judge getrennte Rollen) zur Prüfung von F-local-, Adjazenz- und Manifestannahmen.
2. Dokumentiert eingefrorener offline Korpus mit objektivem Ground Truth; **nicht** aus aktuellen NEXUS-Kollektiväußerungen abgeleitet. Verwandte Aufgaben nach Familien gruppieren; Dev/Kalibrierung/gesperrten Test getrennt halten. Unabhängige Experten lösen Konflikte zu Labels.
3. Vorab festgelegte adversarielle Fähigkeitsmatrix: falsche Senderkonfidenz, kolludierende Fehler, prompt-injizierte empfangene Nachrichten, gemeinsame Modell-Fehlannahmen, Replay/Duplikate, Timing, Netzwerkpartition und Verletzung des lokalen Fehlerbudgets. Angriffe außerhalb der Theorie werden als separate Stressprüfung gekennzeichnet, nicht als angebliche Widerlegung der Annahmen.
4. Primäre Metrik: gepaarte Differenz in Strong-Group-Genauigkeit auf **Aufgabenebene**; sekundär globale IAA/FAA/BFTI, RA, H-Majority, Fehlakzeptanz, HOLD/REJECT/Unknown-Raten, Latenz, Bytes, CPU/GPU/Energie. Report des **Nenners der tatsächlich geprüften Aufgaben** und der fehlenden Outputs.
5. Pre-registered Nichtunterlegenheitsmarge, Analysemethode, Konfidenzintervalle, Effektgröße und Sample-Power erst aus Pilot/Referenzwerte herleiten; **keine erfundenen NEXUS-Zielwerte**. Tasks sind statistische Einheiten; Agent-Runden derselben Aufgabe sind keine unabhängigen Stichproben.
6. Gleiches Modell-/Prompt-/Seed-/Budget-Profil, soweit anwendbar; Topologie von `r-robust` mathematisch bzw. durch unabhängigen Prüfer zertifiziert; Angreiferadaptivität und Transportautorisierung dokumentiert. Proof-Level `FORMAL | EXHAUSTIVE | BOUNDED_STATISTICAL | UNIT_SYNTHETIC | UNKNOWN` pro Claim.
7. Harte Stop-Regel bei Geheimnis-/Privacy-Breach, unbelegter Verifikation, falscher Rollenzuordnung, `HOLD`-Verdeckung, ungebundener Quellenidentität oder Runtime-Mutation.

**Abbruch-/Exitklassifikation:** `GAP` (Quelle/Identity), `REJECT` (bekannter Veto-Fehler), `HOLD` (unbekannte Grenze), `NOGO` (kein zulässiger Kandidat), `RESEARCH_ELIGIBLE` (nur synthetischer Feasibility-Status), `AUTHORIZED_EXPERIMENT` (nur nach ausdrücklichem Operatorauftrag, derzeit nein), niemals `C2_AUTHORITATIVE`.

## 7. Lieferpakete und R18-Implementierungsreife

| Arbeitspaket | Unabhängig prüfbarer Output | Startrecht | Status |
|---|---|---|---|
| WP0 Quellfixity | 9/9 lokale SHA, v1/v2-Konfliktmatrix, Git-SHA-Pins, K7-Gaps | Forschungsread | Abgeschlossen / K7 offen |
| WP1 Spezifikationsgates | Exakte Rollen-/Bedrohungs-/Gateschemas, 42 synthetische Tests, 3 Mutationsfehler | Forschungsread | Lokal synthetisch durchgeführt |
| WP2 unabhängiges Prüfprogramm | Fremd-authentisierte Evaluator-Umgebung, Generator-Schreibverbot, unabhängiges Oracle/Replay | gesonderter Auftrag | `NOT_EXECUTED` |
| WP3 Offline-Sandbox | Keine Netzwerk-/Runtime-Änderung; nur kontrollierte Nachrichten- und Topologie-Simulation mit vollständigem Receipt | gesonderter Auftrag | `NOT_EXECUTED` |
| WP4 adversarielle gepaarte Studie | Echte SAC/CP-WBFT-Replikation, Statistik, Ledger-/Hardware-Nachweise | gesonderter Auftrag | `NOT_EXECUTED` |
| WP5 R18-Ratifizierung | Human-authentifizierter C01–C47-Entscheid, K7–K18, Rechte-/Retention-Klärung | Operator | `PENDING` |

**Empfehlung:** R18 lässt sich als wissenschaftlich substanziell begründetes **Forschungsfundament R1** binden. Aktive Auswahl von SAC/CP-WBFT, ein technischer Shadow-Loop, Verschieben historischer R18-Objekte und tatsächliche Node-Aktivierung bleiben **HOLD**. R18 darf nicht voreilig als empirisch oder produktiv geschlossen gelten.

## 8. Nachprüfbare Primärquellen und Quellengrenzen

1. [SAC, arXiv 2605.09076v1](https://arxiv.org/html/2605.09076v1) — Version/Konfiguration, alte Tabelle 1, 30 MATH; Inhalte gelesen, HTTP-Rohkörper-SHA offen.
2. [SAC, arXiv 2605.09076v2](https://arxiv.org/html/2605.09076v2) — Hauptvergleich mit 100 MATH, 30 Commonsense; Algorithmus 1, Section 5.1, Tabellen 1–6.
3. [CP-WBFT, arXiv 2511.10400v2](https://arxiv.org/abs/2511.10400) — Originalanspruch 85,7 % unter eigener Versuchsanordnung.
4. [SAC offizielles Autorenrepo](https://github.com/daniel-eai/Robust-Multi-Agent-LLMs-under-Byzantine-Faults/tree/2ef7061590d0968ea4bd19f82b8d7ddde8f2bb89) — Quellcode und Tests, Lizenzfrage offen.
5. [CP-WBFT offizielles Repo](https://github.com/Z1ivan/Byzantine-Fault-Tolerance-in-LLM-MAS/tree/7f7464dc0415f415182f25e99b71738730a87408) — Baseline, MIT deklariert.
6. [nexuscone](https://github.com/Aperintelligence/nexuscone/tree/45b51e7a987d97a23d279f6f2c57e12d231b6201) — Bitcoin-/TSA-Anker nur bei aktiver Nutzung, Projektquellen.
7. [ogentic-audit](https://github.com/OgenticAI/ogentic-audit/tree/bd994be094f4c468054873027712091600f32fc6) — HMAC/Ketten-Checkpoint, Exploit-/Recovery-Beispiele, Dokumentscope.
8. [judgekit](https://github.com/mohammadi-hadi/judgekit/tree/ae2603488ba257f29873162bc2ff58ee8b18bd3f) — Bias-/Kalibrierungs-Audit, nicht genereller Wahrheitsprüfer.
9. [SLSA v1.2](https://slsa.dev/spec/v1.2/), [SLSA FAQ](https://slsa.dev/spec/v1.2/faq), [Build-Provenance](https://slsa.dev/spec/v1.2/build-provenance), [in-toto](https://in-toto.io), [Sigstore](https://sigstore.dev/) — Protokoll-/Build-Standards.
10. Bröcker (2009), [Proper scoring rules](https://doi.org/10.1002/qj.456) — probabilistische Kalibrierung als eigenständiges Messkonzept.
11. [NIST AI RMF GenAI Profile](https://doi.org/10.6028/NIST.AI.600-1) sowie [NIST AI RMF TEVV](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) — unabhängigere Bewertung und Dokumentation.
12. R18 Physical-Control-Metaphern: Videos [`8a3GfozsU0s`](https://www.youtube.com/watch?v=8a3GfozsU0s) und [`20ZhzyT2HR0`](https://www.youtube.com/watch?v=20ZhzyT2HR0) — ausdrücklich **S0-Analogie**, keinerlei NEXUS-Effizienz-Messnachweis.

---

## 9. Kanonische Adjudikation

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_INDEPENDENT_DEEP_RESEARCH_AND_INTEGRITY_FOUNDATION_20261018_R1
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_FOUNDATION_ESTABLISHED
SOURCE_FILE_INTAKE = 9_ORIGINALS_SHA256_READ
SAC_ARXIV_VERSION_V1_V2 = CONTENT_CHECKED_AND_SEPARATED
SAC_ARXIV_V3 = NOT_VERIFIED
SAC_LICENSE = SOURCE_GAP_NO_LICENSE_AT_CHECKED_ROOT
SAC = PRIORITY_EVALUATION_CANDIDATE
SAC_PRODUCTION_SELECTION = NOT_ESTABLISHED
CP_WBFT = PROBE_AND_THREAT_MODEL_DEPENDENT
MULTI_OBJECTIVE = VETO_THEN_PARETO_DESIGN_ONLY
LOCAL_SYNTHETIC_ORACLE = 42_OF_42_PASS
LOCAL_INTENTIONAL_INTEGRITY_BYPASS_MUTANT = 39_OF_42_PASS_EXPECTED_FAIL
INDEPENDENT_AGENT_ACCEPTANCE = NOT_ESTABLISHED
R18_EMPIRICAL_VALIDATION = NOT_PERFORMED
R18_SHADOW_LOOP = HOLD_NO_START
R18_47_CONDITIONS = DRAFT_PENDING_OPERATOR_RATIFICATION
R18_R0_AND_R17_PRIORS = PRESERVED
RUNTIME_CHANGE = NO
HOSTINGER_WRITE = NO
CLAIM_PROMOTION = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

`SOURCE ≠ TRUTH · GENERATOR ≠ JUDGE · RECEIVER_LLM_JUDGE ≠ INDEPENDENT_DETERMINISTIC_ORACLE · CONSENSUS ≠ CORRECTNESS · EVIDENCE > AGREEMENT · HUMAN AUTHORITY PRESERVED`
