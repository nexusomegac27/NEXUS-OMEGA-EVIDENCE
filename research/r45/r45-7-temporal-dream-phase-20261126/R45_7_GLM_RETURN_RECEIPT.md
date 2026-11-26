# R45-7 · GLM Return R1 — Übergabestatus (append-only, kein Merge, kein Dispatch)

```
OBJECT = AXIOM_R45_7_GLM_RETURN_R1
RETURN_CHANNEL = GITHUB_ONLY (ZIP + .sha256 + Manifest im ZIP; Receiver-Rehash beim Empfänger)
BASE_COMMIT = 332de9892c9b57d7bcdf19721c6bbb8ee0e42159
RETURN_COMMIT = siehe Branch axiom/r45-7-glm-return-r1

ZIP_BYTES = 255587
ZIP_SHA256 =
 82094ad9557215a12e16e2068c5372ae8e9b021e9c102041de3741e0d7f7588c
MANIFEST_SHA256 =
 b8921dfd5e2db8bfaab7f62ab8742616fa361adbf893de1d14e333829c3a9c4a
MITGLIEDER = 85 (testzip OK, Manifest 84/84 MATCH; Platzhalterinterpolation geprüft)

EINGANG (Anhang R45-7, NEXUSO~1.TXT) =
 19.045 B, 394 Zeilen,
 4856e44fd3302f0d5da396a351b44deca23872ce4f891c5390e293c2be2c9e27

TRANSFER_CHECK =
 R45_7_EXPERT_ORDER_R1.zip = 35883 B,
 SHA-256 0ff1cee1d2b33447265161316671250316515e1cfd4d6db2addee06fa9de7985 = MATCH
 SIDECAR = MATCH, MANIFEST 13/13, CRC 14/14

KREUZVALIDIERUNG =
 09_PRIOR_SANDBOX.py stdout =
  a9d2856ddb9cc9062b4d2e440abfe2ff8dd6eb39071f8b6acdce493ae9be7f10 (byteexakt gepinnt)
 06_REFERENCE.js Ausführung == 07_RECEIPT.json.result (node v24.22.3)
 PREREG = 4/4 reproduziert (fairness 24/54/9/0; no_tick 6/10/3/3;
  budget_overrun 4/0/6; e_process 3.1/99.95/86.95/2.15/99.85)
 PRIOR_DIAGNOSTIK 3360/24718 = SOURCE_GAP (erzeugendes Artefakt nicht übertragen)
 PRIOR_DIAGNOSTIK 49152/413952 = SOURCE_GAP (dito)

PROGRAMM_E =
 RAUM = 4096, ZULÄSSIG = 1, VERWEIGERT = 4095
 MUTATIONSZEUGEN = 12/12, UNKNOWN_VERWEIGERUNG = 12/12 (fail-closed)
 SITUATIONEN = 8/8 STIMMEN MIT ANHANG (DENIED×4/ALLOWED/REVIEW_ELIGIBLE/UNKNOWN/EFFECT_IDENTIFIED)
 E1_MATRIX = 13/13 ABGEDECKT
 E_REGISTER = NEGATIV 24/24, POSITIV 4/4 (prädikatsbasiert, kein stiller Pass,
  do_not_sum; getrennt vom historischen Register 20/20 + 4/4)

E2_OBSERVATION (Seed 45712, 1000 Läufe) =
 OS: 94,47 % Abdeckung, 431 falsche Zuordnungen
 Verfolger: 97,70 %, 0 falsch, 376 offen unbekannt
 Beleg: 25,00 %, 0 falsch, 3000 blind, 41 unbekannt (verlorener ACK)

E3_MATCHED_BUDGET (Seed 45711, Budget 20, identische Aufgabenfolge) =
 direkte Planung 197/200, 3 falsch-irreversibel
 statische Simulation 197/200 (Zirkularität)
 unsicherheitsgeführt 198/200, Brier 0,0318 gegen 0,0470
 unsicherer Fallback 197/200 (Gegenzeug; strukturell verblockt, N18)
 raumfüllende Exploration 191/200 (Nachtraining verschlechtert)
 Entdeckungen der Fehlspezifikation = 0 bei allen Strategien

E4_HANDSHAKE = 1 ACK, 2 HOLD_INCOMPLETE, 4 REJECT; FRAME_LOCK=HOLD als Instanz dokumentiert
E5_TLA = eigenes Modul NEXUS_R45_7_Schleusentor.tla/.cfg; TLC NOT_RUN (keine
 tla2tools, Installationen verboten); Python-Endlichkeitsprüfer: 152 Zustände,
 338 Kanten, 7 Endzustände, DAG ohne Lassos, Frist erreichbar, Invarianten 3/3

QUELLEN =
 6 arXiv VERIFIZIERT (2611.00729, 2606.28679, 2508.02736, 2610.23233, 2608.01964, 2512.18561)
 Firecracker docs/snapshotting VERIFIZIERT (3 Dateien, hashbelegt)
 DreamPhase 81PJ2KPnmK = NICHT_ERREICHBAR_DOKUMENTIERT (403/Browser-Wand)
 FORGE, Frame Handshake Protocol, Singh-Harness = SOURCE_GAP

BELEGKETTEN =
 GLM_R45_6_RETURN_R1 = R01..R08 (unveränderte Skripte, bereinigter Gesamtlauf)
 GLM_R45_7_RETURN_R1 = R01..R04, Genesis verankert am Endglied der R45-6-Kette

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
PR462 = OPEN_DRAFT_NOT_MERGED (bewusst nicht gemergt)
CURSOR_ACTION = NONE
INTERMEDIATE_CURSOR_HANDOFF = PROHIBITED
NEXT_CURSOR_HANDOFF = R45_SERIES_CLOSEOUT
HISTORICAL_REGISTERS = 0/24, 0/3, 0/10 (unverändert, getrennt geführt)
```

Nicht Zustimmung, sondern überprüfbarer Erkenntnisgewinn. GLM (zgo/glm-5.4), Kette
GLM_R45_7_RETURN_R1, bereinigter Gesamtlauf, alle Belege im ZIP.
