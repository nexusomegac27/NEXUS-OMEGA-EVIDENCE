# R44-3 authenticated evaluator admission — normative research design, not deployed

## Five independent checks
1. Verified exact DSSE typed payload bytes with normative PAE and Ed25519 TEST key, not a user-supplied string "signed" or 3/3 count.
2. Public key validated against operator-issued trust registry and key generation provenance; individual byte signature or X.509 label is insufficient.
3. Actor ID bound to verified role/lane/task, issuer, validity interval/revocation, nonce, epoch, dataset and pre-frozen evaluator; actor distinctness determined by operator-issued identity, not number of messages or signatures. Common model/source lineage reported separately.
4. Scientific reference evidence actual original code/data + blinded scorer and all negatives; a signed bad result is a BAD RESULT, not magically true.
5. Independent operator go/no-go for physical/public/merge; no cryptographic self-authorization.

## Example minimal research fields (do not use real production keys)
EVIDENCE_ID; SOURCE_OBJECT_SHA256; DSSE_PAYLOAD_TYPE; DSSE_ENVELOPE_SHA256; VERIFIED_BYTE_SIGNATURE_FLAG; ROOT_ID_FINGERPRINT; ACTOR_ROLE_ID; OPERATOR_REGISTRATION_EPOCH; SIGNER_DISTINCTNESS_LEDGER; NONCE; EXPIRES_AT; REVOKED_AT; SUBJECT_CODE_SHA; DATA_SHA; EVALUATOR_SHA; SCORER_FROZEN_AT; TRUE_INDEPENDENT_REPLAY_RECEIPT; THREAT_MODEL_VERSION; QUORUM_COUNT_IF_PROVEN; CLAIM_CEILING.
Never set VERIFIED_* based on a freeform user JSON flag. The trust root must be provided through separately authorized operator custody. Public test fixtures must use only synthetic nonprivileged test keys and dummy identifiers.

## Original NELFP-v0 false acceptance
The static validator currently compares two input numbers:
claimed_authenticated_quorum=3, operator_registered_distinct_actors=3.
If attacker/agent controls both numbers, NELFP may emit ACCEPTED_ONLY_WITHIN_DECLARED_C1_SCOPE. The correct gate for claims of authenticated quorum must require an independent trusted identity proof; missing proof -> AUTHENTICATED_QUORUM_NOT_ESTABLISHED/HOLD. Existing NELFP 15/15 only validated a subset of static contracts and is preserved as a past observation, not rewritten to FAIL_ALL.

## Required negative/positive
Wrong key, wrong role, wrong payloadType, altered payload, duplicate signer, untrusted root, stale/expired/revoked and nonce replay -> negative. Correct TEST signature with trusted test root, valid role, valid fresh nonce -> positive. Scientific validity remains separate. Do not create or publish actual production credential, real exploit or unpatched endpoint.
