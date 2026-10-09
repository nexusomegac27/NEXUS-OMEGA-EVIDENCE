# GROK_R14_REAL_SIGNAL_QUALIFICATION_SPEC.md

**OBJECT:** `NEXUS_OMEGA_AXIOM_TO_GROK_R14_SATELLITE_EMPIRICAL_MILESTONE_PREPARATION_20261009_R0`  
**PARENT:** `NEXUS_OMEGA_SATELLITE_AUTARKY_C1_CONSOLIDATED_STATUS_AND_R13_COMPLIANT_EXECUTION_20261009_R0`  
**PARENT_SHA256:** `905edf392236270bcf58e78e7673b5832bf3e1eefffec40b911c435c7b26369e`  
**ARTIFACT_SHA256:** *to be computed after final write*  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**SCOPE:** `PREPARE_ONLY` / `NO_EXECUTION`  
**DATE_UTC:** 2026-10-09  

---

## 1. Purpose

Define the minimum scientific requirements that distinguish a **real, independently verifiable satellite reception** from:
- a simulated RF recording,
- a pre-existing fixture,
- a demodulated audio stream without provenance,
- or a decoded frame whose origin cannot be traced to an actual over-the-air emission.

The target milestone remains:  
**REAL_SATELLITE_SIGNAL → LOCAL_DECODE → VERIFIED_C1_RECEIPT**

---

## 2. Mandatory Qualification Fields

A reception qualifies as scientifically usable only when **all** of the following are present and bound:

| Field                              | Requirement                                                                 | Evidence Form                          |
|------------------------------------|-----------------------------------------------------------------------------|----------------------------------------|
| Satellite identity                 | NORAD ID + common name + TLE epoch used for pass prediction                 | TLE set + prediction log               |
| Technical specification            | Frequency (nominal + Doppler range), modulation, baud rate, protocol        | SatYAML / public reference + measurement |
| Frequency band & modulation        | Exact centre frequency, bandwidth, modulation type (BPSK/GMSK/AFSK/APT…)    | Spectrum screenshot or IQ metadata     |
| Legal passive reception            | Confirmation that only receive-only amateur-band or public downlink used    | Operator declaration + regulatory note |
| Receiver identity                  | Hardware model, serial (if available), antenna type, LNA if used            | Hardware log / photo / config dump     |
| Software versions                  | GNU Radio version, gr-satellites version, SoapySDR / driver versions        | `gr_satellites --version`, package list |
| Raw I/Q or equivalent recording    | Complex float32 or int16 IQ file covering the full pass or relevant segment | File + SHA-256                         |
| Capture start time (UTC)           | ISO-8601 with sub-second precision if possible                              | Timestamp from disciplined clock       |
| Clock uncertainty                  | Estimated max error (e.g. ±50 ms NTP, ±1 µs GPS)                             | Clock source description               |
| Reproducible demodulation params   | Sample rate, frequency offset, RRC alpha, Costas/FLL BW, syncword threshold | Exact command line or .grc parameters  |
| Decoder output                     | Hex frames, KISS, or parsed telemetry + integrity checks (CRC/RS)           | Output file + SHA-256                  |
| Raw-data hashes                    | SHA-256 of IQ file, of intermediate soft bits (if kept), of final payload   | Hash list                              |
| Positive control                   | Successful decode of a known-good public recording of the same satellite    | Reference run log                      |
| Negative control                   | Failure or empty output on noise-only or wrong-satellite recording          | Reference run log                      |

---

## 3. Distinctions That Must Be Maintained

| Stage                        | Definition                                                                 | What it does **not** prove                     |
|------------------------------|----------------------------------------------------------------------------|------------------------------------------------|
| Received RF signal           | Energy present in the expected band during a predicted pass                | Identity of the emitter                        |
| Demodulated signal           | Soft/hard symbols recovered after matched filtering / Costas / clock recovery | Correct satellite or valid framing             |
| Valid frame decoding         | Syncword found, FEC passed, CRC/RS correct                                 | That the frame originated from the claimed satellite |
| Proven satellite attribution | All of the above **plus** pass geometry, Doppler residual consistent with TLE, and exclusion of terrestrial interferers | Absolute legal identity (requires additional regulatory context) |

A successful frame decode alone is **insufficient** for the claim “real satellite signal”.

---

## 4. Recommended Reference Targets (Open, Legal, Passive)

These are publicly documented amateur / weather satellites suitable for a first empirical milestone (receive-only):

- **NOAA-15 / 18 / 19** — APT, 137.x MHz, FM + 2.4 kHz AM subcarrier (widely documented, many public IQ samples).
- **AO-73 (FUNcube-1)** — 1200 baud BPSK, 145.935 MHz (gr-satellites native support, NORAD 39444).
- **ISS APRS digipeater** — 145.825 MHz, 1200 baud AFSK AX.25 (when active).
- Any currently active CubeSat listed in the gr-satellites SatYAML collection that transmits on 145 / 435 MHz amateur allocations.

All of the above can be received legally with ordinary amateur-radio or SDR equipment under receive-only conditions in most jurisdictions; local regulations must still be verified by the operator.

---

## 5. Minimum Acceptable Capture Format

- Complex samples (I/Q), preferably float32 or int16.  
- Sample rate ≥ 4× symbol rate (preferably higher for Doppler margin).  
- Continuous recording covering at least the period of expected AOS–TCA–LOS for the selected pass, or a clearly annotated segment containing the signal of interest.  
- Metadata (SigMF recommended) containing: centre frequency, sample rate, start time UTC, receiver description, antenna, and any Doppler compensation applied.

---

## 6. Qualification Verdict Logic (for future execution)

```
IF (raw_IQ_hash_present
    AND satellite_identity_bound
    AND demod_params_reproducible
    AND decoder_output_hash_present
    AND positive_control_pass
    AND negative_control_fail
    AND clock_uncertainty_documented)
THEN validation_status = "QUALIFIED_C1_CANDIDATE"
ELSE validation_status = "INCOMPLETE"
```

No execution of the above logic has occurred under R14.

**SIGNAL_QUALIFICATION_VERDICT:** `SPECIFICATION_COMPLETE_NO_NEW_CAPTURE`

---

*End of GROK_R14_REAL_SIGNAL_QUALIFICATION_SPEC.md*  
