# G11 — PART C: AUTHORITY CAPSULE V2 THREAT MODEL (Lane 1, external non-lineage reviewer)

CLAIM_CEILING: C1_DESCRIPTIVE_ONLY · LAST_VERIFIED 2026-10-05 · Sources = `G01_part_lane1.csv` (L1-xxx).
STATUS: design review only. NEXUS states `cryptographic_authority = NOT_ESTABLISHED` [L1-053]. Nothing in this file implements, tests or certifies a capsule.
Reviewer stance: **Capsule V2 is, at present, a profile of existing capability-token prior art.** Where it is not, the gap is semantic (epistemic claim ceilings), not cryptographic.

## 1. NAC levels — semantics and what each level does NOT prove

| Level | Name | Proves (if verified) | Does NOT prove | Closest prior art |
|---|---|---|---|---|
| NAC-0 | UNBOUND | nothing beyond the bytes present | integrity, origin, order, authority | WAL-0 / WAL-1 without crypto [L1-003]; SLSA Build L0/L1 (L1 provenance "trivial to bypass or forge") [L1-011] |
| NAC-1 | HASH_LINKED | byte integrity of each capsule *relative to a trusted head*; parent-pointer continuity | who produced it (anyone can recompute hashes); authority; that the head is genuine; absence of forks | Merkle/hash chains (RFC 9162 tree structure [L1-043]); WAL-3 hash-chained log component [L1-003] |
| NAC-2 | SIGNED | possession of the private key bound to KEY_ID at signing time, over exact canonical bytes, in a given domain | that KEY_ID belongs to ISSUER (needs a trust anchor); that ISSUER may grant SCOPE (needs policy); non-revocation; timeliness of signing; uniqueness of use | JWS/COSE [L1-040, L1-039]; Ed25519 [L1-037]; Biscuit blocks [L1-048]; UCAN [L1-049] |
| NAC-3 | TRANSPARENCY_ATTESTED | that a specific signed statement was registered in a specific Transparency Service's VDS under its registration policy (receipt) | truth (RFC 9943 §9.2); issuance order (§9.1); completeness (§9.3, selective registration); authorization (out of scope); revocation (out of scope) | SCITT RFC 9943 + COSE Receipts RFC 9942 [L1-001, L1-002] |

The levels are **not** a total order of "trust". NAC-3 does not imply NAC-2 authorization; it implies only NAC-2 *signature* plus registration. **No NAC level implies SCIENTIFIC_VALIDITY.**

## 2. Required NAC-2 fields — review

| Field | Purpose | Prior-art anchor | Reviewer note |
|---|---|---|---|
| ALG = Ed25519 (or justified alternative) | signature primitive | RFC 8032 [L1-037]; Biscuit default Ed25519, alt secp256r1 [L1-048]; WCA WAL-2 Ed25519/P-256 [L1-003] | Pin the algorithm in the *protected* bytes. Reject `none`/unknown algorithms (RFC 8725 §2.1 weak/insufficient signature validation, §3.1 perform algorithm verification [L1-036]). |
| KEY_ID | key lookup | JWS `kid` [L1-040]; A2A kid/jku [L1-006] | KEY_ID is a *hint* and is untrusted until resolved in a pinned trust store (RFC 8725 §3.10 do not trust received claims [L1-036]). Fetching keys from a URL in the token (jku-style) is an attack surface. |
| ISSUER | who claims to grant | JWT/CWT `iss` [L1-035, L1-045] | Must be bound to KEY_ID by a trust-anchor record (RFC 8725 §3.8 validate issuer). |
| AUDIENCE | intended verifier | `aud` RFC 7519; RFC 8707 resource indicators [L1-041]; MCP audience validation [L1-008] | Exact-match only. A verifier MUST reject any capsule that does not name it (RFC 8725 §3.9). |
| SCOPE | granted authority | Biscuit Datalog checks; UCAN policy; ERC-8370 clauses [L1-048, L1-050, L1-029] | Needs formal subset semantics, otherwise ⊆ cannot be decided. This is the hardest unresolved field. |
| ISSUED_AT / NOT_BEFORE / EXPIRES_AT | time window | `iat`/`nbf`/`exp` RFC 7519 | Define clock source and allowed skew. ISSUED_AT is a *claim*, not proof (only a NAC-3 receipt or RFC 3161-style timestamp gives an external time witness; RFC 3161 not re-audited). |
| NONCE_OR_REPLAY_BIND | one-time use / binding | `jti`/`cti`; DPoP jti cache [L1-046]; WCA signed nonce queries [L1-003] | A nonce only works with a verifier-side seen-set within the validity window. |
| PARENT_CAPSULE_HASH | delegation link | Biscuit binds previous signature via `\0PREVSIG\0` [L1-048]; RFC 8693 nested `act` [L1-034] | Must cover the parent's *full signed bytes incl. signature*, not only its payload. |
| CANONICAL_SERIALIZATION | byte determinism | RFC 8785 JCS [L1-038] (A2A mandates it [L1-006]); deterministic CBOR in COSE [L1-039] | Pick one. Dual JSON/CBOR encodings create signature-confusion risk (cf. RFC 8725 §2.6 multiplicity of JSON encodings [L1-036]). |
| DOMAIN_SEPARATION | prevent cross-protocol reuse | Biscuit `\0BLOCK\0` strings [L1-048]; RFC 8725 §3.11 explicit typing [L1-036] | Include a context string + capsule type + version in the signed bytes. |
| *(Reviewer-added)* TRUST_ANCHOR_ID | which root policy applies | RFC 4949 trust anchor [L1-044]; SCITT trust anchors [L1-001]; Biscuit root key [L1-048] | Required to turn a signature into authority. Without it, Capsule V2 can never reach AUTHORIZED. |
| *(Reviewer-added)* REVOCATION_REF / status pointer | revocation check | Biscuit revocation ids [L1-048]; UCAN revocation sub-spec [L1-049] | SCITT puts revocation out of scope, so NEXUS must supply it. |
| *(Reviewer-added)* CLAIM_CEILING / ROOT_PROPERTY | what the parent actually proved | — (NEXUS-specific) | Enforces "child must not claim a stronger root property than proven". |

## 3. SIGNATURE_VALID ≠ AUTHORIZED

```
AUTHORIZED(c, verifier, t) :=
    SIG_VALID(c.bytes, key(c.KEY_ID))
  ∧ KEY_BOUND(c.KEY_ID, c.ISSUER, TRUST_ANCHOR, t)      -- trust root
  ∧ ¬REVOKED(c.KEY_ID, t) ∧ ¬REVOKED(c, t)               -- revocation
  ∧ c.AUDIENCE = verifier                                  -- audience
  ∧ c.NOT_BEFORE ≤ t < c.EXPIRES_AT                        -- time
  ∧ FRESH(c.NONCE)                                         -- replay
  ∧ POLICY(TRUST_ANCHOR) permits (c.ISSUER grants c.SCOPE) -- policy
  ∧ (c is root ∨ (AUTHORIZED(parent(c), c.ISSUER, t) ∧ ATTENUATES(c, parent(c))))  -- delegation
```
Any conjunct that is UNKNOWN makes the result UNKNOWN, and UNKNOWN maps to **deny** (non-compensatory, cf. L1-016 as a formal proposal). Prior art states the same separation: RFC 9943 leaves authN/authZ out of scope [L1-001]; A2A makes authorization implementation-specific and requires per-request checks [L1-006]; SPIFFE provides identity, not authorization [L1-051].

## 4. Delegation attenuation

```
ATTENUATES(child, parent) :=
    child.SCOPE ⊆ parent.SCOPE
  ∧ child.EXPIRES_AT ≤ parent.EXPIRES_AT
  ∧ child.NOT_BEFORE ≥ parent.NOT_BEFORE
  ∧ child.AUDIENCE-chain consistent (child.ISSUER = parent.AUDIENCE)
  ∧ child.CLAIM_CEILING ≤ parent.PROVEN_ROOT_PROPERTY
  ∧ child.PARENT_CAPSULE_HASH = H(parent.signed_bytes)
  ∧ depth(child) ≤ MAX_DEPTH
```
Prior-art comparison:
- Macaroons: caveats can only add restrictions, through chained HMAC. Verification needs the root secret (symmetric key) and the tokens are bearer [L1-047].
- Biscuit: append-only signed blocks; later blocks cannot add rights (scope rules); offline, public-key verifiable [L1-048].
- UCAN: the chain is valid only between the latest `nbf` and the earliest `exp`. UCAN therefore **intersects** time windows instead of rejecting child-exp > parent-exp [L1-050]. *Design choice for NEXUS:* reject (stricter; it surfaces escalation attempts) or intersect (more robust). Recommended default: **reject**, because it yields a detectable FAIL rather than a silent clamp.
- ERC-8370 (unmerged): clause-wise child ⊆ parent plus a depth counter ("telomere") [L1-029].
- RFC 8693: nested `act` records the chain, but `exp`/`nbf`/`aud` inside `act` carry no meaning, so it **records** delegation and does not **attenuate** it [L1-034].

## 5. Attack gates (sec. 35 gate format)

Common preconditions: canonical bytes are recomputed by the verifier, never taken from the capsule. The verifier holds a pinned TRUST_ANCHOR set.

### G-C01 SCOPE_ESCALATION
- INPUT: child capsule, verified parent capsule, scope grammar.
- PREDICATE: `child.SCOPE ⊆ parent.SCOPE` is decidable under the grammar and holds.
- PASS: subset proven. FAIL: any element of child.SCOPE outside parent.SCOPE. UNKNOWN: the grammar cannot decide (wildcards, free text, or a null subject, cf. UCAN "powerline" [L1-050]).
- RECOVERY: reject. Re-issue from the parent with an explicit, enumerable scope.
- FALSE_POSITIVE_RISK: semantically equivalent but syntactically different scopes get rejected (normalize first).
- FALSE_NEGATIVE_RISK: the grammar is too coarse, e.g. a "read:*" parent admits unintended reads. The risk is highest with free-text scopes.

### G-C02 EXPIRY_ESCALATION
- INPUT: child/parent EXPIRES_AT, NOT_BEFORE; verifier clock t; skew bound.
- PREDICATE: `child.EXPIRES_AT ≤ parent.EXPIRES_AT ∧ child.NOT_BEFORE ≥ parent.NOT_BEFORE ∧ NOT_BEFORE ≤ t < EXPIRES_AT`.
- PASS: all hold. FAIL: any violated. UNKNOWN: no trusted clock, or a missing field.
- RECOVERY: reject. Do not clamp silently (contrast UCAN's intersection [L1-050]).
- FALSE_POSITIVE_RISK: clock skew. FALSE_NEGATIVE_RISK: the issuer back-dates ISSUED_AT, since time claims are self-asserted without a NAC-3 receipt or external timestamp.

### G-C03 AUDIENCE_SWAP
- INPUT: capsule.AUDIENCE, verifier identity.
- PREDICATE: exact match (RFC 8725 §3.9 [L1-036]; RFC 8707 [L1-041]; MCP audience validation and no token passthrough [L1-008]).
- PASS: match. FAIL: mismatch. UNKNOWN: AUDIENCE absent or wildcard.
- RECOVERY: reject. Require the issuer to mint per-audience capsules.
- FALSE_POSITIVE_RISK: identifier aliasing (multiple names for one verifier). FALSE_NEGATIVE_RISK: a shared audience across services (confused deputy, MCP security best practices [L1-010]).

### G-C04 PARENT_SWAP
- INPUT: child.PARENT_CAPSULE_HASH, candidate parent bytes.
- PREDICATE: `child.PARENT_CAPSULE_HASH = H(parent.full_signed_bytes)` *and* the hash is inside the child's signed bytes.
- PASS: match. FAIL: mismatch. UNKNOWN: parent not retrievable.
- RECOVERY: reject. Fetch the parent from a content-addressed store or the SCITT log.
- FALSE_POSITIVE_RISK: re-serialization of the parent changes its bytes (canonicalization bug). FALSE_NEGATIVE_RISK: the hash covers only the payload, not the signature, which allows signature-malleability splicing. Biscuit binds the previous *signature* to avoid this [L1-048].

### G-C05 KEY_SWAP
- INPUT: KEY_ID, ISSUER, trust store at time t.
- PREDICATE: `KEY_BOUND(KEY_ID, ISSUER, TRUST_ANCHOR, t)` via a pinned store (never jku/URL from the capsule itself).
- PASS: bound. FAIL: the key is bound to a different issuer or not bound. UNKNOWN: store unavailable.
- RECOVERY: reject. Manage keys out of band.
- FALSE_POSITIVE_RISK: legitimate key rotation not yet propagated. FALSE_NEGATIVE_RISK: the attacker controls the trust store or the key-discovery channel. SCITT leaves key discovery out of scope [L1-001].

### G-C06 REPLAY
- INPUT: NONCE_OR_REPLAY_BIND, verifier seen-set, validity window.
- PREDICATE: nonce unseen within [NOT_BEFORE, EXPIRES_AT] for this AUDIENCE; nonce inside signed bytes.
- PASS: fresh. FAIL: seen. UNKNOWN: seen-set lost (restart, multi-node without shared state).
- RECOVERY: reject. Keep validity windows short. DPoP-style jti caching [L1-046].
- FALSE_POSITIVE_RISK: a legitimate retry after a network failure. FALSE_NEGATIVE_RISK: distributed verifiers with unsynchronized seen-sets.

### G-C07 REORDERING
- INPUT: an ordered sequence of capsules or log entries.
- PREDICATE: the order is derived from the PARENT_CAPSULE_HASH chain (causal order), **not** from log position or ISSUED_AT.
- PASS: the chain order is consistent. FAIL: the claimed order contradicts the hash links. UNKNOWN: siblings with no causal relation.
- RECOVERY: treat siblings as concurrent. Do not infer precedence.
- FALSE_POSITIVE_RISK: none material. FALSE_NEGATIVE_RISK: relying on SCITT log order. RFC 9943 §9.1 says VDS order need not match issuance order [L1-001].

### G-C08 CYCLE
- INPUT: delegation graph reconstructed from parent hashes.
- PREDICATE: the graph is acyclic and depth ≤ MAX_DEPTH. A hash cycle is cryptographically infeasible, but an *issuer/authority* cycle (A→B→A re-delegation) is possible.
- PASS: acyclic in both the hash and issuer graphs. FAIL: a cycle. UNKNOWN: graph incomplete.
- RECOVERY: reject. Cap the depth (cf. ERC-8370 telomere [L1-029]).
- FALSE_POSITIVE_RISK: legitimate round-trip delegation patterns. FALSE_NEGATIVE_RISK: cycles split across trust domains.

### G-C09 ORPHAN
- INPUT: non-root capsule whose parent cannot be resolved.
- PREDICATE: the parent is resolvable and AUTHORIZED.
- PASS: resolved. FAIL: the parent is proven absent or invalid. UNKNOWN: the parent store is unreachable.
- RECOVERY: deny (UNKNOWN → deny). Allow retry after the store recovers.
- FALSE_POSITIVE_RISK: availability outages cause denials. FALSE_NEGATIVE_RISK: a verifier treating "no parent field" as "root". The root status must be explicit and anchored to the TRUST_ANCHOR.

### G-C10 REVOKED_KEY
- INPUT: KEY_ID, capsule id, revocation source, t.
- PREDICATE: neither the key nor any capsule in the chain is revoked at t (Biscuit revocation ids [L1-048]; A2A "expired/revoked keys MUST NOT be used" [L1-006]).
- PASS: no revocation found from a fresh source. FAIL: revoked. UNKNOWN: revocation source stale or unreachable.
- RECOVERY: deny on UNKNOWN for high-impact scopes.
- FALSE_POSITIVE_RISK: stale caches. FALSE_NEGATIVE_RISK: no revocation mechanism defined at all. **This is the current gap:** SCITT puts revocation out of scope [L1-001], and UCAN admits no confinement [L1-049].

### G-C11 UNKNOWN_TRUST_ROOT
- INPUT: chain root issuer/key; pinned TRUST_ANCHOR set.
- PREDICATE: the root key is in the pinned set and the anchor's policy permits the root scope.
- PASS: pinned and permitted. FAIL: not pinned. UNKNOWN: the anchor set itself is unverifiable.
- RECOVERY: deny. Add trust anchors only through an operator-governed process.
- FALSE_POSITIVE_RISK: a new legitimate root not yet onboarded. FALSE_NEGATIVE_RISK: TOFU (trust on first use) or accepting any self-signed root. This is the most likely real-world failure.

## 6. Easiest attack (reviewer ranking)
1. **G-C11 / G-C05: signature valid, authority unproven.** A capsule self-signed with a fresh Ed25519 key passes NAC-2 *signature* verification if the verifier does not pin trust anchors. NEXUS today states `cryptographic_authority NOT_ESTABLISHED` [L1-053], so no anchor is defined and this attack succeeds by default.
2. **G-C03 audience confusion / substitution** (RFC 8725 §2.7–2.8 [L1-036]) if AUDIENCE is optional or wildcarded.
3. **G-C10 revocation absent.**
4. **G-C01 scope escalation via an undecidable scope grammar.**

## 7. Reduction verdict (prior-art overlap)
- Attenuation plus offline public-key verification plus parent-signature binding plus revocation ids are **already provided by Biscuit** [L1-048]. Delegation chains with time windows are provided by **UCAN** [L1-049/050]. The actor chain is in **RFC 8693** [L1-034]. Transparency is in **SCITT** [L1-001]. Audience binding is in **RFC 8707** and MCP [L1-041, L1-008].
- What remains NEXUS-specific (unproven): CLAIM_CEILING / ROOT_PROPERTY monotonicity, meaning a child cannot claim stronger *epistemic* status than its parent proved, and binding capsules to referent / causal-position (the R7 triad). These are semantic, not cryptographic.
- RECOMMENDATION (C1): `REDUCE_C1_PART_C_TO_PROFILE(Biscuit-or-COSE capsule + SCITT registration + NEXUS claim-ceiling caveat)`. Do not invent a new token format.
- FALSIFIER of this recommendation: a concrete NEXUS requirement that none of Biscuit, UCAN, RFC 8693 or COSE+SCITT can express. None was identified in the available materials.
