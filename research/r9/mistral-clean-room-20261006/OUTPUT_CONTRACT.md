# Mistral Return Contract — N00 bis N17

Die folgenden Dateien sind geforderte künftige Reviewer-Ausgaben. Das Auftragspaket enthält keine vorgetäuschten N-Ergebnisse. UTF-8, eindeutige JSON-Schlüssel, keine NaN/Infinity-Werte; CSV mit Header und korrekt gequoteten mehrzeiligen Feldern. Hashes immer über physische Bytes, ohne stilles Normalisieren.

| Datei | Mindestinhalt |
|---|---|
| N00_PRE_BOT_FREEZE.json | Phase-1-Urteile und Quellen; Modell/Version soweit bekannt; Vorexposition; Mechanismusmodell; A/B/C; Reduktion und stärkstes Gegenargument; offene Annahmen; Zeit |
| N01_BYTE_INTAKE_RECEIPT.json | Paket-Commit, ORDER-Hash, Input-/Manifest-Hashes, erwartete/beobachtete Bytes, ZIP-/G24-Checks, N00-Hash, Abrufzeit, Lücken |
| N02_ORIGINAL_R10R9_WORDING_LEVEL_CLAIM_AUDIT.md | jede materielle Originalbehauptung einschließlich PASS/FAIL- und Schlussfolgerungssätzen, exakte Fundstellen und korrigierte Formulierungen |
| N03_PRIMARY_SOURCE_CORRECTION_LEDGER.csv | claim_id,original_location,source_title,source_url,version,date,accessed_at,source_class,source_location,status,supports,does_not_support,correction,uncertainty,falsifier,impact |
| N04_GROKBOT_DISCREPANCY_MATRIX.csv | D01–D10 und alle zusätzlichen Findings; BOT-Aussage vs. Reviewer-Befund, Primärbeleg und Materialität |
| N05_SOFT_LINEAGE_MECHANISM_DEMARCATION.md | C/M/E/P/L-Definitionen, ARCH_A0/A1/A2, P_TASK/P_ALL, Implementierungsstatus, Standardreduktion, Teil-A-Urteil |
| N06_PART_A_FACTORIAL_INDEPENDENT_RECALCULATION.md | Design-/Alias-Matrix, Kontraste, alle geforderten Interaktionen, Placebo/None-Arme, Formeln, Einheiten, DEFF/ICC/MESOI-Sensitivität, Parsing/Judge/Leakage |
| N07_A_MIN_LITE_VS_A_MIN_VS_FULL_DESIGN.md | identifizierbare und nicht identifizierbare Effekte, Tasks/Runs/Calls, Präzision, Kostenfunktion, Confounds und kleinster sinnvoller Test |
| N08_R10R8_CAUSAL_DEFECT_REPAIR_LEDGER.md | Original/R1/aktueller Geltungsbereich mit Datei-/Hash-/Zeilenbindungen, nicht ausgeführte Prüfung als solche, Restpflichten |
| N09_AIR_GAP_TO_UNRESOLVED_NCI_MIGRATION_SPEC.md | Zustands-/Relationstypen, GATE5-Übergangstabelle, epistemische vs. Autorisierungsebene, Kompatibilität, geplante Fixtures; keine Implementierung |
| N10_PART_C_TRUST_MODEL_AND_STANDARDS_REDUCTION.md | C-SYNTH/C-REAL, Angriffsmatrix, Standards-Crosswalk, vollständige Trust-Bedingungen, Claim-Ceiling-Ordnung/Attenuation und Rest |
| N11_PART_B_PH_AND_BASELINE_RECHECK.md | Primärliteratur, Pipelinevergleich, faire Abstention, Risk-Coverage, B0-Freeze-Bedingungen, B1-Datenlücken |
| N12_NEXUS_RESIDUAL_REDUCTION_ANALYSIS.md | Komponenten-/Framework-/Metaphernreduktion, stärkstes Anti-NEXUS-Argument, stärkster verbleibender Gegenbefund, Suchgrenzen |
| N13_DIRECT_SYMBIOSIS_EMPIRICAL_HYPOTHESIS.md | Vorregistrierbares Relay-vs-direkt-Design, Komponentenablationen, Fehlertaxonomie/Nenner, primäre Metrik und Falsifikator; nicht durchgeführt |
| N14_ORDER_REFERENTIAL_CLOSURE_AUDIT.md | ungebundene Begriffe/Dateien/Symbole/Zustände/Terminalpfade, externe Abhängigkeiten, Annahmenregister und genaue Lane-Abhängigkeiten; kein globaler Glaubwürdigkeits-Score |
| N15_FINAL_CLEAN_ROOM_CHECKPOINT_VERDICT.md | Antwort auf zentrale Frage zuerst, primärer Checkpoint-Zustand, A/B0/B1/C-SYNTH/C-REAL-Empfehlungen, D01–D10, falsifizierbare Umkehrbedingungen, keine Freigabe |
| N16_MANIFEST_SHA256.json | alle Return-Dateien außer N16 selbst: relativer Pfad, Bytes, SHA-256; N17 eingeschlossen; N00 unverändert |
| N17_HANDSHAKE.json | role, object, in_reply_to, source_commit, order_sha256, input_manifest_sha256, n00_sha256, primary_state, lane_states, corrections, assumptions, unresolved, execution_authorized=false, github_writes=false, r10r6_e2=PROHIBITED, node_activation=false, promotion=false, delivery_status, next_actor=AXIOM |

Hash-Reihenfolge ohne Kreis: N00 einfrieren → übrige Berichte und N17 abschließen → N16 berechnen → N16-Hash im begleitenden Return nennen. N17 enthält keinen Hash des noch nicht fertigen N16. Ein optionaler ZIP wird zuletzt berechnet und im Return separat gebunden. Keine Datei enthält einen erfundenen eigenen Hash oder die noch unbekannte eigene Commit-ID.

Das Auftragspaket bezeichnet `HANDSHAKE.json` ausschließlich als ausgehenden Handoff, nicht als Mistral-ACK. N17 ist erst nach tatsächlicher Review-Erstellung eine Reviewer-Antwort. Bei Limitierung keine ACK-/Ausführungs-/Vollständigkeitsbehauptung ohne physisch vorhandene Ausgaben.
