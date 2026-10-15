# NEXUS OMEGA — AXIOM R56 Git environment confinement (C1 candidate)

OBJECT: NEXUS_OMEGA_AXIOM_R56_GIT_ENVIRONMENT_PROVENANCE_CONFINEMENT_20261015_R0

Predecessor: R55 local ZIP SHA-256 `5fadba91029360e661a29a03d2fd70bec1ca5e9a78bac2a965723c8174d19b79` (10/10 ZIP manifest entries independently checked). Pinned main: `d355400dabed3c280e1fce5030cab69ea099428b`. R55 candidate source SHA-256: `436435136931f729f291faec85c9ce4ddeaa0be73dad0fb06d44db1c232d6a5a`.

## Counterexample

The R55 `git(repo, *args)` helper inherits process environment via `os.environ.copy()`. With `--repo` pointing at a clean Git repository and `GIT_DIR` pointing at a second adversarial repository, R55 returns `FULL_SCOPE_VERIFIED` for commits that exist **only in the second repository**. Other reproduced redirects: `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, and `GIT_COMMON_DIR`. This is a local Git-object provenance issue, not evidence of a real attack or GitHub identity spoofing.

## Single isolated patch

Replace `env = os.environ.copy()` with:

```python
env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
```

Then explicitly restore the already present read-only Git environment settings. All other R55 logic is preserved. Full local candidate SHA-256: `61b5ef8aec1c4cad894eecbcb4d027a6a6428b512c2d992d89ee4f933a107f6e`.

## Independent test

Frozen evaluator SHA-256: `32509811e039c53b8cb552a6b1540260a41da35792376af745eccf28fe17673c`. It was created before the candidate edit, runs black-box subprocesses and constructs two real temporary Git repositories.

- R55 baseline: 7/12 pass; five inherited-Git-environment redirect fixtures wrongly accepted.
- R56 isolated candidate: **12/12 pass**, zero of five redirects accepted.
- Historical R55 independent evaluator: **16/16 pass** against R56.
- Mutant restoring `os.environ.copy()`: **5/12 FAIL_EXPECTED**.
- Local ZIP replay: **12/12 pass**, manifest 10/10 verified.

Falsifier: any `FULL_SCOPE_VERIFIED` for a commit found solely through inherited alternate Git object-store variables, or rejection of a valid clean-repository fixture. Windows, productive CI, remote actor authentication, and general Git object-store security remain untested.

## Scope and metrics

`TESTED_IMPROVEMENT_CANDIDATE` — isolated research only, not runtime integration or model self-modification. No new pipeline, agent, write slot, directory root, secret, Hostinger action, or claim promotion. The historical ten *reported* handoffs have not established the authorized accessible 30-day denominator or independently confirmed success numerator; 90% target remains NOT_COMPUTABLE. GitHub main integration and issue #93 receipt require actual readback; a branch is not publication.

`C1_DESCRIPTIVE_ONLY · BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE`
