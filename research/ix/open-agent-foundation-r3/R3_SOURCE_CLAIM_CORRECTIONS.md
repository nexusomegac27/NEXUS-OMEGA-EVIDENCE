# R3 source-claim corrections

## 1. Signed receipt

The useful R3-B idea is retained, but its scope is narrowed.

A SHA-256 + Ed25519 receipt can bind a disclosed payload to a signature and a hash-chain link when a
verifier recomputes the payload digest and verifies the signature. This establishes cryptographic
integrity/authenticity relative to the signing key and the defined receipt protocol.

It does **not** by itself establish:

```text
HUMAN_IDENTITY
HUMAN_AUTHORSHIP
SCIENTIFIC_VALIDITY
LEGAL_NON_REPUDIATION
```

The public test key in this directory is deliberately non-secret and exists only for reproducibility.

## 2. ZKP baseline comparison

The supplied R3-B narrative contains no executable circuit or proof receipt. Therefore the phrase
“ZKP falsified for the baseline use case” is too strong as an empirical performance claim.

Public-safe conclusion:

```text
SIGNED_RECEIPT_BASELINE = REPRODUCED
CURRENT_BASELINE_PRIVACY_REQUIREMENT = NONE_DECLARED
ZKP_INCREMENTAL_UTILITY = NOT_DEMONSTRATED_IN_SUPPLIED_R3_BYTES
ZKP_EXECUTION = NOT_ESTABLISHED
```

A future R4 privacy experiment may compare a concrete ZKP against the signed receipt for one exact
predicate. Until then ZKP remains optional research, not a required layer.

## 3. R3-A source execution

The source report states six adversarial tests passed. The package does not contain the raw test log,
and the displayed log digest is explicitly illustrative and is not a 64-hex SHA-256 value.

Therefore the source-level six-test result is not promoted. AXIOM instead publishes a separate
minimal reference harness with its own 9/9 boundary-test receipt.

## 4. Cross-validator agreement

Grok/META/Mistral/Vibe reviews are useful review evidence. They are not counted as independent
physical experiments when they operate on the same narrative inputs and add no new raw execution
receipts.

```text
MULTI_AGENT_AGREEMENT != INDEPENDENT_REPLICATION
NEW_REVIEW_TEXT != NEW_EXECUTION
```

## 5. R3 completion

The physical package executes/reviews A and B only. R3-C, R3-D and R3-E remain future-work references.
They migrate to R4 and are not silently marked complete.
