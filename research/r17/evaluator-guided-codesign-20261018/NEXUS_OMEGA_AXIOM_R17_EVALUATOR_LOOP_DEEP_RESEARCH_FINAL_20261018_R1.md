# NEXUS OMEGA — R17 Evaluator-Guided Co-Design: wissenschaftliche Tiefenrecherche und kanonische Fundamentierung R1

**Stand:** 18.10.2026 · **Objekt:** `NEXUS_OMEGA_AXIOM_R17_EVALUATOR_GUIDED_CO_DESIGN_FINAL_SCIENTIFIC_RESEARCH_20261018_R1`

```text
CLASS = INDEPENDENT_PRIMARY_LITERATURE_AUDIT + ADVERSARIAL_DESIGN_REVIEW + SYNTHETIC_GUARD_FALSIFICATION
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_SUBSTANTIVELY_COMPLETE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PARENT = R17_EVALUATOR_GUIDED_LLM_QUANTUM_CIRCUIT_CO_DESIGN_SYMBIOSIS_FOUNDATION_20261018_R0
R18 = FOLLOW_ON_DESIGN_PROPOSALS_DRAFT_PENDING_OPERATOR_RATIFICATION
RUNTIME = FROZEN
GENERATIVE_LOOP_STARTED = NO
QUANTUM_COMPUTING_EXECUTED_BY_NEXUS = NO
HUMAN_STUDY = NO
CLAIM_PROMOTION = NO
```

## 0. Herkunft, Umfang, strikte Originaltrennung

Sieben am 18.10.2026 vom Operator gelieferte Originaldateien wurden physisch gelesen und mit SHA-256 geprüft. Die Originale sind nicht durch diesen Nachfolgebericht überschrieben. Intake-Namen, Bytes und Hashes sind im beiliegenden `intake_manifest.json` dokumentiert. Die drei Dateien mit Endung `.DOC` sind technisch **OOXML-DOCX-Dateien**, keine alten binären Word-97-Dokumente. Ihre XML-/Tabelleninhalte wurden strukturiert gelesen; kein versteckter redaktioneller Konsens wird aus gleichlautenden Agenten-Returns abgeleitet.

- **R17 R0** ist die eigentliche Gegenstandsforschung: LLM schlägt vor, externes deterministisches Programm bewertet, mehrere Kandidaten und Ressourcenkonflikte. Autorisierung nur `RESEARCH_ONLY`.
- **R18 R0** priorisiert Unabhängigkeit, Fail-Closed, Pareto, Negative Evidence. Es ist ein Nachfolge-*Vorschlag*, kein Bestandteil eines automatisch legitimierten R17-Ergebnisses.
- **R17/R18 Quellensynthese R1** fügt methodische und organisatorische Spezifikationsforderungen hinzu.
- **R18 DOC v1** sagt `K7–K12 ACCEPTED`; diese von einer Generatorinstanz formulierte bindende Entscheidung ist epistemisch/organisatorisch unzulässig.
- **R18 DOC v2** korrigiert ausdrücklich auf `DRAFT_PENDING_OPERATOR_RATIFICATION_C1` (`K13–K18`) und behält die bisherige v1 als historische Quelle bei. Diese Korrektur ist zu erhalten.
- **R18 D1–D8** liefert konkrete theoretische Abnahmeschemata, aber **keinen Nachweis einer abgeschlossenen Prüfung oder Operatorratifikation**; nach eigener Deklaration bleiben Hash-Bindungen offen.

Die bereits gebundenen R9–R16-Forschungs-/Ausführungslanes werden nicht neu definiert. Ebenso wenig darf die bestehende `research/r17/axiom-mind-module-20261012`-Lane überschrieben werden; für R17 Co-Design ist ein anderer registrierter Pfad notwendig.

## 1. Wissenschaftliche Primärquellen — genaue Reichweite

### 1.1 Anthropic / Harvard, 15.–16.10.2026

**Primärtext 1:** Gu, Kemeny, Yelin, Lukin (2026), *Discovering state-of-the-art quantum circuits with large language models*, arXiv:2610.22367, eingereicht 15.10.2026. https://arxiv.org/abs/2610.22367

**Primärtext 2:** Anthropic Science (16.10.2026), *Designing more efficient quantum circuits with Claude*. https://www.anthropic.com/research/designing-efficient-quantum-circuits

Beide URLs wurden über Webzugriff am 18.10.2026 inhaltlich gelesen. Autor, Titel, Veröffentlichungsdaten und untersuchte Aufgaben sind nachvollziehbar. **Wichtig:** Hier liegt *kein eigener lokaler Roh-HTTP-Body mit Status-/Content-Type-/SHA256-Protokoll* vor. Für den verschärften R18-K7-Auditstatus gilt daher `SOURCE_AUDIT=PARTIAL`, nicht `BYTE_VERIFIED`. Sekundärschriften oder bloße Online-Lesbarkeit schließen die K7-Transport-/Byte-Lücke nicht.

Kernbefunde im begrenzten Originalscope:

1. **Acht** spezifische, als klassisch berechenbare Funktionen eingebettete Quantum-Circuit-Primitiven wurden mittels LLM-Vorschlägen und handgeschriebener evaluatorseitiger Prüfung untersucht; **sieben von acht** zeigten Reduktion sowohl in Toffoli- als auch Qubit-Kosten relativ zu den gewählten Referenzen. Die achte Aufgabe führt zu einer neuen reversiblen Modularinversions-Architektur auf einer Ressourcen-Paretofront.
2. **53 Stunden** betreffen einen konkreten langen Suchlauf mit *wenig*, nicht notwendigerweise *null*, menschlicher Mitwirkung; laut Anthropic erfolgten gelegentliche Aufforderungen, breiter zu explorieren. Nicht als allgemeine Betriebsautonomie für NEXUS verallgemeinern.
3. **17× weniger Gatter und ca. 12 % mehr Qubits** ist ein spezifischer Vergleich mit einer bestimmten zuvor qubitsparenden Konstruktion. Das belegt weder 17× bessere reale Laufzeit noch Pareto-Dominanz in **beiden** Achsen für diesen Punkt.
4. Das **ungefähr 12×** Gatterergebnis bezieht sich auf einen bestimmten Reed–Solomon-Decoder als DQI-Subroutine, **nicht** die gesamte Quantum-Hardware, die Gesamtdauer von DQI oder alle Dekoderverfahren.
5. Einzelne mathematische Identitäten und Korrektheitsargumente wurden nach Simulation **in Lean formalisiert**; das ist nicht gleichbedeutend mit einem maschinenverifizierten Beweis sämtlicher veröffentlichter Circuit-Designs oder quantenphysikalischer Ausführung.
6. **Materiell für R17:** Die Arbeit lässt ein kontrolliertes Fehlerrisiko bei begrenztem Fehlerbudget zu: der DQI-Decoder hat für die knapp bemessene History-Speicherung einen seltenen Zweit-Stack-Fall von etwa `1e-4` in der beschriebenen Inputverteilung; bei der Modularinversion werden weitere seltene Lauf-/Speichergrenzen beschrieben. Die Wahl ist **domänenspezifisch legitimierbar**, für NEXUS Integritäts- oder Sicherheits-Vetos jedoch kein automatisch zulässiges Modell.
7. Der Ansatz beschränkt die effiziente Korrektheitsprüfung auf **eine besondere Klasse** von Circuit-Funktionen: bei beliebigen Quantum-Circuits kann klassische Simulation weiterhin exponentiell teuer sein. Daraus folgt kein universelles `LLM + deterministic evaluator`-Rezept für unentscheidbare oder schlecht spezifizierte Forschungsfragen.

### 1.2 Externe triangulierende Primär- und Methodenquellen

- **FunSearch** (Romera-Paredes et al., *Nature* 2023), https://www.nature.com/articles/s41586-023-06924-6: evolutionäre Programmsuche unter algorithmischem Evaluator; unterstützt das Grundmuster, nicht R17-Wirksamkeit.
- **AlphaEvolve** (Novikov et al., 2025), https://arxiv.org/abs/2506.13131 und https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/: Programmvorschläge und Feedback an prüfbare Optimierungsaufgaben. NEXUS darf nicht implizit behaupten, die veröffentlichten Google-Ergebnisse zu reproduzieren.
- **LLM-as-Judge Bias** (Shi et al., IJCNLP-AACL 2025), https://aclanthology.org/2025.ijcnlp-long.18/: positionsabhängige Evaluator-Verzerrungen in umfangreicher Analyse. **Multi-Agenten-Einigung allein ist keine unabhängige sachliche Validierung**.
- **Multi-Agent Bias Amplification** (Ma et al., EMNLP Findings 2025), https://aclanthology.org/2025.findings-emnlp.941/: manche Debatten-Setups verstärken Verzerrungen. Externe Expertenanzahl ersetzt harte Prüforakel nicht.
- **NIST AI RMF Measure** https://airc.nist.gov/airmf-resources/airmf/5-sec-core/: unabhängige Prüfer, dokumentierte TEVV-Testmengen und Abgleich mit Einsatzkontext relevant.
- **in-toto** https://in-toto.io/ und **SLSA Provenance v1.2** https://slsa.dev/spec/v1.2/provenance: optional vergleichbare Schema-/Signaturgrundlagen für Produzenten-, Prüfer- und Materials-Ledger; kein installierter NEXUS-Pflichtdienst.

## 2. Wesentliche epistemische Grenze: Was zählt als „unabhängiger Judge“?

Ein *deterministischer* Prüfer ist nicht zwingend *unabhängig* und ein *unabhängig ausgeführter* Prüfer ist nicht automatisch *sachlich korrekt*. Drei getrennte Ebenen sind deshalb erforderlich:

- `INDEPENDENT_ACTOR`: separate authentifizierte Konten/Rechte, keine Generator-Rechte an Evaluator, Frozen Oracle und Ledger.
- `INDEPENDENT_METHOD`: vorab eingefrorene, selbstständig überprüfbare Prüfstrategie mit Gegenbeispielen; übertragene Agenten-Selbstaussagen zählen nicht.
- `VALIDITY_SCOPE`: expliziter Geltungsbereich des Prüfverfahrens — Beweis, Exhaustion, statistischer Test, Analogie oder unbestätigte Behauptung.

Ein SHA-256-Hash belegt ein Byteobjekt, nicht die wissenschaftliche Richtigkeit; ein Werkzeugname, Repo-Commit oder CI-Success belegt nicht eine extern authentifizierte wissenschaftliche Gegenprüfung. Generator-Testdaten dürfen keinen versteckten Einfluss auf das Frozen Oracle haben. Kandidatencode darf nur in isolierten, ressourcenbegrenzten Umgebungen laufen; Standard-Interpreter mit Zugriff auf Host-Filesystem/Netz sind kein sicherer Code-Sandboxersatz.

Der neue harte Klassifikator lautet:

```text
PROOF_LEVEL = FORMAL_PROOF | EXHAUSTIVE | BOUNDED_STATISTICAL | UNKNOWN
ERROR_BOUND = stated_scope + distribution + confidence/method + allowed_budget
INDEPENDENCE = ACTOR_ATTESTED AND EVALUATOR_PINNED AND HOLDOUT_FROZEN
C1_EVIDENCE_CLASS != CLAIM_PROMOTION
```

**Schärfung:** Selbst ein `FORMAL_PROOF`-Label genügt nicht; vor einer tatsächlichen wissenschaftlichen Freigabe ist ein überprüfbares Proof-Artefakt samt Validator/Trust-Base-Bindung notwendig. Der isolierte P0-Prototyp weiter unten verifiziert **keine echten Beweise oder Signaturen** und darf nicht als solcher ausgegeben werden.

## 3. R17/R18: materielle Widersprüche und präzise Remediationen

| Objekt / Defekt | AXIOM-Bewertung | Erforderliche Korrektur |
|---|---|---|
| R18 v1 `K7–K12 ACCEPTED` aus Generatorquelle | `CONTRADICTION_APPEND` | DRAFT v2 (`K13`) gilt als Nachfolgevorschlag, **nicht ratifiziert**; historische v1 unverändert halten |
| R18 `VERIFIED`-Quellenstatus ohne Rohantwort und Body-Hash | `HOLD_SCOPED_K7` | Feldgenauer, extern nachvollziehbarer Source-Audit; keine erfundenen Header/Bytes |
| R18 L1/L2: Hash ≠ getrennte Schreibrechte / identische Session-Credentials | `DESIGN_INCOMPLETE` | Executable Identity- und Write-Denial-Tests, Credentials **nie als Dump oder Klartext** ausgeben; nur nicht-sensitive Identitätsnachweise |
| R18 L4 „gleiche Eingabe + Environment-Pin“ | `DESIGN_SCOPE` | Prüfbare deterministische Verdicts unter identischen Pins, definierte Toleranz/Seed; deterministische Ergebnisse allein nicht gleich sachliche Wahrheit |
| R18 DQI-Zahlen als potenzieller 100-%-Korrektheitsbeleg | `NEEDS_SCOPE_REPAIR` | `BOUNDED_STATISTICAL`/Fehlerbudget vs `FORMAL_PROOF`; NEXUS-Integritätsachsen haben strengere Veto-Regeln |
| R18 Ledger allein hash-verkettet | `NOT_IMMUTABILITY_PROOF` | Ein Angreifer kann gesamte Kette neu berechnen oder einen Suffix löschen; unabhängig verankerter Checkpoint, Signaturen/Rechte/Retention sowie externer erwarteter Head+Count nötig |
| R18 `NO_DELETE` bei `PERMANENT` | `POLICY_CAVEAT` | Ein Feld **verhindert** weder Löschung noch erfüllt es Datenschutz-/Aufbewahrungsanforderungen; private Daten nicht ungeprüft permanent protokollieren |
| R18 `HOLD terminal until authenticated operator lift` | `STATE_NAMING_AMBIGUITY` | `HOLD_AUTH` bleibt verriegelt bis Operator, `EXIT_NOGO` ist endgültiger Laufabbruch; kein automatischer Zeitablauf oder Auto-Resume |
| Quantensystem-Reversibilität ≡ NEXUS Resume-Capsule | `ANALOGY_ONLY` | Physikalische/unitäre Umkehrbarkeit nicht mit dokumentiertem Software-Rollback oder Rekonstruktion verwechseln |
| Externe Agenten mit mehreren Stimmen | `NOT_JUDGE_ATTESTATION` | Agenten-Consensus nicht mit unabhängigem, autorisiertem, methodisch validen Prüfer gleichsetzen |

## 4. Falsifizierbare Forschungsarchitektur — begrenzter Schattenentwurf

```text
OPERATOR-approved frozen research spec
     -> generator (proposals, untrusted)
     -> immutable candidate bytes + lineage (no secrets)
     -> independent fixed schema/preflight [fail-closed]
     -> checker authority + evaluator pin + isolated process + frozen oracle
     -> correctness veto + integrity veto + classified proof strength
     -> multi-objective cost vector (only after veto)
     -> nondominated C1 research Pareto front
     -> operator decision or NO_GO
     -> append-only negative+positive ledger with external anchoring
```

Dazu wird **kein neuer Worker, kein R18-Shadow-Loop, kein Modellgewichtswechsel und kein reales NEXUS-Laufzeitsystem** gestartet. Die vom Operator noch nicht ratifizierten R18-Änderungsaufträge bleiben `DRAFT_PENDING_OPERATOR_RATIFICATION`. Ein *Forschungsbericht* darf publiziert werden; eine funktionsfähige autonome Evaluator-Engine darf daraus nicht abgeleitet oder gestartet werden.

**Lexikographische Veto-Reihenfolge:** (0) Scope/Quelle/Human Authority/Process Independence → (1) Korrektheit mit vorab festgelegtem erforderlichem Prüfniveau → (2) Integrität/Falsifikations-/Provenienzbedingungen → (3) Ressourcenkosten als Vektor statt Einzelproxy. Bei keinem Kandidaten: `EXIT_NOGO` und bewahrte Negativ-Evidenz. Bei mehreren nondominierten Kandidaten: keine automatische „beste“ Lösung, menschliche Outer Authority. `T×Q` ist im Quantum-Paper zulässiger Proxy für den dortigen Vergleich; im NEXUS-Kontext nicht die beste Gesamtmetrik.

### Harte Negativ-Fixtures

`F-ABSENT`, `F-CORRUPT`, `F-MISMATCH`, `F-LATE`, `F-WRONG-PROOF-LEVEL`, `F-GENERATOR-JUDGE-SHARED-IDENTITY`, `F-PROXY-REWARD-HACK`, `F-C2-AUTHORITY-PROMOTION`, `F-HIDDEN-HOLD`, `F-NO-CANDIDATE`, `F-LEDGER-TAMPER`, `F-LEDGER-TRUNCATION`, `F-UNAUTHENTICATED-ROLE-LIFT`, `F-UNPINNED-DEPENDENCY`.

## 5. Isolierter methodischer Prüfprototyp — tatsächliche lokale Ergebnisse

In der Arbeitsumgebung wurde **vor Implementation** der separate synthetische Prüfer `test_r17_integrity_guard_frozen.py` eingefroren (SHA256 `cd399bf0e521bdade486ba28cee5cb146ab5a0c73c4c79bede927c0c9a6e8a28`), danach erst `r17_integrity_guard.py` verfasst (SHA256 `53e749dc336604b2ebbd74b5f15e9f91e66b53109c8291a65e4b4d999a461ded`).

- Kandidat: **20/20** von der separat angelegten synthetischen Testsuite bestanden, Exit 0.
- Mutante: Aushebelung der Prüfniveauordnung (`PROOF_LEVEL`), Ergebnis **18/20**, zwei erwartete Falsifier aktiv (Test 08/09), Exit 1.
- Nachweise in `frozen_test_stdout.txt`, `mutant_failure_stdout.txt`, die Testquellen und separates Manifest.
- Methodengrenze: Beide Programme wurden vom gleichen AXIOM-Forschungsprozess verfasst; dies ist ein **vorab fixierter technischer Regressionstest, keine externe unabhängige Abnahme**. Die Eingabeflags `role_ratified` und `evaluator_independently_attested` sind synthetische Fixtures; das Programm validiert weder kryptografische Operator-Signaturen noch authentifizierte Actor-Register.
- Nur strukturierte Forschungsergebnisse `C1_ELIGIBLE_RESEARCH_ONLY`, `HOLD_*`, `SOURCE_GAP`, `EXIT_NOGO`. Kein tatsächliches `APPROVED_FOR_RUNTIME`/`C2`.
- Ledger-Demo überprüft Hash-Konsistenz und zeigt Änderung/Truncation innerhalb eines erwarteten Count/Anchors an. Sie beweist **keine** reale WORM-Speicherung oder externe Anker-Unveränderlichkeit.

**Wichtig:** Es wurde kein realer Quantum-Circuit-Algorithmus getestet, weder eine reale Agentenrolle noch die 53-Stunden-Suche reproduziert; die übernommene Primärarbeit bleibt **extern**.

## 6. Open-Source-Kandidaten: Referenz, nicht Pflichtabhängigkeit

| Kandidat | Eignung für NEXUS | Grenze |
|---|---|---|
| `algorithmicsuperintelligence/openevolve` (Apache-2.0) | Architekturvergleich: Fitness, Programmpopulation, Evaluationsfeedback, Diversitätsstrategien | Weder Evaluator-Identitäts-Isolation noch Lizenz-/Sandbox-/Cloud-/Providerfreiheit pauschal nachgewiesen; **nicht aktivieren** |
| `inter-co/science-codeevolve` (Apache-2.0) | Forschungsgegenprobe einer Open-Source-Entwicklungssuche | Keine zugesagte vollständige Oracle-/Credential-Isolation |
| `google-deepmind/funsearch` (Apache-2.0) | Grundreferenz für automatisierten Programmsucher mit Hard-Evaluator | Kein Drop-in NEXUS-Go oder Autonomie-Freigabe |
| `in-toto/in-toto` + SLSA v1.2 | Signierte Materials-/Steps-/Provenance-Designinspiration für reproduzierbare Buildketten | Verifizierte Herkunft ≠ Wahrheitsbeweis; Integrationsaudit separat |
| `leanprover/lean4` (Apache-2.0) | Optionaler Formalisierungs-Forschungspfad für **konkrete** Invarianten | Lean-Proof gilt nur für formal modellierte Aussage und Assumptions |
| `model-checking/kani` (Apache-2.0) | Begrenztes Model-Checking für Rust-Checker-Kerne, falls verfügbar | Eigene Spezifikation/Umgebung erforderlich, keine universelle Beweismaschine |

**Autonomiepräferenz:** minimaler lokaler stdlib-/GitHub-first Forschungsprüfkern ist gegenüber schweren verteilten Agentenframeworks vorzuziehen. Ein neues Framework ist hier kein Fortschrittsindikator. Kein Plugin oder Package wurde zur Laufzeit installiert oder aktiviert.

## 7. Schlussadjudikation und Übergang zur R18-Governance

```text
OBJECT = NEXUS_OMEGA_AXIOM_R17_EVALUATOR_GUIDED_CO_DESIGN_FINAL_SCIENTIFIC_RESEARCH_20261018_R1
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_RESEARCH_FOUNDATION_SUBSTANTIALLY_STRENGTHENED
SOURCE_PRIMARY_ANTHROPIC_ARXIV = CONTENT_RETRIEVED + SCOPE_CHECKED
K7_RAW_BODY_AUDIT = PARTIAL_NOT_BYTE_VERIFIED
R17_7_OF_8_EXTERNAL = SUPPORTED_FOR_QUOTED_DOMAIN
R17_53H_EXTERNAL = HUMAN_PROMPTS_OCCASIONAL_NOT_FULL_AUTONOMY
R17_17X_EXTERNAL = SPECIFIC_COMPARATOR_12_PERCENT_QUBIT_TRADEOFF
R17_BOUNDED_ERROR_EXTERNAL = EXPLICITLY_RESTORED
R17_NEXUS_QUANTUM_EXECUTION = NOT_EXECUTED
R17_SYNTHETIC_POLICY_PROBE = 20_OF_20_PASS
R17_SYNTHETIC_MUTANT = 18_OF_20_EXPECTED_FAIL
R17_EXTERNAL_INDEPENDENT_AUDITOR = NOT_ESTABLISHED
R18_R1_DRAFT = PENDING_OPERATOR_RATIFICATION
R18_SHADOW_LOOP = HOLD_NO_START
RUNTIME = FROZEN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

**Entscheidung:** Das R17-Fundament ist wissenschaftlich substanziell gestärkt und als *falsifizierbare Forschungsrichtung* zulässig. Die R18-Anschlussentwürfe sollen **nicht** durch AXIOM stillschweigend ratifiziert oder als laufendes System behandelt werden. Nächster sinnvoller Schritt ist eine **gesondert autorisierte, unabhängige Beweis-/Rollen-/Ledger- und Source-Audit-Runde**, nicht die Aktivierung eines automatischen Quantum-/Evolver-Loops.

`SOURCE ≠ TRUTH · GENERATOR ≠ JUDGE · DETERMINISM ≠ INDEPENDENCE · EVALUATOR_PASS ≠ FORMAL_PROOF · PROXY ≠ GROUND_TRUTH · HUMAN AUTHORITY PRESERVED`
