# R45-3 Return — Eingangsintegrität und Rehash-Grenzen
## Bestätigt (GitHub-seitig)
- Alle 12 Paketdateien (#457-Ordner, 00_START_HERE ... 99_SHA256SUMS.txt, ZIP, Sidecar) am HEAD 8623bff1... gelesen.
- Git-Blob-Identitäten des Verzeichnislistings stimmen mit den Download-Bestätigungen je Datei überein; Sidecar-Text wortgleich b5cdac156cb0722a8451b7f1b8eed15c7c4c5e80f7bec9df5d1d498783c7030e.
- Inhaltliche Anker verifiziert: 02_ADJUDICATION.json (GLM 47/47, unabhängiger Return 11/11, Ledger 14/14 mit 8/14 Skriptidentität), 05_CONTROLS.json (24 Designs, STATE DESIGN_ONLY_FORMAL_NOT_RUN), 08_RECEIPT.json (Zeugen).
- Beide Rohbytes-Zeugen von 08 exakt reproduziert: sha256('{"a":1,"b":2}') = 43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777; sha256('{"b":2,"a":1}') = 3fb75453225c732a76b7899ea2096dda1455189c89817239732182f73fe5a09f; Sortier-Kanonisierung EQUAL.

## Nicht byte-genau rehashbar in dieser Umgebung (dokumentiert, erfahren in R45-2 und hier)
1. Die Konnektor-Textausgabe für GitHub-Dateien ist nicht bytegetreu (partielles JSON-Escaping der Downloadtexte; führendes '"' plus literale \n-Sequenzen statt sauberem Dekoding). Damit ist ein Rehash des ausgelieferten Textes gegen 99_SHA256SUMS.txt nicht aussagekräftig.
2. Das sha256sum-Werkzeug der Dateisystemumgebung ist defekt (JS-Fehler "reading 'digest'"); SHA-256 wurde stattdessen mit eigenem JS-Stack geführt.
3. ZIP binär nicht übertragbar/rehashbar (ZIP-NOT-REHASHABLE aus R45-2 gilt fort); MANIFEST_SHA256 1d6d41a7ae981afff0865d64fef8e2a9be59c5a68ad6d8fe53306bf47a279991 bleibt an das interne ZIP-Modul gebunden.

Formaler csrf... formaler Rehash bleibt gemäß 06_RETURN_CONTRACT Element der formalen Phase (Operator-Kustodie / internes ZIP-Modul).

**NEXUS Ω OMEGA**
