# R44-5 R1 · Chat-transmission snapshot of the canonical order — receiver-published additive commit

PUBLISHED_AT = 2026-11-24 (Europe/Berlin)
PUBLISHED_BY = OFFCHAIN_UNREGISTERED_ADVISORY_C1 receiver, at explicit operator chat instruction:
               "R44-5 MAXIAUFTRAG starten. Anschließend den Vollständigen Stack von R44-5 zur verfügung stellen [Plugin:github]"
PARENT_BINDING = Issue #439 / Draft PR #440 / branch axiom/r44-5-operator-start-binding-20261124-c1 head 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a
OBJECT = NEXUS_OMEGA_AXIOM_R44_4_TO_R44_5_GITHUB_IMPLANT_BODYTWIN_EVIDENCE_BRIDGE_RESEARCH_ORDER_20261124_R1
SCOPE = The text below is the verbatim chat transmission of the AXIOM document
        "AXIOM — R44-4 Abschluss und R44-5 Experten-MAXIAUFTRAG" (NEXUS OMEGA, 24. November 2026).
        Layout of highlighted statistic blocks is normalized to plain lines; every number and wording is preserved as transmitted.
        The operator-custodied R44-5 R1 ZIP (11 files, 33,427 B, ZIP SHA-256 303a4761580dcbaa604e6e723bc8972d215f6660b86488fa8e4b57a76f541b67,
        manifest 10/10 MATCH as reported) is NOT_OBTAINED by the receiver. Its original bytes remain PENDING_OPERATOR_UPLOAD
        and are NOT reconstructed, paraphrased or substituted here (per Issue #439: "Der Stack wird NICHT rekonstruiert oder paraphrasiert").
NO_CURSOR_HANDOFF = TRUE ; EXPERT_ACK = NOT_RECEIVED ; PR_MERGE = NO ; CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

---

# AXIOM — R44-4 Abschluss und R44-5 Experten-MAXIAUFTRAG

NEXUS OMEGA · 24. November 2026 · Kanonischer Forschungsanschluss

Das nachgeforderte GLM-ZIP liegt vollständig vor. Damit können wir die bisherige Kustodielücke schließen und R44-4 als administrativen Forschungscheckpoint abschließen, ohne offene wissenschaftliche Gates künstlich auf PASS zu setzen.

## 1. Unabhängige Abschlussprüfung des GLM-Arbeitsstacks

Originalmanifest: **141/141** SHA-256 MATCH
Fehlende Manifest-Mitglieder: **0** — Kustodielücke geschlossen
Archivintegrität: **PASS** — ZIP CRC fehlerfrei
Erhaltene Dateien: **283** (141 unterschiedliche Dateihashes)

Archiv: `R44-4_~1.ZIP`

```
BYTES = 1478570

SHA256 =
9bd62223f43a536077b795c91e04b8152a4100b9fc5fcddde05409a15a1f88b3

MANIFEST = 141_OF_141_MATCH
MISSING_ORIGINALS = 0
CRC = PASS
```

Das Archiv enthält sowohl den Arbeitsstack als auch Kopien im separaten Evidenzverzeichnis. Die 283 Dateien werden deshalb nicht als 283 unabhängige wissenschaftliche Beiträge gezählt.

## 2. Tatsächliche Prüfung der GLM-Ledger

Erstmals liegen die ursprünglichen Receipt- und Lease-Dateien vor. Sämtliche Einträge wurden eigenständig gehasht und ihre Verkettung gegen den mitgelieferten Anker geprüft.

| Prüfgegenstand                             | AXIOM-Ergebnis       |
| ------------------------------------------ | -------------------- |
| Receipt-Ledger                             | 30 Einträge          |
| Strikt kanonisch serialisiert              | 29/30                |
| Hash in gespeicherter Schlüsselreihenfolge | 30/30 MATCH          |
| Verkettung                                 | 30/30 MATCH          |
| Lease-Ledger                               | 249/249 Hashes MATCH |
| Anzahl und Endhash beider Ledger           | MATCH                |
| Skripthashes der Receipt-Einträge          | Alle MATCH           |
| Präregistrierung R1 und R2                 | Beide Hashes MATCH   |

Der von GLM offengelegte Serialisierungsdefekt in `seq 3` wurde bestätigt. Ebenso konnte verifiziert werden, dass der Korrektureintrag `seq 11` dieselben Beobachtungsdaten enthält und exakt auf den ursprünglichen Eintrag verweist.

Das ist ein wichtiger Unterschied zur vorherigen Adjudikation: Der Fehlermechanismus ist nun nicht mehr nur plausibel, sondern anhand der tatsächlich erhaltenen Originaldateien nachgewiesen.

Der strikte Ledger-Status bleibt trotzdem `FAIL_SEQ3`. Die Korrektur darf den historischen Defekt nicht rückwirkend auslöschen. Auch der mitgelieferte Ledger-Anker ist noch kein Beweis für eine unabhängig verwahrte, zeitlich unveränderliche Versiegelung.

**GLMs konstruktive Fehleroffenlegung hat sich bei der unabhängigen Byteprüfung bestätigt.**

## 3. Zusätzlicher fundamentaler Befund — GLM-Statistik

Durch die nachgereichten Originalskripte konnte ein weiterer methodischer Fehler eindeutig lokalisiert werden.

Die Funktion `pvalue_minlike` in `expB/run_B.py` behauptet, denselben exakten zweiseitigen Binomialtest wie SciPy abzubilden. Tatsächlich implementiert sie jedoch die verdoppelte Randwahrscheinlichkeit.

| Prüfgröße                        | Ergebnis       |
| -------------------------------- | -------------- |
| AXIOM-Gegenbeispiel              | N = 50, k = 47 |
| Nullhypothese                    | p = 0,95       |
| GLM-Testdefinition               | 0,918934       |
| SciPy-Wahrscheinlichkeitsordnung | 0,738899       |
| Differenz                        | 0,180035       |

Auch GLMs eigene Originaldatei `B_cells.json` dokumentiert diese maximale Abweichung.

**Der Fehler liegt somit nachweislich in der Gleichsetzung zweier unterschiedlicher statistischer Testverfahren.**

Die zuvor von AXIOM nachgerechneten Mindeststichproben bleiben für ihre jeweils definierte Testmethode gültig.

Dieser Befund wird dauerhaft als `CR-04_EQUAL_TAIL_MISLABELLED_PROBABILITY_ORDER` in R44-5 aufgenommen.

Für BodyTwin ist das besonders relevant: Es muss nicht nur das physikalische Modell und seine Parameter falsifiziert werden, sondern ebenfalls die statistischen Instrumente, mit denen seine Güte beurteilt wird.

## 4. R44-4 — Kanonischer Abschluss (administrativ)

| Evidenzebene                 | Abschlussstatus    |
| ---------------------------- | ------------------ |
| QWEN-Return-Integrität       | 50/50 MATCH        |
| GLM-Originalmanifest         | 141/141 MATCH      |
| FDA- und UCI-Originalproben  | SHA-256 MATCH      |
| GLM-Lease-Hashintegrität     | 249/249 MATCH      |
| GLM-Receipt-Serialisierung   | FAIL_SEQ3 erhalten |
| Unabhängige GLM-Reproduktion | NOT_RUN            |
| Wissenschaftliche Vollgates  | 0/10               |
| Authentifiziertes Quorum     | 0/3                |
| Claim Ceiling                | C1                 |

R44-4 wird nicht erneut administrativ geöffnet. Die noch offenen wissenschaftlichen Forschungsgegenstände werden kausal an R44-5 weitergegeben.

## 5. R44-5 — Aktualisierter Experten-MAXIAUFTRAG R1

Der bisherige R0-Auftrag und der GLM-Nachtrag bleiben unverändert versiegelt. R1 konsolidiert beide und integriert die vollständige GLM-Abschlussprüfung.

Die Experten erhalten folgende priorisierte Forschungsstruktur:

**Priorität P0 — Fundament und Quellenzugang**

- **F01 · GitHub-Implant-Evidenzbrücke**: Cursor-unabhängige Quellenbeobachtung, Feed-Frische, Originalbyte-Parität und zuverlässiger Quellenzugang für sämtliche Experten.
- **F02 · Kanonische Ledger-Integrität**: Deterministische Serialisierung, unabhängig verwahrte Hash-Anker, Append-only-Korrekturen und strikte Fail-closed-Prüfung.
- **F03 · Originalquellen und Provenienz**: Gepinnte NELFP- und Fisher-Artefakte, FDA-/UCI-Quellen sowie verpflichtender Source-Access-Preflight.

**Priorität P1 — Wissenschaftliche Vertiefung**

- **F04 · Authentifizierung und Erkenntnisunabhängigkeit**: GLM-Testvektoren, QWEN-KeyID-Alias-Befunde, synthetische Trust-Root-Prüfung und unabhängige Akteuridentität.
- **F05 · Mathematische BodyTwin-Falsifikation**: Fisher-Identifizierbarkeit, Whitening, Sensorkorrelation, nichtlineare Schätzung, Prior-Robustheit und exakte statistische Testplanung.
- **F06 · Ressourcen und Evidenzproduktivität**: Vollständige Erfassung von Prozessbaum, Netzwerk, Cache, Retries, CPU und Tokens. Keine Effizienzbehauptung bei fehlenden Kostenwerten.
- **F07 · Konstruktive Capability-Isolierung**: Familie D: gezielte Sperrung fehlerhafter Funktionen bei fortgesetzter, autorisierter Forschungsarbeit. Ausschließlich kontrollierte synthetische Umgebung.

## 6. Aktualisierte Forschungsumgebung (Struktur, wie im Chat übertragen)

- NEXUS OMEGA · AXIOM: Governance · Quellenbindung · Adjudikation
- NEXUS GitHub Implant: Read-only · Transport · Quellenzugang · Frischeprüfung
- Experten E27, E28, E29, E30, E31, E32, E33, E34
- Isolierte Forschungs-Sandbox: Eigenständige Experimente · Gegenhypothesen · RED/GREEN
- Ledger: Transport-Ledger · Ausführungs-Ledger · Ressourcen-Ledger · Evidenz-Ledger
- AXIOM → Operatorentscheidung: Unabhängige Prüfung · Kein automatischer Claim-Aufstieg

## 7. Vollständiger Expertenauftrag — versiegelt

**NEXUS OMEGA R44-5 — MAXIAUFTRAG R1**: 11 Dateien · 33.427 Bytes · 10/10 Manifest MATCH · Versiegelt

ZIP-SHA-256: `303a4761580dcbaa604e6e723bc8972d215f6660b86488fa8e4b57a76f541b67`

Das Paket enthält:

- Vollständig konsolidierten Experten-MAXIAUFTRAG R1.
- Aktualisierten maschinenlesbaren Forschungsvertrag.
- GLM-Abschlussreceipt mit 141 einzelnen Quellenzuordnungen.
- GitHub-Implant-Architektur und Testdesign.
- 28 vorgesehene Positiv-/Negativkontrollen.
- Standardisiertes Experten-Return-Schema.
- AXIOM-Nachrechnungen und ausführbares Rehash-Prüfskript.
- Kanonische Vorgängerbindung und SHA-256-Manifest.

Die ZIP-Integrität und sämtliche Manifest-Einträge wurden nach der Erstellung erneut geprüft. Das Rehash-Skript wurde zusätzlich unter `python -O` ausgeführt.

## 8. HARD — Kanonischer Übergabestatus

```
OBJECT =
 NEXUS_OMEGA_AXIOM_R44_4_TO_R44_5_
 GITHUB_IMPLANT_BODYTWIN_EVIDENCE_BRIDGE_
 RESEARCH_ORDER_20261124_R1

R44_4 = ADMINISTRATIVE_CHECKPOINT_CLOSED
R44_4_GLM_CUSTODY = COMPLETE_141_OF_141

GLM_STRICT_RECEIPT_CHAIN = FAIL_SEQ3_PRESERVED
GLM_LEASE_HASHES = 249_OF_249_MATCH
GLM_ORIGINAL_EXPERIMENT_REPLAY = NOT_RUN

R44_5_R0 = PRESERVED
R44_5_GLM_ADDENDUM = PRESERVED
R44_5_R1 = SEALED_RECEIVER_READY
R44_5_EXECUTION = NOT_STARTED

EXPERT_MANDATES = E27_TO_E34
GITHUB_IMPLANT_RESEARCH = INTEGRATED
FALSIFIER_DESIGNS = 28

CANONICAL_NEGATIVE_TESTS = 0_OF_24
AUTHENTICATED_QUORUM = 0_OF_3
FULL_SCIENTIFIC_PASSES = 0_OF_10

BODYTWIN_VALIDATED = NO
PHYSICAL_14_GATES = HOLD
ALT_D_DO_NOT_RUN = ACTIVE
E23_PRIVACY = HOLD
W1 = OPEN
B01_B05 = OPEN

CURSOR_ACTION = NONE
GITHUB_WRITE = NO
PR_MERGE = NO
HOSTINGER_WRITE = NO
WWW_WRITE = NO

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO

NEXT =
 OPERATOR_START_R44_5_EXPERT_RESEARCH
```

**Abgrenzung:** Der R5-Vorschlag wurde als R44-5 verstanden. Der Auftrag ist vollständig aktualisiert, lokal versiegelt, aber noch nicht auf GitHub eingestellt oder an die Experten versendet worden. Die unabhängige experimentelle Reproduktion bleibt Gegenstand der kommenden Runde.

**R44-4 abgeschlossen. R44-5 R1 vorbereitet.**

Die Ergebnisse, Fehler und Gegenbeweise bleiben im Fundament erhalten. Die nächste Runde kann auf den Start hin wissenschaftlich darauf aufbauen.

Operator-Direktive (Chat 2026-11-24): "NEXUS Ω OMEGA - R44-5 MAXIAUFTRAG starten. Anschließend den Vollständigen Stack von R44-5 zur verfügung stellen [Plugin:github]"
