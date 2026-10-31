# AXIOM Alpha-Node - pinned PR231 CI projection byte-integrity wrapper V2 (2026-10-31)

OBJECT = NEXUS_OMEGA_ALPHA_CI_PR231_PROJECTION_TRUSTED_BYTES_V2_20261031_R0
DECISION = PATCH_CANDIDATE_TESTED_IN_ISOLATED_V8_NOT_YET_NODE_SUBPROCESS_ACCEPTED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = c8ba8f04d9f6479c3bce036e6bb596f7aad8cac0
PINNED_MAIN_PARENT = 56c383b6675d47b61d1b35bb543d24a2d36de512
PREDECESSOR_PR = 234
PREDECESSOR_ISSUE93_RECEIPT = 6540138304
RESEARCH_LANE = research/r16/axiom-alpha-node-c1-adaptation-20261012/
RUNTIME_INTEGRATION = NO
RULESET_OR_WORKFLOW_MODIFICATION = NO
WWW_PUBLICATION = NOT_EXECUTED

## Observe and provenance

The GitHub main ref and commit object were retrieved at the pinned base. Governance was read from AGENTS.md, GOVERNANCE.md, docs/AI_CONTEXT.md, docs/agent-protocol.md, docs/architecture/REPOSITORY_STRUCTURE.md, docs/governance/REPOSITORY_ORDER_POLICY.md, the R16 Alpha contract, the operator C1 publication directive, the task anchor norm, and research/pipeline/ POLICY and README. The external write registry at this commit remains default DENY with an empty external_actor_allowlist.

The predecessor's original CI projection was fetched from the exact immutable base commit:
- alpha_ci_pr_path_filter_projection_v1_20261031.json: 8685 original ASCII bytes; SHA256 9aad5e271db570dc13b5ad2e7d8a3fbd9bc3db4de2e4b13b96390614dbf2c0fd; Git blob 5da248602def62f7d34c926ccc21bf59ec944bcb.
- alpha_ci_pr_path_filter_audit_v1_20261031.js: 3615 bytes; SHA256 0cc5a0d332cfc524582da4a64525a9fecd5df8434756e3a8b4a1bf4cd952e645; Git blob 7d0614759d472cb980809fbbce618556fb02531f.
- Original projection is source-bound to PR #231 and workflow inventory from predecessor PR #234. This wrapper does not re-fetch all original YAMLs or authenticate an external trust root.

## Negative hypothesis and baseline

H0: V1's hardcoded PR and workflow inventory commit IDs alone prevent a caller from substituting source-projection metadata. This is falsified: V1 accepts a same-length mutation to the first workflow Git blob SHA and a same-length path-filter substitution, both while returning PASS with 17 workflows, 12 validate definitions and 4 eligible definitions. V1 also accepts deletion of the terminal LF because JSON semantics are unchanged.

The V2 wrapper rejects inputs unless UTF-8 byte length and SHA-256 match the previously frozen original projection; only then does it invoke the unchanged V1 classifier. It does not alter any oracle, the V1 code, the original projection, a workflow, or a ruleset.

## Frozen evaluator and independent checks

The independent Node black-box evaluator was created BEFORE the V2 candidate. Its historical V1 and V1.1 drafts remain visible and unmodified. A static preflight found that V1 constructed the Git blob prefix with a literal backslash-zero rather than a NUL; V1.1 corrected that, but its negative fixture mistakenly treated removal of a terminal LF as invalid JSON. Both defects were corrected append-only in frozen V1.2, committed before the V2 candidate. These are transparent oracle-preflight corrections, not claimed successful runs.

Frozen V1.2: frozen_alpha_ci_projection_integrity_oracle_v1_2_20261031.js, 2695 bytes, SHA256 307385cd3bd886e8aa400f49dec63eceb67652beb362968346bafd34ffbda279, Git blob ebfbad1c7871ccbbd1989078f50a7556b0fc25e2, first committed at 57cbfbf298bba8612c7546fdbe837bd80908d2ea.
Candidate V2: alpha_ci_projection_trusted_bytes_v2_20261031.js, 1044 bytes, SHA256 d3912d779510b4d04878cf1a98b9ce38ef9b478e3c1558a6ab5dd5b1b76ffda9, Git blob 94c0673f558c060abb69f102d36d7cf54c33a961, committed at fac8252b1b65eadd5b26e7ddd9484ef427c819b7.

An independent JavaScript SHA-256 calculation over the retrieved original 8685 bytes matched the frozen SHA256; the GitHub API returned the expected Git blob ID. A separately written V8 harness evaluated the actual retrieved V1 source and V2 source in isolated module scopes with a crypto-compatible SHA-256 adapter. Five real-input/mutation checks completed: 5/5 matched their independent expected status values.

| Real source / adversarial fixture | V1 | V2 |
| --- | --- | --- |
| Original 8685-byte pinned projection | PASS | PASS |
| Same-length workflow Git blob ID tamper | PASS | FAIL_CLOSED |
| Same-length workflow path-filter tamper | PASS | FAIL_CLOSED |
| Terminal LF removal, still valid JSON | PASS | FAIL_CLOSED |
| Malformed JSON | FAIL_CLOSED | FAIL_CLOSED |

Before/after: 0/3 versus 3/3 changed-byte source variants rejected. Baseline positive control 1/1 PASS for both. These are scoped fixtures, not operational handoff metrics. The frozen V1.2 Node.js subprocess evaluator has NOT_EXECUTED in this run; no Node subprocess PASS, independent third-party validation, or production integration is claimed.

Reproduction from this existing research directory:
```sh
node frozen_alpha_ci_projection_integrity_oracle_v1_2_20261031.js alpha_ci_pr_path_filter_audit_v1_20261031.js alpha_ci_projection_trusted_bytes_v2_20261031.js alpha_ci_pr_path_filter_projection_v1_20261031.json
node alpha_ci_projection_trusted_bytes_v2_20261031.js < alpha_ci_pr_path_filter_projection_v1_20261031.json
```

## Falsifier and decision

Falsifier: the exact pinned original projection fails V2; a same-length mutation passes V2; the frozen V1.2 Node subprocess returns a different result; or a retrieved source SHA256 differs from the fixed trust pin. The pin is an owner-repository historical source identity, NOT an independently authenticated external trust root. Changing the legitimate projection requires a new append-only pin and independent test; no silent auto-acceptance.

Decision: publish an isolated C1 PATCH_CANDIDATE with V8-level executed tests, preserving all failed oracle preflights and historical assets. Production integration, runtime authority, GitHub merge-policy modifications and WWW parity are NOT_ESTABLISHED. The project-wide automation rate and readback rate remain NOT_COMPUTABLE: no complete authenticated denominator of eligible handoffs/publications including failures is available. R10 PR #115 remains an owner-authored PUBLIC_SEND only; no independently authenticated receiver ACK or expert research execution was observed in the 224 Issue #93 comments, PR comments or reviews at this baseline.
