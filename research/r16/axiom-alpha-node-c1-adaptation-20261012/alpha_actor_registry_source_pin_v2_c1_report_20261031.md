# AXIOM Alpha-Node — operator registry source pin for Issue #93 actor census V2 (2026-10-31)

```text
OBJECT=NEXUS_OMEGA_ALPHA_ACTOR_REGISTRY_SOURCE_PIN_V2_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=5df8953165087fabf50aba52eb15e3668f50d940
PREDECESSOR_MAIN=7500742672bca68c5c84e524a1262f9b786a7aef
PREDECESSOR_PR=230
PREDECESSOR_ISSUE93_RECEIPT=6537747640
FROZEN_ORACLE_FIRST_COMMIT=4ff21e59fb07b8b76c3e39832868dfa962cebbf6
CANDIDATE_SECOND_COMMIT=a44b2a8e6d18194dc9527243e963241f09ef5cd0
PRODUCTION_INTEGRATION=NO
```

## OBSERVE → ORIGINAL_BYTES / PROVENANCE

Source of authority: pinned `main`, `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha-Node adaptation contract, owner C1 publication directive, task-anchor norm, repository-order contract, research pipeline, and the passive Issue #93. At this observation, GitHub API returned **220/220 owner-authored Issue #93 comments**, latest ID `6537747640`; R10 PR #115 remained OPEN, with zero PR comments, reviews and review threads. These are GitHub metadata observations, not expert authentication or a handoff denominator.

Pinned V1 source: `alpha_issue93_actor_provenance_gate_v1_20261031.js`, **3,444 bytes**, SHA-256 `efb132f95e7b1e7fa5062e762a964835ecf3f59925313779acf6b5ee627e5a90`, Git blob `71c06ae01a0d8f4e7f4238413d78a82cd980c44b`. Exact GitHub bytes were reproduced locally and independently rehashed.

Actual owner registry: `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json`, **2,178 UTF-8 bytes**, SHA-256 `d257be3faef8336e30f688d440758b051d93dd2a29ece693882af4ed8e463e7c`, Git blob `1fabcab7f556e83621a3676ddfb3d11cdd964b55`, pinned to `main` above. `external_actor_allowlist=[]`, `default=DENY`. These are actual fetched source bytes, not an owner summary. Git blob SHA-1 does not establish independent GitHub transport authentication.

R10 detached manifest at immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea`: 4,588 UTF-8 bytes, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`; independently rehashing its SHA-256 was **not performed in this iteration**. No new authenticated independent receiver return was observed.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

H0: The V1 classifier accepts a caller-supplied `registeredActors` array without independently binding it to the actual operator registry. A synthetic caller can inject `fabricated-expert` and cause a formally complete handshake to be labeled `REGISTERED_ACTOR_RETURN_CANDIDATE_BYTES_UNVERIFIED`, even though the physical registry is empty. This does **not** yield an ACK in V1, but it mislabels the actor's registration provenance.

The frozen black-box evaluator reproduces that behavior: **V1: 1/1 injected actor labeled registered candidate**. V2 accepts only `{comments,registry_utf8}`, verifies the raw Git blob against the independently pinned registry ID, enforces the current default-deny/empty allowlist, rejects any caller `registeredActors` override, and then invokes the unchanged V1 census. **V2: 0/1 injected actor labeled registered**. Missing, altered, truncated, or policy-divergent registry bytes fail closed.

## ISOLATED CANDIDATE → INDEPENDENT TEST

The independent evaluator was committed **first**, before the V2 candidate, and remained unchanged. It runs baseline and candidate in separate Node.js subprocesses, checks exit codes, stdout JSON, stderr and exact classifications; it is not imported by the candidate.

- Frozen evaluator: `frozen_alpha_actor_registry_pin_oracle_v1_20261031.js`; **3,125 bytes**, SHA-256 `21781961b08177b92c01b6d1ef026c6745eaa13ea587f3d2dc2e35808555eaa7`, Git blob `ef45b7ddd145c9959fba298bb9d0993519de7432`.
- Candidate: `alpha_actor_registry_source_pin_v2_20261031.js`; **2,472 bytes**, SHA-256 `0301546cf8876c0beb77b75a4de989c5af33518d2649c5638ab1fb8865300c2b`, Git blob `733c63466acd2cc6629ce34433e465ccde3fd9d7`.
- Independent local Node.js v22.16.0 black-box result: **15/15 checks PASS**, **11/11 fail-closed negatives**. Three positive controls cover an empty census, an owner plus unregistered actor, and one unregistered actor. The baseline synthetic spoof is an additional explicit comparison check.
- Negative controls: tampered allowlist, changed default, truncated registry, appended registry byte, caller override, duplicate comment ID, malformed user, invalid census type, null/missing registry, and invalid ID.
- Both published GitHub candidate/evaluator file blobs were fetched after their respective commits and matched the independently computed local Git blob IDs. No CI or merge is inferred from this report.

| Scoped metric | V1 | V2 |
| --- | ---: | ---: |
| Forged caller actor list mislabeled as registered candidate | 1/1 | **0/1** |
| Empty real registry preserves unregistered status | Caller dependent | **1/1** |
| Negative fixtures with fail-closed response | Not pinned to registry | **11/11** |
| Frozen black-box checks | Baseline contrast | **15/15 PASS** |
| Project-wide authorized handoff automation | NOT_COMPUTABLE | NOT_COMPUTABLE |
| Project-wide complete publication readback | NOT_COMPUTABLE | NOT_COMPUTABLE |

**Falsifier:** If the V2 candidate labels an injected non-owner actor as registered while the pinned registry has an empty allowlist, accepts a modified registry, or drops valid owner/unregistered comments from the denominator, the scoped improvement is disproved.

## DECISION / LIMITS / REPRODUCE

`TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE`. The registry is intentionally fixed to one immutable `main` blob; any later operator-authorized registry change requires a separately pinned successor, not a silent update. This tests local source-bound classification, **not** independent GitHub transport authentication, external expert identity, R10 return byte verification, expert scientific execution, or production integration.

The complete authenticated denominator of routine public authorized handoff attempts including failures is absent. No synthetic fixture enters the operational 90% numerator. The complete denominator of all project publications and readbacks is also absent. `AUTOMATION_RATE=NOT_COMPUTABLE`, `FULL_READBACK_RATE=NOT_COMPUTABLE`.

`PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`.

Reproduce in a checkout (without network, writing only test output to stdout):

```bash
node research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_actor_registry_pin_oracle_v1_20261031.js \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_actor_provenance_gate_v1_20261031.js \
  research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_actor_registry_source_pin_v2_20261031.js \
  docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json
```

No new automation, pipeline root, external registration, evaluator self-approval, Cursor dispatch, R10 merge, runtime/Hostinger/WWW mutation, source overwrite, or claim promotion. Publication and Issue #93 receipt remain conditional on actual PR checks, exact main readback and independently observed merge.
