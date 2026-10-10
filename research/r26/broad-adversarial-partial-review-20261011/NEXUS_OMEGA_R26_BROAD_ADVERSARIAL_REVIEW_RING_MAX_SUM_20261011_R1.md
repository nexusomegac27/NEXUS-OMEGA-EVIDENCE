# NEXUS OMEGA · R26 — Breiteres adversariales Review: Ringstabilität und MAX/SUM-Inhibition (C1, Teilreview)

**Objekt:** NEXUS_OMEGA_R26_BROAD_ADVERSARIAL_REVIEW_RING_STABILITY_MAX_SUM_20261011_R1
**Typ:** Unabhängiger Arbeitsbericht, Teilreview (kein vollständiges adversariales R26-PASS; kein zugewiesener External-Research-Return; keine kanonische Übergabe behauptet)
**Claim-Deckel:** `C1_DESCRIPTIVE_ONLY`
**Experimente:** `NOT_EXECUTED` · Keine HOLD-Anhebung · Kein NF-Ausführung · Kein neuer Cursor-Worker · Kein Production-Write
**Transport:** Bereits bestätigte GitHub-Hash-/Transport-Nachweise werden NICHT erneut geprüft.

---

## 1 · Auftrag und Versionsbindung

AXIOM benennt in der [PR-#73-Adjudikation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/92cb92b94201a69e5c849b7cbae111458d953a3b/research/r26/meta-independent-review-20261010/NEXUS_OMEGA_AXIOM_META_R26_R2_SCOPED_CROSS_REVIEW_ADJUDICATION_20261010_R0.md) als nächsten sinnvollen Schritt „das verbleibende breitere adversarielle Review, insbesondere der Ringstabilität und der MAX-/SUM-Modellvergleiche". Dieser Bericht führt genau diese Prüfung als **Teilreview** durch.

**Versionsbindung:** Untersucht wird der aktuelle [PR-#70](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/70)-Head **`41ab803d415a72c12a29babc9c4c4929534fdecf`** (über `.head.sha` ermittelt). Gelesen wurden:

- [R26-03_R1 — in Kraft](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R1.md) (200 Zeilen, vollständig)
- [R26-03_R2 — Präzisierungsannotation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R2.md)
- [NA-1 Ring Stabilizer Spec](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/17e0a3275ad9749458e251b1ec4eb07348b2c5ee/research%2Fr10r23%2Fna1-ring-stabilizer%2Forders%2FNA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0.md) (PR-#65-Head `17e0a327`; relevante Modell- und Protokollabschnitte gelesen)
- [R25-03 Ring and Orbit Error Model](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/1fcda32defea8e43f15380346b2c115527f47f9b/research%2Fr25%2Fexternal-expert-archive-20261010%2FR25-03_RING_AND_ORBIT_ERROR_MODEL.md) (PR-#67-Head `1fcda32d`; relevante Modellabschnitte §1–§3 gelesen)
- [R26-03_R0 — historisch](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/0b00c859ae02b9bd2aa9fd34a1158a554eefb23e/research%2Fr26%2Fmistral-vibe-priority-tracks-20261010%2FR26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT.md) (`SUPERSEDED_PRESERVED`; Zeugen W1–W4 werden von R1 §1 ausdrücklich unverändert fortgeführt)

---

## 2 · Modellgegenüberstellung (aus NA-1-Spec und R25-03)

| Dimension | [MODEL_MAX (NA-1-Spec §3)](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/17e0a3275ad9749458e251b1ec4eb07348b2c5ee/research%2Fr10r23%2Fna1-ring-stabilizer%2Forders%2FNA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0.md) | [MODEL_SUM (R25-03 §2)](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/1fcda32defea8e43f15380346b2c115527f47f9b/research%2Fr25%2Fexternal-expert-archive-20261010%2FR25-03_RING_AND_ORBIT_ERROR_MODEL.md) |
|---|---|---|
| **Update** | `h_i(t+1) = Σ_j W_ij·r_j(t) − g_inhib·max_j r_j(t) + I_ext(θ_i,t)` | `r_i(t+1) = f(Σ_j W_ij r_j(t) − g_inhib·Σ_k r_k(t) + I_ext(θ,t) + ξ_i(t))` |
| **Aktivierung** | `r_i(t+1) = max(0, h_i(t+1))` (ReLU; „bzw. tanh-Cap; beide dokumentieren") | `f` = sättigende Nichtlinearität („e.g. ReLU or sigmoid") |
| **Rauschterm** | keiner deklariert | `ξ_i(t)` (Kandidat: unabhängig Gaussian oder circular) |
| **Gewichte** | `W_ij = w0 + w_exc·cos((θ_i−θ_j)/2)^p` | `W_ij` = lokaler excitatorischer Kern („e.g. cosine or Gaussian") |
| **N** | {32, 64} | {32, 64} |
| **Readout** | PVA | PVA |
| **Normierung** | keine deklariert | keine deklariert |

**Offene Punkte:** (a) Aktivierungsfunktion (ReLU vs. tanh-Cap/Sigmoid — beides erlaubt, muss fixiert werden); (b) kein Zeitschritt-Deklarat; (c) keine 1/N-Gewichtsnormierung deklariert; (d) `w0`/`w_exc`/`g_inhib`-Wertebereiche; (e) ξ_i-Verteilung (nur Kandidaten).

---

## 3 · Neuer Befund: Positive Homogenität beider Arme (Amplitudenneutralität)

**Allgemeine Identität:** Bei festem W und g, ReLU-Aktivierung, ohne additive Eingänge (I_ext = 0) und ohne Rauschterm (ξ = 0) gilt für beide Inhibitionsoperatoren P_MAX(r) = max_j r_j und P_SUM(r) = Σ_j r_j:

\[ F_P(α·r) = [α·W·r − g·α·P(r)·1]₊ = α·F_P(r), \quad α > 0 \]

(Der Beispielring illustriert die Identität; er beweist sie nicht. Der Beweis folgt aus der positiven Homogenität vom Grad 1 von ReLU, W·r und beiden P.)

**Deterministische Illustration** (Beispielring, α=3):

- **MODEL_MAX:** `F_MAX(α·r) vs. α·F_MAX(r)` — maximale Abweichung 4,44·10⁻¹⁶ (numerische Rundung).
- **MODEL_SUM:** `F_SUM(α·r) vs. α·F_SUM(r)` (I_ext=0, ξ=0, f=ReLU) — maximale Abweichung 4,44·10⁻¹⁶.

**Konsequenz (beide Arme):** Für jeden vorhandenen nichtnulligen Fixpunkt r* existiert eine skalierte Fixpunktfamilie (α·r* für alle α>0). Deshalb ist die **isolierte asymptotische Stabilität eines einzelnen solchen Fixpunkts ausgeschlossen**. An differenzierbaren Stellen besitzt der Update-Jacobian die radiale Eigenrichtung r* mit Eigenwert 1. Das bestätigt weder die Existenz eines nichtnulligen Fixpunkts noch Instabilität der gesamten Familie. Lyapunov-Stabilität, Formpersistenz und Ein-Peak-Struktur bleiben davon unentschieden. Das ist von einer neutralen **Phasenrichtung** (Rotationssymmetrie) zu unterscheiden. Die optionale tanh-Cap-/Sigmoid-Variante ist **nicht** positiv homogen und muss getrennt behandelt werden.

**Grenzen dieses Befunds:** (1) Nur für ReLU, I_ext=0, ξ=0 nachgewiesen; (2) gilt für beide Arme gleich, diskriminiert also nicht zwischen MAX und SUM; (3) keine Aussage über Formpersistenz, Phasenneutralität, Lyapunov-Stabilität oder Ein-Peak-Struktur; (4) tangiert die MAX/SUM-Regionshypothese nicht direkt; (5) ist kein Gegenbeweis gegen ein Ein-Peak-Profil.

---

## 4 · Reviewmatrix

Format: **Behauptung → genaue Modellversion → analytischer Check → Literaturbezug → Gegenfall → Urteil → fehlende Voraussetzung**.

### 4.1 R1 §4 — Modenverhältnis-Formel und Richtung

| Dimension | Inhalt |
|---|---|
| **Modellversion** | R26-03_R1 §4, K_B(Δ) = Σ_m c_m e^{imΔ}, c_m = C(2k, k+m)/4^k |
| **Analytischer Check** | `R(k) = (k−1)/(k+2)`: k=2 → 0,25; k=4 → 0,50; k=8 → 0,70; k=16 → 0,833; k=32 → 0,912. `R'(k) = 3/(k+2)² > 0` → monoton steigend. **Formel korrekt, Richtung strikt steigend.** |
| **Falsifizierer** | R1 §7.3 — deterministisch bestanden. |
| **Urteil** | **PASS** (Koeffizientenrechnung) |

### 4.2 R1 §4 — „Mode-separation margin 3/(k+2) DECREASING"

| Dimension | Inhalt |
|---|---|
| **Analytischer Check** | `1−R(k) = 3/(k+2)`: 0,75 → 0,50 → 0,30 → 0,167 → 0,088 (monoton fallend); absoluter Rand `c₁−c₂`: 0,188 → 0,0085. **Algebraisch nachvollziehbar.** |
| **Gegenfall** | „Single-Bump-Onset fragiler" ist eine modellabhängige Interpretation, kein eigenständig bestätigter Robustheitsbefund. |
| **Urteil** | **PASS** (Koeffizientenrechnung) · **BEDINGT** (Onset-Inferenz) |

### 4.3 R1 §5 — MAX/SUM auf REGISTERED_HYPOTHESIS herabgestuft

| Dimension | Inhalt |
|---|---|
| **Analytischer Check** | Bei nichtnegativen Aktivitäten, **gleichem positivem Inhibitionsgain** und nichtnegativen r gilt `Σ_j r_j ≥ max_j r_j` — nur eine größere momentane Subtraktion, **keine** allgemeine Inklusion stabiler Multi-Peak-Parameterregionen. |
| **Skalierung** | ReLU ist nicht Heaviside: Summeninhibition skaliert allgemein mit der Aktivitätsmasse `A = Σ_j r_j`, nicht allein mit der Anzahl aktiver Neuronen. Bei `M = max_j r_j > 0` gilt `1 ≤ A/M ≤ N`; Gleichsetzung mit einer aktiven Neuronenzahl setzt gleiche Aktivitätshöhen voraus. |
| **Differenzierbarkeit** | MAX ist bei mehreren gleich großen Maxima nicht differenzierbar → keine eindeutige Linearisierung; eine Linearisierung um einen einzelnen Gewinner beantwortet symmetrische Multi-Peak-Fälle nicht. |
| **Rauschterm** | Im SUM-Arm steht zusätzlich ξ_i; ein Unterschied wäre nicht ausschließlich der Inhibitionsoperation zurechenbar. |
| **Vergleichsdesigns** | (a) identischer Gain und (b) baseline-abgeglichen (explizite Normierungswahl) beantworten unterschiedliche Fragen; (b) wäre ein eigener DESIGN_ONLY-Vergleich. |
| **Urteil** | **PASS** — Herabstufung korrekt und wird bestätigt |

### 4.4 NA-1-Spec — „Max-Term sichert Bump-Einzigkeit"

| Dimension | Inhalt |
|---|---|
| **Gegenfall** | Die kategorische MAX-Einzigkeitsgarantie ist **nicht nachgewiesen**. [R25-03 §2](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/1fcda32defea8e43f15380346b2c115527f47f9b/research%2Fr25%2Fexternal-expert-archive-20261010%2FR25-03_RING_AND_ORBIT_ERROR_MODEL.md) formuliert dagegen eine vorsichtigere allgemeine Grenze („Uniqueness of a single bump is **not** guaranteed by global inhibition alone. Multi-peak and oscillatory regimes exist."). Beide Aussagen müssen modell- und parameterbezogen abgegrenzt werden; die Gegenüberstellung liefert keinen Gegenbeweis gegen Ein-Peak-Verhalten eines konkret parametrisierten MAX-Modells. Einzigkeit und die größere Multi-Peak-Parameterregion sind zudem unterschiedliche Behauptungen. |
| **Urteil** | **NICHT NACHGEWIESEN** |
| **Fehlende Voraussetzung** | Kein Beweis; NE-1 (MULTIPEAK_INJECTION) ist der vorgesehene Prüfpfad |

### 4.5 R26-03_R0 §7 — Amari-Zeugen W1–W4 (aus R0 durch R1 fortgeführt)

| Dimension | Inhalt |
|---|---|
| **Hinweis** | [R26-03_R1 §1](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R1.md) übernimmt W1–W4 ausdrücklich unverändert („Retained from R0, unchanged in force"). Sie sind nicht nur historisch, sondern fortgeführt. |
| **Numerische Reproduktion** | Der numerische Suchlauf fand **zwei Kandidaten** für W1 (a≈0,4232, 1,1187), **einen** für W3 (a≈0,2962) und **keine** für W2/W4. Kanten: W1 a=1,1187 → 0,036 < 0,3; W3 → 0,837 > 0,1. Keine mathematisch vollständige Nullstellenzählung behauptet. |
| **Grenzen** | **Numerische Nullstellenkandidaten und Kantenwerte reproduziert; vollständige Nullstellenzählung, Profilkonsistenz und dynamische Stabilität nicht bestätigt.** Falls Vollständigkeit benötigt: monotone Intervalle über `F'(a) = 2(w_exc·K(2a) − g_eff)` abgrenzen. |
| **Urteil** | **BEDINGT** — Kandidaten reproduziert; Stabilitätsaussage unter Vorbehalten |

### 4.6 R1 §3 — D1-Freeze-Felder

**Urteil: PASS** — FUNCTION, WRAP_CONVENTION, ENDPOINTS, SMOOTHNESS, NORMALIZATION, SOFTWARE_SEMANTICS, HISTORICAL_MAPPING als verbindliche Deklaration; R2 erweitert auf 11 Felder.

### 4.7 R2 §4 — Floating-Point-Präzision am Antipoden

| Dimension | Inhalt |
|---|---|
| **Befund** | **Teilweise tragfähig, mit bereits adjudiziertem Gegenbefund** ([AXIOM-Adjudikation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/92cb92b94201a69e5c849b7cbae111458d953a3b/research/r26/meta-independent-review-20261010/NEXUS_OMEGA_AXIOM_META_R26_R2_SCOPED_CROSS_REVIEW_ADJUDICATION_20261010_R0.md) C1-2): Die dokumentierte Auslöschung in `1+cos Δ` (Form A) motiviert eine numerisch sorgfältigere Auswertung; Form A verliert bei Δ=π−1e-9 relative Präzision (100% Abweichung). Aber: die universelle Antipoden-Schranke `1e-16` ist **falsch** (AXIOM-Adjudikation C1-2 widerlegt sie; `|cos(π/2)|^0.5 / 1e-16 = 7,8251·10⁷` ≈ 78,25 Millionen). Wrap-first ist eine dokumentierte **Implementierungsvorgabe**, keine bewiesene einzig zulässige oder allgemein ausreichend genaue Auswertung. Die `T(p)`-Toleranzregel stammt aus dem **[META-Review](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/2505ec8e7a611c6764fe6c505afecf8798adbcbb/research%2Fr26%2Fmeta-independent-review-20261010%2FMETA_AI_R26_R2_C1_SCOPED_CROSS_REVIEW_SOURCE_EXACT_20261010_R0.txt)** (PR #73), nicht aus der Produzenten-R2; sie ist Testkandidat, nicht ratifiziert. |
| **Urteil** | **BEDINGT** — Auslöschungsphänomen bestätigt; universelle Schranke widerlegt; wrap-first als Vorgabe dokumentiert |

---

## 5 · Literaturprüfung (gelesen, versionsgenau)

### Noorman et al. 2024 — rekurrente Eingangsgleichung (über [nature.com](https://www.nature.com/articles/s41593-024-01766-5))

- **Rekurrente Gewichte:** `W_jk^sym = J_I + J_E·cos(θ_j − θ_k)`; **Input:** `h_j = c_ff + (1/N)·Σ_k (…)·r_k` mit φ = ReLU, τ=0,1 s. **Die eigentliche dynamische Gleichung (1) fehlte im ausgegebenen Text** — nur die rekurrente Eingangsgleichung und 1/N-Normierung wurden gelesen.
- **Inhibition:** Uniformes `J_I` → `J_I·(1/N)·Σ_k r_k` additive Inhibition. **Keine MAX-Inhibition im gelesenen Material.**
- **Multi-Peak/Einzigkeit:** Zwei Sätze von N Fixpunkten (ein stabiler, ein instabiler) für die meisten Parameter; keine explizite Multi-Peak-Koexistenz-Diskussion, kein allgemeiner Einzigkeitsbeweis.

**Tragfähiger Literaturvergleich:** Im gelesenen Noorman-Modellmaterial findet sich eine uniforme, summengekoppelte Inhibition mit 1/N-Normierung; ein MAX/SUM-Stabilitätsvergleich wurde dort nicht gefunden. Das unterstützt die begrenzte Modellgegenüberstellung, nicht einen Stabilitätsnachweis für NA-1. Die Herabstufung einer unbelegten Behauptung ist vernünftig; sie wird nicht dadurch „von der Literatur bestätigt", dass diese Literatur den Vergleich nicht behandelt.

### NA-1-Spec-Literaturhinweise (hier nicht unabhängig geprüft; übernommene Projektbewertungen)

- [Kim et al., Science 356 (2017)](https://doi.org/10.1126/science.aal4835) — `PRIMARY_FULLTEXT_CHECKED` laut Spec (übernommene Projektbewertung, keine eigene Prüfung).
- [Seeholzer et al., PLOS Comput. Biol. (2019)](https://doi.org/10.1371/journal.pcbi.1006928) — `PUBLISHER_ABSTRACT_CHECKED` laut Spec.
- [Kurz et al., arXiv:1501.05151](https://arxiv.org/abs/1501.05151) — `PREPRINT_CHECKED` laut Spec.

### Weitere Literatur (nur über Suchauszüge gelesen)

- [Yousaf/Einevoll/Tetzlaff, BMC Neuroscience](https://bmcneurosci.biomedcentral.com/articles/10.1186/1471-2202-12-S1-P377) — Abstract zu Existenz/Einzigkeit/Stabilität von Bump-Lösungen.
- [Cihak/Kilpatrick, SIAM](https://pmc.ncbi.nlm.nih.gov/articles/PMC11781529/) — Suchauszug zu Bump-Dynamik.
- Laing-Troy-Originalarbeit: **nicht aufgelöst**; Belegzuordnung wird nicht verwendet.

---

## 6 · Fehlende Voraussetzungen (Prüfungsgrenzen)

1. Vollständige Stabilitätskriterien-Übertragung: kontinuierlich Realteile vs. diskret Beträge; neutraler Phasenmodus Eigenwert 0 (kontinuierlich) bzw. 1 (diskret).
2. Vollständige Nullstellenzählung für die Amari-Zeugen (nur Kandidaten reproduziert).
3. Bedeutung von „stabil" (Breitenstabilität bei neutraler Translation vs. vollständige asymptotische Stabilität).
4. Herleitung von `g_eff` aus dem tatsächlichen MAX-/SUM-Modell.
5. Homogenitätsbefund (§3) nur für ReLU, I_ext=0, ξ=0; tanh-Cap/Sigmoid-Variante getrennt zu behandeln.

**Konsequenz:** Für die Frage „ist MAX- oder SUM-Stabilität besser?" lautet das Urteil **NICHT ENTSCHEIDBAR**. Die NA-1-Spec und R25-03 enthalten die entscheidenden Definitionen (ReLU-Aktivierung, diskrete Zeit, N, Gewichte, MAX/SUM-Inhibition, ξ_i-Rauschterm); die verbleibenden Lücken sind Normierung, g_eff-Herleitung und Stabilitätskriterien-Übertragung.

---

## 7 · Zusammenfassung und Urteile

| Prüfpunkt | Urteil |
|---|---|
| R1 §4 Modenverhältnis-Formel und Richtung | **PASS** |
| R1 §4 Separationsrand fallend (Koeffizienten) | **PASS** · Onset-Inferenz **BEDINGT** |
| R1 §5 MAX/SUM auf REGISTERED_HYPOTHESIS | **PASS** |
| NA-1-Spec „Max-Term sichert Einzigkeit" | **NICHT NACHGEWIESEN** (R25-03 formuliert eine vorsichtigere allgemeine Grenze; beide Aussagen modell- und parameterbezogen abzugrenzen) |
| R0 §7 Amari-Zeugen W1–W4 (fortgeführt) | **BEDINGT** (Kandidaten reproduziert) |
| R1 §3 D1-Freeze-Felder | **PASS** |
| R2 §4 Antipoden-Präzision | **BEDINGT** (Auslöschung bestätigt; Schranke widerlegt; wrap-first als Vorgabe) |
| Homogenität beider Arme (neu, §3) | **BESTÄTIGT** für ReLU, I_ext=0, ξ=0 (beide Arme; für jeden vorhandenen nichtnulligen Fixpunkt existiert eine skalierte Fixpunktfamilie, isolierte asymptotische Stabilität ausgeschlossen) |
| MAX/SUM-Stabilitätsrangfolge | **NICHT NACHGEWIESEN** |
| Vollständige Stabilitätsentscheidbarkeit | **NICHT ENTSCHEIDBAR** |

**Gesamturteil (Teilreview):** Die algebraischen Modenverhältnisse sind nachvollziehbar; die MAX/SUM-Regionsbehauptung wird korrekt als Hypothese geführt; eine allgemeine Stabilitätsrangfolge und deren Übertragung aus den Amari-Kriterien ist nicht nachgewiesen. Neu bestätigt: Für jeden vorhandenen nichtnulligen Fixpunkt existiert in beiden deterministischen ReLU-Armen eine skalierte Fixpunktfamilie — isolierte asymptotische Stabilität eines einzelnen solchen Fixpunkts ist ausgeschlossen; der Befund trifft beide Arme gleich und diskriminiert nicht. Die kategorische MAX-Einzigkeitsgarantie ist nicht nachgewiesen; R25-03 formuliert eine vorsichtigere allgemeine Grenze. Die tanh-Cap-/Sigmoid-Variante muss getrennt behandelt werden. NF-05 bleibt der vorgesehene, noch nicht ausgeführte Prüfpfad; analytische Beweise, Gegenbeispiele und weitere spezifizierte Vergleiche bleiben möglich.

---

## 8 · Nächste Schritte

1. **MISTRAL/VIBE/Operator:** Aktivierungsfunktion fixieren (ReLU vs. tanh-Cap); Zeitschritt-Deklarat und Gewichtsnormierung ergänzen; g_eff-Herleitung dokumentieren.
2. **AXIOM:** MAX/SUM-Hypothese als REGISTERED_HYPOTHESIS einfrieren; NE-6 als vorgesehenen DESIGN_ONLY-Prüfpfad mit expliziter Normierungswahl führen; analytische Beweise, Gegenbeispiele und weitere spezifizierte Vergleiche bleiben möglich.
3. **Forschung:** Die NA-1-Spec-Aussage „Max-Term sichert Bump-Einzigkeit" mit der R25-03-Aussage („not guaranteed by global inhibition alone") harmonisieren — kategoriale Formulierung streichen oder als Hypothese markieren.
4. **Status halten:** PR70 bleibt OPEN; PR65/PR67-HOLDs unangetastet; keine Experimente, keine HOLD-Anhebung, kein neuer Cursor-Worker, kein Production-Write.

---

## 9 · Quellen

### Gelesene Literatur
- [Noorman, M., Hulse, B. K., Jayaraman, V., et al. (2024). Nature Neuroscience — rekurrente Eingangsgleichung über nature.com](https://www.nature.com/articles/s41593-024-01766-5) (1/N-Normierung, additive Inhibition; dynamische Gleichung (1) fehlte im ausgegebenen Text; zwei Fixpunkt-Sätze).
- [Yousaf, M., Einevoll, G. T., & Tetzlaff, R. (2011). BMC Neuroscience](https://bmcneurosci.biomedcentral.com/articles/10.1186/1471-2202-12-S1-P377) (nur Suchauszug).
- [Cihak, H. L., & Kilpatrick, Z. P. (2024). SIAM](https://pmc.ncbi.nlm.nih.gov/articles/PMC11781529/) (nur Suchauszug).

### NEXUS-Quellen (projektintern, versionsgebunden)
- [R26-03_R1 — in Kraft, PR-#70-Head 41ab803d](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R1.md)
- [R26-03_R2 — Präzisierungsannotation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/41ab803d415a72c12a29babc9c4c4929534fdecf/research/r26/mistral-vibe-priority-tracks-20261010/R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R2.md)
- [NA-1 Ring Stabilizer Spec — PR-#65-Head 17e0a327](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/17e0a3275ad9749458e251b1ec4eb07348b2c5ee/research%2Fr10r23%2Fna1-ring-stabilizer%2Forders%2FNA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0.md)
- [R25-03 Ring and Orbit Error Model — PR-#67-Head 1fcda32d](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/1fcda32defea8e43f15380346b2c115527f47f9b/research%2Fr25%2Fexternal-expert-archive-20261010%2FR25-03_RING_AND_ORBIT_ERROR_MODEL.md)
- [R26-03_R0 — historisch, SUPERSEDED_PRESERVED](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/raw/0b00c859ae02b9bd2aa9fd34a1158a554eefb23e/research%2Fr26%2Fmistral-vibe-priority-tracks-20261010%2FR26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT.md)
- [PR #70 — aktueller Head 41ab803d](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/70)
- [PR #73 — META-Intake und AXIOM-Adjudikation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/73)
- [AXIOM META-R26-R2-Adjudikation](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/92cb92b94201a69e5c849b7cbae111458d953a3b/research/r26/meta-independent-review-20261010/NEXUS_OMEGA_AXIOM_META_R26_R2_SCOPED_CROSS_REVIEW_ADJUDICATION_20261010_R0.md)

### Literaturhinweise der NA-1-Spezifikation (hier nicht unabhängig geprüft)
- [Kim et al., Science 356 (2017)](https://doi.org/10.1126/science.aal4835) · [Seelig & Jayaraman, Nature 521 (2015)](https://doi.org/10.1038/nature14446) · [Seeholzer et al., PLOS Comput. Biol. (2019)](https://doi.org/10.1371/journal.pcbi.1006928) · [Kurz et al., arXiv:1501.05151](https://arxiv.org/abs/1501.05151)

---

**NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.**
