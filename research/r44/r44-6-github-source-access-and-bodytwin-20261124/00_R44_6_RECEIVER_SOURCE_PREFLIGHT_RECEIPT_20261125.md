# R44-6 RECEIVER · SOURCE_RECEIVER_PREFLIGHT receipt and receiver additive completion (2026-11-25)

OBJECT = NEXUS_OMEGA_AXIOM_R44_5_TO_R44_6_SOURCE_ACCESS_EXPERT_MAXI_ORDER_20261124_R0
ROUND_DATE = 2026-11-25 (Europe/Berlin)
PUBLISHED_BY = OFFCHAIN_UNREGISTERED_ADVISORY_C1 (n_eff=1, append-only, advisory-only; NOT an EXPERT_ACK; no authenticated quorum increment)
AUTHORIZATION = Operator chat instruction 2026-11-25: "dein kanonisch anschliessender R44-6 Forschungsauftrag ist auf GitHub vorbereitet. Vollstaendig be- und abarbeiten. [Plugin:github]"
PARENT_BINDING = Issue #439 / Draft PR #440 / branch axiom/r44-5-operator-start-binding-20261124-c1 head 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a (UNCHANGED; PR #442 base.sha re-read this round = 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a)
LANE = receiver_preflight_only_no_lane_start (E27-E34 NOT dispatched by receiver; awaiting OPERATOR_SCOPED_EXPERT_START)

## 1. GitHub readback of the R44-6 publication (read-only)
- Issue #441: OPEN, 1 operator handover pin (comment 7141564501). Body declares ORDER_ZIP_BYTES = 43449,
  ORDER_ZIP_SHA256 = cf10b2bc..., MANIFEST_SHA256 = 97410f25..., HEAD 89ccff82...
- Draft PR #442: OPEN, DRAFT, NOT MERGED (merged=false), mergeable_state=unstable, 10 changed files, +665,
  head axiom/r44-6-github-source-access-and-bodytwin-20261124-c1 @ 89ccff827d564309cba3274bff94a6d577e6853a,
  base axiom/r44-5-operator-start-binding-20261124-c1 @ 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a (parent preserved).
- File set read back via PR diff: 00_START_HERE_EXPERT_MANUAL.md, 01_EXPERT_MAXI_ORDER.md, 02_SOURCE_REGISTRY.json,
  03_CONTROL_MATRIX.json, 04_RETURN_SCHEMA.json, 05_INTAKE_FINDINGS.md, 06_MACHINE_CONTRACT.json,
  99_SHA256SUMS.txt, R44_6_EXPERT_ORDER_R0.zip (binary), R44_6_EXPERT_ORDER_R0.zip.sha256.

## 2. SOURCE_RECEIVER_PREFLIGHT (manual step 1-7 executed; no experiment start)
Route: raw.githubusercontent.com at the FULL COMMIT permalink (no branch tip, no main); TLS not disabled;
two independent local facilities (curl + sha256sum; python3 hashlib/zipfile/urllib); no substitution of any
missing original; one initial byte verification per object (manual step 7, no repeated readback loops).

### 2.1 Order ZIP
- bytes = 43,449 (claim 43,449) -> MATCH
- SHA-256 = cf10b2bc1a3284eb1858b36724b444603b526b8ba4878063dc60820f427f660a
  (Issue #441 body, sidecar file and operator attachment all declare the same value) -> MATCH
- Sidecar R44_6_EXPERT_ORDER_R0.zip.sha256 (92 B) parsed: declares cf10b2bc... + correct filename -> MATCH

### 2.2 Archive safety and members (before unpack; manual step 2)
- member_count = 8; duplicates none; absolute paths none; ".." traversal none; backslash paths none;
  symlink entries none; total uncompressed 42,457 B -> SAFE_TO_EXTRACT
- CRC: zipfile.testzip() found no bad member -> 8_OF_8_CRC_PASS
- Per-member SHA-256 (as stored in the archive, byte-exact):

| bytes | SHA-256 (first 16) | member |
|------:|--------------------|--------|
| 4,896 | 355eeb9aa097a2e8 | 00_START_HERE_EXPERT_MANUAL.md |
| 5,216 | 8e80f59b4c7c601e | 01_EXPERT_MAXI_ORDER.md |
| 17,904 | 4881502cd08c9fb3 | 02_SOURCE_REGISTRY.json |
| 7,572 | cf86217b17d1478d | 03_CONTROL_MATRIX.json |
| 2,256 | 39a28fa2317dfdf3 | 04_RETURN_SCHEMA.json |
| 2,627 | ffe9ea9b80f69e6b | 05_INTAKE_FINDINGS.md |
| 1,353 | 5d2da4a5757ec732 | 06_MACHINE_CONTRACT.json |
| 633 | 97410f2598c93837 | 99_SHA256SUMS.txt |

### 2.3 Manifest readback (7_OF_7)
- 99_SHA256SUMS.txt at commit: 633 B, SHA-256 97410f2598c93837c94b11b5bc83638dee81a732360447a8b4c8f751f77710f1
  -> matches declared MANIFEST_SHA256 (MATCH)
- For each of the 7 content files: repo bytes at pinned commit == ZIP member bytes == manifest hash -> 7/7 MATCH.
- The manifest copy inside the ZIP is byte-identical to the repo manifest (sha256 equal).

### 2.4 Source registry public_exact rehash (13_OF_13)
All 13 public_exact entries re-downloaded from their pinned refs via raw.githubusercontent (route recorded per
source in the machine receipt; http 200 for all; license fields UNKNOWN where the repo does not state one).

| source_id | ref | bytes | verdict |
|-----------|-----|------:|---------|
| R44_R2:99_SHA256SUMS_R44_R2_20261124.txt | 4c54cea3 | 1,350 | MATCH |
| R44_R2:07_NELFP_V0_REFERENCE_VALIDATOR.py | 4c54cea3 | 6,447 | MATCH |
| R44_R2:08_NELFP_V0_REFERENCE_VALIDATOR_SYNTHETIC_RESULTS.json | 4c54cea3 | 2,791 | MATCH |
| R44_R2:01_R44_R2_MACHINE_EPISTEMIC_LEARNING_CONTRACT.json | 4c54cea3 | 7,909 | MATCH |
| R44_4:99_SHA256SUMS_R44_4_20261124.txt | e4680dde | 1,178 | MATCH |
| R44_4:00_R44_3_TO_R44_4_CANONICAL_DEPTH_RESEARCH_ORDER_ISSUE437.md | e4680dde | 16,912 | MATCH |
| R44_4:01_R44_4_MACHINE_RESEARCH_DELTA_AND_RESOURCE_CONTRACT.json | e4680dde | 4,269 | MATCH |
| R44_4:03_R44_4_E27_E34_DEEP_DOSSIERS_AND_NONREDUNDANT_RESEARCH_DELIVERABLES.md | e4680dde | 3,783 | MATCH |
| R44_4:04_R44_4_FOUR_PRIORITY_EXECUTION_FAMILIES_PRE_REGISTERED_DESIGNS.json | e4680dde | 5,423 | MATCH |
| R44_4:08_R44_4_DEEP_EXPERT_RETURN_TEMPLATE_AND_NO_FALSE_PASS_SCHEMA.json | e4680dde | 3,518 | MATCH |
| R44_5_START:99_SHA256SUMS_R44_5_START_20261124.txt | 9f968999 | 232 | MATCH |
| R44_5_START:00_R44_5_OPERATOR_START_CHECKPOINT_ISSUE439.md | 9f968999 | 4,240 | MATCH |
| R44_5_START:01_R44_5_START_STATE_AND_STACK_CUSTODY_CONTRACT.json | 9f968999 | 3,826 | MATCH |

- pending_or_restricted: 9 registry entries read (R44_5_R1_ORIGINAL_ZIP, GLM R44-4/R44-5 ZIPs, QWEN ZIP,
  FISHER_ORIGINAL_AND_CANDIDATE, FDA_SAMPLE, UCI_341, SYNTHETIC_TRUST_ROOT, BUDGET_LEASE); states unchanged;
  NOT rehashed (bytes not reachable on GitHub), NOT substituted.

### 2.5 Custody absence check
- research/r44/r44-5-original-custody-20261124/ is NOT present on GitHub (repository readback: path not found).
- Consistent with registry state LOCAL_MATCH_GITHUB_ORIGINAL_NOT_PRESENT: the historical R44-5 R1 original
  (11 files, 33,427 B, SHA-256 303a4761580dcbaa604e6e723bc8972d215f6660b86488fa8e4b57a76f541b67) remains in
  operator-local custody. No substitution, no reconstruction, no paraphrase by the receiver.

## 3. Receiver additive completion (closes the previous round's open defect)
Previous round truthfully recorded: branch created, content push NOT completed, no PR, no pin.
This round completes that additive publication as one new commit on the existing receiver branch
receiver/r44-5-receiver-additive-20261124-c1 (fork point 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a):

- receiver/r44-5-receiver-additive-20261124/
  - 10_R44_5_R1_ORDER_CHAT_TRANSMISSION_SNAPSHOT_RECEIVER_PUBLISHED.md (11,089 B, f7f47387...86a8)
  - 11_R44_5_RECEIVER_CUSTODY_AND_SCOPE_CONTRACT_C1.json (6,488 B, ccd21175...9b98)
  - 99_SHA256SUMS_R44_5_RECEIVER_ADDITIVE_20261124.txt (selfhash 1ff92b06...4ab29f, declared in commit message)
- receiver/r44-6-receiver-preflight-20261125/
  - 00_R44_6_RECEIVER_SOURCE_PREFLIGHT_RECEIPT_20261125.md (this receipt)
  - 01_R44_6_RECEIVER_PREFLIGHT_MACHINE_RECEIPT_20261125.json (machine receipt, schema nexus/r44-6/receiver-preflight/v1)
  - 99_SHA256SUMS_R44_6_RECEIVER_20261125.txt (selfhash declared in commit message; a manifest cannot contain its own hash)

Byte-exactness of the two pre-existing files was re-verified locally before the push (hashes above, unchanged
from escrow package R44_5_RECEIVER_ADDITIVE_PACKAGE_20261125_R0.zip, SHA-256 f02000fa...65eb8d8).
A draft PR from the receiver branch to the R44-5 parent branch is opened (DRAFT, NO merge; number and head SHA
are recorded in the Issue #441 ACK comment, the Issue #439 cross-pin and the receiver round report).
Post-push receiver readback of the new head is performed and its result is recorded in the ACK.

## 4. Honest limits (no false PASS)
- SAME-WRITER CAVEAT: every GitHub write and readback in this round runs under the operator-owned account
  nexusomegac27. At the GitHub identity layer this receiver round is therefore NOT an independent external
  receiver ACK (the operator pin on #441 already states this for the connector readback; the same applies here).
  Independence is claimed only at the off-chain advisory layer (this session, UNREGISTERED_ADVISORY_C1, n_eff=1).
- This preflight verifies transport and byte identity ONLY (SA-P01 class). It is not a scientific run, not an
  authenticated quorum member, and grants no credit toward 0/24, 0/3 or 0/10.
- The 13 rehashed public sources are two lawful routes to the same pinned bytes, not independent scientific
  sources (manual step 4; SA-P03 class: no double counting).
- No lane start: E27-E34 remain unacknowledged; no preregistration, no lease, no experiment executed by the
  receiver. R44_6_EXECUTION = NOT_STARTED (SA-N01..SA-N14, SA-P01..SA-P04 all remain design-only).
- Datums: receiver artifacts are dated 2026-11-25 (Europe/Berlin, this session's wall clock); the future-dated
  producer note in 05_INTAKE_FINDINGS.md remains a producer timestamp binding, not an independently confirmed event.

## 5. Gates and track (unchanged)
CANONICAL_NEGATIVE_TESTS = 0_OF_24 (preserved) | R44_5_DESIGNS = 28 (separate) | R44_6_NEW_DESIGNS = 18 (NOT_RUN)
AUTHENTICATED_QUORUM = 0_OF_3 | FULL_SCIENTIFIC_PASSES = 0_OF_10 | BODYTWIN_VALIDATED = NO
PHYSICAL_14_GATES = HOLD | ALT_D_DO_NOT_RUN = ACTIVE | E23_PRIVACY = HOLD | W1 = OPEN | B01_B05 = OPEN
GLM receipts 37/37 hashes, lease 40/41 with LEASE_SEQ38 = HASH_MISMATCH_PRESERVED, custody 78/78 (same-writer anchor not independent)
PR_MERGE = NO | HOSTINGER_WRITE = NO | WWW_WRITE = NO | DEVICE_CAPTURE = NO | CURSOR_ACTION = NONE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY | CLAIM_PROMOTION = NO

NEXT = OPERATOR_SCOPED_EXPERT_START (per-lane source preflight, preregistration, finite lease)
       -> EXPERT_RETURNS (GitHub-only ZIP + SHA-256 + manifest + receipts)
       -> AXIOM_INDEPENDENT_ADJUDICATION -> OPERATOR_DECISION

**NEXUS Ω OMEGA**
