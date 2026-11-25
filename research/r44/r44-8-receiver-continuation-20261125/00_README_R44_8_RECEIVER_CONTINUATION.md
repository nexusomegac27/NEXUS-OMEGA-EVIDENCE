# R44-8 RECEIVER CONTINUATION (R0) — 2026-11-25

Receiver: Off-Chain Independent Expert, UNREGISTERED_ADVISORY_C1, n_eff=1, append-only.
Entry: Issue #446 @ a46d8e34efacd08a970949d43bb64e7210aa6018 (GitHub-only, bytes verified).
Order: 01_ORDER.md (P0 E32/E33 receiver correction executed). Claim ceiling C1.

Contents
- 30_GITHUB_READBACK_VERIFICATION.json : canonical intake verification (10/10 files sha256+git-blob; ZIP anchors; 10/10 members; manifest anchor resolved)
- 31_RC03_JOINT_METRIC_RECOMPUTATION.json : mechanical defect proof (20/20), AXIOM frechet table recompute (confirmed), rowwise all-covered subsample, paired contrasts
- 32_R8_N01_COUNTEREXAMPLE_AND_SIMULATION.json : exact integer-atom counterexample + Gaussian-copula sweep (seed 20261125)
- 40_RC03_METRIC_NAME_CORRECTION_APPEND_ONLY.md : the append-only metric-name correction of record
- 90_CONTINUATION_LEDGER_R44_8.json : events, scope basis, resource ledger, script versions
- 99_SHA256SUMS.txt : sha256 of all package members

Key results
1. coverage_joint in R44-7 15_RC03_RESULTS.json is np.prod(marginals) in all 20 cells (defect confirmed in own bytes, script line 174).
2. AXIOM's 20-cell Frechet bound table independently recomputed and confirmed; product-vs-joint not identifiable; headline "67.78% -> 41.95%" is a product drop, not a measured joint drop.
3. Retained 20-trial subsamples: orig 14/20 joint, corr 11/20 (headline cell); wide CIs; no paired cell p<0.125; full-n joint NOT recoverable.
4. Exact counterexample: identical marginals admit joints = Frechet bounds (0.8495/0.6360 orig; 0.7045/0.2485 corr); product matches neither.
5. No canonical credit claimed; R8-N01 stays NOT_RUN_FORMAL; all gates unchanged (0/24, 0/3, 0/10, BodyTwin NO).

NEXUS Ω OMEGA
