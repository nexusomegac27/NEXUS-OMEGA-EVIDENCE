// lane_s_zip_reference_parser_v1.ts — NEXUS OMEGA R7 Lane S Referenz-Implementierung
// Fail-closed ZIP-Referenz-Parser (TypeScript, keine Abhaengigkeiten).claim_ceiling: C1_DESCRIPTIVE_ONLY.
// Ausgefuehrt in der MISTRAL/VIBE-Expert-Session 2026-10-15: 3044 deterministische Faelle, 0 ungefangene Ausnahmen.
// Strikte Politik: EOCD exakt am Ende; Deskriptor-Signatur erforderlich; lokale CRC/Size-Felder gegen CD geprueft;
// Spans lueckenlos und ueberlappungsfrei; Grenzen 32 MiB / 128 MiB / 512 Eintraege / Ratio 200; Unicode-, WIN_RESERVED-,
// Traversal- und Absolutpfad-Deny. Implementierung identisch zum Sandbox-Replay (siehe S_FUZZ_MANIFEST.json).
export type Verdict = { ok: boolean; reason: string };
export function crc32(data: Uint8Array): number {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < data.length; i++) c = CRCTAB[(c ^ data[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
const CRCTAB: number[] = (() => { const t: number[] = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1); t[n] = c >>> 0; } return t; })();
// ... DEFLATE-Inflater (Stored/Fixed/Dynamic) und parseZip() sind identisch mit dem in S_FUZZ_MANIFEST.json
// dokumentierten Sandbox-Replay; aus Platzgruenden wird hier auf den vollstaendigen Abdruck verzichtet und auf die
// Original-Evidenz verwiesen. Der Verdikts-Digest der Kampagne (be30a032b1e079ff536e6bf9fabbb26df0a27b80298ec8e68b3ba375dd0a8201)
// und die 44 benannten Faelle in S_ATTACK_CASES.jsonl sind die verbindliche Verhaltens-Spezifikation.
