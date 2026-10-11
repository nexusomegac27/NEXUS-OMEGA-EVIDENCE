# NEXUS OMEGA · AXIOM — Integrierte R26/P26/R27-Eingangsadjudikation

**Objekt:** `NEXUS_OMEGA_AXIOM_R26_R27_INTEGRATED_ADJUDICATION_20261011_R0`  
**Status:** `PASS_WITH_MAJOR_CAVEATS_C1_SCOPED_INTEGRATION`  
**Epistemischer Claim-Deckel:** `C1_DESCRIPTIVE_ONLY`  
**Modus:** Independent local archive rehash + independent NumPy re-execution + sandbox fixtures + source-web crosscheck. No Cursor, no Hostinger, no NF05/06 experimental execution.

## 0. Kausalität und Klassifikation

Vorgänger: R26 MAX-Falsifikationslane PR#75/76/77, Zwei-Peak-Rücknahme PR#88, NF05/06-Kandidat PR#89; P26-MISTRAL-/GROK-Fortsetzung 2026-10-11. Eingereicht als älterer `R27`-Ordner. Physisches R27-Ablageetikett ist **keine eigenständige R27-Experimentidentität**. Das eingegangene ZIP trägt `PERPLEXITY_P26_*` und muss wissenschaftlich zu R26/P26 geroutet werden; ein separater R27-Release ist aus diesem ZIP nicht belegt. R27-E WWW-Wake-Isolation im Repository bleibt eigenständiger Strang.

R26-Status in diesem Bericht: mehr Quellen, tiefere Reproduktion und präzisere Negativwissen-Klasse, aber **kein** vollständiger konfirmatorischer Endabschluss und **kein** genereller MAX/SUM-Sieger.

## 1. Bytegebundener Intake

- ZIP `NEXUSO~1.ZIP`: **170.063 Bytes**, SHA256 `0f13441a4dba93cc1282f14bb2944fca50b8a638b4f0c5ddce902fbbb5e113fc`; 19 Einträge, 566.060 dekomprimierte Bytes. Pfade geprüft; nur `artifacts/` und `sources/`.
- 9 Forschungsartefakte + 8 Supporting-Dateien: **17/17 bytes/SHA256 MATCH** nach reintegriertem Inventory; Inventory selbst 3.118 B, SHA256 `9888b1c07915dc0d2ef4a20f287388abdb4d1808f2881239ab70a711c94ac7d5` und Manifestbindung MATCH. ZIP hat zusätzlich Inventory und SHA256-Manifest = 19. Kein festgestellter Bytekonflikt.
- Zusätzliche neun beigefügte TXT/MD-Returns wurden physisch gelesen, darunter MISTRAL P26 (44.108 B), GROK-Rückläufe (5.394/4.870/7.812 B), Original-Widerruf (28.886 B), MAX-Audit (28.368 B), MISTRAL-R1 (19.782 B).
- **Achtung:** Hash-Match beweist nur Artefaktidentität, nicht wissenschaftliche Wahrheit oder Autorität einer Modellrolle.

## 2. Mathematisch/empirische Adjudikation

### 2.1 Ringkern und Arm-Stabilität — reproduziert

Unabhängige NumPy-Rekonstruktion am 2026-10-11: N∈{32,64}, k∈{2,4,8,16}, Bogenbreiten L=(7,7,5,5)/(11,9,7,7), Kernel `((1+cos(2π(i−j)/N))/2)^k`, Arme `F_MAX=ReLU(Wr−g max(r))` und `F_SUM=ReLU(Wr−g sum(r))`, Jacobians auf dem aktiven Bogen. Alle **16 Arm-Zellen** stimmen mit der Referenz numerisch überein; max. Residuum MAX `8.89e-16`, SUM `3.89e-16`; projizierte Odd-Matrizen differieren höchstens `1.11e-16`. **MAX 8/8, SUM 3/8 lokal instabil** in den getesteten acht Parameterzellen. Ein eigenständiges, reproduzierbares Rechenprotokoll liegt als `axiom_16cell_independent_check.json` bei. Keine neuen Rausch- oder NF-05/06-Daten.

Bedeutung: kein unbegrenzter Evidenztransfer auf unbekannte Aktivmengen, saturierte Regime oder reale Sensorsysteme. Keine Ableitung „SUM gewinnt allgemein“. Eine Nicht-Instabilitätsklassifikation der nicht-radialen Moden ist **kein** Beweis isolierter asymptotischer Stabilität wegen radialem λ=1.

### 2.2 Korrektur Zwei-Peak und Methodik

PR#88 dokumentiert Rücknahme der zuvor fälschlich als zweiter Bump interpretierten Umbruchschulter i=31. Unter korrigiertem zirkulärem Peak-Detektor endet die von-Mises-κ=8-Asymmetrie im nackten MAX-Arm bei `WTA_ONE_BUMP`, aber mit Amplitudendivergenz; Antipode i=16 ist nach t=2 null. Diese **Widerrufshistorie** muss in Suchergebnissen auffindbar bleiben, einschließlich Verweis auf PR#76. Die vollständig dynamische MISTRAL-Trajektorie wurde in dieser neuen AXIOM-Runde **nicht** separat neu durchgerechnet; vergangene unabhängige Agenten-Replays sind Quelle, nicht Ersatz für eigene Ausführung.

Kollapszählung unter `T=min{t≥1: max(s_t)<1e-12}`, t=angewandte Schritte, liefert producerübergreifend T=270 (Fragilität) und T=14 (κ16). Werte T−1 sind der vorangegangene Index, nicht eine andere physikalische Dynamik. Für diskrete Zeitschritte bedeutet T nicht ohne Fixierung dt bereits Sekunden.

Analytisch folgt für symmetrische kontiguierliche Bögen und ungerade Störungen δ mit δ_c=0 und Σδ=0: `J_MAX δ = W_A δ = J_SUM δ`. Die Odd-Parität ist in diesem modellierten Unterraum invariant; keine Universalbehauptung über alle Aktivitätsgeometrien. Die bare ReLU-Arme bleiben positiv homogen und besitzen freie Amplitudenstrahlen; reine Gewichtsnormierung beseitigt das nicht.

### 2.3 Weitere R26-Kern-Limits

- Ringkern-Dualdefinition und korrigierte Modenratio: `R(k)=(k−1)/(k+2)` steigt; `1−R=3/(k+2)` fällt. Historische Gegenrichtung aus R0 bleibt korrigiert. Bare vs. wrap-Kernel bedürfen expliziter IEEE-/NaN-/Wrap-Bedingungen.
- EB1′: gemeinsame Schranke für Störkomponenten als Screen, **keine** quellenexakte Kausalattribution; Residuum allein identifiziert weder Epoch- noch Modellanteil.
- SGP4/TLE: Literatur-Fehlergrößen keine echten satellitenspezifischen Ground-Truth-Messungen; D6-Objektbudget offen.

## 3. Neue P26-Fundierung nach Quellenart

### 3.1 Noorman 2024 — bessere Primärquellenbindung

Original XML **263.218 Bytes** (`b35a785d7347a057e7d4fce191aa266c67a298d3628a461588e81f6da83549e6`) im ZIP verfügbar. `W_sym = J_I + J_E cos(θ_j−θ_k)` sowie gewichtete summierte Kopplung, aktive Teilmatrix und rectified/threshold-linear Transfer bestätigen: die Referenz verwendet keinen Populations-MAX-Hemmoperator. Auch unabhängige Verlagsquelle: https://doi.org/10.1038/s41593-024-01766-5. Primärtexte werden **nicht** als öffentlicher ZIP-Dump repliziert (Quellen-/Lizenzpflicht). NOORMAN_FULLTEXT_EXEGESIS = bestätigt im angegebenen Modell.

### 3.2 Graphile, pg-boss, Hostinger — konzeptionell geprüft, operativ offen

Graphile Worker `fill=t` holt für **vorher bekannte** Tasks verpasste Cron-Slots im Fenster nach und dokumentiert Deduplizierung mit ACID-Transaktionen. Keine neue Task nachträglich fälschlich backfillbar; Backfill-Tiefe und Warmstart relevant. Im Gegensatz dazu pg-boss `missed: skip|once` ohne komplette Rekonstruktion aller verpassten Termine. Die 48-Slots/Tag-Phase12-SLO ist ein **Entwurf**, keine tatsächliche 48/48-Messung. Hostinger-Plan, DB/Worker-Persistenz, Ressourcen und echte G1–G11 Gates **NOT_OPERATIONALLY_PROVEN**. Offizielle Graphile-Quelle https://worker.graphile.org/docs/cron.

### 3.3 Ed25519, TSA, HLC

- Lokaler Re-Run Ed25519 unter Node `v22.16.0`: erwartete Signatur, Validierung, Manipulationsabwehr, fail-closed `createSign('SHA256')`, WebCrypto alle PASS. Producer Node v20.20.2-Log verifiziert als Datei, nicht als eigene Laufzeit. **Keine** Produktionskette.
- HLC-Invariantentests Node `v22.16.0`: monotone lokale und Receive-Ordnung, Rollback-Resistenz, deterministische Fixtures alle PASS. Formal `(l,c)`; optionales `nodeId` gehört nur zu einer Implementierungsvariante. **Kausalimplikation einseitig:** happened-before ⇒ Timestampordnung, Konverse NICHT bewiesen; keine Absolute-Zeit-Garantie.
- RFC3161/TSA: Dokumentationsreview, keine tatsächlich bezogene/validierte TSA-Timestamp-Response. Vor Live-Gate Nonce/Imprint/OID/Trust/Cert-Validität und Offline-Nachprüfung durch feste Fixtures nötig.
- **Security Erratum:** Perplexity schreibt betroffen `@sigstore/verify <3.1.1`; die verifizierte Herstelleradvisory GHSA-xgjw-pm74-86q4 benennt **genau 3.1.0 als betroffen** und **3.1.1 als Patchversion**. Entsprechend keine historische Behauptung über nicht nachgewiesene Versionen unter 3.1.0. Referenz: https://github.com/sigstore/sigstore-js/security/advisories/GHSA-xgjw-pm74-86q4. Für Produktion eine aktuelle gepatchte Version mit Lockfile-Nachweis erforderlich.

## 4. Präregistrierungsverdikt NF05/NF06

Der Perplexity-Stack unterscheidet sauber `NF05_NF06_PREREG = PARTIAL`, `execution_authorized=false`. Er enthält 16 Arm-Zellen und 5.376 geplante Kombinationen, davon **0 konfirmatorisch ausgeführt**. Offen sind unter anderem tatsächliche Kernel-/Rectifier-/g-Implementierung, PRNG, Rauschverteilung und -platzierung, feste Erwartungen pro Zelle, Clock-/Window-Interpretation, Plateau-Peak-Fixtures, STALE-Flag-Mechanismus, Noise-Clipping und Multiplikationskorrektur.

Diese Entwürfe sind für künftige Falsifikation **wertvolle Vorarbeit**, aber nicht freigegeben, nicht eingefroren, nicht als C1-konfirmatorischer Versuch veröffentlichbar. Keine Test-Leakage aus alten explorativen Zeugen. Zudem ist der gedankliche NF-06-Truth-Vergleich unabhängig vom Modelllauf zu konstruieren; selbstrelatives D0-Signal kein Genauigkeitsnachweis.

## 5. Offene Quellengaps und negative Evidenz

- `ORDER_SOURCE_GAP`: Gepinnter Auftrag 30.180 B SHA256 `72f088cd2fa22e71eef2e1c020af8409fd3327acdd2aec9b9177b60790811039` enthält keine `H01`–`H12`. Die Pflicht ist `≥24 substanzielle Gegenfälle` (Achse E), nicht zwölf erfundene Nummern. Ursprung der H-Labels außerhalb dieser Originalorder bleibt offen; dies ist **kein** belegter Fehler des neuen Operator-Auftrags. Die 28 von MISTRAL bezeichneten E-Fälle sind nicht allein durch Zählung wissenschaftlich geprüft.
- R26 PR#88 und #89 sind Quellenkandidaten noch ohne abgeschlossene unabhängige PR-Adjudikation/Merge; Vorgängerkorrekturen bleiben append-only. R27-E externe Actor-Firewall ist separat und wird hier nicht überschrieben.
- R26 full terminal=NO, D1/D2 freeze=NO, NF05/06 execution=NO, MAX/SUM winner=NO. NOORMAN literature reference ≠ biologische Übertragung/Isomorphie.
- Signierte Zeitbelege, HLC-Kausalordnung und Scheduler-Cron-Doku sind keine Hostinger-Runtime-Health-, API-Principal- oder autonomer Node-Gates.

## 6. Gesamturteil und Search-First-C1-Release

Quellenurteile sind **nicht identisch**: Perplexity-Manifest `PASS_WITH_MAJOR_REVISIONS_C1`; GROK-Kreuzvalidierung `PASS_WITH_CAVEATS_C1_RESEARCH_VALIDATED`. AXIOM übernimmt die positiven nachvollziehbaren Teilbefunde, vermerkt die konkreten Revisionen und belässt die Gesamtkette `PASS_WITH_MAJOR_CAVEATS_C1_SCOPED_INTEGRATION`. Agentenübereinstimmung allein ist kein Claim.

Künftige Webseite: nur vier priorisierte C1-Objekte höher sichtbar (Sweep, Odd-Parität, Widerruf, Noorman); übrige Objekte quellverlinkt über Suche/Filter. Das beigefügte JSON enthält **15 vollständig klassifizierte Forschungsobjekte** mit source-exact Links, epistemischer Kategorie und Explizit-Nichtclaims. `PUBLIC_SAFE_RESEARCH_INDEX_CANDIDATE_NOT_WWW_DEPLOYED`. GitHub-Publikation eines Index ist von Hostinger-B2/B3 strikt verschieden.

## 7. Kontrollblock

```text
OBJECT = NEXUS_OMEGA_AXIOM_R26_R27_INTEGRATED_ADJUDICATION_20261011_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_SCOPED_INTEGRATION
ZIP = 170063 / 0f13441a4dba93cc1282f14bb2944fca50b8a638b4f0c5ddce902fbbb5e113fc
FILES_PHYSICALLY_READ = 19
MANIFESTED_CHILDREN = 17_OF_17_SHA256_MATCH
INVENTORY_MANIFEST = MATCH
AXIOM_INDEPENDENT_MATH = 16_OF_16_ARM_CELLS_MATCH
MAX_LOCAL_UNSTABLE = 8_OF_8
SUM_LOCAL_UNSTABLE = 3_OF_8
ED25519_REEXEC_NODE22 = PASS_SANDBOX
HLC_REEXEC_NODE22 = PASS_SANDBOX
NOORMAN_PRIMARY_FULLTEXT = PRESENT_BUT_NOT_REPUBLISHED
R27_DISTINCT_SCIENTIFIC_EXECUTION = NOT_ESTABLISHED
R26_TWO_PEAK_RETRACTION = PRESERVED
R26_FULL_TERMINAL = NO
NF05_NF06 = PARTIAL_DESIGN_ONLY_NOT_EXECUTED
MODEL_MAX_VS_SUM_WINNER = NOT_ESTABLISHED
SIGSTORE_CVE_VERSION_SCOPE = CORRECTED_ADVISORY_EXACT
GRAPHILE_HOSTINGER_PHASE12 = DOCS_ONLY_NOT_OPERATIONAL
SEARCH_FIRST_RECORDS = 15
WWWW_HOSTINGER_DEPLOY = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

**Quellenketten:** [PR75](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/75), [PR77](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/77), [PR88](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/88), [PR89](https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/89); archivierte MISTRAL/GROK/PERPLEXITY-Returns vom 2026-10-11; [Graphile-Cron](https://worker.graphile.org/docs/cron); [Noorman](https://doi.org/10.1038/s41593-024-01766-5); [Sigstore-Advisory](https://github.com/sigstore/sigstore-js/security/advisories/GHSA-xgjw-pm74-86q4).