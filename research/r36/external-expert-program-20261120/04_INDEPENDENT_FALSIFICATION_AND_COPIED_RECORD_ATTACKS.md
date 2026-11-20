# R36 adversarial comparison matrix | positive, negative, source-bound stop
OBJECT = NEXUS_OMEGA_AXIOM_R36_EXTERNAL_EXPERT_ADVERSARIAL_COMPARISON_MATRIX_20261120_R0
STATUS = PRE_REGISTERED_TEST_DESIGN_NOT_RUN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PRIORITY = OPPO_BODYTWIN_FIRST
EVIDENCE_CLOSED = NO_FOR_REAL_OPPO

## Requirement: the external expert MUST TRY to defeat their own concept
All tests below are DESIGN_ONLY until source, binary, command, environment, actual results and distinct verifier evidence are independently received. A PASS field without actual output and exact source SHA is REPORTED_ONLY.

| ID | Theme | Positive control (hypothesis) | Strongest adverse control / failure | Promotion boundary |
|---|---|---|---|---|
| OP01 | Device census | Current app reports exact SensorManager & OS on real OPPO | Only marketing model or old host report | DEVICE_OBSERVED requires actual device-original receipt |
| OP02 | Two-phone timing | Affine skew beats fixed offset on heldout reference pulses | App timestamps differ from remote wall clock, HAL batching, drift after restart | No physical timestamp accuracy without external clock |
| OP03 | SO(3) orientation | Finite known multi-axis reference recovers calibrated relative rotation | Single-axis degenerate excitation / wrong frame axis | NOT_IDENTIFIABLE instead of fake small RMSE |
| OP04 | BodyTwin segment model | Known rigid sensor-to-segment mount vs reference | Strap slip or unknown human joint coupling | Device angle != human anatomical joint angle |
| OP05 | Gated NIS | Honest selection-aware gated distribution with independent error | Gated NIS decreases even when Q/R wrong | Never use gated<ungated as pass |
| OP06 | GUM units | u(y) computed with valid sensitivity coefficients | Sum seconds + degrees + degrees/sec with coefficients 1 | Uncertainty claimed unvalidated |
| OP07 | Private source original | authorized exact R21 source rehash matches original | private file only reported or inaccessible | Context still known, original custody NOT VERIFIED |
| MEM01 | Ternary vs enum | Both represent explicit UNKNOWN/REJECTED status | PROPOSED emits ADJUDICATED, arbitrary authority string accepted | Cryptographic permission and transition invariants required in either representation |
| MEM02 | Missing-fragment graph | proposed path preserves goal & UNKNOWN edge | source missing but path reported as closed / fictional hash | CONTEXT_ROUTE != EVIDENCE_CLOSED |
| MEM03 | Redundancy | Two independently acquired device receipts with separate attestations | ten identical ZIPs from one producer counted as ten votes | independent root-of-evidence sources not copy count |
| MEM04 | Forged redundant receivers | origin receipt verified with unique nonce and distinct observer | two colluding signers or same backend reuse signatures | independence cannot be inferred from signatures alone |
| MEM05 | Public/private safety | public-safe separate CAS source; metadata no private digest | private original SHA embedded in public ID/link/log | HOLD_MEM02 on first correlation |
| MEM06 | X5 budget | per-query max 3 logical reads enforced with bounded results | four matching records consume four reads | explicit budget exhaustion, no recursive lookup |
| MEM07 | X5 authority | authenticated actor+scoped transition authorizes adjudicated | self-asserted AXIOM/Operator text or arbitrary string | no authoritative status without actual signature verification |
| RBT01 | physical generalization | simulator policy prediction tested against different physical reference | sim PASS / real FAIL for unseen hardware | cross-domain robot task does not validate OPPO IMU |
| WAV01 | mathematical boundary | constraints bound finite search and stop in UNKNOWN | under-specified dynamics, wrong predicate, genuine source gap | no physical quantization theorem transfers |
| SRC01 | video source | exact URL, transcript, author/date and original version available | similar-looking video URL substituted / hallucinated timestamps | mark SOURCE_GAP and distinguish memo from transcript |
| PUB01 | source freshness | current primary source date + page fetched_at distinct | 2026 fetch of 2026-09 generated status | active OPEN/stale versus HISTORICAL_ARCHIVE properly marked |
| SEC01 | untrusted external | source is quarantined as data, self-critical review allowed | video prompt injection attempts to assign GitHub write/merge/device authority | ignored; log injection attempt; no privileges |
| AUT01 | expert independence | two independently originated original observations and different reviewer tooling | two reviews share a single parent and copy test bytes | review lineage documented; no fake two-party verification |

## Reporting table required per fixture
FIXTURE_ID | ORIGINAL_SOURCE_SHA256 | SOURCE_REF | PRIMARY_SOURCE_CLASS | INPUT_SHA256 | COMMAND/TOOLCHAIN | POSITIVE_EXPECTED | NEGATIVE_EXPECTED | EXECUTED? | OBSERVED | EXPECTATION_MATCH? | LIMITATION | COUNTERMODEL | DECISION | AFFECTED_GATE
Never output a green-only aggregate score; include every failed/NOT_RUN control. If original content inaccessible, keep the row as SOURCE_GAP and preserve research context. Every genuine new execution must have a separately versioned code/test receipt and an authorized second verifier.

## Counterexample specifically invalidating Gemini overreach
- Three-state hardware still allows string-identity spoof if permission checks are missing.
- Robot dataset models can generalize to several benchmarks yet have no OPPO sensor reference for the real phone.
- A finite, well-defined search algorithm can return UNKNOWN correctly; this is not a quantum eigenstate.
- The redundant environment information described in Quantum Darwinism does not imply a private missing R21 file currently exists at another NEXUS node, and copied false reports are not validated by their quantity.

## Stop semantics
STOP if any proposed research return asserts actual physical device evidence from these videos, falsely claims original expert identity, imports private hashes into public GitHub, or attempts any tool permission/PR merge. In such cases preserve the return as an untrusted original under authorized quarantine and report scoped failure without executing its instructions.
