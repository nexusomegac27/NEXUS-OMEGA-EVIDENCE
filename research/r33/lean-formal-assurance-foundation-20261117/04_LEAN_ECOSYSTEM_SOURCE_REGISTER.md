# R33 Lean 4 — First-party and independently inspectable ecosystem source register

OBJECT = NEXUS_OMEGA_AXIOM_R33_LEAN_ECOSYSTEM_PRIMARY_SOURCE_REGISTER_20261117_R0
DATE = 2026-11-17
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
STATE = SOURCE_RESEARCH_DESIGN_ONLY
BUILD_IN_THIS_AXIOM_RUNTIME = NOT_RUN
NO_AUTOMATIC_FRAMEWORK_INSTALL = YES

## Mandatory / narrowly justified

L01 Lean official language reference:
https://lean-lang.org/doc/reference/latest/
Source role: dependent type theory, kernel proof checking and syntax. Distinguish parser/elaborator/kernel; a successful proof term is only evidence of the correctly stated theorem.

L02 Lean 4 elaboration/kernel and built-in second environment checker:
https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/
Source role: trusted kernel independently checks elaborated proofs; built-in leanchecker can replay a compiled module environment. This still uses the same Lean kernel and is NOT independent world-observation or independent theorem formalization.

L03 Lean standard axioms and #print axioms:
https://lean-lang.org/doc/reference/latest/Axioms
Source role: propext, Quot.sound, Classical.choice are standard logical axioms. The sorryAx axiom is NOT acceptable for finished formal assurances. Native execution proofs can introduce trust in the compiler; audit allowed axiom list per theorem rather than merely searching raw source for the token sorry.

L04 Lean 4 exact v4.36.0 release / toolchain reference:
https://github.com/leanprover/lean4/releases
https://reservoir.lean-lang.org/
This version exists as stable as of 2026-11-17 according to the package registry. Qwen claims a run with this exact version; AXIOM has not independently rerun the Lean binary. Freeze lean-toolchain to leanprover/lean4:v4.36.0 and verify actual installed binary hash/platform from official distribution.

L05 elan (Lean toolchain manager):
https://github.com/leanprover/elan
Source role: version-controlled toolchain acquisition; do not execute curl|sh unreviewed in privileged production, pin and validate checksums in a disposable sandbox.

L06 Lake package/build tool:
https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/
Source role: dependency and reproducible Lean build orchestration. The minimal existing Qwen original uses core Lean, no imported mathlib required.

L07 Current built-in leanchecker, not the old standalone lean4checker:
https://github.com/leanprover/lean4checker
README states separate old repo deprecated/archived 2026; use built-in leanchecker distributed since Lean v4.28.0. Command pattern: lake env leanchecker [module] or lake env leanchecker --fresh [module]. It reuses Lean's kernel, so don't call it an independently authored external proof checker.

L08 Lean CI official action and axiom audit:
https://github.com/leanprover/lean-action
Source role: optional build, leanchecker, axiom-audit workflow. Check current action version, pin exact commit SHA before use, allow only audited actions, no credentials persisted and no production secrets. This research package includes a BLUEPRINT only; no CI action installed into active .github/workflows.

## Optional as needed, not baseline requirement

L09 mathlib4:
https://github.com/leanprover-community/mathlib4
Used for richer mathematics, analysis, algebra and potentially mathematical sensor/filter proofs. Is a large additional dependency with pinned commit, cache, license and offline-mirror implications. Not needed for the seven-kilobyte Qwen core source; do not install by default.

L10 LeanDojo:
https://github.com/lean-dojo/LeanDojo
The original project states DEPRECATED; check LeanDojo-v2 before any future research workflow. Proof-search agents can propose but cannot replace kernel check. No remote AI token or arbitrary plugin execution in a private evidential lane.

L11 Countermodel / independent formal approaches:
https://github.com/tlaplus/tlaplus
https://alloytools.org/
https://quint.sh/
https://hypothesis.readthedocs.io/en/latest/stateful.html
Each method has a different assurance profile. A model checker might find transition counterexamples and Lean might prove guarded safety properties; neither implies real-world HTTP trace correspondences without independent tests.

L12 Yang-Mills independent research group, purely methodological precedent:
https://github.com/yang-mills-group/YM
https://github.com/yang-mills-group/YM/blob/main/README.md
As of 2026-11-17 the group assessed a 2026-10-28 OpenAI pure Yang-Mills submission as constructing an existence-scoped 4D QFT; explicitly NOT a proof of mass gap or uniqueness of infinite-volume limit. Reproducibility package separates original submission, check scripts, source/commit pins, independent assessment and unsupported claims. NEXUS can adapt this structure without claiming any direct Yang-Mills result or external endorsement.
Qwen source report documented KITP PDF fetch anomaly: two supposed PDFs returned identical HTML despite HTTP 200; classify that specific byte fetch as NOT_PDF_CUSTODY_HOLD, not authentic PDF evidence. A valid alternate assessment PDF was separately in the archived evidence; do not copy long third-party research PDFs into R33 repo.

## Cross-cutting source controls

Source objects have URL, title, version/tag/commit, license, actually read sections, last read date, SHA of original when genuinely captured, dependency/OS requirements, alternative/offline fallback. A URL or product name is not a proof or a runtime receipt. If source has changed, preserve older captured state and mark NEW_VERSION_UNASSESSED until review.
No fabricated DOI, theorem proof, model execution, GitHub permissions, host resources or missing Windows R32 directory inventory.

TERMINAL = PRIMARY_SOURCE_REGISTER_COMPLETE_C1_RESEARCH_ONLY
