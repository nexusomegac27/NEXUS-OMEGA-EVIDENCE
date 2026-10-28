# NEXUS OMEGA · AXIOM Alpha-Node · PR/receipt chain audit · 2026-10-28

```text
OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_CHAIN_RECONCILIATION_20261028_R0
DECISION=TESTED_C1_ISOLATED_METADATA_RECONCILIATION_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=a56c7a8eb4d922df543b534d7d90a5c0ada5bf3a
PREDECESSOR_ISSUE93_RECEIPT=6470285817
PUBLICATION_MAIN_AND_RECEIPT=PENDING_SEPARATE_READBACK
PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE
PROJECT_READBACK_RATE=NOT_COMPUTABLE
```

## Single bounded improvement

Prior receipts described each Alpha-Node PR separately. This iteration introduces a **separate offline chain-reconciliation witness** and a pinned, nine-record public metadata snapshot for GitHub PRs #164–#172. The witness rejects missing PR records, inconsistent PR merge/receipt main hashes, broken receipt predecessors, wrong main parents, duplicate receipt IDs, and contradictory one-ahead/zero-behind/three-additive-file comparisons. It does not authenticate its caller-supplied snapshot or validate file bytes, CI, external expert identity, or the project-wide handoff census.

**Negative hypothesis:** narrative-only per-PR readbacks do not automatically establish cross-PR causal continuity. A bounded metadata reconciliation should detect a broken parent, receipt or GitHub compare relation.

## Original GitHub API response provenance

The GitHub connector fetched the original UTF-8 JSON response text from official REST endpoints `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pulls/{number}` and `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/comments/{id}`. The byte counts and SHA-256 below were calculated over the returned JSON text, not reconstructed chat summaries. The GitHub JSON responses are mutable snapshots, not cryptographically signed immutable assets. Original source bytes were inspected in this execution; the published derived fixture is not the raw API response.

Main ref JSON: **366 bytes**, SHA-256 `53f9a2b2091173280511c1d99e4fcf889615230447147ce0cea18a0789848517`, observed main `a56c7a8eb4d922df543b534d7d90a5c0ada5bf3a`.

| PR | PR response bytes / SHA-256 | Issue #93 receipt | Receipt response bytes / SHA-256 |
|---|---|---|---|
| 164 | 19540 / `4ce0e1ffaed59fec3537cba7ed05be6ad73fcfc76847243a7d708e33e6b092a5` | 6460634584 | 6746 / `6160444c10e76a221da71126df9969bc8444b7b27b9bc624e9d6af6e155b8888` |
| 165 | 19801 / `810359d2af82566f6e732877fa59b0a3e1a6b5a2b4a3574197f8c3b52167fab2` | 6461898518 | 6406 / `c3edd3671f593926360da73f5f0e4b75ac7042b46907c10775f6e6cf796804bb` |
| 166 | 20177 / `49da1d472dd86614c5b75782528147b29808392d83a1049a79bef1612f64ed64` | 6462252014 | 7219 / `ac0fad4363ef39e78d02086de6cdc068fbdfecd7bc445d72461fb050b63fbc24` |
| 167 | 20197 / `05451e7efa2a565c462ffce1188b657058138a6441e693995f77fd2784ce2656` | 6463634536 | 7770 / `527db2157171c27b01de70723d6e362d927803b5b1cde94ff9d0bf8cc6a0ff57` |
| 168 | 20136 / `fea0db9c40aff49e85aafb848c6b31b4899db9b577def18f4ce9f0b9de52576a` | 6464324854 | 7132 / `52ee8476e89542dbeb4b79706bc4447a4302aa993fc378af2e75cf0cb9e3f67f` |
| 169 | 20012 / `1db2fabf71ce3148d6aee325b76695cf994388002a3df54cd4c6e7749ffd66a9` | 6465851951 | 6376 / `9af30628f5048e23f631f35cac33d866c0269dfac83856c04cd1e8a024258756` |
| 170 | 19962 / `362446a4eb88c9b961afa535b0af4d45a63b865297db23d8611cf109f9e7ebcf` | 6467072191 | 6750 / `f986ec1922754e31fe92f1cb29bd89fff0b3328876a383bf77cad79586889139` |
| 171 | 20000 / `cca037a4ba2f9c1ba9f1588af12e5c3cf961bd3733cae14c4ccad53971781c76` | 6469264130 | 6813 / `3384ca85aba1afeee73de031acd6d340611287d4b741b71d00e9b267b82deb65` |
| 172 | 19709 / `4ffd25048072d7d5741912e5caf1cb089f88e1eb6af066849157749e84ca6472` | 6470285817 | 6645 / `a79ffc0ddad6fb8f0a66e1615a7cbbcdb5fbfc7745bdc5c638af22f6cf421ab8` |

The derived normalized input `alpha_receipt_chain_observed_snapshot_20261028.json` is **4,693 bytes**, SHA-256 `f9c78661d0f026ff9fea26a6ad60291e382c71b2d95403e26519e32c8d59842a`. It binds a selected nine-PR window, not a complete project inventory.

## Independent tests and actual scoped observations

GitHub PR records, Issue #93 comments and nine independent `compare_commits` API results were cross-checked. For each adjacent pair, GitHub reported ahead=1, behind=0, three files added, none modified/deleted. **9/9** selected PR merge SHAs matched their receipt main SHAs; the predecessor receipt IDs and adjacent main parent claims formed a continuous chain.

The frozen independent Python subprocess evaluator (no candidate imports) executed **16/16 PASS** in the local isolated environment. The actual nine-record derived snapshot produced `metadata_chain_match=9/9`. Three separately injected negative fixtures (wrong receipt main for #168, broken predecessor for #171, wrong added-file count for #166) were rejected **3/3**. The evaluator was committed to the owner branch before the candidate; this is not independent third-party validation.

Reproduce from this existing R16 research directory:

```bash
python frozen_receipt_chain_oracle_v1_20261028.py -v
python alpha_receipt_chain_reconciler_v1_20261028.py < alpha_receipt_chain_observed_snapshot_20261028.json
```

Before: nine separate one-at-a-time reports with **no combined machine-checked cross-PR chain**. After: **9/9 metadata-consistent** in this exact selected window. The denominator **9** covers only PRs #164–#172, not all authorized routine handoffs. The project's actual automation numerator/denominator and full published-change source/test readback denominator remain **NOT_COMPUTABLE**.

## Falsifiers and boundaries

Any authentic PR/receipt/compare mismatch, missing original API response, or failing frozen fixture falsifies the scoped consistency result. A jointly fabricated but internally consistent input can still pass: `api_origin_authenticated=false`, `source_file_byte_readback_verified=false`, `external_receiver_ack_established=false`. All nine receipts are owner-authored, not independent expert ACKs. No new R10 expert receipt was observed in PR #115's comments, reviews or review threads. The pinned R10 manifest and its source boundaries remain unchanged.

No production Steward, repository governance, actor registry, runtime, Hostinger, WWW, node reset, external worker, source overwrite, or claim promotion. This is isolated C1 research only.
