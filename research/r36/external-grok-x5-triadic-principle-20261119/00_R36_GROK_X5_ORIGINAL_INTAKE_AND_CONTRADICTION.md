# R36 external GROK X5 return — independent source intake
OBJECT = NEXUS_OMEGA_AXIOM_R36_GROK_X5_ORIGINAL_INTAKE_AND_CROSSADJUDICATION_20261119_R0
DATE = 2026-11-19
PARENT = PUBLIC_R36_PR375_HEAD_6d49c733dc9a0b0fb0b7e3000c28a9b44f239a34
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = PASS_WITH_MATERIAL_CAVEATS_C1_SOURCE_RECEIVED
SOURCE_CLASS = USER_UPLOADED_EXTERNAL_SELF_DECLARED_GROK
EXTERNAL_AGENT_IDENTITY = SELF_DECLARED_UNVERIFIED
AGENT_AUTHENTICATED_DELIVERY = NOT_ESTABLISHED
OPPO_REAL_DEVICE = NOT_EXECUTED
BODYTWIN_VALIDATED = NO
CLAIM_PROMOTION = NO
GITHUB_MERGE = NO
HOSTINGER_WRITE = NO

## Original object, not publicized as source bytes
Incoming ZIP (operator supplied) length 14321 bytes, full SHA256 96d0991b1a78671cbdf1b70e980622f73a0bb44ea7df024ecb70fca75c324dfd. ZIP CRC PASS, manifest 6/6 content sha256 MATCH. Nine ZIP entries include three directories and six manifest-covered files:
- GROK full report 9166 bytes SHA 4b832e08cf573ea0112d9b89f3fa10c7e0afb779d189f2c497b8722db69d0bb1.
- executive capsule 956 bytes SHA f7c38806be04c0411382eca4472ebc5f785fd3bc5a742adec3a40bc3a02c42ee.
- self-declared standalone reproduction code 1395 bytes SHA 1d3a5bee29895a5e0847a4b6b523fcac94a03f3ed835b5e76ec099992906436a.
- machine rubric 1552 bytes SHA f8e7f0a7a34c89f3a0f5b3a4dceba9aa30685a118253085106e57bdeb44d15f4.
- prior R36 760-byte independent X5 receipt SHA 1403aaa97d264e979d6993f299006da5e2e990a8e9a860599b7bce5610d8ccb5.
- original 16361-byte RECONC X5 Python source SHA 54d18bb0f1106275d66eced28866967a984e84e94d8abd452f07611538d70ad5.
- 744-byte SHA256SUMS SHA b0c929b59ff525a9fed1b6036c1107520e26af9f2166af361bab54ca2b66c29f.

## Fundamental contradiction
The self-declared Grok return says its reproductions were executed in that session. But its supplied executable source at line 23 contains invalid f-string syntax: an expression with an unmatched literal closing brace. Executing THAT EXACT file using CPython 3.13.5 yields SyntaxError, exit 1 before the three tests. Therefore:
PRODUCER_ASSERTED_SUCCESSFUL_EXACT_SCRIPT_EXECUTION = NOT_REPRODUCIBLE_AS_DELIVERED.
Do not accuse producer fraud or infer its internal session actions; it could have used a different edited script not delivered. No original run log or exact alternate script is present in the package to prove this.
This syntax failure does NOT refute the underlying three X5 behavior allegations.

## Existing + independent evidence
Actual X5 SOURCE hash matches historical original and previous R36 audit.
A separately authored fresh independent test harness run against unmodified original X5 source exited 0 and verified:
(A) PROPOSED can store status ADJUDICATED without authority.
(B) ADJUDICATED can be stored with caller-chosen nonempty authority string.
(C) a single by_tags query for six matching records returns six and increments logical_reads six while design target max_reads_per_query=3 is not enforced.
Machine receipt (Operator-local file) SHA256 c53e4bded4a5852de728888d59bd6723b2f79632449c52b0a6d9d11af04ac515. Independent harness SHA256 7c3e528d8619da67aaba76e280c5ef13e63eeb7135bc12773b0f7951ac62d5d2. Source has NOT been patched.
Any future 'second party pass' requires both the source and actually executed exact test bytes, environment, stdout/stderr, exit and independent rerun. Self-labelled independent Grok reports do not authenticate the agent identity.

## Gates and implications
STATUS_EVENTTYPE_COHERENCE OPEN
AUTHORITY_ATTESTATION OPEN
LOGICAL_READ_BUDGET OPEN
SQL_INSERT_SEMANTIC_GUARD DESIGN_CONCERN_OPEN
GROK_REPRO_ORIGINAL_SYNTAX OPEN
MEM02_PUBLIC_PRIVATE_CAS OPEN separately
POST_REPAIR_SECOND_PARTY_RETEST OPEN
Do not include these results in public NEXUS BODYTWIN physical success status. No Cursor remediation started by this PR.
