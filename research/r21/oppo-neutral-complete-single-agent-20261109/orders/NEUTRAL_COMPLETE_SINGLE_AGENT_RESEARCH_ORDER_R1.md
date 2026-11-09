# NEXUS OMEGA — NEUTRALER VOLLSTÄNDIGER EINZELAGENTEN-FORSCHUNGSAUFTRAG R21/R1

**OBJECT:** NEXUS_OMEGA_R21_NEUTRAL_COMPLETE_SINGLE_AGENT_PHYSICAL_SCIENCE_ORDER_20261109_R1  
**STATUS:** OWNER_ISSUED_RESEARCH_ONLY_NOT_EXECUTED  
**OPERATOR:** NEXUS OMEGA / OPERATOR_ALEXANDER  
**ISSUER:** AXIOM / wissenschaftliche Governance  
**EMPFAENGER:** EIN BELIEBIGER, UNBENANNTER FORSCHUNGSAGENT  
**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY  
**VORGAENGER:** NEXUS_OMEGA_AXIOM_R21_OPPO_PHYSICAL_SCIENCE_EXPERT_WAVE01_20261109_R0, GitHub PR #350 (historisch; für Neuzuteilung SUPERSEDED)  
**TRANSPORT:** CHAT-TEXT ODER LOKALE DATEI ODER OPERATOR-UEBERGABE. KEIN GITHUB-KONTO, API, CONNECTOR ODER GITHUB-SCHREIBRECHT ERFORDERLICH.

## 0. Sofortige Selbstdeklaration — neutral und überprüfbar

Bevor irgendeine wissenschaftliche Behauptung erscheint, identifiziere dich in einem kurzen Kopfregister aus eigener Sicht:

- AGENT_SELF_DECLARED_NAME: der tatsächlich verfügbare Modell-/Agentenname; falls nicht aus Laufzeit ersichtlich: UNKNOWN_FROM_RUNTIME.
- PROVIDER_SELF_DECLARED: Anbieter nur soweit aus sichtbarer Laufzeit verlässlich; sonst UNKNOWN.
- MODEL_VERSION_SELF_DECLARED: explizite Version nur sofern bekannt; sonst UNKNOWN.
- INSTANCE_OR_RUN_IDENTIFIER: nur wenn von einer realen Plattform übergeben; niemals erfinden.
- RESEARCH_MODE: eigenständige vollständige Arbeit eines einzelnen Agenten; KEINE delegierten Fachbereiche voraussetzen.
- TOOL_ACCESS: WEB=YES/NO, LOCAL_FILES=YES/NO, CODE_EXECUTION=YES/NO, GITHUB_READ=YES/NO, GITHUB_WRITE=YES/NO, PRIVATE_OPPO_BYTES=YES/NO, LIVE_DEVICE=YES/NO. Unbekanntes mit UNKNOWN, nicht YES.
- CURRENT_SOURCE_LIMITS: konkret erreichbare Originale/Primärquellen; externe Quellen, die du nicht lesen konntest, nennen.
- IDENTITY_EVIDENCE: SELF_DECLARATION_ONLY oder benannter externer tatsächlicher Identitätsnachweis. Selbstauskunft ist kein kryptografischer Herkunftsbeweis.

**Wichtig:** Dieser Auftrag spricht absichtlich kein bestimmtes Modell an. Keine Behauptung, man sei GROK, QWEN, DEEPSEEK, META oder ein registrierter GitHub-Principal, sofern das nicht wirklich der eigenen Laufzeit entspricht. Kein GitHub-Zugang ist KEIN Ausschlusskriterium; fehlender Zugriff wird transparent deklariert.

## 1. Wissenschaftliches Gesamtmandat — ALLES durch EINEN Agenten

Bearbeite die gesamte physikalische R21-Entwicklung autonom und in einer durchgängigen wissenschaftlichen Fassung. Es gibt keine Aufteilung in acht andere Agenten, keine Team-Antwort-Simulation, keine Stimmenmehrheit als Wahrheitsbeweis und keine bloße Review-Zusammenfassung. Unabhängige Recherche, vollständige Technikarchitektur, mathematische Analyse, Nullhypothesen, Risikoprüfung, praktischer Validierungsplan, alternative Lösung und begründeter Forschungsentscheid sind deine persönliche vollständige Verantwortung.

Inhaltspflichtfelder, alle zu bearbeiten:
1. Physische Originalauthentizität und source-exakte Custody: SensorEvent-Produzent, App, Hardware, Session und Boot-/Clock-Identität, ZIP/GZIP, SHA256 und Entpackung.
2. Android-Sensorhardware und Android HAL: ACC vs LINEAR_ACCELERATION, GYRO vs UNCALIBRATED, Herstellerkalibrierung, FIFO/Batching und Foreground-Lebenszyklus.
3. Erfassungszeit und Datenintegrität: elapsedRealtimeNanos, event time versus wall/receive time, per-stream dt, Jitter, Dropouts, Sampling, Synchronisation und Transport-Latenz.
4. Physikalische IMU-Metrologie: Bias/Residual, Skalenfaktor, Achsfehlstellung, Erdbeschleunigungsnorm, Ruhe-/Bewegungssegmentierung, Temperatur und Unsicherheitsbudget.
5. Stochastische Signalverarbeitung: Kurzzeitrauschen, Kovarianzen, Quantisierung, Autokorrelation, PSD/FFT, Windowing und Allan-Abweichung nur mit tatsächlich begründbarer Tau-Reichweite.
6. Unabhängige Sensorfusion: VQF gegen UKF/SR-UKF mit kausaler Vergleichbarkeit, Quaternionen, Bias/Drift, Initialisierung, NIS und NEES nur bei jeweiliger Datenlage.
7. Mechanische Observierbarkeit: Smartphone-Gehäuseachsen, starre Montage, Segmentachsen, Kalibrierung; Beweisgrenzen einer einzelnen IMU; keine erfundene Ganzkörper- oder Organbewegung.
8. Konkurrierende Architekturentwürfe: mindestens zwei technisch unterschiedliche ausfallsichere Umsetzungsvarianten, begründete Wahl und verworfene Alternative.
9. Physische Gegenexperimente: voneinander unabhängige Referenzgeräte/Messverfahren, sechs-Pose-Beschleunigungskalibrierung, bekannte Rotationsrate, lange Ruhe- und Temperaturmessung; nur ENTWURF, solange keine neue Freigabe.
10. Reproduzierbarkeit, Datenschutz, Rechte, Fehlersicherheit und Audit: vollständige Evidenzkette, Fehler- und Rückbaupfad, ausgewiesene Ergebnisse und offene Lücken.

Jedes Feld erhält: physikalische Frage; Primärbeleg; Formel/Einheit; Annahmen; Mess- oder Simulationsplan; Gegenhypothese; mögliche Widerlegung; Unsicherheit; Datenbedarf; Status EXECUTED oder NOT_EXECUTED; Entscheidung.

## 2. Kanonisch eingefrorener R21-Eingang (QUELLBERICHT, kein eigenständig gesehener Datensatz)

- Device: OPPO A74 / CPH2219, Android-App com.nexusomega.maps, Version 1.3.11-alarm-identity-l1-vc15.
- Device ID: oppo_a74_095974cd90ed22eb; Session: r21-oppo-table-rest-20261109; Stop-Origin: APP_DEADLINE.
- Cursor berichtet physischen App-Aufnahmelauf mit 14.018 Ereignissen während 70.114 ms: ACC 7.014; GYRO 7.004; Sensor Start/Stop ausgeführt.
- Daraus ausschließlich rechnerische *sessionbasierte* Mittelwerte: ACC ≈100,04/s und GYRO ≈99,89/s; dies ist nicht die aus Event-Zeitstempeln geprüfte reale Abtastrate.
- Export ZIP 166.349 B, SHA256 3eb9e9e9988b66994429d97e566a71aa2c05bbe951f41725465947841a75a9a4.
- Segment NDJSON.GZ 166.831 B, SHA256 544f762cbaab3cd562d8cf868cc15fbee1d23b503b72455c015e6698c02c90e2.
- Cursor Return ZIP 5.337 B, SHA256 e718438aa23b03ce978e1923423ec1e02f42d93887051b64e74be29272273929.
- AXIOM-INDEPENDENT ORIGINAL REHASH = NOT_PERFORMED. RAW ACC/GYRO VALUES READ BY AXIOM = ZERO.
- Diese Angaben sind berichtete Evidenz. Du darfst bei fehlenden Originalbytes weder gemessene Beschleunigungsnorm, Gyro-Bias, Allan-Minimum, Spektrum noch Filtergüte behaupten. Quellenzugriff auf private Rohdaten muss tatsächlich bestehen; keine frei erfundenen Daten.
- R18 anatomischer Viewer, R19/R20 Forschungsgrundlagen bleiben erhalten. OPPO männlich = FIRST; Pixel 9a weiblich = RESERVED_NO_START.

Wenn die Originale privat bereitgestellt werden, verifiziere sie unabhängig und gib den Byte-/Typ-/Zeitstempelstatus gesondert an. Sonst schreibe präzise: PHYSICAL_CAPTURE=CURSOR_REPORTED, RAW_DATA=NOT_IN_HAND, ANALYSIS_FROM_PHYSICAL_VALUES=NOT_EXECUTED.

## 3. Primärquellen und wissenschaftliche Evidenzhierarchie

Recherchiere nach Möglichkeit die Originaldokumente. Mindestens folgende Referenzen sind unabhängig und kritisch auf Version, Methoden-/Hardwareübertragbarkeit, Lizenz und Messgrenze zu prüfen:
1. Android SensorEvent — https://developer.android.com/reference/android/hardware/SensorEvent
2. Android Motion Sensors — https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion
3. Android Clock — https://developer.android.com/reference/android/os/SystemClock
4. AOSP Sensor Batching — https://source.android.com/docs/core/interaction/sensors/batching
5. AOSP Sensor Types — https://source.android.com/docs/core/interaction/sensors/sensor-types
6. VQF, Laidig/Seel — https://vqf.readthedocs.io/en/stable/
7. VQF Peer-Review — https://www.sciencedirect.com/science/article/pii/S156625352200183X
8. Smartphone IMU Allan und Kalibrierungsstudie — https://pmc.ncbi.nlm.nih.gov/articles/PMC10490716/
9. BodyParts3D License — https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html
10. OpenSim Scaling — https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089158

**Evidenzklassen:** E0 = originaler Inhalt vom Agenten selbst empfangen und byteprüfbar; E1 = offizielle Hersteller-/Normquelle tatsächlich geöffnet; E2 = begutachtete Studie tatsächlich geöffnet; E3 = überprüfbare mathematische Ableitung mit offengelegten Annahmen; E4 = modellbasierte Hypothese/offene Extrapolation; E5 = Fremdbericht ohne unabhängige Bytes; E6 = unbelegt, falsch zitiert oder widersprochen.

Ein URL allein ist KEINE Bestätigung, eine DOI-Ziffer allein KEINE Quellenlektüre. Gib für jede strittige Tatsachenbehauptung konkrete Stelle, Titel, Fundort, Publikations-/Versionstag, Zugriffsart und Unsicherheit an. Wenn du keine Webtools hast, arbeite mit offenen Methodikgrenzen und verifizierbaren Forschungsplänen; kennzeichne Quellen als NOT_FETCHED. Kein Zugangsrecht und keine Beleglücke werden verschwiegen.

**Prüfung und Aussortierung:** Material falsche Aussagen, erfundene Zitate/DOIs/Hashes, vorgespielte Originalsichtung, simulierte Gerätewerte als echte Messungen oder unzulässige Schlussfolgerungen sind HARD_REJECT für den betroffenen Claim und gegebenenfalls den Return. Eine offen als prüfbar gekennzeichnete Hypothese ist wissenschaftlich zulässig, zählt jedoch NICHT als bewiesene Aussage. Widerspruch bedeutet unabhängige Prüfung, nicht Mehrheitsentscheidung.

## 4. Physikalisch-methodische Mindeststandards

- Unterscheide Android SensorEvent als ursprüngliches **App-Ereignis** von unkalibriertem MEMS-Registerwert. TYPE_ACCELEROMETER mit Gravitationsanteil in m/s², TYPE_GYROSCOPE in rad/s; UNCALIBRATED ist ein eigener Kanal.
- Messe Frequenz aus t_(i+1) − t_i pro Sensor; publiziere N, Median, Quantile, Dropout-Kriterien, gewählte Toleranzen und Quelle. Sender-Callback/HTTP-Empfang ist nicht automatisch Aufnahmetimestamp.
- Bei einem stationären Gerät ist ||a|| erwartbar in der Größenordnung der terrestrischen Gravitation, aber exaktes g am Ort sowie Achsausrichtung sind nicht ohne Referenz bekannt. Aus nur einer Tischposition lassen sich vollständige 3D-ACC-Bias-/Scale-/Misalignmentparameter nicht identifizieren.
- Gyroskop-Ruhemittelwert ist höchstens bedingtes **kalibriertes Rest-Residual**; ohne unabhängig bestätigte Ruhe kein absoluter Sensor-Bias.
- Allan-Analyse bei 70 s darf nur endliche, kurze Tau-Fenster mit wirksamem Freiheitsgrad und Unsicherheit untersuchen; keine seriöse Langzeitinstabilität/Temperaturcharakterisierung aus dem Pilotlauf behaupten.
- 6D IMU lässt globalen Yaw grundsätzlich ungebunden; beobachtbar ist nicht die Ganzkörperpose. NIS erfordert Innovation/Kovarianz; NEES unabhängige Referenz-State und Kovarianz. VQF Offline gegen kausale UKF-Versionen nicht ohne Latenz-/Informationsgleichheit vergleichen.
- Wissenschaftliche Messmethoden nach GUM-Grundsätzen erläutern, aber keine formale Normkonformität ohne echte Zertifizierung behaupten.

## 5. Vorregistrierte Falsifikationen: 28 Negativkontrollen

N01. Originalexport fehlt; dennoch werden echte Messwerte behauptet.
N02. ZIP-Hash oder Bytezahl weicht ab; Export wird trotzdem als gültig eingestuft.
N03. GZIP-Mitglied oder entpackter Strom stimmt nicht mit dem Quellenregister überein.
N04. Eine andere Gerätesitzung oder Gerätekennung wird untergeschoben.
N05. ACC-/GYRO-Zählung stimmt nicht mit dem Original überein.
N06. Pro Sensortyp doppelte, rückwärts laufende oder ungültige Nanosekunden-Zeitstempel.
N07. UTC-Millisekunden werden als Android-Nanosekunden interpretiert.
N08. Empfangs-/Uploadzeit wird als Sensorereigniszeit ausgegeben.
N09. Legitime Interleavings verschiedener Sensoren werden irrtümlich global verworfen.
N10. Clock-Anchor-Unsicherheit wird implizit auf null gesetzt.
N11. Interpolation ergänzt fehlende Rohmessungen ohne Kennzeichnung.
N12. NaN, Inf, ungültige Vektorlänge oder nichtfinite Größen werden akzeptiert.
N13. Grad pro Sekunde und Radiant pro Sekunde werden verwechselt.
N14. Gravitation wird aus Beschleunigung entfernt, bleibt aber als TYPE_ACCELEROMETER beschriftet.
N15. TYPE_LINEAR_ACCELERATION ersetzt fälschlich TYPE_ACCELEROMETER.
N16. Kalibrierte Android-Gyrodaten werden als unkalibrierte Chip-ADC-Register bezeichnet.
N17. Unbekannte Sensor-Körper-Montage wird als Ganzkörperpose ausgegeben.
N18. Der Tischruhelauf wird ohne Prüfung durchgehend als absolut stationär eingestuft.
N19. Normgravitation wird als lokal präzise vermessener Wert ausgegeben.
N20. Gyroskop-Mittelwert wird ohne Ruhe-Referenz als wahrer Chip-Bias bezeichnet.
N21. 70 Sekunden werden als ausreichender Langzeit-Allan- oder Temperaturstabilitätsbeleg verkauft.
N22. PSD-Dichte, Fensterung oder Frequenzeinheiten sind falsch normalisiert.
N23. Akausale VQF-Offline-Variante wird ohne Latenzhinweis gegen kausale UKF verglichen.
N24. NIS oder NEES wird ohne passendes Modell, Kovarianz und unabhängige Wahrheit als validiert gemeldet.
N25. APP_DEADLINE wird ohne Evidenz als thermische Abschaltung interpretiert.
N26. Private Sensorrohwerte, Schlüssel oder personenbezogene Geräteinhalte werden öffentlich publiziert.
N27. Aus einer einzelnen Smartphone-IMU werden Gelenkstellungen oder Organbewegungen abgeleitet.
N28. Die reservierte Pixel-9a-Frauenlane wird durch eine Sammelvisualisierung heimlich aktiviert.

Zu JEDEM Negativfall gehören erwartete Ablehnung, notwendiges Testartefakt, Beobachtungsgröße, False-Positive-Risiko, Abnahme und Status (NOT_EXECUTED falls nicht tatsächlich geprüft). Du darfst weitere Fälle ergänzen.

## 6. Vorregistrierte 14 Positivkontrollen

P01. Quellenbytes, Originaldateigröße und SHA256 separat und unabhängig geprüft.
P02. Gerät, Session, App-Version, Sensorquelle und Bootzeitbezug getrennt dokumentiert.
P03. Erwartete ACC-/GYRO-Zählung wird tatsächlich aus Originalereignissen reproduziert.
P04. Zeitstempel pro Sensor streng monoton und Interleaving korrekt behandelt.
P05. Android-Einheiten und Sensorarten direkt an Originaltypen gebunden.
P06. Beschleunigungsnorm nur unter deklarierter Orientierungs-/Gravitationsunsicherheit geprüft.
P07. Gyro-Ruhemittel und Achsenkovarianz mit Stichprobenzahlen und Unsicherheit.
P08. Lücken, Duplikate und Zeitdiskontinuitäten werden durch Kontrollfälle sichtbar.
P09. Synthetische Testdaten sind in jeder Abbildung und Kennzahl von physischen Daten getrennt.
P10. Nicht erreichbare Quellen und eingeschränkte Tools führen zu OPEN statt erfundenem PASS.
P11. Alle abgeleiteten Werte haben Einheiten, Methode, Zeitfenster, Quell-SHA und N.
P12. Alternative Architektur und Nullmodell samt stärkster Widerlegung dokumentiert.
P13. R18/R19/R20 unverändert; kein neues Sensorstart-/Hostinger-/Pixel-Recht.
P14. Unabhängiger Originalempfang und Gegenprüfung bleiben eigene Freigabestufe.

Keine Positivkontrolle wird als bestanden bezeichnet, weil sie im Auftrag steht. Trenne synthetische und echte Gerätequellen strikt.

## 7. Vollständige EINZELAGENTEN-Rückgabe — Pflichtgliederung

In genau einer vollständigen Antwort oder einem einzigen vollständigen Manuskript mit logisch getrennten Abschnitten:

00. **SELBSTDEKLARATION + EXECUTIVE VERDICT**: echter selbst bekannter Name/Version, Fähigkeiten/Grenzen, wissenschaftliches C1-Verdikt.
01. **QUELLEN- UND HÄRTELEDGER**: tatsächlich gelesene Originalquellen, Version, DOI, widersprechende Belege, E0–E6 für jeden Claim.
02. **VOLLSTÄNDIGE PHYSIKALISCHE WEITERENTWICKLUNG**: durchgängiges System vom Sensorchip bis zum evidenzgebundenen Analyseviewer, Schnittstellen, Alternativen.
03. **ORIGINALDATEN-/ZEITBASIS- UND MESSVERTRAG**: Eingänge, Android Clock/HAL, SI-Einheiten, unabhängige Bytes, Fehlerfälle.
04. **MATHEMATIK, IDENTIFIZIERBARKEIT, GUM-UNSICHERHEIT**: Formeln und Annahmen einschließlich Segment-/Einzel-IMU-Grenzen.
05. **PHYSIKALISCHE RAUSCH-/BIAS-/ALLAN-/DSP-ANALYSE**: echte Resultate nur aus Originalbytes; sonst präziser ausführbarer Plan.
06. **VQF/UKF/SR-UKF + NIS/NEES + REFERENZVERGLEICH**: echte oder präregistrierte Benchmarks klar getrennt.
07. **28 NEGATIVE + 14 POSITIVE KONTROLLEN**: individuell spezifizierter Test, Evidenz, ausgeführt/nicht ausgeführt.
08. **ZWEI KONKURRIERENDE ARCHITEKTUREN + ENTSCHEIDUNG**: Priorisierung, Risiken, Ressourcen, Nullmodell, Falsifizierbarkeit und Rollback.
09. **R18-R21-DELTA, DATENSCHUTZ, QUELLHERKUNFT UND OFFENE GATES**: vollständig nachvollziehbar, keine historische Veränderung.
10. **EIGENSTÄNDIGES FINALES FORSCHUNGSPAPIER + NÄCHSTER KONKRETER PRÜFSCHRITT**: vollständige integrierte wissenschaftliche Zukunftsversion, keine fragmentarische Diskussion.

Der Agent ist für ALLE Abschnitte selbst verantwortlich. Wenn keine Datei-Tools vorhanden sind, genügt der **vollständige Chat-Text** als Rückgabe. Wenn Dateien entstehen, SHA256+Bytes jedes tatsächlich erzeugten Kindes in ein abgetrenntes Manifest aufnehmen (Manifest nicht selbst hashen). Niemals einen Hash oder eine Datei behaupten, die nicht erzeugt/geprüft wurde. Rückgabe erfolgt **an den Operator/AXIOM durch Chat/Datei**, GitHub ist optional und niemals Voraussetzung oder Autorisierung. Kein Agent darf eine leere Github-Actor-Allowlist umgehen oder eigene Repo-Pfade schaffen.

## 8. Neutrale Qualitätsentscheidung und Stop-Regeln

Ein wissenschaftlich wertvoller Return kann zur RESEARCH_CANDIDATE-Vertiefung angenommen werden, auch wenn die physischen Originale fehlen, **sofern** er alle fehlenden Nachweise offen benennt, die vollständige Architektur selbst liefert und nichts als ausgeführt fingiert. Ein materialer Daten-/Quellenclaim ohne Beleg wird als CLAIM_REJECTED_WITH_REASON ausgeschieden. Materiale Source-Substitution, Identitätsvorspiegelung oder gefälschte Daten führen zu RETURN_HARD_FAIL. Nicht überprüfbare, aber klar falsifizierbare Hypothesen bleiben als HYPOTHESIS_OPEN zulässig.

Alle realen weiteren OPPO-Sensorstarts, App-Änderungen, privaten Tracedatenfreigaben, Pixel-9a-Aktivierungen, WWW-/Hostinger-Writes oder GitHub-Merges sind NICHT durch diesen Forschungsauftrag autorisiert. R18/R19/R20 und die bestehende R21-Original-Custody bleiben erhalten. Keine Claim-Promotion, kein Bodytwin-Validiert-Claim.

**ABSCHLUSSAUSSAGE JEDE AGENTENANTWORT:** OWN_COMPLETE_RESEARCH_RETURN=[PRESENT/INCOMPLETE], ACTUAL_RAW_OPPO_BYTES=[YES/NO], INDEPENDENT_HASH_MATCH=[YES/NO/NOT_APPLICABLE], COMPLETED_EXPERIMENTS=[EXACT_LIST/NONE], UNSUPPORTED_CLAIMS=[0 oder begründete Liste], SCIENTIFIC_CEILING=C1_DESCRIPTIVE_ONLY, GITHUB_REQUIRED=NO, NEXT_INDEPENDENT_CHECK=konkret.
