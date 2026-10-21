# AXIOM Alpha-Node · Publication Proof and Denominator Guard V1

OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_PUBLICATION_PROOF_DENOMINATOR_GUARD_20261021_R0
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR = NEXUS_OMEGA_ALPHA_PHYSICAL_DELIVERY_READBACK_20261021_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATUS = TESTED_ISOLATED_C1_NOT_PRODUCTION

## Falsifiable finding

Local export completeness does not prove public GitHub publication. A branch-only, PR-only, producer receipt, or blocked write is not a main-verified successful handoff. The eligible 90% denominator excludes private, inaccessible, unauthorized, non-routine, or platform-blocked items; attempted but incomplete eligible writes remain failures. Zero denominator means undefined rate.

## Isolated candidate

Publication Proof & Denominator Guard V1 checks branch/PR/CI/main/Issue #93 receipt identity against actual supplied artifact bytes, SHA-256 and Git-blob. A separately frozen evaluator (SHA-256 1f8a02236acdaef1371257a5058d01697ca68b2457a3411b802bdb217a1d1c04) produced 24/24 fixture passes and 4/4 aggregate passes; an intentional producer-self-receipt mutant produced 23/24. All fixtures are synthetic, not authenticated GitHub results.

## Limitations

Offline API snapshot consistency is NOT independent GitHub authentication. Actual publication requires fresh authenticated API readback of immutable main, blob and inbox comment. The project-wide handoff denominator is UNKNOWN; actual successes attributable to this candidate = 0. WWW parity NOT_ESTABLISHED. No claim promotion, runtime/Hostinger write, external actor authorization or node reset.

## Falsifiers

Branch-only counted as success; changed main bytes accepted; failed CI accepted; private/inaccessible items included in denominator; duplicate IDs counted twice; zero denominator reported as 100%; producer self-report treated as independently authenticated receipt.

Full local research code, frozen evaluator and fixture outcomes are isolated candidate materials; they are not claimed to be published by this report.
