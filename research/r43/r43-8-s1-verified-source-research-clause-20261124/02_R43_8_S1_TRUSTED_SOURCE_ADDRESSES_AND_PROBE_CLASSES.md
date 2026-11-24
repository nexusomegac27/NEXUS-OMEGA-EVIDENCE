# VSRD-C1 · Verifizierte Recherche-Adressen und Zugangsmatrix (Recherche-Einstieg, keine allgemeine Wahrheitsgarantie)

**Normative Grundregel:** institutionelle/persistente Originaladresse priorisieren; danach tatsächlich gelesenen Inhalt und Originalbytes separat prüfen. Sichtbare Domain und DOI sind keine inhaltliche Verifikation. Forschung darf außerhalb des Registers neue wissenschaftliche Hypothesen und Quellen entdecken; neue Treffer werden solange Q0 geführt, bis ein rechtmäßiger Originalweg Q1+ erfüllt.

## Institutionelle Startpunkte und Primärfragen

| Institutioneller Ursprung | Adressmuster | Was die Quelle belegen kann | Was nicht ohne weitere Evidenz belegt ist |
|---|---|---|---|
| FDA OSEL | https://www.fda.gov/medical-devices/regulatory-science-tools-catalog/open-access-wearables-dataset-evaluate-factors-impacting-accuracy-smartphone-gait-metrics | amtlicher Katalog-Eintrag, wenn tatsächlich erreichbar | 370 unveränderte Originaldateien, Dual-OPPO-Validierung |
| FDA OSEL Source Repo | https://github.com/dbp-osel/wearables-for-gait-synchronized-smartphone-imu-and-walkway-data | README, Origin und commitgepinnten Synchronisationscode | Inhalt/Verfügbarkeit der vollständigen unveröffentlichten Daten |
| UCI MHEALTH | https://archive.ics.uci.edu/dataset/319/mhealth%2Bdataset | Dataset-Identität, Aufgaben, Data Rights | replizierte S1→S2 80/81 ohne echten Rehash |
| PhysioNet | https://physionet.org/ | echte registrierte Datensätze, Datenversions- und ggf. Zugangsmetadaten | automatisch Zugang zu einer angekündigten FDA-Reihe |
| DOI resolver | https://doi.org/ | persistent identifizierbaren Landing-Publisher | Fachdaten und vollständige PDF Originalmethodik |
| Crossref | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ und https://api.crossref.org/works/{doi} | DOI, Autoren, Veröffentlichungsstand, Korrekturen/Lizenzen soweit hinterlegt | inhaltliche Replikation, Artikel-PDF |
| DataCite | https://api.datacite.org/dois/{doi} | Data-Doi Ursprung/Version/Herausgeber sofern hinterlegt | Gewähr für Zugriffsrechte oder Datendatei-Korrektheit |
| NLM PubMed | https://pubmed.ncbi.nlm.nih.gov/ und https://pubmed.ncbi.nlm.nih.gov/download/ | bibliografische ID, DOI, Abstract/Retraction Links, E-Utilities | vollständige Rohmethoden und Patientendaten |
| PMC | https://pmc.ncbi.nlm.nih.gov/ | tatsächlich offene Volltexte und Lizenzen nach Artikel | Nutzungsrecht anderer zugehöriger Datenprodukte |
| Zenodo | https://zenodo.org/ | veröffentlichte Daten-/Code-Version und DOI | Rechte und Datenintegrität ohne tatsächlichen Lizenz/Dateiabgleich |
| GitHub Originale | https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files | commitgepinnte Datei, Git-Origin, Vergleich mit SHA256 | experimentelle Wahrheit, ohne die Originalmessung |

## R43-8 user-supplied Offchain-vantage test, 11 recorded GETs (NOT AXIOM live rerun)
- 5× HTTP200 with source-specific title, 1× HTTP200 generic UCI title, 1× HTTP200 without extracted PMC title.
- 3× HTTP203 Proxy cache / indirect generic PubMed: classify *indirect access*, NOT direct authoritative original content.
- 1× HTTP401 blocked FDA catalogue: classify *this observer's access gap*, NOT FDA source deletion or data invalidity.
- 1× FDA github original repository HTTP200 and `git ls-remote` HEAD `1bc52d3d3c23b5bf61dc912efb92dd9566a1fab8`: existence/identity, no underlying data rehash.
The received probe is a source-existence experiment, not scientific re-verification of the eleven underlying content claims. Never escalate Q1 to Q3/4 from a title match or HTTPS code alone.

**Discovery discipline:** locate candidate paper/data in legitimate search, journal index, DOI registry and independent bibliography; switch to original publisher or data host; record access problem and legal mirror instead of bypass. Any retraction/corrigendum, version drift, over-hyped clinical claim and source redundancy must be listed as contradiction or risk.
