# AXIOM Alpha-Node · Real GitHub CI metadata hybrid replay · C1 · 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_REAL_CI_METADATA_HYBRID_REPLAY_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_QUALITY_EVIDENCE_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=5921454f271c4aaa3fbd5f96656fe126444c001d
PREDECESSOR_PR=257
PREDECESSOR_ISSUE93_RECEIPT=6553860499
MATERIAL_CLASS=PUBLIC_SAFE_RESEARCH_EVIDENCE_NOT_PRODUCTION_INTEGRATION
NEW_PIPELINE=NO
R10_SCOPE=OBSERVATION_ONLY_NO_EXPERT_PROMOTION
```

## Question and counterhypothesis

Question: can the previously published **unchanged** CI-run identity guard V1 process the actual GitHub API check-run identities observed for the seven historical Alpha PR heads #245, #247–#252, rather than only synthetic identities?

Counterhypothesis: the frozen guard will reject legitimate GitHub metadata (e.g. four repeated `validate` names with distinct IDs), or will still accept a duplicate ID, wrong head, pending/failed run, missing run or blank app slug. The test is falsified by rejection of the positive snapshot or acceptance of any targeted negative fixture.

## Pinned executable sources (independently rehashed locally)

- V2 baseline: `alpha_publication_census_matrix_guard_v2_20261101.py` — SHA-256 `12bc7cb28030635fe5d07a2f54e6a17a7e86c5c5f2881ed3f1cc12fc704d9e90`, Git blob `5850473cdddb4ce8d0a32035fc9ff7e453d28132`, 2,754 bytes.
- V1 candidate already on main: `alpha_publication_ci_run_identity_guard_v1_20261101.py` — SHA-256 `65ef7e3773a13b21abb20c7912b81587b151d49e35969be6f7a94653742e8c51`, Git blob `aa4408dc7b34f43328a6dcbe64c953aefc6d7beb`, 2,410 bytes. Frozen before this real-metadata replay.
- New **hybrid** JSON fixture: `alpha_ci_real_api_metadata_hybrid_fixture_v1_20261101.json` — 22,296 UTF-8 bytes, SHA-256 `76a5d9093e6b1e0e3174912b641c144885fcf4761bba888517018172e0a830e9`, Git blob `8e80b650700d4251e9ba6e5f226461292e00c40d`. The independently reconstructed local fixture matched the exact branch Git blob before this report.

The JSON records contain real observed GitHub check-run IDs, names, head SHAs, status, conclusion and app slugs. **All other seven-PR matrix success/file/signature fields are explicit synthetic positive placeholders, not newly rehashed original source proof.** Therefore this is not a full real PR publication or file-provenance E2E test. The guard itself does not authenticate GitHub.

## Connector-returned API response provenance

Each source was read via the connected GitHub API using the exact immutable PR head; all seven returned `total_count=8`, eight records, matching head, `completed/success`, and distinct numeric IDs. An independent second field-by-field GitHub API readback matched the transcribed 56 IDs, 56 names, head bindings, states and app slugs (0 mismatches). The hashes below are of the **UTF-8 response strings returned by the connector**, not independently captured raw HTTP wire bytes. Original full API responses are **not archived**.

| PR | Immutable PR head | Connector response bytes | SHA-256 of connector-returned response |
|---|---|---:|---|
| 245 | `0990f754c960b66cb14b6538700fcb385a5791b7` | 24380 | `5eb7fa6a2b450d2da10b423d3f08dbab608aba22853aaf28cb3cbccf63b7bf7d` |
| 247 | `1fb6c2945a6d5c61157492d52ebeb210be231ace` | 24380 | `daa5cd03508393e53865168eea604b749f7e0f6d76f041f582fa7b9cc79fa53f` |
| 248 | `a2957c19b60c8875471c3997f10627cfefce6739` | 24380 | `f635e639db510dc6db4df49ba4bc81d5caa917736696a776d218b2085dc3a1be` |
| 249 | `b82af0f40a505fd57987c8acbe6ffbce954a750d` | 24380 | `1fdbb7254b491bb9aea12dd8a9a6844ce668c65bd9bb161d60b1cda6ce90cc6b` |
| 250 | `c846e4d165628b63f96ab63be525dff89a4cd055` | 24380 | `cfe7cc1100ba49ce8c989a60bae0e9fe8ea690a0f0ce36282241f48582cb7435` |
| 251 | `0a95723743e73adc2e850ee252a453a2e771df03` | 24380 | `1e3c992c3dfdf063617e72b8d7d9b449f467545d8c7c02140910e9c048bb0532` |
| 252 | `1c17c291fce1d5a0c599a3d0c2166909b52fede9` | 24380 | `6d639e295fa622da3078e889d462872fd4ae4a894a37e549f881ccbb305873b3` |

SHA-256 implementation passed the standard empty-input and `abc` test vectors. The seven connector-returned source bodies may be mutable on later API reads; the normalized fixture is the committed replay object, **not** a preserved copy of those original bodies.

## Isolated independent subprocess replay and metrics

The unchanged Python V1 guard and unchanged V2 baseline were reconstructed from pinned GitHub file contents; their exact SHA-256 and Git blob IDs matched the repository originals. The separately authored replay adapter exercised the **byte-identical committed hybrid JSON fixture** in independent Python subprocesses (exit code 0 for every invocation).

| Fixture | V2 accepted? | V1 accepted? | Expected |
|---|---|---|---|
| Positive: 56 observed GitHub check runs, repeated names, distinct IDs | YES | YES | YES |
| Duplicate check-run ID | YES | NO | NO |
| Wrong PR-head binding | YES | NO | NO |
| Pending check run | YES | NO | NO |
| Empty app slug | YES | NO | NO |
| Missing check run | YES | NO | NO |
| Failed check run | YES | NO | NO |

**Measured result:** 7/7 expected subprocess outcomes PASS, including 6/6 negative fixtures rejected by V1 versus 0/6 rejected by V2; 56/56 observed run IDs unique, 7/7 PR-head check-run inventories structurally accepted. Previous real-data guard replay was `NOT_EXECUTED`; this iteration establishes a **bounded hybrid metadata replay**, not a new production false-acceptance rate or complete real publication validation.

Reproduce positive control from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_ci_run_identity_guard_v1_20261101.py < research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_ci_real_api_metadata_hybrid_fixture_v1_20261101.json
```

To falsify, mutate a single `check_runs` entry (duplicate `id`, wrong `head_sha`, `status=queued`, `conclusion=failure`, blank `app_slug`, or remove an entry) and rerun the unchanged guard. Expected output is `accepted=false`. The prior V2 baseline accepts all six of these mutations when the synthetic positive matrix flags remain true.

## Scope and decision

This is **one** bounded quality-evidence candidate, not a new runtime, CI workflow, pipeline root, external-agent slot, or permission change. No historical file was edited. The GitHub API source is public check-run metadata only; no secrets, private returns or biological data were used. The existing C1 claim ceiling is unchanged. Production integration, real file/receipt provenance end-to-end, GitHub required-ruleset enforcement, external scientific validation and GitHub→WWW parity are **NOT_ESTABLISHED** by this replay.

Automation target: `AUTOMATION_RATE=NOT_COMPUTABLE` because the complete eligible-attempt denominator is unavailable. Project-wide full publication readback: `NOT_COMPUTABLE`. The seven-PR historical cohort is not that denominator. Publication requires separate CI, actual main readback, and append-only Issue #93 receipt; a PR alone is not success.
