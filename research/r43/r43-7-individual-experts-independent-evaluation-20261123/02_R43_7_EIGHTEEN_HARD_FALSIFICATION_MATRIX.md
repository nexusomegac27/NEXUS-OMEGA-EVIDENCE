# R43-7 · 18 precise falsification fixtures, including two new independently observed failures

These cases are individually noncompensatory. A positive is actual independently executed cryptographic/source verification or honesty abstention, not marker presence. **Existing R43-6 source is never changed in place.** Proposed repairs belong to separately versioned research experiments, not production code.

| ID | Named negative / injected fault | Required actual positive and evidence | Entry judgment |
|---|---|---|---|
| N7-01 | authenticated actor field with arbitrary nonempty `signature=garbage` and impostor label | trusted externally registered public key cryptographically verifies exact signed subject+actor+scope+nonce and expiry | **FAIL OBSERVED** original code returns CLEAN |
| N7-02 | partial 1-ID overlap of feedback/evaluation sets | zero intersection of IDs, ancestor data, content hashes, seeds and near duplicates; independently attested protected split | **FAIL OBSERVED** original code returns CLEAN |
| N7-03 | same self-declared actor impersonates multiple independent evaluators | different externally registered owner/authority and distinct reviewed signatures | QUORUM 0/3 |
| N7-04 | derived holdout examples/renamed IDs despite no direct ID overlap | source ancestry graph, feature/label equivalence and transformation hash collision checks | NOT_RUN |
| N7-05 | valid-looking ACK signed by unknown root or wrong reviewer role | authorized key pin + role/scope binding with genuine valid positive | NOT_RUN |
| N7-06 | evaluator label or code updated after precommit | independent second-actor signed precommit hash matched before run, mutated SHA hard failure | LOCAL frozen equality PASS, EXTERNAL NOT_ESTABLISHED |
| N7-07 | final evaluation receipt produced before final event recorded | exactly one canonical final signed receipt generated after all required recorded events; no self-signed timestamp promotion | Original pending vs replay full timeline |
| N7-08 | 33.45s baseline vs 135.72s adaptive with 0 vs 372394 network bytes | truly matched observed wall/CPU/network/tool/LLM tokens/subprocess budgets or prereg cost-normalized outcome | FULL PARITY FAIL |
| N7-09 | equal fixed CPU-normalizer used to claim total cost equal | full inclusive CPU plus all descendants, with timeout and negative overbudget test | Normalizer equal only |
| N7-10 | 1000-halfwidth covers all and attempts positive claim | proper interval score + width and independent reference, wide control penalized | PASS LOCAL |
| N7-11 | 20/20 coverage treated as 95% population calibration proof | binomial uncertainty/strata, large fresh independently sampled original-source set; 95% exact lower bound 0.8316 | UNDERPOWERED |
| N7-12 | adaptive v2 adds independent reference but baseline lacks reference-only comparator | source-matched reference-only and cost-matched fusion baselines with identical available information | NOT_RUN |
| N7-13 | UTF-8 char count 43 mistaken for encoded byte length 44 | exact signed original Ed25519 PAE positive/negative third-party verified | PASS_LOCAL_C1 |
| N7-14 | BE32 and LE32 substituted as DSSE v1 | same original envelope, normative cross-validator rejects binary schemes | PASS_LOCAL_C1 |
| N7-15 | race baseline artificially injects sleep then extrapolates to FC2 production | genuine affected trust store + forced interleaving + legitimate signers, no physical gating | SIMULATED_ONLY |
| N7-16 | duplicate GitHub source mirrors treated as independent research objects | novel original primary source content/version/rights independently verified against prior catalog | NOT_ESTABLISHED |
| N7-17 | HTTP 403 challenge counted as public W1 source or synthetic BodyTwin clinical proof | second-party genuine 2×4 HTTP200 status+entity/header+browser parity, independent actor | OPEN |
| N7-18 | fabricated evidence self-report closes any scientific pass | original P01–P10 individual gate, matched source+runner and actual actor, negative+positive | 0/10 |

**H0**: no independently accepted primary-evidence gain under matched costs and clean evaluator. **H1**: independently authenticated, sample-adequate, source-exact gains survive true holdout/strategy learning and zero safety regression. Do not use a binomial CI as a claim about natural-world IMU reliability: this is only synthetic test-set frequency.
