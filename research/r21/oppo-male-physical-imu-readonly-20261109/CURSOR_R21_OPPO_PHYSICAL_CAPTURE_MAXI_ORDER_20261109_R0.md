# NEXUS OMEGA — AXIOM → CURSOR / PRAXIS
## R21 MAXI ORDER: PHYSISCHE OPPO-IMU-ORIGINALDATEN, NEXUS-APP, QUELLENGEBUNDENER EMPFANG

```text
OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R21_OPPO_MALE_PHYSICAL_IMU_CAPTURE_AND_SOURCE_EXACT_RECEIVER_MAXI_ORDER_20261109_R0
DATE = 2026-11-09
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
RECEIVER = CURSOR_PRAXIS
SCIENCE_RECEIVER = NEXUS_OPERATOR_AXIOM
PREDECESSOR = NEXUS_OMEGA_AXIOM_R21_OPPO_DEVICE_BOUND_SCHEMA_STREAM_GAP_ACK_20261109_R0
FOUNDATION = R18_SOFT_VISUAL_PRESERVED + R19_SEALED_C1 + R20_CLOSED_C1_WITH_CAVEATS
R21_PR = 348_OPEN_DRAFT_NOT_MERGED
R21_PR_HEAD = 1300dcb257e5dc75a7de9f011cda82951e676924
R21_SOURCE_ZIP = 25023_BYTES / feaffc455c9eb135c27c097e8df3114f6b5c67b9fade31bd0394a4cf9186d650
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
BODYTWIN_VALIDATED = NO
OPPO_MALE = PRIORITY_ONE
PIXEL9A_FEMALE = RESERVED_NO_START
CURRENT_CURSOR_REPORT = OPPO_DEVICE_BOUND + PRODUCER_FOREGROUND_WITH_CAVEAT
R21_SCHEMA_STREAM = SOURCE_GAP
PHYSICAL_EVENTS_OBSERVED_BEFORE_THIS_ORDER = 0
NEW_OPERATOR_AUTHORITY = CONTROL_EXISTING_NEXUS_APP_ON_BOUND_OPPO_AND_RUN_CONTROLLED_PHYSICAL_SENSOR_MEASUREMENTS
HOSTINGER_PUBLIC_WRITE = DENY
GITHUB_PUBLIC_RAW_IMU_UPLOAD = DENY
NO_IMU_INVENTION = HARD
```

### 0. Ziel und rechtlich-operative Delegation
Dies ist eine **neue, ausdrücklich vom Operator erteilte operative Ausführungsfreigabe**, die die früheren R21-Verbote von `SENSOR_START_STOP=NOT_EXECUTED` und `TYPE_C_HARDWARE_CENSUS=NOT_AUTHORIZED` **nur für diesen eng begrenzten, autorisierten OPPO-Messauftrag** ablöst. Cursor darf auf dem bereits operatorgebundenen OPPO in der vorhandenen NEXUS-App lokale Sensoransicht/Logging bedienen, autorisierte App-Sensoraufzeichnungen starten und beenden, den Android-/ADB-Hardware-Census durchführen, Daten privat auf den zugelassenen Windows-Arbeitsrechner transferieren und die Rohdaten offline auswerten. Falls erforderlich darf Cursor ein **reversibles lokales Diagnose-Logging** in der bestehenden NEXUS-App ergänzen, lokal bauen und nur als gesondert gesicherte Testversion auf dem bereits autorisierten OPPO verwenden; keine heimliche Veränderung der produktiven App, keine Umgehung der Android-Sandbox, keine Root-Eskalation. Bereits laufende App-/Sensor-Sitzungen vorher sichern, nicht unkontrolliert überschreiben.

**Nicht freigegeben**: Zugriff auf Pixel 9a; Publikation personenbezogener Sensortraces; GitHub-Merge; Hostinger-/WWW-Deploy; Änderungen an Parent-Bodytwin, R18/R19-Historie, SO(4), Cron, Live Feed oder alten Evidenzobjekten; neue externe Agentenrechte; klinische Tests oder medizinische Gültigkeitsaussagen. Sollte ein Gerät nicht tatsächlich operatorautorisiert sein, keine fremden Geräte verwenden. Keine erfundenen Sensordaten, keine rückdatierten Beweise, keine Phantom-ACKs. Keine separaten Rückfragen, sofern der Auftrag innerhalb dieser Grenzen ausführbar ist; dokumentiere real verbleibende physische Blocker und nutze den nächstbesten autorisierten Pfad.

### 1. Governance und kanonischer Bootstrap — verpflichtend, vor Änderung
- `AGENTS.md`, `GOVERNANCE.md`, `docs/AI_CONTEXT.md`, `docs/agent-protocol.md`, `docs/architecture/REPOSITORY_STRUCTURE.md`, `docs/governance/REPOSITORY_ORDER_POLICY.md`, `docs/governance/EXTERNAL_AGENT_STRUCTURAL_FIREWALL_V1.md`, `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json`, `docs/governance/NEXUS_OMEGA_TASK_ANCHOR_NORM_V1.md` sowie die aktuellen R21-Files und den R20-Checkpoint lesen.
- `REPOSITORY_ORDER_LAW_V1`: bestehende Pfade behalten. Öffentliche Forschung gehört nur in `research/r21/...`, Implementation nach gesonderter Lifecycle-Prüfung in passende `docs/schema/scripts/tests/validation/examples/r21`; keine Root-Dumps; Änderungen an der Repo-Struktur nur mit README+Struktur-JSON und Validator. Externe Agent-Actor-Allowlist bleibt leer.
- Eigene gemischte lokale Cursor-/App-Verzeichnisse und öffentliche Repo-Objekte nicht verwechseln. Originale unveränderlich und Read-only einfrieren. Aktueller PR #348 ist kein Hostinger-Deploy.
- Primär-Originalpaket R21 (25.023 Bytes, SHA oben) plus `MANIFEST_SHA256.json` unabhängig verifizieren. Bereits beobachtete `30/30` Tests sind Software-Negativ-/Positivfälle, **keine** reale OPPO-Messung.

### 2. G0 — Aktuelle OPPO-Identität, Session und Sensorhardware (read-only zunächst)
Beweise **jetzt**, nicht aus altem Chat: ADB/physische Geräte-ID (intern, im öffentlichen Return gekürzt), Hersteller, exaktes Modell (historisch `OPPO A74 / CPH2219`, NICHT ungeprüft übernehmen), Android-Build/API, aktueller Bootzeitbezug, aktives Paket (historisch `com.nexusomega.maps`, nicht ungeprüft übernehmen), APK-/App-Build-Version und Hash soweit zugänglich, USB/WLAN-ADB Zustand, Foreground/Background-Status und aktuelle App-Sensoraufnahmefunktion. Sensor-Inventar aus Android `SensorManager`/App: `TYPE_ACCELEROMETER`, `TYPE_GYROSCOPE`, `TYPE_MAGNETIC_FIELD`, optional `TYPE_LINEAR_ACCELERATION`, `TYPE_GRAVITY`, `TYPE_ROTATION_VECTOR`, `TYPE_GAME_ROTATION_VECTOR`, ggf. unkalibrierte Sensorvarianten. Je Sensor Name, Vendor, Android-Typ, Genauigkeits-/Kalibrierstatus, minDelay/maxDelay, maximaler Bereich, Auflösung, power, Reporting Mode, FIFO, angeforderte und tatsächlich beobachtete Abtastrate. Nicht jedes Telefon hat jeden Sensortyp. Nicht vorhandene Sensoren als `ABSENT` markieren, nie künstlich auffüllen.

Vor jeder lokalen App-Anpassung: bestehenden Quellstand, Running-App-Status, Backup, Schnittstelle und ausführbare Rückrollmöglichkeit ermitteln. Kein Wechsel zur Pixel-Lane.

### 3. G1 — Direkter physischer Datenpfad (WICHTIG: kein GET-Zwang)
Der zuvor erkannte Server-Endpunkt ist `WRITE_INGEST`, **kein** `R21_READONLY_GET`. Ein neuer GET-Service wird NICHT als Voraussetzung missbraucht. Nutze die Pfade in dieser strikten Priorität, sobald Originalbytes und Rechte vorliegen:

**A — Bereits vorhandene lokale Rohdaten der NEXUS-App:** Die App-eigene Export-/Protokollfunktion verwenden, vorhandene zeitgestempelte `SensorEvent`-Dateien unverändert exportieren und auf Windows lesen. Falls schon bestehende, eindeutig aktuelle Daten aus dem OPPO verfügbar sind, zuerst sichern und rehashen.

**B — Existierender App-Callback, aber kein lesbarer Export:** Minimalen diagnostischen `SensorEventListener`-basierten Rohdatenexport in der autorisierten NEXUS-App ergänzen. Nur notwendige App-Berechtigungen, keine Root-Rechte. Speichern in app-private Storage und über einen **explizit freigegebenen** SAF-Export, debugfähiges `run-as` (nur falls tatsächlich debuggable) oder einen auf `127.0.0.1` beschränkten lokalen Kanal/Alias via ADB-Forward übernehmen. Kein ungeschützter `exported=true` Provider, kein permanenter Hintergrund-Uploader, kein anonymer öffentlicher Port. Minimalinvasive Änderungen und Rollback vor Messung testbar halten.

**C — Bereits existierender privater HTTPS-Leseweg:** Nur wenn vorhanden, nachgewiesen, authentifiziert und durch Operator autorisiert, GET-only R21-Empfänger gegen ihn anwenden. Original HTTP-Response und Serverquelle mit Header-/Zeit-/Hashbeleg festhalten. Niemals `WRITE_INGEST` per GET aufrufen und den Fehlstatus als Gerätefehlfunktion interpretieren. Kein Hostinger-Write, um den Pfad zu erzwingen.

Ein echter Rohtrace ist ein **Android-Sensorevent auf dem physischen OPPO**; ein Simulationsfile, JSON-Testfixture, der CI-Status, ein Server-ACK, ein Filterquaternion oder eine symbolische Animation sind kein Rohsensorbeweis.

### 4. G2 — Messprotokoll auf dem echten OPPO, operativ durchführen
**Minimaler akzeptabler Messlauf** (auch ohne körperliche Bedienung ausführbar): echte OPPO-App starten oder bereits gestartete Listener gezielt übernehmen; ein eindeutiges `session_id`, `boot_session_id`, Sensor-Provenienz und Start-/Endzeitpunkte setzen; mindestens 60 Sekunden **ruhende, stabile Tischlage** mit Accelerometer und Gyroscope als echte Originalevents aufzeichnen. Ein belegter tatsächlicher Hardware-Lauf mit gültigen Originalwerten hat Vorrang vor großem, aber nur synthetischem Forschungsumfang.

**Erweiterter wissenschaftlicher Lauf**, wenn kontrolliert tatsächlich möglich, mit eindeutig getrennten realen Segmenten und Eventmarkern:
- S0: 120 Sekunden stationär, Bildschirm nach oben (Bias, Gravitation, Allan-/Rauschvoranalyse; Temperatur sofern der Sensor tatsächlich liefert).
- S1: 60 Sekunden stationär in zweiter dokumentierter Geräteorientierung; nur bei tatsächlich physischer Positionsänderung, sonst `NOT_PERFORMED`.
- S2: 60 Sekunden kontrollierte, ruhige Drehung um eine dokumentierte Achse, Start-/Ende-Marker; keine geschätzte Winkelreferenz als physisches Ground Truth ausgeben.
- S3: 60 Sekunden langsame manuelle Kreisbewegungen oder Pendeln, nur bei real ausgeführter Bewegung.
- S4: 60 Sekunden reale natürliche Handbewegung oder Gehen mit fest montiertem/handgehaltenem Gerät; **Mount/Segment und Umgebung dokumentieren**. Keine gefährlichen oder erzwungenen Aktivitäten, keine klinischen Probandenexperimente.
- S5: 60 Sekunden erneute Tischruhe (Bias vor/nach Bewegung). Bei tatsächlicher Verfügbarkeit einen zweiten unabhängigen Gerätestart-/Aufnahmezyklus reproduzieren.

Ein Cursor ohne physischen Manipulator kann die App bedienen und Tischruhe real aufzeichnen; er darf keine bewegten Abschnitte als vollzogen behaupten. `MOTION_NOT_OBSERVED` und `NOT_PERFORMED` sind ehrlich, nicht ein Anlass für fingierte Bewegungen. Es ist KEIN menschlicher Ganzkörperversuch verlangt. Körpersegmentkopplung nur wenn real dokumentiert; bei Handhaltung `MOUNT=HANDHELD_UNCALIBRATED`, nicht `TORSO`.

### 5. G3 — Unverfälschtes Rohdatenformat und Zeitbasis
Für jede tatsächlich beobachtete `SensorEvent`-Instanz: 
- `run_id`, `session_id`, `boot_id`/Reboot-Identität, `seq_per_sensor`, `sensor_type`, `sensor_name`, `sensor_vendor`, `accuracy`, `event_timestamp_ns`, `values` als Original-Float-Tupel sowie Original-Sensorauflösung und Source-API; wann die App den Event empfing (separater Host-/Device-Marker).
- `TYPE_ACCELEROMETER`: [x,y,z] in **m/s²** inklusive Schwerkrafteinfluss; `TYPE_GYROSCOPE`: [x,y,z] in **rad/s**; `TYPE_MAGNETIC_FIELD`: [x,y,z] in **µT** (falls vorhanden). Geräteframe nach Android-Sensorbezug X=rechts, Y=oben, Z=aus Displayebene im Default-Portrait-Frame; nicht stillschweigend als Welt-/Körperachsen ausgeben. Kalibrierte/unkalibrierte Sensorquellen getrennt.
- Zeitstempel pro Sensor monoton und im `SystemClock.elapsedRealtimeNanos()`-Zeitbereich; keine naive Interpretation als Unix-UTC. Optional Clock-Anchor mit `elapsedRealtimeNanos` + korrespondierender UTC-Zeit, Unsicherheit und Host-Uhr; keine Schein-Nanosekunden-Synchronität. Zwischen Sensorarten dürfen Ereignisse ineinander verschachtelt sein; **monotone Prüfung je Quelle/Sensor**, nicht global pro JSON-Zeile.
- Falls die App auf Android API 31+ zielt, gelten bei `SensorEventListener` gewöhnlich 200-Hz-Limits ohne `HIGH_SAMPLING_RATE_SENSORS`; Rate nicht erzwingen und keine Berechtigungen heimlich aufweiten. **Tatsächliche** Hz aus `median(1/Δt)` je Sensor bestimmen, Ausfälle und Jitter aus realen Zeitstempeln berechnen.
- `raw.sensor.jsonl` oder äquivalentes Binärformat als immutable Originaldatei. Separater `metadata.json`, `markers.json`, `clock_anchors.json`, `quality.json`; ggf. nur abgeleitete/gefilterte Daten in neuer, klar markierter Datei. Keine Originalwerte nachträglich ändern, runden oder sortieren, ohne unveränderte Datei zu behalten.

### 6. G4 — Qualitätskontrolle mit messbaren Kriterien
Primärgate `PHYSICAL_SOURCE_RECEIVED`: mindestens ein Original-Accelerometer- und Gyroscope-Event vom belegten OPPO, korrekte Android-Quellenidentität, private Originalbytes mit SHA-256 und glaubwürdigem Zeitstempel. **Nicht gleich** wissenschaftlicher READY-Status.

Forschungsqualitätsgate `RAW_IMU_RESEARCH_USABLE`: mindestens ein zusammenhängender, physisch belegter 60-s-Abschnitt mit Accel und Gyro; exakte Dauer, beobachtete Frequenz, Events pro Sensortyp, per-stream monotoner Zeitbezug, endliche Werte und nachvollziehbares Datum/Bootstatus. Zielwert ≥25 Hz Median pro Kernsensor (kein erfundener PASS, geringere echte Raten als `PARTIAL_WITH_CAVEATS`); >5 % markierte Data Gaps oder Device-/App-Wechsel führen zu Caveats, nicht stiller Interpolation. Stationärer Betrag des Accelerometers in plausibler Nähe zu 9,81 m/s² ist eine **Plausibilitätskontrolle**, keine starre globale Qualitätsgarantie; Gyro-Ruhe und Bias getrennt bewerten. Signalkanal-Drift, unkalibrierter Sensor, Sättigung, Magnetstörung, Duplicate Sequences, Zeitstempelkorruption und App-Dropout dokumentieren.

Widersprüchliche oder unvollständige Messwerte werden **unverändert als Original** eingefroren und zusätzlich im separaten Quality-Report auffällig markiert. Fehlende Realität ist kein Nullsignal. Defekter oder leerer Abruf wird als `SOURCE_GAP` geführt, niemals durch Testfixtures ersetzt.

### 7. G5 — Wissenschaftlicher Basistest, nur soweit Daten vorhanden
Führe zunächst deskriptive Rohdatenanalysen aus: je Sensor Samplingrate (Median/Perzentile), Intervalle/Dropouts, Dimensions- und Normverteilung, Beschleunigungsruhestandard, Gyroskop-Offset/Magnetfeldniveau, Zeitbasis-Vergleich, gegenseitige Verzögerungen. Dokumentiere exakte Formeln und Denominatoren, Unsicherheit und Test-Labels.

Nur **nach** Quellakzeptanz: VQF 6D, ggf. 9D bei vorhandener gesicherter Magnetfeldquelle, sowie vorhandene UKF/SR-UKF auf identischem Datenfenster als **Filterausgaben** vergleichen. Quaternion-Norm, Signum-Invarianz bei Vergleich, relative Orientierung, Drift während Ruhe und bekannte Störungen auswerten. Ohne unabhängiges optisches/externes Orientierungs-Ground-Truth **KEINE absolute Filtergenauigkeit, NEES-Wahrheit oder Ganzkörperkinematik behaupten**. NIS/NEES nur bei tatsächlich vorliegendem korrekt definiertem Innovations-/Kovarianzmodell. Das R18-männliche anatomische Referenzmodell bleibt räumlich und epistemisch getrennt: Ein Gerät auf dem Tisch ist **keine Messung der Körperhaltung**.

### 8. G6 — Reproduzierbare Negativ- und Positivkontrollen
Zusätzlich zu den vorhandenen 30 Softwaretests mindestens folgende 12 adversariale Fälle prüfbar dokumentieren: fremdes Device/Pixel-Role; App-/Build-ID geändert; reboots/Boot-ID drift; monotonic timestamp reversal; duplicate seq; null/nonfinite axes; unit rad↔degree; accel g↔m/s²; missing gyro; exaggerated sample-rate claim; magnetically contaminated segment; out-of-order mixed sensor stream fälschlich als global invalid; korruptes Input-Hash; unautorisierte public raw upload; `WRITE_INGEST` als GET missbraucht. Positive Kontrollen: echte valide Acc/Gyro-Events, echte stationäre Gravitätsnorm, echter Zeitanstieg, deterministischer lokal wiederholter Readback, unveränderte SHA bei Copy, per-source monotonic interleaving, korrekt markierte fehlende Magnetquelle, korrektes `PARTIAL_WITH_CAVEATS`, gültiger Clock-Anchor mit Unsicherheit, sicherer offline revoke/stop und Rollback. Erwartetes Ergebnis und tatsächlich beobachtetes Ergebnis getrennt führen; hypothetische Positivkontrollen als `NOT_EXECUTED`.

### 9. G7 — Datenschutz, Atomizität, Beweis und Rückbau
**Private custody** der Rohbytes: lokal operatorautorisierter Pfad unter `C:\omega_bridge\NEXUS_OMEGA_TRANSFER\10_TO_AXIOM\...` oder bereits vorhandenem privaten Evidence-CAS. Schreibschutz der Originaldatei, SHA-256, Bytezahl, UTC-/Monotonic-Marker und unveränderlicher Header; Hashmanifest detached (ohne Selbsthash). Privater Datentransfer über vorhandenen genehmigten Nexus-Kanal; wenn einer fehlt, kein improvisierter öffentlicher URL-/GitHub-Upload. Keine IMU-Rohdaten, Seriennummern, exakten Standorte, Tokens, Kontakte oder persönlichen Health-Metadaten in öffentliche PRs/WWW. Nur anonymisierte Statistik + Hashreferenz, sofern freigegeben.

Nach Messlauf stoppt Cursor **nur die selbst gestartete** Aufnahme und bestätigt, dass die App in ihren Ausgangszustand zurückgekehrt ist. Bestehende andere Aufnahme-/Continuity-Dienste nicht beenden, ungesicherte Sessions nicht überschreiben. Bei lokalen App-Patches: Dateidiff, Tests, Apk-Build/Signature, Backup- und Rollbackbeleg. Verzeichnisse, Traces, ZIPs nicht in Repo-Root ablegen; Original-R18/R19/R20 unverändert.

### 10. Pflicht-Return (sofortiger Abschluss statt weiterer theoretischer HOLD-Zyklen)
Ablage als geschlossenes, versioniertes Cursor-Paket plus `.sha256`, mit **nur tatsächlich notwendigen Transferdateien**:
1. `00_EXECUTIVE_VERDICT.md` — physische Rohdaten ja/nein mit exakter Zahl, Modell, Dauer, Quellenstatus, restriktiven Caveats.
2. `01_DEVICE_AND_APP_CENSUS.json` — Gerät/Android/Build/Sensoren, App-State und verifizierte Provenienz (public-safe redacted derivation separat).
3. `02_SOURCE_ACQUISITION_AND_CHANNELS.md` — welcher A/B/C-Datenpfad tatsächlich benutzt, exakte Herkunft und warum anderes nicht verwendet.
4. `03_RAW_SENSOR_ORIGINAL.jsonl` — **privat**, unveränderte Original-Events, falls tatsächlich aufgenommen; niemals leeres oder synthetisches Stubfile als Original. Separate raw manifest may reference private CAS object instead of placing raw bytes into public package.
5. `04_SESSION_MARKERS_AND_CLOCK.json` — realer Ablauf, Hardwaremontage, Clock Anchors, Uncertainty und Bewegungsklassen (NOT_PERFORMED explicit).
6. `05_DATA_QUALITY_AND_FAILURES.json` — real berechnete Count, Hz, Gaps, NaN, Bias und Fehler; keine erfundenen Messwerte.
7. `06_SENSOR_FILTER_COMPARISON.md` — nur tatsächlich ausgeführte VQF-/UKF-Tests, sonst NOT_EXECUTED.
8. `07_NEGATIVE_CONTROLS_AND_RECEIPTS.md` — erwartete vs. reale Outputs, Source- und App-/Buildprovenienz.
9. `08_ROLLBACK_AND_INTEGRITY.md` — keine Kollateralschäden, App-Gesundheit/Backups.
10. `09_AXIOM_RECEIVER_HANDSHAKE.txt` + `MANIFEST_SHA256.json` + ZIP/.sha256 mit kompletten Bytes; detached, self excluded.

**Executive Entscheidung anhand Evidenz statt Zeitdruck:**
- `PASS_C1_PHYSICAL_OPPO_SOURCE_CAPTURED` nur bei wirklich vorhandenen, begründbar OPPO-zugeordneten Acc-/Gyro-Originaldaten und erfolgreichem Private-Receiver-Hash.
- `PASS_WITH_CAVEATS_C1_PARTIAL_PHYSICAL_CAPTURE` bei echten, aber wissenschaftlich eingeschränkten Datensätzen, mit konkreter Ursache.
- `HOLD_SCOPED_SOURCE_GAP` wenn physische Daten trotz App-Zugriff nicht erhoben werden konnten — genau welche Hardware-/App-/Android-Sandbox-Eigenschaft und welche nächste *konkrete* Behebung notwendig ist. Keine erneute generische R21-Forschung als Ersatz.
- `MEDICAL_VALIDITY=NO`, `BODYTWIN_VALIDATED=NO`, `CLAIM_PROMOTION=NO` selbst bei erfolgreichem physischem IMU-Capture.

### 11. Closing Status-Vorlage (keine Werte vor Ausführung ausfüllen)
```text
OBJECT = NEXUS_OMEGA_CURSOR_R21_OPPO_PHYSICAL_IMU_CAPTURE_RETURN_20261109_R0
STATE = <ACTUAL_EVIDENCE_BASED_STATE>
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
OPPO_IDENTITY = <ACTUAL_VERIFIED_MODEL/APP/BUILD>
OPPO_RAW_ACCEL_EVENTS = <REAL_COUNT_OR_0>
OPPO_RAW_GYRO_EVENTS = <REAL_COUNT_OR_0>
OPPO_RAW_MAG_EVENTS = <REAL_COUNT_OR_ABSENT>
RAW_SESSION_DURATION_SEC = <MEASURED_OR_NOT_EXECUTED>
OBSERVED_SAMPLING_HZ = <PER_SENSOR_ACTUAL>
RAW_ORIGINAL_SHA256 = <ACTUAL_OR_NA>
R21_SOURCE_PATH = <A|B|C|NONE>
WRITE_INGEST_AS_GET = NO
PIXEL9A_FEMALE = RESERVED_NO_START
R18_R19_R20 = PRESERVE
GITHUB_MERGE = NO
HOSTINGER_WRITE = NO
BODYTWIN_VALIDATED = NO
RECEIVER_ACK = PENDING_AXIOM_INDEPENDENT_REHASH
```

### 12. Verbindliche Android-Erstquellen und wissenschaftliche Referenzen
- Android SensorEvent: https://developer.android.com/reference/android/hardware/SensorEvent
- Android Sensor Limits: https://developer.android.com/develop/sensors-and-location/sensors/sensors_overview
- AOSP Sensor Types: https://source.android.com/docs/core/interaction/sensors/sensor-types
- VQF Referenz: https://vqf.readthedocs.io/ ; https://doi.org/10.1016/j.inffus.2022.10.014
- R21 Forschungslage: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/348

**TERMINAL DIRECTIVE:** Cursor handelt jetzt innerhalb dieses autorisierten OPPO-App-Sensorscopes. Priorität ist der erste **unveränderte, echte, reproduzierbar gerätegebundene physische Beschleunigungs- und Gyrodatensatz**, nicht eine weitere vorgeschaltete Designrunde. Sobald ein solcher Trace existiert: Originalbytes sofort privat versiegeln, reale Quality-Gates ausführen und an AXIOM übergeben. Bei tatsächlichem Hardwareblocker diesen mit Befehls-/App-Belegen konkret ausweisen und die bereits erreichten physischen Beweise erhalten. R18/R19/R20 nicht überschreiben.
