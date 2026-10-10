# R26 Teilreview-Synthese: Ringstabilität und MAX/SUM — Unabhängige Verifikation

**Objekt:** NEXUS_OMEGA_R26_BROAD_ADVERSARIAL_REVIEW_RING_STABILITY_MAX_SUM_20261011_R1 (Teilreview, `C1_DESCRIPTIVE_ONLY`, `EXPERIMENTS = NOT_EXECUTED`)
**Rahmen dieser Synthese:** Unabhängige Nachprüfung der überprüfbaren Kernbehauptungen des Berichts — Algebra, Identitäten, Literaturbasis. Keine Netzwerkexperimente, keine NF-Ausführung, keine HOLD-Anhebung, kein Production-Write. Diese Synthese ist ein Arbeitsbeitrag: keine kanonische Übergabe, keine Adjudikation.

---

## Frage

Sind die zentralen Behauptungen des breiten adversarialen Teilreviews — Modenverhältnis-Algebra, fallender Separationsrand, positive Homogenität beider Arme, Literaturbefunde zu Noorman 2024 und zur Bump-Einzigkeit — unabhängig korrekt? Welche Konsequenzen ergeben sich daraus für die R26-Kette (NA-1-Spec, Drift-Bound-Protokoll, NF-05/NE-1/NE-6)?

---

## Executive Summary

1. **Modenverhältnis-Algebra vollständig bestätigt.** `R(k) = (k−1)/(k+2)` stimmt numerisch exakt für k ∈ {2, 4, 8, 16, 32}; `1−R(k) = 3/(k+2)` identisch; `R′(k) = 3/(k+2)² > 0` analytisch korrekt. Beide R1-PASS-Urteile (Formel, fallender Rand) werden unabhängig bestätigt; die Onset-Inferenz bleibt korrekt als BEDINGT geführt.
2. **Homogenitätsbefund reproduziert.** `F(α·r) = α·F(r)` gilt für MAX und SUM (ReLU, I_ext=0, ξ=0) mit einer Abweichung in der Größenordnung 10⁻¹⁴ (Rundung). Die Schlussfolgerung — skalierte Fixpunktfamilien, keine isolierte asymptotische Stabilität, radiale Eigenrichtung mit Eigenwert 1 — ist mathematisch korrekt und trifft beide Arme gleich.
3. **Literaturbefunde gestützt.** Noorman et al. 2024 arbeiten mit lokaler Kosinus-Erregung und breiter uniformer (summengekoppelter) Inhibition; ein MAX/SUM-Stabilitätsvergleich findet sich dort nicht. Die Multi-Bump-Literatur zu Amari-Typ-Modellen stützt die vorsichtige R25-03-Formulierung, wonach globale Inhibition allein keine Ein-Bump-Einzigkeit garantiert.
4. **Zusatzbefund (eigene Einordnung).** Die positive Homogenität ist kein MAX/SUM-Spezifikum, sondern generisch für schwellenfreie, nicht-sättigende Ratenmodelle ohne Bias — sie träfe ebenso das Noorman-Modell. Konsequenz: Amplitudenkontrolle erfordert Sättigung (tanh-Cap), Schwellen, Rauschen (ξ) oder Normierung. Für das NA-1-Drift-Bound-Protokoll ist das eine harte Voraussetzung, kein Formdetail.
5. **Urteilsstruktur des Teilreviews ist konsistent.** MAX/SUM-Rangfolge NICHT NACHGEWIESEN; vollständige Stabilitätsentscheidbarkeit NICHT ENTSCHEIDBAR; die NA-1-Einzigkeitskategorialformulierung bleibt unbewiesen; NE-1 (MULTIPEAK_INJECTION) und NF-05 bleiben die vorgesehenen Prüfpfade.

---

## Methodik

- **Algebra-Check:** Exakte Binomialkoeffizienten `c_m = C(2k, k+m)/4^k`, deterministische Auswertung (reine Arithmetikprüfung, keine Modellsimulation).
- **Homogenitäts-Check:** Illustrationsring N=16, Zufallsgewichte, α=3, beide Inhibitionsoperatoren; Bestätigung der Identität bis auf Rundung.
- **Literaturrecherche:** Web-Suche nach Primärquellen (Noorman 2024, Kim 2017, Amari-/Neural-Field-Literatur); Auszuglese über Suchsnippets, kein Volltext-Retest der Noorman-Gleichung (1) — die Lückenmeldung des Berichts bleibt bestehen.
- **Nicht re-verifiziert:** Amari-Zeugen W1–W4 (vollständige Parametersätze fehlen im Extrakt), GitHub-Transportnachweise (per Bericht bereits bestätigt), R2 §4 Antipoden-Präzision (Gegenstand der AXIOM-Adjudikation C1-2, dort maßgeblich).

---

## Befunde

### 1 · Modenverhältnis-Algebra — BESTÄTIGT

| k | R(k) numerisch | R(k) Formel | 1−R(k) | 3/(k+2) | c₁−c₂ |
|---|---|---|---|---|---|
| 2 | 0,2500 | 0,2500 | 0,7500 | 0,7500 | 0,1875 |
| 4 | 0,5000 | 0,5000 | 0,5000 | 0,5000 | 0,1094 |
| 8 | 0,7000 | 0,7000 | 0,3000 | 0,3000 | 0,0524 |
| 16 | 0,8333 | 0,8333 | 0,1667 | 0,1667 | 0,0220 |
| 32 | 0,9118 | 0,9118 | 0,0882 | 0,0882 | 0,0085 |

- `R′(k) = 3/(k+2)² > 0` ⇒ strikt monoton steigend; Separationsrand `3/(k+2)` strikt fallend; absoluter Rand `c₁−c₂` fällt von 0,1875 auf 0,0085 — deckungsgleich mit den Berichtswerten (0,188 → 0,0085).
- **Urteil:** Beide PASS-Urteile des Berichts (Koeffizientenrechnung, Richtung) unabhängig bestätigt. Die Inferenz „Single-Bump-Onset fragiler" bleibt korrekt als BEDINGT geführt (modellabhängige Interpretation).

### 2 · Positive Homogenität — BESTÄTIGT, mit Einordnung

- **Numerisch:** Maximale Abweichung ≈ 1,6·10⁻¹⁴ (N=16, α=3, beide Arme; deterministische Illustration). Konsistent mit der Berichtsmessung (4,44·10⁻¹⁶ am Beispielring).
- **Analytisch:** ReLU, `W·r` und beide Inhibitionsoperatoren (max, Σ) sind positiv homogen vom Grad 1; die Identität folgt unmittelbar. Der Bericht trennt sauber zwischen Illustration und Beweisgrund.
- **Einordnung:** Der Befund ist schwächer als er klingen könnte — er schließt isolierte asymptotische Stabilität einzelner Fixpunkte aus, sagt aber nichts über Formpersistenz, Ein-Peak-Struktur oder Lyapunov-Stabilität der Familie. Er ist zudem **generisch**: jedes nicht-sättigende Ratenmodell ohne Schwellen/Bias mit homogenter Kopplung (auch das Noorman-Modell mit uniformer Summeninhibition) besitzt dieselbe Eigenschaft. Die Aussage „trifft beide Arme gleich, diskriminiert nicht" ist daher korrekt und ohne MAX/SUM-Diskriminierungskraft.
- **Konsequenz für NA-1:** Jede Drift-Bound- oder Amplitudenstabilitätsaussage, die implizit eine fixe Bump-Amplitude annimmt, benötigt einen Mechanismus, der die Skalierungsfreiheit bricht — tanh-Cap, Schwellen, Rauschterm ξ oder Normierung. Die Berichtsforderungen „Aktivierungsfunktion fixieren" und „Gewichtsnormierung ergänzen" sind damit **harte Voraussetzungen**, nicht Formdetails.

### 3 · Literaturprüfung — GESTÜTZT

- **Noorman et al. 2024 (Nature Neuroscience):** Primärquelle bestätigt die Berichtslesart — „local cosine-tuned excitation and broad uniform inhibition"; die rekurrente Kopplung ist kosinusförmig mit J_E/J_I und breiter uniformer (summengekoppelter) Inhibition. Ein MAX-Inhibitionsoperator oder ein MAX/SUM-Stabilitätsvergleich findet sich im zugänglichen Material nicht. Die Berichtslücke (dynamische Gleichung (1) nicht im ausgegebenen Text) bleibt bestehen und wird hier nicht behoben.
- **Bump-Einzigkeit:** Die Neural-Field-Literatur zu Amari-Typ-Modellen kennt explizite Ein-Bump-Lösungen (Amari 1977), aber auch Zwei-/Multi-Bump-Lösungen und -Familien (u. a. Laing & Troy 2003); laterale Inhibition allein gilt nicht als hinreichend für allgemeine Einzigkeit. Das stützt die vorsichtige R25-03-Formulierung („not guaranteed by global inhibition alone") und das Berichtsurteil NICHT NACHGEWIESEN zur NA-1-Kategorialformulierung.
- **Kim et al. 2017 (Science):** Bestätigt lokaler Erregung und globale Inhibition im Fliegen-Ringattractor („local excitation and global inhibition between the compass neurons"). Relevanter Kontext — das biologische System nutzt summenartige breite Inhibition —, aber kein Beweis für irgendeinen Arm.
- **Vorsicht (Konsistenz mit Bericht):** Die Herabstufung einer unbelegten Behauptung wird nicht dadurch „von der Literatur bestätigt", dass diese den Vergleich nicht behandelt — diese Grenzziehung des Berichts wird übernommen.

### 4 · Urteile des Teilreviews — überwiegend bestätigt

| Prüfpunkt | Urteil Bericht | Diese Synthese |
|---|---|---|
| R1 §4 Modenverhältnis-Formel und Richtung | PASS | **Bestätigt** (numerisch exakt) |
| R1 §4 Separationsrand fallend | PASS · Onset BEDINGT | **Bestätigt** |
| R1 §5 MAX/SUM auf REGISTERED_HYPOTHESIS | PASS | **Bestätigt** (konsistent mit Beweis- und Literaturlage) |
| NA-1 „Max-Term sichert Einzigkeit" | NICHT NACHGEWIESEN | **Bestätigt** (literaturgestützt) |
| Amari-Zeugen W1–W4 | BEDINGT | **Hier nicht re-verifiziert** (Parameter fehlen im Extrakt); Vorbehalt bleibt angemessen |
| R1 §3 D1-Freeze-Felder | PASS | Nicht vertieft; unverändert |
| R2 §4 Antipoden-Präzision | BEDINGT | Nicht Gegenstand; AXIOM-Adjudikation C1-2 bleibt maßgeblich |
| Homogenität beider Arme | BESTÄTIGT (ReLU, I_ext=0, ξ=0) | **Bestätigt** (~10⁻¹⁴); als generische Eigenschaft eingeordnet |
| MAX/SUM-Stabilitätsrangfolge | NICHT NACHGEWIESEN | **Bestätigt** |
| Vollständige Stabilitätsentscheidbarkeit | NICHT ENTSCHEIDBAR | **Bestätigt** |

### 5 · Verbleibende Lücken (aus Bericht §6, unverändert gültig)

1. Stabilitätskriterien-Übertragung: kontinuierlich (Realteile, neutraler Modus Eigenwert 0) vs. diskret (Beträge, Eigenwert 1).
2. Vollständige Nullstellenzählung für die Amari-Zeugen W1–W4 (nur Kandidaten reproduziert).
3. Präzisierung des Stabilitätsbegriffs (Breitenstabilität bei neutraler Translation vs. asymptotische Stabilität).
4. Herleitung von `g_eff` aus dem tatsächlichen MAX-/SUM-Modell.
5. tanh-Cap-/Sigmoid-Variante: getrennt zu behandeln (nicht positiv homogen).

---

## Quellennotizen

| Quelle | Glaubwürdigkeit | Letzte Aktualisierung |
|---|---|---|
| [Noorman et al. 2024, Nature Neuroscience](https://www.nature.com/articles/s41593-024-01766-5) | 5/5 | 2024-10-03 |
| [Kim et al. 2017, Science](https://www.science.org/doi/10.1126/science.aal4835) | 5/5 | 2017 |
| [Laing & Troy, Two-bump solutions of Amari-type models (Physica D)](https://www.sciencedirect.com/science/article/abs/pii/S0167278903000137) | 5/5 | 2003 |
| [Scholarpedia: Neural fields](http://www.scholarpedia.org/article/Neural_fields) | 4/5 | - |
| [Turner-Evans et al., The neuroanatomical ultrastructure and function of a biological ring attractor (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/) | 5/5 | 2020 |
| Projektupload NEXUSO~2.MD — R26-Teilreview (intern, Berichts-ID …_20261011_R1) | — | 2026-10-11 (Berichtsdatum) |
| Eigene deterministische Algebra-/Homogenitätsprüfung (intern, keine Netzwerksimulation) | — | Diese Sitzung |

**Konflikte und Vorbehalte:** Noorman-Gleichung (1) wurde nicht im Volltext geprüft (Lücke bleibt); Amari-Zeugen W1–W4 wurden hier nicht reproduziert (vollständige Parametersätze fehlen im Extrakt); die Laing-Troy-Originalarbeit war laut Bericht „nicht aufgelöst" — die hier zitierte Physica-D-Arbeit wurde nur über Suchauszüge gelesen.

---

## Offene Fragen

1. Existiert im konkret parametrisierten NA-1-MAX-Modell ein stabiler Ein-Peak-Zyklus? (NE-1 / MULTIPEAK_INJECTION bleibt der Prüfpfad.)
2. Bleibt die Skalierungsfreiheit unter ξ>0 und I_ext≠0 als langsame Amplituden-Drift erhalten — und geht sie als Fehlerquelle in EB1′ bzw. die Drift-Bound-Ableitung ein?
3. Lässt sich `g_eff` so spezifizieren, dass MAX- und SUM-Arm vergleichbare effektive Inhibition besitzen (identischer Gain vs. baseline-abgeglichen), ohne das Vergleichsdesign vorwegzunehmen?

---

## Empfehlungen / Nächste Schritte

1. **MISTRAL/VIBE/Operator:** Aktivierung fixieren — ReLU für den Homogenitätsarm, tanh-Cap als explizit getrennter Arm; Zeitschritt-Deklarat und Normierungswahl (identischer Gain vs. baseline-abgeglichen) dokumentieren.
2. **g_eff-Herleitung als minimale Vorarbeit:** Für MAX (Skalierung mit `M = max_j r_j`) und SUM (Skalierung mit `A = Σ_j r_j`) explizit hinschreiben; ohne sie bleibt jeder MAX/SUM-Vergleich unterbestimmt.
3. **NA-1-Spec:** Kategorialformulierung „Max-Term sichert Bump-Einzigkeit" als REGISTERED_HYPOTHESIS markieren (Harmonisierung mit R25-03, wie im Bericht Schritt 3 vorgesehen).
4. **Drift-Bound-Protokoll:** Prüfen, ob der Amplitudenfreiheitsgrad (Homogenitätsbefund) in EB1′-Fehlerbudgetsätzen erfasst ist; falls nicht, ergänzen.
5. **Kette:** Teilreview-Verdikt über den GitHub-API-Handshake an AXIOM übergeben; bis zur Adjudikation bleibt offener Punkt 2 der Kette als „teilweise adressiert" geführt. PR70 bleibt OPEN; PR65/PR67-HOLDs unangetastet; keine Experimente, keine HOLD-Anhebung, kein Production-Write.

---

*Prüfung bleibt das Fundament. Diese Synthese fügt dem Teilreview eine unabhängige Bestätigung der überprüfbaren Kerne hinzu und ergänzt die Einordnung des Homogenitätsbefunds als generische, nicht diskriminierende Eigenschaft — eine Herkunfts-Spur im Symbiose-Artefakt, keine Inhalts-Autorität.*