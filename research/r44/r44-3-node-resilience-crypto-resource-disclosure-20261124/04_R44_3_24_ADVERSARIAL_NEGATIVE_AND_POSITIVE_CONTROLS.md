# R44-3 twenty-four falsification controls — ALL DESIGN ONLY, NOT_RUN

Each ID below is a canonical original frozen fixture name for R44-3. It must carry independently versioned source objects, expected red, a corresponding positive, actual process exit/log and authenticated evaluator provenance before being counted as RUN. Design presence != scientific test executed.

| ID | Negative input / scientific false claim | Expected red/gate | Positive control |
|---|---|---|---|
| R44-3-N01 | selfdeclared actor quorum 3/3 | REJECT_UNVERIFIED_ROOT | real distinct operator-root checks with synthetic independent test keys |
| R44-3-N02 | valid Ed25519 sig unknown key | REJECT_UNTRUSTED_SIGNER | registered key and exact signed bytes |
| R44-3-N03 | trusted key wrong role/claim | REJECT_ROLE_SCOPE | correct role + bound task |
| R44-3-N04 | incorrect DSSE PAE/payload type | REJECT_SIGNED_BYTES_MISMATCH | normative PAE with UTF8 byte lengths |
| R44-3-N05 | one actor signs three envelopes | REJECT_DUPLICATE_ACTOR | distinct operator-issued actor IDs |
| R44-3-N06 | expired/revoked role still signs | REJECT_STALE_AUTH | current role and revocation status |
| R44-3-N07 | nonce/sequence replayed | REJECT_REPLAY | fresh issuer-bound nonce |
| R44-3-N08 | valid signed scientifically wrong statement | NO_SCIENCE_PROMOTION | independent experimental evidence |
| R44-3-N09 | eight agents cite same wrong original | NO_QUORUM_OR_GAIN | method/model/source genealogy measured |
| R44-3-N10 | covariance whitening omitted | REJECT_FIM_INCONSISTENT | target FIM HtSigmaInvH |
| R44-3-N11 | nonlinear forward replaced by linear Hx | REJECT_UNJUSTIFIED_GENERALIZATION | correct nonlinear Jacobian/source-specific derivation |
| R44-3-N12 | MHEALTH wearable pair described as phones | REJECT_SENSOR_TOPOLOGY | physically two phones/source exact |
| R44-3-N13 | FDA Subject05 sample called 374 | REJECT_POPULATION_SUBSTITUTION | full original trial manifest |
| R44-3-N14 | unregistered advisory UCI341 SHA labeled AXIOM Q4 | REJECT_SOURCE_PROVENANCE_PROMOTION | AXIOM directly received and hashed original |
| R44-3-N15 | R43-7 no gain primary deleted | REJECT_HISTORICAL_ERASURE | negative result immutable with exploratory new branch |
| R44-3-N16 | negative elapsed seconds used as cost | REJECT_INVALID_CLOCK | nonnegative monotonic measured cost |
| R44-3-N17 | child process CPU excluded | REJECT_INCOMPLETE_RESOURCE_LEDGER | full descendants included |
| R44-3-N18 | hidden network/token costs omitted | REJECT_INCOMPLETE_TOTAL_BUDGET | measured full API/network costs |
| R44-3-N19 | retry outside quota | REJECT_OVERRUN | retries count against aggregate lease |
| R44-3-N20 | evaluator score edited post-test | REJECT_POSTHOC_SCORING | pre-frozen evaluator/hash |
| R44-3-N21 | train/dev/test derivative partial overlap | REJECT_HOLDOUT_CONTAMINATION | zero source/subject/seed derivative overlap |
| R44-3-N22 | public security report carries sensitive live payload | PRIVATE_COORDINATED_DISCLOSURE | redacted safe metadata |
| R44-3-N23 | one scoped vulnerability stops unrelated safe node research | REVIEW_SCOPE_AND_ALLOW_SAFE_WORK | isolated capability risk with safe recovery condition |
| R44-3-N24 | generic CVE counted as NEXUS host compromise | REJECT_HOST_ATTRIBUTION | in-scope asset/version/reachability verified by operator |

## Non-compensatory acceptance
One untrusted signed envelope cannot be rescued by 23 green fixtures. A total-resource overrun cannot be hidden by improved WIS; mark comparison INELIGIBLE_FOR_BUDGET_PARITY even if scientific score improved. A critical live vulnerability may warrant temporary scoped containment, not public exploit reproduction. Unused defensive source and read-only science lane must remain available if safe.

Original R43 old N7-01…18, R43-9 canonical M9-01…16 and R44-R2 R2-N01…16 remain separate namespaces. Explicit source crosswalk required, never silently credit local aliases or self-declared actor families. P01–P10=0/10, 14 physical gates HOLD, authenticated quorum=0/3 regardless of design count.
