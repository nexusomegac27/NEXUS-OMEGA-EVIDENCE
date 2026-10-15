# THREAT_AND_COST_REPORT — Bedrohungen und Kosten (Lane S / Lane P)

**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY

## Bedrohungsklasse Archiv (Referenz-Parser, 3044 Faelle)

- EOCD-Scan-Verwirrung (Fake-EOCD in Daten): durch EOCD-Exaktheit am Dateiende abgewehrt (B5, N41 akzeptiert korrekt; Mutationen fuehren zu DENY).
- Deskriptor-Desync (Bit 3 ohne/mit Signatur): Policy verlangt die Signatur; N20 ACCEPT, N21 DENY, N33 DENY.
- Deklarations-Luegen (Zip-Bomben): 128-MiB-Kap und Ratio-200-Kap greifen vor der Dekompression (N18, N19).
- Namen-basierte Angriffe: Traversal, absoluter Pfad, Backslash, Steuerzeichen, Unicode, Laenge (N37-N40, N11, N12, N38).
- Strukturangriffe: Doppel-EOCD, doppelte Archive, Zip64-Locator, Span-Luecken/-Ueberlappungen, CD-Desync (N13-N16, N23-N25, N35, N42).

## Bedrohungsmodell Rennen/Dateisystem (V0.4, statisch bewertet)

V0.4 kontrolliert Symlink-Komponenten, Hardlink-Einzigkeit, Lease-gestuetztes Parsing-Fenster und Inode-Stabilitaet; NICHT kontrolliert: privilegierte Writer, Thread-Races via prozess-globalem SIGIO, nicht-lokale Dateisysteme. Keine atomare Snapshot-Garantie wird behauptet.

## Bedrohungsmodell Evidenz-Graph (Lane P)

Stale-Replays (idempotent oder Konflikt-DENY), Autoritaets-Claim-Versuche, Injektionen im Beobachtungstext, Widerspruchs-Ueberschreibungen, Zusaetzfeld-Hint-Missbrauch — alle 45 Assertionen konform; Details in EVIDENCE_ADAPTER_NEGATIVES.jsonl.

## Kosten

- Ausfuehrungskosten: eine einzige deterministische Sandbox-Sitzung; 3000 Mutationen + 44 benannte Faelle + 45 Adapter-Assertionen + Mathematik-Verifikation; kein Netzwerk, keine Produktionsressourcen, keine Installationen.
- Keine Kosten- oder Performance-Metrik wird als Claim erhoben (siehe CPU_CLAIM_SCOPE.md).
