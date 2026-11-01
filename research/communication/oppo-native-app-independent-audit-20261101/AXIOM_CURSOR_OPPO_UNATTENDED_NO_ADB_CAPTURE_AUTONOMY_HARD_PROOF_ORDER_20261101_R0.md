# NEXUS OMEGA · AXIOM → CURSOR
## KANONISCHER MAXI-AUFTRAG — UNATTENDED OPPO SENSORAUFNAHME OHNE AKTIVE ADB-VERBINDUNG
### 01.11.2026 · P0–P10 · C1_DESCRIPTIVE_ONLY

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_OPPO_UNATTENDED_NO_ADB_CAPTURE_AUTONOMY_HARD_PROOF_ORDER_20261101_R0
PARENT = NEXUS_OMEGA_AXIOM_OPPO_NATIVE_APP_AND_COMMUNICATION_GATE_INDEPENDENT_ADJUDICATION_20261101_R0
SOURCE_ADJUDICATION_COMMIT = ed1f0b24edc3c67e29b7714c827d05aafda7bd83
SOURCE_TASK_ANCHOR_COMMIT = 5c25c6ce9bed895ed76f05b8c4fdeca53426af14
SOURCE_OPPO_RETURN_COMMIT = 77f26c0d1cfaf18b9c1addfac2e47444c614478a
SOURCE_PR263 = OPEN_NOT_MERGED
SOURCE_PR266 = OPEN_NOT_MERGED
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
OPERATOR_ACTION_DURING_RUN = NONE
CURSOR_TASK_CLASS = LOCAL_SAFE_REAL_OPPO_INSTRUMENTATION_AND_EVIDENCE
DEVICE = EXISTING_AUTHORIZED_OPPO_A74_CPH2219_ONLY
ANDROID_APP = com.nexusomega.maps / current installed VC11 (VERIFY)
OPPO_WLAN_ADB = AUTHORIZED_FOR_SETUP_AND_POST_RUN_READBACK_ONLY
PIXEL9A = NOT_ADMITTED_NO_DEVICE_ACTION
PUBLIC_WRITE_API = OFF
REAL_EXTERNAL_AGENT_ACK = NOT_ESTABLISHED
GLOBAL_CUTOVER_ACTIVE = NO
FRAMEWORK_V1 = CLOSED_LIVING
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## A. Fragestellung und Anspruchsgrenze

Falsifiziere die These: Die bestehende native NEXUS-Android-App braucht während des gesamten tatsächlichen IMU-Aufnahmezyklus weder eine ADB-Verbindung noch einen Operator-Tastendruck, um zu beginnen, zu messen, zu stoppen und die lokalen Segmente sicher zu versiegeln.

Dieser Auftrag ist bewusst strenger als die bisherige P7/NO_ADB-Quittung. Der Operator erklärt ausdrücklich, während des gesamten Vorgangs keinerlei manuelle Aktion auszuführen. Cursor übernimmt vollständig Vorbereitung, automatisiertes Setup, Abtrennung, hostseitige Beweisführung, Wiederverbindung und Quellenprüfung. Es wird keine stillschweigende Berührung, Freigabe, Entsperrung oder Zustimmung des Operators vorausgesetzt.

Die korrekte Behauptung bei erfolgreichem Test lautet:
  SENSOR_SESSION_START_STOP_SEAL_WITHOUT_ACTIVE_ADB = DEVICE_REPORTED_AND_SOURCE_BOUND_C1
NICHT:
  ALL_ANDROID_FUNCTIONALITY_NEVER_REQUIRES_ADB = PROVEN
  ARTIFICIAL_AGENT_IDENTITY = ATTESTED
  EXTERNAL_TRANSPORT_ACK = ESTABLISHED
  PIXEL_TWIN = ACTIVATED

Auch ein erfolgreich protokolliertes Testscript ist nur ein C1-Beleg auf definiertem Gerät/Build. AXIOM kann über GitHub später Bytes und Methoden unabhängig nachprüfen; AXIOM kann aus Textbelegen allein nicht den physischen Funkzustand direkt beobachten.

## B. Gesicherte Ausgangsbelege und offene Defekte

PARENT PR #263 enthält ein tatsächlich vom Github-Eigentümerkonto veröffentlichtes Return und drei via GitHub-API belegte Public-Safe-Canaries. Die installierte OPPO VC11 App, die No-ADB-Messung mit zwei Segmenten und 28/28 JVM Tests sind CURSOR-REPORT_LEVEL_C1; unabhängige APK-/Rohdaten-Rehash- und vollständige Android-Source-CI fehlen.

AXIOM hat ALLE 26 originalen GitHub-Blob-Dateien gegen SHA256SUMS geprüft: nur 13/26 MATCH, 13/26 MISMATCH. Besonders NO_ADB_OPERATIONAL_TEST.txt und P8_FALSIFICATION.txt weichen im Original-GitHub-Bytehash ab. Die Originalquellen, SHA256SUMS und alten Ausführungsbelege bleiben unverändert. Ein neuer sauberer Test darf einen neuen PASS erbringen, aber NIEMALS einen historischen 26/26-PASS behaupten.

P8 beschreibt weiterhin ein Risiko: falsch geschriebene STOP-Intent-Aktion kann in den Startpfad fallen. Vor neuem Experiment eine tatsächliche Fail-Closed-Logik für unbekannte Actions nachweisen oder nur den geprüften korrekten Pfad verwenden und die separate Fix-Bedingung explizit als HOLD führen. Keine ungesicherte Release-Promotion.

Die lokal vorhandenen Android-Quellen, 24-Zeilen-Differential und ungepushte S1–S5-Modifikationen dürfen keinesfalls durch Checkout/reset/clean verloren gehen. Die öffentliche EVIDENCE PR ist kein GitHub-Quellcode-Build-Beweis.

## C. Leitdesign: Nachweis durch Geräte-eigenen zeitversetzten START und STOP

BEVOR ADB getrennt wird, richtet Cursor über den bereits autorisierten Entwicklungskanal eine klar sichtbare, kontrollierte TESTSESSION ein. Verwende bevorzugt vorhandene Funktionen. Falls noch nicht vorhanden, implementiere minimal, nur innerhalb der existierenden App, eine versionierte, test-spezifische lokale Aufnahme-Routine; keine neue Framework-/Agentenarchitektur und keine unbekannte App von Dritten.

Die Routine muss eine VISIBLE USER-APP-ACTIVITY verwenden und bei vorhandener gültiger App-Sensor-Einwilligung lokal VOR dem Disconnect einen ordnungsgemäß gestarteten, sichtbaren Foreground-Service ARMED betreiben (noch keine Registrierung der IMU-Leseoperation). Dadurch muss der Foreground-Service NICHT erst aus einem möglicherweise verbotenen Android-Hintergrundzustand gestartet werden. Die App kann anschließend anhand eigener monotoner Android-Uhr den eigentlichen Sensor-START auslösen; der durch Cursor über das Android UI angestoßene ARMED-Zustand ist eine dokumentierte Testvorbereitung und keine versteckte Zustimmung.

Sicherer deterministischer Zeitablauf als technische Zielkonfiguration (nicht als vorgetäuschte tatsächliche Laufzeit):
  T0: Native Activity sichtbar, nur bereits erteilte Berechtigungen, Countdown über App-Oberfläche ARMED.
  T0 bis T0+90 s: Service bleibt im ARMED-Zustand; Sensoren NICHT aktiv.
  HOST: ADB-Verbindung vollständig trennen und Verbindungszustand vor T_start beweisen.
  T_start >= 90 s nach ARMED: Sensorregistrierung IN DER APP, ohne ADB-/Host-Trigger.
  T_stop = T_start + 7 Minuten: auto-stop IN DER APP, ohne ADB-/Host-Trigger.
  T_seal: jedes Gzip-Segment/Sidecar/Manifest lokal atomar versiegeln, Queue-Status SEALED_LOCAL.
  T_reconnect: Host verbindet sich erst nach gemeldeter oder konservativ erwarteter Seal-Deadline PLUS Sicherheitszuschlag erneut; niemals früher, um den NO-ADB-Nachweis nicht zu verfälschen.

Cursor darf 90 s/7 min nur nach technischer Eignungsprüfung ändern und muss tatsächliche Parameter protokollieren. Keine Zeitschätzung als Messbeleg. App-Timeout muss lokale Files sicher schließen; bei Crash oder Timerfehler => FAIL_CLOSED, Preserve/Pending, kein erfundener PASS.

Die App-Laufzeit darf keine im ADB-Shell-Prozess gehosteten Sensorleser, Unix-/logcat-Pipes, USB-Tethering, Host-Clock-Watchdog als Aufnahmetrigger, Desktop-WebSocket, Remote-Scheduler, ADB-Port-Forwarding oder fremde Shell-Kommandos benötigen. Der OPPO darf auf unverändertem WLAN sein; das ist kein offline-netzunabhängiger Telemetrietest. Während des Aufnahmefensters ist ADB vollständig getrennt, auch bei App-Wiederanlauf.

Der geplante STOP darf nur über interne App-Codepfade ausgeführt werden. KEIN ADB-STOP, KEIN nachträglicher Host-Fallback als gleichwertiger Erfolg. Die Activity muss unbekannte oder falsch geschriebene Actions grundsätzlich ignorieren/ablehnen, niemals auf START fallen.

## D. Ausführung P0–P10 ohne manuelle Operatorinteraktion

P0 · READ-ONLY SOURCE / GEFAHRENPRÜFUNG.
- Aktuelles lokales Android Repo, HEAD, dirty S1–S5, Version, Signature, APK hash, vorhandene wissenschaftliche Sessions, Erreichbarkeit und ADB-Serial source-exakt feststellen.
- Vorinstallation/Datenerhalt/Restore nur mit tatsächlich zugänglichem Mechanismus belegen; keine unbewiesenen ADB-Backup-Versprechen.
- Keine neue Pairing-/Android-Einwilligungsaktion des Operators. Falls Permission/Unlock/Systemdialog erscheint, keine automatische Umgehung oder blindes UI-Klicken; genau die betroffene Teilfähigkeit HOLD, restliche sichere Arbeiten fortsetzen.
- Noch offene GitHub SHA-Abweichungen als UNRESOLVED_PAST_EVIDENCE erhalten. Keine Ausweitung auf die Pixel-Kette.

P1 · APP ACTION SAFETY.
- SOURCE-AUDIT des LaunchActivity Action-Matchings; unknown ACTION muss fail-closed bleiben und darf weder Sensorerfassung starten noch alte Daten verändern.
- Isolierte instrumentierte Negativtests; wenn ein Fix notwendig ist, nur nach geprüfter Daten-/Signatur-/Rollback-Kette risikoarm installieren. Kein pm clear, kein uninstall, kein root, kein Factory Reset, keine Neuinstallation mit Signaturkonflikt.
- Falls sichere neue Version nicht herstellbar/prüfbar, STOP_DEVICE_MUTATION, dokumentiere SOURCE_GAP; kein unsicheres Gerät manipulieren.

P2 · IN-APP UNATTENDED SEQUENCE.
- Reuse existierenden IMU ForegroundService/SensorManager. Falls notwendig, implementiere kleine zeitversetzte ARM/START/STOP/SEAL-Funktion unter sichtbarer App-Aktivität und versioniertem Testmodus mit begrenzter Dauer; KEINE neuen privilegierten Rechte/Accessibility.
- App-Audit-Events: SESSION_ARMED, HOST_DISCONNECT_TARGET, SENSOR_START, SENSOR_STOP_REQUESTED, SENSOR_UNREGISTERED, SEGMENT_SEALED, PACKAGE_SEALED, RUN_COMPLETE; jeweils device elapsedRealtimeNanos, wall-clock UTC-Anchor und Unsicherheitsmetadaten, seq, event digest, source code/build hash und präzise Triggerklasse.
- Falls App nicht native autopause/autostop leisten kann, KEIN unehrlicher Ersatz per hostseitigem ADB-Stop. HOLD_NO_NATIVE_AUTOSTOP.

P3 · HOST SETUP UND DISCONNECT.
- Ausschließlich einen überprüften autorisierten OPPO A74 CPH2219 als ADB-Ziel wählen (private Serial/IP niemals in GitHub). USB oder zusätzliche aktive ADB-Sitzungen/Clients ausschließen, soweit überprüfbar.
- Cursor startet genau EINE Testsession über die sichtbare native Activity vor der Abtrennung. Jedes außerhalb der App liegende ARM-Skript und dessen Ende markieren.
- Hostside PowerShell-Command/Network Audit und getrennte Zeitstempel append-only führen; ADB-Gerätecheck vor Disconnect, adb disconnect auf EXAKTE autorisierte Serial, anschließend hostseitig ohne ADB-Aufruf den Verbindungsabbruch dokumentieren. Kein adb devices Polling, Logcat, mDNS-Reconnect, file pull, shell am, am force-stop, Testcommand, Host-Agent-Trigger und keine ADB-CLI zwischen T_disconnect und T_reconnect.
- Passive Windows-Socket/Prozess-Inspektion zulässig, solange sie keine neue Geräteverbindung erzeugt. Monitoring-Skript darf KEINE ADB-Kontrollfunktion haben. Wenn ADB ungewollt automatisch reconnectet oder USB angeschlossen ist, TEST_INVALID_NO_ADB.

P4 · UNBEAUFSICHTIGTE GERÄTESESSION.
- OPERATOR_INPUT_EVENTS = NONE; Cursor darf während des gesamten Fensters weder manuelle Geräteinteraktion erwarten noch fremde Android-Einstellungen modifizieren.
- Eigener Android-Scheduler/ForegroundService betreibt ARMED→START→CAPTURE→STOP→SEAL. Nutzereinwilligung und Notification müssen bereits im legitimen Preflight vorhanden sein. Kein versteckter Hintergrundstart, keine neue Berechtigungsvergabe.
- App läuft mit ihrem eigenen Speicher; kein externer Host-Eingriff. Misserfolg bei System-Kill/Doze wird dokumentiert und NICHT durch nachträgliche ADB-Kommandos kaschiert.

P5 · NACHLAUF UND RECONNECT.
- Host wartet mit autonomem Ablaufskript auf konservativ definierte Abschlusszeit + Puffer, ohne zwischendurch ADB-Verbindung. Danach ein einziger klar protokollierter automatischer adb connect mit bestehender legitimer Pairing-Information (nicht in Belegausgabe kopieren).
- Wenn Reconnect fehlschlägt, ursprüngliche private Dateien nicht löschen; recoverable HOLD, keine manuellen Aufgaben erfinden. Erneuter Versuch nur begrenzt und ohne Geräteeinstellungsänderungen.
- Host erfasst NACH dem Reconnect über run-as nur nach zulässigem App-Debugzugriff die bereits von App erzeugten finalen Artefakte und Auditlogs; keine ADB-getriggerte Nachversiegelung und keine Änderungen an Quelldaten.

P6 · DOPPELTE ORIGINALE HASH-BINDUNG.
- Originalgzip, Sidecar, Manifest und Paket im privaten OPPO-/Hostbereich jeweils SHA256, Dateilänge, Session/segment id, Timebase und Recordanzahl bestimmen und unabhängig mit den device-seitigen vorab versiegelten SHA-Werten vergleichen.
- Ein zweiter selbständiger Host-Hasher (unabhängiger Codepfad und Lauf) soll alle abgeholten Bytes prüfen. Gleichheit ist BELEG DER UNVERÄNDERTHEIT BEIM AUSLESEN, nicht Wahrheitsbeweis von Sensorwerten. Rohdateien nicht öffentlich posten.
- Vollständiges neu erzeugtes öffentliches Evidence-Paket bytegenau serialisieren und VOR dem GitHub-Push final rehashen; nach Push exakten 40-hex Commit neu fetch+hash. Kein BOM/CRLF-Drift und kein erneut behaupteter 26/26-Match ohne Prüfergebnis.

P7 · INVARIANTEN UND NEGATIVTESTS.
- N01 No ADB before native SENSOR_START: app event times after host disconnect, mit angegebener Clock-Skew-Grenze. Wenn Uhrvergleich nicht sauber kalibriert, NOT_ESTABLISHED statt PASS.
- N02 No ADB during entire SENSOR_START..PACKAGE_SEALED: Host-Audit ohne ADB Calls/Verbindung, deviceseitige Events alle innerhalb des Fensters. Nur dokumentierte Beweisstärke, keine allumfassende physische Absenzbehauptung.
- N03 No ADB START / STOP / SEAL triggered: Event cause = APP_INTERNAL; keine shell/service command requests nach Host Disconnect.
- N04 Unbekanntes/falsches STOP-Intent darf NICHT STARTEN (getrennte sichere Negativprobe vor eigentlichem Lauf).
- N05 Zero operator input: Skriptlog und keine eingeplanten User-Clicks/Prompts. Keine Behauptung, dass alle zukünftigen App-Läufe ohne manuelle Zustimmung laufen dürfen.
- N06 Sensorwerte & Zeitbasis: acc und gyro count > 0, monotone Timestamps je Sensor, nichtnegative Laufzeit, Samplingintervalle und Lücken ehrlich auswerten; keine erwartete fixe 100Hz-Zahl erfinden.
- N07 Auto-stop and local seal ohne Host/ADB; Korrekte Gzip- und Paket-Hash-Referenzen, kein nachträglicher hostseitiger Abschluss.
- N08 Data preservation: ältere Oppo Segmente und Sessionindex unverändert; neue Daten nur append-only, keine Duplicate ID.
- N09 Kill Switch / Permission denied / unrecoverable errors lead to safe HOLD, never secret bypass.
- N10 Keine Netzwerk-Sensorübertragung, kein public WRITE, keine App-GitHub-Fremdidentität.
- N11 PAST_RETURN_HASH_MISMATCH_13_OF_26 bleibt ausdrücklich OPEN; neuer Proof beginnt separate Version.
- N12 Re-run nach Möglichkeit zweiten unabhängigen vollständigen Prozessdurchlauf. Wenn nur ein echter Lauf möglich ist, SINGLE_RUN_C1, keine reproduzierbare Mehrfachvalidierung behaupten.

P8 · ABNAHME / BEWEISKLASSEN.
Abnahmeklassen streng getrennt:
  TEST_PREP_ARMED_WITH_ADB = TRUE
  ACTUAL_SENSOR_START_AFTER_ADB_DISCONNECT = PASS_OR_FAIL_OR_NOT_ESTABLISHED
  ACTUAL_SENSOR_STOP_WITHOUT_ADB = PASS_OR_FAIL_OR_NOT_ESTABLISHED
  ACTUAL_LOCAL_SEAL_WITHOUT_ADB = PASS_OR_FAIL_OR_NOT_ESTABLISHED
  SENSOR_DATA_BYTES_MATCH_AFTER_RECONNECT = PASS_OR_FAIL_OR_NOT_ESTABLISHED
  INDEPENDENT_RUNNING_APP_WITHOUT_ANY_ADB_SETUP_EVER = NOT_CLAIMED
  NO_HUMAN_OPERATOR_ACTION_DURING_TEST = YES_IF_EXECUTION_LOG_PROVES
  GH_OWNER_ONLY_ACK = NOT_A_DEVICE_RECEIVER_OR_EXTERNAL_AGENT_ACK

Ein PASS_NO_ACTIVE_ADB_SESSION gilt nur wenn alle Kernbedingungen stimmen. Kein PASS aus einem fehlenden runtime_status.json, einem bestandenen Mock-Test, 8/8 EVIDENCE CI, einem Gzip SHA-Claim oder einer nachträglich ausgeführten Stop-Activity.

P9 · QUELLEN / KANONISCHER HANDSHAKE.
Ein source-safe GitHub-only Return auf einem neuen scoped PR/Branch; privates OPPO-Rohmaterial ausschließlich in dem dafür berechtigten privaten Kanal. Public-Safe Daten nur: pseudonymes Gerät, App-Version/Codecommit, Eventtypen, relative Zeitdifferenzen, Sample Counts, Bytes + SHA der privaten Quelldateien (nicht Dateien selbst), Hash Vergleichsergebnis, skriptbasierte Host-Audit Befunde, Fehler-/Wiederaufnahmeklassen, mit geschwärzten Debug Netzwerk/Device-IDs.
APPEND_ONLY neue Originale + SHA256SUMS mit tatsächlichem Rehash, CI Logs, Task Anchor Norm V1, GitHub-Ref, tatsächliche Testvorgangsdauer und Original-Eventledger. Alte 13 HASH_MISMATCH nicht verschweigen.
Keine neuen öffentlichen API-Write-Endpunkte, kein Hostinger-Deploy, kein PR-Merge ohne Owner-Review.

P10 · TERMINAL UND NÄCHSTE GRENZE.
  SUCCESS: genau dieser OPPO-App-Build hat START, CAPTURE, STOP, SEAL in dem geprüften Fenster ohne aktive ADB-Kontrollverbindung durchgeführt. Weitergehende App- und Kommunikationsautonomie, Android-Release-Reproduzierbarkeit und Pixel9a bleiben eigene unabhängige Nachweise.
  FAIL: objektive Testverletzung mit unveränderter Session-/Host-Evidenz und explizitem Reparaturscope.
  HOLD: fehlende legitime Android-Einwilligung, nicht sichere Debug-APK-Installation, fehlende In-App-AutoStop-Funktion, USB/ADB Autoreconnect, beschädigte Originale, Datenzugriff nicht legitim. Operator darf während dieser Durchführung nicht benötigt werden; kein verdeckter Workaround.

## E. OPERATOR UNATTENDED: KEINE INTERAKTION

OPERATOR_PHYSICAL_INPUT = NONE
OPERATOR_APP_TAP = NONE
OPERATOR_PERMISSION_DIALOG = NONE
OPERATOR_ADB_RECONNECT = NONE
OPERATOR_FILE_COPY = NONE
OPERATOR_PASSWORD_OR_CODE_DISCLOSURE = NONE

Falls etwas davon nötig wird, stoppe NUR den betreffenden Versuch und melde den tatsächlichen technischen Blocker. Keine Umgehung von Android-Sicherheits- oder Einwilligungsmechanismen.

## F. Canonical Return

RETURN_OBJECT = NEXUS_OMEGA_CURSOR_OPPO_UNATTENDED_NO_ADB_CAPTURE_AUTONOMY_PROOF_RETURN_20261101_R0
PARENT_ORDER = NEXUS_OMEGA_AXIOM_CURSOR_OPPO_UNATTENDED_NO_ADB_CAPTURE_AUTONOMY_HARD_PROOF_ORDER_20261101_R0
SOURCE_APP_BUILD = EXACT_COMMIT_VERSION_SHA256_OR_LOCAL_SOURCE_HOLD
PREVIOUS_OPPO_DATA = PRESERVED_OR_FAIL
SESSION_ID = ACTUAL_PSEUDONYM
ARMED_ADB = TRUE_AND_DOCUMENTED
HOST_ADB_DISCONNECT_TIME = ACTUAL_PRIVATE_WITNESS
SENSOR_START_EVENT = DEVICE_MONOTONIC_AND_UTC_UNCERTAINTY
SENSOR_STOP_EVENT = DEVICE_MONOTONIC_AND_UTC_UNCERTAINTY
PACKAGE_SEALED_EVENT = DEVICE_MONOTONIC_AND_UTC_UNCERTAINTY
HOST_RECONNECT_TIME = ACTUAL_PRIVATE_WITNESS
HOST_IN_WINDOW_ADB_COMMANDS = ZERO_OR_FAIL
HOST_IN_WINDOW_ADB_CONNECTIONS = NONE_OBSERVED_OR_NOT_ESTABLISHED
OPERATOR_MANUAL_ACTIONS = ZERO
SEGMENTS = ACTUAL_COUNT_BYTES_SHA
SENSOR_ACC_COUNT = ACTUAL
SENSOR_GYRO_COUNT = ACTUAL
PRIVATE_BINARY_REHASH = ACTUAL_OR_NOT_ESTABLISHED
APP_SOURCE_REPRODUCIBILITY = ACTUAL_OR_HOLD
UNKNOWN_ACTION_FAIL_CLOSED = ACTUAL_OR_HOLD
ORIGINAL_RETURN_13_SHA_MISMATCH = PRESERVE_UNRESOLVED
PUBLIC_DEBUG_IDS = REDACTED
EXTERNAL_ACK = NOT_ESTABLISHED
CUTOVER_ACTIVE = NO
PIXEL9A = NOT_ADMITTED_NO_ACTION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = AXIOM_INDEPENDENT_UNATTENDED_OPPO_CAPTURE_SOURCE_AND_TIMEBASE_ADJUDICATION

## G. Offizielle technische Referenzen

Android ADB: https://developer.android.com/tools/adb
Android Foreground-Service Start: https://developer.android.com/develop/background-work/services/fgs/launch
Android Hintergrundrestriktionen: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start
Android SensorEvent Timebase: https://developer.android.com/reference/android/hardware/SensorEvent
Android Background / Energie: https://developer.android.com/topic/performance/background-optimization

TERM: EXECUTE bounded safe OPPO unattended measurement on actual device NOW. No human action, no fake PASS, no silent data modifications, no Pixel activation, C1 only.
