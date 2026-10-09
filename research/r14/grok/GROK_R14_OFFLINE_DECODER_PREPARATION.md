# GROK_R14_OFFLINE_DECODER_PREPARATION.md

**OBJECT:** `NEXUS_OMEGA_AXIOM_TO_GROK_R14_SATELLITE_EMPIRICAL_MILESTONE_PREPARATION_20261009_R0`  
**PARENT:** `NEXUS_OMEGA_SATELLITE_AUTARKY_C1_CONSOLIDATED_STATUS_AND_R13_COMPLIANT_EXECUTION_20261009_R0`  
**PARENT_SHA256:** `905edf392236270bcf58e78e7673b5832bf3e1eefffec40b911c435c7b26369e`  
**ARTIFACT_SHA256:** *to be computed after final write*  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**SCOPE:** `PREPARE_ONLY` / `NO_EXECUTION`  
**DATE_UTC:** 2026-10-09  

---

## 1. Scope Statement

This document prepares a **reproducible offline decode specification**.  
No decoder was installed, no flowgraph was run, no IQ file was processed, and no output was claimed under R14.

---

## 2. Recommended Open-Source Stack

| Component          | Role                                      | Current Reference Versions (as of research) | Notes |
|--------------------|-------------------------------------------|---------------------------------------------|-------|
| GNU Radio          | Core SDR framework                        | 3.10.x (v5.x series of gr-satellites)      | Required base |
| gr-satellites      | Satellite-specific demod + deframe + FEC  | 5.9.0 / 5.10.0-git                          | Primary decoder |
| SoapySDR + drivers | Hardware abstraction (optional for offline) | Matching GNU Radio build                    | Needed only for live RX |
| SatNOGS client / flowgraphs | Alternative capture & decode pipeline | Current Libre Space releases                | Useful for station automation |
| SigMF              | Metadata for IQ recordings                | Latest                                      | Strongly recommended |

Primary repository: https://github.com/daniestevez/gr-satellites  
Documentation: https://gr-satellites.readthedocs.io/

---

## 3. Exact Decode Specification Template (Offline)

### 3.1 Input Formats Supported by gr_satellites

- `--wavfile`   : real or complex WAV  
- `--rawfile`   : raw complex float32 (default)  
- `--rawint16`  : raw complex int16  
- `--sigmf`     : SigMF recording (preferred for provenance)

### 3.2 Canonical Command-Line Skeleton (NOT EXECUTED)

```bash
# Example skeleton only — DO NOT RUN under current HOLD
gr_satellites <SATELLITE_NAME_OR_NORAD> \
  --rawfile /path/to/capture.iq \
  --samp_rate <RATE> \
  --iq \
  --start_time <ISO8601_UTC> \
  --f_offset <Hz> \
  --rrc_alpha 0.35 \
  --kiss_out /path/to/output.kiss \
  --hexdump \
  --telemetry_output /path/to/telemetry.txt
```

Satellite may be specified by:
- common name (e.g. `FUNcube-1`),
- NORAD catalogue number (e.g. `39444`),
- path to a custom SatYAML file.

### 3.3 Required Parameter Documentation for Any Future Run

For every future decode the following must be recorded:

- Exact gr-satellites and GNU Radio version strings  
- Full command line (or .grc file hash)  
- Sample rate, centre frequency, any Doppler compensation applied  
- All tunable demodulator parameters (FLL BW, Costas BW, clock recovery, syncword threshold, etc.)  
- Input file SHA-256  
- Output KISS / hex / telemetry SHA-256  
- Start time and clock uncertainty  

### 3.4 Expected Output Artefacts

- Hex dump of recovered frames  
- Optional KISS file  
- Optional human-readable telemetry (when SatYAML contains parsers)  
- Exit status / any Reed-Solomon or CRC failure counts  

### 3.5 Negative Fixtures (to be prepared later)

- Pure noise IQ of identical length and sample rate  
- Correct modulation but wrong satellite SatYAML  
- Truncated or bit-flipped IQ  
- Audio-only recording presented as IQ  

---

## 4. SatNOGS Path (Alternative / Complementary)

SatNOGS provides ready-made flowgraphs and a global observation database.  
For offline work the relevant artefacts are:

- IQ dump option (`ENABLE_IQ_DUMP`)  
- Waterfall + audio + decoded data uploaded to network.satnogs.org  
- gr-satnogs OOT module  

A future empirical run may use either pure gr-satellites or a SatNOGS observation as the capture source; both must still satisfy the qualification fields defined in G14-B.

---

## 5. Missing Prerequisites & Reproducible Test Plan (PREPARE_ONLY)

| Prerequisite                     | Status          | Concrete Test Plan (when authorised) |
|----------------------------------|-----------------|--------------------------------------|
| GNU Radio 3.10 + gr-satellites 5.x installed | NOT present in this sandbox | Install from source or package; record versions |
| Known-good public IQ sample      | ABSENT          | Download a published recording of AO-73 or NOAA APT; compute SHA-256 |
| Positive-control run             | NOT_EXECUTED    | Decode the known-good sample; verify expected frames appear |
| Negative-control run             | NOT_EXECUTED    | Feed noise / wrong satellite; verify no false positives |
| Custom SatYAML (if needed)       | NOT created     | Create only after explicit Scope-A order |

---

## 6. Decoder Specification Verdict

```
DECODER_SPEC = COMPLETE_TEMPLATE_NO_EXECUTION
```

All parameters, input formats, version constraints and expected outputs have been defined.  
No decoder binary was invoked.

---

*End of GROK_R14_OFFLINE_DECODER_PREPARATION.md*  
