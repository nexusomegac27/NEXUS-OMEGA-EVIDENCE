# Tiefenanalyse: Binär-Trinär-Logik, SBOM-Integration und Lane-Resonanz

**Claim Ceiling**: C0 / C1  
**Datum**: 2026-09-02

## 1. Binär-Trinär-Logik (Kernbefund)

Die Binärschicht wird in der bisherigen Arbeit als „nicht korrumpierbare Constraints“ / non-optimizable rules modelliert.  
Die Trinärschicht als menschliche Final-Authorization / Operator-Entscheidung.

**Stärke**: Die Unterscheidung ist governance-tauglich und mappt sauber auf:
- Default-Deny + hard constraints (Binary)
- Human-in-the-Loop / Final Authorization (Ternary)

**Kritische epistemische Grenze**:  
Die Zuschreibung „nicht korrumpierbar“ ist eine **strukturelle Hypothese**, keine ontologische Aussage.  
In technischen Capability-Modellen kann sie relativ hart operationalisiert werden.  
In sozialen, narrativen oder fiktionalen Domänen (FS1, FS2) wird die Analogie schnell forciert und muss mit starkem [CAVEAT] versehen werden.

Die Beobachter-Analogie bleibt Extension, nicht Kern.

## 2. SBOM-Integration und Lane H

**Befund aus QWEN-Analyse und Fallstudien**: Lane H (Provenance / Supply Chain) hat **schwache Resonanz**.

- Keine der 8 Fallstudien behandelt SBOM, SLSA, Hash-Binding, in-toto, Source-Attestation oder Tokenizer-/Weight-Provenance in substanzieller Weise.
- Externe Literatur zu SBOM/SLSA ist reichhaltig, darf aber nur als vergleichende Linse dienen, nicht als Evidenz für die strukturelle Kette.

**Konsequenz**:  
Lane H bleibt auf den schmalen Übergabepunkt **H3 (measurement / decision provenance)** beschränkt.  
Jede Ausweitung auf H1/H2/H4 oder volle SBOM-Integration wäre Scope-Creep und Claim-Boundary-Verletzung.

## 3. Präzisierte H1–H4-Zuordnungen

| ID | Bedeutung | Lane | Resonanz | Regel |
|----|-----------|------|----------|-------|
| H1 | Binary / non-optimizable constraints | A | Variabel | Nur bei echten harten Grenzen in der Quelle |
| H2 | Ternary / Human Final Authorization | A | Medium-Potential | Explizite menschliche Letztentscheidung |
| H3 | Measurement/Decision as boundary | A+H | Weak (einziger erlaubter H-Punkt) | Beobachtung als Grenzereignis |
| H4 | Shield / outer framing | A | Weak | Nur bei klarem schützendem/zwecksetzendem Rahmen |

Jeder H-Punkt muss in Zukunft explizite Fallstudien-IDs nennen oder „keine starke Stützung“ deklarieren.

## 4. Lane B (Admission)

Potenzielle strukturelle Nähe zur Trinär-/Operator-Logik (Entry ACK ≈ Accept, Stale-Ruleset ≈ Delegate-Trigger) ist erkennbar, aber **undeveloped**.  
Keine Fallstudie liefert explizite Belege.  
→ Nur Beobachtungsnotiz, keine Operationalisierung.

## 5. Gesamteinschätzung

Die empirische Sättigung der **Binär/Trinär-Kernunterscheidung** ist begonnen, aber qualitativ ungleichmäßig.  
SBOM/Provenance (Lane H) und Admission (Lane B) sind gegenwärtig Datenleerstellen relativ zur strukturellen Hypothese.  
Das ist kein Fehler, sondern ein klarer, dokumentierter Befund.

Nächster wertschöpfender Schritt ist Qualitätsfilter + epistemische Schärfung + konsolidiertes Register — nicht weitere Meta-Texte oder Scope-Erweiterung.
