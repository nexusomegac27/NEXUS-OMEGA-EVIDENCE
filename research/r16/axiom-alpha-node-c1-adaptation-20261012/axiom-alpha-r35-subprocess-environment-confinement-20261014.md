# NEXUS OMEGA · AXIOM Alpha-Node R35 · inherited subprocess environment (C1)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R35_SUBPROCESS_ENVIRONMENT_GUARD_20261014_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_R34_HISTORICAL_REGRESSION_CONTINUITY_20261014_R0
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = TESTED_ISOLATED_SCAFFOLD_CANDIDATE_NOT_INTEGRATED
```

## Original bytes and falsifier

The original local R34 ZIP was rehashed: 269723 bytes, SHA-256 `dc05ce765cc9571818f105bccc08325640850dfd43602ba508f48f9fbb16e761`, 13/13 manifest children MATCH. R34 runner SHA-256 `131b5c5e426c798f309e1d899c40d06103907e286545115dcee99657e7449720`. This ZIP is not claimed to be present on main. Issue #93 last public receipt ID `6137726458`.

R34 invokes each historical evaluator with `subprocess.run` without an explicit `env`. A separately authored synthetic one-test oracle launched a controlled child process that copied a **fake** environment canary to a temporary file outside the evaluator working directory. Original R34 reported PASS 1/1 while exposing the fake canary 1/1. This is a reproducible confidentiality gap in the isolated runner, not a claim of a real secret leak.

R35 changes only the subprocess launch: allowlisted minimal environment (PATH, temporary HOME/TMP*, locale, Python no-user-site/no-bytecode flags), plus Python `-I`. The R31/R32/R33 historical oracle hashes and predecessor binding remain unchanged. Candidate SHA-256 `71321ca344229f9d7b61707fc3f3ecc880a7f45bd5389d37169aac812bc53ab6`. Independently written evaluator was frozen before implementation: SHA-256 `960f7c55f74e63e35408c5efc05c3e3a26cc3a76aab80de804ed6589ad0b45ab`.

## Actual isolated results

- Frozen independent evaluator: **8/8 PASS**.
- Synthetic canary inherited: R34 **1/1**, R35 **0/1**; synthetic oracle itself PASS in both.
- Unmodified historical R31/R32/R33 single-positive smoke under sanitized env: **3/3 PASS**.
- Complete 50-test historical regression: **NOT EXECUTED in R35**. External scientific acceptance: **NOT ESTABLISHED**.
- Falsifier: any inherited canary in R35, valid positive test rejected, or full historical regression broken by the env change.

**Important limit:** Environment scrubbing is not an OS sandbox; a candidate can still access accessible filesystem/network resources. Never treat this as permission to run untrusted code on a privileged host. No node, Hostinger, runtime, model weights, evaluator oracle or access control was changed.

## Goal metrics and publication boundary

Historical R25 subset: ten receipts, ten unknown preflight eligibility states. Actual 30-day eligible denominator **UNKNOWN**, 90% target **NOT COMPUTABLE**. No new verified main publication in this research result; main readback ratio 0/0 undefined. Branch-only research notes are not main publications or WWW parity. The report is a C1 research candidate, not integration authority.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
