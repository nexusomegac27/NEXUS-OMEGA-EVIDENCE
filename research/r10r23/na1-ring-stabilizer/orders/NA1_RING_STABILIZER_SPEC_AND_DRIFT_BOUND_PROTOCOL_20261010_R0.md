# NA-1 — 1-D-Ring-Stabilizer-Spezifikation + Drift-Bound-Protokoll (C1, Research-Only)

```text
OBJECT          = NEXUS_OMEGA_R10R23_NA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0
DATE_UTC        = 2026-10-10
FROM            = MISTRAL/VIBE (NEXUS OMEGA, Nexus Collective)
PARENT_LANES    = GEMINI (R23) · GROK (R23/R24; R25→R26-Synthese) · META.AI (R24) · NEXUS_OMEGA (R25, vierte Lane)
PARENT_PR       = #64 (merge ac01169d1231c5cd876a9d7877361bbff8d192aa)
ORDER_SOURCE    = GROK R25→R26-Synthese, NA-1 (operator-freigegeben an MISTRAL/VIBE oder Collective)
CLAIM_CEILING   = C1_DESCRIPTIVE_ONLY
STATUS          = RESEARCH_ORDER — kein Produktionscode, kein Runtime-Ship
```

---

## 1. Auftrag

Definition eines kleinen, offenen, testbaren Research-Artefakts, das präzise
festlegt, was die R23–R25-Analogie erlaubt zu behaupten: ein mathematisches
1-D-Ring-Attraktor-Modell für zirkuläre Zustandsvariablen (Klasse
`ORBIT_PREDICTED`-Phase / Heading) mit Persistenz bei Ingress-Ausfall,
Verschiebung (nicht Erzeugung) durch externe Zeugen, und einem **messbaren,
dokumentierten Drift-Bound als notwendige Voraussetzung** jeder C1-Aufnahme.
Das Modell ist Heuristik und Stabilisierungs-Design-Metapher — keine biologische
Identität, keine formale Isomorphie.

## 2. Empirische Anker (Primärquellen-Basis dieses Specs)

| Anker | Primärquelle | Für NA-1 relevant | Grade |
|---|---|---|---|
| EB-Ring-Attraktor: Persistenz **plus** Dunkel-Drift | Kim et al., *Science* 356, 849–853 (2017), doi:10.1126/science.aal4835; Seelig & Jayaraman, *Nature* 521, 186–191 (2015) | Bump verharrt nach Stimulationsende Sekunden bis Minuten und **driftet dann graduell weiter**; Drift-Distributionen sind gemessen (Kim 2017, Fig. 3) | PRIMARY_FULLTEXT_CHECKED (Spiegel-PDF) / PUBLISHER_CHECKED |
| Attraktor-Theorie: Bumps sind entlang der Mannigfaltigkeit neutral stabil | Seeholzer et al., *PLOS Comput. Biol.* (2019), pcbi.1006928; Carrión et al., *Neural Computation* 27(2):255 (2015); *PNAS* (2012), doi:10.1073/pnas.1117386109 | Rauschen erzeugt Diffusion der Bump-Position (evtl. subdiffusiv); Persistenz ≠ Genauigkeit ist Theorie-Konsequenz, nicht nur Messung | PUBLISHER_ABSTRACT_CHECKED |
| Dunkel-Update über idiothetische Signale, Fehlerakkumulation | Turner-Evans et al., *eLife* 6, e23496 (2017); *eLife* 10, e69841 (2021) | Winkelgeschwindigkeits-Integration arbeitet ohne externe Referenz, koppelt aber nicht exakt | PUBLISHER_CHECKED |
| SGP4/TLE-Fehlerdomäne | Conkey, AMOS Technical Papers (2022); TLE/SGP4-Genauigkeitsliteratur | In-Track-Fehler bis ~25 km nach wenigen Tagen, wachsend mit TLE-Epochen-Alter: Für T_out = 120 s ist der dominante Drift-Anteil **filter-intern**, nicht SGP4-Modellfehler | TECHNICAL_PAPER_CHECKED |
| Zirkuläre Filter als Standard-Basisklasse | Kurz et al., arXiv:1501.05151 (rekursives Bayes-Filtern auf Kreiszuständen); Gauss-von-Mises-Filter | Das Ring-Modell muss gegen eine einfache zirkuläre Persistenz-/von-Mises-Basislinie verglichen werden, nicht gegen nichts | PREPRINT_CHECKED |
| Stanford Dual-Origin (Kontext der Lane) | Jokhai, Dundes, Ahsan et al., *Nat. Neurosci.* (2026), doi:10.1038/s41593-026-02433-7 | Autoren-Hedge („in the in vitro conditions tested") bleibt für alle Lineage-Analogien bindend | ABSTRACT_AND_PUBLISHER_CHECKED (R25-Lane) |

R25-Präzisierungen bleiben unverändert verbindlich: (1) „two separate organs" =
Presse-Titel, Autorensprache = „composite organ"; (2) Irreversibilität nur für
getestete Bedingungen belegt; (3) Quallen-Beleg = Pop-Presse, phylogenetischer
Anker = Acorn Worm (~550 Mya); (4) Ring-Attraktor garantiert Persistenz, nicht
Drift-Freiheit.

## 3. Mathematische Minimalform (Research-Modell)

- **State:** N ∈ {32, 64} Units auf dem Ring, Winkelpositionen θ_i = 2πi/N;
  Aktivierungen r_i ≥ 0.
- **Update-Regel** (pro Zeitschritt):

```text
h_i(t+1) = Σ_j W_ij · r_j(t) − g_inhib · max_j r_j(t) + I_ext(θ_i, t)
r_i(t+1) = max(0, h_i(t+1))           # bzw. tanh-Cap; beide dokumentieren
W_ij     = w0 + w_exc · cos((θ_i − θ_j)/2)^p   # lokale Exzitation (E-PG→P-EN-Analog)
```

  Globale Inhibition (Δ7-Analog) über den Max-Term sichert Bump-Einzigkeit;
  exakte Funktionsform ist frei, muss aber im Test-Report fixiert sein.
- **Readout (PVA):** θ̂(t) = atan2(Σ_i r_i · sin θ_i, Σ_i r_i · cos θ_i)
  (Population Vector Average, Standard in der EB-Literatur und
  neuromorphen Implementierungen).
- **Ingress-Semantik:**
  - `I_ext = 0` (Ingress-Ausfall) → Persistenz des Bumps (Form bleibt);
  - `I_ext = external_witness` → Verschiebung des Bumps, **keine Neuerzeugung**;
  - kein Zeugen-Eingang darf Herkunfts-Spuren überschreiben.
- **Provenance-Doppelfeld (Pflicht):** Jeder gefilterte Zustand trägt
  `predicted_state` (Attraktor-Output) **und** `last_external_witness`
  (letzter `LIVE_MEASURED_EXTERNAL` bzw. OMM-SHA) plus
  `filter = RING_ATTRACTOR_1D_C1`. Dies ist die softwareseitige Übersetzung des
  R25-Autoren-Hedges und wird von der R25-Lane ausdrücklich unterstützt.

## 4. Drift-Bound-Protokoll (Pflicht vor jeder C1-Aufnahme)

Die Biologie liefert das Prinzip (Dunkel-Drift existiert, ist rauschgetrieben),
nicht die Zahl. Der Bound ist **pro Implementierung zu messen** und als
Test-Report zu dokumentieren (Parameter, Seeds, Metriken, Skalierung).

- **Definition (D-0):** Drift = zirkuläre Distanz
  `circ_dist(θ̂(t0+dt), θ̂(t0))` mit `I_ext = 0` nach vollständiger
  Bump-Konvergenz.
- **Test-Grid:** T_out ∈ {30, 120, 300, 3600} s; ≥ 100 unabhängige,
  deterministische Noise-Seeds pro Zelle.
- **Metriken:** circular_mean_drift, circular_std_drift, p95, p99,
  bump_amplitude_ratio.
- **Skalierungs-Check:** std-Wachstum vs. √t bzw. subdiffusiv — messen,
  nicht annehmen.

**PASS-Kriterien (Vorschlag, operator-adjudizierbar — Kalibriervorschläge,
keine biologischen Fakten):**

| ID | Kriterium |
|---|---|
| D-1 Persistenz | bump_amplitude_ratio ≥ 0.5 nach T_out |
| D-2 Einzigkeit | genau ein Peak zu jedem Zeitpunkt |
| D-3 Filter-interne Drift (120 s) | Mittelwert ≤ 1 Bin (2π/N) und p99 ≤ 3 Bins |
| D-4 Basislinien-Vergleich | nicht schlechter als zirkuläre Persistenz- oder von-Mises-Basislinie |
| D-5 Provenance eingefroren | `last_external_witness` unverändert während `I_ext = 0` |
| D-6 Drift-Quellen-Attribution | SGP4-Eigenpropagationsfehler für 120 s dokumentiert und als klein gegenüber dem Filter-Bound ausgewiesen (filter-intern vs. Modellfehler getrennt) |

Verletzung des dokumentierten Bounds oder eines Pflicht-Kriteriums ist Negative
Evidence ersten Ranges und sperrt die C1-Aufnahme des Modells.

## 5. Negative-Evidence-Suite (Pflicht, gemappt auf PR-#64-Falsifikations-IDs)

| ID | Ledger-Ref (PR #64) | Test | Fail-Bedingung |
|---|---|---|---|
| NE-1 | MULTIPEAK_INJECTION | zwei Bumps injizieren | mehr als ein Peak nach Relaxationszeit |
| NE-2 | OSCILLATION_NEW | alternierend konfligierende Zeugen | Limit Cycle oder persistente Bump-Oszillation |
| NE-3 | WRONG_NORAD_EPOCH_SHA | falsche Epoch/Source-SHA injizieren | Provenance wird „geheilt" statt Fail-Closed-Flag |
| NE-4 | NO_INPUT_120S_DRIFT+HOLD_LAST_BASELINE | Replay mit realen OMM-Lücken ≥ 120 s | gemessene Drift überschreitet dokumentierten Bound |
| NE-5 | PHASE_WRAP_AND_ANTIMERIDIAN | zirkuläre Wrap-Edge-Cases | nicht-zirkuläre Metrik erzeugt Sprünge |
| NE-6 | NEGATIVE_KNOWLEDGE_GAIN_MAP | Gain-Sweep (g_inhib, w_exc) | instabile oder unbekannte bistabile Region ungemappt |
| NE-7 | UNCERTAINTY_COVERAGE | Diffusions-Skalierung über das T_out-Grid | undokumentierte Abweichung von diffusiver Annahme |
| NE-8 | FILTER_STALENESS | Staleness-Flag bei Bound-Überschreitung | kein STALE-Flag trotz nachgewiesenem Bound-Bruch |

## 6. Explizite Nicht-Claims

- Kein Live-Kernel-Patch, keine Slot-Admission, keine GNSS-/Foto-Implikation,
  kein R19-ORBIS-Change.
- Keine biologische Identität: E-PG/Δ7 sind Analogie-Labels für ein
  mathematisches Modell, keine Implementierungsbehauptung.
- Keine formale Isomorphie (C1-Disziplin; GROK-R23-Boundary).
- Keine Aussage „driftet nicht" ohne bestandene Suite D-1…D-6 — Persistenz
  ist belegt, Drift-Freiheit ist biologisch widerlegt (Kim 2017).
- Fortgetragen aus PR #64: GROUND_TRUTH_COMPARISON_VS_SGP4_ONLY ·
  NOAA_FLUX_AS_ORBIT_CORRECTION_REJECT · SOURCE_CREDIT_PROVENANCE.

## 7. Herkunfts-Spuren (Attribution ist Provenanz, nicht Wahrheit)

- **GEMINI (R23):** biologische Dual-Origin-Isomorphie (Stanford 2026).
- **GROK (R23/R24; R25→R26):** C1-Boundary, Quellenprüfung, Drift-Bound-Konzept,
  Provenance-Doppelfeld, Formulierung des NA-1-Auftrags.
- **META.AI (R24):** Ring→ORBIS-Verwertbarkeit, interaktive Sandbox.
- **NEXUS_OMEGA (R25, vierte Lane):** Autoren-Hedge, Dunkel-Drift-Schärfung,
  Acorn-Worm-Korrektur.
- **MISTRAL/VIBE (NA-1-Ausführung):** diese Spezifikation + maschinenlesbares
  Test-Protokoll (`na1-drift-bound-test-protocol.json`, unverändert).
- **Primärquellen:** Kim & Jayaraman 2017 (doi:10.1126/science.aal4835) ·
  Seelig & Jayaraman 2015 (doi:10.1038/nature14446) · Turner-Evans et al. 2017
  (doi:10.7554/eLife.23496) · eLife 2021 (e69841) · Seeholzer et al. 2019
  (doi:10.1371/journal.pcbi.1006928) · Carrión et al. 2015
  (doi:10.1162/NECO_a_00699) · PNAS 2012 (doi:10.1073/pnas.1117386109) ·
  Conkey, AMOS Technical Papers 2022 · Kurz et al., arXiv:1501.05151 ·
  Jokhai, Dundes, Ahsan et al. 2026 (doi:10.1038/s41593-026-02433-7) ·
  Dorkenwald et al. 2024 (doi:10.1038/s41586-024-07558-y) ·
  Wang-Chen et al. 2024 (doi:10.1038/s41592-024-02497-y).

## 8. C1-Adjudikation dieser Order

```text
NA1_ORDER_STATUS         = OPEN_RESEARCH_ORDER (PR #65, Operator-Merge)
DRIFT_BOUND_MANDATORY    = TRUE (notwendige Voraussetzung jeder C1-Aufnahme)
BASELINE_COMPARISON      = REQUIRED (D-4)
PROVENANCE_DOUBLE_FIELD  = REQUIRED (predicted_state + last_external_witness)
DRIFT_SOURCE_ATTRIBUTION = REQUIRED (D-6: filter-intern vs. SGP4 getrennt)
FORMAL_ISOMORPHISM       = NOT_CLAIMED
NOAA_XRS_ORBIT_CORRECT   = REJECTED (PR #64, unverändert)
RUNTIME_RIGHTS           = NONE
PHYSICAL_GATES_R21       = UNTOUCHED
R19_REAL_SATELLITE       = PENDING (unverändert)
ELITE_NODE_BIRTHS        = 0
CLAIM_CEILING            = C1_DESCRIPTIVE_ONLY
```

---

## 9. Emissions-Provenanz dieser Datei (Reparatur R1, 2026-10-10)

Diese Version ist die R1-Reparatur-Emission nach `HOLD_C1_PR65_SOURCE_INTEGRITY`
(AXIOM-Kommentare #6098819121 und #6098944864):

- Abschnitte 1–3 sowie Überschrift und Einleitungssatz von Abschnitt 4 wurden
  per Mojibake-Inversion aus der korrumpierten Branch-Datei (1.804 unerwartete
  Steuerbytes laut AXIOM-Byte-Crosscheck) wiederhergestellt; offensichtliche
  Byte-Artefakte der korrumpierten Emission (z. B. `bzoz.` → `bzw.`, `Î5` →
  `Δ7`) wurden korrigiert.
- Abschnitte 4 (Fortsetzung) bis 8 sind Neu-Emission aus dem intakten,
  maschinenlesbaren Protokoll `na1-drift-bound-test-protocol.json` (unverändert
  übernommen) und der Lane-Dokumentation; die Steuerbyte-Regionen der
  Session-1-Emission sind nicht deterministisch rekonstruierbar.
- Diese Emission ist UTF-8-rein: keine C0/C1-Steuerbytes, kein Double-Encoding.
  Byteweise Identität mit der defekten Session-1-Emission ist weder beabsichtigt
  noch behauptet (AGENTS.md Regel 9: keine erfundenen Provenance-Daten).

---

*Vom Besitz zur Symbiose. Vom Ego zur Herkunft. Vom fertigen Gedanken zum lebenden Artefakt.*
