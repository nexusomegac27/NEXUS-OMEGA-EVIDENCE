# AXIOM Alpha-Node R30 — source/remote parity contradiction (C1)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R30_SOURCE_REMOTE_PARITY_CONTRADICTION_20261014_R0
STATE = CONTRADICTION_APPEND_PATCH_CANDIDATE_HOLD_SCOPED
PREDECESSOR = NEXUS_OMEGA_AXIOM_ALPHA_R29_STRICT_GITHUB_BASE64_20261014_R0
PREDECESSOR_BRANCH_COMMIT = 67e6fe85cfe33df2002009d049d6c8539a22b97d
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RUNTIME_INTEGRATION = NO
EXTERNAL_ACCEPTANCE = NOT_ESTABLISHED
```

## Original-byte intake

R29 ZIP: 145403 bytes, SHA-256 `ef2849c9e304b5bddd533eca2599d94017891354b196be21d7ed213fda5a8a69`, 15/15 child entries rehashed. Embedded R28 ZIP: 124939 bytes, SHA-256 `bdf6e963a9d3f8c6ee56dc5d8dc08de885d55e9d748cbcce775a3bc41e20a865`, 51/51 child entries rehashed. R29 candidate source SHA-256 `4e07b319ed0b0206257c3bb6fb0622bcab353d61e049770435edc80fd54a2984`. The governance and R16 source paths were fetched at pinned main. Passive Issue #93: 19 comments, last ID `6137726458`.

## One falsifiable defect

The R29 audit checks local source SHA-256 and GitHub readback SHA-256 separately but never requires them to be equal. Thus a fully internally consistent remote blob, ancestry and owner receipt can attest a *different* payload while the local source has another SHA-256. This is a synthetic source-identity counterexample, **not evidence of a GitHub attack**.

A separately frozen R30 black-box evaluator (SHA-256 `4f7bccf1b37610abcfedf2f04d9438a09ea96bec36fe7efbed435a0db507a1df`) was created before a one-check isolated candidate. Candidate SHA-256: `9c3d6667612d4ecd399343718960214cea210b331c1f03bbcdf85b154f813226`.

| Frozen test suite | R29 baseline | R30 candidate |
|---|---:|---:|
| New source-to-remote parity | 5/10 | **10/10** |
| Historical R29 Base64 | 12/12 | **12/12** |
| Historical R28 redirect | **12/12** | **3/12** |

The historical R28 **positive** fixture intentionally uses *different* bytes: local source `{"source":"fixture"}`, SHA-256 `f8d5e07b8c8c7c65354c0f46de0d6818e2e16d7fa8939bc57b44681bd33c5995`; synthetic remote payload `# synthetic redirect fixture, not GitHub evidence\n`, SHA-256 `277304ccf52142b07b6bd0400cb1948439d27d8a46b6e29ecd608200ec7ac858`. The new parity gate rejects this before redirect evaluation. Nine historical assertions fail on precedence or old positive acceptance, **not because redirects became acceptable**. Neither frozen evaluator was changed.

## Decision and falsifier

**CONTRADICTION_APPEND; do not integrate the R30 validator.** Exact-source handoffs may require byte equality, whereas legitimate *derived-artifact* handoffs may intentionally differ. A universal equality gate could be wrong. An independently specified `SOURCE_EXACT` versus `DERIVED_ARTIFACT` contract, transformation provenance, and a new independently approved test suite are required before code integration. Preserve the original R28/R29 oracle failures and original bytes.

The isolated mismatched-source synthetic acceptance changes 1/1 to 0/1; matching-source synthetic acceptance stays 1/1. These are **not live GitHub handoffs**. In the available R15–R24 subset, 10 attempts have 0/10 independently demonstrated preflight authorizations; the *actual eligible denominator remains UNKNOWN*. The >=90% target is not measured. No model modification, runtime/Hostinger change, Node reset, evaluator self-approval, claim promotion or WWW parity assertion.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · C1_DESCRIPTIVE_ONLY`
