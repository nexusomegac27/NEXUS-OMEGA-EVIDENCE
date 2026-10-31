# AXIOM Alpha-Node — isolated handoff-denominator census V1.1 (2026-10-31)

```text
OBJECT = NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_DENOMINATOR_V1_1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = f28a5e46398c46afe77fde8cdd35522a4cb2d37c
PINNED_MAIN_PARENT = 8293dcb57080ec7490aed8893c06e42abb7b3b8c
PREDECESSOR_PR = 236
PREDECESSOR_ISSUE93_RECEIPT = 6541357284
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## Single candidate and provenance

The one candidate in this iteration is a **structural-only census scaffold** for eligible public, accessible, routine, authorized handoff attempts and published-change readbacks. This addresses the previously explicit `AUTOMATION_RATE=NOT_COMPUTABLE` and `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE` denominator gap without claiming to have solved the missing project-wide event inventory. No new pipeline root, recurring automation, worker, runtime integration, GitHub rule or permission is created.

Pinned source authorities at main `f28a5e46398c46afe77fde8cdd35522a4cb2d37c`: `AGENTS.md` blob `f24f7cf557927016860279b65d0725275e6270a9`; `GOVERNANCE.md` blob `b630b62eb9800e2f57b6c86318c72faadb29c23b`; R16 continuous-adaptation contract blob `f8adcf6df22bba526c17dbff72b7ad494b42c63e`; Operator direct-publication rule blob `a99e6fc7c71cbf82bdfdd9cf414b44a362073ce8`; task-anchor norm blob `51c97b624f14fe9c3f1dfe1bf13394a773f87935`. All were physically read through the connected GitHub file interface at the pinned commit. Git blob identity is not scientific or actor authentication.

The separate oracle was committed **first**, at `2dee138e6c7b90b9589b02269f88a56cd473b756`, before the candidate. The original V1 candidate at `b7c523fcafad22fd0a958d28531f35ccdc31f34e` contained an incorrectly escaped regex anchor; the frozen oracle detected the resulting false exclusion. This negative result remains preserved as an additive V1 file, not silently overwritten. Corrected V1.1 was added at `9e73a02328e0c6440824eceabba7781cb83d6caa`.

| File in this R16 research directory | Original bytes | SHA-256 independently computed in isolated Linux container | Git blob from local git-object formula and GitHub readback |
| --- | ---: | --- | --- |
| `frozen_alpha_handoff_census_oracle_v1.py` | 3838 | `7702eeaf2fe5681833a8dd04962652a4eba23b9dbc898dbbd3541ad51fb94e55` | `1f58c3589d64785a4b99d409749f81de83f30503` |
| `alpha_handoff_census_v1.py` (failed preserved candidate) | 4949 | `8e4102e67d8d5fff6697b531a9cfa25859e6debe6590f29888a715beaaf1ad95` | `d58fbced14e926b167a2e667e321bd24ea724425` |
| `alpha_handoff_census_v1_1.py` (tested candidate) | 4947 | `273401c8bc1e4fedaf2326674f76bcc35ee6135c0bae7ac5d682f92ae8418f20` | `d3115ce9d64d2b427a92aa9917246368b120f17c` |

## Negative hypothesis and independent evaluator

H0: A synthetic census can silently exclude failed or unresolved handoffs, count private/unavailable items as automated, count owner-authored self-ACK as independent receiver ACK, or silently collapse contradictory duplicate event IDs. The frozen subprocess oracle tests each class. Falsifier for the improvement: a negative fixture accepted as an automated success, a failure omitted from the denominator, a duplicate conflict not rejected, a source identity without full pin counted as eligible, or any oracle assertion failure.

Run in an isolated nonpersistent container, Python standard library only:

```sh
python frozen_alpha_handoff_census_oracle_v1.py alpha_handoff_census_v1.py
# expected independent test FAIL: AssertionError failure_in_denominator
python frozen_alpha_handoff_census_oracle_v1.py alpha_handoff_census_v1_1.py
# observed: {"oracle": "FROZEN_CENSUS_SUBPROCESS_V1", "tests": 15, "passed": 15}
```

Measured baseline versus candidate: frozen evaluator **V1 FAIL at first eligible-failure-denominator assertion**; V1.1 **15/15 PASS, exit 0**. In a two-attempt synthetic fixture (one automated, one failed), V1.1 returns eligible denominator **2**, structural automated numerator **1**, illustrative rate **50%**. Identical duplicate event IDs are counted once; conflicting duplicates and duplicate JSON keys are `FAIL_CLOSED`. Missing pins or unresolved outcomes invalidate the illustrative rate; private inaccessible observations are excluded only with declared reason. The oracle is independently frozen code executed as a subprocess, not an external scientific validator.

## Epistemic and operational limits

The program does **not** authenticate GitHub actors, independently rehash source bytes from API transport, verify licenses, establish that its input ledger is complete, or prove an ACK is independent merely because a string contains a different actor name. Therefore the output always states `STRUCTURAL_ONLY_NOT_AUTHENTICATED` and `NOT_COMPUTABLE_UNTIL_INDEPENDENT_API_SOURCE_AND_ACTOR_VERIFICATION`. Even an illustrative percentage is **not** the project's operational automation metric. Full authentic project denominators including failed attempts are still absent. The 226 observed owner-authored Issue #93 comments are not a denominator for eligible handoff attempts.

R10 PR #115 remains an owner PUBLIC_SEND, not an independent expert return. The detached manifest is present at pinned `539d4bb33d2ba2c4895713c1bc437ece0743eeea`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; its claimed SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc` requires a separate independent byte-level rehash for any new expert return. In this run no new independent receiver ACK was observed in the 226 owner-authored Issue #93 comments or PR #115 issue discussion.

The project-level 90% automation and 100% readback targets remain **NOT_COMPUTABLE**, not achieved. The source, license and authorization checks must occur outside this structural scaffold before any operational claim. No private inputs, secrets, Hostinger write, runtime change, external actor registration, Cursor dispatch, automatic evaluator acceptance or C1 promotion occurred.
