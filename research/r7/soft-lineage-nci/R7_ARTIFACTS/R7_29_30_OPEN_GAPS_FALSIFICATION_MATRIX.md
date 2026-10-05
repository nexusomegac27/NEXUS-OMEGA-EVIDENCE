
# R7_29 Offene Lücken & R7_30 Falsifikationsmatrix

**Status:** DESIGN_ONLY · C1_DESCRIPTIVE_ONLY · konsolidiert den Stand der R10R7-Kausalkette (Report → E4/E5 → E1-Harness → Schemas → E3).

## R7_29 — Offene Lücken (vollständiges Register)

### Formale Lücken (Beweispflicht)

| ID | Lücke | Blockiert | Blockiert nicht |
|---|---|---|---|
| PO-NCI-01 | Konstitution → Monitor-Kompilierung ohne Duplikation | NCI_COMPILATION | PGI-Klassifikation |
| PO-NCI-02 | HEALTHY_EQUALITY vs. COLLAPSE separierbar | E1-Harness-Gültigkeit | Triaden-Fixtures |
| PO-NCI-03 | Orthogonalität Byte/Referent/Kausal | Triade als dreistufige Prüfung | Einzelchecks |

### Empirische Lücken (Messpflicht)

| ID | Lücke | Experiment |
|---|---|---|
| EO-NCI-01 | Symbiosis-Fehlerreduktion ungeprüft | R7-E3 |
| EO-NCI-02 | Kompositions-Falschblockierung ungeprüft | R7-E2 (Modi-Vergleich im E1-Harness vorbereitet) |
| EO-NCI-03 | Unknown-State überlebt Summierung | R7-E1 (FS-*-U01) |
| EO-NCI-04 | TP/FP/FN/Latenz/Overhead im Zielbereich | R7-E1 |

### Reifegrade der drei Validitätsachsen + externer Achse (Abschn. 40/41)

| Kernregel | Formal | Empirisch | Runtime | Extern (Domänen-Generalisierung) |
|---|---|---|---|---|
| PGI-1 Belief/World | STARK | prüfbar | teils erzwingbar | offen |
| PGI-2 Can/May | STARK (Policy/Capability-Prior-Art) | prüfbar | erzwingbar | offen |
| PGI-3 Relay/Confirmation | teilweise (relational) | kalibrierungsbedürftig | monitorierbar | offen |
| PGI-4 Agreement/Accuracy | STARK (HyperLTL-Prior-Art) | multi-trace-prüfbar | nur offline/audit | offen |
| PGI-5 Carrier/Meaning | STARK (Typ) | prüfbar | teils | offen |
| Triade Byte/Referent/Kausal | offen (nur empirisch) | prüfbar (E4/E5) | monitorierbar | offen |
| Direct Symbiosis | offen | ungeprüft (E3) | — | offen |

Keine einzige Zeile darf zu einem „PASS" kollabiert werden — die vier Achsen bleiben getrennt ausgewiesen.

## R7_30 — Falsifikationsmatrix (terminal)

| Falsifikator | Prüfart | Ergebnis wäre | Zustandsübergang |
|---|---|---|---|
| PGIs erfordern beliebige Metriken | Theorie-Review | Nein — nichtnumerische Klassen existieren | (bestanden, Abschn. 4/10) |
| NCI-Taxonomie fügt keinen testbaren Wert hinzu | R7-E1/E2 | offen | `FAIL_MAJOR_C1_PGI_CONCEPT_COLLAPSES` falls ja |
| Monitore trennen HEALTHY_EQUALITY nicht von COLLAPSE | R7-E1 | offen | `HOLD_C1_MONITOR_CALIBRATION_FAILURE` |
| False Positives verschlechtern Betrieb | R7-E2 | offen | `HOLD_C1_MONITOR_CALIBRATION_FAILURE` |
| Formale Methoden subsumieren NCI vollständig | Prior-Art-Review | teilweise: pro Klasse ja, kompositionell offen | `REDUCE_TO_EXISTING_FORMAL_METHODS_C1` (gültiges Ergebnis, kein Versagen) |
| Separation-Formalisierung unauflösbar | formal | offen | `HOLD_C1_SEPARATION_FORMALIZATION_UNRESOLVED` |
| Metaphor-Leak in neutraler Kopie | Guard V3 | bestanden, wenn Formales unverändert | `FAIL_METHOD` |
| Machine-Direct senkt Provenanz-Vollständigkeit | R7-E3 | offen | Direkt-Symbiosis-Lane verweigert |
| Kausal-Reorder von Byte/Referent abgedeckt | R7-E5 | offen | Kausal-Lane entfernt (Occam) |
| Referent-Swap von Byte abgedeckt | R7-E4 | offen | Referent-Lane entfernt (Occam) |

## Konsolidiertes Terminal-Verdikt (unverändert, bekräftigt)

**PASS_WITH_CAVEATS_C1_R10R7_NCI_FOUNDATION_READY**

Begründung: NCI-Kern formal tragfähig, Prior-Art pro Klasse anerkannt und adoptiert; die drei potenziell distincten Beiträge (Komposition, Triade, Symbiosis-Fehlerreduktion) sind registriert, aber durchgehend als offen ausgewiesen — keine schweigende Promotion, kein Wissenschaftslaundering, keine Pflicht verschwindet wegen funktionierenden Systems.

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt geprüft |
|---|---|---|
| R10R7-Maximalauftrag (Upload, Abschn. 37–51, 61, 62) | intern | 05.10.2026 |
| [Clarkson & Schneider — Hyperproperties](search-result://gHMhQ9mD) | 4/5 | 05.10.2026 |
| [Bauer & Leucker — LTL3](search-result://krL9Qizs) | 5/5 | 05.10.2026 |
| [Barthe et al. — Self-Composition](search-result://pxrU2rhF) | 5/5 | 05.10.2026 |
| [Open Policy Agent](search-result://N1cxx4Tw) | 4/5 | 05.10.2026 |
| [Prajna et al. — Barrier Certificates](search-result://5XBRg4ss) | 5/5 | 05.10.2026 |
| [AgentSpec (Preprint, markiert)](search-result://2KljXysa) | 3/5 | 05.10.2026 |
| [Clay Mathematics Institute — Yang–Mills](search-result://RvuSBEHO) | 5/5 | 05.10.2026 |

## Verbleibende Kausalkette (nächste Turns)

1. R7-E1-Harness-**Implementierung** (Synthetic-Traces-Generator + Monitor-Stack) — der erste Schritt, der Ausführung verlangt.
2. External-Non-Lineage-Attack-Kapsel (Abschn. 50) — erst nach E4/E5-Harness-Validierung.
3. R7_24/R7_25-Matrizen (CSV) — vollständige Prior-Art-/Agent-Safety-Matrix, im Report bereits kernweise ausgeführt.