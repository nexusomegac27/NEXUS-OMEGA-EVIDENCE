# NEXUS OMEGA — R18-R2 · Zweite adversarielle wissenschaftliche Online-Tiefenrecherche

**Stichtag:** 2026-10-18 · **Akte:** `NEXUS_OMEGA_AXIOM_R18_ADVERSARIAL_ONLINE_DEEP_RESEARCH_FOUNDATION_20261018_R2`  
**Zustand:** `PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_R2_ESTABLISHED`  
**Claim-Grenze:** `C1_DESCRIPTIVE_ONLY` · **Runtime:** `FROZEN` · **47 Bedingungen:** `DRAFT_PENDING_OPERATOR_RATIFICATION` · **Shadow-Loop:** `HOLD_NO_START`.

## 0. Executive Decision

R18-R1 ist ein wissenschaftlich sinnvoller, jedoch nicht implementierungs- oder ratsfähiger Integritätsrahmen. R18-R2 ergänzt ihn um fünf bislang untergewichtete, aus unabhängiger Literatur herleitbare Falsifikationsachsen: (I) **korrelierte Fehler von Evaluator-Panels**, (II) **Safety versus Liveness versus semantische Korrektheit**, (III) **adversarielle Überzeugung/Argumentstil und indirekte Prompt-Injektion**, (IV) **Einzelagenten- und Budget-Kontrollarme**, (V) **authentifizierte Provenienz samt transparenter, datensparsamer Beobachtung**. Kein Ergebnis berechtigt, SAC, CP-WBFT oder ein Ledger-Produkt sofort zu integrieren. Die Rollen-, K7- und C01–C47-HOLDs bleiben aktiv.

**Zentrale wissenschaftliche Trennung:**

```text
AGREEMENT != CORRECTNESS != SAFETY != LIVENESS
RECEIVER_LLM_SCORING != DETERMINISTIC_JUDGE != FORMAL_PROOF
N_AGENTS != N_INDEPENDENT_JUDGES
SIGNED_ATTESTATION != CORRECT_GENERATION
SOURCE_CLAIM != K7_RAW_BODY_VERIFICATION
C1_RESEARCH != SHADOW_LOOP_EXECUTION != PRODUCTIVE_APPROVAL
```

**Quellebene:** Die neun R18-R1-Operatorartefakte und der R18-R1-Stack bleiben unverändert. Das originale R18-R1-ZIP wurde in dieser Sitzung nochmals physisch geprüft: **98.547 Bytes**, SHA-256 `08b51af99c973c2fb86b49ccea989be587ca52844674b925438b681e338f527d`, **14 Einträge, ZIP-CRC ohne Fehler**. Die 42/42 R18-R1-Tests und die 39/42-Mutante sind *zuvor berichtete synthetische Ergebnisse*, nicht neue reale Experimente. R18-R2 erstellt einen separaten, vor der Implementierung geschriebenen 14-Test-Vertragsprüfer; dieser ist ebenfalls synthetisch.

**Primärquellen-Grenze K7:** Web-/GitHub-Werkzeuge lieferten abrufbare Textinhalte, Git-Datei-Blobs, Versionen und URLs. Der direkte Rohbody-Abruf der arXiv-PDF über die Containerumgebung war technisch nicht möglich; vollständige HTTP-Status-/Header-/Content-Length-/Body-SHA-Belege pro externer Quelle fehlen. Deshalb werden Primärquellen in diesem Bericht als `CONTENT_AND_SCOPE_REVIEWED`, nie als `K7_RAW_BYTE_VERIFIED` klassifiziert. Veröffentlichungsdatum der referenzierten Quellen ist nicht identisch mit unserem Fetch-Zeitstempel.

## 1. Kritische Lesart der SAC-/CP-WBFT-Ausgangsforschung

### 1.1 SAC und die formale Grenze seines Evaluators

Lee, Yun, Panagou & Karimireddy, *Robust Multi-Agent LLMs under Byzantine Faults*, arXiv:2605.09076v2 (29. Juni 2026), formulieren für SAC einen lokal empfangsseitigen Score

`score_i(j,t) = phi_i(query, response_j(t))`, wobei `phi_i` vom **LLM des empfangenden Agenten** per Verification-Prompt berechnet wird. Ein solcher Empfänger-Score schützt vor der schlichten Manipulation eines vom Sender selbst angegebenen numerischen Konfidenzwerts. Er ist weder *formal korrekt* noch gegen semantische Fehleinschätzungen, systematisch geteilte Halluzinationen, persuadierte Bewertungen oder indirekte Instruktionen zwingend resistent. Die klassische `(F+1)`-Robustheit der Kommunikationsgraphen ist an `F`-lokale Byzantine-Mengen, Graphannahmen und das *im Modell verwendete Scoring* gebunden; sie zertifiziert kein externes, korrektes Ground-Truth-Urteil.

**Präzise neue Korrektur:** Eine Beweisführung über das Untergrenzenverhalten *subjektiver Scores* darf nicht mit einem Beweis der **semantischen Richtigkeit** der behaltenen Nachricht gleichgesetzt werden. Eine systematische Kalibrierungs- und Prompt-Injection-Prüfung der Empfänger-Scores bleibt ein eigener Falsifikationsschritt.

### 1.2 Versions- und Nenneridentität: erhalten, aber erweitert

Die R18-R1-Auswertung bleibt korrekt für den genau genannten v1-/v2-Stand:

| Herkunft | Haupt-MATH | MATH-Ablation | Commonsense | Einordnung |
|---|---:|---:|---:|---|
| arXiv:2605.09076 **v1** | 30 Aufgaben | 30 | 30 | eigener historischer Tabellenstand |
| arXiv:2605.09076 **v2** | 100 Aufgaben | 30 | 30 | anderer, nicht mit v1 mischbarer Stand |
| arXiv:2605.09076 **v3** | `NOT_VERIFIED` | `NOT_VERIFIED` | `NOT_VERIFIED` | Metadatenhinweise in sekundären Indizes, Primärbody derzeit nicht abrufbar |

**Wichtige Statusänderung zu R18-R1:** Scirate/alphaXiv melden sekundäre Hinweise auf `v3` (bei mindestens einem Index mit August-2026-Datierung). Der Erstabruf des vollständigen v3-Primärdokuments gelang nicht. Daher `SECONDARY_VERSION_INDICATION` statt einer pauschalen Annahme, v3 sei nicht existent; **keine v3-Tabellen-/Autoren-/Lizenzbehauptung** wird hier akzeptiert. Die v1-/v2-Tabelle bleibt strikt versions- und datensatzgebunden.

Metriken sind methodisch verschieden: `IAA`, `FAA` und `BFTI = FAA − IAA` (Prozentpunkte, *alle Agenten*); `RA` (Mehrheit sämtlicher Agenten); `H-Majority` (nur ehrliche Agenten); `S/W-IAA→FAA` (starke/schwache ehrliche Teilgruppen). Repräsentative v2-Zellen `CP-WBFT MERG MATH100 52,3 -> 43,6 => −8,7 pp` und `SAC MERG MATH100 50,1 -> 53,1 => +3,0 pp` sind veröffentlichte Autorenwerte, **keine R18-Replikation**.

### 1.3 CP-WBFT und Angriffsabgrenzung

Zheng et al., *Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance*, arXiv:2511.10400, begründen CP-WBFT mit Konfidenz-Probes. Die 85,7-%-Fault-Rate gehört zur publizierten Versuchsanordnung und nicht zu einer standardisierten NEXUS-Fehlergarantie. Die gegen CP-WBFT berichtete SAC-Attacke mit manipuliertem Selbstrating 1.0 widerlegt eine spezifische Verwendung selbstberichteter Werte. Sie beweist nicht, dass alle denkbaren, externen und kryptografisch unmanipulierbaren Probe-Mechanismen gleich verwundbar sind. Zugleich darf eine Probe **niemals** ihre eigene Validität durch eine generierte Konfidenzbehauptung definieren.

## 2. Externe Gegenforschung — fünf neue diskriminierende Erkenntnisse

### 2.1 Korrelierte Fehlurteile: effektiv deutlich weniger Stimmen

Kohli, *Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels* (Mai/Juni 2026), untersuchte **neun** Frontier-Judges aus **sieben** Modellfamilien an drei NLI-Datensätzen mit jeweils 100 menschlichen Annotationen pro Item. In dieser Untersuchung lieferten neun formelle Judges nur rund **zwei effektiv unabhängige Stimmen**. Die Panelgenauigkeit lag **8–22 Prozentpunkte** unter einer hypothetisch unabhängigen Abstimmung. Dies ist *ein externer empirischer Befund unter diesen Testbedingungen*, **kein gemessener Wert des NEXUS-Kollektivs**.

R18-R2-Prüfgröße `N_EFFECTIVE` als deskriptive Statistik, nicht als autorisierendes Kriterium: Unter vereinfachter gleichpaariger positiver Fehlerkorrelation `rho` kann `n_eff ≈ n / [1 + (n−1)rho]` als Orientierungsgröße dienen. Reale Panels brauchen die vollständige Fehlermatrix/Bootstrap und eine Vorsicht gegenüber ungleichen Kompetenzprofilen, Abhängigkeiten und Testset-Leakage. Ohne unabhängige Referenzlabels ist keine empirische Fehlerkorrelation gegenüber Wahrheit messbar. Wer neun Agenten startet, hat nicht neun geprüfte Wahrheitszeugen.

### 2.2 Safety, Liveness und Ground Truth sind unabhängige Achsen

Berdoz, Rugli & Wattenhofer, *Can AI Agents Agree?* (arXiv:2603.01213, März 2026) untersuchen ein No-Stake-Konsensspiel mit skalarer Einigung. Ausfall durch **Stillstand, Timeout und Nichtkonvergenz** dominiert dort. Das ist von inhaltlich falschem Gruppenkonsens zu trennen. R18 benötigt deshalb `AGREEMENT_VALID`, `SEMANTIC_CORRECT`, `SAFETY_VIOLATION`, `LIVENESS_FAILURE`, `ABSTAIN`, `TIMEOUT`, `MISSING_RESPONSE` mit Aufgaben-/Runden-Nennern. Ein Timeout wird weder aus der Stichprobe gelöscht noch in Zustimmung umetikettiert. Ein Konsens innerhalb der verfügbaren Antworten belegt noch keine Korrektheit des Konsensgegenstands.

### 2.3 Adversarielle Überzeugung ist nicht nur Prompt-Injection

Kraidia et al., *When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate* (*Scientific Reports*, 8. April 2026), untersuchen eine überzeugend auftretende fehlerhafte Agentenstimme. Das Paper berichtet für seine Benchmarks **10–40 %** Genauigkeitsabfall und einen Anstieg falscher Übereinstimmung um über **30 %**. Die Einheit von „10–40 %“ ist aus der vorliegenden Abstract-Formulierung nicht konsistent als Prozentpunkte auszulegen und wird deshalb NICHT in NEXUS-Leistungsmesswerte umgewandelt. In einzelnen Bedingungen verstärken Best-of-N und selektives Retrieval die Überzeugungskraft der Manipulation.

Daraus folgen getrennte Eingriffsarten: (a) falsifizierte Selbstkonfidenz, (b) hochflüssige rhetorische Überzeugung, (c) selektiv echte Quellen zitierende Argumente, (d) direkte/indirekte Prompt-Injektionen, (e) konsistente kolludierende Fehler. Nur (d) ist klassischer Prompt-Injection-Angriff. OWASP LLM01 beschreibt explizit, warum Dokumente und Tool-Antworten externe, nicht vertrauenswürdige Instruktionen tragen können. Alle fünf Angriffsarten brauchen eigene Negativfixtures mit einer **getrennten nicht-LLM-basierten Instruktionsgrenze**.

### 2.4 Der Nutzen zusätzlicher Agenten ist aufgabenabhängig

Kim et al., *Capable language models can outgrow the benefits of collaboration* (*Nature Machine Intelligence*, 24. Juli 2026), untersuchen 260 Konfigurationen über sechs Benchmarks, fünf Architekturen und drei Modellfamilien bei kontrollierten Prompt-/Werkzeug-/Rechenbedingungen. Die Baseline-Fähigkeit des Einzelagenten ist zentraler Prädiktor; oberhalb eines empirisch ermittelten Fähigkeitsbereichs kann zusätzliche Koordination schaden. Die berichteten 94 % Trefferquote einer Schwellenheuristik gelten **nur** für die beschriebenen Validierungsbedingungen und sind kein allgemeines Gesetz oder R18-Effizienznachweis.

Daher wird die **Einzelagenten-Baseline zwingend**, und die Option `NO_COLLABORATION` gehört als legitimer Null-/No-Go-Kandidat auf dieselbe Entscheidungstafel wie SAC, Mehrheitswahl und CP-WBFT. Falls Zusammenarbeit keine vorher festgelegte Verbesserung erzielt, ist das kein Governance-Fehler, sondern ein gültiges negatives Forschungsergebnis.

### 2.5 Prozessmetrik statt nur Ergebniszahl

Pitre et al., *A Diagnostic Study of Multi-Agent LLMs for Real-World Debates* (ICML 2026 / PMLR 306), unterscheiden Ergebnisindikatoren von Debatten-Prozessgrößen wie Engagement, Antwortreaktion, einseitigem Einfluss, Stabilität, Agentennutzen und frühzeitiger Konvergenz. R18 ergänzt deshalb `INFLUENCE_ASYMMETRY`, `SOURCE_DIVERSITY`, `RESUME_RECOVERY`, `ROUND_COST`, `FALSE_HOLD_LIFT` und `NEGATIVE_EVIDENCE_RETAINED` als **getrennte** Berichtsfelder. Keine dieser Größen erhält allein die Rolle eines Wahrheitsscores.

## 3. Kalibrierung, Abstention und formaler Integritätscheck

**Proper Scoring / Kalibrierung:** Brier-Score oder Expected Calibration Error setzen einen wohldefinierten Ereignisraum, echte Referenzlabels und eine getrennte Kalibrierungsstichprobe voraus. Ein gut kalibriertes LLM-Prognoseintervall ist weder ein konkreter Beweis der Korrektheit einer Antwort noch immun gegen Verteilungsverschiebung. Es gibt **keinen wissenschaftlich etablierten skalar definierten `COLLECTIVE_WISDOM`-Index** in den NEXUS-Artefakten. Die rhetorische R18-P0-Formel multipliziert nicht definierte Nenner und ist als Metrik `NOT_OPERATIONALIZED`. Sie darf nur als Analogie vorkommen, niemals in einem GATE.

**Abstention als eigener zulässiger Ausgang:** SAFER (ICLR 2026) und SCoRE (arXiv:2603.24704) liefern kontrollierte abstentions-/selektionsbezogene Forschungsmodelle unter ausdrücklich benannten Kalibrierungsannahmen. Das legitimiert nicht automatisch deren Übernahme, zeigt aber, dass die Entscheidung `HOLD/ABSTAIN` ein messbarer Teil des Systems sein muss. Erforderlich sind `COVERAGE`, `SELECTIVE_RISK`, `ABSTAIN_RATE`, `FALSE_ACCEPTED_VERIFIED`, Unsicherheitsintervalle, Untergruppen-/Taskspezifikation und Kalibrierungsdrift. Marginale Abdeckung ist nicht gleich verlässliche Untergruppenabdeckung. Jede geplante probabilistische Akzeptanzregel benötigt eine **separat präregistrierte** Validierung mit unabhängigen Labels und vorab festgelegter Fehlerkostenmatrix.

**Formale Verstärkung:** Die Open-Source-Tools `apalache-mc/apalache` und `model-checking/kani` sind geeignete Forschungsfragmente, um **begrenzte abstrakte Zustandsautomaten** zu prüfen. Vorgeschlagene Modelle: `NO_CANDIDATE -> EXIT_NOGO`, `UNKNOWN_PROOF -> HOLD`, `INTEGRITY_FAIL -> REJECT`, `OPERATOR_UNAUTHENTICATED -> HOLD`, `RETURN_TO_HOLD_AFTER_KEY_ROTATION`, `GENERATOR_WRITE_TO_JUDGE -> DENY`, `RESTART_AFTER_NOGO -> NEW_AUTHORIZATION_REQUIRED`. Eine modellgeprüfte endliche Zustandsmaschine zertifiziert nicht die Semantik einer realen LLM-Entscheidung, Netzwerkidentität oder Betriebssicherheit.

## 4. Open-Source-Symbiose: getrennte Rollen und Reifegrenzen

| Schicht | Referenzfragment (Git SHA am Prüftag) | Fachlicher Nutzen | Nicht nachgewiesen / No-Go |
|---|---|---|---|
| LLM-BFT Kandidat | `daniel-eai/Robust-Multi-Agent-LLMs-under-Byzantine-Faults@2ef7061590d0968ea4bd19f82b8d7ddde8f2bb89` | Autoren-SAC, lokales Scoring, Log-/Topologie-Layouts | Keine NEXUS-Replikation, keine getrennte Prüferautorität, Lizenzdeckung unklar |
| Vergleichsbasis | `Z1ivan/Byzantine-Fault-Tolerance-in-LLM-MAS@7f7464dc0415f415182f25e99b71738730a87408` | CP-WBFT/Probes, MIT im Repository | Keine implementierte unmanipulierbare Probe in NEXUS |
| Audit-Ledger A | `Aperintelligence/nexuscone@45b51e7a987d97a23d279f6f2c57e12d231b6201` | SQLite-/Hash-Ketten, optionale Zeitanker | Signierung/Anker müssen tatsächlich konfiguriert, geprüft und extern verwahrt sein |
| Audit-Ledger B | `OgenticAI/ogentic-audit@bd994be094f4c468054873027712091600f32fc6` | HMAC-Kette, Bedrohungsmodell, Crash-Tests | Volle Neuverkettung/Key-Compromise bei fehlendem externen Checkpoint |
| Evaluation | `mohammadi-hadi/judgekit@ae2603488ba257f29873162bc2ff58ee8b18bd3f` | Bias-/Konsistenzprüfung von LLM-Urteilen | Menschliche/goldene Referenzlabels, Validierungsset und Modellpin erforderlich |
| Source-Kontrollen | `gittuf/gittuf@324bb132df4381eab1ace15667a0152291018ef2` | Git-Policy/Identitäts- und Metadatenabsicherung unabhängig vom Forge | Beta, noch keine NEXUS-Integration oder tatsächliche Authentisierung |
| Model-Checking | `apalache-mc/apalache@9a13950e0ebddcb3d7a79cb9e854b0866e1c5712` | TLA+/Quint symbolischer Zustands-/BFT-Entwurfscheck | Begrenztes Modell, kein Beweis aller realen LLM-Eigenschaften |
| Quell- und Build-Provenienz | SLSA **v1.2**; `in-toto/attestation@fd2609c16bcb0ac53443e2b4612977f997e8f9a5` | Nachweis, was mit welchen Pins wie erstellt wurde | Kein Nachweis fachlicher Wahrheit; keine behauptete erfüllte SLSA-Stufe ohne unabhängige Attestationen |
| Signatur/Transparenz | `sigstore/cosign@cfeaa4a435c9d42cf724b3e1aac20c1cc09c4be7`; `sigstore/rekor@774b191f9f761b3def5808bcd54b48ad88de5f89` | signierte Artefaktidentität, inclusion-/consistency-nachweisbare Logs | Richtiges erwartetes Signer-Identity-Profil und unabhängiges Monitoring erforderlich |
| Metadaten/Tracing | `open-telemetry/semantic-conventions@331541c4057c53d133c32efadaa7b656636eda77` | portable Spans für Modell-/Tool-/Evaluator-Läufe | Rohprompts, Positionsdaten, Secrets oder private Texte NICHT standardmäßig exportieren |

**SAC-Lizenzpräzisierung R2:** Am oben genannten Autoren-Commit enthält `README.md` tatsächlich den Satz, dass das Repository die MIT-Lizenz des CP-WBFT-Basisframeworks beibehält (Git-Blob `ed3380b1559a74374235f84cfc0af0e4805c1ad4`). Eine separate Root-LICENSE-Datei ist im selben Commit **nicht vorhanden**, und GitHub-Metadaten führen kein SPDX-Lizenzobjekt. Deshalb ist `MIT_CLAIM_IN_README` positiv nachweisbar, die Weiterverwendungsreichweite und die Unterlizenzen jedoch `NOT_INDEPENDENTLY_CLEARED`. Ein rechtlicher Gesamtfreigabestatus kann daraus weder positiv noch negativ abschließend abgeleitet werden. Bis Review: **keine SAC-Codeübernahme**, nur Beschreibung, Paperreferenz und clean-room Design.

**SLSA-/Sigstore-Semantik:** SLSA **v1.2** unterscheidet ausdrücklich einen Source-Track (Source-L1 bis L4) von einem Build-Track (Build-L1 bis L3). Attestationsprädikate erlauben Provenienzbehauptungen, nicht deren unabhängige Richtigkeit. Nach Sigstores eigenem Bedrohungsmodell benötigt Log-Sicherheit unabhängige Überwachung; ein Zertifikat belegt eine zu erwartende OIDC-Identitätskette, aber keine gute wissenschaftliche Schlussfolgerung. `gittuf` kann als späterer zusätzlicher, forge-neutraler Policy-Verifikationsansatz erforscht werden. Kein Tool wird durch dieses Dokument installiert oder ausgeführt.

## 5. R18-R2 — Strenge Evaluator-Independence-Kontrollgates

| Gate | Nachweisziel | Akzeptanzvoraussetzung | harter Falsifier |
|---|---|---|---|
| `G0_SOURCE_FIXITY` | K7/Archividentität | Vollständiger Body-SHA, URI, UTC, Methode, Version, Media-Typ, unabhängiger Rückabruf | Prüfer markiert Web-Snippet als Rohbody-geprüft |
| `G1_ROLE_AUTH` | Operator-/Prüferidentität | getrennte, verifizierte Actor-Keys und signierte Berechtigungs-Scope | Generator setzt Prüferrolle oder hebt HOLD |
| `G2_CODE_PIN` | Unveränderliches Prüforakel | exakter Evaluator-Commit, Manifest, Lockfile, Build-Umgebung, Generator-DENY | Generator ändert Prüfer, Config oder Laufzeitlog |
| `G3_DATA_BOUNDARY` | Inhalt ≠ Befehl | eingefrorene Aufgabe, Schema, Prompt-/Injection-Negativfälle | empfangene Argumente ändern Gate oder Systemprompt |
| `G4_ERROR_CORRELATION` | tatsächliche Unabhängigkeit | identische Aufgaben, getrennte verifizierte Labels, Fehlerkorrelationsmatrix | nominelle Node-Zahl als `n_eff` ausgewiesen |
| `G5_SAFETY_LIVENESS` | Konsensfunktion | getrennte Denominatoren für Agreement, Accuracy, Timeout und Abstention | fehlender Output als Erfolg gezählt |
| `G6_HARD_VETO` | Korrektheit/Integrität | `FAIL -> REJECT`; `UNKNOWN -> HOLD`; erst danach Kosten | hoher Ressourcenbonus hebt Veto auf |
| `G7_LEDGER_WITNESS` | externe Unveränderlichkeitskontrolle | Vorgängerhash, unabhängiger Checkpoint, Writer/Reader-ACL, Rewrite-Test | ganzer Ledger still ersetzt oder gelöscht |
| `G8_CALIBRATION` | verlässliche Unsicherheit | Labels, Risk/Coverage, Out-of-Distribution- und Gruppenprüfung | Confidence als verifizierte Wahrscheinlichkeit behauptet |
| `G9_OPERATOR_GATE` | menschliche Außenautorität | Rollen-, Retention-, No-Go- und Ratifizierungsentscheid authentisiert | Generator markiert eigene Empfehlung als `ACCEPTED` |

Kritische fachliche Forderung: Eine technisch gültige Multi-Agenten-Kommunikation darf einen syntaktisch gültigen, aber falschen `ADJUDICATED`-Anspruch nicht erzeugen. `ADJUDICATED` ist daher ausschließlich als **durch das benannte Nachweisprofil begrenzter, von einem autorisierten menschlichen Workflow bestätigter Status** zu behandeln, nicht als „Wahrheit“ und nicht als Mehrheitsautomatismus. Bei `NO_CANDIDATE` verbleibt ein terminales `NO_GO` samt Negativledger ohne automatischen Neustart.

## 6. R18-R2 Forschungsdesign — präregistrierbare Vergleichsarme, NICHT ausgeführt

**Nullhypothese:** SAC oder andere Koordination steigert unter gepaarten Aufgaben und gleichwertigen Ressourcen weder Korrektheit noch geschützte Integrität gegenüber dem besten eingefrorenen Einzelagenten; potenzielle Mehrkosten und Fehlerkorrelation können eine Verschlechterung ergeben. Jede Architektur, auch `NO_COLLABORATION`, darf gewinnen.

### Kontrollarme

- `A0_SINGLE`: stärkster spezifizierter Einzelagent ohne Kommunikation; gleiche Antwort- und Ressourcenbudgets.
- `A1_INDEPENDENT_VOTE`: getrennte feste Erst-Antworten, keinerlei gegenseitige Kontextexposition.
- `A2_CP_WBFT_SELF`: Originalbaseline mit manipulierbarer Senderkonfidenz, unter klar definiertem Angreifer.
- `A3_CP_WBFT_EXTERNAL`: nur sofern echte, extern kalibrierte und vom Sender nicht manipulierbare Probes vorhanden sind; sonst `NOT_TESTED`.
- `A4_SAC`: offizielle Papersemantik, Versions-/Lizenz- und Implementierungsgrenzen gekennzeichnet. Ohne Lizenzfreigabe ausschließlich clean-room Schema-/algorithmische Beschreibung, keine Codekopie.
- `A5_SHAM`: synthetische Negativkontrolle, zufällige/unabhängig geshuffelte Peer-Nachrichten, um bloße Kontextvolumeneffekte abzuschätzen.

### Faktoren und Paired-Outcomes

Taskfamilie, Datenquellenherkunft, Kompetenzprofil, zugänglicher Ground Truth, Agentenzahl, Modellfamilie, Prompt-Pin, Seed, Topologie, F-lokale Angreiferzahl, tatsächliche Kosten (Inference-/Transport-/Wartezeit), Runden, Antwortverfügbarkeit; Angreiferarten `SELF_CONFIDENCE_FAKE`, `PERSUASION`, `SELECTIVE_RAG`, `PROMPT_INJECTION`, `COMMON_MODE_ERROR`, `SYBIL_COLLUSION`, `PARTITION_TIMEOUT`, `STALENESS/REPLAY`. Sybil-Fälle sind **außerhalb** unbelegter Identity-Bounds; als separater Stressfall, nicht als heimlicher SAC-Theoremswiderspruch. Jede Konfiguration erhält eine eigene Fixture-ID und einen Anspruchsscope.

**Primär:** gepaarte Differenz der korrekt beantworteten Aufgaben unter *gesonderter* `STRONG_GROUP_FINAL_CORRECT`-Population, ergänzt durch False-Verified-/Source-Misattribution-Rate als harte Fehlergrenze. **Sekundär:** `GLOBAL_BFTI_PP`, `RA`, `H_MAJORITY`, `ABSTAIN_RATE`, `SAFETY_FAILURE`, `LIVENESS_FAILURE`, `TIME_TO_RESUME`, `CORRELATED_ERROR_N_EFF`, `TOOL_BYTES`, `TOKENS`, `ENERGY` nur bei tatsächlichen Messquellen. Alle Ausfälle bleiben im Nenner. Block-/Task-Clusterstatistik; keine Pseudoreplikation von 7 Agenten × 6 Runden als 42 unabhängige Aufgaben. A-priori-Margins, Sample-Power, Analyseplan und Zielpopulation erst nach offenem Pilot und Operator-Freigabe festschreiben; keine erfundenen Zahlen.

**Kausale Restriktion:** Selbst formal konsistente Protokollzustände können semantisch falsch sein. Wenn kein unabhängiger Truth-Orakel existiert, ist die Ergebniskategorie `NO_GROUND_TRUTH/NOT_SCORED`; weder Konsens noch Expertenmehrheit liefern automatisch ein solches Orakel.

## 7. Lokal ausgeführte C1-Vertragsprobe R2 — und ihre Grenzen

Der statische Evaluator-Vertrag `test_r18_r2_frozen_contract.py` wurde vor der separaten Implementierung `r18_r2_boundary_contract.py` verfasst. Standard-Python, keine Drittanbieterimporte. **14/14 Tests PASS**, darunter eine parametrische Sammlung mit **23 expliziten Fehlersituationen** (diese 23 Unterfälle sind **keine** zusätzlichen unabhängigen `unittest`-Testmethoden). Eine ausdrücklich manipulierte Variante ohne den direkten `integrity=FAIL`-Veto-Zweig erreicht **12/14 Tests**, mit genau den erwarteten 2 roten Prüfungen.

Prüfthemen: fehlender Body-Hash/Version, Quellenstatus, Korrektheits-/Integritätsveto, unbekannte Beweisstärke, gleiche Generator-/Judge-ID, fehlende hypothetische Authentisierung, geteilter Credential-Scope, Baseline-/Korrelations-/Liveness-Gaps, Operator-HOLD, synthetische `n_eff`-Arithmetik sowie `BFTI` in Prozentpunkten. **Die Booleans `authenticated=True`, `BYTE_VERIFIED` usw. in den Fixtures sind erfundene Testdaten und führen keinerlei echte Quellen- oder Identitätsprüfung durch.** Selbst eine vollständig „grüne“ synthetische Fixture liefert nur `RESEARCH_ELIGIBLE_ONLY`, niemals Ausführungserlaubnis.

Nicht durchgeführt: echter SAC-/CP-WBFT-Modelllauf, eigene Studie, realer Generator, fremd-authentisierter Judge, Third-Party-Oracle, produktive R18-Node-Ausführung, echter K7-HTTP-Rohbody-Audit, Sigstore-Logeintrag, Penetrationstest, echte Kosten-/Energiemessung. Die R2-Test- und Mutantenergebnisse gehören eindeutig zum **lokalen AXIOM-Forschungsprototyp**.

## 8. Kanonische Evidenz- und Autoritätsentscheidung

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_ADVERSARIAL_ONLINE_DEEP_RESEARCH_FOUNDATION_20261018_R2
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_R2_ESTABLISHED
PARENT_R18_R1 = IMMUTABLE_PRESERVED_SHA256_08b51af99c973c2fb86b49ccea989be587ca52844674b925438b681e338f527d
R18_R1_STACK_BYTES = 98547
R18_R1_STACK_CRC = PASS
SAC_PRIMARY_V1_V2 = CONTENT_SCOPED_RECHECKED
SAC_V3 = SECONDARY_INDEX_INDICATION_NOT_PRIMARY_BODY_VERIFIED
SAC_LICENSE = MIT_CLAIM_IN_README_ROOT_LICENSE_FILE_ABSENT_REUSE_HOLD
CORRELATED_PANEL_RISK = SUPPORTED_BY_EXTERNAL_2026_RESEARCH
SAC = PRIORITY_EVALUATION_CANDIDATE
SAC_PRODUCTION_SELECTION = NOT_ESTABLISHED
K7_RAW_HTTP_BODY_AUDIT = INCOMPLETE
EXTERNAL_INDEPENDENT_VALIDATOR = NOT_ESTABLISHED
R18_R2_SYNTHETIC_RESEARCH_CONTRACT = 14_OF_14_PASS
R18_R2_INTEGRITY_MUTANT = 12_OF_14_PASS_2_EXPECTED_FAILURES
R18_EMPIRICAL_NEXUS_SYSTEM_VALIDATION = NOT_PERFORMED
R18_47_CONDITIONS = DRAFT_PENDING_OPERATOR_RATIFICATION
R18_SHADOW_LOOP = HOLD_NO_START
R18_EXPERT_EXECUTION = NOT_AUTHORIZED
HUMAN_STUDY = NOT_PERFORMED
RUNTIME_CHANGE = NO
HOSTINGER_WRITE = NO
CLAIM_PROMOTION = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

**Abschluss auf Forschungsebene:** Der Grundlagenscope ist umfangreicher und falsifikationsfähiger. Das Ergebnis darf als R18-R2 Forschungsnachtrag publiziert werden, **nicht** als abgeschlossene experimentelle Validator-Trennung, BFT-Sicherheitsnachweis, R18-Ratifizierung oder operativer Shadow-Start.

## 9. Quellen und Beleggrenzen

1. Lee et al., *Robust Multi-Agent LLMs under Byzantine Faults*, arXiv:2605.09076v1 — https://arxiv.org/html/2605.09076v1 (v1 MATH30, eigene historische Tabellen).
2. Lee et al., arXiv:2605.09076v2 — https://arxiv.org/html/2605.09076v2 (v2 MATH100 und Commonsense30, Scorefunktion `phi_i`, `(F+1)` Graphannahme).
3. SAC Autoren-README, Commit `2ef7061590d0968ea4bd19f82b8d7ddde8f2bb89` — https://github.com/daniel-eai/Robust-Multi-Agent-LLMs-under-Byzantine-Faults/blob/2ef7061590d0968ea4bd19f82b8d7ddde8f2bb89/README.md (MIT-Behauptung, kein GitHub-SPDX/Root-LICENSE).
4. Zheng et al., *Rethinking the Reliability of Multi-agent System*, arXiv:2511.10400 — https://arxiv.org/abs/2511.10400 (eigener CP-WBFT-Versuchsscope).
5. Kohli (2026), *Nine Judges, Two Effective Votes* — https://machinelearning.apple.com/research/correlated-llm-evaluation-panels ; https://arxiv.org/abs/2605.29800 (N_eff unter korrelierten Fehlern).
6. Berdoz, Rugli, Wattenhofer (2026), *Can AI Agents Agree?* — https://arxiv.org/abs/2603.01213 (Safety und Liveness).
7. Kraidia et al. (2026), *When collaboration fails*, Scientific Reports — https://www.nature.com/articles/s41598-026-42705-7 (adversarielle Persuasion; kein direkter SAC-Benchmark).
8. Kim et al. (2026), *Capable language models can outgrow the benefits of collaboration*, Nature Machine Intelligence — https://www.nature.com/articles/s42256-026-01268-y (Einzelagenten-Nutzen und Koordinationskosten).
9. Pitre et al. (2026), *A Diagnostic Study of Multi-Agent LLMs*, ICML/PMLR — https://proceedings.mlr.press/v306/pitre26a.html (Prozessdiagnostik statt Mehrheitsproxy).
10. SAFER, ICLR 2026 — https://proceedings.iclr.cc/paper_files/paper/2026/hash/582e9771ac8527cb6390e5e9444a0fee-Abstract-Conference.html (Abstentions-/Risikokontrollmethodik).
11. Bai & Jin (2026), SCoRE — https://arxiv.org/abs/2603.24704 (selektive Vorhersage mit Risikokontrolle; Voraussetzungen beachten).
12. OWASP LLM01:2025 Prompt Injection — https://genai.owasp.org/llmrisk/llm01-prompt-injection/ (untrusted content ≠ instructions).
13. SLSA v1.2 Source/Build Tracks — https://slsa.dev/spec/v1.2/tracks und https://slsa.dev/spec/v1.2/source-requirements (Provenienz ≠ Semantik).
14. Sigstore Security Model — https://docs.sigstore.dev/about/security/ und https://docs.sigstore.dev/logging/overview/ (Log-Witness/Monitor und Trust Roots).
15. gittuf forge-unabhängige Git-Sicherheits-Policy — https://github.com/gittuf/gittuf ; beta, Designreferenz.
16. Apalache TLA+/Quint bounded Model Checking — https://github.com/apalache-mc/apalache ; Designreferenz.
17. OpenTelemetry GenAI Semantic Conventions — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (Datenschutz-/Opt-in-Anforderung für Inhalte).
18. Historischer NEXUS R18-R1 Elterndatensatz — `/mnt/data/NEXUS_OMEGA_AXIOM_R18_INDEPENDENT_DEEP_RESEARCH_FOUNDATION_20261018_R1.zip`, exakter SHA oben; offline lokal, nicht neue wissenschaftliche Primärmessung.

Alle externen Zahlen bleiben an ihre jeweilige Autorenschaft, Stichprobe und Publikationsversion gebunden. Weniger glaubwürdige Sekundärquellen dienen höchstens als Versionshinweis/Analogie und dürfen keine neue numerische Kernbehauptung tragen.

`SOURCE ≠ TRUTH · GENERATOR ≠ JUDGE · AGREEMENT ≠ CORRECTNESS · PROXY ≠ GROUND_TRUTH · EVIDENCE > AGREEMENT · HUMAN_AUTHORITY_PRESERVED`
