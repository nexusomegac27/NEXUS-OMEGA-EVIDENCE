# G09 — PART B1 REAL-DATA VALIDATION REQUIREMENTS (R10R9, Lane 2)

```text
OBJECT        = R10R9_G09_PART_B1_REAL_DATA_VALIDATION_REQUIREMENTS_LANE2_20261005_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS        = REQUIREMENTS ONLY · NOT EXECUTED (ORDER §17: do not execute unless data is actually available)
LAST_VERIFIED = 2026-10-05
```

## 1. Minimum data requirements (ORDER §17)

Each requirement carries the reason it is needed and what happens if it is missing.

| # | Requirement | Minimum acceptable | Why | If missing |
|---|---|---|---|---|
| R1 | Real time-lapse microscopy | Raw (not compressed lossy) 2D+t or 3D+t stacks, original bit depth | Real optics and noise | No B1 |
| R2 | Vesicle or organelle label | Named construct/dye + target compartment | Defines the claim referent ("vesicles of type X") | Claims restricted to "fluorescent puncta" |
| R3 | Frame rate | Per-movie frame interval (s) | Motion-model and linking-gate validity | Movie excluded from linking metrics |
| R4 | Pixel size | µm/px (and z-step if 3D) | Unit conversion, gate ε in physical units | Movie excluded from physical-unit metrics |
| R5 | Exposure | Exposure time per frame | Noise/SNR model; dose estimate | Dose analyses impossible |
| R6 | Illumination dose (if available) | Laser line, power at sample (or setting + calibration), exposure, frames → dose estimate | Needed for any bleaching/phototoxicity dose–response (Laissue et al. 2017 recommend reporting illumination conditions and dose; L2-130) | Bleaching may be analysed only as a measured intensity trend. Phototoxicity: NO claim. |
| R7 | Manual or trustworthy track annotations | Track-level (ID across frames) annotations. ≥ 2 annotators on a ≥ 10% subset with an inter-annotator agreement metric, or a documented consensus protocol | GT for α/β/HOTA/IDF1. Δ evaluation needs identity, not just events. | Event-level only (e.g., x,y,t points) → detection metrics only, no identity metrics |
| R8 | Acquisition metadata | Microscope modality, objective NA, camera type/gain, temperature, sample prep; OME metadata preferred | Reproducibility; domain shift analysis | Movies grouped as "metadata-incomplete"; no cross-modality claims |
| R9 | License / access | Open license allowing research reuse, a citable DOI, and a version | Reproducibility receipt | Not usable |
| R10 | Split discipline | Train/tune/test split by *cell/sample/session*, not by frame | Prevents leakage of the same cell between DEV and TEST | Results downgraded to "in-sample" |
| R11 | Signal-loss annotations (desirable) | Annotator flags for "particle present but not visible", or a proxy | Lets Δ-HOLD in loss windows be scored as correct | Loss-window metric NOT_EVALUABLE on real data |

## 2. Three phenomena that must not be conflated (ORDER §17)

| Phenomenon | Operational definition for R10R9 | Observable in images alone? | Required evidence | Allowed claim |
|---|---|---|---|---|
| IMAGE_DEGRADATION | Any loss of image information content: noise, blur, defocus, drift, background rise, compression, low SNR, *including but not limited to* bleaching | Yes (image statistics, SNR per frame) | Per-frame SNR / background / sharpness metrics | "Tracking performance under measured image degradation of type X" |
| PHOTOBLEACHING | Irreversible loss of fluorophore emission caused by illumination | Partly. An intensity decay is observable, but it is confounded with focus drift, exit from the focal plane, expression changes and blinking. | Intensity-decay curves vs. dose, with controls (e.g., fixed-sample bleaching curve; non-illuminated region or delayed-start comparison) | "Intensity decay consistent with photobleaching" unless dose-linked with controls |
| PHOTOTOXICITY | Light-induced damage to the *biological specimen* that alters physiology | **No.** Laissue et al. 2017 state that phototoxicity and photobleaching are distinct, that phototoxicity can affect a sample before bleaching is measurable, and that absence of bleaching is no guarantee of absence of phototoxicity (L2-130). | A **biological endpoint**: e.g., cell-division timing, morphology, viability or a functional readout; dark/low-dose controls; dose–response (L2-130) | **NO phototoxicity claim without a biological endpoint** (ORDER §17). The B0 LIGHT_TOXICITY_PROXY is never evidence of phototoxicity. |

**Consequence for Δ.** If Δ holds more often late in a movie, the observation that may be reported is "Δ responds to time-correlated image degradation". It must never be reported as "Δ detects phototoxicity".

## 3. Candidate public datasets (only those verified to exist on 2026-10-05)

| ID | Dataset | Verified facts | Fit for B1 | Gaps |
|---|---|---|---|---|
| DS-1 | MSP-tracker data (Cambridge Apollo repository), DOI 10.17863/CAM.114339; CC BY 4.0; version dated 2025-04-11 (L2-131) | Live vesicle movies acquired with Airyscan and spinning-disk microscopy (Cad99c and Nidogen labels), with ground-truth tracks, accompanying the MSP-tracker method (PLoS Biol 2025, doi 10.1371/journal.pbio.3003099; preprint doi 10.1101/2024.01.25.577201) (L2-131, L2-132) | **Best verified fit:** real vesicles + track-level GT | Number of trajectories NOT verified. Annotation protocol and inter-annotator agreement to be checked before use. Dose metadata UNVERIFIED. |
| DS-2 | ExoDeepFinder dataset, Zenodo doi 10.5281/zenodo.11204932; paper PLoS Comput Biol 2025, doi 10.1371/journal.pcbi.1013556 (L2-133) | 120 TIRFM movies of 1001 frames; 20,567 manually annotated exocytosis events (x, y, t); single annotator; pixel 0.160 µm; ~300 ms/frame; EMCCD; 491 nm laser (L2-133) | Event-level detection and Δ-hold on *events* only | No trajectories, so identity metrics are impossible. Single annotator, so no agreement estimate. |
| DS-3 | ISBI 2012 Particle Tracking Challenge data (Chenouard et al. 2014, L2-101) | Challenge design verified from the paper | Ideal for comparability, but it is **synthetic** (B0-type), not real | Current download availability UNVERIFIED (bioimageanalysis.org/track returned 404). Do NOT use downloads.imagej.net/ISBI-2012-challenge.zip: that is the 2012 EM *segmentation* challenge, a different challenge. |
| DS-4 | Cell Tracking Challenge (Maška et al. 2023, L2-134) | Benchmark for cell segmentation/tracking | **Not suitable** for vesicle claims (cells, not sub-resolution puncta); usable only as a methods sanity check | — |

Any other dataset is `UNVERIFIED` until its DOI, license and annotation level are fetched.

## 4. B1 protocol requirements

1. **Frozen transfer.** Pipelines and Δ are tuned on B0 DEV and/or B1-DEV movies, then evaluated once on B1-TEST. The split is by cell/sample (R10).
2. **Same metrics as B0** (G08 §5), restricted to what the annotation level supports:
   - track-level GT → α, β, HOTA, IDF1, MOTA, fragmentation, IDSW;
   - event-level GT → detection Jaccard, FPR/FNR, risk–coverage.
3. **Annotation uncertainty.** Each metric is reported against each annotator separately and against the consensus. Δ "errors" on frames where annotators disagree are reported separately.
4. **Domain-shift report.** For each B1 movie, measure SNR (G08 definition), density, background and intensity-decay rate, and place it inside or outside the B0 parameter envelope. Claims are limited to movies inside the envelope.
5. **No biology claims.** B1 still validates *tracking/hold behavior*, not biological conclusions about vesicle transport.

## 5. Gate G09-B1 (§35 gate format)

| Field | Content |
|---|---|
| INPUT | Dataset (DOI, version, license, hashes), annotation description, metadata, B0 receipt |
| PREDICATE | R1–R5, R7, R9, R10 satisfied **and** G08-B0 = PASS **and** H-B0-1 replicates on B1-TEST within its margin |
| PASS | `B1_REAL_DATA_TRACKING_VALIDATION_C1` for the named dataset, label, modality and parameter envelope |
| FAIL | Δ does not reduce high-cost FPs at coverage ≥ 0.80 on real data, or abstention concentrates on true tracks |
| UNKNOWN | Annotation level is insufficient (event-only) for identity metrics; or the dataset is unavailable → `NOT_EXECUTED_DATA_UNAVAILABLE` |
| RECOVERY | Acquire or annotate data meeting R7 (≥ 2 annotators). Add dose metadata. |
| FALSE_POSITIVE_RISK | Annotators used a tracker similar to one of the pipelines to pre-annotate, which biases toward that pipeline. Check the annotation protocol. |
| FALSE_NEGATIVE_RISK | Annotation noise caps measurable performance, so true improvements are hidden. Mitigated by reporting the annotator-vs-annotator ceiling. |

## 6. Answer to Q08 (§35 major-claim format)

| Field | Content |
|---|---|
| OBSERVATION | B0 is synthetic. A biological claim requires real data with label, frame rate, pixel size, exposure, track-level annotations and metadata. A phototoxicity claim additionally needs a biological endpoint with dose control (L2-130). |
| SOURCE | ORDER §12, §17 (L2-001); L2-130; L2-131–133 |
| SOURCE_CLASS | VENDOR_OR_PROJECT_DOC (order); PEER_REVIEWED (Laissue; MSP-tracker; ExoDeepFinder) |
| INTERPRETATION | The minimum route to a *tracking* claim on real vesicles is DS-1-type data (track GT) passing G09-B1. A *biological* claim about vesicles (transport, physiology) is outside R10R9 entirely. |
| ALTERNATIVE | Event-only data (DS-2) supports a narrower claim about detecting or holding events. |
| UNCERTAINTY | DS-1 annotation protocol and size are not verified. |
| FALSIFIER | DS-1 turns out to have tracks produced by an automated tracker without manual curation. It then does not meet R7 as GT. |
| IMPACT_ON_R10R9 | All "real vesicle" wording stays blocked until G09-B1 PASS. |
