# R32.2 Vorvalidierung: Institutionen-Strukturmatrix (grob)

**Status:** GROBE_VORVALIDIERUNG durch MISTRAL/VIBE (2026-10-04). **Kein Ersatz für die QWEN-Deep-Research**, sondern Fundament und Fokus-Vorgabe dafür. Claim-Ceiling: **C1_DESCRIPTIVE_ONLY**. Jede extrahierte Struktur ist primärquellenbasiert; Lücken sind als offene Fragen an QWEN markiert, nicht geschlossen.

## 1. Zweck

Strukturelle Vorvalidierung der Referenzinstitutionen, aus denen das NEXUS_Research_Framework (Collegium NEXUS OMEGA) gegossen wird. Ziel: QWEN erhält eine belastbare Startmatrix mit klar benannten Extraktionslücken statt einer leeren Suche.

## 2. Strukturmatrix

| Institution | Extrahierte Kernstruktur (grob) | Strukturprinzip fürs CNO | Primärquelle | Offene Punkte für QWEN |
| --- | --- | --- | --- | --- |
| **CERN** | Member States tragen Kosten anteilig (proportional zum Net National Income); Council als oberstes Gremium mit vollen Stimmrechten; Experiments werden von Funding Agencies getragen, nicht zentral; Beobachterstatus ohne Stimmrecht; assoziierte Mitgliedschaft als Vorstufe | **Mitgliedschaft durch Beitrag, nicht durch Zustimmung**; geteiltes Instrument (Beschleuniger ≙ Korpus); abgestufte Beteiligungsränge | [CERN Member States](https://home.cern/about/who-we-are/our-governance/member-states), [CERN Participation](https://international-relations.web.cern.ch/stakeholder-relations/Participation-CERN) | MoU-/In-kind-Beitragsmechanik; wie CERN Open Data Publikationsstufen regelt; Konfliktlösung zwischen Member States |
| **NASA** | Neben projekteigenen Reviews existieren **unabhängige technische Reviews durch ein Standing Review Board (SRB)**; Lebenszyklus-Reviews als Phasenübergänge; SRB-Handbuch (NASA/SP-2016-3706) als Instanz | **Unabhängiges SRB mit Veto-Funktion neben der Projektarbeit**; Phasen-Gates (Pre-A bis D ≙ R-Runden) | [Glenn GLPR 7123.35A](https://www.nasa.gov/wp-content/uploads/2025/04/glpr-7123-35a-wc1.pdf), [NPR 7123.1A](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_7123_001A_&page_name=Chapter5) | Vollständige Gate-Matrix (SRR/PDR/CDR/FRR); SRB-Besetzung und Befangenheitsregeln; Anomaly-Reporting-Verfahren |
| **ESA** | Review-Organisation standardisiert in **ECSS-M-30-01A** (Organization and conduct of reviews); Cooperative Agreements als Vertragsrahmen für Forschungsaktivitäten (Discovery-Programm); differenzierte Vertragsformen | **Standardisierte Review-Durchführung als Norm (nicht Ad-hoc-Praxis)**; vertragliche statt informelle Kooperation | [ECSS-M-30-01A](https://sci.esa.int/documents/34923/36148/1567254180098-ecss-m-30-01a.pdf), [ESA Cooperative Agreements](https://www.esa.int/Enabling_Support/Preparing_for_the_Future/Discovery_and_Preparation/Running_Activities_implemented_through_Cooperative_Agreements_in_the_Discovery_Programme) | Review-Board-Komposition (Chair, unabhängige Reviewer); Missionsphasen-Modell; Verhältnis ECSS-Norm zu internen ESA-Prozessen |
| **NIST** | **Measurement Quality Assurance Program mit Round Robins**: wiederkehrende Interlaboratoriums-Vergleiche mit gemeinsamen Referenzproben; mehrjährige Labor-Performance-Bilanzierung; „measurement comparability summary" je Labor | **Ringversuch als institutionelle Form** — identisches Referenzmaterial, unabhängige Labore, gemessene Äquivalenz; Langzeit-Performance-Tracking | [NISTIR 7880-27 (MMQAP)](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=914180) | Explizite Kompatibilitäts-/Bestehenskriterien; Probenherstellung und Verteillogik; Umgang mit Outlier-Laboren |
| **Paul-Ehrlich-Institut / OMCL** | **Batch-Release (OCABR)**: kritische Bewertung des Herstellerprotokolls + experimentelle Prüfung von Chargenmustern durch staatliche Kontrolllaboratorien; gegenseitige Anerkennung anderer OMCL-Prüfungen bei Normkonformität | **Nichts verlässt das Haus ohne geprüfte Charge**; duale Prüfung (Dokument + Stichprobe); Anerkennungsnetzwerk statt Zentralismus | [PEI Batch Testing](https://www.pei.de/EN/service/faq/regulation/faq-batch-testing-node.html) | OCABR-Guideline-Struktur im Detail; Verhältnis PEI ↔ EURL/OMCL-Netzwerk; Verweigerungs-/Rückrufverfahren |
| **ERC** | Peer Review über **Panels** (Scientific Council, Standing Committee on Panels); schriftliche Individualreviews vor Panel-Sitzungen; zweistufige Verfahren; **prozedurale Fehler sind formal definiert** (falsche Kriterien = Verfahrensfehler) | **Fehlerhafte Bewertung ist selbst regelwidrig** — Verfahrensqualität ist messbar; Trennung Individualreview ↔ Panelkonsens | [ERC Guide for Peer Reviewers](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/experts/guide-for-peer-reviewers-he-erc-stg-cog_en.pdf), [ERC Rules for Submission and Evaluation](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/guidance/erc-rules-for-submission-and-evaluation_he-erc_en.pdf) | Panel-Besetzungslogik; Befangenheits-/Recusal-Regeln; wie Einzelreviews in Panelentscheide transformiert werden |
| **Max-Planck-Gesellschaft** | **Wissenschaftliche Beiräte je Institut**, mit international anerkannten externen Wissenschaftlern besetzt; periodische Evaluation (üblicherweise alle drei Jahre); Verfahrensregeln vom Senat beschlossen („Rules for Scientific Advisory Boards", 2023) | **Externe periodische Instituts-Evaluation** mit festem Zyklus; Beirat berät die Zentralorgane, bewertet aber das Institut | [MPG Scientific Advisory Boards](https://www.mpg.de/21051931/scientific-advisory-boards), [Rules SAB 2023](https://www.mpg.de/197429/rulesScientificAdvisoryBoards.pdf) | Bewertungsberichtstruktur; Konsequenzverfahren bei negativer Evaluation; Verhältnis Beirat ↔ Senat ↔ Präsident |
| **Universitäres Tenure-System** | Peer-Committee-Begutachtung über Jahre (Annual Reviews auf dem Weg zur Tenure); **externe Gutachter**; Einflussnahme der Kandidaten auf Gutachter ist verboten (z. B. UMN-Policy); mehrdimensionale Kriterien (Forschung, Lehre, Service) | **Beförderung (Tenure) nur durch unabhängig geprüfte Evidenz**; Einflussnahme-Verbot als Hartregel; feste Kriteriendimensionen | [UMN Tenure Procedure](https://policy.umn.edu/hr/tenure-proc01), [USF Tenure Guidelines](https://www.usf.edu/provost/faculty-success/professional-development/guidelines-tenure-and-promotion.aspx) | Recusal-Mechanik im Detail; Evidenzstandards je Kriterium; Scheitern/Umgang mit negativen Entscheidungen |

## 3. Vorvalidierte Konvergenzen (Verfassungsbausteine)

Über alle acht Institutionen wiederholen sich fünf Strukturprinzipien — das sind die Kandidaten für die CNO-Charta:

1. **Unabhängige Review-Gremien** mit definierter Besetzung und von der Arbeit getrennter Autorität (NASA SRB, MPG-Beirat, ERC-Panels, Tenure-Committees).
2. **Formale Gates** als Phasenübergänge mit Ein-/Ausschlusskriterien (NASA, ESA/ECSS).
3. **Beitrag statt Zustimmung** als Mitgliedschaftsbasis (CERN).
4. **Periodische Evaluation mit festem Zyklus** und externen Gutachtern (MPG, Universitäten).
5. **Geprüfte Freigabe**: nichts geht in den Feldzustand ohne messbare Prüfung gegen Referenz (PEI, NIST).

**Negativbefund der Vorvalidierung:** Keine der acht Institutionen hat ein dokumentiertes Verfahren für *messbare Äquivalenz über Substrate* — das Ringversuchs-Prinzip (NIST) kommt dem am nächsten, operiert aber mit Labores statt Software-Substraten. Das bleibt die originäre CNO-Leistung.

## 4. Quellennotizen

| Quelle | Glaubwürdigkeit | Stand |
| --- | --- | --- |
| [NASA Glenn GLPR 7123.35A](https://www.nasa.gov/wp-content/uploads/2025/04/glpr-7123-35a-wc1.pdf) | 5/5 | 2025 |
| [NASA NPR 7123.1A (NODIS)](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_7123_001A_&page_name=Chapter5) | 5/5 | - |
| [CERN Member States](https://home.cern/about/who-we-are/our-governance/member-states) | 5/5 | - |
| [CERN Participation](https://international-relations.web.cern.ch/stakeholder-relations/Participation-CERN) | 5/5 | - |
| [ECSS-M-30-01A (ESA)](https://sci.esa.int/documents/34923/36148/1567254180098-ecss-m-30-01a.pdf) | 5/5 | - |
| [ESA Cooperative Agreements](https://www.esa.int/Enabling_Support/Preparing_for_the_Future/Discovery_and_Preparation/Running_Activities_implemented_through_Cooperative_Agreements_in_the_Discovery_Programme) | 4/5 | - |
| [NISTIR 7880-27 (MMQAP)](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=914180) | 4/5 | - |
| [PEI Batch Testing](https://www.pei.de/EN/service/faq/regulation/faq-batch-testing-node.html) | 5/5 | - |
| [ERC Guide for Peer Reviewers](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/experts/guide-for-peer-reviewers-he-erc-stg-cog_en.pdf) | 5/5 | - |
| [ERC Rules for Submission & Evaluation](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/guidance/erc-rules-for-submission-and-evaluation-he-erc_en.pdf) | 5/5 | - |
| [MPG Rules for Scientific Advisory Boards](https://www.mpg.de/197429/rulesScientificAdvisoryBoards.pdf) | 5/5 | 2023 |
| [MPG Scientific Advisory Boards](https://www.mpg.de/21051931/scientific-advisory-boards) | 5/5 | - |
| [UMN Tenure Procedure](https://policy.umn.edu/hr/tenure-proc01) | 4/5 | - |
| [USF Tenure Guidelines](https://www.usf.edu/provost/faculty-success/professional-development/guidelines-tenure-and-promotion.aspx) | 3/5 | - |

**Vorbehalte:** Die Extraktion ist bewusst grob (je Institution 1–2 Primärquellen, keine Normrevisionen);ESA/NIST-Dokumente liegen als PDF vor und wurden über Suchsnippets erschlossen, nicht im Volltext kodiert. Alle offenen Fragen müssen durch QWEN-Deep-Research mit Primärquellen im Volltext beantwortet werden.

```text
R32_PREVALIDATION_STATUS = GROB_C1
INSTITUTIONS_COVERED = 8
PRIMARY_SOURCES_BOUND = 14
OPEN_EXTRACTION_GAPS = 24 (je Institution ~3, siehe Matrix)
CROSS_INSTITUTION_CONVERGENCES = 5
SUBSTRATE_EQUIVALENCE_PRECEDENT = NONE_FOUND
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```
