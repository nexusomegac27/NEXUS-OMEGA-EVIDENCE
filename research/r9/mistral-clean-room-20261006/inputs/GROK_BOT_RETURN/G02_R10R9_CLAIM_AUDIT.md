# G02 — R10R9 CLAIM AUDIT (Lane 1, GROK-BOT external non-lineage reviewer)

CLAIM_CEILING: C1_DESCRIPTIVE_ONLY · LAST_VERIFIED: 2026-10-05 · Source IDs refer to `G01_part_lane1.csv` (prefix L1-).
Stance: skeptical outside review. The goal is to reduce claims to what primary sources support, not to confirm them.

## 0. Global precondition — the operator's R10R9 draft is missing

```
MATERIAL_AMBIGUITY_ID: MA-L1-01  (R10R9 draft text unavailable)
OBSERVATION: The R10R9 draft is not in either repo (L1-053, L1-056; see work/REPO_CONTEXT_lane1.md). ORDER.txt only paraphrases it (sec. 31 is a list of topic names; sec. 12 quotes one contradiction).
ASSUMPTION_OPTIONS: (A) each sec.-31 topic names the most likely public referent checked below; (B) the draft cites different works under the same names.
CONSEQUENCE_MATRIX: if A holds and the verdict is right, the audit applies directly. If B holds, every verdict below is about the referent, not the operator's wording, so each verdict must be re-bound to the draft's exact citations.
RECOMMENDED_DEFAULT: A, with no wording-level verdicts. Every row says "MOST_LIKELY_REFERENT_CHECKED".
BLOCKS_WHAT: any statement that "R10R9 says X and X is wrong" at wording level; final acceptance of R10R9 citations.
DOES_NOT_BLOCK_WHAT: status/class verdicts on the referents themselves; claim-language normalization; Part C threat model.
WHAT_WOULD_CHANGE: the draft text or a hash/URL of it committed to a repo.
```

## 1. Verification of the ORDER's sec.-4 "source corrections" (independent)

| # | Order's correction | Independent result | Evidence |
|---|---|---|---|
| 4.1 | SCITT architecture = RFC 9943, Proposed Standard, June 2026 | **CONFIRMED** (also: from draft-ietf-scitt-architecture-22; companion RFC 9942 COSE Receipts is also a PS from June 2026) | L1-001, L1-002 (rfc-editor.org JSON + text) |
| 4.2 | A2A latest released version 1.0.0; official position "stable/production-ready open standard" | **PARTIALLY CONFIRMED / CORRECTION NEEDED.** The protocol version is 1.0 and the spec page says "Latest Released Version 1.0.0". But the latest GitHub release is **v1.0.1 (2026-05-28)**, a patch release. Spec §3.6 says patch numbers are not negotiated, so the protocol version stays 1.0. The words **"stable"/"production-ready" were NOT found** on the spec, home or what's-new pages I fetched; the spec says "open standard" and "Enterprise Ready". A2A is an LF project spec, **not an SDO standard**. | L1-004, L1-005, L1-006 |
| 4.3 | MCP: interaction/transport layer, not a governance layer | **CONFIRMED** and bound to the current version **2026-07-28**. The spec itself says "MCP itself cannot enforce these security principles at the protocol level". Authorization is OAuth-based and resource/audience-bound. | L1-007..L1-010 |
| 4.4 | draft-bondar-wca-00 expired, individual draft, not a standard | **CONFIRMED** (rev 00 only; datatracker state "Expired"; group none; dated 2026-03-01; expired 2026-09-02). **Additional fact:** the *intended status is Informational*, so it was never on the standards track. | L1-003 |
| 4.5 | SLSA = build/supply-chain integrity, not semantic truth | **CONFIRMED.** SLSA v1.2 was approved on 2025-11-24. Its own "What SLSA doesn't cover" section excludes code quality, producer trust and transitive trust. Build L1 provenance "may be incomplete and/or unsigned" and is "trivial to bypass or forge". | L1-011, L1-012 |

## 2. Sec.-31 item audit

Format per item: REFERENT_CHECKED · VERDICT (sec. 31) · major-claim block (sec. 35) · NORMALIZED_CLAIM (sec. 32).

### 2.1 Non-compensatory runtime assurance contracts
- REFERENT_CHECKED: arXiv:2609.39717v1 (Zabolotnii, 2026-09-30) [L1-016]; arXiv:2608.11274v1 (position paper) [L1-017].
- **VERDICT: PREPRINT + VERIFIED_WITH_DEMOTION**
- OBSERVATION: The paper defines Runtime Assurance Contracts in which any failed or unknown mandatory gate forces retry, switch, escalation, deferral or stop, and the gates cannot be traded off against a score. In a study of 280 *constructed* cases, a score rule admitted 80 of 100 block-required injections. A score rule tuned in hindsight matched the gate conjunction. The authors write that the results "establish neither deployed safety nor cross-domain effectiveness".
- SOURCE_CLASS: PREPRINT (single author, 5 days old at verification, author comment "no deployment claim").
- INTERPRETATION: This supports the *design argument* that NEXUS gates should be non-compensatory and that UNKNOWN should not mean PASS. The same failure mode appears inside NEXUS: the R10R8 caveat that missing GATE2/GATE3 default to VERIFIED [L1-053].
- ALTERNATIVE: A well-calibrated score with hard floors is equivalent in practice. The paper itself shows that a hindsight-tuned score matches the gates.
- UNCERTAINTY: high. The evidence is synthetic and has not been replicated.
- FALSIFIER: a deployment or field study where compensatory scoring with floors performs as well as or better than gate conjunction under distribution shift.
- IMPACT_ON_R10R9: R10R9 may cite this only as a formal proposal. It must not say the approach is "proven", and NEXUS's own fail-open default must be fixed before it claims non-compensatory gating.
- NORMALIZED_CLAIM: "Non-compensatory runtime assurance contracts are **formally proposed in** Zabolotnii (arXiv:2609.39717, preprint) and **demonstrated on** 280 synthetic constructed cases; deployed effectiveness is **not yet empirically established**."

### 2.2 Ternary logic / "Epistemic Hold"
- REFERENT_CHECKED: Ternary Moral Logic (TML) / TernaryLogic by L. Goukassian [L1-018], plus two AI and Ethics articles [L1-019, L1-020].
- **VERDICT: VERIFIED_WITH_DEMOTION** (the concept exists as a self-published framework with two articles in a peer-reviewed venue; the compliance and certification claims are unverified).
- OBSERVATION: The repo defines three states +1 / 0 / −1. State 0 is "Sacred Zero" / "Epistemic Hold". The rule is "No Log = No Action". The repo self-claims EU AI Act satisfaction and "Level 3 Certified" conformance, and I found no independent certifier.
- SOURCE_CLASS: VENDOR_OR_PROJECT_DOC (repo); PEER_REVIEWED (bibliographic existence of the two articles via Crossref; their content was not audited).
- INTERPRETATION: "Epistemic Hold" is a *named proposal*, not an established logic. Three-valued decision states (allow / hold / deny) are generic. NEXUS's own PASS/FAIL/UNKNOWN gate format already gives a ternary outcome without importing TML.
- ALTERNATIVE: R10R9 may mean generic three-valued logic, or three-valued runtime monitors. That literature was **not re-fetched by Lane 1** and is therefore not cited here.
- UNCERTAINTY: high about the referent (MA-L1-03); low about TML's status.
- FALSIFIER: the R10R9 draft cites a different, peer-reviewed formalism.
- IMPACT_ON_R10R9: use neutral terms (UNKNOWN / HOLD). Do not import TML branding or its compliance claims. A repo commit had already rejected "ternary overclaims" earlier (REPO_CONTEXT §4).
- NORMALIZED_CLAIM: "A ternary allow/hold/deny decision state with an 'Epistemic Hold' is **formally proposed in** the Ternary Moral Logic project (self-published; related articles **reported in** AI and Ethics 2025/2026); its effectiveness and regulatory conformance are **not yet empirically established**."

### 2.3 DITL hardware claim
- REFERENT_CHECKED: TernaryLogic `No_Log-No_Action/readme.md` [L1-021] and `Hardware_Architecture/readme.md` [L1-022].
- **VERDICT: MISCHARACTERIZED** (if R10R9 presents DITL as existing or working hardware).
- OBSERVATION: The project's own text says, verbatim: "DITL/MT has been demonstrated at transistor simulation level (IBM PDK 1.2V 130nm CMOS). No fabricated DITL chip exists as of the date of this specification." A second project document names "TSMC N2 CoWoS ReRAM 1T1R 2025 PDK" as the fabrication baseline. That is a target node that contradicts the 130 nm simulation basis.
- SOURCE_CLASS: VENDOR_OR_PROJECT_DOC.
- INTERPRETATION: At most, this is a simulation-level circuit concept. The project's own documents disagree with each other about the process node.
- ALTERNATIVE: "DITL" in R10R9 may mean something else (MA-L1-07; no other referent found).
- UNCERTAINTY: low that no chip exists, since the source denies it itself.
- FALSIFIER: a fabricated-die measurement paper or tape-out record.
- IMPACT_ON_R10R9: remove any hardware-enforcement claim. Software "Architecture B" is the only shipping baseline the source names.
- NORMALIZED_CLAIM: "A DITL/MT circuit is **reported in** project documentation as **demonstrated on** transistor-level simulation only (IBM 130 nm PDK); no fabricated hardware exists per the same source."

### 2.4 W3C PROV
- REFERENT_CHECKED: PROV-DM and PROV-O [L1-013, L1-014]; PROV-Overview Note [L1-015].
- **VERDICT: STANDARD** (W3C Recommendations, 2013-04-30) — VERIFIED_EXACT as to status.
- OBSERVATION: PROV defines Entity, Activity and Agent, derivation, attribution and delegation (actedOnBehalfOf).
- INTERPRETATION: PROV is a provenance *vocabulary*. It has no integrity, signature or authorization semantics, and PROV assertions can be false.
- ALTERNATIVE: none material.
- FALSIFIER: none for status. A use-level falsifier would be R10R9 treating a PROV record as proof.
- IMPACT_ON_R10R9: suitable as the serialization vocabulary for lineage edges. It must be paired with signing (COSE/JWS) and transparency (SCITT) to carry any integrity claim.
- NORMALIZED_CLAIM: "Provenance interchange is **standardized for** data models by W3C PROV-DM/PROV-O (Recommendations, 2013); PROV does not provide integrity or authorization."

### 2.5 SCITT
- REFERENT_CHECKED: RFC 9943 [L1-001], RFC 9942 [L1-002].
- **VERDICT: STANDARD** (IETF Proposed Standard, June 2026) — VERIFIED_EXACT.
- OBSERVATION: Signed Statements are COSE_Sign1 with CWT iss/sub claims. Transparency Services issue COSE Receipts and maintain trust anchors and registration policies. The VDS is append-only, non-equivocating and replayable. Several things are explicitly out of scope or not guaranteed:
  - truth of the statement (§9.2: registration "only proves it was produced by an Issuer");
  - issuance ordering (§9.1);
  - completeness (§9.3: issuers can register selectively);
  - client authN/authZ, key discovery and revocation.
- INTERPRETATION: SCITT fits NAC-3 (transparency attestation) and the order's rules SCITT_RECEIPT ≠ NEXUS_AUTHORIZATION and SCITT_RECEIPT ≠ SCIENTIFIC_VALIDITY.
- ALTERNATIVE: CT-style logs (RFC 9162 [L1-043]) or Sigstore-like logs. Sigstore was not verified by Lane 1.
- FALSIFIER: none for status.
- IMPACT_ON_R10R9: cite as Proposed Standard, not "Internet Standard". R10R9 must not infer issuance order or completeness from receipts.
- NORMALIZED_CLAIM: "Transparent registration of signed statements is **standardized for** supply-chain use in RFC 9943 (IETF Proposed Standard, June 2026); a receipt proves registration, not truth, order of issuance, or completeness."

### 2.6 SLSA
- REFERENT_CHECKED: SLSA v1.2 [L1-011, L1-012].
- **VERDICT: VERIFIED_EXACT** as an approved community specification. If R10R9 calls SLSA an "SDO standard", the verdict becomes **VERIFIED_WITH_DEMOTION**.
- OBSERVATION: Build L0–L3 are defined. L1 provenance "may be incomplete and/or unsigned" and is "trivial to bypass or forge". L2 adds signed provenance from a hosted platform; L3 adds a hardened platform. v1.2 adds a Source Track. SLSA states it does not cover code quality, producer trust or transitive trust.
- INTERPRETATION: SLSA levels measure the trustworthiness of *build provenance*, not the semantic truth of claims. WCA explicitly borrowed the levelling idea [L1-003].
- FALSIFIER: none for status.
- IMPACT_ON_R10R9: use SLSA only for code/artifact build integrity of NEXUS tooling. Do not map SLSA levels to epistemic confidence.
- NORMALIZED_CLAIM: "Build-provenance integrity levels are **standardized for** software supply chains by the SLSA v1.2 community specification (approved 2025-11-24); SLSA does not address semantic correctness."

### 2.7 WCA / WAL
- REFERENT_CHECKED: draft-bondar-wca-00 [L1-003].
- **VERDICT: DRAFT_ONLY** (expired individual I-D; Informational intent).
- OBSERVATION: WAL-0 means no provenance. WAL-1: provenance logged, crypto optional. WAL-2: signed source responses with Domain-WCA-certified Ed25519/P-256 keys. WAL-3: reference-monitor properties RM1–RM3, a hash-chained attestation log and signed nonce queries. The draft coins the term "semantic laundering".
- INTERPRETATION: The draft is a useful design vocabulary. It has no standing, no WG adoption, no consensus and no known implementations (none verified).
- ALTERNATIVE: none.
- FALSIFIER: a -01 revision, WG adoption, or RFC publication. On 2026-10-05 the datatracker showed rev 00 only.
- IMPACT_ON_R10R9: cite as "an expired individual Internet-Draft". Do not cite it as a "standard" or "IETF framework". Crosswalk only (see G12).
- NORMALIZED_CLAIM: "Warrant Assurance Levels are **formally proposed in** draft-bondar-wca-00 (individual Internet-Draft, Informational intent, expired 2026-09-02); not standardized."

### 2.8 DREAM v3
- REFERENT_CHECKED: "DREAM v3 — Dynamic Retention Episodic Architecture for Memory" (M. Pereira da Silva, Zenodo preprint 2026-07-19) [L1-023], plus the author blog [L1-024].
- **VERDICT: PREPRINT + VERIFIED_WITH_DEMOTION.** The canonical Zenodo DOI was **NOT retrieved**: the Zenodo API and Crossref returned no match, so the identifier is UNVERIFIED and the record is located only through an index page.
- OBSERVATION: The paper separates memory *retention* from *influence* and uses a Hygiene Gate (allow/uncertain/block) and hash-chained traces. All results are synthetic: 100% grounding fidelity, 0% false reinforcement, a 7,000-run ablation, and 34.3% false reinforcement when retention and influence are merged. The author says the work does not establish generalization.
- INTERPRETATION: It is conceptually close to NEXUS's D_EPISTEMIC/D_CONTROL split (PR #45 [L1-054]). It is not independent evidence.
- ALTERNATIVE: R10R9 may mean **DreamerV3** (world-model RL). That paper was **not checked** (MA-L1-04).
- FALSIFIER: a DOI or record showing a different version or authorship; independent replication.
- IMPACT_ON_R10R9: cite as a single-author preprint with synthetic results. The 100% and 0% figures must not be quoted as performance claims.
- NORMALIZED_CLAIM: "Separation of memory retention and influence is **formally proposed in** DREAM v3 (independent preprint, 2026) and **demonstrated on** synthetic benchmarks only; generalization is **not yet empirically established**."

### 2.9 VAIL
- REFERENT_CHECKED: (a) projectvail.com, "VAIL — Verification Infrastructure for AI Systems" [L1-025]; (b) "VAL — Verifiable Authorization Lineage", draft v0.1 [L1-026].
- **VERDICT: NOT_FOUND** as a standard or peer-reviewed method named "VAIL". (a) exists only as a vendor product site. Its "our ICML 2026 paper" claim is UNVERIFIED.
- MATERIAL_AMBIGUITY_ID: **MA-L1-02** (VAIL vendor vs VAL protocol vs another acronym).
  - ASSUMPTION_OPTIONS: A = vendor VAIL; B = VAL draft protocol; C = something else.
  - CONSEQUENCE_MATRIX: under A, the source is vendor marketing and cannot support claims. Under B, it is a draft protocol and close Part C prior art. Under C, the source is unknown.
  - RECOMMENDED_DEFAULT: treat it as VENDOR_OR_PROJECT_DOC with no supporting weight.
  - BLOCKS_WHAT: any R10R9 claim leaning on "VAIL".
  - DOES_NOT_BLOCK_WHAT: Part C, which has stronger prior art (Biscuit, UCAN, RFC 8693).
- FALSIFIER / IMPACT: the R10R9 citation decides between the options. Drop VAIL from load-bearing claims.
- NORMALIZED_CLAIM: "A commercial runtime verification offering named VAIL is **reported in** vendor material; no standard or peer-reviewed VAIL method was found."

### 2.10 Persistent-homology vesicle tracking
- REFERENT_CHECKED: Assaf et al., IJIST 31(2):753–762, DOI 10.1002/ima.22503 [L1-027]; Oda et al., Sci. Rep. 2023 [L1-028].
- **VERDICT: PEER_REVIEWED + VERIFIED_WITH_DEMOTION.**
- OBSERVATION: Relative persistent homology detected moving vesicles on **one synthetic and two real** quantitative-phase sequences. The only comparison was with one newly developed tracking tool, and the stated strength is independence from prior parameters. Oda et al. used 9 cell datasets and compared against Image-Pro and watershed.
- INTERPRETATION: The method exists and is peer-reviewed. The evidence base is tiny. There is no standard benchmark and no claim of superiority over modern trackers.
- ALTERNATIVE: there may be more recent PH tracking work that I did not verify.
- FALSIFIER: a benchmark (e.g. Cell Tracking Challenge) result for PH methods. Not checked here.
- IMPACT_ON_R10R9: the order's sec. 12 notes that R10R9 contradicts itself on "real vesicles". The source does use real vesicle images, but only 2 sequences. Any "validated on real vesicles" wording must say n=2.
- NORMALIZED_CLAIM: "Relative persistent homology for 2D+t vesicle track detection is **demonstrated on** one synthetic and two real quantitative-phase sequences (Assaf et al., peer-reviewed, 2020/2021)."

### 2.11 ERC-8370
- REFERENT_CHECKED: ethereum/ERCs PR #1930 "Inheritable Agent Mandates" [L1-029].
- **VERDICT: DRAFT_ONLY.** The PR is open and unmerged, labelled s-draft / c-new / e-review, and mergeable_state is "blocked". It has not reached Draft status in the ERC repo.
- OBSERVATION: The proposal requires child ⊆ parent on every clause. It adds a depth counter ("telomere") and a freeze cascade. A Base Sepolia reference implementation is claimed but was not verified.
- INTERPRETATION: It is prior art for attenuation and parallels Part C's rule CHILD_SCOPE ⊆ PARENT_SCOPE. It carries no standards weight.
- FALSIFIER: merge as an ERC Draft or a status change.
- IMPACT_ON_R10R9: cite as an "unmerged ERC proposal".
- NORMALIZED_CLAIM: "Clause-wise mandate attenuation for agents is **formally proposed in** an unmerged ERC pull request (ERC-8370, PR #1930, opened 2026-08-05)."

### 2.12 Multi-agent constitutional design
- REFERENT_CHECKED: arXiv:2603.13189 (CMAG) [L1-030], arXiv:2602.00755 [L1-031], Constitutional AI arXiv:2212.08073 [L1-032].
- **VERDICT: PREPRINT.**
- OBSERVATION: CMAG is a simulation and its author-stated AMSTA 2026 acceptance is forthcoming and unverified. 2602.00755 is a grid-world simulation. Constitutional AI is a *training-time* method for a single model.
- INTERPRETATION: There is no empirical evidence that runtime multi-agent constitutions improve governance in real deployments. Conflating CAI (training) with runtime constitutions is a mischaracterization risk.
- ALTERNATIVE: R10R9 may mean the PR #45 citations (same arXiv IDs). MA-L1-05.
- FALSIFIER: a peer-reviewed field evaluation.
- IMPACT_ON_R10R9: label these as design inspiration only.
- NORMALIZED_CLAIM: "Constitutional governance of multi-agent LLM systems is **formally proposed in** preprints (arXiv:2603.13189; arXiv:2602.00755) and **demonstrated on** simulations only."

### 2.13 A2A
- REFERENT_CHECKED: the A2A spec (latest), and GitHub releases v1.0.0 and v1.0.1 [L1-004..006].
- **VERDICT: VERIFIED_WITH_DEMOTION.** "1.0.0 latest" is SUPERSEDED at patch level by v1.0.1, and "production-ready" wording is UNVERIFIED (MA-L1-06).
- OBSERVATION: Protocol version 1.0. AgentCard JWS signatures over RFC 8785-canonicalized JSON. Authorization is implementation-specific, and servers must authorize every request.
- INTERPRETATION: A2A is a transport/interaction protocol with authentication hooks. It provides no epistemic or governance semantics.
- FALSIFIER: an official A2A page using "production-ready" (not found on the pages fetched).
- IMPACT_ON_R10R9: write "A2A protocol version 1.0 (latest release v1.0.1, 2026-05-28)".
- NORMALIZED_CLAIM: "Agent-to-agent interaction is **standardized for** interoperability by the A2A project specification (protocol v1.0; latest release v1.0.1; Linux Foundation project, not an SDO standard)."

### 2.14 MCP
- REFERENT_CHECKED: MCP spec 2026-07-28 [L1-007..010], OAuth 2.1 draft [L1-052].
- **VERDICT: VERIFIED_EXACT** for the version (current = 2026-07-28; previous = 2025-11-25).
- OBSERVATION: This version is stateless: there is no initialize handshake and no sessions. Authorization requires RFC 8707 audience binding and forbids token passthrough. The spec says it "cannot enforce these security principles at the protocol level". Its OAuth 2.1 dependency is an Internet-Draft: MCP cites -13, while -16 is current.
- INTERPRETATION: MCP is a tool/context interaction layer, not governance (sec. 4.3 confirmed). Any document written against pre-2026-07-28 MCP (sessions, initialize, sampling) is now outdated.
- IMPACT_ON_R10R9: pin to 2026-07-28 and remove any reliance on deprecated Roots/Sampling/Logging or sessions.
- NORMALIZED_CLAIM: "Tool/context interaction is **standardized for** LLM hosts by the MCP project specification (version 2026-07-28); MCP explicitly does not enforce security or governance at the protocol level."

## 3. Summary table

| Item | Verdict | Load-bearing allowed? |
|---|---|---|
| Non-compensatory RAC | PREPRINT / VERIFIED_WITH_DEMOTION | design argument only |
| Ternary / Epistemic Hold | VERIFIED_WITH_DEMOTION | no (use neutral UNKNOWN/HOLD) |
| DITL hardware | MISCHARACTERIZED | no |
| W3C PROV | STANDARD | vocabulary only |
| SCITT | STANDARD (PS) | yes, for registration/transparency only |
| SLSA | VERIFIED_EXACT (community spec) | build integrity only |
| WCA/WAL | DRAFT_ONLY | vocabulary only |
| DREAM v3 | PREPRINT / VERIFIED_WITH_DEMOTION (DOI unverified) | no |
| VAIL | NOT_FOUND (as standard/method); ambiguity | no |
| PH vesicle tracking | PEER_REVIEWED / VERIFIED_WITH_DEMOTION | only with n=2 caveat |
| ERC-8370 | DRAFT_ONLY (unmerged) | prior-art idea only |
| Multi-agent constitutional design | PREPRINT | no |
| A2A | VERIFIED_WITH_DEMOTION (patch superseded; wording unverified) | transport only |
| MCP | VERIFIED_EXACT (2026-07-28) | interaction layer only |

## 4. Material ambiguities register
- MA-L1-01: the R10R9 draft text is absent (§0).
- MA-L1-02: VAIL vendor vs VAL protocol vs another referent.
- MA-L1-03: ternary logic referent (TML vs generic three-valued logic/monitors).
- MA-L1-04: DREAM v3 (Pereira da Silva) vs DreamerV3 (world-model RL; not checked).
- MA-L1-05: the "multi-agent constitutional design" referent (CMAG / 2602.00755 / CAI conflation).
- MA-L1-06: the A2A "stable/production-ready" wording is not found in first-party pages.
- MA-L1-07: "DITL" — only the TernaryLogic referent was found.
Each uses the same RECOMMENDED_DEFAULT as MA-L1-01 (bind to the checked referent, non-load-bearing), and each would change if the R10R9 draft's exact citations become available.
