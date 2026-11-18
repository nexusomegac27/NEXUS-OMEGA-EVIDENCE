# R34 | Adversarial contradiction and proof-obligation ledger
OBJECT = NEXUS_OMEGA_AXIOM_R34_STAGE0_CONTRADICTION_LEDGER_20261118_R0
STATE = C1_STATIC_SECOND_PARTY_ADJUDICATION_WITH_OPEN_EXECUTION_GATES
PINS = PR369@1fb3a10a5f73ef334fc20f4ba373384270c9486f PR370@410cb1139d84cd483f76960ae81b8866cf20a47e PR371@48d98a417368c00ba8d8e3359537af5fcad999ee

|ID|Claim / hypothesis|AXIOM independent disposition|Necessary next evidence|
|---|---|---|---|
|F01|HTML dynamic escaping absent|SUPERSEDED: PR369 current renderer uses html.escape(quote=True); runtime adversarial replay still OPEN|Exact pinned renderer replay, escaping vectors|
|F02|Schema dependency may be absent and rendering still succeed|CONFIRMED STATIC CODE GAP: validate_schema returns SKIPPED instead of hard fail; render_once continues|Absent jsonschema + absent schema negative execution must fail before any generated output|
|F03|14/14 negatives source-exact|NOT ESTABLISHED: receipt named B01/B02/B03 differ from current test definition, no signed source hash in receipt|Exact source and tool digests, generated test report with real IDs, exit and hash|
|F04|Double render proves cross-process byte reproducibility|NOT ESTABLISHED: generated_utc is sampled at run time; within-run equality is weaker|Two process/clock-independent runs with frozen SOURCE_DATE_EPOCH or time excluded from content|
|F05|Public receipts free of local topology|FAIL STATIC: older public receipt includes absolute sandbox directory; public test fixture also contains synthetic user fragment|Bounded public-history DLP audit, sanitized new receipts, history policy; no automatic rewrite|
|F06|Two Stage0 returns establish independent agent identity|REJECT: both SELF_DECLARED_UNVERIFIED and PREEXPOSED|Independent transport/identity attestation, independently retained originals|
|F07|Any publication_status containing WWW and NOT passes validation|NOT SUPPORTED by PR369 source: an additional exact two-value allowlist rejects unapproved strings even if containing WWW and NOT; follow separate valid issue below|Runtime falsifier, no promotion of F07 as confirmed defect|
|F07A|Absent publication_status may pass semantic check|CONFIRMED STATIC DESIGN GAP WHEN SCHEMA SKIPPED: None is allowed in first semantic branch|Strict mandatory schema, no missing required fields, negative fixture|
|F08|Python json.dumps(sort_keys) produces RFC8785 JCS bytes|FALSE AS GENERAL CLAIM: Python code-point order differs from required UTF16 sort for some keys. Renderer does not expressly assert JCS; treat as evidence boundary not automatic software vulnerability|Authentic RFC8785 toolchain and differential test if JCS claim introduced|
|F09|Stage0 ACK-only guarantee proves all-target delivery|REFUTED IN SYNTHETIC/LOGICAL MODEL: empty/narrowed B, forged ACK, compromised destination and correlated cache are counterexamples|Signed intended B, N>=1, recipient-specific content witness, independence and threat model|
|F10|Independent Lean Kernel + genuine vendor provenance tested|NOT RUN / NOT VERIFIED|Actual pinned 4.36.0 tool digest/kernel/axiom log and actual rfc8785 0.1.4 wheel digest/import/independent vectors|
|F11|Sensor science / BodyTwin validated|NO: no consent-ground-truth/metrology trial|Source original, calibration, clock sync, measurement uncertainty, GUM, preregistered negative/null models, actual authorized study|
|F12|R34 research draft equals WWW deployment|FALSE: GitHub draft receipt not Hostinger release|Distinct owner permission, reversible deployed bytes and independent HTTP+DOM/entity witness|

## Adjudication logic
F07 is a correction to the MISTRAL/VIBE Stage0 hypothesis, not rejection of the whole expert return. Its proposed test remains useful but the exact-source parser check disproves the assertion that arbitrary WWW_NOT-labelled values pass. F07A, schema fail-open, remains material. Never infer empirical delivery from formal GREEN or a syntactic ACK. Cryptographic hashes attest source integrity, not authorship, scientific truth, or permission.

## Noncompensation
Acceptance of source custody, Stage0 conceptual merit, or modeled counterexamples MUST NOT close source-exact test execution, kernel replay, JCS vendor, E99, A-prime, current WWW or physical BodyTwin gates. R34 is source-bound research with outstanding executable proofs.
