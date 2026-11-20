# R36 Collective Experience Ledger | adversarial repair contract
OBJECT = NEXUS_OMEGA_AXIOM_R36_COLLECTIVE_MEMORY_PRIVACY_AUTHORITY_AND_QUERY_GATES_20261118_R0
STATE = NEGATIVE_TESTS_CONFIRMED_ON_SYNTHETIC_PROTOTYPES_REMEDIATION_NOT_AUTHORIZED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
DEVICE_DATA = NO_PRIVATE_RAW_IN_PUBLIC
CONSCIOUSNESS_OR_AUTONOMY_CLAIM = NONE

## Original source witness
R35 TAR X4B code reproduces a PUBLIC pointer to a PRIVATE content-addressed original. R35 RECONC X6 synthetic 'SALTED_COMMIT' claimed MEM02_PASS but published code has predictable default key, and its attack checks only SHA256(candidate bytes), never key-aware reconstruction. Exact independent R36 check on original source reproduced exposed-key candidate confirmation.
R35 RECONC X5 original SHA256 54d18bb0f1106275d66eced28866967a984e84e94d8abd452f07611538d70ad5. Exact R36 independent synthetic code import demonstrates:
- event_type=PROPOSED, status=ADJUDICATED accepted without authority.
- event_type=ADJUDICATED accepted using any nonempty caller-supplied authority string, without externally verified signing.
- a single by_tags request with four matches performs four logical reads, despite three reads proposed as per-query budget.
- prior R35 report of 'logical_reads=5' was a CUMULATIVE suite counter, not proof of single-request violation; new four-match controlled test supplies the actual witness.
These do not demonstrate an attack on an existing production NEXUS service; do not overclaim.

## R36 candidate repairs (NOT implemented)
MEM-A status authority: event_type/status transition pairs enforced via explicit state machine, separate actor identity and scoped public-key signature verification, canonical signed exact record bytes, replay/sequence/expiry/revocation. No user-provided 'AXIOM' string suffices.
MEM-B sealed private custody: raw originals and content digests remain in a private ACL store; public data are separately redacted and content-hashed from the PUBLIC ARTIFACT, never the private source. No raw private SHA in public IDs, links, error pages, archive headers or feed item.
MEM-C source transparency: keep authenticated private source commitment inside private audit domain; publish only controlled public-safe content digest and bounded metadata. Distinguish verifiable public content from proof of a private underlying original; avoid overstating public auditability.
MEM-D query budget: per-request atomic counter covers all DB transactions including nested exact lookups, tags, candidate scans, walks, bytes and wall-clock; stop early fail closed before overspending, including >=4 matches, cyclic supersedes, high entropy and concurrent requests. No recursive semantic/web fallback.
MEM-E causal memory: append-only claims + contradiction/supersedes links with immutable original and provenance classes. Correction links not last-write-wins. Negative evidence and UNKNOWN remain available.
MEM-F independent ablation: typed ledger vs a no-memory baseline and unrestricted-free-search control, 100/1000/10000 corpora; precision/recall and false-confidence, total cold/warm latency, cost, abuse and privacy metrics preregistered. Runtime benchmarks on one Windows build do not establish cross-machine performance.

## Minimum adversarial tests
MEM-R36-N01 PROPOSED can never self-label ADJUDICATED.
MEM-R36-N02 arbitrary nonempty 'authority' string cannot confer reviewer/owner permission.
MEM-R36-N03 public index never exposes private original source bytes/digests or correlation even with known candidates.
MEM-R36-N04 adversary knows every shipped source line and public protocol, cannot recover any private signing secret.
MEM-R36-N05 4+ tagged records cannot exceed query read budget 3, or return explicit budget exhaustion.
MEM-R36-N06 immutable contradictory A->B->C retains all versions, plus revoked attacker receipt.
MEM-R36-N07 stale/tampered snapshot, NaN, Unicode ambiguity, path traversal and duplicate keys fail closed.
MEM-R36-N08 externally untrusted feed text cannot execute instructions or impersonate a reviewer.
MEM-R36-N09 exact original source hashes and real independent binary/test logs must match.
MEM-R36-N10 no private and public namespaces are merged when archiving historic records.

Stop/hold on first authority/privacy leakage, any lack of original source, any public archive of private OPPO measurements, or any unverified claim-promotion. R36 approval requires source-exact second-party replay and a documented fallback; receipt SHA alone is custody, not security proof.
