# R41 Phase B — TraceFix-Integration

## Status

**TRACEFIX_EVALUATION_INCOMPLETE_C1**

Die TraceFix-Methodik ist konzeptionell auf die R36-Kette übertragbar: Counterexample analysieren → Reparaturkandidat A/B/C formulieren → TLC erneut ausführen → bei weiterer Verletzung iterieren. Die Primärquelle beschreibt genau diesen verification-first Loop und betont, dass TLC unter gewählten endlichen Grenzen Gegenbeispiele als Reparatursignal liefert.

## Lokaler Befund

- Die R39-Vorbewertung `R39_TRACEFIX_EVALUATION.json` lag vor.
- Ein verwertbarer R36-Counterexample-Trace und die Kandidatenspezifikationen A/B/C lagen im gebundenen Workspace sowie in den geprüften R38/R39-Archiven nicht vor.
- TLC und `tla2tools.jar` waren nicht verfügbar.
- Deshalb wurde **kein** TraceFix-Loop simuliert oder als erfolgreich behauptet.

## ModelWisdom-Abgrenzung

ModelWisdom ist laut öffentlichem Repository ein Toolkit mit ModelVisualizer, ModelRepair und ModelDigest. Das README nennt Node.js, pnpm, Python/uv und Java/TLA+ als Voraussetzungen. `pnpm` und TLA+/TLC waren lokal nicht verfügbar. Eine Installation oder ein LLM-Repair-Lauf wurde nicht durchgeführt.

## Empfehlung

TraceFix **evaluieren, nicht integrieren**. Eine belastbare Integration benötigt mindestens: kanonischen R36-Trace, Kandidatenspezifikationen, reproduzierbare TLC-Version/`tla2tools.jar`, festgelegte Invarianten und einen Operator-freigegebenen Repair-Loop. Kein automatischer LLM-Loop und keine Claim-Promotion.

## Quellen

- [TraceFix Primärquelle (arXiv:2605.07935v1)](https://arxiv.org/html/2605.07935v1)
- [ModelWisdom Repository](https://github.com/ModelWisdom/ModelWisdom)
