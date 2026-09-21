# Astratis X / R3: validated synapse protocol (C1)

Public derivative of the Astratis X R3 archive directory. This lane extends the existing Astratis X location research/r5/astratis-x-r2-dtepn-meta/ as a sibling. It does not create a research/x/ root.

## Status

- CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
- BIND = VALIDATED_PROTOTYPE_FOUNDATION
- VALIDATED_PROTOTYPE_FOUNDATION != PRODUCTION_CRYPTO != PRODUCTION_DEPLOY
- READY_FOR_IMPLEMENTATION != PRODUCTION_READY
- ACTIVATION = NO
- INSTALLATION = NO
- DEPLOYMENT = NO
- PROMOTION = NO
- R4 = NOT_IMPLICITLY_AUTHORIZED
- R7 closed-package seal = HOLD (not closed by this lane)
- FUNDUS = UNCHANGED
- TRUTH_AUTHORITY = NONE
- SOURCE+UNCERTAINTY+STATUS != FINAL_TRUTH

## Protocol bind

PRIMARY = NEXUS_SYNAPSE_PROTOCOL

MESSAGE_TYPES = CLAIM, RECEIPT, QUERY, REVOKE

INVARIANTS = SOURCE+UNCERTAINTY+STATUS, NO_ROOT_TRANSFER, FAIL_CLOSED, NO_AUTO_RESET, CONTRADICTION_PRESERVED

STATES = NULL, NEGOTIATING, ACTIVE, DEGRADED, QUARANTINED, DEPRECATED, CONSERVED, TOMBSTONE

## Files

sources/ is a byte-exact copy of the eight archive files. Names were not repaired. SHA256SUMS covers those sources plus this README, CAVEATS.md, and .gitattributes. Limits that the source reports do not themselves bind are in CAVEATS.md.

## Path caveats (preserved)

- Windows 8.3 short name NEXUS-~1.PDF is sources/nexus-synapsen-protokoll-kausal-kanonische-vertiefung-&-validierungs-implementierung.pdf.
- Windows 8.3 short name NEXUS-~2.MD is sources/nexus-synapsen-protokoll-kausal-kanonische-vertiefung-&-validierungs-implementierung.md.
- Inside META_HANDOVER_PACKAGE_FINAL.zip the same PDF and Markdown bytes are stored as source/NEXUS-_1.PDF and source/NEXUS-_2.MD (underscore, not tilde). The zip is unchanged. Loose filenames were not renamed to match zip member names.

## What source PASS language does not establish

Computer-validation text inside the zip, including ed25519 and token/PoW PASS wording, is a source assertion. It is not production cryptography, not token activation, not empirical network validation, and not external crossvalidation. See CAVEATS.md.

Pandora truth containment and the airgap complement stay in force. This lane does not write FINAL_TRUTH.
