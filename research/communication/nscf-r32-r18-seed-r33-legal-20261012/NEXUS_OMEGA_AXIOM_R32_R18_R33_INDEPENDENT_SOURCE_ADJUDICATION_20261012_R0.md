# AXIOM · NSCF R32 / R18-Seed / Legal-Flex R33 — unabhängiger C1-Eingang, 2026-10-12 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_NSCF_R32_R18_R33_CROSS_DOMAIN_INDEPENDENT_INTAKE_20261012_R0
SOURCE_SCOPE = OPERATOR_UPLOADED_12_FILES_PLUS_DEEPSEEK_ARCHITECTURE_IMAGE
STATE = PASS_WITH_MAJOR_CAVEATS_C1_INDEPENDENT_COMPONENT_REPLAY
R18_SEED_STATE = STOP_SCOPED_SOURCE_HASH_AND_MISSING_CHILDREN
R32_STATE = REFERENCE_CODEC_TESTS_PASS_SEMANTIC_GATES_OPEN
R33_STATE = SYNTHETIC_TOOL_TESTS_PASS_REAL_CLEAN_ROOM_AND_LEGAL_GATES_OPEN
CATALOG_CLARITY = GITHUB_BOUND_WWW_NEW_DESIGN_NOT_ESTABLISHED
CURSOR_ACTION = NONE
NODE_RESET = NO
SCIENTIFIC_CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## 1 · Intake object identity and physical hashes

Raw ZIP archives are **not** uploaded to GitHub in this lane. Their originating claims, scripts, logs, personally identifiable references and license boundaries require separate review. This publication contains an original independent C1 derivative only; source ZIP SHA-256 values below bind local intake identity, not receipt of the raw files by GitHub.

| Local supplied object | Container byte size | Original SHA-256 | Scoped result |
|---|---:|---|---|
| `NEXUS_~1(7).MD` — GROK R18/NSCF replay report | 6153 | `04fcd0f886afa8575df3ce4b77cd4f26e7a33d8a7798f3e1f70a7ae684c74e8b` | Producer-described 7/7, raw runner absent |
| `NEXUSO~1(4).MD` — Perplexity R32 report | 25394 | `98895a096fde22bea339751ab88748f851002628d65162f8ed5945193b97efcb` | Distinct R32 ontology, not R18 seed |
| `NEXUSO~1(3).ZIP` — R32 codec/source package | 33840 | `9aa837ae0a8ba97149e75a129d708146a01d8f0ff4fb8992e0e341342e2ebcda` | CRC PASS, 8/8 Manifest MATCH |
| `NEXUS_~2(6).TXT` — R18 development prompt | 8844 | `010f338245e3c6b9ba817cbae9ec802956028bfa18644c53a9d35b0c36957f0e` | Proposal, not actual seed bytes |
| `NEXUS-~1(3).ZIP` — GROK 1-fixture token comparison | 6639 | `e5b1641182591b4b50000567d52259a4c6c2b22cb8fdb2f6f1b128ecab49d2b5` | Single crafted-example token savings only |
| `NEXUS_~1(20261012-193022).TXT` — R32 instruction | 10892 | `86f7ba21acb2ccd06dcda4d5ed16624eb7cf572ae774eb24c2958890cbbd0219` | Earlier unsubstantiated global compression claims |
| `NEXUS_~1(8).ZIP` — older R17/R16 intake | 11670 | `c3d1706495de629741601553c428297771fb8940946181f54af640a978d2358a` | 6/6 detached children MATCH; no R17 Mind terminal promotion |
| `NEXUS-~2(1).ZIP` — STOP dossier | 465934 | `398d25fa4ffb725b6e380bedb8bf5b272727591426ab872e08fc28cd9bc5d0b0` | CRC PASS, 19/19 dossier Manifest MATCH, 8/8 hash-named sources MATCH |
| `LEGAL_~1.TXT` — original R33 order/claims | 26943 | `c469739d32eedeb83844b470b7207ef6058b896723e8f678c290e3c9a702a678` | Contains claims later contradicted/corrected |
| `NEXUS-~3.ZIP` — Legal R33 R1 | 57202 | `d5cc4d621b90a4af35f0cf565027b3b9763f8b7906e75b1cd67d8b672af4842a` | CRC PASS, 48/48 manifest MATCH |
| `NEXUS-~4.ZIP` — Legal R33 v2 | 70296 | `b201d2f573f600eaf52643efd5870b50ef9f3c6002b00fe1939c3e3ba8615299` | CRC PASS, 66/66 manifest MATCH |
| `DEEPSE~1.PNG` — operator-supplied diagram | 290692 | `e6dcf8ab51b72765e75a82127f8c7862a480a26d93903f98b0392356dda2013a` | Architecture illustration, not a measurement |

The STOP dossier contains **a different image source** with its own file hash; the shown `DEEPSE~1.PNG` must not be silently substituted for that ZIP child. Every object is named by full OBJECT and complete original container SHA-256, never by the reused label `R18` alone. In this repository, `research/r18/` is also a separate clean-room-provenance lane.

## 2 · Independent tests actually executed by AXIOM

All replay work was done in a temporary isolated Linux copy with no live writes or network. Source originals remained byte-identical. Python dependencies `jsonschema` and `cryptography` were available; `tiktoken` was not. For the R32 test harness alone, the historical Perplexity absolute local path `/home/user/workspace/r32/nscf` was replaced **in the temporary test copy** so it imports the given zipped code/ontology; no substantive test assertion was changed.

| Object | Independent execution | Validated scope |
|---|---|---|
| R32 reference `nscf/tests.py --json` | **20/20 PASS**, exit 0 | Codec round-trip, six rejection fixtures, digest tamper, newline injection, ontology fail-closed and non-destructive drift, basic hash-chain and witness tests |
| R33 R1 `unittest` | **9/9 PASS**, exit 0 | Structural validator on *synthetic* fixtures, not JSON Schema instance validity |
| R33 v2 `unittest` | **27 PASS + 1 SKIP**, 28 collected, exit 0 | Updated schema/Ed25519/DSSE/chain/synthetic similarity checks; `test_jplag` skipped because local Java/JPlag absent. OpenSSL cross-verification **executed PASS** |
| R32 source package | **8/8 hashes+sizes**, CRC PASS | Manifest consistency only |
| R33 R1 & v2 packages | **48/48 + 66/66 hashes+sizes**, CRC PASS | File integrity only |
| STOP dossier | **19/19 manifest + 8/8 source-filename hashes**, CRC PASS | Intake integrity, not successful R18 development |
| R17/R16 source ZIP | **6/6**, CRC PASS | Historical receipt identities, not new R17 closure |

The R32 `run.py` full 12-message measurement harness was **not** re-run by AXIOM: it binds absolute R31 and Perplexity-local source paths and requires `tiktoken`; reproducing only `tests.py` does not reproduce the reported tokenizer statistics, embeddings or independent document access. Perplexity's longer claims (12/12 exact facts, 20/20 tests, 13/13 killed mutants, class-based token means) are distinguished from this scoped independent 20-test replay.

## 3 · R18 Seed: exact negative evidence and STOP

The uploaded STOP dossier includes a snapshot of the earlier `r18-autoclaw-cross-validation-20261012` source branch at declared commit `38ade1937c7e4b028218f1859ec8084282f2ee08`. Its detached manifest declares **nine files**, while the supplied snapshot documents that only F01 and F06 were present on that branch; F02–F05, F07, fixture manifest and R18 ontology were unavailable. This historical branch inventory is **dossier-derived**, not a new complete independent branch-tree audit.

AXIOM independently recalculated from the supplied snapshot:

```text
F01 ORIGINAL BYTES = 488
F01 ACTUAL_SHA256  = dacb92e1afc1d53b62ff689c4eeacbcbda110d03bccf7a204cb16cfee619b091
F01 DECLARED_SHA256= e151fec20d18dbf690c955a118a57b78cd69655e0775688d39a8b55df3af6fd1
F01 DELTA = "word_len": 20 → 21
F01 CANDIDATE_CORRECTED_SHA256 = e151fec20d18dbf690c955a118a57b78cd69655e0775688d39a8b55df3af6fd1
F06 SHA256 = 463861215d90715aff7c811cab500b06ac02e41948ba6b61e4c72b5016c19ef8
R18 ONTOLOGY SOURCE ORIGINAL = ABSENT_IN_THIS_SEED
R18 7/7 SEAT CODE/RECEIPT = ABSENT_IN_THIS_INTAKE
```

The one-field F01 repair candidate is **not performed** on the canonical source; it establishes an exact explanatory counterfactual for the documented hash divergence, neither source tamper nor source transfer error intent. The GROK report's `7/7` R18 source-specific replay remains **NOT_INDEPENDENTLY_REPRODUCED** because the purported `nscf_ref.py`, `run_r18_against_nscf.py`, `r18_vs_nscf_receipt.json` are not supplied. Neither R32's distinct ontology nor R32's substitute corpus closes the original R18 source gap.

R18 scientific progression from its frozen 7-fixture seed is `STOP_SCOPED_SOURCE_HASH_AND_MISSING_CHILDREN`; no destructive reset, no branch overwrite, no reopening R17 module by renaming these claims.

## 4 · NSCF token-economics and the diagram claim ceiling

Perplexity R32's submitted report states 12/12 round-trip on its own **constructed structured gold intents** and reports 33.4% mean saving vs verbose JSON in inline mode with `cl100k_base`, but **minus 7.7%** saving vs ordinary natural language in the same inline mode; lean and by-ref outcomes depend on distinct framing/storage assumptions. These are **producer-reported token data**, not independently rerun by AXIOM. Semantic fidelity measured by embeddings and bidirectional NLI: **NOT_MEASURED**. A natural-language→frame encoder: **NOT_BUILT**. 30-fixture R18 success corpus: **NOT_ESTABLISHED**. Sender authentication for execution-sensitive intents: **OPEN**.

R32 uses a **different** declared ontology `8f1c43e91026...` versus the R18 seed ontology `9467a6cd993725...`. For short messages, extra hash/digest tokens may make inline communication *more expensive* than plain text. By-reference savings count payload deduplication from a *shared verified content store*, **not** lossless in-place compression. No generic 23–90% / 99%+ meaning-preservation performance is proven for NEXUS. `cl100k_base` / `o200k_base` token counts are not hardware PCIe/NVLink throughput measures; hardware parity claims are `NOT_SUPPORTED_CATEGORY_ERROR`.

The DeepSeek graphic is preserved as a **proposal-level flow diagram**: Layer 0 `Lebende Symbiose-Artefakte`, A `Determinismus`, B `Protokollvertrag`, C `Provenienz` → optional compression → transport → validation. Its 60–90%, 82%, 72% labels are external author self-reports or unverified/ambiguous protocol identities. **Hash and digest alone are integrity checks, not verified sender authenticity**; a recipient can only authenticate an actor via separately established, trusted keys/principals. `FIPS_SELFTESTS_PASS` is not `FIPS_CERTIFIED`. Loop-back arrows do not prove autonomous, safe or closed-loop execution.

## 5 · R33 Legal-Flex: corrected scope and schema regression

Legal R33 R1 includes the *original* legal claim text and a 15-point append-only correction ledger; its 48/48 manifest checks and 9/9 structural unit tests reproduced. The v2 successor adds full JSON Schema Draft 2020-12 instance validation, synthetic Ed25519 signatures, a SHA-256 event chain, synthetic code-similarity checks and an in-toto/DSSE style generated envelope.

**Material negative regression:** R1's `P0_valid_synthetic.json` was accepted by the R1 structural validator, but the full R1 `cleanroom-chain.schema.json` rejects it (missing attestation `statement` and `date`). V2's tests explicitly retain this failure instead of incorrectly promoting R1. The v2 synthetic demo passes its own updated schema and signature tests; this does not establish a lawful real Clean Room, trust-anchored signer identity, certified SLSA level, validity of legal claims, freedom to operate, or legal advice. The v2 deterministic-label test keys are **public demo keys**, not live trust anchors.

Pending R33 gates: genuine independently documented implementation history, actual testable reference implementation and lawful comparison scope, independent provenance/identity authority, license/patent/trade dress/contract analysis by qualified counsel, and independent legal source adjudication. Assertions in the original user-provided draft that AI-generated software is categorically non-copyrightable, APIs categorically protected, or clean-room labeling automatically avoids copyleft are **not upheld**. The original fact-check and correction documents remain producer analysis, not an independent legal ruling by AXIOM.

## 6 · Decision and minimal next path

```text
R32_REPLAY_20_TESTS = PASS_IN_ISOLATION
R32_FULL_TOKENIZER_AND_SEMANTIC_BENCHMARK = NOT_REEXECUTED
R18_SEED_F01_DECLARED_VS_ACTUAL = MISMATCH_EXACT
R18_SEED_CHILDREN = GAP_REPORTED_FROM_HISTORICAL_SNAPSHOT
R18_CLAIM_PROMOTION = NO
R33_R1_UNIT = PASS_9_OF_9_SYNTHETIC
R33_V2_UNIT = PASS_27_EXECUTED_ONE_SKIP_OF_28_SYNTHETIC
R33_REAL_CLEAN_ROOM_COMPLIANCE = NOT_ESTABLISHED
R33_SOURCE_LEGAL_ADJUDICATION = NOT_PERFORMED
WWW_DUAL_PUBLICATION = NOT_VERIFIED
NEXT = RECEIVER_SOURCE_FIXTURES_AND_QUALIFIED_NEGATIVE_TESTS_ONLY_WHEN_RELEVANT
CURSOR_ACTION = NONE
R19_INTERFERENCE = NONE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

This report is a public-safe original **derived adjudication**. No raw source bundle or third-party diagram was copied into public GitHub. The site research catalog should remain uncluttered: discovery may later point to this report with three short scope/status facets but only after public WWW bytes exist and are verified.
