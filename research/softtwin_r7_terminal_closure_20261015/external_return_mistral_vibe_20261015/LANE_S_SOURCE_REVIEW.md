# LANE_S_SOURCE_REVIEW — V0.4 statische Quellen-Review (G1/G2/G3)

**Objekt:** src/nexus_artifact_triage_v04.py · 15786 Bytes · SHA-256 a2972e6a1eaef8e933fcb2597bc5be85be76a36b6cbb3ad82ec28175103bff3a (aus der oeffentlichen R6-Kapsel, 47436 B, SHA-256 7f31a9177a8e38f64e81c13b1cdd2d28edf47b102e5f8db26492eed3d2b93aac, 18/18 CRC)

**Ausfuehrungsklasse:** STATIC_REVIEW_ONLY. Die Expert-Sandbox bietet keine Linux- und keine Python-Runtime; alle Laufzeit-Gates fuer V0.4 sind daher HOLD_WITH_PRECISE_REASON, nicht PASS.

## Befunde der Zeilen-Review

1. **Datei-Zulassung (G1):** openat-Root-Walk mit O_NOFOLLOW je Pfadkomponente; O_PATH-Oeffnung ohne FIFO-/Geraete-Zugriff; F_SETLEASE(F_RDLCK) vor dem Parsing mit SIGIO-Handling; nlink==1-Pruefung; Reopen ueber /proc/self/fd mit dev+ino-Match; pre/post-fstat ueber dev, ino, size, mtime_ns, ctime_ns.
2. **Ressourcen-Grenzen:** MAX_FILE 32 MiB, MAX_UNCOMPRESSED 128 MiB, MAX_ENTRIES 512, MAX_RATIO 200 — als Deklarations- und Deskriptorgrenzen vorhanden.
3. **ZIP-Strenge (G2):** EOCD-Exaktheit am Dateiende; Central-Directory-Konsistenz; lueckenlose, nicht-ueberlappende Spans bis zum CD; Local/CD-Match; Unicode-Deny; WIN_RESERVED-Deny (Backslash); fail-closed ueberall.
4. **Residuen:** R7-S01 — die lokalen CRC/Size-Felder des Local-Headers werden bei nicht gesetztem Bit 3 nicht gegen das CD geprueft (Inhalts-CRC wird gegen das CD verifiziert; gering). SIGIO ist prozess-global: Thread-Race verbleibt. F_SETLEASE wirkt nur auf unterstuetzten lokalen Linux-Dateisystemen. /proc wird vorausgesetzt. Ein FIFO- oder Einhaengungs-Angriff durch privilegierte Schreiber wird durch die Kontrollen nicht ausgeschlossen — es wird keine atomare Snapshot-Garantie gegen privilegierte hostil Writer behauptet.
5. **Referenz-Differenzial (G2/G3):** Die beigefuegte TypeScript-Referenz-Implementierung (lane_s_zip_reference_parser_v1.ts) ist strikter als die dokumentierte V0.4-Politik: sie prueft die lokalen CRC/Size-Felder gegen das CD und fordert die Deskriptor-Signatur. 3044 deterministische Faelle: 0 ungefangene Ausnahmen; 44/44 benannte Ein-Defekt-Faelle erwartungskonform; Details in S_ATTACK_CASES.jsonl und S_FUZZ_MANIFEST.json.
6. **Kein Code-only-PASS:** Fuer V0.4 wird hier kein PASS beansprucht; G1/G2/G3 = HOLD_WITH_PRECISE_REASON mit den genauen fehlenden Ausfuehrungsnachweisen.
