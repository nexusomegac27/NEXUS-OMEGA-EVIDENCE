# R43-3 E28 / E33 · cryptographic and differential science falsifiers

## E28 — authenticated source subject vs label spoofing
Source: external R43-2 inner 30412B package SHA256 ecb934d3931864869fba56a8349651ed3b81953fe0b2e5081c1d76cc67e27e74. Its r43_2_e28_poc_v2_deterministic_script.py SHA256 b7028c2d15b20a522530602a8bc54a88a2b98683956ff3debbc5109ec9c00275 uses a public deterministic TEST seed, Ed25519 and DSSE-v1 Pre-Authentication Encoding. AXIOM independently ran script with only output path redirected to isolated scratch. Exit=0, original receipt vectors/results exactly matched.

Cryptographic operations reproduced:
- positive: Ed25519 verification of signed DSSE PAE typed payload (1/1);
- negatives: tampered payload, wrong signing key, digest-only altered PAE (3/3).
- **not reproduced as a true test**: claimed FC2_PRODUCTION_ROOT signer mismatch is hard-coded to policy_reject=True and PASS_NEG. No function actually authenticates actor+role+policy trust root. Therefore 4/4 reported negatives cannot be called 4 independent enforced negatives. Add real negative: present an otherwise valid signature from a known public test root with forged production actor label and require real verifier policy reject. Add legitimate positive with a separately registered REAL authorized root; until authorized root exists, policy accept is NOT_ESTABLISHED.

Additional mandatory actual checks: role binding signer != reviewer, exact subject SHA256 + immutable git tree, payload schema/DSSE type, nonce, timestamp and expiry, key revocation, replay and scope, key provenance, canonicalization, duplicate keys, TOCTOU, rollback. Public test seed must NEVER become a production signing secret. No FC2 actual source runtime claim because its original version and trust root are missing from R43-2 receiver.

## E33 — C5 source gap and differential cost-matched H0
R43-1 X19 original code synthetic replay had ratios single/difference SD = 5.9058 (rho=+1), 1.9836 (+.5), 1.4436 (0), 1.0450 (-1). That is model-specific and **not** cross-comparable by simple rescaling to new C5 ratios. R43-2 C5 receipt reports MC with seed 20261124, 50000 samples per scenario, rho=1,0.5,0,-1, f_m=0.9 or 0.5, maximal analytic-vs-MC relative deviation 0.0069263082. **Original C5 executable script not included**; hence independent replay NOT_ESTABLISHED. The claim rho<=0 => R_diff/R_avg <= 1/2 is restricted to the reported formulas/definitions; it is a falsifiable conditional claim not a universal empirical theorem.

R43-3 demands: recover original C5 source, independently derive formulas from declared y_A/y_B signal models and cost parity; predeclare sign convention and error covariance, assay positive/negative rho and independent clock/delay/mounting noise; compare single, independent-average cost-matched, difference, permutation null with 95% coverage and intervals. Reject extrapolation to two actual phones without source-exact logs and independent optical/angle reference. Quantum Galileo DOI 10.1126/sciadv.aec8045 is permissible **only** as paired experiment/reference methodology, no quantum-gravity/consciousness/bodytwin claims.

## Gate accounting
R43_3_E28_DEMO_REPLAY_PASS_LIMITED = YES.
R43_3_REAL_FC2_AUTH = NO.
R43_3_E33_C5_SOURCE_INDEPENDENT_REPLAY = SOURCE_GAP.
R43_3_METROLOGY_GUM_MC_INDEPENDENT_REFERENCE = OPEN.
R43_3_BODYTWIN_VALIDATED = NO.
14_PHYSICAL_GATES_HOLD, C1_DESCRIPTIVE_ONLY, NO_CAPTCHA_BYPASS, NO_CURSOR_IMPLEMENTATION_ORDER.
