/-
  NEXUS OMEGA — R31 | Qwen independent fourth reading — machine-checked core.

  E99 RNBS GREEN predicate, formalized faithfully to the quotation in the
  authenticated PR #365 intake comment 6943848606 (body UTF-8 SHA-256
  d9d1009bec6f5e4b47bf9c7664e6fb035c64c61d4314c822c6270deb648d1c53):

    "GREEN(h,B,N) iff current>=N AND for every prior period in N and
     every r in authorized B: h is in Ack-set A_r(p) and not in
     Revoke-set W_r(p)."

  Scope and epistemic limits (C1):
  * Finite decidable model, core Lean 4 only (no mathlib).
  * This formalizes the SPECIFICATION AS QUOTED. E99 original bytes are
    not in this witness's custody; quotation fidelity = UNKNOWN.
  * `delivered` / `honest` are ground-truth MODEL FIELDS. No theorem inside
    this model can bridge the model-reality gap (T4 auto-ack; compromised
    endpoints are observationally indistinguishable). Formal correctness
    and empirical adequacy are separate closure mechanisms.
-/

inductive Rec where
  | e1 | e2
  deriving DecidableEq, Repr

/-- A finite world: ack/revoke ledger bits per recipient and period,
    plus ground-truth delivery and honesty flags. -/
structure World where
  ack : Rec → Nat → Bool
  rev : Rec → Nat → Bool
  delivered : Rec → Bool
  honest : Rec → Bool

/-- GREEN(h,B,N) at `current`; prior N periods are [current-N, current). -/
def green (w : World) (B : List Rec) (N current : Nat) : Bool :=
  (current >= N) &&
  ((List.range N).all fun i =>
    B.all fun r => w.ack r (current - N + i) && !(w.rev r (current - N + i)))

/-- Proposed minimal guard: GREEN plus nonempty authorized set. -/
def greenGuarded (w : World) (B : List Rec) (N current : Nat) : Bool :=
  green w B N current && !B.isEmpty

/-- Ground truth: every authorized target really received the content. -/
def allDelivered (w : World) (B : List Rec) : Bool := B.all w.delivered

/-- Subset relation on recipient lists (own definition, core-only). -/
def RecSub (l₁ l₂ : List Rec) : Prop := ∀ r, r ∈ l₁ → r ∈ l₂

/-! ### Worlds for the counterexamples and controls -/

/-- CX1: E1 honest and really delivered; E2 compromised, never delivered,
    forged-but-valid-looking acks in every period. -/
def wCX1 : World where
  ack := fun _ _ => true
  rev := fun _ _ => false
  delivered := fun r => match r with | .e1 => true | .e2 => false
  honest := fun r => match r with | .e1 => true | .e2 => false

/-- CX2: empty authorized set; nothing delivered. -/
def wCX2 : World where
  ack := fun _ _ => false
  rev := fun _ _ => false
  delivered := fun _ => false
  honest := fun _ => true

/-- CX4 (new, Qwen): all honest; E1 delivered+acks, E2 intended target,
    never delivered, never acks; authorized set narrowed to B = {E1}. -/
def wCX4 : World where
  ack := fun r _ => match r with | .e1 => true | .e2 => false
  rev := fun _ _ => false
  delivered := fun r => match r with | .e1 => true | .e2 => false
  honest := fun _ => true

def wCtrl1 : World where
  ack := fun _ _ => true
  rev := fun _ _ => false
  delivered := fun _ => true
  honest := fun _ => true

def wCtrl2 : World where
  ack := fun r _ => match r with | .e1 => true | .e2 => false
  rev := fun _ _ => false
  delivered := fun r => match r with | .e1 => true | .e2 => false
  honest := fun _ => true

def wCtrl3 : World where
  ack := fun _ _ => true
  rev := fun r p => match r, p with | .e1, 1 => true | _, _ => false
  delivered := fun _ => true
  honest := fun _ => true

/-! ### General lemmas (universal, not just instances) -/

/-- Pointwise characterization of GREEN. -/
theorem green_iff (w : World) (B : List Rec) (N c : Nat) :
    green w B N c = true ↔
      (c >= N) = true ∧
      ∀ i ∈ List.range N, ∀ r ∈ B,
        w.ack r (c - N + i) = true ∧ w.rev r (c - N + i) = false := by
  simp [green, List.all_eq_true]

/-- Vacuity: with B empty, GREEN reduces to the history check alone (CX2 class). -/
theorem green_empty (w : World) (N c : Nat) : green w [] N c = (c >= N) := by
  simp [green, List.all_eq_true]

/-- NEW edge case surfaced by formalization (Q-CX5): N = 0 makes GREEN
    vacuously true for ANY B and ANY world. Requires N >= 1 precondition. -/
theorem green_N_zero (w : World) (B : List Rec) (c : Nat) : green w B 0 c = true := by
  simp [green]

/-- Anti-monotonicity in the authorized set (Q-CX4 class): shrinking B can
    only help GREEN. CX2 is the limit case B' = []. -/
theorem green_antitone (w : World) (B B' : List Rec) (N c : Nat)
    (hsub : RecSub B' B) (hg : green w B N c = true) : green w B' N c = true := by
  rw [green_iff] at hg ⊢
  exact ⟨hg.1, fun i hi r hr => hg.2 i hi r (hsub r hr)⟩

/-- Constructive salvage: under N >= 1 and ack-soundness for one honest
    authorized recipient, GREEN certifies EXISTENCE of a real receipt
    (publication-existence), never delivered-to-all. -/
theorem existential_salvage (w : World) (B : List Rec) (N c : Nat)
    (hN : 0 < N) (r : Rec) (hrB : r ∈ B) (hrH : w.honest r = true)
    (hsound : w.honest r = true → ∀ p, w.ack r p = true → w.delivered r = true)
    (hg : green w B N c = true) : w.delivered r = true := by
  have hg' := (green_iff w B N c).mp hg
  have h0 : 0 ∈ List.range N := List.mem_range.mpr hN
  exact hsound hrH _ (hg'.2 0 h0 r hrB).1

/-! ### Machine-checked counterexample instances -/

/-- CX1 replicated: GREEN true, an honest authorized recipient exists,
    yet universal real delivery is FALSE. ">=1 honest suffices for
    delivered-to-all" is refuted in the exact quoted predicate. -/
theorem cx1_counterexample :
    green wCX1 [.e1, .e2] 3 3 = true
    ∧ ([.e1, .e2] : List Rec).any wCX1.honest = true
    ∧ allDelivered wCX1 [.e1, .e2] = false := by decide

theorem cx2_vacuous_green : green wCX2 [] 3 3 = true := by decide

theorem cx2_no_honest_receipt :
    ([.e1, .e2] : List Rec).any (fun r => wCX2.delivered r && wCX2.honest r) = false := by decide

theorem cx2_guard_repairs : greenGuarded wCX2 [] 3 3 = false := by decide

/-- Q-CX4 (new): even with ALL recipients honest, narrowing B forces GREEN
    while an intended target was never delivered. -/
theorem cx4_B_narrowing :
    green wCX4 [.e1] 3 3 = true
    ∧ ([.e1, .e2] : List Rec).all wCX4.honest = true
    ∧ allDelivered wCX4 [.e1, .e2] = false := by decide

theorem cx4_guard_insufficient : greenGuarded wCX4 [.e1] 3 3 = true := by decide

theorem cx1_guard_insufficient : greenGuarded wCX1 [.e1, .e2] 3 3 = true := by decide

/-- Q-CX5 (new): N = 0 vacuity instance. -/
theorem cx5_N_zero_vacuity : green wCX2 [.e1, .e2] 0 0 = true := by decide

/-! ### Controls -/

theorem ctrl1_all_honest_delivered :
    green wCtrl1 [.e1, .e2] 3 3 = true ∧ allDelivered wCtrl1 [.e1, .e2] = true := by decide

theorem ctrl2_channel_loss_not_green : green wCtrl2 [.e1, .e2] 3 3 = false := by decide

theorem ctrl3_revoke_blocks : green wCtrl3 [.e1, .e2] 3 3 = false := by decide

theorem ctrl4_short_history_blocks : green wCtrl1 [.e1, .e2] 3 2 = false := by decide

/-! ### Axiom hygiene: no sorryAx allowed -/

#print axioms green_iff
#print axioms green_empty
#print axioms green_N_zero
#print axioms green_antitone
#print axioms existential_salvage
#print axioms cx1_counterexample
#print axioms cx4_B_narrowing
