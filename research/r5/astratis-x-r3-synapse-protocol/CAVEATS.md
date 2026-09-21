# CAVEATS — Astratis X R3 synapse protocol

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ACTIVATION = NO
PROMOTION = NO

VALIDATED_PROTOTYPE_FOUNDATION != PRODUCTION_CRYPTO != PRODUCTION_DEPLOY
READY_FOR_IMPLEMENTATION != PRODUCTION_READY

CAVEAT_01 ED25519 verification is PLACEHOLDER not real crypto enforcement
CAVEAT_02 REVOKE ownership is format check not actual signer provenance lookup
CAVEAT_03 TOKEN/PoW cost_proof QUARANTINED — TOKEN_ACTIVATION=NO (do not bypass existing token quarantine)
CAVEAT_04 EMPIRICAL_NETWORK_VALIDATION=NOT_ESTABLISHED
CAVEAT_05 EXTERNAL_CROSSVALIDATION=NOT_ESTABLISHED_BY_R3_REPORT_ALONE

R4 = NOT_IMPLICITLY_AUTHORIZED
R7_SEAL = HOLD
PANDORA_TRUTH_CONTAINMENT = PRESERVED
AIRGAP = PRESERVED
TOKEN_QUARANTINE = PRESERVED
TRUTH_AUTHORITY = NONE
SOURCE+UNCERTAINTY+STATUS != FINAL_TRUTH
CONTRADICTION_PRESERVED = YES

Source reports inside META_HANDOVER_PACKAGE_FINAL.zip that describe ed25519 or token/PoW checks as PASS are report-level assertions. They do not override CAVEAT_01 or CAVEAT_03. The published Python prototype marks signature validation as a placeholder that returns success when a signature field is present, and REVOKE ownership as a UUID format check.
