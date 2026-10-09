# GROK_R14_ADVERSARIAL_FIXTURE_MATRIX.md

**OBJECT:** `NEXUS_OMEGA_AXIOM_TO_GROK_R14_SATELLITE_EMPIRICAL_MILESTONE_PREPARATION_20261009_R0`  
**PARENT:** `NEXUS_OMEGA_SATELLITE_AUTARKY_C1_CONSOLIDATED_STATUS_AND_R13_COMPLIANT_EXECUTION_20261009_R0`  
**PARENT_SHA256:** `905edf392236270bcf58e78e7673b5832bf3e1eefffec40b911c435c7b26369e`  
**ARTIFACT_SHA256:** *to be computed after final write*  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**SCOPE:** `PREPARE_ONLY` / `NO_EXECUTION`  
**DATE_UTC:** 2026-10-09  

---

## 1. Purpose

Define eight adversarial checks that must be satisfiable before any claim of the form  
“real satellite signal → local decode → verified C1 receipt” can be advanced beyond C1_DESCRIPTIVE.

All tests remain **NOT_RUN** under the present R14 PREPARE_ONLY order.

---

## 2. Adversarial Fixture Matrix

### AF-01 — Synthetic Signal Instead of Real Satellite Reception

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | A purely software-generated or laboratory-modulated signal can be made to look identical to a real satellite downlink after decoding. |
| **Test data**          | IQ file produced by a GNU Radio modulator (or commercial simulator) using the exact modulation parameters of the target satellite, plus a real over-the-air capture of the same satellite (when available). |
| **Expected result**    | Both files may decode to valid frames, but only the real capture carries independent pass-geometry / Doppler residual evidence. |
| **Falsification criterion** | If a synthetic file is accepted as `REAL_SATELLITE_OVER_THE_AIR` solely on the basis of a successful decode, the classification is falsified. |
| **Remaining uncertainty** | Even a real capture can be replayed; additional temporal and geometric provenance is required. |
| **Status**             | `NOT_RUN` |

### AF-02 — False Satellite Identification

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | A correctly decoded frame from satellite A can be labelled as originating from satellite B. |
| **Test data**          | Two distinct satellites that share similar modulation (e.g. two 9k6 GMSK CubeSats) with known different NORAD IDs and TLEs. |
| **Expected result**    | Decoder produces frames; satellite identity must still be bound by TLE-predicted Doppler, frequency, and pass timing. |
| **Falsification criterion** | Acceptance of a frame under an incorrect NORAD ID without residual checks. |
| **Remaining uncertainty** | Coincident frequency allocations or terrestrial interferers. |
| **Status**             | `NOT_RUN` |

### AF-03 — Altered or Incomplete Raw I/Q Data

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | Truncation, bit-flips, or selective editing of an IQ file can still produce a plausible decode while destroying provenance. |
| **Test data**          | Original IQ + systematically mutated copies (first/last 10 % removed, random bit flips, amplitude scaling, DC offset). |
| **Expected result**    | Some mutations still decode; the capture_sha256 and any intermediate soft-bit hashes must change. |
| **Falsification criterion** | Identical receipt hashes after mutation, or acceptance of a mutated file under the original capture_sha256. |
| **Remaining uncertainty** | Sophisticated adversarial editing that preserves hash by collision (practically negligible for SHA-256). |
| **Status**             | `NOT_RUN` |

### AF-04 — Unsuitable Decoder Configuration

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | An incorrect sample-rate, frequency offset, or SatYAML can still yield occasional frames by chance or by parameter search. |
| **Test data**          | Correct IQ of a known satellite run against deliberately wrong SatYAML / sample-rate / baud-rate settings. |
| **Expected result**    | No valid frames, or frames with failed CRC/RS that are rejected. |
| **Falsification criterion** | Acceptance of output produced under a configuration whose hash does not match the documented decoder_config_sha256. |
| **Remaining uncertainty** | Overly permissive syncword thresholds. |
| **Status**             | `NOT_RUN` |

### AF-05 — Reused or Manipulated Receipt

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | An old valid receipt can be re-submitted with a new timestamp or attached to a different capture. |
| **Test data**          | A previously issued receipt JSON + a new capture file; attempt to bind the old receipt_id / hashes to the new file. |
| **Expected result**    | parent_receipt_sha256 chain and capture_sha256 mismatch must be detected. |
| **Falsification criterion** | Acceptance of a receipt whose capture_sha256 does not match the presented IQ file. |
| **Remaining uncertainty** | Collisions or stolen private keys (out of scope for C1). |
| **Status**             | `NOT_RUN` |

### AF-06 — Unjustified PHYSICALLY_DEMONSTRATED Classification

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | The label PHYSICALLY_DEMONSTRATED can be applied on the basis of a decode alone or a prior report. |
| **Test data**          | Any fixture or report that lacks raw IQ + pass geometry + clock provenance. |
| **Expected result**    | Classification must remain REPORT_ONLY or FIXTURE_ONLY until all qualification fields of G14-B are satisfied. |
| **Falsification criterion** | Promotion of the label without the full evidence set. |
| **Remaining uncertainty** | Historical claims that can no longer be re-verified. |
| **Status**             | `NOT_RUN` |

### AF-07 — Missing or Contradictory Time Provenance

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | A capture whose start time is unknown or contradicts the predicted pass window can still be treated as valid. |
| **Test data**          | IQ files with missing, grossly wrong, or deliberately shifted timestamps. |
| **Expected result**    | Receipt must record clock_uncertainty and must fail qualification if the timestamp is incompatible with the TLE-predicted visibility window. |
| **Falsification criterion** | Acceptance of a receipt whose capture_start_utc is absent or lies outside any plausible pass. |
| **Remaining uncertainty** | Clock drift during long recordings. |
| **Status**             | `NOT_RUN` |

### AF-08 — Successful Frame Decode Without Verified Signal Origin

| Element                | Content |
|------------------------|---------|
| **Hypothesis**         | Obtaining a CRC/RS-correct frame is sufficient to claim a real satellite reception. |
| **Test data**          | Any decode that lacks at least one of: raw IQ hash, satellite identity binding, Doppler residual, or independent pass confirmation. |
| **Expected result**    | validation_status remains INCOMPLETE or HOLD. |
| **Falsification criterion** | Any claim of REAL_SATELLITE_OVER_THE_AIR based solely on frame validity. |
| **Remaining uncertainty** | Future stronger cryptographic satellite authentication (out of present amateur practice). |
| **Status**             | `NOT_RUN` |

---

## 3. Aggregate Status

```
ADVERSARIAL_FIXTURES = 8 defined, 0 executed (all NOT_RUN)
```

No test data were generated, no decoder runs were performed, and no falsification results were obtained under R14.

---

*End of GROK_R14_ADVERSARIAL_FIXTURE_MATRIX.md*  
