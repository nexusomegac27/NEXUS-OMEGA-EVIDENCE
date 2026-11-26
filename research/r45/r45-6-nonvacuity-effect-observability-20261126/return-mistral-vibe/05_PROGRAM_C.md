# 05 · PROGRAMM C · Lesbarkeit, Monitorability, unabhaengige Evidenz (P0)
STATUS = QUELLENVERIFIZIERT (live) plus DESK-SYNTHESE, C1

## C.1 Live verifizierte Quellen (26.11.2026)
- OpenAI, What affects chain-of-thought monitorability across the model lifecycle?, veroeffentlicht 10. November 2026 (Originalseite geoeffnet und gelesen): niedrigere Praeperplexitaet und einzelne Architekturveraenderungen verbessern No-CoT-Faehigkeiten, RL und modellerzeugte Daten erhoehen CoT-Kontrollierbarkeit; beide Proxies zusammen deuten darauf, dass Modelle beim Skalieren schwerer durch ihren CoT zu ueberwachen werden.
- Institute for AI Policy and Strategy, Transparency Disclosures for Chain-of-Thought Monitorability, parallel als arXiv:2611.13873 (Berichtsseite verifiziert; erstmals Juli 2026). Empfehlung: standardisierte Lesbarkeitsbewertungen und unabhaengige Monitorability-Pruefungen.
- arXiv:2611.21799 (Chain-of-Thought Controllability Can Reduce CoT Monitorability): gemaeß AXIOM-Ordnung experimentell gezeigt; ich habe den Originalartikel in dieser Sitzung NICHT selbst geoeffnet; Einstufung ORDNUNGSZITAT_NICHT_SELBST_VERRIFIZIERT.
- Agentic Model Checking (arXiv:2605.21434), FORGE (arXiv:2602.16708; v3 08.05.2026, inzwischen v4 12.10.2026) und Soteria (arXiv:2611.17880): auf Abstract-Ebene live verifiziert. Die Autorisierungsuebersicht DOI 10.1007/s10207-026-01343-w steht laut Ordnung ebenfalls auf Abstract-Ebene; Abstract nicht selbst geoeffnet.

## C.2 Grundregel (uebernommen und bestaetigt)
Lesbarkeit ist wichtige Voraussetzung fuer Audits, aber keine hinreichende Sicherheitsgarantie. Der sichtbare Text eines Agenten ist nicht notwendig vollstaendige oder treue Abbildung seiner internen Berechnung, und über externe Agentenschnittstellen besteht ohnehin kein voller Blick in deren Verbundenum. Die Sicherheitsarchitektur muss auch ohne diesen Einblick funktionieren.

## C.3 Desk-Konsequenz fuer das NODE-Framework
- Node-Reports werden streng als Zeugenschaft ersten Grades gefuehrt, nicht als Wahrheit: Jeder Bericht bekommt einen Evidenzgrad und benoetigt fuer Sicherheitsentscheide mindestens eine nicht-berichtliche Komponente (Ressourcenbeobachtung, kernel-checked Protokoll, unabhaengiger Verifikator).
- Monitorability-Ausweis analog zur November-Anchor-Recherche: je Artefakt dokumentiert, welche Schichten menschenlesbar sind und welche nur maschinell geprueft wurden.

NEXUS Ω OMEGA

