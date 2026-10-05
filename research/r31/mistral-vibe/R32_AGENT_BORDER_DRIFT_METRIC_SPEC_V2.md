# R32 — AGENT-BORDER DRIFT-METRIK-SPEZIFIKATION v2

`text
OBJECT =
NEXUS_OMEGA_R32_AGENT_BORDER_DRIFT_METRIC_SPEC_V2_20261004_R0

PARENT =
NEXUS_OMEGA_AXIOM_R32_BORDER_METRICS_AND_LANE_B_SEQUENCING_ADJUDICATION_20261004_R0

STATE =
SET_U_DESIGN_ONLY

CLAIM_CEILING =
C1_DESCRIPTIVE_ONLY

AUTHORITY =
OPERATOR_ALEXANDER_VIA_AXIOM

IMPLEMENTATION =
NO

CLAIM_PROMOTION =
NO

NODE_ACTIVATION =
NO
`

## 0. Kernregel — Measurand vor Metrik

`text
MEASURE_THE_BOUNDARY,
BUT_FIRST_DEFINE
WHAT_THE_BOUNDARY_MEASUREMENT
IS_ACTUALLY_MEASURING.
`

Jede Metrik dieser Spezifikation deklariert verbindlich: **Measurand** (das gemessene Merkmal), **Gueltigkeitsdomain** (fuer welche Repraesentationen sie aussagekraeftig ist), **Grenzregeln** (Abbruch-/Leerwerte) und **Falsifikationsbedingungen**. Eine Metrik ohne deklarierten Measurand ist unzulaessig.

## 1. Border-Vektor — kein globaler Drift-Score

`text
BORDER_VECTOR = {
  DISTRIBUTION_SHIFT,
  ORDERED_FEATURE_SHIFT,
  TOP_K_STRUCTURE_SHIFT,
  SAMPLE_SUFFICIENCY
}

GLOBAL_DRIFT_SCORE =
NO
`

Die vier Komponenten werden unabhaengig ausgewiesen und interpretiert. Es existiert bewusst KEINE Aggregation zu einer einzigen Zahl: Eine Aggregation wuerde unterschiedliche Measurands unsichtbar mischen und Praezision vortaeuschen.

## 2. Metrik-Regeln

### 2.1 JSD — Primaere Verteilungsmetrik (DISTRIBUTION_SHIFT)

- Measurand: Aenderung einer diskreten Wahrscheinlichkeitsverteilung zwischen Referenz- und Beobachtungsfenster.
- Gueltigkeit: Nur bei **gueltigen Wahrscheinlichkeitsverteilungen** (nicht-negativ, Summe 1) und **natuerlichem Logarithmus**.

`text
JSD_BOUND =
[0, ln(2)]
ONLY_IF_NATURAL_LOG_AND_VALID_PROBABILITY_DISTRIBUTIONS
`

- Leerwert-Regel (Domain-Regel, verbindlich):

`text
IF total_observations == 0
THEN
METRIC_STATE = INSUFFICIENT_DATA
NOT
JSD = 0
`

Ein vollstaendig leerer Beobachtungsblock besitzt keine normalisierbare empirische Verteilung. Jede Glattung (Smoothing, Pseudo-Counts) ist verboten, sofern sie nicht explizit als Regel mit Begrifflichkeit, Auswirkung auf die Bound und Kalibrierungslage deklariert ist.

### 2.2 PSI — Sekundaere Verteilungsmetrik (DISTRIBUTION_SHIFT)

`text
PSI_BANDS =
HEURISTIC_INITIAL_OPERATING_THRESHOLDS

NOT =
SCIENTIFICALLY_UNIVERSAL_THRESHOLDS
`

Die Startwerte 0.10 / 0.25 duerfen als initiale Betriebspunkte fuer Fixtures dienen, sind aber **nicht kanonisch**. Sie muessen spaeter an Null- und Drift-Korpora gegen False-Positive- und False-Negative-Raten geprueft und gegebenenfalls ersetzt werden. Bis zur Kalibrierung ist jede PSI-Alarmkategorie ein SET_U-Signal, keine Evidenz.

### 2.3 Wasserstein-1 — nur bei geordneten Features (ORDERED_FEATURE_SHIFT)

`text
FEATURE_SPACE =
ORDERED_OR_METRICALLY_MEANINGFUL
`

W1 ist nur zulaessig, wenn der Feature-Raum eine echte Ordnungs- oder Metrikstruktur besitzt (z. B. Zeitreihenwerte, Groessen, Rangfolgen). Bei willkuerlichen Kategorien ist W1 semantisch fragwuerdig und unzulaessig.

### 2.4 Top-k-n-Gramm-Cosine — Struktursignal (TOP_K_STRUCTURE_SHIFT)

`text
COSINE_DISTANCE =
STRUCTURAL_SHIFT_SIGNAL

NOT =
SEMANTIC_DRIFT_PROOF
`

Abdeckungs- und Strukturveraenderungen im Token-/n-Gramm-Raum sind ein Hinweis auf strukturelle Verschiebung. Sie beweisen keine semantische Drift; HASH_DISTANCE != SEMANTIC_DISTANCE bleibt bindend.

### 2.5 Entropie — Kontextsignal (SAMPLE_SUFFICIENCY / Kontext)

`text
ENTROPY =
CONTEXT_SIGNAL_NOT_DRIFT_PROOF
`

Entropiewerte dienen der Kontextualisierung (Komplexitaet, Diversitaet) und der Beurteilung der Beobachtungsdichte. Sie sind kein Driftnachweis.

## 3. Falsifikationsbedingungen der Spezifikation

`text
F1 =
NULL_FIXTURES_TRIGGER_ALARM

F2 =
KNOWN_DRIFT_FIXTURES_ESCAPE_DETECTION

F3 =
ESSENTIAL_METRIC_PATH_REQUIRES_EXTERNAL_TOKEN_REASONING

F4 =
THRESHOLDS_ARE_POST_HOC_TUNED_TO_DESIRED_RESULTS

F5 =
METRIC_IS_UNSTABLE_UNDER_EQUIVALENT_REPRESENTATIONS
`

F5 konkret: Derselbe Inhalt mit abweichender Chunking-, Encoding- oder Whitespace-Struktur darf keinen massiven Alarm ausloesen, wenn der Measurand davon unberuehrt sein sollte. Die Repraesentationsinvarianz ist vor Inbetriebnahme an Fixtures zu pruefen — und ist genau der Grund, warum der Measurand VOR der Metrik definiert wird.

## 4. Token-Neutralitaet

Die EXTERNAL_TOKEN_NEUTRALITY_LAW bleibt bindend: Kein essentieller Metrik-Pfad darf externes Token-Reasoning erfordern (F3). Alle Berechnungen sind lokal reproduzierbar.

## 5. Kalibrierung

`text
CALIBRATION_SOURCE =
R31_P8_EXTERNAL_NEGATIVE_TESTING_FIXTURES_ONLY
`

Zulaessige Fixture-Klassen: Null-Fixtures (keine Drift erwartet), bekannte Drift-Fixtures (Drift erwartet), adversariaelle Fixtures (aequivalente Repraesentationen — F5). Kalibrierung ausserhalb dieser Korpora ist unzulaessig.

## 6. Border-Befugnisse (Mailbox-Vertrag, R30-konform)

`text
BORDER_MAY =
OBSERVE
MEASURE
CLASSIFY
QUARANTINE
TRIGGER_REVIEW

BORDER_MAY_NOT =
PROMOTE
EXECUTE
WRITE_CANON
`

Der Mailbox-Eingang erzeugt ausschliesslich REACTION_EVENTs (REVIEW_EVENT, NODE_REACTIVATION-Signal, AXIOM_ATTENTION, CURSOR_ATTENTION) — niemals privilegierte Ausfuehrung. THE_OUTSIDE_WORLD MAY KNOCK. IT MAY NOT TURN THE HANDLE.

## 7. HOMEOSTASIS-Gabelung (G6) und G8 reformuliert

`text
G6_A =
SUPPLY_HOMEOSTASIS_BIRTH_EVIDENCE
-> TEST_REGISTRY_DIVERGENCE

G6_B =
WITHDRAW_BIRTH_PREMISE
-> NO_REGISTRY_DIVERGENCE_FROM_HOMEOSTASIS
`

R32 setzt nicht implizit HOMEOSTASIS = BORN voraus. G8 wird nicht neu erfunden, sondern an die vorhandene Birth-Law gebunden:

`text
G8 =
WHICH_BIRTH_STAGE_WAS_CLAIMED_FOR_HOMEOSTASIS
AND_WHICH_PRIMARY_EVIDENCE_SATISFIES_THAT_STAGE?

B0_CONCEIVED
B1_FOUNDATION_BOUND
B2_ARTIFACT_BORN
B3_OPERATIONALLY_BORN
B4_PUBLICLY_BORN
B5_CONTINUITY_WITNESSED
`

Eine nachtraegliche Neudefinition von Geburt, nur um HOMEOSTASIS passend zu machen, ist unzulaessig. NO EVIDENCE GAP MAY BE REPAIRED BY SEMANTICS AFTER THE FACT.

## 8. Hostinger-Anker

`text
HOSTINGER =
DISCOVERY_AND_PUBLIC_READBACK_ANCHOR

NOT =
SOLE_IMMUTABILITY_ROOT
`

Ein oeffentlich angezeigter Hash ist noch kein unveraenderlicher Anker. Immutability entsteht nur durch Kombination:

`text
CONTENT_HASH
+
GIT_COMMIT
+
PUBLIC_READBACK
+
TIMESTAMPED_RECEIPT
`

Ein externer Transparency-/Archive-Witness ist optionaler spaeterer Schritt.

## 9. Lane-B — Sequenzierung

`text
LANE_B_RESEARCH_PREPARATION =
ALLOWED_NOW

LANE_B_NULL_MODEL_BINDING =
BLOCKED_UNTIL_G6
`

Verbindliche Reihenfolge:

`text
G6
-> DEFINE_NODE_POPULATION
-> DEFINE_AUTHORITY_GRAPH
-> DEFINE_MEASURAND_FOR_POWER_CONCENTRATION
-> BUILD_NULL_MODEL
-> FALSIFICATION
`

Nicht umgekehrt: Eine un aufgeloeste Node-Population wuerde den Fehler in das Referenzmodell einbauen.

## 10. Kanonischer R32-Bind

`text
OBJECT =
NEXUS_OMEGA_R32_AGENT_BORDER_METRIC_SET_U_AND_LANE_B_SEQUENCING_BIND_20261004_R0

PARENT =
R31_MISTRAL_EXECUTION_COMPLETE_C1_REPORTED

CLAIM_CEILING =
C1_DESCRIPTIVE_ONLY

BORDER_STATE =
SET_U_DESIGN_ONLY

PRIMARY_DISTRIBUTION_METRIC =
JENSEN_SHANNON_DIVERGENCE

JSD_EMPTY_SAMPLE_POLICY =
INSUFFICIENT_DATA

PSI_THRESHOLDS =
HEURISTIC_START_POINTS_NOT_CANON

WASSERSTEIN_1 =
ONLY_FOR_METRICALLY_MEANINGFUL_FEATURES

TOP_K_COSINE =
STRUCTURAL_SIGNAL_NOT_SEMANTIC_PROOF

ENTROPY =
CONTEXT_SIGNAL_NOT_DRIFT_PROOF

GLOBAL_DRIFT_SCORE =
NO

LANE_B_PREPARATION =
YES

LANE_B_NULL_MODEL_BIND =
BLOCKED_PENDING_G6

HOMEOSTASIS_REGISTER_DIVERGENCE =
CONDITIONAL

G8_REFORMULATED =
IDENTIFY_CLAIMED_BIRTH_STAGE
+
BIND_STAGE_SPECIFIC_PRIMARY_EVIDENCE

MAILBOX =
REVIEW_TRIGGER_ONLY

EXTERNAL_EXECUTION_AUTHORITY =
NONE

IMPLEMENTATION =
NO

CLAIM_PROMOTION =
NO

NODE_ACTIVATION =
NO
`

## 11. Status und Luecken

- Diese Spezifikation ist SET_U_DESIGN_ONLY: keine Implementierung, kein Betrieb, keine Schwellwert-Heiligung.
- Offen: Kalibrierung an R31-P8-Fixtures (Null / Drift / adversarial), G6-Entscheid, G8-Stage-Bindung, BigQuery-G3 (Project-ID), F5-Repraesentationsinvarianz-Pruefprotokoll.
- Falsifikation der Spezifikation: Widerlegt, wenn eine der Bedingungen F1-F5 in der Kalibrierung eintritt oder wenn ein Pfad ohne deklarierten Measurand betrieben wird.
