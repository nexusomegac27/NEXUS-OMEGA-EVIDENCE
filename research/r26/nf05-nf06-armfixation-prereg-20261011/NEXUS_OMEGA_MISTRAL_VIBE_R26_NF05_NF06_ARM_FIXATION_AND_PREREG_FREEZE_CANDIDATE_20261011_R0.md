# NEXUS OMEGA · R26 — NF-05/NF-06 Arm-Fixierungs- und Prereg-Freeze-Kandidat R0

**Ausführungslane:** MISTRAL/VIBE (Ausführungsstrang, Entwurf; Transport operator-vermittelt) · **Datum:** 2026-10-11 · **Claim-Deckel:** C1_DESCRIPTIVE_ONLY

```text
OBJECT = NEXUS_OMEGA_MISTRAL_VIBE_R26_NF05_NF06_ARM_FIXATION_AND_PREREG_FREEZE_CANDIDATE_20261011_R0
PARENT_OBJECT = NEXUS_OMEGA_AXIOM_R26_PERPLEXITY_PR77_ADJUDICATION_20261011_R0 (Main 8c37445c709986a39191fd46af8efe70d1150b9c)
ORDER_SOURCE = AXIOM_PR77_ADJUDICATION_NEXT_SCIENCE_CONNECT (MAX/SUM-Fixierung + NF-05/06-Felder vor konfirmatorischem Vergleich)
SIBLING_OBJECT = NEXUS_OMEGA_MISTRAL_VIBE_R26_TWO_PEAK_REPLAY_RETURN_20261011_R0 (separater Transport)
CLASSIFICATION = NEW_PROPOSAL_DESIGN_ONLY
EXECUTION_AUTHORIZED = FALSE
EXPERIMENTS = EXPLORATORY_SYNTHETIC_ONLY (deterministische Zeugen; keine präregistrierten Trials)
REPO_FETCH_MODE = CONNECTOR_API_READ (AGENTS.md, Firewall V1, Slot-Registry auf main 88e8e798 gelesen)
GITHUB_TRANSPORT = OPERATOR_TO_AXIOM_TRANSFER_NOT_AGENT_GITHUB_SEND (R27-E-Firewall §2-Label)
MERGE_BY_PRODUCER = NO
D1_KERNEL_FREEZE = NO (unverändert; K_B bleibt Forschungskandidat)
D2_ARM_FREEZE = PROPOSED_FIELDS_ONLY (dieser Entwurf; Entscheidung bei AXIOM)
NF05_NF06 = DESIGN_ONLY_NOT_EXECUTED
MODEL_MAX_VS_SUM_WINNER = NOT_ESTABLISHED (unverändert)
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Frage (Auftragsinterpretation)

Die AXIOM-Adjudikation von PR #77 ordnet als verbindlichen nächsten Forschungsanschluss: (a) NF-05/NF-06 um Eigenmoden- und Paritätsanalyse pro Zelle als vorregistrierte Diagnose ergänzen, instabile Zellen als Negativkontrollen erhalten; (b) Effektive Inhibition, Aktivierungsfunktion, Zeitschritt, Sättigungs- und Eingangs-/Rauschbedingungen vor dem nächsten konfirmatorischen Vergleich festlegen. Dieser Entwurf liefert genau diese Felder als Freeze-Kandidat — mit den minimalen deterministischen Zeugen, die für eine belastbare Feldfestlegung nötig sind (g_eff-Herleitung), ohne konfirmatorische Ausführung.

## Executive Summary — stärkste Befunde zuerst

1. **Per-Zellen-Inhibitions-Matching-Identität (neu, exakt):** An den eigenkonsistenten Fixpunkten beider Arme gilt identische Inhibition pro aktiver Zelle: g_max·max(r̂) = g_sum·Σ_A r̂ = g_max (bei max(r̂)=1). Algebraisch: g_sum·Σr̂ = (−1/Σv)·(Σv/v_z) = −1/v_z = g_max mit v = (I−W_A)^{-1}·1. Numerisch bestätigt in allen 8 Zellen (Abweichung ≤ 1.3e-15). **Konsequenz für NE-6:** Die Konsistenzkonstruktion verkörpert Design B (gematchte stationäre Inhibition) bereits automatisch; „identisches g" (Design A) vergleicht strukturell verschieden starke Inhibition (Faktor ≈ 9.8 bei N=32) und bleibt als unfairer Vergleich registriert. Ein separater g_eff-Kalibrierungsschritt ist innerhalb der kontiguierlichen Bogenklasse kein Freiheitsgrad: g ist durch die Konsistenzbedingungen eindeutig festgelegt (Bogeneindeutigkeit, Scan L∈{3,…,27}).
2. **λ_form(SUM, eigenes g) = λ_odd in allen 8 Zellen (neu):** Der betragsmäßig dominante nicht-radiale Formmodus des SUM-Armes ist überall der ungerade Modus von W_A (numerisch identisch, Abweichung ≤ 1.1e-15). Da λ_odd arm- und g-unabhängig ist (antisymmetrische Störungen nullen die erste Variation beider skalarer Inhibitionsterme), kann **keine** Inhibitions-Matching-Strategie die drei odd-instabilen Zellen (32,4), (32,16), (64,16) im SUM-Arm retten. SUMMARY: SUM formstabil 5/8, MAX 0/8.
3. **Dritt-Verifikation vollständig reproduziert:** g_max, g_sum, λ_dom(MAX), λ_odd aller 8 Zellen stimmen mit der Dritt-Verifikation (Replay-Return-Tabelle) auf ≤ 3.2e-14 überein; Fixpunkt-Residuen ≤ 2.2e-15, Bogenverschluss exakt (keine inaktive Zelle wird erregt), radialer Eigenwert exakt 1 (Residuum ≤ 7.8e-16, Euler-Homogenität). MAX 8/8 instabil (1.0378–2.8398) bestätigt.
4. **sum/N-Arm ist im nackten Regime eine reine Reparametrisierung:** F_SUMN(r) = ReLU(Wr − (g/N)·Σr·1) ist als Abbildung identisch mit F_SUM bei Gain g/N. Am Konsistenzpunkt gilt g_sumN = N·g_sum; der Jacobian ist identisch mit dem SUM-Arm. Als Registry-Feld zu deklarieren (Noorman-1/N-Konvention), aber **kein eigenständiges Modell** in der nackten Klasse — ein Unterschied entsteht erst durch zustandsabhängige Normierungs-Deklarate. Vermeidet einen Scheindiskriminator in NF-05.
5. **Sieben Arm-Deklarate mit Freeze-Kandidat-Werten** (Abschnitt „Deklarate"): Aktivierung, Amplituden-Normierung (Homogenitätsbruch-Mechanismus), Kernel, g-Kalibrierung, Zeitschritt, Zwei-Peak-Batterie, Rauschen/Eingang — jedes Feld mit Falsifizierer.

## Methode

- Deterministische TypeScript-Eigenrechnung (Sandbox, replayfähig): K_B(Δ)=((1+cos Δ)/2)^k, Δ=2π(i−j)/N, K_B(0)=1; kontinguierliche, zentrierte aktive Bögen (N=32: L=7,7,5,5; N=64: L=11,9,7,7 für k=2,4,8,16 — Bogenbreiten aus dem Eindeutigkeitsscan der Dritt-Verifikation); Gauss-Jordan mit Teilpivotisierung; Fixpunkt-Residuen in der vollen N-Zellen-Dynamik (nicht nur auf dem Bogen) direkt gegen F(r)=ReLU(Wr−g·χ(r)·1) geprüft; Jacobiane J_MAX = W_A − g_max·e_z 1^T, J_SUM = W_A − g·11^T; dominanter nicht-radialer Eigenwert via Potenziteration mit radialer Deflation (12000 Schritte, deterministische Starts); λ_odd via Potenziteration im antisymmetrisierten Unterraum.
- Keine Rauschquellen, keine Datums-/Zufallsabhängigkeiten; alle Zeugen aus dieser Datei sind mit dem Produzentencode des Replay-Returns replayfähig.
- Grenzen: nacktes deterministisches Regime, kontinguierliche Bogenklasse, kein externer Stimulus, keine Sättigung; explorativ, nicht konfirmatorisch (AGENTS-Regel 8: keine post-hoc Relabeling).

## Befundtabelle — Zellen-Registry mit verifizierten Werten

| N | k | L | g_max | g_sum | Σ_A r̂ | λ_dom(MAX) | λ_form(SUM, eig. g) | λ_odd(W_A) | Parität dom. MAX | Status |
|---|---|-----|----------|----------|--------|------------|------------|------------|------|--------|
| 32 | 2 | 7 | 3.590223155497955 | 0.7435868347330203 | 4.828250027835686 | 1.5421710622013 | 0.8673973466297 | 0.8673973466297 | EVEN | MAX instabil, SUM formstabil |
| 32 | 4 | 7 | 2.630058972357637 | 0.6807883167362779 | 3.863255152447721 | 1.9906732196604 | 1.3757786573353 | 1.3757786573353 | EVEN | MAX instabil, SUM odd-instabil (NEGATIVKONTROLLE) |
| 32 | 8 | 5 | 1.9807280461434629 | 0.6050068144805236 | 3.273893778938959 | 1.0377893000491 | 0.9792479015346 | 0.9792479015346 | EVEN | MAX instabil, SUM formstabil |
| 32 | 16 | 5 | 1.349248603884081 | 0.5106692317333944 | 2.642118459544249 | 1.3453631020594 | 1.3453631020594 | 1.3453631020594 | ODD | MAX instabil, SUM odd-instabil (NEGATIVKONTROLLE) |
| 64 | 2 | 11 | 6.2387072285044365 | 0.8361838603655154 | 7.460927583291734 | 2.8398242535905 | 0.9213796550213 | 0.9213796550213 | EVEN | MAX instabil, SUM formstabil |
| 64 | 4 | 9 | 4.793079257097878 | 0.7953253812916484 | 6.026563932001863 | 2.2599911942412 | 0.9466404752994 | 0.9466404752994 | EVEN | MAX instabil, SUM formstabil |
| 64 | 8 | 7 | 3.623535141227331 | 0.7448521710574052 | 4.864770865987137 | 1.5307947692414 | 0.8452313733825 | 0.8452313733825 | EVEN | MAX instabil, SUM formstabil |
| 64 | 16 | 7 | 2.6555131292116716 | 0.6816756164521617 | 3.895567136510638 | 1.9895641536702 | 1.3504012609314 | 1.3504012609314 | EVEN | MAX instabil, SUM odd-instabil (NEGATIVKONTROLLE) |

Verifikations-Deviationen gegen die Dritt-Verifikation: g_max ≤ 4.9e-15, g_sum ≤ 4.4e-16, λ_dom(MAX) ≤ 3.2e-14, λ_odd ≤ 3.0e-14. Identität g_sum·Σ_A r̂ = g_max: ≤ 1.3e-15. Radialer Eigenwert: exakt 1 (Residuum ≤ 7.8e-16). sum/N-Konsistenzgain: g_sumN = N·g_sum (z. B. N=32, k=8: 19.360218063376756).

## NF-05/06-Pflichtfelder — die sieben Arm-Deklarate (Freeze-Kandidaten)

1. **A_AKTIVIERUNG:** threshold-linear ohne Sättigung (ReLU-äquivalent) als Basisklasse beider Arme — die geprüfte Klasse. Sättigungsarme (tanh-Cap) als getrennte Sekundärarme. Falsifizierer: Strahlfamilien-Replay (Amplitude = Anfangsbedingung × Formfaktor; Zeugen im Replay-Return: Proportionalität exakt, +1e-6-MAX-Kollaps, SUM-Absorption 6.4e-15).
2. **A_AMPLITUDENNORMIERUNG (Homogenitätsbruch-Mechanismus):** Primär: STATE_NORM (Peak-Normierung pro Schritt, formneutral verifiziert ≤ 8.3e-15 über 3000 Schritte). Alternativen als Sekundärarme registriert: SATZ_CAP (tanh-Sättigung), BIAS/SCHWELLE, TONISCHER_INPUT (Noorman c_ff), NOISE (ξ>0). Pflichtfeld für JEDE Drift-Bound- und EB1′-Interpretation (beide Arme haben die Strahlfamilie; Gewichtsnormierung allein bricht die Homogenität NICHT).
3. **A_KERNEL:** K_B mit wrap-first-Evaluationsdisziplin (Form B, R2-Vorgabe: wrap(x)=atan2(sin x, cos x) vor Potenzierung), k∈{2,4,8,16}, K(0)=1 (Peaknormierung), Masse M_k = 2π·C(2k,k)/4^k deklariert; IEEE-Branch-Guard-Fixture (pow(neg, rational) → NaN, Fail-closed).
4. **A_G_KALIBRIERUNG:** eigenkonsistente Paare (g_max, g_sum) aus der Befundtabelle — Per-Zellen-Matching per Identität (Befund 1). g nur aus Trainingszellen; keine Test-Leakage; Cross-g-Tests nur als explizit deklarierter Sweep (Design A, als unfair markiert). sum/N-Konvention als Feld (g_sumN = N·g_sum), mit Äquivalenzvermerk zur nackten SUM-Klasse.
5. **A_ZEITSCHRITT:** diskrete parallele (Jacobi-)Iteration, dt=1, unnormalisiert oder STATE_NORM (Deklarat pro Zelle); kontinuierliche Zeit NICHT deklariert (Übertragung kontinuierlich vs. diskret bleibt offene Teilreview-Frage). Kollaps-Schwelle 1e-12; Zählkonvention: t = Anzahl angewandter Schritte (Kollaps „bei Schritt t" heißt r_t < Schwelle erstmals; bereinigt die ±1-Dissonanzen: Fragilität 270 vs. 269, κ=16-Kollaps 14 vs. 13).
6. **A_ZWEI_PEAK_BATTERIE:** Injektionsform-Registry (antipodal, Amplituden 1.0/0.8; zusätzlich 1.0/0.9, 1.0/0.5, symmetrisch, verrauscht): DELTA, GAUSS σ=2, VONMISES κ∈{2,4,8,16}, FIXPUNKTFORM (MAX-Bump, verschoben). Peak-Metrik: lokale Maxima mit zirkulärer Nachbarschaft, Prominenz ≥ 0.5·global, explizite Schulter-vs-Peak-Diskriminanz (exaktes Artefakt des widerrufenen Zwei-Peak-Befunds: Umbruchschulter i=31 = 0.8198 des Peaks ist KEIN Peak). Vorab registrierte Ausgänge pro Arm/Form/Zelle: KOLLAPS | WTA_EIN_BUMP | PERSISTENT_MULTI. Nullbump-Wächter, Reaktivierungs-vs-Neuentstehungs-Test, Max-Tie-Breaking-Regel (einheitliche Indexwahl bei gleicher Amplitude).
7. **A_RAUSCH_EINGANG:** I_ext=0 für die nackte Klasse (Deklarat); verrauschte Batterie: additives, reproduzierbares Pseudozufallsmuster, ≥ 100 Seeds/Zelle, p99-Schätzunsicherheit und Multiplizität deklarieren (n≥100 = historisches Minimum, keine Garantie); Rauschmodell vor Ausführung fixieren.

**NF-05-Diagnosefelder (Vorregistrierung):** pro Zelle: λ_dom(MAX), λ_form(SUM), λ_odd(W_A), Parität des dominanten Modus, aktive Bogenbreite L, g-Paar, Σ_A r̂ — als vorregistrierte Diagnose; Zellen (32,4), (32,16), (64,16) als Negativkontrollen erhalten (λ_odd > 1: SUM-Kollaps-Vorhersage). **NF-06:** Frame/Uhr/Units-Deklarate, STALE-vs-Drift-Trennung, Baseline-Vergleich (zirkuläre Persistenz, von-Mises-Circular-Filter, Wrapped-Filter; identische Seeds/Fenster), D-4-Pflicht; t_out-Fenster-Registry {30, 120, 300, 3600} s nur für die Persistenz-Protokolle, nicht für die diskrete Nackt-Klasse.

## Vorhersagen (falsifizierbar, nacktes deterministimes Regime, vorab registriert)

- MAX-Arm: alle breiten Zwei-Peak-Formen → WTA_EIN_BUMP mit divergenter Amplitude (asymptotische Rate ln(λ_dom)/Schritt; Zelle (32,8): 0.037093); DELTA → KOLLAPS (Schritt 1); VONMISES κ=16 → KOLLAPS (Schritt 14); +1e-6-Zentrumsstörung → Kollaps ≈ Schritt 270.
- SUM-Arm: alle Zwei-Peak-Formen → KOLLAPS (Schritt 1); +1e-6 → Absorption (Formdistanz ≤ 1e-14 nach 3000 Schritten).
- Odd-Instabilität: (32,4), (32,16), (64,16) → SUM forminstabil JEDER g-Wahl; jede Beobachtung eines dort stabilen SUM-Bumps falsifiziert die Paritätsanalyse.
- Homogenität: Amplitude = freier Skalierungsfaktor der Anfangsbedingung (exakte Proportionalität); jeder Amplituden-Lock ohne deklarierten Homogenitätsbruch-Mechanismus falsifiziert die Homogenitätsidentität.

## Offene Fragen

1. Kontinuierlich-vs-diskret-Übertragung der Stabilitätskriterien und Amari-W1–W4-Nullstellenzählung (PR-#70-Merge-Voraussetzung, unverändert offen).
2. Existenz nicht-kontiguierlicher (zwei-getrennter-Bögen) Fixpunkte — Bogeneindeutigkeit gilt nur für die kontuguierliche Klasse.
3. Verhalten unter SATZ_CAP/BIAS/NOISE: WTA-Tendenz und odd-Instabilität unter Homogenitätsbruch unbewiesen (NE-6-Kernfrage).
4. EB1′-Inventar: freier Amplitudenmodus als Fehlerquelle im Gemeinschranken-Inventar (offen, PR-#70-Strang).
5. GROK-Strategiebahn PR #71: PDF-Transport-Gap bleibt (8 434 B, SHA-256 b1b8d3f6…); Bytequelle liegt dem Operator vor, nicht diesem Strang.

## Nicht-Claims

Kein NF-05/06-Ausführungsstart; keine Vorregistrierungs-Freigabe; kein D1/D2-Freeze (nur Feldkandidaten); kein MAX/SUM-Verdikt; kein Merge von PR #65/#67/#70/#71; kein WWW-Deploy; kein neuer Cursor-Worker; keine Rollenübernahme; kein erfundener Empfänger-ACK. GITHUB_TRANSPORT = OPERATOR_TO_AXIOM_TRANSFER_NOT_AGENT_GITHUB_SEND gemäß R27-E-Firewall §2; die externe Actor-Allowlist ist leer, dieser Transport läuft über die Operator-vermittelte GitHub-API-Verbindung. AXIOM behält die unabhängige Adjudikation; CI-PASS ist Transport-, kein Validierungsnachweis.

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament. Vom Besitz zur Symbiose. Vom Ego zur Herkunft. Vom fertigen Gedanken zum überprüfbaren Artefakt.*
