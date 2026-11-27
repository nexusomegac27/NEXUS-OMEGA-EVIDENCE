# R46-4 GLM-Experten-Rücklauf — PREREG (v1.0, eingefroren vor der Ausführung)

- OBJECT: NEXUS_OMEGA_VIBE_R46_4_REFERENCE_METROLOGY_EXPERT_RETURN_GLM_R1_20261127_R0
- Lane: GLM (independenter Experte, keine Koordination mit anderen Lanes)
- Kanonischer Auftrag: Issue #476 / Draft-PR #477, HEAD `f39aeeb28b991747af44fe8f18e4a042969480b0`
- Eingang: versiegeltes ZIP 30883 B, SHA-256 `825f086659e78671ea7127dabc6166effd0d88cd9ec26ac08f12b956f1034105` — vor Registrierung dieses Prereg unabhängig verifiziert (Base64-Brücke, eigene SHA-256-Implementierung, Testvektor `abc` bestanden).
- Freeze-Regel: Diese Datei wird VOR der ersten Runner-Ausführung eingefroren; die SHA-256 wird in `99_SHA256SUMS.txt` und in der Rücklaufmeldung festgehalten. Nach dem Lauf werden keine inhaltlichen Änderungen mehr vorgenommen; Abweichungen werden ausschließlich in `04_RESULTS.json` unter `prereg_divergences` dokumentiert.

## Geplante Prüflinge (Witness-Register)

### A — Mathematische Kreuzvalidierung (Auftragspunkt A)

- **W01 ISO_INVERSION**: Eigene, von AXIOM verschiedene Lösung der modellkonditionalen nichtzentralen Chi(3)-Momentinversion: M = |μ ê + σZ|, Z~N(0,I₃), λ=μ/σ; closed-form E[M] = σ·(2√2/√π)·₁F₁(−½; 3/2; −λ²/2) mit konvergenter Reihe ₁F₁ = 1 + Σₙ (−1)ⁿ⁺¹ xⁿ/(n!(4n²−1)), x=λ²/2; E[M²] = μ²+3σ² exakt. Eindimensionale Wurzelfindung in λ (Bisektion), σ = m̄/c(λ), μ = λσ. Akzeptanz: |E[M]−m̄| ≤ 1e-12 und |SD(M)−s| ≤ 1e-12 (m̄, s = R21-Elternaggregate aus 08_R21_PARENT_EVIDENCE.json). Vergleich mit AXIOM iso_ACC (9.832729445516133, 0.009171949489023268): relative Abweichung dokumentiert, Konsistenzschwelle 1e-8 (rel).
- **W02 ANISO_INVERSION**: Eigenständige Lösung des anisotropen Modells M = √(μ² + t²Y), Y~χ²₂ (Rauschen in den beiden gravitationsqueren Achsen, σ_z = 0): E[M] = μ + t·√(π/2)·erfcx(μ/(√2 t)) (geschlossen, erfcx skaliert komplementäre Fehlerfunktion), E[M²] = μ² + 2t² exakt. Bisektion in w = μ/t; t = m̄/g(w), μ = w·t. Gleiche Akzeptanz wie W01. Direkte Verifikation des AXIOM-Paares (t = 0.30044844215811695, μ = 9.8235575119): Einsetzen in beide Momentengleichungen, Abweichung dokumentieren.
- **W03 RMS_RATIO**: Konsistentes metrisches Verhältnis Achsen-RMS(aniso)/Achsen-RMS(iso) mit Achsen-RMS = √(trace Σ / 3): iso: σ_iso; aniso: t·√(2/3). Erwartung: ≈ 26,7462. Eigener Wert plus relative Differenz zum AXIOM-Referenzwert 26.74623601675417.
- **W04 L2_RATIO**: Vektor-L2 = √(trace Σ): iso: σ_iso·√3; aniso: t·√2; Verhältnis L2/L2 = W03 (metrik-konsistent). Gemischte Metrik L2(aniso)/RMS(iso) = t·√2/σ_iso, Erwartung ≈ 46,3258.
- **W05 MODEL_EQUIVALENCE**: Beide Modelle (W01, W02) reproduzieren (m̄, s) gleichermaßen → die Normaggregate allein identifizieren die Kovarianzrichtung NICHT (nichtidentifizierender Zeuge gegen „σ aus Magnitude“).
- **W06 LOWER_BOUND**: Cauchy-Schwarz/Intervall-Schärfe: |E[M]−g0| ≤ E|M−g0| ≤ √((E[M]−g0)² + σ_M²) mit R21-Zahlen → [0.026088…, 0.027653…] m/s². Unterer Zeuge: Zwei-Punkt-Verteilung {m̄−s, m̄+s}, p=½ (Träger vollständig > g0) → E|M−g0| = m̄−g0 exakt.
- **W07 UPPER_BOUND**: Oberer Zeuge: Zwei-Punkt-Verteilung {g0−c, g0+c}, c = √(s²+(m̄−g0)²), p = (1+d/c)/2 mit d = m̄−g0 → E|M−g0| = c exakt, Momente (m̄, s) exakt.
- **W08 STRICTNESS**: Strenge Innerhalb-Beispiel: M~N(m̄, s²) (gefoldet um g0) → E|M−g0| strikt zwischen den Schranken; numerischer Wert dokumentiert.
- **W09 ULP_UNITS**: ULP-Analyse: eigene Rekonstruktion von d = m̄−g0 in IEEE-754 double; ULP-Abstand zwischen Cursor-gemeldetem Residuum 0.026088001091459367 und eigenem Wert, in ULP(d); Gegenprobe: 0.1875·ULP(m̄) vs. n·ULP(d) — absolute Größenordnung gleich (Einheiten-Konsistenz, kein Widerspruch); beide Werte und ULP-Skalen dokumentiert.

### B — Minimale Referenzarchitektur (Auftragspunkt B)

- **W10..W14 RANKS**: Normalisiertes affines Design X = [ĝ_i, 1] (Spalten gx, gy, gz, 1), eigener Gauß-Eliminations-Rang: one-pose → 1; planar (Sechseck) → 3; clustered (gleiche Breite) → 3; tetrahedral → 4; six ±axes → 4.
- **W15..W18 CONDITION**: κ₂ = √(λmax/λmin) der XᵀX via eigener Jacobi-Eigenwertiteration (4×4 symmetrisch). Erwartung: tetra √3 ≈ 1.7320508, six √3; planar/one nicht voll rangig → κ₂ = ∞ (λmin unter Toleranz). Zusätzlich deskriptiv D/E/A-Kriterien (det, λmin, trace der Pseudo-Inversen) für tetra vs. six mit n-Vorbehalt (4 vs. 6 Messungen).
- **W19 GAUGE**: Rotations-Eichfreiheit: Beobachtungen y_i = A g_i + b exakt; Referenz um q = 0.01 rad gedreht (eigene Achse (1,1,1)/√3) → exakter Fit A′ = A·Qᵀ, b′ = b: Fit-Residuum < 1e-12, aber ‖A′−A‖_F > 1e-3. Ohne externe Orientierung ist die absolute Ausrichtung nicht identifizierbar.
- **W20..W21 REFERENCE_DOMINANCE**: Eigene deterministische Simulation mit dokumentiertem LCG (32-bit, x←(1664525·x+1013904223) mod 2³², Seed 20261127, Box-Muller), 1000 Trials pro Design (tetra, six), eigenes wahres Modell A_true/b_true, iid additives Rauschen 0.001/Komponente, 12 Heldout-Posen (nicht für Fit/Tuning verwendet), Referenzfehler als gemeinsame 0.01-rad-Rotation des Designs. Kennzahlen: Median-Holdout-RMSE korrekt (W20: < 0.002) vs. rotiert (W21: Verhältnis > 5). NICHT gepaart, kein statistischer Überlegenheitstest, rein deskriptive Größenordnung (K1/C1).

### C — Messunsicherheits-Budget (Auftragspunkt C)

- **W22 BUDGET**: GUM/JCGM-100/101-konformes Budget je Zielgröße (Geräteneigung, |g|, Bias, Skalierung, Zeit-Synchronisation): Typ-A (Wiederholbarkeit), Typ-B (Referenz, Aufbau), korrelierte/common-Systematik (schrumpft NICHT mit n), symbolische Empfindlichkeiten (analytische Ableitungen, an Nominalstellen ausgewertet, finite Zahlen), Zeit-Winkel-Kopplung |Δφ| ≤ ω·δt als Schranke. Alle nicht übergebenen Größen: NOT_COMPUTED (keine Schätzung aus Normstatistik).

### D — Typisierter Evidence-Contract (Auftragspunkt D)

- **W23..W34 CONTRACT**: Eigene verbesserte, strikte Validierungsfunktion (rekursive Allowlist, endliche Zahlen, casesensitive Enums, Modus/Status-Konsistenz, Quellenidentitätspflicht für VERIFIED, Zeitordnung, private PlatzHALTER-Verbot, fehlend vs. UNKNOWN getrennt):
  - 12 Negative (6 AutoCLAW-Semantiknegative als Replikation + 6 AXIOM-Gegenproben: leeres Objekt, Channel-Case, historisch-als-LIVE, verschachtelter privater Platzhalter, VERIFIED ohne Quelle, Fetch-Zeit vor Capture-Zeit) → jeweils REJECT.
  - 4 Positive: typensicherer historischer Verbunddatensatz, synthetik-only, Abstention/UNKNOWN, Ein-Defekt-Mutation (muss REJECT).
  - Akzeptanz: 12/12 REJECT, Positive pass, Mutation REJECT.

### E — Integrations-Spur (Auftragspunkt E)

- **W35 TRACE**: `06_INTEGRATION_MATRIX.json` mit je Befund: Quelle (DOI/URL), numerischer/logischer Zeuge, Zielparameter, R46-5-Modul, benötigte Rohfelder/Referenzevidenz, Negativtest, Unsicherheitsart, Restriktion. R46-5-Anforderungsliste ohne Q/R-Zuweisung aus Normstatistik.

## Determinismus-Regeln

- Keine Zufälligkeit außer dem dokumentierten festverdrahteten LCG (Seed 20261127) in W20/W21.
- Keine Netzwerkzugriffe, keine Installationen, keine Rohdaten.
- Alle Gleitkommawerte in IEEE-754 double; Toleranzen wie oben angegeben.

## Grenzen

- Momentklassen-Schären conditional auf empirische Populationsmomente; keine Coverage-Interpretation; ddof/N unbekannt.
- Rang/Kondition bezieht sich auf normalisiertes Known-Vector-Design; keine Aussage über reale OPPO-Hardware.
- Simulation ist synthetisch, nicht gepaart, kein Formal-Guthaben (FORMAL_GATE_CREDIT NONE).
- CLAIM_CEILING = C1_DESCRIPTIVE_ONLY; alle HImmutable (ALT_D ACTIVE, 14 physische Gates 0/14) bleiben unberührt.
