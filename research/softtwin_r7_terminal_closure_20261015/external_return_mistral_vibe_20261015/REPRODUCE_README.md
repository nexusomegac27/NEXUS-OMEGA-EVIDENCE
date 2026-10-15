# REPRODUCE_README — Reproduktion des Returns

## Voraussetzungen

- Beliebige TypeScript-Runtime (kein Node-spezifischer API-Gebrauch in den Referenz-Implementierungen; keine Netzwerkzugriffe).
- Die beiden Referenz-Implementierungen dieses Umschlags: lane_s_zip_reference_parser_v1.ts und evidence_adapter_v1.ts.

## Schritte

1. **Selbsttests:** sha256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad; crc32("123456789") = 0xCBF43926; Inflater-Selbsttests: Stored-Block, Fixed-Huffman "AAAABBBB", LZ77 "abcccccccX" (len=6, dist=1).
2. **Basis-Fixtures:** 8 syntetische ZIPs (siehe S_FUZZ_MANIFEST.json, base_fixtures) muessen alle ACCEPT ergeben (B3 = EMPTY_ARCHIVE).
3. **Fuzz-Kampagne:** mulberry32-PRNG mit Seeds 0x20261015, 0x0f0f0f0f, 0xdeadbeef; je 1000 Ein-Defekt-Mutationen (flipBit/setFF/set00/truncate/insert/swap) ueber die 8 Basis-Fixtures; zwei identische Laeufe. Referenz-Ergebnis: 426 ACCEPT / 2574 DENY, 0 ungefangene Ausnahmen, Verdikt-Digest be30a032b1e079ff536e6bf9fabbb26df0a27b80298ec8e68b3ba375dd0a8201.
4. **Benannte Ein-Defekt-Faelle:** 44 Faelle N01-N44 (S_ATTACK_CASES.jsonl); Referenz-Ergebnis 44/44 erwartungskonform.
5. **Adapter-Suite:** 43 Fixtures / 45 Assertionen (EVIDENCE_ADAPTER_NEGATIVES.jsonl); Referenz-Ergebnis 45/45 konform.
6. **Mathematik:** E(1000) = 3993.333333 = 4(N-2+1/3); invalide Schranke 888.888889 verletzt; konservative Schranke 8000 haelt.

## Integritaet des Umschlags

- SHA256SUMS.txt deckt alle 18 Umschlagsdateien mit Ausnahme von SHA256SUMS.txt selbst und FINAL_RETURN.json (Kreisfreiheit). FINAL_RETURN.json ist ueber seinen Git-Blob im Commit dieses Returns verankert und nach Checkout mit sha256sum neu pruefbar.
- Die gepinnten Quellen und deren SHA-256-Werte: siehe SOURCE_AND_BINARY_MANIFEST.json und PROVENANCE_AND_RIGHTS_R7.md.
- Die Referenz-Implementierungen sind die in der Sandbox dieser Session ausgefuehrte Logik; die Datei-Hashes liegen in SHA256SUMS.txt.

## Grenzen

- Es wird keine Ausfuehrung gegen die Python-Zielimplementierung V0.4 behauptet (G1/G2/G3 = HOLD). Windows: NOT_CLAIMED. Produktion/MCP: NOT_AUTHORIZED.
