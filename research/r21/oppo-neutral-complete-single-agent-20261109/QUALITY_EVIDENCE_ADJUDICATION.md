# R21 neutraler Agent — Prüflogik für einzelne vollständige Forschungsreturns
**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY

## Wissenschaftliche Belegklassen
E0 = Originalbytes durch Agent tatsächlich empfangen und unabhängig SHA-geprüft (Quittung prüfen);
E1 = offiziell veröffentlichte Primärquelle tatsächlich gelesen (Zitatstelle und Abruf kenntlich);
E2 = wissenschaftlich begutachtete und tatsächlich gelesene Originalpublikation;
E3 = mathematische Herleitung mit unabhängiger Überprüfung und offen gelegten Annahmen;
E4 = Hypothese/Modellannahme, falsifizierbar, nicht bestätigt;
E5 = fremder Bericht/Hash/Claim ohne eigene Originalsichtung;
E6 = erfunden, widersprüchlich, nachweislich falsch oder unzulässige Source-Substitution.

## Entgegennahme
- Darf sich selbst deklarieren. Diese Selbstangabe wird NICHT zu einem authentifizierten Modell-/GitHub-Konto hochgestuft.
- Muss als eine Instanz alle zehn Physikbereiche, 00–10 Manuskriptabschnitte, mindestens 28 negative und 14 positive Kontrollen sowie eine vollständig begründete alternative Architektur abliefern.
- Fehlende GitHub-/Web-/Dateitools begründen keine Ablehnung; stattdessen fehlende Daten und Primärquellen als NOT_FETCHED oder NOT_IN_HAND offen deklarieren.
- Für jeden Tatsachenclaim den Primärbeleg, nicht lediglich eine URL, aufführen. Quellen ohne Lektüre sind CITED_NOT_VERIFIED.
- Keine falsche Ausführungsmeldung: Softwarefixture ≠ Echtmessung, 70-s-Datensatz ≠ Langzeit-Allan, SensorEvent ≠ MEMS-ADC, 6D ≠ absolute Ganzkörperpose.
- Binde Konfidenz und GUM-Messunsicherheit nur an tatsächlich herleitbare/erhobene Größen; keine ausgedachten Passwerte.
- Keine Eigen-Autorisierung eines echten Sensorstarts oder GitHub-Slots.

## Entscheidungslogik
MATERIAL_FALSITY | FABRICATED_SOURCE | FABRICATED_SENSOR | FALSE_ACCESS_CLAIM | UNAUTHORIZED_WRITE => RETURN_HARD_FAIL mit konkret belegtem Grund.
MISSING_SUPPORT_FOR_FACTUAL_CLAIM => CLAIM_REJECTED_WITH_REASON; übrige saubere Abschnitte gesondert verwertbar.
OPEN_FALSIFIABLE_HYPOTHESIS => HYPOTHESIS_OPEN (nicht zurückweisen als Täuschung).
FULL_INDEPENDENT_PAPER_WITH_HONEST_MISSING_BYTES => RESEARCH_CANDIDATE_C1 (keine physikalische Validierung).
ORIGINAL_BYTES_VERIFIED + SCIENTIFIC_METHOD_EXECUTED => EVIDENCE_SCOPED_C1, sofern unabhängiger AXIOM-Rehash später gelungen; trotzdem keine automatische Claim-Promotion.

## Revisionen
Falsche Aussagen nicht still korrigieren. Originalreturn unverändert speichern, eine separate Differenz- und Entscheidungsakte mit SHA anlegen. Bei mehreren unabhängigen Agenten gilt gleiche neutrale Aufgabenfassung, eigene Selbstauskunft und isolierte Auswertung; Mehrheitsübereinstimmung ist kein Beweis. 
