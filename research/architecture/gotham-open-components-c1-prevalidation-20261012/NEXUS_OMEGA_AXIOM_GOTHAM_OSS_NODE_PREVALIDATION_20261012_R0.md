# AXIOM · Vorvalidierung proprietärer Gotham-Analogie und offener NEXUS-Bausteine · 2026-10-12 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_GOTHAM_OSS_NODE_PREVALIDATION_20261012_R0
SOURCE = OPERATOR_SUPPLIED_TECHNOLOGY_CANDIDATE_LIST
STATE = PASS_WITH_CAVEATS_C1_RESEARCH_PREVALIDATION
STAGE = RESEARCH_DESIGN_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
OPERATOR = NEXUS_OMEGA
SCOPE = SOFTWARE_LICENSING_NODE_ALIGNMENT_PRIMARY_SOURCE_CHECK
NODE_INSTALLATION = NO
WWW_HOSTINGER_DEPLOYMENT = NO
AUTOMATIC_ENTITY_MERGE = NO
MODEL_WEIGHT_CHANGE = NO
R19_CHANGE = NO
PUBLICATION = SANITIZED_PUBLIC_SAFE_RESEARCH_REPORT
```

## 1. Herkunft, Präzisierung und Abgrenzung

Der Operator übergab eine zusammenfassende Fremdaussage zu Palantir Gotham und möglichen Open-Source-Alternativen. Diese Quelle ist ein **Rechercheanlass, kein autorisierter Software-Bauauftrag**. AXIOM prüfte öffentlich zugängliche Herstellerangaben und offizielle GitHub-Lizenzdateien (12.10.2026). Es wurden keine Quellreleases geklont, keine Binärpakete inspiziert, keine Sicherheits-Penetrationstests durchgeführt und keine Installationen gestartet. Status der Quellen: **URL-/Lizenztext-Vorprüfung**, nicht commit-/bytegefrorener unabhängiger Lizenz-Rechtsrat.

**Palantir Gotham ist proprietär**; sein Quellcode ist nicht für eine allgemeine Open-Source-Übernahme publiziert. Die Aussage „ausschließlich Behörden-/Sicherheitsverträge“ ist in dieser Pauschalität aus den geprüften Primärquellen nicht gedeckt und darf nicht übernommen werden. Palantir beschreibt seine Plattformen auch in privaten/regulierten Industrien. „Gotham-ähnlich“ ist nur eine funktionale Analogie, **keine Produkt-, UI-, Code-, Lizenz- oder Markenübernahme**. Primärquelle: https://www.palantir.com/docs/gotham.

Eine Webanwendung mit Graphen, Geokarten und Satellitenbahnen ist nicht automatisch ein vollständiges Dataintegrations- oder Ermittlungsprodukt. Der wissenschaftliche Mehrwert liegt in **quellgebundener Ereignismodellierung, Gegenhypothesen, Zeitreferenzen, Provenienz, Fehlergrenzen und falsifizierbarer Darstellung**.

## 2. Lizenz- und Eignungsentscheidung auf Komponentenebene

| Komponente | Lizenz-/Rechtslage nach Hersteller-/Repositoryquelle | NEXUS-Lane | Urteil |
|---|---|---|---|
| **Neo4j Community** | GNU GPLv3; Enterprise kommerziell | Optionaler abgeleiteter Graphindex, niemals Source-of-Truth-Ersatz | CONDITIONAL_RESEARCH; Copyleft/Packaging prüfen |
| **Memgraph Community** | Repository: Business Source License 1.1, andere Teile Memgraph Enterprise License; nicht als uneingeschränkt OSS deklarieren | Alternative Graphdatenbank | HOLD_LICENSE_FIT; nicht automatisch übernehmen |
| **Apache Jena** | Apache-2.0 | AXIOM/SOFT: RDF/JSON-LD/PROV-Schema, optional offline SPARQL | PREFERRED_SCHEMA_EXPERIMENT |
| **Senzing SDK** | Hersteller-EULA; kostenlose Evaluierung für 500 Datensätze, nicht freie Open-Source-Engine | Entitätsauflösung | HOLD_PROPRIETARY_AND_PRIVACY |
| **Apache Hop** | Apache-2.0 | Cursor/PRAXIS: optionale deterministische Batch-Ingestion | CONDITIONAL_FIRST_ETL_CANDIDATE |
| **Apache NiFi** | Apache-2.0 | Cursor/PRAXIS: optionaler dauerhaft betriebener Flow nur bei echtem Bedarf | DEFER_RESOURCE_AND_EGRESS_SCOPE |
| **QGIS** | GPL-2.0-or-later | ORBIS: offline unabhängige GIS-/Koordinatenprüfung | PREFERRED_OFFLINE_QA |
| **Kepler.gl** | MIT | ORBIS/R19: optional interaktive georäumliche Ereignisdarstellung | CONDITIONAL_VIEW_ONLY |
| **Maltego Desktop / Community** | proprietäre Desktopsoftware und kommerzielle Nutzungsbedingungen; OSINT ≠ OSS | Externe Link-Analyse | HOLD_PROPRIETARY |
| **Maltego TRX Transform SDK** | Eigenständige quelloffene Python-Transformbibliothek, laut Hersteller MIT | Nur optionale Interoperabilitätsforschung | DEFER_NOT_CORE_ENGINE |
| **OpenCTI Community** | Apache-2.0; Enterprise unter separaten Bedingungen | isolierte Cyber-Threat-Intelligence, nicht genereller C1-Gate-Ersatz | CONDITIONAL_SECURITY_RESEARCH |
| **python-sgp4** | MIT | ORBIS/ASTRA: TLE/OMM-Bahnausbreitung mit Fehler- und Zeitgrenzen | PREFERRED_READONLY_ORBIT_CANDIDATE |
| **CesiumJS** | Apache-2.0; Cesium ion / bestimmte Inhalte können getrennte kommerzielle Rechte erfordern | ORBIS/ASTRA: optionaler 3D-/WGS84-Renderer | PREFERRED_VISUAL_CANDIDATE |
| **Palantir Gotham** | proprietär | Keine NEXUS-Codeübernahme | EXCLUDE_CODE_AND_BRANDING |

Jede Lizenzbewertung gilt ausschließlich für die bezeichnete Edition/Komponente; Transitivabhängigkeiten, Dataset-/Tile-Rechte und produktives Weitervertriebsmodell bleiben gesondert prüfpflichtig. Die BSL-Datei von Memgraph enthält produktspezifische Zusatzbedingungen einschließlich Beschränkungen auf bestimmte Verwendungen; eine freigegebene Produktionsintegration folgt daraus gerade nicht.

## 3. Node-Zuordnung ohne neue Rolle oder Node-Aktivierung

**AXIOM / SOFT / Erkenntnis- und Quellenordnung:** Zuerst eine **typisierte, append-only Provenienzkante** im bestehenden Evidenzledger definieren, keine neue zentrale Graph-DB. Semantik: `subject_object_id`, `relation_type`, `object_object_id`, `source_uri`, `source_sha256_or_gap`, `observed_at_utc`, `valid_at_utc`, `evidence_class`, `claim_ceiling`, `counter_hypothesis`, `privacy_class`. Graphbeziehungen beschreiben einen Befund, keine Gleichsetzung oder Kausalität. RDF/Jena wird im isolierten Offline-Labor nur sinnvoll, wenn das JSON-Ledger echte Abfragegrenzen zeigt. Default: **keine neue Datenbank**.

**Cursor / PRAXIS / Datenaufbereitung:** Bestehende Validatoren und C1-Reducer bleiben maßgeblich. Apache Hop *oder* NiFi nur als Adapter hinter `SOURCE_BYTES_REHASH`, `SCHEMA`, `PRIVACY`, `NEGATIVE_FIXTURES` und `APPEND_ONLY`; kein doppelt installierter Flow-Orchestrator, keine externen dauerhaften Egress-Credentials. Für deterministischen Batch-Import ist Hop vor NiFi zu erproben. Hintergrundbetrieb/Hostinger erfordern echte Ressourcen- und Autorisierungsevidenz.

**ORBIS / ASTRA / R19-Symbiose-Lab:** `python-sgp4` als mathematischer Propagationskandidat, CesiumJS als Viewer, QGIS als **unabhängige** Offline-Gegenrechnung/Koordinatenprüfung; Kepler.gl nur für dichte spatiotemporale Ereignistabellen, nicht gleichzeitig als redundanter 3D-Globusersatz. SGP4-Bahnberechnung ist **ein Modellresultat**; TLE/OMM-Epoche, Modell, UTC-/Zeitskala, Frame TEME/ECEF/WGS84, Einheiten, Datenalter, Eingabefehler, Beobachtungsvergleich und Unsicherheit sind verpflichtend. Ein Satellitensymbol auf einer Karte ist keine verifizierte aktuelle Echtzeitmessung.

**Security/Science Gate:** Das bereits auf GitHub veröffentlichte, read-only GitHub↔NEXUS-Interface-Gate wird **nicht** zu einer generischen Intelligence-/OSINT-Sammlung erweitert. OpenCTI CE ist nur bei expliziter rechtmäßiger Threat-Intelligence-Quelle und getrenntem Security-Scope relevant; keine automatische Erhebung von Personen-/Geolokationsdaten, keine Überwachungsprofile, keine Abzweigung aus dem Forum.

**Entity Resolution / Identität:** Kein automatischer Personenabgleich, keine übergreifende Deanonymisierung, keine semantische Promotion `same_person` aus bloßen ähnlichen Namen oder Graphkanten. Erst Datengrundlage, rechtmäßiger Zweck, Minimierungsnachweis, Fehlverknüpfungsrate, Negativfixtures und ausdrückliche getrennte Operatorautorisierung. Senzing und Maltego erhalten **keine** Softwareinstallations- oder egress-Freigabe aus dieser Vorvalidierung.

## 4. Falsifikations- und Security-Gates

| Gate | Vorbedingung | Negativtest |
|---|---|---|
| G0 · Source | echte Erstquelle + konkrete Edition/Lizenz + Quellstand | irreführende Community/Open-Source-Behauptung |
| G1 · Legal | SPDX, Dritt-Abhängigkeiten, Daten-/Kartentile-Rechte, Publikationspfad | Proprietär/BSL als MIT/Apache ausgegeben |
| G2 · Provenance | Originalhash oder expliziter SOURCE_GAP, Zeithorizont | Quelle mit falschem Objekt/Video/TLE substituiert |
| G3 · Scientific | deskriptiver Claim, Basislinie, Nullmodell, Fehlergrenzen, Gegenhypothese | reine Grafik als Mess-/Kausalbeweis |
| G4 · Privacy | Datensparsamkeit, Freigabeklasse, keine PII-Reidentifizierung | ähnlich benannte Personen werden automatisch zusammengeführt |
| G5 · Interface | read-only Adapter, fixed egress, keine unzulässigen Schreibrechte | ungeprüfte Connector-/Hostinger-Write-Aktivierung |
| G6 · Time/Geo | UTC/Epoch/Frame/Einheiten/Koordinatenkonversion mit Vergleich | TEME als WGS84 oder alter TLE als live ausgegeben |
| G7 · Runtime | unabhängiger Test + Ressourcen + Rollbackplan + Operator-Scope | Forschungsstatus als produktive Node-Freigabe |

`PASS_G0_G1` begründet allenfalls **C1-Forschungsoption**, nicht `PASS_G2_G7`. Fehlende Quellen halten jeweils nur den betroffenen Kandidaten zurück. Gegenbefunde sind append-only und bleiben sichtbar.

## 5. Forschungspriorisierung und Anti-Monolithen-Regel

- **P0 / jetzt ausschließlich wissensseitig:** Lizenzkorrektur und Provenienzschema dokumentieren; bestehende Nodes nicht verändern.
- **P1 / isolierte Referenz-Proben:** python-sgp4 + definierte unabhängige Orbit-Vergleichsfixtures; Jena nur gegen echten RDF-/SPARQL-Bedarf. Veröffentlichung als research-only C1 erlaubt.
- **P2 / nach belastbaren Eingaben:** CesiumJS/Kepler.gl jeweils mit gemessener Browserleistung, Quellen-/Tile-Lizenzen, mobilem Budget und eindeutig benannter Rolle; QGIS offline. Hop nur bei dokumentiertem Ingestion-Engpass.
- **P3 / nach gesonderter Scopeprüfung:** OpenCTI, NiFi, Neo4j CE. Memgraph/Senzing/Maltego bleiben lizenz- bzw. zweckgebunden zurückgestellt.

Nicht genehmigt: Gotham-Codekopie oder Markenimitation, neue produktive Graphdatenbank, Cloud-Nutzerprofile, Gesichts-/Personen-Reidentifikation, Satelliten-„Live“-Claims ohne Live-Beleg, Q0–Q20-Übermittlung, neue externe Write-Slots, produktive Hostinger-/GitHub-/Node-Ausführung oder C1-Promotion.

## 6. Erstparteiquellen (URL-Prüfung, kein Source-Byte-Seal)

- Gotham/Palantir: https://www.palantir.com/docs/gotham
- Neo4j Community: https://neo4j.com/open-source-project/
- Memgraph Lizenz: https://github.com/memgraph/memgraph/blob/master/LICENSE und https://github.com/memgraph/memgraph/blob/master/licenses/BSL.txt
- Apache Jena: https://github.com/apache/jena/blob/main/LICENSE
- Senzing SDK EULA/Evaluierung: https://www.senzing.com/docs/quickstart/quickstart_linux/
- Apache Hop: https://github.com/apache/hop/blob/main/LICENSE
- Apache NiFi: https://github.com/apache/nifi/blob/main/LICENSE
- QGIS: https://github.com/qgis/QGIS und https://qgis.org/license/
- Kepler.gl: https://github.com/keplergl/kepler.gl/blob/master/LICENSE
- Maltego App: https://support.maltego.com/en/support/solutions/articles/15000011921-if-maltego-is-open-source-where-can-i-find-the-source-code-
- Maltego SDK: https://docs.maltego.com/en/support/solutions/articles/15000053545-building-integrations-for-maltego
- OpenCTI Community vs EE: https://github.com/OpenCTI-Platform/opencti/blob/master/LICENSE
- Python SGP4: https://github.com/brandon-rhodes/python-sgp4/blob/master/LICENSE
- CesiumJS: https://github.com/CesiumGS/cesium/blob/main/LICENSE.md

## 7. Abschluss

```text
LICENSE_PRECHECK = PASS_WITH_CAVEATS_PRIMARY_SOURCE_URL_LEVEL
GOTHAM_FOSS_CLAIM = FALSE
MEMGRAPH_UNRESTRICTED_OSS_CLAIM = FALSE
MALTEGO_APPLICATION_FOSS_CLAIM = FALSE
SENZING_SDK_FOSS_CLAIM = NOT_SUPPORTED
VALID_INDEPENDENT_OPEN_CANDIDATES = JENA_HOP_NIFI_QGIS_KEPLER_OPENCTI_CE_SGP4_CESIUMJS_NEO4J_CE
ORIGINAL_LIBRARY_BYTES_HASHED = NO
NEXUS_NODE_INSTALLS = ZERO
NEXT_ALLOWED = INDIVIDUAL_OFFLINE_EXPERIMENTS_WITH_INDEPENDENT_NEGATIVE_FIXTURES
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
