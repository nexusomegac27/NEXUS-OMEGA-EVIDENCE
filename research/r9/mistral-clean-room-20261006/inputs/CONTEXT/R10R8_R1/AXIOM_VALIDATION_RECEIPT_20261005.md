# AXIOM Validation Receipt — R10R8 / E0.2

**Date:** 2026-10-05  
**Claim ceiling:** `C1_DESCRIPTIVE_ONLY`  
**Verdict:** `PASS_WITH_MAJOR_CAVEATS_C1_R10R8_E0_2_SYNTHETIC_GATE_SURFACE_PUSHABLE_NOT_PRODUCTION`

## 1. Outer stack witness

- file: `E0_2_G~3.zip`
- bytes: `211032`
- SHA-256: `7d18b9e53f24d0f7c76c3c2b7e11036b8ca65866cce7de994d6b383da1f7130f`
- ZIP test: PASS
- entries: 82

Selected nested containers independently opened without ZIP corruption:

- Grok E0.2 crossvalidation/order: 7171 B · `7a454a05d77cf386f44b536bb0f0be1713ab4537a80c030c18476e0fa5fb8d1d`
- E0.2 nonexistence-audit/seed: 5383 B · `dbad913b49cd9ad7ff4d4502b7ec668dcf78b631aa09d22b7501a5ea38b1eb4e`
- Manus R10R8 crossvalidation package: 42477 B · `6dfc5d4d3474ce8892f9d00a346f327d0c477014560197b1c439f3301d8966ab`
- Manus R10R8 continuation package: 90337 B · `e2f568c82bcc50a1e7cf5c43add457ba7816f5a7fe4a5bc134c67ebb4680fb14`
- Grok full-integration package: 119632 B · `db030e943077159ab74fb46cf3472f770db6c71a1f12bdf7c4975955d40b68ac`

## 2. Hash-set verification

AXIOM independently recomputed the available declared SHA-256 sets.

- Gate2 top-level set: 2/2 MATCH
- Gate4–Gate7 / V2 binding/spec set: 10/10 MATCH
- E0.2 seed package: 3/3 MATCH
- Grok crossvalidation package: 3/3 MATCH
- Manus Gate2/Gate3 continuation set: 5/5 MATCH

The UTF-8 BOM on one Manus checksum file is a transport/text-format detail; the listed target file digests themselves match.

## 3. Independent execution

Re-executed in a clean local Python environment:

- GATE2 hard-product fixtures: PASS
- GATE3 Δ non-compensation fixtures: PASS
- GATE4 standalone fixtures: PASS
- GATE5 standalone fixtures: PASS
- GATE6 standalone fixtures: PASS
- GATE7 standalone fixtures: PASS

Python compilation of all inspected gate scripts: PASS.

## 4. Grok full-integration reproduction

Original source SHA-256:
`fd877806ccdec14ebb81f27415dcbb05946714b47017e3e9e769985f458b57e1`

Original declared result SHA-256:
`6f17592102b7dad119a891242ebc739514cf1d87d5fe8022576c19d585a96454`

Re-execution reproduced the same JSON semantics for all four declared assertions. The byte hash changes under local re-write only because the original result uses CRLF and the local Python write used LF; normalized JSON objects are equal.

### Material method caveat

The original integration implementation does not justify the phrase “fully fail-closed seven-gate product” without qualification:

1. absent `gate2_state` defaults to VERIFIED;
2. absent `gate3_state` defaults to VERIFIED;
3. integrated GATE4 is weaker than the standalone provenance-chain checker;
4. integrated GATE5 returns AIR_GAP for a missing capsule, whereas the standalone GATE5 contract returns FALSIFIED;
5. integrated GATE7 does not enforce the C1 ceiling or provenance requirement.

Therefore the original result is accepted only as:

`PASS_C1_BOUNDED_SYNTHETIC_PRIORITY_AGGREGATION_FIXTURE`

—not as production enforcement or full formal closure.

## 5. AXIOM R1 fail-closed regression

AXIOM generated a stricter independent regression harness specifically to attack those weaknesses.

- R1 source SHA-256: `50fa60258f92d84df82bbd1a9d5fb3f0f6233a8a11b8efdb16809579847199f1`
- R1 result SHA-256: `5d9e23d37b5593120e8dcb12e01da5e4d86538a6d6bf22224836605a539c87ae`
- fixtures: 10/10 PASS
- terminal: `PASS_C1_AXIOM_R1_FAIL_CLOSED_REGRESSION`

Added attack cases include:
- missing GATE2 → AIR_GAP;
- missing GATE3 → AIR_GAP;
- missing authority capsule → FALSIFIED;
- missing defeat condition → AIR_GAP;
- C2 claim under this fixed-C1 order → FALSIFIED;
- provenance cycle → FALSIFIED;
- orphan parent without ROOT marker → AIR_GAP.

This remains synthetic regression evidence only.

## 6. Remaining open obligations

- Gate4 must be hardened beyond minimal synthetic chains before any production claim.
- Gate5 attenuation/delegation-chain semantics are not yet demonstrated by the current minimal fixture.
- Gate6 currently proves only a minimal provenance/hygiene policy, not semantic memory correctness.
- Gate7 remains a local claim-ceiling fixture, not a general constitutional proof.
- No real R10R8 microscopy / persistent-homology / light-toxicity PoC has been implemented or empirically validated.
- No cryptographic binding of authority capsules is established.
- No evidence here promotes Soft-Lineage beyond C1.
- R10R6 E2 remains PROHIBITED.

## 7. Push boundary

The public push is authorized as **research evidence with explicit caveats**. Local `.work/` material, duplicate Windows-path ZIP entries, and unrelated transport debris are excluded from the public research lane.
