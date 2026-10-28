# AXIOM Alpha-Node · GitHub API 17-PR receipt census · 2026-10-28

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_LIVE_API_17PR_RECEIPT_CENSUS_20261028_R0
DECISION = KNOWLEDGE_APPEND_C1_SOURCE_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN = 559ab94676fa900409498a8cb2a961bf788deb6b
PREDECESSOR_MAIN = 59bc5b6aeeda70e11f342f3cb745c4da4b651146
PREDECESSOR_ISSUE93_RECEIPT = 6481362322
PREDECESSOR_PR = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/180
SCOPE = EXISTING_R16_RESEARCH_ONLY
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Observation and provenance

A read-only GitHub API audit on 2026-10-28 checked the **bounded, explicitly enumerated** series of owner PRs #164–#180. The pinned source is the immutable GitHub main commit above; no chat or agent summary was used as original evidence. The audit read:

- The 17 individual GitHub PR metadata objects (merged state, merge SHA, changed-file count).
- The 17 actual `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commits/{merge_sha}` objects (single parent, GitHub verification status, added file paths and Git blob IDs).
- The `GET /repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/contents/research/r16/axiom-alpha-node-c1-adaptation-20261012?ref=559ab94676fa900409498a8cb2a961bf788deb6b` directory listing, a **separate GitHub API endpoint**, used to crosscheck the 54 recorded file-path/blob pairs against pinned main.
- All 170 Issue #93 comments returned by the connector, filtered by exact PR URL and receipt predecessor ID; each of the 17 PRs had one matching owner-issued receipt. The 170 comments are an observed inbox inventory, **not** the project-wide handoff denominator.

The 17 merge SHAs, in order, were:

```text
164 b8be4e59f52d8d3739a5d0521e7d7bd80c9d7611 receipt 6460634584
165 1157a2f9d9affc71414ca750333bcd2a1810c9db receipt 6461898518
166 ec66b61010212855a79297ec0673f84582dd8543 receipt 6462252014
167 259aa1bfa0019903268f71f72fc0dc458137a1ad receipt 6463634536
168 2d9bebb5788bdcc47d95a2e68fb955d5cd230356 receipt 6464324854
169 64170faa12da85db8d2c7d5cfcf6995269ea2f8e receipt 6465851951
170 3834ef7eddf08c5b3e0cd0bb662372d8c41e29e8 receipt 6467072191
171 03fe4c62d3bb82c2ce28e36039d16ce6e086731d receipt 6469264130
172 a56c7a8eb4d922df543b534d7d90a5c0ada5bf3a receipt 6470285817
173 c0f69e9fcd2ff54243ffa1bf3aa9d90ce2bda62d receipt 6472047244
174 0bf3ac5a36402ed526cfaf222c011dfe2feea595 receipt 6473538115
175 505afedaf90258c6941ccd54de19746a0d6905c1 receipt 6474399729
176 bd1c230cdc005196a256b5f2c23133b5563479a2 receipt 6476336042
177 1c434c820c30d662ea8d557c7a5b06bb90f75823 receipt 6477928081
178 6e700be6fd408c3d78d3d7e08619b635de92966f receipt 6478246029
179 59bc5b6aeeda70e11f342f3cb745c4da4b651146 receipt 6480022471
180 559ab94676fa900409498a8cb2a961bf788deb6b receipt 6481362322
```

## Bounded result and denominator

| Check | Numerator / denominator | Result |
|---|---:|---|
| Merged owner PR metadata | 17/17 | MATCH |
| GitHub-verified single-parent merge commits | 17/17 | MATCH |
| Consecutive commit-parent links, #165–#180 | 16/16 | MATCH |
| Exact PR-to-Issue-#93 owner receipt association | 17/17 | MATCH |
| Consecutive Issue-#93 receipt predecessor links | 16/16 | MATCH |
| Added file paths and Git blob IDs crosschecked against pinned main directory | 54/54 | MATCH |
| Independently rehashed original bytes/SHA-256 of all 54 files **in this audit** | 0/54 | NOT_EXECUTED |
| Project-wide eligible routine public handoff census | UNKNOWN/UNKNOWN | NOT_COMPUTABLE |
| Project-wide automated handoff rate | UNKNOWN/UNKNOWN | NOT_COMPUTABLE |
| Project-wide full commit/source/test/receipt readback rate | UNKNOWN/UNKNOWN | NOT_COMPUTABLE |

This extends the earlier PR #173 nine-PR metadata sample (#164–#172, 9 PRs / 27 files) to 17 PRs / 54 files, with cross-endpoint Git blob checks. The result is **metadata integrity within the enumerated series**, not independent verification of all original source bytes, independent scientific validation, project-wide completeness, or an automation success rate. GitHub's verified commit status is a platform attestation, not proof of scientific correctness.

## Negative hypothesis, isolated evaluator and falsifier

H0: A contiguous-looking owner receipt series could conceal a broken commit-parent edge, a changed file blob on current main, or a wrong receipt predecessor. The actual API-derived series showed no such contradiction in the specified scope.

An evaluator function separate from the API-extraction loop was executed over the 17 records. It checked sequential PR numbers, parent edges, one parent per signed merge, strictly increasing receipt IDs, predecessor links, unique paths, added-only file status, and cross-endpoint blob equality. Three isolated negative fixtures were created by mutating **one field at a time** while keeping the rest unchanged:

1. Replace PR #173 parent SHA with a different 40-hex value: `PARENT_173` detected.
2. Replace one PR #174 directory blob SHA with a different 40-hex value: `BLOB_...` detected.
3. Replace PR #180 receipt predecessor ID with zero: `RECEIPT_180` detected.

**Observed:** valid source-derived series 0 diagnostics; negative mutations **3/3 rejected**. This was an in-session separate-function evaluator, **not a precommitted frozen oracle or external third-party review**. No claim of a newly deployed production validator is made. A future actual API observation with a mismatching parent, blob, missing receipt, or predecessor falsifies the corresponding scoped integrity claim.

## Boundaries and next actionable gap

The 54/54 result compares two GitHub metadata endpoints; both are controlled by GitHub and are not independent cryptographic rehashes of 54 original file bodies. A complete source/test readback requires fetching the exact 54 file byte streams at their immutable commits, independently computing byte length and SHA-256, checking Git blob identity and test receipts, and preserving an authenticated inventory of **all eligible attempts including failures** before any project-wide 90%/100% metric. Do not treat success-only PR receipts as the complete denominator.

No existing source, validator, evaluator, registry, CI, runtime, Hostinger, WWW, or model state was modified by this research observation. This report is an append-only C1 source audit, not a new pipeline or authority grant.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
