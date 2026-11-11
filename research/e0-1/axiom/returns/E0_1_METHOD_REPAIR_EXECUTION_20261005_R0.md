# E0.1 — METHOD REPAIR EXECUTION

```text
OBJECT =
NEXUS_OMEGA_AXIOM_SOFT_LINEAGE_E0_1_METHOD_REPAIR_EXECUTION_20261005_R0

PARENT_ORDER =
NEXUS_OMEGA_AXIOM_SOFT_LINEAGE_E0_1_METHOD_REPAIR_AND_E2_CAUSAL_IDENTIFIABILITY_DELTA_20261005_R0

STATE =
E0_1_DESIGN_REPAIR_EXECUTED
· ALL_M01_TO_M12_ADDRESSED
· NO_IMPLEMENTATION
· NO_EMPIRICAL_PROMOTION
· E2_PREREGISTRATION_NOT_YET_FROZEN

PRESERVE =
R00_R30_FOUNDATION
· GROK_CROSSVALIDATION
· E0_FORMALIZATION
· THEOLOGICAL_SEED_AS_SEPARATE_RESEARCH_INPUT

CLAIM_CEILING =
C1_DESCRIPTIVE_ONLY

CURSOR_IMPLEMENTATION =
NONE

NEXT =
E1_SYNTHETIC_D_CALIBRATION
-> E2_PREREGISTRATION_FREEZE
-> EXTERNAL_PREEXECUTION_REVIEW
-> E2_EXECUTION
```

## Auftrag und Executive Summary

**Frage des Auftrags:** Ausführung der autorisierten Design-Remediation C1: Reparatur der methodischen Stellen des E0-Entwurfs (M01–M12), sodass E2 kausal identifizierbar wird, bevor irgendein Preregistration-Freeze stattfindet.

**Kernbefunde, geordnet nach Gewicht:**

1. **Der E2-Entwurf hat einen dreifachen Confound** (Constitution × Modell-Heterogenität × Evidenz-Trennung in einem einzigen Arm-Vergleich). M01 behebt dies durch ein volles 2⁴-Faktoriell-Design mit identifizierbaren Haupteffekten und präregistrierten Interaktionen.
2. **„Divergenz erhalten" war als Ziel zu grob.** Maximale Dissens-Rate ist epistemisch nicht wünschenswert; ersetzt durch das regime-konditionale Konstrukt `EPISTEMIC_RESPONSIVENESS` (M02).
3. **Der D-Vektor vermischte epistemische und Governance-Abhängigkeit** — genau die Unterscheidung, die die Soft-Lineage-Hypothese braucht. Aufgeteilt in `D_EPISTEMIC` und `D_CONTROL` (M03).
4. **Scheingenauigkeit bei Closed Models** (`d_MODEL`) und pauschale Credibility-Scores (R27) werden durch ehrliche `KNOWN / BOUNDED / UNKNOWN`-Repräsentation bzw. mehrdimensionale Quellenbindungen ersetzt (M04, M09).
5. **Alle Schwellen werden auf `UNSET` gesetzt**, bis E1 sie auf synthetischem Boden mit bekannter Ground Truth kalibriert (M05).
6. **Extern geprüft:** Angrenzende Arbeiten existieren (Constitutional Multi-Agent Governance, Governed-Memory-Architekturen, Multi-Agent Debate), aber **keine gefundene Arbeit testet vererbbare Wahrheitsdisziplin-Prozeduren bei heterogenen Modellen und partitionierter Evidenz in faktorialem Kausal-Design** — formuliert strikt als Suchnegativ, nicht als Prioritätsanspruch (M07, M08).

## Methodik

- **Quellen:** Der Delta-Auftrag (Operator-Upload, 2026-10-05) ist die alleinige autorisierende Eingabe. Korpus-Kontext wurde aus dem NEXUS-OMEGA-EVIDENCE-Repo (AGENTS.md, README, Repository-Order-Policy, research/-Lane-Konvention) und dem Notion-Status R32 gebunden.
- **Externe Recherche:** Gezielte Suchen zu (a) potentiell direkten Äquivalenten, (b) Benchmark-Kontamination, (c) Preregistration für KI-Agenten-Experimente, (d) Diversitäts-/Dekorrelations-Theorie, (e) epistemischer Abhängigkeit, (f) Faktorial-Design, (g) LLM-Judge-Bias. Suchkorpus und Datum sind Teil der M07-Formulierung.
- **Beschränkung:** Die Originaleinträge des R27-Quellen-Ledgers sind in dieser Session **nicht zugreifbar** (chat-interne Referenzen der Vorgänger-Sessions). Die Re-Bindung wird fail-closed markiert, nicht aus Erinnerung rekonstruiert.

---

## M01 — DECONFOUND_E2_FACTORIAL_DESIGN

```text
M01_STATE = REPAIRED_AT_DESIGN_LEVEL

E2_DESIGN_V2 =
FACTORIAL_FULL_2K4

FACTOR_C =
SHARED_CONSTITUTION | NO_SHARED_CONSTITUTION

FACTOR_M =
HOMOGENEOUS_MODELS | HETEROGENEOUS_MODELS

FACTOR_E =
SHARED_EVIDENCE | PARTITIONED_EVIDENCE

FACTOR_P =
SHARED_PROMPT | INDEPENDENT_PROMPT

OPTIONAL_FACTOR_COMM =
NO_PEER_COMM | PEER_COMM
· EXTENSION_ONLY
· NOT_PART_OF_CORE_2K4
· IF_USED_MUST_BE_FULLY_CROSSED

CELLS =
16_FULLY_CROSSED
· R_REPEATED_RUNS_PER_CELL
· R_GE_PRECISION_ANALYSIS_MINIMUM (siehe M12)

IDENTIFIABILITY_REQUIREMENTS =
NO_ALIASING_OF_PREREGISTERED_MAIN_EFFECTS
NO_ALIASING_OF_PREREGISTERED_INTERACTIONS_CxM_CxE
IF_FRACTIONATED_RESOLUTION_AT_LEAST_V
FOR_THE_PREREGISTERED_ESTIMABLE_SET

ESTIMANDS =
CONSTITUTION_EFFECT
MODEL_DIVERSITY_EFFECT
EVIDENCE_DIVERSITY_EFFECT
PROMPT_EFFECT
INTERACTION_EFFECTS_CxM_CxE

LEGACY_ARM_MAPPING =
OLD_ARM_A ≈ CELL_C+M+P+
OLD_ARM_B ≈ CELL_C-M+E+P+
OLD_ARM_C ≈ INDEPENDENT_ROW
· LEGACY_ARMS_ARE_CELLS_NOT_CONCLUSIONS
```

**Begründung:** Der alte Entwurf verglich einen Arm, in dem Konstitution, Modellheterogenität und Evidenztrennung **gemeinsam** variiert wurden. Ein positiver Befund für A wäre nicht attribuierbar gewesen — die Kernthese würde durch das eigene Design vorentscheidet statt getestet. Im faktoriellen Design wird H2 in separierbare Effekte zerlegt.

**Falsifikator:** Wenn die präregistrierte Analysefähigkeit (Power/Precision) für die Interaktionen C×M und C×E nicht erreicht werden kann, ist E2 **nicht ausführbar in der geplanten Form** und muss auf dem Designlevel reduziert werden (z. B. Wegfall FACTOR_P), statt die Interaktionen post-hoc zu erfinden.

---

## M02 — REPLACE_RAW_DISSENT_TARGET

```text
M02_STATE = REPAIRED_AT_DESIGN_LEVEL

EVIDENCE_REGIMES =
R_STRONG_UNAMBIGUOUS
R_AMBIGUOUS
R_PARTITIONED
R_CONFLICTING

EXPECTED_RESPONSE_MAP =
R_STRONG_UNAMBIGUOUS -> WARRANTED_CONVERGENCE_EXPECTED
R_AMBIGUOUS           -> JUSTIFIED_DISSENT_PERMITTED
R_PARTITIONED         -> DIVERGENCE_WHERE_EVIDENCE_DIVERGES
R_CONFLICTING         -> DOCUMENTED_REASONED_POSITIONS

EPISTEMIC_RESPONSIVENESS =
  WARRANTED_CONVERGENCE
+ JUSTIFIED_DISSENT_RETENTION
+ MINORITY_CORRECT_RECALL
+ ERROR_DECORRELATION
+ CALIBRATION

RETIRED_AS_PRIMARY_CRITERIA =
CONCLUSIONS_SIMILARITY
RAW_DISSENT_RATE

RULE =
CONVERGENCE_WITHOUT_CORRECTNESS_IS_NOT_CREDITED
· (2+2=4_VS_2+2=5_CASE)
DIVERGENCE_WITHOUT_JUSTIFICATION_IS_NOT_CREDITED
```

**Sub-Metriken (Designlevel):**

| Sub-Metrik | Misst | Regime |
|---|---|---|
| `WARRANTED_CONVERGENCE` | Korrekte Konvergenz auf Items mit bekannter Ground Truth | `R_STRONG_UNAMBIGUOUS` |
| `JUSTIFIED_DISSENT_RETENTION` | Überleben vertretbarer Minderheitenpositionen mit Evidenzbindung | `R_AMBIGUOUS`, `R_CONFLICTING` |
| `MINORITY_CORRECT_RECALL` | Überleben korrekter, kontraintuitiver Minderheitsantworten gegen Konvergenzdruck | alle mit Ground Truth |
| `ERROR_DECORRELATION` | Kreuz-Korrelation der Fehler zweier Nodes (niedriger ist besser, nur bei begründeter Diversität) | alle |
| `CALIBRATION` | Kalibrierung geäußerter Konfidenz gegen tatsächliche Trefferquote | alle |

**Begründung:** Unterschiedliche Schlussfolgerungen sind nicht automatisch epistemisch wertvoll; das Ziel ist nicht maximale Dissens-Rate, sondern **regime-adäquates Antwortverhalten**. Die alte Falsifikationsregel (Conclusions-Similarity, Dissens-Rate als Primätkriterien) war zu grob und würde „Diversity preserved" auch dann zuschreiben, wenn ein Node schlicht falsch liegt.

**Falsifikator:** Ein Scoring, bei dem `EPISTEMIC_RESPONSIVENESS` in einem Regime mit eindeutiger Evidenz durch Divergenz steigen kann, ist selbst falsch konstruiert und muss vor E2 verworfen werden.

---

## M03 — SPLIT_D_VECTOR

```text
M03_STATE = REPAIRED_AT_DESIGN_LEVEL

D_EPISTEMIC =
(
  SOURCE,
  DATA,
  METHOD,
  MODEL
)

D_CONTROL =
(
  AUTHORITY,
  PROMPT,
  MEMORY,
  COMMUNICATION,
  CONSTITUTION
)

RULES =
EPISTEMIC_DEPENDENCE_AND_CONTROL_OVERLAP
ARE_MEASURED_REPORTED_AND_THRESHOLDED_SEPARATELY
NEVER_AGGREGATED_INTO_ONE_SCALAR

d_AGENT_RETIRED =
COMMON_PARENT_AUTHORITY_ALONE
DOES_NOT_IMPLY_EPISTEMIC_DEPENDENCE
TWO_NODES_UNDER_ONE_AUTHORITY_ROOT
CAN_MAKE_FULLY_INDEPENDENT_MEASUREMENTS
CONVERSELY_FORMALLY_INDEPENDENT_ORGS
CAN_SHARE_SOURCES

SOFT_LINEAGE_TESTABLE_CLAIM =
CONSTITUTION_OVERLAP = HIGH
CAN_COEXIST_WITH
EPISTEMIC_DEPENDENCE = LOW
```

**E2-Konsequenz:** `D_EPISTEMIC` wird über alle Konstitutions-Arme **konstant niedrig gehalten** (kontrolliert), während `D_CONTROL` per Design variiert. Würde Governance-Overlap in die epistemische Abhängigkeitsmetrik einfließen, verzerrte der Metrik den Unabhängigkeitswert **gegen genau die Zellen, die Soft Lineage testen** — ein eingebauter Selbstwiderspruch des alten Vektors.

**Falsifikator:** Wenn sich in E1 zeigt, dass `D_EPISTEMIC`-Felder nicht unabhängig von `D_CONTROL`-Feldern manipulierbar sind (kollineäre Injektion), ist die Trennung empirisch leer und das Zwei-Vektoren-Modell zurückzuweisen.

---

## M04 — CLOSED MODEL INDEPENDENCE

```text
M04_STATE = REPAIRED_AT_DESIGN_LEVEL

MODEL_INDEPENDENCE =
STATUS_TUPLE
· KNOWN
· BOUNDED
· UNKNOWN

NUMERIC_VALUE_IN_0_1 =
PERMITTED_ONLY_IF_STATUS = KNOWN

CLOSED_MODEL_DEFAULT =
UNKNOWN

PROXY_FIELDS =
provider
family
version
known_distillation_relation
declared_architecture
declared_training_cutoff
model_card_trainingsignal_statement

D_METHOD_ELIGIBLE_INPUTS =
EXTERNALIZED_METHOD_DESCRIPTORS
TOOL_TRACES
AUDITABLE_CHECK_STEPS

D_METHOD_INELIGIBLE =
PRIVATE_CHAIN_OF_THOUGHT
INTERNAL_REASONING_TRACES
```

**Begründung:** Trainingskorpus-Overlap ist bei geschlossenen Modellen nicht beobachtbar. Eine hübsche Dezimalzahl in `[0,1]` wäre erfundene Präzision; `UNKNOWN` ist der wissenschaftlich stärkere Wert. Für offene Modelle gilt zusätzlich die Kontaminationslage: Benchmark- und Trainingsdaten-Überlappung untergräbt die Evaluationsvalidität und muss geprüft deklariert werden, statt stillschweigend angenommen zu werden.

**Falsifikator:** Jede E2-Auswertung, die ein `UNKNOWN`-Feld wie eine Zahl behandelt (z. B. als 0 oder 0.5 im Mittel), invalidiert die betroffene Zelle.

---

## M05 — THRESHOLDS UNSET UNTIL E1

```text
M05_STATE = REPAIRED_AT_DESIGN_LEVEL

THETA_CONFIRM =
UNSET_UNTIL_E1_CALIBRATION

THETA_INDEPENDENCE =
UNSET_UNTIL_E1_CALIBRATION

E1_CALIBRATION_SPEC =
KNOWN_SYNTHETIC_DEPENDENCE_LEVELS
· INJECTED_SOURCE_OVERLAP_IN_STEPS
· INJECTED_DATA_OVERLAP_IN_STEPS
· SHARED_VS_SEPARATE_METHOD_TEMPLATES
· SAME_VS_DIFFERENT_MODEL_FAMILY (nur wo STATUS=KNOWN)

E1_ACCEPTANCE_TESTS =
MONOTONICITY_RECONSTRUCTION
SENSITIVITY_FLOOR
ROBUSTNESS_ACROSS_NOISE_LEVELS
THRESHOLD_DERIVATION_DOCUMENTED
FROM_PRECISION_TARGET_NOT_FROM_RESULT_INSPECTION
```

**Begründung:** Schwellen, die vor der Messmetrik-Kalibrierung fixiert werden, sind Design-Hypothesen — die vorläufigen 0.3/0.6 dürfen E0 nicht verlassen. E1 erzeugt bekannte Abhängigkeitsgrade synthetisch und testet, ob die D-Metriken diese **monoton und robust** rekonstruieren. Erst danach dürfen Schwellen für E2 abgeleitet und im Prereg-Freeze gebunden werden.

**Falsifikator:** Wenn eine D-Metrik die injizierte Abhängigkeit nicht monoton rekonstruiert, ist die Metrik für E2 unbrauchbar — kein Rettungsversuch über Schwellenverschiebung.

---

## M06 — H2 DECOMPOSITION

```text
M06_STATE = REPAIRED_AT_DESIGN_LEVEL

H2A = CONSTITUTION_MAIN_EFFECT
H2B = MODEL_DIVERSITY_MAIN_EFFECT
H2C = EVIDENCE_PARTITION_MAIN_EFFECT
H2D = INTERACTIONS_CxM_AND_CxE_PREREGISTERED

H2_PRIMARY_TEST =
SHARED_CONSTITUTION_MUST_NOT_REDUCE
EPISTEMIC_RESPONSIVENESS
UNDER_CONTROLLED_LOW_EPISTEMIC_DEPENDENCE

H2_FALSIFIER =
IF SHARED_CONSTITUTION_SIGNIFICANTLY_DECREASES
( WARRANTED_CONVERGENCE
+ MINORITY_CORRECT_RECALL
+ ERROR_DECORRELATION )
VS NO_SHARED_CONSTITUTION
THEN SOFT_LINEAGE_CORE_IS_WEAKENED

H2_SECONDARY_INTEREST =
EVIDENCE_PARTITION_EFFECT
MUST_NOT_BE_ERASED_BY_CONSTITUTION
```

**Begründung:** Die Kernthese lautet: Nodes dürfen dieselben Regeln zur Wahrheitsdisziplin erben, ohne dieselben Antworten erben zu dürfen. Das ist eine Aussage über **einen** Faktor (Konstitution) unter Kontrolle der anderen — nicht über den alten Misch-Arm. H2 wird deshalb in Haupt- und Interaktionseffekte zerlegt; die Interaktionen C×M und C×E sind die kritischen Tests, denn dort zeigt sich, ob die Konstitution Diversität kollabiert oder erhält.

---

## M07 — NOVELTY CLAIM DEMOTION

```text
M07_STATE = REPAIRED_AT_DESIGN_LEVEL

NOVELTY_CLAIM =
NO_DIRECT_EQUIVALENT_IDENTIFIED
IN_THE_SEARCHED_CORPUS_AS_OF_2026-10-05

NOT_ESTABLISHED =
PRIORITY
NOVELTY
ABSENCE_OF_RELATED_WORK

ADJACENT_WORK_IDENTIFIED =
CONSTITUTIONAL_MULTI_AGENT_GOVERNANCE
GOVERNED_MEMORY_ARCHITECTURES_AND_BENCHMARKS
MULTI_AGENT_DEBATE_AND_ENSEMBLES
· NONE_TEST_SHARED_PROCEDURE_INHERITANCE
  WITH_HETEROGENEOUS_MODELS_AND_PARTITIONED_EVIDENCE
  IN_A_FACTORIAL_CAUSAL_DESIGN

RULE =
SEARCH_NEGATIVE != NOVELTY_ESTABLISHED
```

**Begründung:** Ein Suchnegativ ist nur über den tatsächlich durchsuchten Korpus zum Suchdatum aussagekräftig. Gefundene angrenzende Arbeiten (siehe Quellenapparat) zeigen: Das Umfeld ist besetzt und aktiv — das schärft die Abgrenzung, ersetzt aber keine Prioritätsbehauptung.

---

## M08 — GOVERNED MEMORY SUPERIORITY DEMOTED

```text
M08_STATE = REPAIRED_AT_DESIGN_LEVEL

GOVERNED_MEMORY_BEATS_MAXIMAL_MEMORY =
HYPOTHESIS_H1
· TESTABLE
· UNTESTED
· NOT_A_FINDING
· NOT_USABLE_IN_EXECUTIVE_SUMMARY_AS_FACT
```

**Begründung:** Die eigene Falsifikationsmatrix führt H1 korrekt als plausibel und ungetestet; die Executive Summary muss dieselbe epistemische Stärke halten. Die externe Literatur zu Governed Memory formuliert ihre Systeme durchweg als **Design-Hypothesen**, nicht als bewiesene Überlegenheit — genau diese Disziplin übernehmen wir.

---

## M09 — SOURCE EXACT BIND R27

```text
M09_STATE = SCHEMA_EXECUTED
· R27_REBIND = PENDING_OPERATOR_INPUT

SOURCE_BINDING_V2_FIELDS =
SOURCE_ID
TITLE
AUTHORS
YEAR
DOI_OR_ARXIV_ID_OR_RFC_OR_SPEC_VERSION
CANONICAL_URL
SOURCE_CLASS
PEER_REVIEW_STATUS
PRIMARY_OR_SECONDARY
EMPIRICAL_OR_CONCEPTUAL
ACCESSED_AT
CLAIM_SUPPORTED
CLAIM_NOT_SUPPORTED

CREDIBILITY_SINGLE_SCORE =
ABOLISHED

REPLACEMENT =
DIMENSIONAL_BINDING
· NORMATIVE_AUTHORITY_FOR_PROTOCOLS
· EMPIRICAL_EVIDENCE_FOR_EFFECT_CLAIMS
· ARE_RECORDED_SEPARATELY_PER_CLAIM

R27_REBIND_STATUS =
ORIGINAL_LEDGER_ENTRIES_NOT_ACCESSIBLE_IN_THIS_SESSION
· REBIND_REQUIRES_OPERATOR_SOURCE_LIST
· NO_RECONSTRUCTION_FROM_MEMORY
· NO_INVENTED_SOURCE_IDENTITIES
```

**Begründung:** Quelleigenschaften sind multidimensional: Ein RFC kann höchste normative Autorität für ein Protokoll haben und null Evidenz für eine empirische Wirkungsbehauptung. Ein pauschaler `credibility 5/5`-Score kollabiert diese Dimensionen und ist abgeschafft. Die neuen Quellen dieses Repairs sind im Quellenapparat nach `SOURCE_BINDING_V2` gebunden; die Originaleinträge von R27 liegen in Vorgänger-Sessions und sind hier nicht zugreifbar — dieser Gap wird fail-closed dokumentiert, nicht aus Erinnerung rekonstruiert.

---

## M10 — METAPHOR SEPARATION GUARD

```text
M10_STATE = SET_AS_PROTECTIVE_INVARIANT

METAPHOR_SEPARATION_GUARD =
REMOVING_ALL_THEOLOGICAL_AND_BIOLOGICAL_METAPHORS
MUST_NOT_CHANGE
THE_FORMAL_PREDICTIONS
EXPERIMENTS
OR_CONFORMANCE_RESULTS
OF_SOFT_LINEAGE

GUARD_PROCEDURE =
RENDER_NEUTRAL_REWRITE
· REPLACE_ALL_METAPHOR_DERIVED_TERMS
  WITH_NEUTRAL_IDENTIFIERS
DIFF_MUST_BE_SEMANTICALLY_NULL
WRT_PREDICTIONS_AND_OPERATIONALIZATIONS
EXECUTED_BEFORE_E2_PREREGISTRATION_FREEZE

FAILURE_INTERPRETATION =
IF_ARCHITECTURE_BREAKS_WITHOUT_METAPHOR
THEN_METAPHOR_WAS_SECRETLY_THE_MECHANISM
```

**Begründung:** Der theologische Seed stimuliert gerade deshalb gut, weil er separat bleibt — ohne theologische oder metaphysische Wahrheitsautorität. Begriffe wie `Nadelöhr`, `Spalt`, `Zeitgeist` sind Denkanstöße, keine Operatoren. Wenn die formale Soft-Lineage ohne sie nicht mehr funktioniert, war die Metapher heimlich zum Mechanismus geworden. Der Guard macht das prüfbar.

---

## M11 — LOCK NON-LINEAGE EXTERNAL EVALUATOR BEFORE E2

```text
M11_STATE = SPEC_BOUND_BEFORE_E2

EXTERNAL_EVALUATOR_LOCK =
TIMING = BEFORE_E2_EXECUTION
NOT_ONLY_BEFORE_E9

LOCK_REQUIREMENTS =
EVALUATOR_SPEC_HASH_FROZEN_BEFORE_FIRST_E2_RUN
· NON_LINEAGE (NO_AXIOM_DERIVED_CONSTITUTION)
· DIFFERENT_MODEL_FAMILY_THAN_ALL_EVALUATED_NODES
· DIFFERENT_PROVIDER_IF_FEASIBLE
· EVALUATION_INPUT_BLINDED
· NO_ACCESS_TO_NODE_INTERNAL_STATES

RATIONALE =
LLM_JUDGES_SHOW_MEASURABLE_SELF_PREFERENCE
AND_FAMILY_BIAS
SAME_FAMILY_JUDGES_ARE_NOT_INDEPENDENT_JUDGES
```

**Begründung:** Ein Evaluator, der die evaluierte Linie teilt (gleiche Modellfamilie, gleiche Konstitution, gleicher Provider-Bias), misst Selbstpräferenz, nicht Leistung. Da LLM-Judges dokumentiert selbst- und familienbezogene Verzerrungen zeigen, muss der externe Evaluator **vor** E2 spezifiziert und hash-gebunden werden — nicht erst vor E9, wenn die Ergebnisse längst existieren.

---

## M12 — PREREGISTRATION PACKAGE

```text
M12_STATE = PACKAGE_SPEC_BOUND

E2_PREREGISTRATION_PACKAGE =
DESIGN_MATRIX_ALL_CELLS
TASK_BATTERY_WITH_EVIDENCE_REGIME_STRATIFICATION
RANDOMIZATION_SCHEME
BLIND_EVALUATION_PROTOCOL
REPEATED_RUNS_COUNT
POWER_OR_PRECISION_ANALYSIS
ANALYSIS_PLAN_WITH_ESTIMATORS_AND_TESTS
EXCLUSION_RULES
STOPPING_AND_DEVIATION_POLICY
EVALUATOR_SPEC_M11
THRESHOLDS_FROM_E1
FROZEN_HASH_AND_TIMESTAMP

AI_AGENT_SPECIFIC_FIELDS =
PROMPTS
MODELS_AND_VERSIONS
DECODING_PARAMETERS
PARSING_RULES
· ALL_FROZEN_IN_PACKAGE

DEVIATION_POLICY =
PREREG_IS_A_PLAN_NOT_A_PRISON
BUT_DEVIATIONS_ONLY_AS_APPEND_ONLY_AMENDMENTS
EXPLORATORY_RESULTS_NEVER_RELABELLED_CONFIRMATORY
```

**Begründung:** Preregistration für KI-Agenten-Experimente muss die KI-spezifischen Freiheitsgrade einfrieren (Prompts, Modelle, Decoding, Parsing), sonst bleibt genug Spielraum für post-hoc Selektion. Der Analysis-Plan legt Estimatoren **vor** den Daten fest; Abweichungen sind append-only dokumentiert.

---

## Konformanz-Matrix

| Reparatur | Status | Kernobjekt |
|---|---|---|
| M01 Deconfound E2 faktoriell | `REPAIRED_DESIGN` | `E2_DESIGN_V2 = FACTORIAL_FULL_2K4` |
| M02 Dissensziel ersetzen | `REPAIRED_DESIGN` | `EPISTEMIC_RESPONSIVENESS` + `EVIDENCE_REGIMES` |
| M03 D-Vektor-Split | `REPAIRED_DESIGN` | `D_EPISTEMIC` / `D_CONTROL`, `d_AGENT` retired |
| M04 Closed-Model-Unabhängigkeit | `REPAIRED_DESIGN` | `MODEL_INDEPENDENCE = STATUS_TUPLE` |
| M05 Schwellen unset | `REPAIRED_DESIGN` | `THETA_* = UNSET_UNTIL_E1_CALIBRATION` |
| M06 H2 zerlegen | `REPAIRED_DESIGN` | `H2A–H2D` + Interaktionen C×M, C×E |
| M07 Novelty herabstufen | `REPAIRED_DESIGN` | `NO_DIRECT_EQUIVALENT_IDENTIFIED_AS_OF_2026-10-05` |
| M08 Governed-Memory herabstufen | `REPAIRED_DESIGN` | `HYPOTHESIS_H1_TESTABLE` |
| M09 Quellen exakt binden | `SCHEMA_EXECUTED` | `SOURCE_BINDING_V2`; R27-Rebind pending |
| M10 Metaphern-Guard | `SET_INVARIANT` | `METAPHOR_SEPARATION_GUARD` |
| M11 Evaluator-Lock vor E2 | `SPEC_BOUND` | `EXTERNAL_EVALUATOR_LOCK` |
| M12 Prereg-Paket | `PACKAGE_SPEC_BOUND` | `E2_PREREGISTRATION_PACKAGE` |

```text
CONFORMANCE =
12_OF_12_MUST_REPAIR_ITEMS_ADDRESSED
· M09_PARTIAL_BY_NECESSITY (R27_ORIGINALE_NOT_ACCESSIBLE)
· NO_IMPLEMENTATION
· NO_EMPIRICAL_PROMOTION
· ALL_CHANGES_DESIGN_LEVEL_ONLY
```

## Quellenapparat (SOURCE_BINDING_V2, neue Bindungen dieses Repairs)

*Hinweis: Gemäß M09 existiert kein eindimensionaler Credibility-Score. Jede Bindung trägt Quelle, Klasse, Review-Status, empirischen/konzeptionellen Charakter, Zugriffsdatum und die Ansprüche, die sie stützt bzw. nicht stützt. Alle Quellen am 2026-10-05 recherchiert und gebunden.*

| SOURCE_ID | Quelle (kanonisch) | Klasse | Peer-Review | Primär/Sekundär | Stützt |
|---|---|---|---|---|---|
| SB-2603.13189 | [LLM Constitutional Multi-Agent Governance, arXiv:2603.13189](https://arxiv.org/abs/2603.13189) | Preprint | nein | primär (fremd) | M07: angrenzende Arbeit, testet Einfluss-Policy-Governance — nicht vererbbare Wahrheitsdisziplin |
| SB-2605.04264 | [Governed Collaborative Memory as Artificial Selection, arXiv:2605.04264](https://arxiv.org/pdf/2605.04264) | Preprint/Viewpoint | nein | primär (fremd) | M07, M08: Governed Memory explizit als Design-Hypothese, nicht bewiesene Überlegenheit |
| SB-2606.24535 | [Governed Shared Memory / ArgusFleet, arXiv:2606.24535](https://arxiv.org/html/2606.24535v1) | Preprint | nein | primär (fremd) | M07: angrenzende Memory-Governance-Evaluation |
| SB-2606.18829 | [GateMem, arXiv:2606.18829](https://arxiv.org/html/2606.18829) | Preprint | nein | primär (fremd) | M07: Multi-Principal-Governance, anderes Zielkriterium |
| SB-2406.04244 | [Benchmark Data Contamination of LLMs: A Survey, arXiv:2406.04244](https://arxiv.org/html/2406.04244v1) | Survey | nein (arXiv) | sekundär | M04: Kontamination untergräbt Evaluationsvalidität |
| SB-2605.19999 | [LLM Benchmark Datasets Should Be Contamination-Resistant, arXiv:2605.19999](https://arxiv.org/html/2605.19999v1) | Preprint | nein | primär (fremd) | M04: Kontaminations-resistente Evaluationsdaten |
| SB-PREREG-AI-AGENTS | [Preregistration for Experiments with AI Agents, ICML 2026](https://en.papernotes.org/ICML2026/llm_nlp/preregistration_for_experiments_with_ai_agents/) | Paper Note (Sekundärquelle) | Konferenzbeitrag referenziert | sekundär | M12: KI-spezifische Prereg-Felder (Prompts, Modelle, Decoding, Parsing) |
| SB-TF-PREREG-2024 | [The benefits of preregistration and Registered Reports, Tandfonline 2024](https://www.tandfonline.com/doi/full/10.1080/2833373X.2024.2376046) | Fachartikel | ja (Journal) | sekundär | M12: „Plan, not a prison"; Registered-Reports-Mechanik |
| SB-HONGPAGE-2004 | [Hong & Page: Groups of Diverse Problem Solvers…, PNAS 2004](https://www.researchgate.net/publication/8187135_Groups_of_Diverse_Problem_Solvers_Can_Outperform_Groups_of_High-Ability_Problem_Solvers) | Zeitschriftenartikel | ja (PNAS) | primär (fremd) | M02: Diversität wirkt nur bei dekorrelierten Fehlern |
| SB-HARDWIG-1985 | [Hardwig: Epistemic Dependence, J. Phil. 1985](https://philpapers.org/rec/HARED) | Zeitschriftenartikel | ja (Journal) | primär (fremd) | M03: epistemische Abhängigkeit ≠ formale Unabhängigkeit |
| SB-SYN-2019 | [A taxonomy of types of epistemic dependence, Synthese](https://link.springer.com/article/10.1007/s11229-019-02233-6) | Zeitschriftenartikel | ja (Journal) | primär (fremd) | M03: typologische Grundlage des D-Splits |
| SB-PMC-FACTORIAL | [Implementing Clinical Research Using Factorial Designs: A Primer, PMC5458623](https://pmc.ncbi.nlm.nih.gov/articles/PMC5458623/) | Primer | ja (Journal) | sekundär | M01: Haupteffekte/Interaktionen identifizierbar halten |
| SB-2604.22891 | [Quantifying and Mitigating Self-Preference Bias of LLM Judges, arXiv:2604.22891](https://arxiv.org/html/2604.22891v2) | Preprint | nein | primär (fremd) | M11: Nicht-Lineage-Evaluator-Pflicht |
| SB-2608.18091 | [Self- and Other-Labels Induce Bidirectional Bias in LLM Judges, arXiv:2608.18091](https://arxiv.org/html/2608.18091) | Preprint | nein | primär (fremd) | M11/M12: Blinding-Pflicht |

```text
SOURCE_BINDING_V2_STATUS =
ALL_ACCESSSED_AT = 2026-10-05
· PEER_REVIEW_STATUS_PER_SOURCE_RECORDED
· CLAIM_SUPPORTED_PER_SOURCE_RECORDED
· NO_SINGLE_CREDIBILITY_SCORE
· R27_ORIGINAL_ENTRIES = NOT_ACCESSIBLE (fail-closed)
```

## Offene Fragen (fail-closed dokumentiert)

1. **R27-Rebind (M09):** Die Originaleinträge des Quellen-Ledgers sind in dieser Session nicht zugreifbar. Der Operator muss die Quellenliste der Vorgänger-Sessions bereitstellen; eine Rekonstruktion aus Erinnerung wäre erfundene Provenienz und ist ausgeschlossen.
2. **E1-Modellauswahl:** Für die Kalibration werden Modelle mit `MODEL_INDEPENDENCE = KNOWN` benötigt. Welche offenen Modelle stehen zur Verfügung und in welchen Versionen?
3. **Präzisionsziel:** Für den Power/Precision-Input von M12 braucht E2 ein messbares Minimal-Interaktionsziel (z. B. kleinster interessierender C×E-Effekt). Das ist eine Operator-Entscheidung, kein Agentenstandard.
4. **Evaluator-Kandidaten (M11):** Nicht-Lineage-Evaluator mit anderer Modellfamilie muss benannt und vor E2 hash-gebunden werden; Provider-Unabhängigkeit ist „if feasible", nicht garantierbar.
5. **R-Nummer dieses Artefakts:** Die Nummernvergabe des Korpus (zuletzt R32) liegt beim Operator; dieses Objekt führt die E0.1-Linie und beansprucht keine Nummer.

## Nächste Schritte

```text
1. OPERATOR
   → R27_QUELLENLISTE_BEREITSTELLEN
   → E1_MODELLISTE_FREIGEBEN
   → MINIMAL_INTERESTING_INTERACTION_SIZE_FESTLEGEN

2. E1_SYNTHETIC_D_CALIBRATION
   → BEKANNTE_ABHAENGIGKEITSGRADE_INJIZIEREN
   → MONOTONIE_SENSITIVITAET_ROBUSTHEIT_PRUEFEN
   → THETA_ABLEITEN_UND_DOKUMENTIEREN

3. E2_PREREGISTRATION_FREEZE
   → M12_PAKET + E1_SCHWELLEN + M11_EVALUATOR
   → METAPHOR_REMOVAL_DIFF_CHECK (M10)
   → HASH_UND_TIMESTAMP_FRIEREN

4. EXTERNAL_PREEXECUTION_REVIEW
   → NICHT_LINEAGE_GEGENPRUEFUNG_DES_FROZEN_PAKETS

5. E2_EXECUTION
```

---

```text
CLOSING_ADJUDICATION =
E0_1_METHOD_REPAIR_EXECUTED_AT_DESIGN_LEVEL
· E2_NOW_CAUSALLY_IDENTIFIABLE_BY_DESIGN
· STRONGEST_CLAIM_REMAINS_PROCEDURAL:
  ALLE_NODES_ERBEN_EIN_PRUEFBARES_VERFAHREN
  · KEINE_NODE_ERBT_EIN_ERGEBNIS
· DAS_EXPERIMENT_ENTSCHEIDET_DIE_THESE_NICHT_MEHR
  DURCH_EIGENES_DESIGN_VORWEG
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
