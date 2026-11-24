# AXIOM R43-9 · Grok-Denkstütze: mathematische Quellenkritik mit Falsifikationsbelegen

**Original** `GROK_INPUT_R43-9.txt`: 30412 Originalbytes, SHA256 `c2bf195a31862be7d53e68d82adf71749a13a743d15bc541d5fbd2137d2506b5`. Volltext gelesen: K01–K14, erwartete/beobachtete Fisher-Matrix, classical CRB, Prior-Informationsmatrix, lokale Posterior-Hesse, Default-Schwellen und 3 rein synthetische Beispiel-Fixtures. Das angeblich erzeugte Python-Artefakt und dessen `SHA256SUMS.txt` wurden **nicht** hochgeladen. Im Text genannter Script-SHA `292c77727081ab6117eb3f23b27527c0be5c855897dfece193573ec15bf606a6` ist **UNVERIFIED_PRODUCER_CLAIM**.

## Präzise Akzeptanzen
1. Die reguläre erwartete FIM kann **lokale** Identifizierbarkeit unter Rothenberg-Regularitätsannahmen prüfen; der CRB liefert unter geeigneten Bedingungen eine Untergrenze für unverzerrte Schätzer.
2. Positiv definiter Prior kann die Posterior-Hesse in likelihood-rangdefizienten Richtungen invertierbar machen. Das ist regularisierte **Prior-Evidenz**, nicht neue Sensormessinformation.
3. Ein Bayesianischer Anteil der gerichteten Präzision `vᵀ I_prior v / vᵀ (I_prior+I_like) v` kann ein **Design-Kandidat** für prior-getriebenes Schätzen sein; sein Schwellenwert, Parameterkoordinaten und Regularitätsannahmen müssen offen gelegt und extern kalibriert werden.
4. ABSTAIN bei nicht beurteilbarer Zielgröße ist ein sinnvoller Design-Ansatz; sinnvollere Endpunkte: `MEASUREMENT_IDENTIFIED`, `PRIOR_DOMINATED_NOT_MEASURED`, `TARGET_IDENTIFIABLE_BUT_NUISANCE_NOT`, `ABSTAIN`.

## Harte Korrekturen gegenüber der Denkstütze
**FIM rank full does not imply GLOBAL identification.** Rothenberg Primärarbeit https://pages.stern.nyu.edu/~dbackus/Identification/id/Rothenberg_id_Econometrica_71.pdf erklärt explizit, dass lokales und globales Problem getrennt sind; bei komplexen zeitabhängigen Modellen zusätzlich observability/dynamische Experimente und Profil-Likelihood.

**Gleiche Montage ist nicht redundante Information:** Zwei unabhängige Gauß-Messungen desselben skalaren theta mit Rauschvarianz 1 haben FI je 1 und FI gemeinsam 2. Bei Varianz 1 und Korrelation rho∈{0,.5,.9} hat FI gemeinsam `2/(1+rho)` = 2, 1.333333333333, 1.052631578947. Diese kleinen NumPy-Rechnungen wurden von AXIOM tatsächlich ausgeführt, sind **mathematische Fixture-Beispiele**, keine echten IMU-Referenzen.

**Rang vs Zielparameter:** Modell `y = theta1+theta2+epsilon`, epsilon~N(0,1) liefert `I_like=[[1,1],[1,1]]` mit Rang1. Die Summe theta1+theta2 ist identifizierbar, die Differenz nicht. `I_prior=I2` macht `I_post=[[2,1],[1,2]]` Rang2, die Likelihood-Information entlang `v=[1,-1]/sqrt(2)` bleibt 0. Richtige Aktion: `theta1-theta2` nicht als gemessen ausgeben; eine sauber referenzierte Summenschätzung ist nicht generell verboten.

**Parameter-Scale:** Für `y~N(theta,1)`, `I(theta)=1`; bei `phi=10^6 theta` ist `I(phi)=10^-12`. Ein universelles `eps_rank=1e-8` würde trotz IDENTISCHEN Physikdaten die Identifizierbarkeit ändern. Normalisierte, physikalisch motivierte Parameterreferenzskalierung und Sensitivitätsband obligatorisch. Der Quelltext nennt `eps_rank=1e-8, kappa_crit=1e8, tau_crit=.85, weak_frac=.05`; all are **CANDIDATE UNCALIBRATED**.

**Kernel-Metrik:** `alpha=sum(lambda_i<eps)/trace(I)` zählt 0-Eigenwerte mit 0 Wert; für `diag(1,0)` ist alpha=0 trotz Nullität1. Bei `trace=0` undefiniert. Stattdessen use dimensionless nullity, rank_ε, target projection and spectral confidence.

**GUM ≠ FI inverse:** CRB is conditional on unbiased regular estimation. JCGM 100 2008 uncertainty includes measurement function, type A/B components and their covariances; JCGM101 2008 Monte Carlo propagation. A biased estimator can have variance lower than an unbiased bound without being a scientifically good estimator.

**Bayesian posterior**: `Cov_post~(I_prior+I_like)^-1` exact in suitable linear-Gaussian conditions or approximate local Laplace; van Trees inequality deals with Bayes MSE and expected information under regular assumptions and need not equal local exact posterior covariance. For two phones, don't count shared prior twice. Origin literature Stanford van Trees https://web.stanford.edu/class/ee378c/lecture14_annotated.pdf and Berkeley notes https://www.stat.berkeley.edu/~aditya/resources/STAT212aOCT23Lecture9.pdf .

**Overconfident non-identification**: FIM cannot by itself provide global posterior multimodality or real risk/coverage calibration, and cannot prove external device readiness, U95 or clinical prognosis. Evaluate `K04/K05/K13` target-specific, proper score, reference firewall and genuine original bytes.

## Causal history constraint
R43-7 original 6-case primary one-domain synthetic test contained byte-identical v0/v2/fusion predictions and `IS/2=18.303982903117085` each, reference-only 6.6217 with reference present as task input, 6/6. No general adaptive gain. FDA two phones different locations and 20 people/370 trial files, not 370 people, original full raw bytes not independently rehased by AXIOM. UCI MHEALTH original 75.6MB not independently supplied. `C1_DESCRIPTIVE_ONLY`, 0/10 and 0/3; 14 physical HOLD and ALT_D active.
