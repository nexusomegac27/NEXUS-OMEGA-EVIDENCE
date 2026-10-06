# G08 — PART B0 SYNTHETIC POC DESIGN (R10R9, Lane 2)

```text
OBJECT        = R10R9_G08_PART_B0_SYNTHETIC_POC_DESIGN_LANE2_20261005_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY — B0 is a SYNTHETIC proof of concept, NOT biological validation
STATUS        = DESIGN ONLY · nothing generated · nothing run
LAST_VERIFIED = 2026-10-05
REPO GAP      = GAP-L2-02: no R9/R10R9 vesicle/PH draft text exists in either repo; the definition of Δ
                and of the PH component are therefore taken from ORDER §12–16 with conservative assumptions (A-Δ1..A-Δ3).
```

## 1. B0 / B1 split (ORDER §12)

| | B0 SYNTHETIC_POC | B1 REAL_MICROSCOPY_VALIDATION |
|---|---|---|
| Data | Generated 2D+t movies with complete ground truth (this file) | Real time-lapse fluorescence microscopy with annotations (G09) |
| What it can show | Whether Δ, as a hold policy, trades coverage against high-cost false positives under *controlled, known* degradations; and whether PH-based features add value over strong non-PH pipelines *in the generator's world* | Whether that behavior transfers to real optics, labels and biology |
| Allowed wording | "In synthetic movies generated under model G (version, hash), Δ …" | "On dataset D (DOI, version) with annotations A …" |
| Forbidden wording | "real vesicles", "biological", "phototoxicity", "in cells" | "phototoxicity" without a biological endpoint (G09 §3) |
| Gate | G08-B0 (§8) | G09-B1 |

**Rule:** a B0 PASS never licenses B1 language. The R9 contradiction ("synthetic specification" vs "real vesicles" rhetoric) is resolved by this split.

## 2. Δ — conservative operational definition (assumptions, because the R9 text is missing)

- **A-Δ1:** Δ is a frozen scalar score computed per *track segment* (a maximal run of linked detections between two linking decisions). Higher Δ means less trustworthy.
- **A-Δ2:** the Δ policy is `HOLD(segment) iff Δ(segment) > τ`. A held segment is output as `HOLD`/unknown. It is neither asserted present nor asserted absent. τ is chosen on DEV only.
- **A-Δ3:** candidate Δ instantiations, each preregistered separately:
  - (Δ-PH) a persistence-based instability score: the change of 0-dim persistence of the segment's supporting intensity peak across frames, from a cubical filtration on intensity (§6);
  - (Δ-DISAGREE) disagreement between two independent non-PH pipelines;
  - (Δ-COST) the tracker's own linking cost or posterior.
- Δ is evaluated **as an abstention / hold policy, not as an accuracy improvement** (ORDER §16). Selective prediction framing: risk–coverage (L2-033; Chow's reject option L2-034).

## 3. 2D+t generator specification (ORDER §13): every parameter

Ranges are **design assumptions** with sensitivity sweeps. They are not claims about real vesicles. Where a range is anchored to the ISBI 2012 particle-tracking challenge design (Chenouard et al. 2014, L2-101), this is stated.

| # | PARAMETER | Model | Default (frozen per scenario) | Sweep range | Anchor / note |
|---|---|---|---|---|---|
| G1 | FIELD / FRAMES | 2D grid, square pixels | 512×512 px, 100 frames | frames 50–200 | Assumption |
| G2 | PIXEL_SIZE, FRAME_INTERVAL | Physical scale for unit conversion only | 100 nm/px, 100 ms | — | Assumption. Movies are generated in px/frame. Physical units are labels only. |
| G3 | VESICLE_COUNT | Initial N0 + birth process | Density levels LOW / MID / HIGH ≈ 100 / 500 / 1000 particles per field | Same three levels | ISBI used three density levels of roughly this size (L2-101) |
| G4 | BIRTH / TRUE DISAPPEARANCE | Poisson births at rate λ_b; per-frame death hazard h_d; out-of-field exits | λ_b chosen so that N stays ≈ stationary; h_d = 0.01/frame | h_d 0.002–0.05 | Each death has a frame-exact GT label `TRUE_DISAPPEARANCE` |
| G5 | TRAJECTORY_MODEL | Hidden Markov switching between motion states {BROWNIAN, DIRECTED, CONFINED} | VESICLE scenario: BROWNIAN only; MIXED scenario: switching, mean dwell 20 frames | Dwell 5–50 | ISBI "vesicle" = Brownian, "microtubule" = directed, "receptor/virus" = switching (L2-101) |
| G6 | BROWNIAN_COMPONENT | Isotropic Gaussian steps, σ = √(2DΔt) | D giving σ = 1.5 px/frame | σ 0.5–4 px/frame | Assumption |
| G7 | DIRECTED_MOTION_COMPONENT | Constant-speed segments with direction persistence (von Mises turning, κ) | v = 3 px/frame, κ = 10 | v 1–8, κ 1–50 | Assumption |
| G8 | MERGE/SPLIT EVENTS | Merge when two particles are < r_m apart with probability p_m (intensity sums); split = reverse with probability p_s | OFF in core; ON in scenario MS: p_m = p_s = 0.005/frame | 0–0.02 | GT parent/child graph recorded. Trackers without merge/split handling are scored per GT convention §4. |
| G9 | OCCLUSION | Crossing / overlap (emergent from density) + explicit occluder masks (random ellipses, lifetime 5–20 frames) | Occluder area fraction 2% | 0–10% | Particles under the mask are *present but unobservable*. Label `SIGNAL_LOSS_WINDOW(OCCLUSION)`. |
| G10 | PSF | 2D Gaussian approximation of the widefield/confocal PSF | σ_PSF = 1.0 px | 0.7–2.0 px | Gaussian PSF approximation per Zhang, Zerubia & Olivo-Marin 2007 (L2-102). Sensitivity arm: Airy-pattern PSF to test model misspecification. |
| G11 | INTENSITY | Per-particle amplitude I0 ~ lognormal | Median giving the target SNR | — | Heterogeneous brightness |
| G12 | BACKGROUND | Constant + low-frequency spatial field (sum of 2D Gaussians) + slow temporal drift of level | Ib constant + 10% spatial modulation | 0–30% | Non-uniform background is a known failure mode for intensity-threshold detectors |
| G13 | SHOT_NOISE | Poisson on expected photon counts | ON | — | Poisson–Gaussian sensor model (Foi et al. 2008, L2-103) |
| G14 | READ_NOISE | Additive Gaussian (σ_r) + offset; optional EM-gain excess-noise factor | σ_r = 2 e⁻ | 0–10 e⁻ | Same as G13 |
| G15 | SNR LEVELS | SNR = (I_o − I_b)/√I_o (ISBI definition) | 1, 2, 4, 7 | Same | ISBI levels and definition. SNR ≈ 4 was reported as a critical level (L2-101). |
| G16 | DRIFT | Global rigid translation per frame: random walk + linear term | 0.2 px/frame linear, σ = 0.1 | 0–1 px/frame | GT drift vector stored. A "drift-corrected" pipeline variant is allowed for all pipelines alike. |
| G17 | BLEACHING | Per-fluorophore population exponential decay of I0: I(t) = I0·exp(−k_b·dose(t)) | k_b giving 50% loss at frame 100 | 0–90% loss | Global intensity decay. Distinct from G18/G19. |
| G18 | SIGNAL_DECAY | Per-particle stochastic blinking / off-states (2-state Markov ON↔OFF) | P(ON→OFF) = 0.02, P(OFF→ON) = 0.3 | 0–0.1 / 0.1–0.9 | Particle present, signal absent. Label `SIGNAL_LOSS_WINDOW(DECAY)`. |
| G19 | LIGHT_TOXICITY_PROXY | **Synthetic degradation only.** Cumulative-dose hazard that (a) reduces the diffusion coefficient, (b) raises the death hazard h_d, (c) adds spurious bright debris blobs, all as monotone functions of the cumulative illumination dose parameter | OFF in core; ON in scenario TOX with dose-response levels 0 / 1 / 2 / 3 | — | **NOT a biological phototoxicity model and NOT a biological claim** (ORDER §13). Debris blobs are labelled `FALSE_DETECTION_REGION(DEBRIS)`. |
| G20 | FALSE-DETECTION REGIONS | Injected non-particle structures: hot pixels, static bright blobs, edge artifacts, debris (G19) | 1% area | 0–5% | Each pixel set labelled `TRUE_FALSE_DETECTION_REGION` with its type |
| G21 | SEEDS / SPLITS | Independent seeds per movie | DEV: 20 movies per scenario × SNR × density; TEST: 20 different movies per cell | — | No movie is in both DEV and TEST. TEST is used once. |

**Scenario grid (core):** {VESICLE-Brownian, MIXED-switching} × SNR {1, 2, 4, 7} × density {LOW, MID, HIGH} = 24 conditions.
**Stress arms:** MS (merge/split), OCC-high, DRIFT-high, BLEACH-high, TOX (proxy levels 0–3), PSF-misspecified.
Each arm varies **one** degradation from the core default, so degradations are not confounded (one-factor-at-a-time around a core). A small 2^3 sub-factorial (bleaching × decay × toxicity-proxy at the MID/SNR4 point) separates signal loss from object loss.

**Reuse option:** the Icy plugin "ISBI Challenge tracking benchmark generator" (v0.0.1.1, 2013-12-09; L2-104) can reproduce ISBI-style scenarios. It does not, by itself, provide G16–G20 labels at the granularity required here. Our generator must emit them, or the plugin's output must be post-processed with documented code.

## 4. Ground truth (ORDER §13): emitted per movie, versioned and hashed

| GT object | Content |
|---|---|
| TRUE_TRACKS | Per particle ID: (frame, x, y, sub-pixel), motion state, intensity, ON/OFF state, occluded flag; parent/child links for merge/split |
| TRUE_DISAPPEARANCE | Frame of death or exit, with cause ∈ {DEATH_HAZARD, EXIT_FIELD, TOX_PROXY_DEATH, MERGE_ABSORBED} |
| TRUE_FALSE_DETECTION_REGIONS | Pixel masks per frame with type {HOT_PIXEL, STATIC_BLOB, EDGE, DEBRIS} |
| TRUE_SIGNAL_LOSS_WINDOWS | Per particle, frame intervals where it is present but its signal is absent or sub-threshold, with cause ∈ {OCCLUSION, DECAY_OFF, BLEACHED_BELOW_SNR1} |
| DRIFT_VECTOR | Per frame |
| DOSE | Cumulative illumination-dose parameter per frame (synthetic) |
| GENERATOR_RECEIPT | Generator version/hash, all parameters, seed, output hashes |

**Scoring convention for merge/split:** primary scoring uses ISBI-style one-to-one track pairing. Merge/split trackers are scored additionally with a graph-aware convention, frozen before TEST.

## 5. Metrics

### 5.1 Tracking metrics (established; cited only from verified sources)

| Metric | Verified definition (source) | Use here |
|---|---|---|
| α, β (ISBI) | α ∈ [0,1]: matching quality of GT tracks to estimated tracks, without penalizing spurious tracks. β additionally penalizes non-paired (spurious) estimated tracks. Computed from an optimal track pairing with a gate distance (ε = 5 px in ISBI) (L2-101). | Primary track-level comparability with the ISBI literature |
| JSC, JSCθ (ISBI) | Jaccard similarity on detections (points) and on whole tracks (L2-101) | Detection- and track-level Jaccard |
| RMSE (ISBI) | Localization error of matched points (L2-101) | LOCALIZATION_ERROR |
| MOTA | MOTA = 1 − Σ_t(m_t + fp_t + mme_t)/Σ_t g_t, with misses, false positives and mismatches summed over frames before the ratio (Bernardin & Stiefelhagen 2008, L2-105; full text read) | Comparability with MOT literature. Distance-gated matching (ε) replaces IoU for point objects. |
| IDF1 | IDF1 = 2·IDTP/(2·IDTP + IDFP + IDFN), from an optimal truth-to-result identity matching (Ristani et al. 2016, L2-106; full text read) | IDENTITY consistency |
| HOTA | HOTA_α = √(Σ_{c∈TP} A(c) / (\|TP\|+\|FN\|+\|FP\|)) = √(DetA_α · AssA_α), where A(c) is an association Jaccard; geometric mean of detection and association (Luiten et al. 2021, L2-107; full text read) | Balanced detection/association. **Adaptation (ours, not in source):** for points, the similarity is S = max(0, 1 − d/ε) in place of IoU, with α thresholds over S. |
| Fragmentation, ID switches | MOTA's mismatch count (mme) = identity switches (L2-105). TRACK_FRAGMENTATION = number of times a GT track's matched estimated ID is interrupted (or changes), per GT track. | ORDER §16 |

Several metrics are kept on purpose because one metric favours some trackers over others; Chenouard et al. report that no single method was best on all data (L2-101).

### 5.2 Δ-gating metrics (ORDER §16): computed on segments, at every τ and at frozen operating points

| Metric | Definition (segment level unless noted) |
|---|---|
| COVERAGE | Fraction of predicted segment-frames *not* held |
| ABSTENTION_RATE | 1 − COVERAGE (reported separately, and also per GT category: held true segments vs held false segments) |
| ACCURACY_CONDITIONAL_ON_NON_ABSTENTION | Among non-held predicted segment-frames: fraction matched to a GT particle within ε with the correct GT identity |
| FALSE_POSITIVE_RATE | Non-held predicted segment-frames that match no GT particle, divided by all non-held. **HIGH_COST_FP** subset: non-held predictions inside TRUE_FALSE_DETECTION_REGIONS, or continuing a track *after* TRUE_DISAPPEARANCE ("ghost continuation") |
| FALSE_NEGATIVE_RATE | GT particle-frames, outside signal-loss windows, with no non-held prediction, divided by GT particle-frames outside signal-loss windows. Reported also *including* signal-loss windows. |
| TRACK_FRAGMENTATION | As §5.1, on non-held output (holding can create fragments, so this is a real cost) |
| IDENTITY_SWITCHES | As §5.1, on non-held output |
| LOCALIZATION_ERROR | RMSE on non-held matched points |
| CALIBRATION | Δ is mapped to P(segment correct) by isotonic regression on DEV. On TEST: Brier score and reliability diagram (L2-041, L2-022) |
| Risk–coverage curve, AURC | Selective risk (HIGH_COST_FP rate) vs coverage (L2-033) |

**Signal-loss behavior (a special case where HOLD is *correct*):** during TRUE_SIGNAL_LOSS_WINDOWS the correct output is HOLD/unknown. It is neither "absent" nor a hallucinated position. HOLD_ACCURACY_IN_LOSS_WINDOWS is the fraction of loss-window frames that are held rather than asserted, and is reported separately.

## 6. Pipelines (fair comparison; full detail in G10)

Every pipeline = DETECTOR + LINKER (+ STATE_ESTIMATOR) + optional Δ.

| ID | Pipeline | Components |
|---|---|---|
| P1 | LoG + LAP | TrackMate LoG detector + LAP tracker with gap closing (TrackMate, L2-108/109; LAP after Jaqaman 2008, L2-110) |
| P2 | LoG + Kalman | TrackMate LoG + linear-motion Kalman tracker (L2-108; Kalman 1960, L2-111) |
| P3 | Spotiflow + LAP | Deep spot detector (L2-112) + LAP |
| P4 | u-track (full) | Jaqaman 2008 / u-track3D: detection + LAP with gap closing and merge/split (L2-110, L2-113) |
| P5 | Probabilistic data association | Godinez & Rohr 2015 (L2-114) |
| P6 | Particle filter | Smal et al. 2008 (L2-115) |
| P7 | Deep tracker | Spilger et al. 2021 (L2-116) and/or Trackastra (L2-117) with a good detector |
| P8 | Optical-flow-assisted linking | Horn–Schunck flow (L2-118) as a motion prior for LAP costs. Expected to be weak for sparse puncta; kept as the ORDER §14 comparator, not as a strawman. |
| P-PH | PH detector + LAP | Per-frame cubical superlevel-set persistence (L2-119, L2-120); 0-dim pairs above a persistence threshold become spots; LAP linking |
| P-PH-V | PH + vineyard Δ | As P-PH, with Δ-PH from persistence vineyards over time (L2-121) |

**Fairness rules:**
1. Every pipeline gets the same DEV movies and the same hyperparameter-search budget (e.g., 100 configurations, random search, frozen search spaces).
2. Thresholds are tuned for β (primary) on DEV, separately per SNR level. Every pipeline may tune per condition, or none may.
3. Deep models are trained only on DEV-generator movies with disjoint seeds. Pretrained weights are also reported.
4. Identical drift-correction preprocessing is either applied to all pipelines or to none.
5. Every pipeline gets the same Δ wrapper options (Δ-COST, Δ-DISAGREE), so that Δ-PH is compared against strong non-PH hold policies, not against "no hold".

**Null comparator:** random holding at matched coverage. Δ must beat it.

## 7. Hypotheses and decision rules (frozen; margins `DEFAULT_PENDING_OPERATOR`)

**H-B0-1 (Δ as hold policy; primary, ORDER §16).** At COVERAGE ≥ 0.80, Δ reduces the HIGH_COST_FP rate relative to the *best* non-Δ-PH hold policy (Δ-COST or Δ-DISAGREE on the best pipeline) at equal coverage, by ≥ 25% relative. The difference in FALSE_NEGATIVE_RATE (excluding loss windows) must stay ≤ +5 pp.

**H-B0-2 (PH adds value).** P-PH or Δ-PH beats the best non-PH pipeline or hold policy on any of:
- β;
- HOTA;
- AURC(HIGH_COST_FP).

The win must hold in ≥ 1 preregistered condition family, with Holm correction across families. Otherwise PH is **demoted**: kept only as an optional feature, and removed from claims.

**Statistics.**
- Unit of analysis = movie.
- Paired comparisons on identical TEST movies, using a movie-level paired bootstrap.
- n_TEST = 20 movies per condition. This is an assumption; the 95% CI half-width is computed on DEV pilot variance before freeze and n is increased if the half-width exceeds 1/2 of the margin.

## 8. Gate G08-B0 (§35 gate format)

| Field | Content |
|---|---|
| INPUT | Frozen generator (hash), DEV/TEST seeds, pipeline configs tuned on DEV, Δ definitions, margins |
| PREDICATE | H-B0-1 holds at coverage ≥ 0.80 on TEST in the core grid at SNR ≥ 2. Abstention is not concentrated on true segments: held true segments / all true segments ≤ 2 × held false / all false. |
| PASS | `B0_SYNTHETIC_POC_PASS_C1`: "Δ is a useful hold policy in synthetic movies under generator vX". No biological claim. |
| FAIL | Δ provides no FP reduction beyond the best non-PH hold policy, or only does so at coverage < 0.80 ("useless through excessive abstention", ORDER §16) |
| UNKNOWN | CI straddles the margin, or the generator failed validation (GT inconsistencies) |
| RECOVERY | Redesign Δ, or drop it. No retuning on TEST. A new TEST seed set is needed for any re-test. |
| FALSE_POSITIVE_RISK | Δ exploits generator artifacts (e.g., Gaussian PSF exactly matching a LoG/PH kernel; debris blobs having a distinctive shape). Mitigated by the PSF-misspecified arm and by debris drawn from several shape families. |
| FALSE_NEGATIVE_RISK | Generator too easy (all pipelines near ceiling) or too hard. Mitigated by the SNR sweep. |

## 9. Major claim (§35)

| Field | Content |
|---|---|
| OBSERVATION | Established particle-tracking evaluation already provides controlled synthetic scenarios, SNR definitions and track-level metrics (ISBI 2012 challenge). No single method was best on all data. |
| SOURCE | L2-101; L2-104; L2-105–107 |
| SOURCE_CLASS | PEER_REVIEWED; VENDOR_OR_PROJECT_DOC (Icy plugin page) |
| INTERPRETATION | B0 should be built on that evaluation tradition, with additional GT labels for disappearance, false-detection regions and signal-loss windows, which the Δ-hold question needs. |
| ALTERNATIVE | Use only the original ISBI data. Its current public availability is UNVERIFIED (the bioimageanalysis.org/track page returned 404 on 2026-10-05), and it lacks the loss-window labels. |
| UNCERTAINTY | Whether synthetic results transfer (B1). The original Δ definition (GAP-L2-02). |
| FALSIFIER | Δ-PH fails to beat Δ-COST/Δ-DISAGREE at matched coverage → PH demoted. |
| IMPACT_ON_R10R9 | B0 is fully specifiable now. Any "real vesicle" language is removed until B1. |
