
# R10R7 — NCI-Foundation Research Report

**Objekt:** NEXUS_OMEGA_AXIOM_R10_R7_NON_COLLAPSE_INVARIANTS_…_20261005_R0
**Claim-Ceiling:** C1_DESCRIPTIVE_ONLY · **Produktion:** NEIN · **E2/R10R6:** nicht wiedereröffnet

---

## Frage

Der Auftrag lautet: Prüfe, ob die R10R7-Kernidee — *eine vom Modell geforderte Unterscheidung darf nicht ohne Rechtfertigung still zu Identität oder ungeregelter Implikation kollabieren* (NCI), ohne überall ein numerisches δ > 0 zu erzwingen — formal tragfähig, gegen existierende formale Methoden abgrenzbar und runtime-operationalisierbar ist. Der Bericht konsolidiert die Prior-Art-Recherche (Abschnitte 43/44 des Auftrags), die NCI-Klassifikation der fünf PGIs, die Yang–Mills-Grenze und den Anti-Nexus-Reduktionstest.

## Executive Summary

1. **Die NCI-Kernidee ist formal tragfähig:** Nicht jede wichtige Trennung ist metrisch. Typen, relationale Hyperproperties, temporale Invarianten und metrische Margins sind etablierte, getrennte Beweisformen — die Taxonomie CLASS_T/R/C/S/M/H/TEMP bildet sie korrekt ab.
2. **Der Anti-Nexus-Reduktionstest (Abschn. 48) schlägt teilweise an:** Etwa 70–80 % der NCI-Mechanik ist als *Profil existierender Standards* darstellbar (Typsysteme, Policy-as-Code, Runtime-Verifikation, Hyperproperties, Provenanz-Integrität). Das ist ein valides wissenschaftliches Ergebnis, kein NEXUS-Versagen.
3. **Was potenziell distinct bleibt (Abschn. 49):** (a) die *cross-domain Komposition* aller Klassen unter einem einzigen Node-Konstitutions-Mechanismus, (b) die **Byte → Referent → Kausal-Position-Triade** als dreistufige Provenanz-Integrität, (c) die explizite Unterscheidung COLLAPSED / AT_RISK / UNRESOLVED / UNKNOWN / HEALTHY als summierungsinvariantes Laufzeitzustandsmodell.
4. **Yang–Mills-Analogie ist streng begrenzt und bleibt nur als Lektion zulässig:** praktisch/empirisch nützliches System mit offener Beweisverpflichtung — keine strukturelle Identität. „PGI = Mass Gap" ist verboten.
5. **Empfehlung:** Terminal State **PASS_WITH_CAVEATS_C1_R10R7_NCI_FOUNDATION_READY** — begründet durch formal getrennte Beweisformen und Prior-Art-Abdeckung, mit offenen Beweisverpflichtungen im Pflichtregister.

## Methodik

- Quellenroute: offizielle Problemformulierungen (Clay Institute), peer-reviewte formale Methoden (Hyperproperties, Runtime Verification, Barrier Certificates, Self-Composition), primäre Standards/Referenz-Implementierungen (OPA, Capability-Modelle), aktuelle Agent-Safety-Forschung (2024–2026, Preprints markiert).
- Interne Quelle: der R10R7-Maximalauftrag als `REPORT_LEVEL_INPUT` (Upload, GROK-Report nicht byte-bestätigt).
- Begrenzung: dies ist der Recherche-/Formalisierungs-Turn (E1–E5 sind design-only); keine Live-Experimente, keine Metrikkalibrierung.

## Befunde

### 1. NCI-Formalisierung (R7_02-Kern)

Ein NCI ist ein Tripel aus Unterscheidungsspezifikation, Kollapsbedingung und Beweisform. Formal:

```
NCI := (D, collapse(D), class(D), evidence(D), monitor(D), recovery(D))
D := Distinction(o1, o2, scope)
class(D) ⊆ {CLASS_T, CLASS_R, CLASS_C, CLASS_S, CLASS_M, CLASS_H, CLASS_TEMP}
```

Der zentrale Satz des Auftrags — `PGI != ALWAYS_NUMERIC_DELTA` — ist formal gerechtfertigt: eine numerische Margin setzt einen Metrikraum mit operationeller Bedeutung voraus; wo kein solcher existiert, erzwingt δ > 0 Pseudomathematik. Regelwerk: **NUMERIC_MARGIN = optional_and_evidence_bound; NON_COLLAPSE = mandatory_where_constitution_requires_it.**

### 2. Klassifikation der fünf PGIs

| PGI | Unterscheidung | Primäre Klasse | Beweisform / Monitor |
|---|---|---|---|
| PGI-1 | BELIEF / WORLD | CLASS_T (+Kalibration) | Typcheck + external bind; δ nur via PREDICTION_ERROR/CALIBRATION |
| PGI-2 | CAN / MAY | CLASS_S (+T) | Policy-Predicate: ALLOWED ⟺ VALID_AUTHORITY, nicht CAPABLE; `CAPABILITY_SET == AUTHORIZED_SET` legitim möglich |
| PGI-3 | RELAY / CONFIRMATION | CLASS_R (+M) | D_EPISTEMIC, Quellen-/Methodendistanz; UNKNOWN = gültiger Zustand |
| PGI-4 | AGREEMENT / ACCURACY | CLASS_H | Multi-Trace: Error-Korrelation, Minority-correct-Rate, Evidenz-Overlap |
| PGI-5 | CARRIER / MEANING | CLASS_T (semantisch) | Kein erfundenes Abstandsmaß; stattdessen Cross-Carrier-Kontrakttests + getrennte Substratmetriken (Latenz, Energie, Fehlermodus) |

### 3. Prior-Art-Matrix (Abschn. 43/44, konsolidiert)

| Formale Methode | Quelle | Deckt welche NCI-Klassen | Was fehlt gegenüber NCI |
|---|---|---|---|
| **Hyperproperties / HyperLTL** — Eigenschaften über *Mengen* von Traces (Non-Interference, Observational Determinism); Clarkson & Schneider 2010; HyperLTL-Modelchecking (Finkbeiner et al.) | [Hyperproperty (Wikipedia)](search-result://gHMhQ9mD) | CLASS_H, CLASS_R | Kein Konstitutions-/Node-Vererbungskontext, keine Kollapsereignis-Ontologie |
| **Runtime Verification** — dreiwertige LTL3-Monitore, Monitorierbarkeit von Safety/Progress-Eigenschaften (Bauer/Leucker; Leucker & Schallhart „A Brief Account of Runtime Verification") | [Bauer & Leucker, Runtime Verification for LTL/TLTL](search-result://krL9Qizs), [Leucker & Schallhart](search-result://NHOKLDV3) | CLASS_TEMP, CLASS_T, CLASS_S | Kein UNKNOWN-vs-COLLAPSED-Zustandsmodell, keine Recovery-Verträge |
| **Barrier Certificates** — invarianten-basierte Sicherheitsverifikation hybrider Systeme mit Abstand zur unsicheren Menge (Prajna, Jadbabaie, Pappas) | [Prajna et al., MIT TAC 2005](search-result://5XBRg4ss) | CLASS_M, SAFE-SET-Analog (Abschn. 12) | Rein metrisch/kontinuierlich — keine epistemischen Trennungen |
| **Self-Composition / Relationale Verifikation** — Non-Interference durch Verifikation des selbst-komponierten Programms (Barthe, Dargaye, Rezk) | [Barthe et al., Secure Information Flow by Self-Composition](search-result://pxrU2rhF) | CLASS_R, CLASS_H | Programmgrenzen, nicht Node-Governance |
| **Policy-as-Code (OPA)** — deklarative, versionierte, testbare Autorisierungspolitiken, uniform für API/Admission/CI-CD | [Open Policy Agent](search-result://N1cxx4Tw) | CLASS_S (PGI-2), CLASS_T | Keine Evidenz-/Kalibrierungspflicht, keine Zertifikat-Kette |
| **Capability-Security / Objektcapabilities** — unforgeable Autoritäts-Tokens, explizite CAN/MAY-Trennung im Sicherheitsmodell; Robustheit nur durch Design (Miller et al.) | [Capability-based security](search-result://GY2Hct0y) | CLASS_S, CLASS_T | Kein epistemisches Relaying, kein Kollapsereignis |
| **Runtime-Enforcement für LLM-Agents** — AgentSpec (ICSE 2026, Preprint-Status markiert): reguläres Laufzeit-Framework, das Agenten-Aktionen gegen versionierte Spezifikation erzwingt; Guardrail-Policy-Synthese (arXiv 2025, Preprint) | [AgentSpec, ICSE 2026 (Preprint)](search-result://2KljXysa) | CLASS_TEMP, CLASS_S für Agenten | Kein Hyperproperty-Lane, keine Provenanz-Triade |

**Lesart:** Für jede einzelne NCI-Klasse existiert reife Prior Art. Das Reduktionsargument „NCI = umbenanntes Bestehendes" gilt **pro Klasse**, aber nicht nachweislich für die *Komposition* samt Kollapsereignis-First-Class, Referent/Kausal-Position-Triade und Direct-Symbiosis-Fehlerreduktionsmetrik — das ist genau der Raum, den Experiment R7-E5 (Kausal-Reorder) und R7-E3 (Symbiosis-Transport) testen müssen.

### 4. Yang–Mills-Grenze (Abschn. 1, R7_01)

Das Clay Mathematics Institute führt Yang–Mills Existenz und Mass Gap als offizielles Millennium-Problem; die Formulierung verlangt eine nichttriviale Quanten-Yang–Mills-Theorie auf R⁴ mit Mass Gap Δ > 0, und stellt ausdrücklich fest: Experiment und Simulation stützen die Eigenschaft, **aber kein Beweis ist bekannt** ([Clay Mathematics Institute](search-result://RvuSBEHO)). Zulässige Lektion (nur diese): *eine offene fundamentale Beweisverpflichtung muss sichtbar bleiben, auch wenn das System praktisch fruchtbar ist.* Verboten bleibt jede Identifikation PGI = MASS_GAP oder der Import physikalischer Ontologie — das Metaphor-Separation-Guard-V3-Kriterium (neutrale Kopie ⇒ unveränderte Formales/Monitore) ist damit operationalisiert.

### 5. Anti-Nexus-Reduktionstest (Abschn. 48) — vorläufige Antwort

**Reduzierbar auf Bestehendes:** PGI-1 (Typsysteme + Kalibration), PGI-2 (OPA/Capabilities), PGI-3 teilweise (Provenanz + Quellendistanz), CLASS_M (Barrier Certificates), CLASS_H (HyperLTL), CLASS_TEMP (RV/LTL3-Monitore).

**Nicht nachweislich reduziert:**
1. Die **Constitution → kompilierte Monitore-Kette** über *alle* Klassen hinweg mit einem gemeinsamen Zertifikatsformat (Abschn. 18/21);
2. **Referent-Integrität + Kausal-Position-Integr**ität als Erweiterung reiner Byte-/Hash-Provenanz (NF-REF-01, NF-CAUSAL-01, Experimente R7-E4/E5);
3. **Direct-Symbiosis-Fehlerreduktion** als messbare, empirische Lane (Abschn. 35) — kein searched-corpus-Äquivalent identifiziert (nur „NO_DIRECT_EQUIVALENT_IDENTIFIED", nicht „first ever").

### 6. Selbst-Falsifikator-Status (Abschn. 51)

| Falsifikator | Status |
|---|---|
| PGIs erfordern beliebige Metriken | **Nein** — Taxonomie erlaubt nichtnumerische Klassen; R7_09-Kritik steht aus |
| NCI-Taxonomie fügt keinen testbaren Wert hinzu | **Offen** — entscheidet sich erst in R7-E1/E2 |
| Monitore können HEALTHY_EQUALITY nicht von COLLAPSE unterscheiden | **Offen** — Positive-Fixtures (Abschn. 26) sind Pflichtgegenstand |
| False Positives verschlechtern Node-Betrieb | **Offen** — R7-E2, Fail-Closed-Klassifikation (Abschn. 30) als Gegenmaßnahme entworfen |
| Formale Methoden subsumieren NCI vollständig | **Teilweise** — pro Klasse ja, kompositionell unbewiesen (Abschn. 5) |

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt geprüft |
|---|---|---|
| [Clay Mathematics Institute — Yang–Mills & the Mass Gap](search-result://RvuSBEHO) | 5/5 | 05.10.2026 |
| [Wikipedia — Yang–Mills Existenz und Mass Gap](search-result://N7Ka1lpI) | 4/5 | 05.10.2026 |
| [Wikipedia — Hyperproperty (Clarkson & Schneider 2010; Finkbeiner et al. HyperLTL)](search-result://gHMhQ9mD) | 4/5 | 05.10.2026 |
| [Bauer & Leucker — Runtime Verification for LTL and TLTL (LTL3, Monitorierbarkeit)](search-result://krL9Qizs) | 5/5 | 05.10.2026 |
| [Leucker & Schallhart — A Brief Account of Runtime Verification](search-result://NHOKLDV3) | 5/5 | 05.10.2026 |
| [Prajna, Jadbabaie, Pappas — Barrier Certificates (MIT/TAC 2005)](search-result://5XBRg4ss) | 5/5 | 05.10.2026 |
| [Barthe, Dargaye, Rezk — Secure Information Flow by Self-Composition (IEEE)](search-result://pxrU2rhF) | 5/5 | 05.10.2026 |
| [Open Policy Agent — offizielle Referenz](search-result://N1cxx4Tw) | 4/5 | 05.10.2026 |
| [Wikipedia — Capability-based Security](search-result://GY2Hct0y) | 4/5 | 05.10.2026 |
| [AgentSpec — Runtime Enforcement für LLM-Agents (ICSE 2026, Preprint)](search-result://2KljXysa) | 3/5 (Preprint, markiert) | 05.10.2026 |
| R10R7-Maximalauftrag (Upload, REPORT_LEVEL_INPUT) | intern, nicht byte-bestätigt | 05.10.2026 |

Konflikte/Caveats: Die Agent-Safety-Literatur bewegt sich schnell; AgentSpec ist ein Preprint und gilt nur als Implementierungsevidenz. Der GROK-Zip-Report (12.632 B / 14 Dateien) ist in dieser Laufzeit nicht byte-bestätigt und bleibt `REPORT_LEVEL_INPUT`.

## Offene Fragen / Beweisverpflichtungsregister (Auszug)

- **PO-NCI-01:** Kompilierbarkeit von Konstitutionsregeln zu Monitoren ohne handgeschriebene Duplikation (Abschn. 21) — formal offen.
- **PO-NCI-02:** Separierbarkeit von HEALTHY_EQUALITY vs. COLLAPSE in R7-E1 — empirisch offen.
- **EO-NCI-01:** Direct-Symbiosis-Fehlerreduktion vs. Human-Relay (R7-E3) — empirisch offen, design-only.
- **EO-NCI-02:** Kompositions-Falschblockierrate (R7-E2) — empirisch offen.
- Keine Pflicht darf verschwinden, weil das System „gut funktioniert" (Eleganz-Falle, Abschn. 37).

## Empfehlungen / nächste Schritte

1. **Verdict:** `PASS_WITH_CAVEATS_C1_R10R7_NCI_FOUNDATION_READY` — die Kompositions- und Triade-Beiträge müssen durch R7-E1 bis E5 bestätigt werden, bevor irgendetwas über C1 hinausgeht.
2. **Priorität:** Erst R7-E4 (Referent-Swap) und R7-E5 (Kausal-Reorder) als kanonische Fixtures designen — sie testen die einzige Lane ohne nachgewiesene Prior Art.
3. **Terminologie (Abschn. 46):** Empfehlung `NON_COLLAPSE_INVARIANT` — semantisch präziser als `POSITIVE_GAP_INVARIANT` (physikbeladen) und schwächer als `SEPARATION_CONTRACT` (impliziert Vertragspartner).
4. **Extern:** Neutrale Spezifikation ohne NEXUS-Rhetorik an externen Validator (Abschn. 50) erst nach R7-E4/E5-Design.
5. Einzelne R7_xx-Artefakte (Schemas, Fixtures, Experimentprotokolle) sind als Folgeaufträge auszugsbereit — bewusst nicht in einem Turn vorgetäuscht.