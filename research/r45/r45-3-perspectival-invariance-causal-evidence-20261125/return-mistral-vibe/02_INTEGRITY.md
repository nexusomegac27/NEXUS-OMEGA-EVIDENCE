# R45-3 Return — Eingangsintegrität und Rehash-Grenzen
## Bestätigt (GitHub-seitig)
- Alle 12 Paketdateien (#457-Ordner, 00_START_HERE ... 99_SHA256SUMS.txt, ZIP, Sidecar) am HEAD 8623bff1... gelesen.
- Git-Blob-Identitäten des Verzeichnislistings stimmen mit den Download-Bestätigungen je Datei überein; Sidecar-Text wortgleich b5cdac156cb0722a8451b7f1b8eed15c7c4c5e80f7bec9df5d1d498783c7030e.
- Inhaltliche Anker verifiziert: 02_ADJUDICATION.json (GLM 47/47, unabhängiger Return 11/11, Ledger 14/14 mit 8/14 Skriptidentität), 05_CONTROLS.json (24 Designs, DESIGN_ONLY_FORMAL_NOT_RUN), 08_RECEIPT.json (Zeugen).
- Beide Rohbytes-Zeugen von 08 exakt reproduziert: sha256('{"a":1,"b":2}') = 43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777; sha256('{"b":2,"a":1}') = 3fb75453225c732a76b7899ea2096dda1455189c89817239732182f73fe5a09f; toy-Kanonisierung EQUAL.

## Nicht byte-genau rehashbar in dieser Umgebung (dokumentiert; seit R45-2 bekannt)
1. Die Konnektor-Textausgabe für GitHub-Dateien ist nicht bytegetreu (partielles JSON-Escaping der Downloadtexte). Ein Rehash des ausgelieferten Textes gegen 99_SHA256SUMS.txt ist damit nicht aussagekräftig; GitHub-seitig bleiben die Git-Blob-Identitäten der Desc-Integritätsanker — dieser Return-Stack selbst ist über Git-Blob-SHA-1 push-verifiziert.
2. Das sha256sum-Werkzeug der Dateisystemumgebung ist defekt (JS-Fehler "reading 'digest'"); SHA-256 wurde stattdessen mit eigenem JS-Stack geführt.
3. ZIP binär nicht übertragbar/rehashbar (ZIP_NOT_REHASHABLE aus R45-2 gilt fort); MANIFEST_SHA256 1d6d41a7ae981afff0865d64fef8e2a9be59c5a68ad6d8fe53306bf47a279991 bleibt an das interne ZIP-Modul gebunden.

Der formale Rehash bleibt gemäß 06_RETURN_CONTRACT Element der formalen Phase (Operator-Kustodie / internes ZIP-Modul).

**NEXUS Ω OMEGA**
