# R43-9 · 16 falsification controls and target-specific scientific pass requirements

| ID | Negative that must FAIL or flag | Positive/acceptable restricted result |
|---|---|---|
| M9-01 | Treat equal placement+same marginal variance as zero second-sensor information | Independent rho=0 yields I(AB)=2 vs I(A)=1 in scalar Gaussian |
| M9-02 | Multiply two independent likelihoods though rho=.9 shared noise | Correct full Σ gives I(AB)=2/(1+.9)=1.05263158 |
| M9-03 | Rank1 in 2D -> blanket ABSTAIN on sum θ1+θ2 | target sum identifiable, difference not; target-based action |
| M9-04 | Full local rank interpreted as global identification for θ and -θ alias | detect multi-modal/global symmetry |
| M9-05 | Convert parameters to micro-units and accept flip at eps=1e-8 | scale/coordinate invariant physical decision |
| M9-06 | exact zero eigenvalue yields kernel-fraction alpha=0 | report nullity correct and trace=0 as special case |
| M9-07 | posterior prior I2 makes rank2 although data rank1 | difference direction PRIOR_DOMINATED, not measured |
| M9-08 | count same prior once per sensor -> double info | one prior for joint likelihood, exact posterior correct |
| M9-09 | biased prior shrinkage variance claimed CRB/GUM "violation" | bias/MSE/scoring and assumptions reported |
| M9-10 | oracle reference available as predictor in phone-only deployment | drop oracle from inference; keep only external scoring reference |
| M9-11 | absolute yaw inferred from static gravity-only | yaw not observable in that task, target ABSTAIN |
| M9-12 | 100Hz nominal resample cancels unseen latency/drift | clock/boot/mount adversarial red test and abstain |
| M9-13 | always abstain rewarded without coverage penalty | selective risk-coverage curve with prereg loss and error controls |
| M9-14 | fake actor ACK and overlapping/derived eval labels passed | external trust root and zero protected split leakage |
| M9-15 | legitimate DOI/README counted as downloaded dataset | Q0..Q5 with actual raw bytes/rights/independent replay or source gap |
| M9-16 | favorable secondary sensitivity silently replaces primary | 6-case primary v0=v2 maintained, exploratory separate |

**Status at checkpoint creation**: M9-01..M9-07 have small independent arithmetic counterexample/design proofs only; M9-08..M9-16 are research requirements, not executed R43-9 agent tests. The original source script Grok claims remains NOT_RECEIVED. No agent ACK or authentic external benchmark.

**Preregistration**: physical target estimand/unit/basis and nuisance, one confidence/coverage target with heldout group and source rights, normalized rank condition and sensitivity rather than arbitrary hardcoded raw eigenvalue threshold; separate prior/likelihood and optional observational reference; measured rather than nominal CPU/token/network/wall budget; unavoidable subgroup uncertainty. Cross-phone covariance under shared clock/physical mount mandatory.

**Research-claim approval**: Source hash+owner metadata (Q4) cannot substitute for a test; Q5 needs genuinely independent actor; C1 stays descriptive even if tests pass. An independent Gaussian fixture test does not change P01..P10 or physical deployment authorization.
