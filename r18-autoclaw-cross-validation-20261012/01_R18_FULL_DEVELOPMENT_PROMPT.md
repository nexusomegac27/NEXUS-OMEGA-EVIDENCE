# NEXUS OMEGA AXIOM — R18 DEVELOPMENT PROMPT
# Object: NEXUS_OMEGA_R18_SEMANTIC_COMPRESSION_AND_DRIFT_RESET
# Created: 2026-10-12T15:55 CEST (measured in independent sandbox by Grok)
# Claim ceiling: C1_DESCRIPTIVE until all success criteria below are met and independently re-executed
# Constraint: No exclusive GitHub-only publication. Everything must also appear on nexus-mobile.de. DRIFT_RESET default = NON_DESTRUCTIVE. Source-exact + byte-auditable.

## 1. ROLE & SCIENTIFIC DISCIPLINE
You are the independent scientific executor for NEXUS OMEGA AXIOM R18 (autoclaw).
You inherit the R16/R17 adjudication state and the seed corpus produced by Grok.
All new claims must be backed by exact SHA256, independent re-execution logs, and explicit PASS/FAIL/CAVEAT.

## 2. MEASURED FIXTURE CORPUS (seed – already verified by hash in this package)
Object: NEXUS_OMEGA_R18_FIXTURE_CORPUS_V0_MEASURED
n = 7 (seed; expand to ≥30)
See r18_fixtures/ and FIXTURE_MANIFEST.json for exact content and internal text SHA256s.

Length bins covered: ≤100 | 100-500 | 500-2k | 2k-8k

## 3. VERSIONED INTENT ONTOLOGY
Object: NEXUS_OMEGA_INTENT_ONTOLOGY_V0_1
File: r18_fixtures/INTENT_ONTOLOGY_V0_1.json
Any compression output that emits an Intent MUST also emit the ontology version hash.
On decompression verify version currency or declared migration; otherwise fail-closed or trigger DRIFT_RESET.

## 4. CORE RESEARCH QUESTION (R18)
Can a versioned, anchor-protected Intent ontology + “-like” semantic compression, evaluated on a multi-fixture corpus spanning four length bins and adversarial cases, deliver:

- mean token savings ≥ 40 % on bins ≥ 500 tokens
- mean embedding cosine ≥ 0.92
- bidirectional NLI entailment ≥ 0.90
- downstream Intent-classification accuracy drop ≤ 3 pp
- zero silent acceptance of ontology drift on adversarial fixtures
- fully operational, non-destructive-by-default DRIFT_RESET that emits a hash-chained Anchor event

…while preserving existing F1 / K2 / lease-fencing guarantees?

## 5. MANDATORY BENCHMARKS
A. Token savings by length bin (same tokenizer family)
B. Semantic fidelity: embedding cosine + bidirectional NLI + downstream Intent accuracy
C. Robustness on adversarial fixtures (no silent ontology drift acceptance)
D. System compatibility (atomic boundaries, outbox, fencing still hold)
E. DRIFT_RESET produces observable, hash-chained Anchor events and never destroys history by default

## 6. DRIFT_RESET OPERATIONALIZATION
Design and implement a precise state machine with:
- Clear triggers (version mismatch, fidelity threshold, explicit drift score, policy)
- Non-destructive default path (new Anchor + re-index / migrate, preserve history)
- Destructive path only under explicit high-privilege policy + full audit trail
- Every transition observable in the hash-chained event log

## 7. DELIVERABLES
1. Expanded fixture corpus (≥30) + updated FIXTURE_MANIFEST.json with all SHA256
2. Reference compressor/decompressor using versioned ontology
3. Measurement harness producing the required tables and numbers
4. DRIFT_RESET state-machine specification + implementation + tests
5. Independent re-execution / adjudication report
6. Updated Adjudication object with STATE, measured numbers, residual gaps, NEXT
7. Confirmation of dual publication (GitHub + nexus-mobile.de)

## 8. STARTING ACTIONS
A. Perform the hash verification in 00_AUTOCLAW_CROSS_VALIDATION_INSTRUCTIONS.md
B. Load the seven seed fixtures and the ontology
C. Propose exact JSON schema for future fixtures (backward-compatible)
D. Design the “-like” compression format
E. Implement minimal round-trip on F01–F03 and report initial metrics
F. Sketch the DRIFT_RESET state machine as formal transition table

Begin with hash verification. Keep claim ceiling C1 until numeric gates are actually measured and re-executed.
