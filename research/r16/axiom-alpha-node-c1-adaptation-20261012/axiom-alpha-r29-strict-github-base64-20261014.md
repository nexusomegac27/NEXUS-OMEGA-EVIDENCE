# AXIOM Alpha-Node R29 — strict canonical GitHub Base64 gate (isolated C1 research)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R29_STRICT_GITHUB_BASE64_20261014_R0
PREDECESSOR = NEXUS_OMEGA_AXIOM_ALPHA_R28_REDIRECT_CONFINEMENT_20261014_R0
PINNED_MAIN_BEFORE = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLASS = PATCH_CANDIDATE_TESTED_IN_ISOLATION
RUNTIME_INTEGRATION = NOT_AUTHORIZED_NOT_EXECUTED
EXTERNAL_SCIENTIFIC_ACCEPTANCE = NOT_ESTABLISHED
```

## Original-byte custody

- Main authority: `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha adaptation contract, operator C1 publication directive, Task Anchor Norm, existing `research/pipeline/` and Repository Steward V1, all fetched from pinned main.
- Predecessor R28 ZIP: `NEXUS_OMEGA_AXIOM_REDIRECT_CONFINEMENT_R28_20261014.zip`, 124939 bytes, SHA-256 `bdf6e963a9d3f8c6ee56dc5d8dc08de885d55e9d748cbcce775a3bc41e20a865`; 51/51 detached manifest entries independently rehashed in the isolated sandbox. The ZIP is **not** asserted to be present on GitHub.
- Exact predecessor Python: `candidate/r28_redirect_confinement.py`, SHA-256 `e74c86fa3558020278e8255424767ed6e81385679cf89cf3cfd790cb9af35023`.
- Existing passive inbox: Issue #93, last observed comment ID `6137726458`, no newer material at intake.

## Negative hypothesis and falsifier

R28 decodes GitHub Contents API `content` with `base64.b64decode(..., validate=False)`. Python silently discards non-alphabet characters and accepts some noncanonical padding/pad-bit representations. Thus syntactically malformed API evidence can be accepted even when the **decoded payload hash and Git blob match**. This is an encoding/provenance strictness defect, **not** evidence of altered payload bytes or a real GitHub compromise.

Falsifier: a malformed Base64 representation (junk prefix/suffix, whitespace/control insertion, nonzero pad bits, over-padding, broken fold) must not yield a verified binding; canonical unwrapped and valid GitHub-style wrapped Base64 must remain accepted. Any accepted malformed fixture or rejected valid fixture refutes this candidate.

## Pinned isolated test result

The separate black-box evaluator was written and SHA-256 frozen **before** the candidate source was modified. It is not a third-party scientific review.

- Frozen evaluator SHA-256: `12e37627d20fc27e307006d64caa4abf3ef35757159ca6f195932bac54d5ad8c`.
- R28 predecessor against new evaluator: **3/12 PASS**; 9/9 malformed fixtures were wrongly accepted.
- R29 candidate against unchanged evaluator: **12/12 PASS**; 0/9 malformed fixtures accepted, 3/3 canonical positives accepted.
- Unmodified historical R28 HTTP-redirect evaluator on the isolated R29 candidate: **12/12 PASS**.
- R29 candidate Python SHA-256: `4e07b319ed0b0206257c3bb6fb0622bcab353d61e049770435edc80fd54a2984`.

Implementation is narrowly scoped to decoding the file-object Base64: bound encoded length, allow only LF/CRLF folding at 4-character boundaries, `validate=True`, canonical re-encoding equality, then retain existing decoded-length, SHA-256, Git blob, main ancestry and atomic owner receipt checks. No evaluator oracle was edited, no runtime or website was changed, no secrets or private sources were used.

## Scope, baseline and decision

The observed historical R15–R24 receipt subpopulation contains 10 handoff attempts, but independently established preflight eligibility remains 0/10 and the true eligible denominator is **unknown**, not 10. Consequently the >=90% 30-day automation target is **not measured**. The 12 test passes are not 12 automated handoffs. This candidate changes evidence parsing, not the measured transfer rate.

Decision: `TESTED_IMPROVEMENT_CANDIDATE` for isolated scaffold only. Productive integration, main publication, Issue #93 append-only receipt and GitHub→WWW parity require their own actual transport/readbacks; this note itself is not those receipts.

`BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE; NODE_RESET=NO; CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`
