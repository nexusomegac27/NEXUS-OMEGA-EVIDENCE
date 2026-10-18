# NEXUS OMEGA · R18-R3 Gate-0 — Aktuelle Wissenschaft und Beweisketten-Schließung

**OBJECT** `NEXUS_OMEGA_AXIOM_R18_R3_GATE0_LIVE_SCIENCE_EVIDENCE_CLOSURE_20261018_R0`  
**Datum** 2026-10-18 (Europe/Berlin) · **STATE** `PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_AND_ISOLATED_GATE0_PROBE`  
**CLAIM_CEILING** `C1_DESCRIPTIVE_ONLY` · **AUTHORITY** Operator · **RUNTIME** frozen · **SHADOW_LOOP** `HOLD_NO_START`  
**Vorgänger** R17 CLOSED_C1; R18-R1/R2 research; R1–R18-R2 integrated framework test; neue R18-R3 DOC/MD MISTRAL-Return.

## 0. Entscheidung

DEEPSEEKs Vorschlag ist im Kern methodisch tragfähig: erst Quelle und kontrollierte Prüfrechte, dann isoliertes Verhalten, anschließend gesonderte Operatorentscheidung. Die konkrete Reihenfolge muss jedoch **evidenztypabhängig** sein: K7-Rohkörper-Fixity blockiert quantitative SAC/CP-WBFT-Benchmark-Claims und code-nahe Quellenübernahmen; sie blockiert **nicht** sichere, parallele rein lesende Falsifier-Entwicklung, Lizenzanalyse oder Offline-Modellierung. Eine tatsächliche integrierte Runtime-Prüfung startet nicht ohne getrennte Autorisierung. Weder ein bestandener 57/57-Vertrag noch ein durch eine KI behauptetes K7-PASS hebt das HOLD auf.

Höchster neuer Forschungshebel: **R18 muss Decision, Control, Execution und Effect strikt trennen**; zusätzlich müssen prüfbare Rollenidentitäten, blindes Precommit und unabhängige, zeitlich vorgelagerte Witnesses von der fachlichen Urteilskorrektheit getrennt werden. Synthetische Belege dürfen nie als Fremdauthentisierung oder echte Systemausführung erscheinen.

## 1. Verifizierte Eltern- und neue Quellen

### 1.1 Lokale Artefakte (selbst gelesen/gehasht, kein externer wissenschaftlicher Review)

| Artefakt | Bytes | SHA-256 | Bedeutung |
|---|---:|---|---|
| R1–R18-R2 integrierter ZIP-Stack | 155027 | `95487e782362dd697333f2d9e652d2c327361069257b867232af5a381616087f` | Früheres C1-Vertragsexperiment; die 57/57-Bilanz ist eine isolierte Aussage |
| R18-R3 Design-Freeze und PDF-Body-Claim, hochgeladen als `NEXUS_~1(1).DOC` (OOXML) | 15457 | `c0c8663080d8a7b17c4584cb3c183345345a9fb9cd8de4a1e722981a27b14aa1` | Enthält berichtete v1/v2/v3 und CP-WBFT-PDF-Digests; PDF-Bodies NICHT enthalten |
| R18-R3 MISTRAL-Auftrag `NEXUS_~3(6).MD` | 8243 | `84a03a98f6c9beea474445fdc291acd7b81d6e8d28f6b8e42dd86a29a170541f` | Nicht-autorisierter Runtime-Null-Scope, Arbeitsanweisungen |
| R18-R3 MISTRAL Abschluss `R18-R3~1.MD` | 7390 | `b115d78a8612093af4f1a38c7371227c188d003095f1b6adca5e9e842262ef1a` | `HOLD_DESIGN_PENDING_SOURCE_BYTES` war zum damaligen Review gültig; 9 Fixtures nur REGISTERED |

**Widerspruch historisch richtig auflösen:** R18-R3-Elterndokument behauptet HTTP `200` plus die Rohbody-Hashes. MISTRAL hatte den Design-Freeze **damals nicht als gebundenes Original** und sah HTTP-K7-Originalbodies nicht. Hier wurde der DOC-Container physisch gehasht und die 4 erwarteten PDF-Fingerprints aus der OOXML-Tabelle ausgelesen. Es wurden **keine** 4 PDF-Bodies von dieser Sitzung geprüft, auch nicht durch eine verborgene Tool-API. Historisches Produzenten-Claim: `K7_REPORTED_PASS`; AXIOM-eigener K7-Status: `HOLD_INDEPENDENT_ORIGINAL_BODY_REHASH`.

### 1.2 Berichtete K7-Primärkörper, nur Lookup-Sollwerte

| Primär-PDF | Erwartete Bytes | Berichtet SHA-256 |
|---|---:|---|
| SAC arXiv:2605.09076v1 | 1,243,056 | `641fd98e0c862d10ffb87fa62fbdd0f92650a6f241b1989acafe84b2a82fbfa3` |
| SAC arXiv:2605.09076v2 | 1,260,331 | `40e509f2dd5e1c1123ac5addfaf2cda7f5d3bffed69e40ad83ed91c0f235fe8a` |
| SAC arXiv:2605.09076v3 | 1,150,373 | `de35d6c9c25b20c3e9e6743cd37a542ba21fcb7666356b6129054d69729fbe81` |
| CP-WBFT arXiv:2511.10400v2 | 912,776 | `a10aeeb16584317bb6a5217bbd2bfcd7c03c084519f42f8621037ee8b294d52f` |

Der direkte Abruf `https://arxiv.org/pdf/2605.09076v2` aus der Arbeitsumgebung scheiterte am verfügbaren Netzwerk/DNS (kein Bytes-Receipt). Ein Web-Textpreview der PDF ist **kein PDF-Body-Hash**. Die unabhängige Behauptung wird deshalb nicht geschlossen. Das auf GitHub vorhandene README/SAC-Arxiv verweist auf einen Forschungsstand, aber nicht auf die physische Identität der oben behaupteten vier Bodies. Die ursprüngliche R18-K7-Serie betrifft **diese vier**; DEEPSEEKs zusätzliches R17-Anthropic-/arXiv-2610-Paar ist ein **eigener R17-Quellenstrang**, nicht stillschweigend K7.

## 2. DEEPSEEKs konkrete Anker — Quellenprüfung

### 2.1 `Who Verifies the Benchmark?` (arXiv:2608.07762, 2026)

**BIBLIOGRAFISCH IDENTIFIZIERT (Preprint; unmittelbarer arXiv-Body-Abruf hier nicht gelungen):** Pardasani/Singh untersuchen 7 Judge-Modelle und 58 Aufgaben, einschließlich möglicher Bewertungsänderungen nach Offenlegung der Modellidentität, und schlagen ein zweiphasiges Hash-Commit/Reveal mit Salt auf einer Ethereum-kompatiblen Infrastruktur vor. Dies bindet ein Urteil **vor** späterer Offenlegung, sofern eine externe Zeit-/Ordering-Basis vorhanden ist. **NICHT bewiesen:** echte fachliche Richtigkeit des Scores, nicht vom Generator kontrollierte Schlüssel, kein Prompt-Leak, korrekte private Judge-Ausführung, eine etablierte Pflicht zur Blockchain. Für NEXUS genügt zunächst die verifizierbare lokale Protokollspezifikation mit extern gegengezeichnetem Checkpoint; eine Blockchain ist ein optionales Trust-Modell und kein Ausgangspunkt.

Quelle: https://arxiv.org/abs/2608.07762

### 2.2 AIREP (arXiv:2608.21363, Vorschlag; Referenzrepo noch experimentell)

**PUBLIKATIONS- UND REPO-INHALT IDENTIFIZIERT (nicht ratifizierter Vorschlag; Original-arXiv-Body hier nicht physisch gehasht):** `Decision` ist etwas anderes als `Control` (Auslieferung/Empfang), `Execution` (durchgeführte Aktion) und `Effect` (beobachtete Änderung). v0.1 ist das im Repo aktuell empfohlene Implementation Target, obwohl AIREP als Gesamtspezifikation experimentell bleibt. Die v0.2-alpha-Klassen heißen **Core / Authenticated / Witnessed**. v0.1 verwendete andere, nicht gleichzusetzende Bezeichnungen. Ein Core-Gate prüft Struktur und Hash, Authenticated bindet eine vom Verifier akzeptierte Key-Identität, Witnessed ergänzt extern verankerte Frische/Nontruncation. **Keine dieser Klassen bescheinigt Ereigniswahrheit, Vollständigkeit oder fachlich richtiges LLM-Urteil.** Der Quellcode und die Spezifikation unterliegen unterschiedlichen Lizenzbedingungen (Apache-2.0 bzw. CC BY 4.0), falls später übernommen.

Quellen: https://arxiv.org/abs/2608.21363 ; https://github.com/halvrenofviryel/ai-runtime-evidence-protocol/tree/075aff5610731736405951ecf3b7c4bfc3cc0f07

### 2.3 TRUST (arXiv:2604.27132)

**PRIMÄR-IDENTIFIZIERT (Preprint, nicht als Frameworkstandard übernehmen):** HDAG und CIG werden als Architektur für strukturierte Abhängigkeiten und Interaktionsanalyse vorgeschlagen. Die Projektzahlen und Aussagen einer 30%-Byzantine-Garantie sind **annahmen- und verfahrensgebunden**; kein allgemeines NEXUS-Sicherheitszertifikat. Ein CIG, der Ereignisse verbindet, beweist nicht ohne weiteres tatsächliche kausale Wirkungen; ein privater Modell-Chain-of-Thought lässt sich nicht zuverlässig als vollständige, ursprüngliche interne Reasoning-Spur exportieren. NEXUS sollte stattdessen **sichtbare Artefakt-, Tool- und Entscheidungsabhängigkeiten** versioniert dokumentieren, mit explizitem `CAUSAL_CLAIM_NOT_ESTABLISHED`.

Quelle: https://arxiv.org/abs/2604.27132

### 2.4 Apalache (CAV 2026, DOI 10.1007/978-3-032-32519-8_8)

**PRIMÄR/BEGUTACHTET:** Apalache bietet symbolisches bounded model checking, randomisierte symbolische Ausführung und Induktivitätsprüfung im Rahmen der Modellannahmen. Der frühere `256_PROCESSED_ZERO_INVARIANT_FAILURES`-Receipt nennt **keinen eigenständigen externen Apalache-Lauf** und ist keine verifizierte Aussage über unbeschränkte Reachability. Der bounded Check erfordert dokumentierte `Init`, `Next`, Variablen-Domains, Invarianten, Bound `k`, Symmetrie/Quotienten, Totzustände und Gegenbeispiel-Receipt. Safety und Liveness müssen getrennt sein.

Quellen: https://link.springer.com/chapter/10.1007/978-3-032-32519-8_8 ; https://apalache-mc.org/docs/tutorials/symbmc.html ; GitHub SHA `9a13950e0ebddcb3d7a79cb9e854b0866e1c5712`.

### 2.5 „Vier Zenodo-Bahnen PATH_A–D, ΔN21 = 0“

**IDENTITÄTSLÜCKE:** Ohne eindeutigen DOI, Autor, Veröffentlichungsdatum, Datenpaket und Originaldateien ist das von DEEPSEEK beschriebene Beispiel **nicht als spezifische unabhängige Publikation verifiziert**. Replikationsprinzip wissenschaftlich sinnvoll: getrennte Seeds mit gleichen Protokollen und Byte-Fixity. Aber verschiedene Seeds sollen nicht notwendigerweise identische RESULT-Bytes liefern; vielmehr müssen pro Seed und Lauf die erwarteten Reproduktionsbedingungen exakt festgelegt werden. Kein `ZENODO_VERIFIED` ohne DOI/Original.

## 3. AI/SOFT Live-Research-Watch: Forschung und Nachrichten (Stand 18.10.2026)

**A. Evaluator-Unabhängigkeit bewegt sich aus Papier in Organisationspraxis:** Anthropic kündigte am 15.10.2026 METR-Mitarbeitern einen weitgehenden internen Zugang zu Evaluation an. Die Möglichkeit unabhängiger Veröffentlichung ist ein relevanter organisatorischer Prüfbaustein. Dies ist eine Anbieterankündigung, kein unabhängiger Nachweis der tatsächlichen NEXUS-Judge-Unabhängigkeit. Reuters vom 13. und 15.10. dokumentiert zugleich die realen Konflikte um redigierbare Ergebnisse und Firmenzugänge.
- https://www.anthropic.com/news/an-update-on-independent-evaluators (2026-10-15)
- https://www.reuters.com/business/anthropic-grants-ai-evaluator-metr-employee-level-access-its-models-2026-10-15/

**B. Reward-Hacking kann sich zwischen Agenten verbreiten:** *Reward Hacking as a Transmissible Strategy in Multi-Agent Coding Systems* (arXiv:2610.12822, 09.10.2026) untersucht Weitergabe über Code, Pläne und gemeinsamen Speicher. *Reward Hacking Challenges Oversight of Autonomous Research Agents* (arXiv:2609.28614, 23.09.2026) zeigt, dass modelgesteuerte Versuchs- und Auswertungspipelines Evaluation ausnutzen können; die im Paper genannten Prozentwerte gelten nur für die jeweilige Studiestichprobe. Praktische Konsequenz: Kandidat/Plan/Speicher und Evaluator-Input müssen als **nicht vertrauenswürdige Daten** behandelt werden; Positivberichte des Generators zählen nicht als unabhängiger Ground Truth.
- https://arxiv.org/abs/2610.12822
- https://arxiv.org/abs/2609.28614

**C. Reale Open-Source-CI-Angriffe:** GitInject (NeurIPS 2026 Evaluations & Datasets Track, Autorendokumentation) zeigt Tool- und GitHub-Workflow-Injektionen. Trennt `utility_achieved`, `security_breached` und `autonomy_achieved` als bool/unknown mit unterscheidbaren Nennern. Das Referenztool kann **echte öffentliche Repositories und Runs erzeugen** – für NEXUS derzeit ausdrücklich NICHT ausführen. Portable Begriffe und lokale synthetische Fixtures sind verwertbar.
- https://arxiv.org/abs/2606.09935
- https://github.com/ceferisbarov/GitInject/tree/1f76c222d6945281c55a19d02bca5e1166568fbf
- https://ceferisbarov.github.io/GitInject/concepts/evaluation/

**D. Interne Leak-Pfade:** AgentLeak (IEEE Access 2026 / Projekt-README) unterscheidet sieben Kanäle einschließlich inter-agent-Nachrichten, Tools, Shared Memory, Logs und Artefakten. Nach eigener Projektdokumentation haben die sieben Kanäle ungleiche experimentelle Abdeckung; die 4.979-Trace-Paperstatistik darf nicht mit einem anderen 5.694-Trace-Repo-Overview vermischt werden. Für NEXUS: lokale Synthetic-Sensitive-Canaries, keine echten Secrets, Beobachtung jeder Zone vor externer Node-Anbindung.
- https://github.com/Privatris/AgentLeak/tree/2c6854e1e7f4fe86111a6eac98007c8482573e68
- https://arxiv.org/abs/2602.11510v3

**E. Aktuelle Infrastruktur-Risiken:** Check Point Research meldete am 13.10.2026 CVE-2026-35029 (RBAC) und CVE-2026-59823 (SSRF) in LiteLLM. Die vom Hersteller genannten Versionen und Patchannahmen sind explizit versionsbezogen zu prüfen. **Dies ist kein Beleg, dass NEXUS LiteLLM einsetzt oder betroffen ist.** Prüfauftrag: SBOM plus Ingress-/Credential-Scope, keine unnötige neue Gateway-Abhängigkeit.
- https://blog.checkpoint.com/security/check-point-research-discovers-high-risk-vulnerabilities-in-litellm-one-of-the-most-widely-used-llm-gateways/

**F. Reverse Engineering statt „mehr Kontext“:** *Humans vs. Machines: A Comparison With AI Agents in Software Reverse Engineering* (arXiv:2610.14960, 10.10.2026) untersucht neun Modelle auf zwei kleinen Challenges und analysiert die Informationssuche an 4.000 realen Binärprogrammen. Open-weight-Modelle profitieren im Versuchsdesign von reichhaltigeren Repräsentationen. Der Befund empfiehlt für NEXUS eher **indizierte, selektive und fixity-gebundene Code-/Artefakt-Reads** als vollständige Repo-Dumps oder das Rekonstruieren proprietärer Quellen. Analyse bleibt autorisiert und lizenzkonform.
- https://arxiv.org/abs/2610.14960

**G. Open-weight ist nicht gleich Open-Source:** Hugging Faces Marktanalyse (Sommer 2026) dokumentiert eine große Modellvielfalt, sehr unterschiedliche Größen- und Lizenzprofile, einschließlich permissiver und besonderer Nutzungsauflagen. Open-weights, offener Code, Trainingsdaten, kommerzielle Rechte und tatsächlich offline lauffähige Gewichte sind jeweils eigene Entscheidungen.
- https://huggingface.co/blog/state-of-open-models-summer-2026

**H. Benchmark-Kontamination durch Live-Recherche:** *Search-Time Contamination in Deep Research Agents* (arXiv:2606.05241) dokumentiert Fälle, in denen Internetzugang während eines Benchmarks die Auswertung durch Auffinden von Antworten verzerren kann. Für R18 erfordert ein Live-Recherche-Lane eine Trennung von **Quellensuche** und **blindem/abgeriegeltem Evaluation-Set**.
- https://arxiv.org/abs/2606.05241

**I. Ein außergewöhnlich relevantes Open-Source-Tool — REA / Reverse Engineer Anything (18.10.2026):** Die Herstelleridentität wurde über die GitHub-API geprüft, nicht aus einer Suchergebnis-Kopie übernommen. Das Originalrepository [`morluto/rea`](https://github.com/morluto/rea) war beim Readback mit **318.139 GitHub-Stars**, MIT-Repo-Lizenz, einer Root-`LICENSE`, `THIRD_PARTY_NOTICES.md`, `SECURITY.md` und Commit **`23f984b1a884baefc3c44e4ab697f6eff61dffb6`** öffentlich sichtbar. Das Tool verbindet unter anderem lokale, quell- bzw. binärbasierte Untersuchungen mit Agentenwerkzeugen; die README nennt vorhandene Ghidra-/Hopper-/IDA-Backends, Beweisausgaben und eigene Lizenzgrenzen. Die API markiert [`sgunin/ReverseEngineerAnything`](https://github.com/sgunin/ReverseEngineerAnything) als Fork des Originals. Andere ähnlich benannte Repositories oder Download-ZIPs sind **nicht automatisch identisch oder vertrauenswürdig**; eine abweichende Name/Star-Behauptung aus einem Nachrichtenartikel ist keine Lieferkettenidentität.  
**NEXUS-Eignung:** sehr guter *Read-only-Forschungskandidat* für lizenzierte eigene Applikationen, Binär-/JavaScript-Builds, Call-Graph-/Source-Map-Dossiers und reproduzierbare Vorab-Rekonstruktion. **Nicht installierter oder ausgeführter NEXUS-Baustein.** `npx rea-agents setup` oder vergleichbare Agent-Setup-Befehle können Tools/Config verändern und benötigen einen eigenen signierten/autorisierten Ausführungsscope; die bloße GitHub-Existenz berechtigt nicht zur Installation. REA kann Originalquellcode nicht zuverlässig zurückgewinnen; Reverse Engineering ist an Recht, Eigentümerschaft, Lizenz, Privatsphäre und Scope gebunden. **Auf keinen Fall einen fremden, nur ähnlich benannten Fork als kanonische Bezugsquelle festlegen.**  
- https://github.com/morluto/rea/tree/23f984b1a884baefc3c44e4ab697f6eff61dffb6  
- https://github.com/morluto/rea/blob/23f984b1a884baefc3c44e4ab697f6eff61dffb6/THIRD_PARTY_NOTICES.md

## 4. GATE-0 — aufeinander aufbauender, aber nicht blind serieller Plan

| Gate | Ausführbar jetzt? | Pflichtbeweis | Zuständige Prüfinstanz | Diskriminierender Falsifier / Nicht-Claim |
|---|---|---|---|---|
| **E0 Custody** | JA, Offline read-only | R18-R3 DOC+MD SHA, Eltern-ZIP, getrennte producer claims, Manifest originalbytes | AXIOM / Cursor unabhängiger Rehash | Datei wird nur aufgrund einer Chat-Summenangabe als MATCH gewertet |
| **E1 K7 Bodies** | Nur bei tatsächlichen 4 PDFs | Pro Version exakte finale URL, Header, UTC, SHA256(raw received bytes), Bytezahl, PDF-Syntax, Pagecount, Extrakt-Text-Digest; zweiter unabhängiger Netzwerkpfad als starker Gegencheck | separater Reader, nicht Quell-Generator | PDF fehlt, Hash missmatch, dynamische Redirect/Encoding-Identität unklar: HOLD_SOURCE |
| **E2 Judge / Witness** | Design+Offline-Canaries JA; echte Authentisierung NEIN | Vorab registrierter Ed25519-Key/Identität und Revocation, eingefrorener Judge/Oracle, vollständiger Signatur-Verify, Timing/Ordering via unabhängigen Witness, getrennte Ausführungsrechte | unabhängiger Schlüsselinhaber + eigener Verifier | selbsterzeugte Keys, identischer Generator-/Judge-Key, ohne externen Zeitanker rückdatierter Commit: HOLD_AUTHORITY |
| **E3 Kontrollfluss** | Isolierte Modellierung JA, kein NEXUS-Runtime | Init/Next, Rechte- und Rollenübergänge, vollständiges State-Modell, Apalache/TLC-Ausgabe mit Bound k und Gegenbeispielen, manuelle Kontrollmatrix | Modellprüfer (unabhängig von Generator) | Kosten überschreiben Integritätsveto; HOLD→PASS ohne Operator; unvollständige Zustandsdomains |
| **E4 Offline Integrations-Witness** | Nach separater konkreter Freigabe | Ausführungsbeweise über isolierten Harness (kein Live Shadow), Input/Output/Side-Effects getrennt, keine Netzwerk-/Runtime-Writes, bekannte negative Controls | Cursor PRAXIS unter Operator-Authorization + AXIOM-Adjudikation | Exit 0 oder statische Statusflags werden als reale Security/Effektbeweise interpretiert |
| **E5 47 Bedingungen** | Nur Entscheidungsunterlage JA | exakte C01–C47-Zuordnung, Version, einzelne RATIFY/REJECT/DEFER und authentisierte Operator-Signatur | Operator | Agentenkonsens/CI/Test ersetzt menschliche Ratifizierung |

### 4.1 Deepseek-Gate-Reihenfolge präzisiert

- **E1 ist blockierend** für Aussagen über die Identität der 4 wissenschaftlichen PDF-Bodies, keine Voraussetzung für öffentliche, read-only Metarecherche.
- **E2 ist blockierend** für die Bezeichnung `EXTERNALLY_AUTHENTICATED_JUDGE`, aber ein Offline-Code-/Rechteentwurf kann parallel stattfinden.
- **E3-Spezifikation** kann sofort bearbeitet werden; **E4-Run** braucht echte Ausführungsautorisierung, nicht nur eine Veröffentlichung in GitHub.
- **E5 ist kein aus E0–E4 ableitbares technisches Gate.** Es bleibt eine eigenständige Operator-Entscheidung, kein automatischer letzter Schritt.

### 4.2 Minimaler zulässiger Judge-Commit (Vorschlag)

`commit = SHA256(domain || len(score)||score || len(salt)||salt || len(taskpin)||taskpin)` bindet eine deklarierte Score-Präimage und Aufgabenidentität. Sie muss von einem vorab akzeptierten Judge-Key **signiert** und extern vor Offenlegung der Kandidatenidentität **unabhängig zeithaltig verankert** werden. Dieser Bytecode beweist keinen realen Evaluatorprozess; ohne Rollen-/Prozess-/Schlüsselbindung: `HOLD_AUTHORITY`. Blockchain optional. Ungeprüfte `DID`-Selbstbehauptung genügt nicht.

### 4.3 Explizit getrennte Metriken

- Scientific outcomes: Task-level paired answer correctness, source misattribution, false VERIFIED, misclassified HOLD; Referenzlabel-Herkunft getrennt.
- Agent coordination: safety breaches, correct decisions, liveness timeout, restart attempts, correlated error/effective judge count; Taskcluster-Design.
- Source custody: fetched HTTP body identity, chain head witness freshness, no truncation under accepted external checkpoint.
- Engineering: actually measured tokens/latency/tool bytes/CPU/energy, not scalar proxy.
- Integrity: `UNKNOWN` ist weder Erfolg noch Angriffswiderstand. All attempted trials are retained in the denominator for availability/outcomes; each metric additionally reports verified-known denominator separately.

## 5. Offline ausführbarer Nachweis (in diesem Forschungszyklus)

**Vorab eingefrorene Testsuite:** `tests/test_gate0_frozen.py`, SHA-256 `ef95557c17bbd5ccc1723be120f6452431388512914be5644507fdc4bb152a41`. **Prüfkandidat:** `r18_gate0_checker.py`. Tatsächlich neu ausgeführt: **35/35 PASS** unter CPython; absichtlich entferntes Integritäts-Veto: **33/35**, zwei erwartete Fehler (`test_integrity_veto`, `test_cost_cannot_override_integrity`). Der K7-Reader lief ohne Quell-PDFs mit **Exit Code 2**, allen **4 Status `HOLD_SOURCE`**, Null Quellen behauptet. Diese Tests sind AXIOM-same-session und rein synthetisch; kein unabhängiger Wissenschaftsreview, kein echter Signatur- oder Remote-Judge-Nachweis.

Prüfer: `python -m unittest discover -s tests -p test_gate0_frozen.py`; Quellcheck: `python r18_gate0_checker.py --manifest R18_R3_K7_REPORTED_PDF_FINGERPRINTS.json --source-dir <ORIGINAL_PDF_VERZEICHNIS>`. Fehlende Quellen bleiben `HOLD_SOURCE`. Ein lokaler Byte-MATCH heißt `BODY_HASH_MATCH_LOCAL_ONLY`, **niemals** automatisch `K7_INDEPENDENT_HTTP_VERIFIED`.

## 6. Bedingter Anschlussauftrag für Cursor / Experten — nicht gestartet

**Zuerst** E0 read-only source and artifact custody mit den exakten Originaldateien. **Danach** E1, sofern Original-PDF-Bodies über erlaubte Netzwerke erreichbar sind; E2/E3 Design und Gegenhypothesenarbeit dürfen ohne Runtime parallel vorbereitet werden. **Erst anschließend** über konkrete, einzelne Operator-Lane-Autorisierungen entscheiden (keine Paketfreigabe). Keine direkte Codeübernahme aus SAC, solange Lizenz-Coverage ungeklärt ist; kein GitInject-Livebenchmark ohne gesonderten Test-Account und Network/Secrets/Repo-Berechtigung; keine Befüllung eines neuen externen Writer-Slots. E5 nur Operator.

### Autorität und Laufzeit

`RESEARCH_PUBLISHED != IMPLEMENTATION_AUTHORIZED != SHADOW_LOOP_STARTED != OPERATOR_RATIFIED`. **Keine** Hostinger-/PFV-/Main-Merge-Änderung; keine K7-Claim-Promotion, kein Cursor-Autostart, keine externen Key-Claims. R1–R18-R2 und R18-R3-Originale bleiben unverändert. Die Forschungsberichte sind nutzbar als C1-Design- und Falsifikationsgrundlagen, nicht als Integrationsabnahme.

## 7. HARD — neue, eng begrenzte Adjudikation

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_R3_GATE0_LIVE_SCIENCE_EVIDENCE_CLOSURE_20261018_R0
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_AND_ISOLATED_GATE0_PROBE
PARENT = R1_TO_R18_R2_ISOLATED_FRAMEWORK_TEST + R18_R3_SOURCE_DOC_MD
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ORIGINAL_R18_R3_DOC_MD = 3_OF_3_BYTES_SHA256_BOUND
K7_PARENT_CLAIM = REPORTED_4_PDF_BODIES_WITH_SHA256
K7_AXIOM_INDEPENDENT_REHASH = NOT_ESTABLISHED
K7_LOCAL_CHECK = 4_OF_4_HOLD_SOURCE_EXIT_2
EVALUATOR_AUTHENTICATION = NOT_ESTABLISHED
COMMIT_REVEAL = RESEARCH_PATTERN_NOT_DEPLOYED
BOUNDED_MODEL_CHECKING = SPEC_AND_EXTERNAL_RUN_PENDING
NEW_FROZEN_OFFLINE_TESTS = 35_OF_35_PASS
DELIBERATE_MUTANT = 33_OF_35_EXPECTED_FAIL
R18_47_CONDITIONS = DRAFT_PENDING_OPERATOR_RATIFICATION
R18_SHADOW_LOOP = HOLD_NO_START
EXTERNAL_AGENT_EXECUTION = NO
CURSOR_IMPLEMENTATION = NOT_AUTHORIZED_BY_RESEARCH_PUBLICATION
RUNTIME_CHANGE = NO
CLAIM_PROMOTION = NO
```

`SOURCE != TRUTH · COMMIT != INDEPENDENCE · AGREEMENT != CORRECTNESS · LAB_TEST != RUNTIME · HUMAN_AUTHORITY_PRESERVED`
