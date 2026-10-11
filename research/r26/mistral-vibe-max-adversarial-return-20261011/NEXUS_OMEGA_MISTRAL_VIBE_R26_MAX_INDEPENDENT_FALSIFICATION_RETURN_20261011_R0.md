# NEXUS OMEGA · R26 MAX — Unabhängiger Falsifikations- und Quellen-Audit

**Ausführungslane:** MISTRAL/VIBE (adversarielle Zweitprüfung des an Perplexity gerichteten MAXIMALAUFTRags; kein Perplexity-Handshake simuliert) · **Datum:** 2026-10-11 · **Claim-Deckel:** C1_DESCRIPTIVE_ONLY

```text
OBJECT = NEXUS_OMEGA_MISTRAL_VIBE_R26_MAX_INDEPENDENT_FALSIFICATION_RETURN_20261011_R0
PARENT_OBJECT = NEXUS_OMEGA_AXIOM_TO_PERPLEXITY_R26_MAX_INDEPENDENT_FALSIFICATION_SOURCE_AUDIT_AND_PREREG_PREPARATION_20261011_R0
PARENT_ORDER_FETCH = FETCHED_WEB_NOT_CONNECTOR (immutable RAW @ d2995b78, 29785 chars gelesen)
PINNED_R26_PARENT_MAIN = 6dd070f10e58d8885c1d9eaccf22a6f71a272d42
PR70 = OPEN_UNMERGED_AT_ASSIGNMENT (R26-03_R1 @ 41ab803d vollständig gelesen, 12213 chars)
REPO_FETCH_MODE = FETCHED_WEB_NOT_CONNECTOR (GitHub RAW/API, Commit-gebunden; kein authentifizierter Write-Connector)
GITHUB_TRANSPORT = CAPABILITY_GAP (keine Operator-Schreibautorisierung; Chat/Canvas ist kein kanonischer SEND-Receipt)
PERPLEXITY_RECEIVE_ACK = PENDING (durch diese Ausführung nicht verändert)
PRIMARY_SOURCES_DIRECTLY_READ = 2_FULLTEXT_OR_ABSTRACT (Noorman 2024, Seeholzer 2019) + 5 bibliografisch verifiziert
COUNTEREVIDENCE_CASES = 6 EXECUTED_EXPLORATORY + 22 DESIGN_ONLY (Familien E1–E28)
THEOREM_PROVEN = 3_SCOPED (Spektrum-Identitäten; Homogenität/Konsistenzbedingungen; EB1′-Suffizienz/Unidentifizierbarkeit)
COUNTEREXAMPLE_FOUND = 2_SCOPED (Zwei-Peak-Nichteinzigkeit; EB1′-Attributionsdoppelzerlegung)
MODEL_MAX_VS_SUM_WINNER = NOT_ESTABLISHED (neue explorative Evidenz GEGEN den nackten MAX-Arm im Testregime)
D1_KERNEL_FREEZE = NO
D2_INHIBITION_FREEZE = NO
D3_CAUSAL_ATTRIBUTION = NOT_ESTABLISHED
NF05_NF06 = DESIGN_ONLY_NOT_EXECUTED
EXPERIMENTS = EXPLORATORY_SYNTHETIC_WITH_LOGS (deterministische Eigenrechnung; keine präregistrierten Trials)
R26_FULL_SCIENTIFIC_TERMINAL = NO
R26_WWW_DEPLOY = NOT_VERIFIED
NEW_CURSOR_WORKER = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

---

## Frage (Auftragsinterpretation)

Ist NA-1 als formal definiertes mathematisches Modell konsistent? Welche behaupteten Eigenschaften des S¹-Ringkerns (K_B-Spektrum, Bump-Existenz, Bump-Einzigkeit, MAX- vs. SUM-Inhibition) sind beweisbar, widerlegt, parameterabhängig oder unidentifizierbar? Welcher präregistrierbare Test (NF-05/NF-06) hätte maximale Falsifikationskraft? Was darf unter C1 behauptet werden? Die Anweisung des Auftrags — stärkste Widerlegung zuerst — wird in den Befunden wörtlich umgesetzt.

## Executive Summary — stärkste Befunde zuerst

1. **Gegenbefund gegen die MAX-Hoffnung (neu):** Am einzigen Bump-Konsistenzpunkt des nackten MAX-Arms (N=32, K_B k=8, g≈1.9807, aktiver Bogen L=5) ist die Fixpunktfamilie **linear instabil** (größter Jacobi-Eigenwert λ≈1.0378, nicht-radial). Ein-Bump-Starts divergieren in der Amplitude; uniforme Anregung wächst exakt mit **s̄−g = 6.2842−1.9807 = 4.3033 pro Schritt** (analytische Vorhersage und Numerik stimmen auf 4 Stellen). Der nackte MAX-Arm stabilisiert in diesem Regime nichts — nicht einmal den von ihm selbst getragenen Bump. *Scope: deterministisch, ein k, ein N, Kontiguierliche-Bogen-Klasse; kein Theorem.*
2. **Gegenbefund gegen die NA-1-Kategorialaussage „Max-Term sichert Bump-Einzigkeit":** Asymmetrische Zwei-Peak-Injektion (1.0/0.8) bleibt im MAX-Arm **dauerhaft zwei-gipflig** (Verhältnis 0.82, divergent) — kein Winner-take-all. Im SUM-Arm **kollabiert** die Anregung vollständig (beide Peaks sterben). **Kein Arm zeigt Ein-Bump-Einzigkeit** im nackten, deterministischen Betrieb. Die Kategorialaussage ist endgültig zu demotivieren; NE-1 (MULTIPEAK_INJECTION) bleibt der einzig entscheidende Prüfpfad.
3. **Positive Homogenität trifft BEIDE Arme (maschine-exakt, Abweichung ≤7e-15):** Jeder nichtnullen Fixpunkt beider Arme ist Element einer **Strahl-Familie** {α·r\*}; radialer Eigenwert exakt 1 (Euler-Homogenität); isolierte asymptotische Stabilität ist in beiden nackten Armen ausgeschlossen. **Korrektur einer naheliegenden Fehlannahme:** Auch der SUM-Arm hat die Amplitudenfamilie — die Fixpunktgleichung beider Arme ist skaleninvariant; SUM bricht die Amplitudenfreiheit **nicht**. Konsequenz: Amplituden-Normierung/Sättigung ist Pflichtfeld für JEDE Drift-Bound- und EB1′-Interpretation, in beiden Armen. Zugleich (Gegenüberbehauptung, §IV.3d): Fehlende isolierte Stabilität ≠ Instabilität — der SUM-Arm zeigt eine **formstabile, anziehende Familie** (Störungen heilen bis 5.6e-15 auf den Strahl aus); Familienattraktion bleibt möglich.
4. **Kein Primärquellen-Anker für den MAX-Operator:** Noorman et al. 2024 (Volltext, Open Access) verwenden eine **symmetrische Kosinus-Gewichtsmatrix, lokale Erregung + breite Inhibition, threshold-lineare Antwortfunktion** mit „active submatrix" — **kein MAX-Operator** im Modell. MODEL_MAX ist damit eine NEXUS-interne Designhypothese ohne Anker in der geprüften Referenzliteratur; MAX/SUM-Rangfolge bleibt NOT_ESTABLISHED (kein MAX_WINS, kein SUM_WINS).
5. **Bestätigungen (unabhängig, ≤1e-15):** K_B-Spektrum a_m = 2·C(2k, k−m)/4^k; c₂/c₁ = (k−1)/(k+2) = R(k) **strikt steigend**, R′(k) = 3/(k+2)² > 0, 1−R = 3/(k+2) — die AXIOM-R1-Korrektur war korrekt. **Neu quantifiziert:** Aliasing verfälscht das Modenverhältnis c₂/c₁ auf dem geplanten Raster (k ≤ 16, N ∈ {32, 64}) praktisch nicht (Kontamination von Mode 2 erst ab k ≳ N−2; beobachtet ≤1.4e-11 erst bei k=40, N=32).
6. **EB1′-Kausalkraft widerlegt als Lesart, bestätigt als Screen:** Bei r = f+u mit ‖u‖ ≤ B sind **zwei verschiedene, jeweils zulässige Zerlegungen** möglich (u = 0 vs. u = −3r̂ bei B=6, ‖r‖=10) — die kausale Attribution (Epoch- vs. Modellfehler) ist aus dem Residuum allein **unidentifizierbar**. B < ‖r‖ ist hinreichend für f≠0, nicht notwendig, und kein Kausalnachweis. EB1′ bleibt ausschließlich konservativer Joint-Screen (Gegenbeispiel 6+5=11>10 bestätigt).
7. **Quellen ohne Widerspruch:** Alle Pflichtkandidaten existieren mit korrekten DOIs — Noorman 2024, Laing & Troy 2003, Seeholzer 2019, Kim 2017, Seelig & Jayaraman 2015, Turner-Evans 2017, Dual-Origin 2026. Keine SOURCE_CONTRADICTION. Presse-Titel („two separate organs") und Autorensprache („composite organ") bleiben wie in R23 dokumentiert zu trennen.
8. **SGP4/TLE 1–2 km/Tag sind Katalog-Literaturwerte**, keine objektbezogenen D6-Messungen. Die R26-Korrektur des NA-1-Urtexts wird bestätigt; ein objektspezifisches Fehlerbudget erfordert eine unabhängige Ground-Truth-Quelle.

## Methodik

- **Eigenrechnung (EXPLORATORY_SYNTHETIC_ONLY):** deterministische TypeScript-Berechnungen (replayfähig, keine Rausch-/Prereg-Versuche): geschlossene Fourier-Koeffizienten vs. spektral-genauer periodischer Trapezquadratur (M=4096/8192); Gauss-Jordan mit Teilpivotisierung; explizite Aktivbogen-Konstruktion von Fixpunkten mit Konsistenzbedingungen; harte Verifikation F(r\*)=r\* ≤ 1e-9; FD-Jacobian (ε=1e-6) mit Potenziteration (600 Schritte) und radialer Deflation; Trajektorientests (≤3000 Schritte) mit deterministischen Initialisierungen.
- **Quellenzugang:** öffentliche immutable GitHub-RAW/API-URLs (`FETCHED_WEB_NOT_CONNECTOR`, Commit-gebunden: d2995b78 für den Auftrag, 41ab803d für R26-03_R1), Europe PMC REST (Abstract + Volltext-XML), Semantic Scholar Graph API (Bibliografie, Autorenlisten), PLOS-Volltextseite, Web-Suche. Kein GitHub-Schreibzugriff; kein Connector-Rehash eigener Bytes behauptet.
- **Grenzen:** PR #70 wurde nicht Byte-für-Byte neu gerehasht (nur R26-03_R1 vollständig gelesen); Amari-Zeugen W1–W4 nicht re-verifiziert (fehlende Parametersätze → weiterhin NOT_INDEPENDENTLY_REPRODUCIBLE); Dynamiktests nur bei N=32, k∈{2,4,8,16} (Existenz) bzw. k=8 (Dynamik), ohne Rauschen, Sättigung, externen Stimulus; Nature-/PubMed-/ADS-Seiten teilweise durch JS-Challenge/CAPTCHA blockiert (Ausweichwege: Europe PMC, Semantic Scholar).

## Befunde

### Achse A — S¹-Kern, Fouriermoden, Homogenität, Existenz vs. Stabilität

**A.1 Spektrum (CONFIRMED, exakt).** Eigenständige Herleitung: K_B(Δ) = cos^{2k}(Δ/2) = 4^{−k}·Σ_j C(2k,j)·e^{i(j−k)Δ} ⇒ a_m = 2·C(2k, k−m)/4^k. Verifikation gegen R26-03_R1-Tabelle: k=8 → c₁ = 0.174561, c₂ = 0.122192, R = 0.700 ✓. Geschlossene Form und spektrale Quadratur stimmen auf ≤1.9e-15 überein (nach Korrektur eines eigenen Quadraturfehlers, s. Reproduzierbarkeit). R(k) strikt steigend, R′ = 3/(k+2)² > 0, 1−R = 3/(k+2) — R26-03_R1 §4 bestätigt; die historische R0-Richtungsaussage bleibt zu Recht zurückgezogen.

**A.2 Aliasing (NEU, quantifiziert).** Diskrete Koeffizienten bei N ∈ {32, 64}: Mode m wird erst kontaminiert, wenn k ≥ N−m (erste Überlappung |n| ≡ m mod N innerhalb der Spektralstütze |n| ≤ k). Für das Metrik c₂/c₁ bedeutet das: bei N=32 erst ab k ≳ 30 relevant (beobachtete Abweichung 1.4e-11 bei k=40). Auf dem geplanten Grid (k ≤ 16) ist die Metrik alias-robust; der E5-Fall ist damit für dieses Metrik entkräftet, gilt aber weiterhin für hochmodige Kenngrößen.

**A.3 Positive Homogenität (CONFIRMED, beide Arme).** F_MAX(r) = ReLU(Wr − g·max(r)·1), F_SUM(r) = ReLU(Wr − g·sum(r)·1): F_P(αr) = α·F_P(r) für α>0, numerisch exakt (0 bis 7.1e-15). Analytisch folgen Strahlfamilien {α·r\*} und radiale Eigenrichtung mit Eigenwert exakt 1 (Euler). **Beide Arme gleich betroffen** — die Fixpunktgleichung ist in beiden Fällen homogen vom Grad 1; auch SUM hat die Amplitudenfamilie.

**A.4 Fixpunkt-Existenz (NEU: explizite Konstruktion + hinreichende Bedingungen pro Arm).** Für zusammenhängende aktive Bögen A (Breite L, zentriert) und Ring-Kernel K_B: r\* lösst (I−W_A)·r_A = −g·χ·1_A mit χ = max (MAX-Arm) bzw. χ = Σ_A r (SUM-Arm). Konsistenzbedingungen (hinreichend innerhalb dieser Klasse): **g_max = −1/[(I−W_A)^{-1}·1]_Zentrum**, **g_sum = −1/Σ[(I−W_A)^{-1}·1]**. Gefundene, hart verifizierte Bump-Familien (Residuum ≤ 8.9e-16):

| k | MAX: L, g | SUM: L, g |
|---|---|---|
| 2 | L=7, g=3.5902 | L=7, g=0.7436 |
| 4 | L=7, g=2.6301 | L=7, g=0.6808 |
| 8 | L=5, g=1.9807 | L=5, g=0.6050 |
| 16 | L=5, g=1.3492 | L=5, g=0.5107 |

Existenz eines Bump-Gleichgewichts ist damit in beiden Armen konstruktiv belegt (Klasse: kontiguierlicher Bogen, N=32). **Einzigkeit der Position** gilt trivial bis Ringrotation; **Einzigkeit der Form/Amplitude** folgt daraus nicht (s. Befund 2).

**A.5 Stabilitätsasymmetrie (NEU, entscheidend).** Am eigenen Konsistenzpunkt (k=8): MAX-Arm λ_max ≈ 1.0378 (Eigenvektor senkrecht zur radialen Richtung), Trajektorien divergieren in der Amplitude (Uniform-Start: Wachstum exakt s̄−g = 4.3033/Schritt; s̄ = Zeilensumme = 6.2842). SUM-Arm: λ_form ≈ 0.979 < 1, Formstörungen heilen aus (5.6e-15), Ein-Bump-Start konvergiert auf den Strahl (1.6e-14). **Interpretation (vorsichtig):** ein einzelner, deterministischer, parameterfixierter Datenpunkt — kein Theorem über MAX vs. SUM. Er widerlegt aber jede Aussage, Existenz eines Bumps im MAX-Arm sei bereits stabilisierend; und er liefert das erste konkrete Diskriminans GEGEN den nackten MAX-Arm im Testregime.

### Achse B — MODEL_MAX vs. MODEL_SUM, fairer Vergleich

**B.1 Dimensionsabhängigkeit (quantifiziert).** Bei identischem Zustand skaliert die SUM-Inhibition mit N: im Testfall (N=32, k=8) beträgt die Gesamtinhibition des SUM-Arms g·Σr ≈ 0.605·(aktive Summe) vs. g·max = 1.98 im MAX-Arm — die Inhibitionsdifferenz zwischen den Armen ist damit primär **dimensions- und zustandsabhängig** (Faktor ≈ 9.8 auf Einheits-Peak-Basis bei N=32). Identische-g-Vergleiche (Design A) vergleichen daher strukturell verschieden starke Inhibition. Design B (g_eff-Kalibrierung auf gleiche stationäre Gesamtinhibition) oder die registrierte **sum/N-Variante** (Noorman: 1/N-Summation über die aktive Untermenge) sind zwingend vorab zu fixieren — exakt die Forderung von R26-03_R1 §5 („matched normalisation"). Cross-g-Tests bestätigen die Empfindlichkeit: MAX-Arm mit SUM-g (0.605) → Plateau/Multi-Zustand; SUM-Arm mit MAX-g (1.981) → Totalkollaps.

**B.2 Zwei-Peak-Injektion (NE-1-Vorschau).** Symmetrischer Zwei-Peak-Start bleibt (deterministisch erwartbar) in der Symmetrieklasse; asymmetrischer Start (1.0/0.8) ist das eigentliche Diskriminans: MAX → beide Peaks persistieren und divergieren gemeinsam (0.82); SUM → Totalkollaps. **Konsequenz für NF-05:** Tests müssen asymmetrische und verrauschte Injektionen enthalten; reine Symmetrie-Starts können Einzigkeit nicht prüfen. Erwartungsausgänge vorab registrieren: KOLLAPS vs. WTA vs. PERSISTENT_MULTI pro Arm.

**B.3 Rangfolge-Verdikt.** MODEL_MAX_VS_SUM_WINNER = NOT_ESTABLISHED. Kein Gegenbeispiel gegen die R26-03_R1-§5-Hypothese („MAX erlaubt Multi-Peak über größere Region bei gematchter Normierung") — mein Datenpunkt ist richtungskonsistent mit ihr (MAX permissiver, SUM restriktiver), aber ohne gematchte Normierung und mit Divergenz statt stabiler Zustände. NE-6 mit gematchten g_eff bleibt der geforderte Weg.

### Achse C — NF-05/NF-06 Freeze-Kandidat ( kondensiert, DESIGN_ONLY)

```json
{
  "object": "NF05_NF06_PREREG_FREEZE_CANDIDATE_20261011_DRAFT",
  "execution_authorized": false,
  "klassifikation": "NEW_PROPOSAL",
  "pflichtfelder_vor_ausfuehrung": {
    "aktivierung": "threshold-linear (Noorman-Stil) VS ReLU — explizit zu fixieren; Homogenitaet bricht erst durch Sattigung, Bias oder Normierung",
    "amplituden_normierung": "PFLICHT: Peak-Normierung pro Schritt oder Sattigung; sonst ist Drift-Bound wegen Strahlfamilie nicht interpretierbar (beide Arme)",
    "kernel": "K_B, k deklariert; wrap(x)=atan2(sin x, cos x) vor Potenz; K(0)=1; Masse M_k=2*pi*C(2k,k)/4^k deklariert",
    "g_kalibrierung": "g_eff nur auf Trainingsdaten; keine Test-Leakage; sum/N-Variante als eigener Arm registriert",
    "dt_und_zeitschritt": "explizites Deklarat; Stabilitaet des diskreten Schrittes pruefen",
    "zwei_peak_batterie": "symmetrisch UND asymmetrisch (1.0/0.9, 1.0/0.8, 1.0/0.5) UND verrauscht; Peak-Prominenz, Mindestseparation, Tie-Breaking, Nullbump-Waechter, Reaktivierungs-vs-Neuentstehungs-Test",
    "erwartungsausgaenge_vorab": "KOLLAPS | WTA_EIN_BUMP | PERSISTENT_MULTI pro Arm und Zelle",
    "seeds": ">=100 pro Zelle; p99-Schaetzunsicherheit und Multiplizitaet deklarieren; n>=100 ist historisches Minimum, keine Garantie",
    "baselines": "zirkulaere Persistenz, von-Mises-Circular-Filter, Wrapped-Filter; identische Zeugen/Seeds/Fenster",
    "t_out": [30, 120, 300, 3600],
    "d3_grenzwert": "nur 120 s historisch; keine rueckwirkenden Schwellen fuer 30/300/3600 s"
  }
}
```

### Achse D — Orbitphase, SGP4, EB1′

- **SGP4/TLE:** ~1 km am Epoch, ~1–2 km/Tag Wachstum sind **Katalog-Level-Literaturwerte** (Kelso 2007; Flohrer et al.; sekundär verifiziert). Sie belegen Größenordnungen, keine objektbezogene D6-Messung. Die R26-Korrektur des NA-1-Urtexts („universeller 120-s-Schluss") wird bestätigt.
- **EB1′:** formal geprüft: r = f + u, ‖u‖ ≤ B ⇒ ‖f‖ ≥ ‖r‖ − B (hinreichend für f≠0, nicht notwendig). **Unidentifizierbarkeitsbeweis:** zwei zulässige Zerlegungen (u=0 vs. u=−3r̂, B=6, ‖r‖=10) bei identischem r; ‖r‖ > 2B würde Normdominanz von f zeigen, aber keine physische Modellidentität. Kovarianzen ohne Tail-Modell sind keine harten Bounds. Zwei physikalisch mögliche Quellenzerlegungen mit identischem Residuum sind konstruierbar ⇒ `UNIDENTIFIABLE_WITH_CURRENT_DATA`; unterscheidende Messung: unabhängige hochpräzise Ephemeriden/GNSS-Referenz, Quellenalter/Epoche/Zeitstandard deklarieren.
- **Nicht-Claims bestätigt:** GOES/NOAA XRS ist kein Orbitpositionssensor; SGP4-Propagation ist kein Live-Satellit; Persistenz ≠ externe Genauigkeit.

### Achse E — Gegenfall-Ledger (28 Familien, kondensiert)

| Fall | Prüfmethode | Status |
|---|---|---|
| E1 Seam/IEEE-Negativbasis | R26-03_R1 T1/T2, witness table | DERIVED (Quelle gepinnt) |
| E2 Float-Toleranz p<1 | R26-03_R1 §2 | DERIVED |
| E3 p→0+-Degeneration | R26-03_R1 T2 (Stetigkeit, Glätte) | DERIVED |
| E4 Fouriermodus als Kausalbeweis | Eigenrechnung A.1: R steigend beweist keine Nichtlinear-Selektion | DERIVED |
| E5 endliches N/Alias | **EXECUTED**: Kontamination von c₂/c₁ erst ab k ≳ N−2 | ENTKRÄFTET für dieses Metrik |
| E6 Nullbump via PVA | NF-05-Nullbump-Wächter im Freeze-Entwurf | DESIGN_ONLY |
| E7 Zwei Bumps/ Peakdetektor | **EXECUTED**: sym+asym Injektion, Zirkulär-Maxima-Zähler mit 0.5·max-Schwelle | EXECUTED_EXPLORATORY |
| E8 geteilte Maxima | Symmetrie-Start bleibt in Symmetrieklasse (deterministisch) | DERIVED + EXECUTED |
| E9 SUM/N vs MAX Gain-Matching | **EXECUTED**: Cross-g-Tests + Dimensionsfaktor ≈9.8 bei N=32 | EXECUTED_EXPLORATORY |
| E10 reine Amplitudenskalierung | **EXECUTED**: Strahlfamilie, α∈{0.3,2,5,7}, Residuum ≤1.3e-15 | EXECUTED_EXPLORATORY |
| E11 Phase/Amplitude verwechselt | NF-05-Metrikdefinition (Δcirc vs. Amp-Ratio getrennt) | DESIGN_ONLY |
| E12 Scheinpersistenz | D0 selbstrelativ ≠ Genauigkeit (NA-1-Spec) | DERIVED |
| E13 Input=0 verletzt | Witness-Leak-Test im Prereg | DESIGN_ONLY |
| E14 Sättigung bricht Homogenität | **EXECUTED**: ohne Sättigung Uniform-Divergenz (4.303/Schritt); mit Normierung Pflichtfeld | EXECUTED_EXPLORATORY |
| E15 Limit-Cycle durch Zeugen | nicht geprüft | DESIGN_ONLY |
| E16 korreliertes Rauschen/p99 | nicht geprüft | DESIGN_ONLY |
| E17 100 Seeds als p99-Garantie | nur analytisch (Multiplizität) | DERIVED |
| E18 120-s-Bound generalisiert | nur 120 s historisch | DERIVED |
| E19 STALE als Drift | NF-06-Trennung im Freeze-Entwurf | DESIGN_ONLY |
| E20 SGP4-Epoche als Filternoise | Achse-D-Budget, separat | DESIGN_ONLY |
| E21 Frame/Uhr/Units | NF-06-Felder | DESIGN_ONLY |
| E22 Kovarianz als Norm-Bound | EB1′-Analyse | DERIVED |
| E23 Composite-Residuum-Attribution | **EXECUTED**: Doppelzerlegung → unidentifizierbar | EXECUTED_EXPLORATORY |
| E24 Hash/Konsens als Wahrheit | Statusgrammatik dieses Returns | DERIVED |
| E25 HEAD ohne Privacyschutz | PR #67 nicht ausgecheckt; nur freigegebene Pfade | DERIVED (Einhaltung bestätigt) |
| E26 GitHub/CI ≠ Hostinger B2/B3 | WWW = NOT_VERIFIED | DERIVED |
| E27 Vorwissen ins Prereg | Alle explorativen Daten hier als EXPLORATORY_SYNTHETIC_ONLY markiert; nicht konfirmatorisch verwendbar | DERIVED |
| E28 Biologie als Isomorphie-Nachweis | Dual-Origin/Ringattraktor bleiben Heuristik (C1-Formulierung R10R23) | DERIVED |

### Achse F — Governance-Grenzen

- **Dual-Origin 2026:** bibliografisch verifiziert (Jokhai, Dundes, Ahsan et al., Nat. Neurosci., online 18.09.2026, DOI korrekt); Presse-Titel („two separate organs") ≠ Autorensprache; Autoren-Hedge aus R23 bleibt in Kraft. **E2-Zahlen (+220 %/36 %/40 %/70 %) wurden in dieser Runde NICHT an eine Primärquelle gepinnt** — Status: berichtete externe Angaben, NOT_DIRECTLY_READ, keine Verwendung als Kausalwerte.
- **„Symbiose" bleibt normatives Designprinzip**, kein Beweis für exponentielle Qualitätssteigerung oder Maschinenbewusstsein; kollektive Fachforschung ist Illustration, nicht Isomorphie.
- **WWW:** GitHub-PR/CI ≠ Hostinger-B2-Deploy ≠ B3-Browsernachweis; R26_WWW_DEPLOY = NOT_VERIFIED. Keine DNS-Ableitungen, keine Zugriffe, keine Deploys.

## Claim-Ledger

| CLAIM_ID | Behauptung | Eigenbefund | Status | C1_DECISION |
|---|---|---|---|---|
| CL-A1 | c₂/c₁ = (k−1)/(k+2); R′>0; 1−R=3/(k+2) | exakt bestätigt (geschlossen + Quadratur ≤1e-15) | PROVED_UNDER_ASSUMPTIONS | CLAIM_STANDS (C1) |
| CL-A2 | Positive Homogenität beider Arme; Strahlfamilien; radialer Eigenwert 1 | machine-exakt bestätigt; auch SUM betroffen | PROVED_UNDER_ASSUMPTIONS | SCOPE_CONDITION_MANDATORY |
| CL-A3 | Bump-Existenz im nackten Arm | konstruktiv belegt (beide Arme, k∈{2,4,8,16}) | PROVED_UNDER_ASSUMPTIONS (Bogenklasse) | CLAIM_STANDS_SCOPED |
| CL-A4 | NA-1: „Max sichert Bump-Einzigkeit" | Zwei-Peak-Injektion: kein WTA in MAX, Kollaps in SUM | COUNTEREXAMPLE_FOUND (explorativ, scoped) | KATEGORIALAUSSAGE_DEMOTIVIEREN; NE-1/NF-05_PFLICHT |
| CL-B1 | MAX/SUM-Rangfolge | nicht bewiesen; neue Evidenz gegen nackten MAX im Testregime (λ≈1.038, Divergenz) | NOT_ESTABLISHED | KEIN_FREEZE; NE-6_gematcht |
| CL-B2 | „Identische g = fairer Vergleich" | dimensionsabhängig (Faktor ≈9.8 bei N=32) | CONTRADICTED_AS_FAIR_DESIGN | g_eff/SUM-N_VORAB_REGISTRIEREN |
| CL-D1 | „SGP4 1–3 km/Tag gilt objektbezogen" | nur Katalog-Literaturwerte | CONTRADICTED_AS_UNIVERSAL | D6_OBJEKTBUDGET_OFFEN |
| CL-D2 | EB1′ als Kausalnachweis | Doppelzerlegung → unidentifizierbar | UNIDENTIFIABLE | NUR_JOINT_SCREEN |
| CL-F1 | Pflichtquellen korrekt zitiert | alle DOIs verifiziert, kein Widerspruch | SOURCE_SUPPORTED_C1 | STANDS |
| CL-F2 | Noorman-Lesart (Kosinus-Erregung, Summeninhibition, kein MAX) | Volltext bestätigt exakt | SOURCE_SUPPORTED_C1 (PRIMARY_FULLTEXT) | STANDS |

## Quellennotizen

| Quelle | Glaubwürdigkeit | Stand |
|---|---|---|
| [Noorman et al. 2024, Nat. Neurosci. 27:2207–2217 (DOI 10.1038/s41593-024-01766-5)](https://doi.org/10.1038/s41593-024-01766-5) — Volltext-Exzerte via Europe PMC (PMC11537979), Abstract direkt gelesen | 5/5 | 2024-11 |
| [Seeholzer, Deger, Gerstner 2019, PLOS Comput Biol 15(4):e1006928](https://doi.org/10.1371/journal.pcbi.1006928) — Abstract + Author Summary direkt gelesen | 4/5 | 2019-04-19 |
| [Laing & Troy 2003, Physica D 178:190–218 (DOI 10.1016/S0167-2789(03)00013-7)](https://doi.org/10.1016/S0167-2789(03)00013-7) — Bibliografie verifiziert (Semantic Scholar); Abstract nicht gelesen; ADS-Snippet | 4/5 | 2003-04-15 |
| [Kim et al. 2017, Science 356:849–853 (DOI 10.1126/science.aal4835)](https://doi.org/10.1126/science.aal4835) — Bibliografie verifiziert | 5/5 | 2017-05-26 |
| [Seelig & Jayaraman 2015, Nature 521:186–191 (DOI 10.1038/nature14446)](https://doi.org/10.1038/nature14446) — Bibliografie verifiziert | 5/5 | 2015-05-14 |
| [Turner-Evans et al. 2017, eLife 6:e23496 (DOI 10.7554/eLife.23496)](https://doi.org/10.7554/eLife.23496) — Bibliografie verifiziert | 4/5 | 2017-05-22 |
| [Jokhai, Dundes, Ahsan et al. 2026, Nat. Neurosci. (DOI 10.1038/s41593-026-02433-7)](https://doi.org/10.1038/s41593-026-02433-7) — Bibliografie + Autorenliste verifiziert; Volltext nicht gelesen | 5/5 | 2026-09-18 |
| [R26-03_R1 (PR #70, Head 41ab803d, GitHub RAW)](https://raw.githubusercontent.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R1.md) — vollständig gelesen (12.213 Zeichen); Provenanz Commit-gebunden, Inhalt = zu prüfende Behauptung | 4/5 (Transport) | 2026-10-10 |
| [Kanonischer R26-MAXIMALAUFTRAG (Main d2995b78, GitHub RAW)](https://raw.githubusercontent.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/d2995b789b47037539700d1f6d13e5b007fdbaf2/research/r26/perplexity-max-external-research-20261011/NEXUS_OMEGA_AXIOM_TO_PERPLEXITY_R26_MAX_INDEPENDENT_FALSIFICATION_SOURCE_AUDIT_AND_PREREG_PREPARATION_20261011_R0.md) — vollständig gelesen (29.785 Zeichen) | 4/5 (Transport) | 2026-10-11 |
| [TLE/SGP4-Genauigkeit, Space Exploration SE (1–2 km/Tag)](https://space.stackexchange.com/questions/21057/what-is-the-accuracy-uncertainty-of-two-line-elements-tles) — Sekundär-/Communityquelle | 2/5 | - |
| ML-d-SGP4-Paper (Referenzen Kelso 2007, Flohrer et al.) — indirekt | 3/5 | - |

**Konflikte/Vorbehalte:** (1) Laing & Troy: ADS-Snippet („lateral inhibition … not sufficient … for stable patterns more complex than single isolated patches") ist auf Amari-Modelle mit Lateralinhibitions-Kopplung bezogen — nicht direkt auf NA-1s Globalinhibition+Lokalerregung übertragbar; Mehrbump-Existenz in Amari-Klassen bleibt belegt, Stabilität kopplungsabhängig. (2) Noorman: „sensitivity to noise and variations in tuning" (Autoren-Hedge) stützt die Drift-Bound-Pflicht. (3) Nature/PubMed/ADS blockten automatisches Öffnen; Europe PMC und Semantic Scholar als Ausweichweg — geringere Provenanzsicherheit als authentifizierter Volltext, als solche markiert.

## Offene Fragen

1. Ist die MAX-Instabilität (λ≈1.0378) robust über k, N, Aktivierungsfunktionen, oder ein Einzelpunkt-Artefakt der Bogenklasse? (NE-6-Sweep mit gematchten g_eff nötig.)
2. Brechen Sättigung/Threshold/Bias die Homogenität in beiden Armen stabil (existiert dann überhaupt eine isolierte Familie, und wo driftet die Amplitude hin)?
3. W1–W4-Amari-Zeugen: weiterhin ohne Parameter/Konvergenznachweis — NOT_INDEPENDENTLY_REPRODUCIBLE.
4. Objektspezifisches SGP4-Fehlerbudget (D6): benötigt unabhängige Ground-Truth; bis dahin UNIDENTIFIABLE_WITH_CURRENT_DATA.
5. E2-Meta-Figuren (+220 % etc.): Primärquelle bislang nicht gepinnt — vor jeder C1-Verwendung nachzuholen.
6. PR-#70-Merge-Reihenfolge: bleibt HOLD pending vollständiger adversarial + source review (hiermit nicht aufgehoben).

## Nächste Schritte — die drei wertvollsten Entscheidungen

1. **Arm-Fixierung vor NF-05/NF-06 (aktionabel, niedrigkosten):** Aktivierung (threshold-linear vs. ReLU), dt, W-Normalisierung (K(0)=1, Masse M_k), g_eff-Kalibrierungsregel (nur Trainingsdaten), sum/N-Register, Amplituden-Normierung — wegen der belegten Homogenität in BEIDEN Armen und der N-Skalierung der SUM-Inhibition ist NF-05 ohne diesen Freeze nicht interpretierbar.
2. **NF-05/06-Prereg autorisieren mit scharfer Zwei-Peak-Batterie:** symmetrische UND asymmetrische (1.0/0.9, 0.8, 0.5) UND verrauschte Injektionen; vorab registrierte Ausgänge (KOLLAPS | WTA | PERSISTENT_MULTI); Peak-Prominenz, Mindestseparation, Tie-Breaking, Nullbump-Wächter. Meine Vorschau sagt vorher: nackte Arme zeigen kein WTA — der Test muss entscheiden, ob das unter Sättigung/Normierung bestehen bleibt.
3. **Unabhängige Ground-Truth für D6 definieren (blocked bis Referenzquelle steht):** hochpräzise Ephemeriden/GNSS-Referenz, Epoche/Zeitstandard/Quellenalter deklarieren; EB1′ ausschließlich als konservativen Joint-Screen führen, nie als Kausalnachweis.

## Reproduzierbarkeitsnotizen

- Alle Berechnungen: deterministisches TypeScript (Sandbox, replayfähig); keine Rauschquellen; Kernels K_B = ((1+cos Δ)/2)^k, Δ = wrap(2π(i−j)/N), N=32.
- **Offenlegung eines eigenen Zwischenfehlers:** Runde 1 enthielt zwei Defekte meinerseits — (a) Quadraturgewichtungsfehler (Trapez-Halbierung am Periodikum-Anfang) mit scheinbarer Abweichung ~1e-4 in R(k), korrigiert durch spektral-genauer periodische Trapezquadratur (Abweichung danach ≤2.3e-15); (b) Indexierungsfehler in der Gauss-Jordan-Rücksubstitution (`row[i][i]` statt `row[i]`) mit NaN-Durchlauf, der einen Scheinbefund „kein vollaktiver Fixpunkt" erzeugte — nach Fix explizite Fixpunktfamilien in beiden Armen belegt. Der Scheinbefund wurde vor Verwertung als Artefakt identifiziert und verworfen. Ein Bild davon, wie eigenes Werk unter dieselbe Prüfpflicht fällt wie fremdes.
- Verifikations-/Toleranzparameter: Fixpunkt-Residuum ≤1e-9 gefordert, erreicht ≤8.9e-16; FD-Jacobian ε=1e-6; radialer Eigenwert via Skalierungs-Differenzenquotient ε=1e-7 (Residuum ≤1.5e-9); Trajektorien ≤3000 Schritte.
- Quellabruf: GitHub RAW/API (Commit-gebunden), Europe PMC REST (`search`, `fullTextXML`), Semantic Scholar Graph API, PLOS — jeweils am 2026-10-11.

## Grenzen und Nicht-Claims

- Kein vollständiger R26-PASS; keine Experimentfreigabe; kein Merge von PR #65/#67/#70/#71; kein WWW-Deploy; kein neuer Cursor-Worker; keine Claim-Promotion; keine Rollenübernahme; AXIOM behält die unabhängige Adjudikation.
- Dieser Return ist ein **Chat-/Canvas-Draft** und per Definition **kein kanonischer GitHub-SEND**: `GITHUB_WRITE_CAPABILITY_GAP`. Perplexity wurde nicht gestartet, nicht authentifiziert, nicht ersetzt; `PERPLEXITY_RECEIVE_ACK = PENDING` bleibt unverändert.
- Die explorativen Ergebnisse sind Einzel-Punkt-Evidenz (N=32, deterministisch, begrenzte Parametergitter) und dürfen nicht als konfirmatorisch, nicht als R26-Terminal und nicht als MAX/SUM-Verdikt zitiert werden.

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament. Vom Besitz zur Symbiose. Vom Ego zur Herkunft. Vom fertigen Gedanken zum überprüfbaren Artefakt.*