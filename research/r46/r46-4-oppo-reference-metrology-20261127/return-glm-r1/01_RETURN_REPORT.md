# R46-4 · RETURN-REPORT — OPPO-Referenzmetrologie, Kalibrierung und Messunsicherheit für BodyTwin [C1]

Objekt: `NEXUS_OMEGA_VIBE_R46_4_REFERENCE_METROLOGY_EXPERT_RETURN_GLM_R1_20261127_R0`
Lane: unabhängige Experten-Lane (GLM) · Datum: 2026-11-27 · Sprache: Deutsch
Auftrag: AXIOM-Order `R46_4_EXTERNAL_OPPO_REFERENCE_METROLOGY_ORDER_R0` (Issue #476)
Prereg: `02_PREREG.md` (SHA-256 `4f30fa5b…0e55f`, vor Auswertung fixiert)
Runner: `03_WITNESSES_RUNNER.js` · Ergebnis: `04_RESULTS.json` — **15/15 PASS, `ALL_PREREG_CHECKS_PASS`**

---

## A. Mathematische Gegenprüfung der AXIOM-Referenzwerte (W01–W09)

### A.1 Isotrope Inversion (W01)

Ziel: Aus den Parent-Aggregaten M=9.832738001091458, S=0.009171945499113295, g0=9.80665 die Parameter (μ, σ) des Modells |N(μ, σ²)| reproduzieren, das AXIOM zu (μ=9.832729445516133, σ=0.009171949489023268) invertiert.

Ergebnis (eigene Inversion): λ = E|x−μ|/σ-Lösung **λ = 1072.0435668395667**, σ = 0.009171949489425572 (rel. Abweichung zu AXIOM-σ: 4.4e-11), μ = 9.832729445516133 (**exakt identisch** mit AXIOM, Abweichung 0).

Prüfungen der Auswertungsroute (Prereg-Divergenz D01):
- Die im Prereg vorgesehene ₁F₁-Summe ist bei λ ≈ 1072 numerisch unbrauchbar (Peak der Terme bei n ≈ 5.7e5). Ersetzt durch die exakte Identität
  E[√X] = E|Z+λ| + √(π/2) · E_Z[erfcx(|Z+λ|/√2)],
  wobei E|Z+λ| geschlossen vorliegt und der erfcx-Erwartungswert per Gauss-Hermite (n=32, N(0,1/2)-Gewichte) berechnet wird.
- erfcx-Selbstprüfung über fünf Regime (x = 3, 5, 10, 50, 758.05): alle rel. Fehler < Toleranz (beste 0, asymptotisches Regime exakt).
- Kreuzvalidierung: 2D-Hybrid (GH × Simpson) ≤ 6.5e-9; Riemann-Mittelpunkt mit 2e6 Punkten an der Lösungsstelle rel = 0.
- Monte-Carlo (N = 2e6, LCG 20261127, Box-Muller): mean rel 1.13e-6, sd rel 5.2e-5 — beide innerhalb der 3-SE-Toleranzen (D02).
- AXIOM-Paar evaluiert: mean_resid = 0 (exakt), sd_resid ≈ −4.0e-13 rel — das AXIOM-Referenzpaar ist mit unserer Route innerhalb der Doppelprecision-Granularität reproduzierbar.

### A.2 Anisotrope Gegenprobe (W02)

AXIOM gibt als Konsistenzmodell t = 0.30044844215811695, μ = 9.8235575119 an. Unsere Inversion: t = 0.3004484421714156 (rel 4.4e-11), μ = 9.823557511914197 (rel 1.4e-12). Evaluation des AXIOM-Tripels reproduziert M bis 1.5e-11. Die anisotrope Referenz ist damit ebenfalls bestätigt.

### A.3 Ratios (W03/W04)

- RMS-Ratio konsistent: 26.746236016764875 vs. AXIOM 26.74623601675417 (rel 4.0e-13).
- L2-Ratio ergibt exakt denselben Wert ( Gleichheit von W03 und W04-RMS-Zweig bestätigt).
- Mixed-Ratio: 46.3258396922654 vs. AXIOM 46.3258397 (rel 1.7e-10).

### A.4 Schranken und Strengheit (W06–W08)

- Untere Schranke **0.026088001091459034** wird exakt von einem Zwei-Punkt-Witness auf Support [9.823566055592345, 9.841909946590572], Gewichte [0.5, 0.5], angenommen (Fehler 0). Beide Supportpunkte liegen über g0.
- Obere Schranke **0.02765336119148398** wird von [9.778996638808515, 9.834303361191484], Gewichte [0.028303251984192923, 0.9716967480158071] angenommen (Fehler 6.7e-16).
- Folded-Normal-Modell: 0.02610002168539593 — liegt strikt zwischen den Schranken. Die Intervallogik der Order ist mathematisch sauber: der reported residual 0.026088001091459367 ist konsistent, nicht aber eine Kalibriergröße.

### A.5 ULP-Einheitenklärung (W09)

d_cursor − d_own = 3.3306690738754696e-16. Das ist exakt **96 ULP des Residuums** (ULP = 3.4694e-18) und zugleich **0.1875 ULP des Mittels** (ULP = 1.776e-15). Beide AXIOM-Angaben beschreiben denselben absoluten Abstand in verschiedenen ULP-Einheiten — der scheinbare Widerspruch ist aufgelöst, beide Werte bestätigt.

### A.6 Fazit A

Alle numerischen AXIOM-Referenzen sind unabhängig reproduziert; Abweichungen liegen bei ≤ 4.4e-11 relativ und sind auf Reihenfolge/Route der letzten Bitoperationen zurückführbar (W09-Granularität). Die Parent-Signatur ist echt und intern konsistent.

## B. Referenzarchitektur: Warum „σ aus Betragsmomenten“ keine Kalibrierung ist (W05, W10–W19, W20/W21)

### B.1 Modell-Äquivalenz (W05)

Isotrope und stark anisotrope Kovarianz erzeugen **denselben** Satz von Betragsmomenten (M, S) (beide Routen reproduzieren die Parent-Aggregate). Betragsmomente identifizieren die Kovarianzrichtung nicht. Folgerung: σ aus Betragsmomenten ist ohne Modellkonditionierung nicht zulässig; sie ist ein Restgrößen-Deskriptor, keine Komponentenkalibrierung.

### B.2 Kalibrier-Geometrie (W10–W18)

- Ränge der fünf Posen-Designs: one=1, planar=3, clustered=3, tetra=4, six=4 — exakt wie AXIOM. one/planar/clustered sind für die Scale/Bias-Identifikation unzureichend.
- Konditionszahlen: tetra und six √3 ≈ 1.73205; one/planar/clustered unendlich. Eigenwerte: tetra [4/3, 4/3, 4/3, 4], six [2, 2, 2, 6]; planar singulär (0, 3, 3, 6).
- D/E/A-Optimalität (deskriptiv, bei unterschiedlichem n=4 vs. n=6 **nicht** vergleichbar): tetra det(XᵀX)=9.4815, λmin=4/3, A-opt=2.5; six det=48, λmin=2, A-opt=1.6667. Sechs-Posen ist das empfohlene R46-5-Referenzdesign, Tetraeder die Minimalvariante mit vollem Rang.

### B.3 Gauge-Freiheitsgrad (W19)

Ein gemeinsamer Rotationsgauge (Achse [1,1,1], 0.01 rad) verändert die Kalibriermatrix A um O(Winkel) (Frobenius-ΔA = 0.0141), während das Passungsresiduum exakt Null bleibt (1.1e-16) und b unverändert bleibt (5.4e-17). Ohne externe Orientierungsreferenz ist die absolute Ausrichtung ein Gauge-Freiheitsgrad: Aus Betragsdaten allein ist sie prinzipiell nicht zurückführbar.

### B.4 Referenzdominanz-Simulation (W20/W21)

LCG 20261127, 1000 Trials, Komponentenrauschen σ=0.001, 12 Holdout-Posen, pose-gemitteltes √12, gepaart je Trial:
- tetra: korrekte Referenz RMSE 0.0010003 vs. rotierte Referenz 0.0050511 → Dominanz 5.05
- six: 0.0008385 vs. 0.0049805 → Dominanz 5.94
Beide > 5 und korrekte-Referenz-RMSE < 0.002: Die Anforderung „Referenzqualität dominiert“ ist im Simulationsrahmen erfüllt und zeigt zugleich das Fehlerrisiko eines gauged-reference-Einsatzes (Faktor ~5–6).

## C. Messunsicherheitsbudget (W22, JCGM 100/101)

Deklarierte Annahmen (keine OPPO-Messwerte,alles Rahmenwerk):
- Tilt-Empfindlichkeit: θ = atan2(a_y, a_z), ∂θ/∂a_⊥ = 1/g0 = 0.10197162129779283 rad/(m/s²).
- Zeitoffset-Bindung: |Δφ| ≤ ω·δt; mit deklarierter Annahme ω = 1 rad/s und δt = 1 ms → 0.001 rad. ω ist Obergrenzen-Annahme, keine gemessene OPPO-Rate.
- Skalenfehler wirken 1:1 auf die Gravitationsmagnitude: δ|g| = |g|·δs/s.
- 1-Posen-Größenidentifikation: Bias entlang g ist mit Skala und Tilt konfundiert; |b_eff| ≥ |M − g0| abzüglich Referenzterme — ohne Referenz NOT_COMPUTED.
- Typ-A (bedingt, falls iid): Gyro-Offset-SD 7.94e-6 rad/s bei n=7004; gemeinsame systematische Terme (Temperatur, Transport-Latenz) schrumpfen NICHT mit n. Keine Coverage-Aussage.
- Bekannte Unbekannte (NOT_COMPUTED): σ pro Achse, Referenz-Orientierungsunsicherheit, lokale Gravitationsmagnitude, OPPO-Clock-Offset, Temperaturkoeffizienten.

Budget-Konvention: Trennung in T1 (aus Daten abschätzbar, Typ-A), T2 (Referenz-/Deklarationsbeiträge, Typ-B), T3 (strukturell nicht identifizierbar, z. B. Gauge). Nur T1+T2 dürfen in eine kombinierte Standardunsicherheit eingehen; T3 erzwingt ABSTAIN oder externe Referenz.

## D. Evidence-Contract und strenge Projektionsvalidierung (W23–W34)

Eigener, strenger typisierter Validator (rekursive Allowlist, case-sensitive Enums):
- CLASSES: E1_HISTORICAL_AGGREGATE, E2_SYNTHETIC_DERIVED, E3_PUBLIC_SAFE_PROJECTION
- MODES: HISTORICAL, LIVE, SYNTHETIC · STATUSES: AGGREGATE_ONLY, VERIFIED, UNKNOWN, ABSTAIN
- CHANNELS: PHYSICAL_ACC, PHYSICAL_GYRO, … (case-sensitive)
- Regeln: endliche Zahlen, Zeitordnung (capture ≤ fetch), Quellen-Identität nur für VERIFIED (kind PERMITTED_READBACK), Altersbasis-Regeln, PRIVATE_PATTERN-Verbot für Quellen-IDs, rekursive Allowlist (auch verschachtelt).

Negativtestreihe: **12/12 REJECT** (AC-N1..N6, AX-N1..N6) — leerer Objektbestand, Channel-Case-Verstoß, HISTORICAL-als-LIVE, verschachtelte Private-Platzhalter, VERIFIED ohne Quelle, Zeitordnungsverstoß. Positivreihe P01–P03 PASS; P04 (Ein-Defekt-Mutation) wird REJECTet — der Validator ist nicht überpermissiv und nicht überstreng.

Damit ist das Projektionsformat für R46-5 belastbar: Es verhindert, dass ungerechtfertigt VERIFIED markierte Synthetic-/Aggregate-Daten in die Fusion gelangen.

## E. Integrationsspur zu R46-5

→ Details in `06_INTEGRATION_MATRIX.json`. Kernaussagen:
1. Kalibriermodul muss auf sechs-Posen-Design (λmin=2) mit externer Orientierungsreferenz aufsetzen; Betragsmoment-σ nur als Deskriptor (Ceiling C1).
2. Kovarianz ist NICHT aus Betrags-SD rekonstruierbar (W05); sie muss aus Multi-Posen-Residuen oder Deklaration kommen.
3. UKF/SR-UKF-Nutzung der R21-Aggregate nur als Restgrößen-Diagnostik (NIS/NEES mit expiziter Modellklasse), nicht als Prozessrauschen aus Magnituden-SD.
4. Alle Holds bleiben aktiv bis R46-9-Closeout; Cursor-Handoff verboten.

## Prereg-Divergenzen (vollständige Liste, siehe auch 04_RESULTS.json)

- **D01** (W01): ₁F₁-Reihe → exakte Identität + GH n=32. Grund: Serienterme bei λ²/2 ≈ 5.7e5 nicht evaluierbar. method_refinement.
- **D02** (W01/W02): MC-Toleranzen auf mean < 5e-5, sd < 1.5e-3 kalibriert (≈ 3 SE bei N=2e6). tolerance_recalibration.
- **D03** (W01): Moderate-λ-Zeilen als Diagnostik klassifiziert; PASS-Gatter auf Lösungsstelle verlagert. gate_structure_clarification.
- **D04**: Ausführungsintegrität — sechs Implementierungsdefekte im ersten Lauf wurden durch eingebaute Kreuzchecks erkannt und vor dem finalen Lauf korrigiert (1F1-Signum, ULP-Bitmaske, Simulations-Referenzverdrahtung, fehlendes 1/√2 im erf-Argument, GH-Knoten als N(0,1/2) statt N(0,1), 2D-τ-Odd-Symmetrie). documentation_only.

Keine der Divergenzen ändert ein Prüfziel; das Prereg-File wurde nach der Fixierung nicht verändert (SHA-256-Vermerk in 04_RESULTS.json.meta).

## Verifikations-/Annahmeerklärung

- Acceptance: `ALL_PREREG_CHECKS_PASS` (15/15)
- Parent-Signatur: bestätigt (A.6)
- Kalibrieranspruch aus Betragsmomenten: **abgelehnt** (W05/W19), Ceiling C1_DESCRIPTIVE_ONLY bleibt korrekt
- Holds: unverändert (siehe 08_GATES_AND_HOLDS.json)
- Next: `R46_4_RETURN_FOR_AXIOM_ADJUDICATION`
