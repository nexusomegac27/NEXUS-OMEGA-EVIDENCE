# AXIOM Alpha-Node · Pinned Fixture Hydration / Replay Closure R0

OBJECT = NEXUS_OMEGA_ALPHA_PINNED_FIXTURE_HYDRATION_REPLAY_20261021_R0
PREDECESSOR = NEXUS_OMEGA_ALPHA_REPLAY_DEPENDENCY_CLOSURE_20261021_R0
PREDECESSOR_RECEIPT_SHA256 = 1bdc76150676e024f90589afb4e95f766475b850c6978263ff68d6854275e613
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = TESTED_IMPROVEMENT_ISOLATED_C1_NOT_PRODUCTION

## One falsifiable repair

The predecessor's frozen evaluator (SHA256 83335d1ca885027d1650db73b613af9d73709a25358048ead97e68b1f134cb2e) cannot start from its delivered export: `branch_original.md` is absent. A new create-only hydration guard requires immutable repository/commit/path, exactly 2070 source bytes, SHA256 and Git blob, and rejects pre-existing destinations. No historical artifact was overwritten.

Source: `nexusomegac27/NEXUS-OMEGA-EVIDENCE` commit `8f37f1c5e2e7d3505fb1660920d9dff24367c95e`, path `research/r16/axiom-alpha-node-c1-adaptation-20261012/ALPHA_PUBLICATION_PROOF_AND_DENOMINATOR_GUARD_20261021_R0.md`; 2070 bytes; SHA256 `5e626c47ce63042c5156aacfe345784a78e719acd0a4f05cf4abe1ae736e21c7`; Git blob `edc5248e954472379bd63e06ae401857d10baa43`. Original bytes were retrieved through the authorized GitHub connector and checked independently in an isolated replay workspace; connector transport is not independently attested.

## Before / after on identical original evaluator

Before: 0/1 replay startups (FileNotFoundError before any case). After create-only hydration in a fresh workspace: 1/1 startup; unchanged original frozen evaluator and unchanged predecessor candidate: 24/24 PASS, exit 0. A separate pre-candidate frozen hydration evaluator (SHA256 `6ee3dd30982952a1186a00006c9566cdb23eac11150610c244a292755b1fe620`) passed 11/11 adversarial cases. An intentional mutant ignoring repository identity passed 10/11; wrong-repository negative fixture failed as expected.

Falsifier: missing/changed bytes, mismatched repository/commit/path or existing target is accepted; or the untouched predecessor evaluator cannot reproduce 24/24 after valid hydration. This result restores **local replayability**, not independent scientific validation, GitHub main publication, productive integration or WWW parity. Original evaluator and previous receipts are unchanged. Project-wide eligible Handoff denominator UNKNOWN; 90% target NOT_ESTABLISHED.
