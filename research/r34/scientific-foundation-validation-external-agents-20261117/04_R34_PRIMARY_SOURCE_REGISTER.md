# R34 primary source register | externally audited references
SOURCE_CLASS = PRIMARY_OR_DIRECTLY_PUBLISHED_STANDARD
STATUS = RESEARCH_REFERENCES_ONLY_NOT_PROOF_OF_LOCAL_RUN
DATE = 2026-11-17

P01 Lean validating a proof: https://lean-lang.org/doc/reference/latest/ValidatingProofs/
Interpretation: #print axioms, sorryAx, trusted theorem statement, kernel. A checked proposition is not real delivery. Exact 4.36.0 runtime bytes not present in this research.
P02 RFC 8785 JCS: https://www.rfc-editor.org/rfc/rfc8785.html
Interpretation: I-JSON, no duplicate keys, ECMAScript number output, Unicode as-is (no NFC/NFD normalization), UTF-16 key order. Canonical content digest does not authenticate sender.
P03 BIPM JCGM official catalogue: https://www.bipm.org/en/committees/jc/jcgm/publications/
Interpretation: JCGM 100:2008 and amendment 1:2026 on nonlinear models, GUM-6:2020, JCGM 101:2008 Monte Carlo. No measured uncertainty for BodyTwin without reference data.
P04 OWASP XSS prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
Interpretation: HTML context-sensitive escaping; validation alone not enough. Current R33-R2 source uses html.escape; independent replay and exhaustive data-lane checks still open.
P05 SLSA build provenance v1.2: https://slsa.dev/spec/v1.2/build-provenance
Interpretation: source/build provenance, not empirical truth. No agent identity implied by file path.
P06 GitHub immutable file permalinks: https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files
Interpretation: cite exact commit SHA not moving branch for evidence.
P07 TLA+ TLC first-party docs: https://docs.tlapl.us/using:tlc:start
Interpretation: bounded model exploration; document finite state domain and fairness assumption; production network behavior remains unproved.
P08 BIPM measurement model GUM-6 and JCGM100:
https://doi.org/10.59161/JCGMGUM-6-2020
https://doi.org/10.59161/JCGM100-2008E
P09 NIST SP 800-218 final security framework: https://csrc.nist.gov/pubs/sp/800/218/final
Interpretation: secure development evidence; no clinical claim.
P10 Official NEXUS Git source custody:
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/363
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/366
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/367
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/368
https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/369
Actual evidence is in exact immutable full heads recorded in 00, not PR URL current state.

Source limits: Material from NEXUS is owner/producer evidence, not a published external scientific replication. References above guide method; they do not verify host toolchains, original hidden source, independent WWW or actual sensor accuracy.
