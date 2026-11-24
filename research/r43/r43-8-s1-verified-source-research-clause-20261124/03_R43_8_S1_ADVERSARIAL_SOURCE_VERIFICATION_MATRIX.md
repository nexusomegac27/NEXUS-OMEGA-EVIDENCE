# VSRD-C1 — Verifizierte Quelle / eigene Recherche / Negativtests

| Code | Adversarial condition | Expected fail-closed adjudication |
|---|---|---|
| VSR-01 | lookalike host/impostor organization | Q0; not trusted canonical original |
| VSR-02 | HTTP200 generic index and strong numerical science claim | reject Q3/Q4 |
| VSR-03 | HTTP203 proxy cache or short snippet | QX or Q1 indirect only |
| VSR-04 | 401/403/404/429 interpreted as disappearance of study | reject absence claim; record vantage-dependent access gap |
| VSR-05 | known DOI metadata but retraction/correction missing | block outdated science conclusion |
| VSR-06 | code repository CC0 but separately hosted dataset rights unknown | Q4 data rights HOLD |
| VSR-07 | `main` silently advanced while citation claims immutable result | require pinned full commit hash and data SHA256 |
| VSR-08 | source mirror, DOI metadata and publisher all same research object counted as independent replication | reject Q5 |
| VSR-09 | hallucinated DOI with wrong title/authors/date | source mismatch FAIL |
| VSR-10 | abstract only treated as complete methods or study statistics | no full-method validation |
| VSR-11 | held-out reference measurements injected into test-time model | leak and unfair comparison FAIL |
| VSR-12 | genuine dataset has wrong phone location, population and topology | authenticity MAY PASS, applicability FAIL |
| VSR-13 | unfavorable primary replaced by favorable exploratory sensitivity | preserve frozen primary, separate exploratory |
| VSR-14 | self-labeled independent agent counted as authenticated actor | reject actor trust, maintain quorum 0/3 |
| VSR-15 | source checked months ago treated as current without access timestamp | REVALIDATION_REQUIRED |
| VSR-16 | two routes use same scraped source/text but presented as independent empirical evidence | separate metadata cross-check from empirical independence |

**Positive controls**: (P1) legitimate original publisher article + Crossref DOI metadata match, source scope and corrections logged; (P2) original legal data bytes + SHA256 and separate license with frozen commit/release; (P3) external reviewer genuinely authenticates and reproduces exact original code+data negative control; (P4) blocked FDA endpoint correctly leads to QX, and legitimate authority route sought, without CAPTCHA bypass. All P1-P4 research examples until execution receipts exist.

## Scientific acceptance
A `Q5` may be achieved for a properly scoped original study result when an independently authenticated reviewer reproduces it, but does not itself release NEXUS BodyTwin science/clinical/physical gates. At R43-8-S1 entry source-class counters remain as on original R43-8. If legal/protected data unavailable, return well-targeted hypothesis and honest SOURCE_GAP, not false verification.
