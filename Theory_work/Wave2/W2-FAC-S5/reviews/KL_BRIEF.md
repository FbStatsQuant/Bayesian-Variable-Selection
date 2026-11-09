# KL brief — global-centre control along a greedy elimination path (block compound symmetry)

Self-contained research problem (W2-FAC-S5, Tier 2). Goal: prove, or refute with a checked counterexample/obstruction,
Lemma KL below. Any rigorous partial result (a smaller exponent, a restricted regime) is valuable; state exactly what is
proved.

## 1. Probability model (fixed n-sequence; all asymptotics as n → ∞)

Constants: 0 < ρ_b < ρ_w < 1, b := ρ_w − ρ_b, d := 1 − ρ_w, group size bound q̄ (study S5: ρ_b = .3, ρ_w = .7,
q = 5). Index set [p] = disjoint union of groups G_1..G_G of sizes 1 ≤ q_g ≤ q̄; p = p_n → ∞ with
limsup log p/log n < 1/2 (p may be as large as n^{α}, α < 1/2; p ≥ n^{δ} is the interesting regime).
A fixed set S₀ of s₀ "truth" indices (s₀ fixed); all others are "nulls".
Noise: h := √ρ_b η, y_j := √b ζ_{g(j)} + √d ξ_j, g_j := h + y_j, with η, ζ_g, ξ_j iid N(0,1).
So g ~ N(0, Σ), Σ = ρ_b 11ᵀ + ⊕_g (b J + d I).

## 2. Exact identities (verified algebra; proofs in the ticket's lemma L1)

For T ⊆ [p] write U_g := T ∩ G_g, u_g := |U_g|, ω_g := u_g/(u_g b + d), ȳ_g := mean of y over U_g.
* **Global error.** e_T := h − E[h | g_T] satisfies the exact normal equation
  e_T (1/ρ_b + Σ_g ω_g) = h/ρ_b − Σ_g ω_g ȳ_g.     (so e_T ≈ −(ω-weighted mean of the retained group means ȳ_g)).
  Equivalently e_T = h − ρ_b Σ_{j∈T} r_j(T)/v_j with r_j(T) := g_j − E[g_j | g_{T∖j}], v_j := Var(g_j | g_{T∖j}).
* **Deletion/addition statistics.** For any j and R := T ∖ {j}, U := R ∩ G_{g(j)}, u := |U|:
  r_j(T) = a_j(U) + c_u e_R, a_j(U) := y_j − (1 − c_u) ȳ_U (ȳ_∅ := 0), c_u := d/(ub + d);
  a_j(U) ~ N(0, s_u²), s_u² := d(d + (u+1)b)/(d + ub), and a_j(U) is independent of (h, g_R).
  τ_j(T) := r_j(T)/√v_j with v_j = s_u² + c_u² V_R, V_R := 1/(1/ρ_b + Σ_g ω_g(R)).
  Write A_j(U) := a_j(U)/s_u ~ N(0,1). Then |τ_j(T)| ≤ |A_j(U)| + κ₀|e_R|, κ₀ := (1 − ρ_b)^{−1/2} (= max_u c_u/s_u).
* **Within a group** (h known) the statistics are exactly compound symmetric: all members' statistics are monotone in
  |y_j − x_g| with one group centre x_g = (1 − c_u)ȳ_U − c_u e (in y-coordinates; e = current global error).
* **Rotation identity** (any Gaussian quadratic form): Φ(T) := g_Tᵀ Σ_TT⁻¹ g_T, Φ(T) − Φ(T∖j) = τ_j(T)²; for l ∉ T,
  Φ(T∪l) − Φ(T) = τ_l(T)²; τ_l(T∖j)² = τ_l(T)² + τ_j(T)² − τ_j(T∪l)².

## 3. The greedy path and Lemma KL

Π: T_0 := [p] (or [p] minus a bounded set), T_{i+1} := T_i ∖ {j_i} where j_i ∈ T_i ∖ S₀ is a null with
τ_{j_i}(T_i)² ≤ min_{j ∈ T_i∖S₀} τ_j(T_i)² + δ_n (δ_n = O(log n / n), an exact-arithmetic perturbation coming from the
real score; you may first take δ_n = 0, i.e. exact argmin of |τ|), until T = S₀. (Π is "backward elimination on
Φ(T) = g_TᵀΣ_TT⁻¹g_T"; the truths are never deleted.) H := √(2 log p).

**Lemma KL (target).** For every fixed c > 0: P( for all i and all T′ ∈ {T_i} ∪ {T_i ∖ j : j ∈ T_i ∖ S₀}:
κ₀|e_{T′}| ≤ c H ) → 1.   (A version for some fixed c < 1/√(2α) − 1 already gives a theorem for exponent α.)

## 4. What is known / what fails (do not repeat these dead ends without a new idea)

* For q̄ = 1 (compound symmetry) KL is proved: Theorem FAC-CS, files Theory_work/Wave2/W2-FAC-B/lemmas/L4_path.md
  (key steps: exact gap invariant — the deleted nulls form an interval of the sorted ξ's around the centre, asymmetry
  recursion Δ_{i+1} ≤ max(Δ_i, g_i + 2d_i/(k−1+κ)); static centre bound (B3) by comparison with a symmetric top set
  Top(J) whose signed sum is a conditional Rademacher sum; end phase by majority-side deletion). Read it: it is the
  template. Events: W2-FAC-B/lemmas/L3_event.md.
* Lattice (all sets of size m): κ₀|e_T| ≲ √(2 log(Cp/m)) — the same order as the deletion level √(2 log(p/m)); this is
  why the all-set route stops at exponent 1/6 (W2-FAC-A). So path information is necessary at every scale.
* Numerically (exact simulator Theory_work/Wave2/W2-FAC-S5/numerics/bcs_core.py, s1_path.py; outputs s1_out/):
  κ₀|e_T|/H ≤ 0.005 in the bulk and ≤ 0.17 overall; outside |τ| reaches ≈ 2 × the current deletion level during
  within-group cascades; within one group (h known) the greedy is exactly CS and re-add invariants hold (s2_readd.py).
* Dead ends tried by the lead: (a) "running-max bootstrap": at a time t where e_t = max_{s≤t}|e_s| =: E, nulls with
  fixed singleton coordinate A(∅) and |A| > ℓ_t + κ₀E were never deleted (as singletons) and retained negatives satisfy
  A ≤ −d_t − κ₀E, which forces e_t ≤ small — this works when (i) all retained nulls are singletons in their group
  (true for m ≤ p/polylog up to a vanishing fraction), (ii) t is a record time of the deletion level (d_t = ℓ_t), and
  (iii) ℓ_t ≥ κ₀E; it fails to start because before the singleton regime only the lattice bound (κ₀E ≈ ℓ) is available,
  and the record-time deficit ℓ_t − d_t is controlled only via an interval/asymmetry structure that early-phase drift
  can destroy. (b) Per-group comparison with flip-symmetric reference states: the natural reference thresholds are
  path-dependent per group (adversarial over q^G choices). (c) Frozen-h coupling (process with e ≡ 0 is separable over
  groups and sign-symmetric): perturbation analysis gives a restoring feedback with gain ~ ℓ², but a rigorous stability
  argument for the delayed feedback was not found.
* Useful symmetries: global flip (h, y) → (−h, −y) leaves Π invariant and maps e → −e; per-group flips
  (ζ_g, ξ_{G_g}) → −(…) are symmetries of the law (not of Π).

## 5. Deliverable

Write your work into Theory_work/Wave2/W2-FAC-S5/lemmas/KL_attempt_sol/ (new folder; several files if long; do not edit
anything else). Final message: RESULT (PROVED / PARTIAL / REFUTED / STUCK), the exact statement proved (constants,
regime), the file list, and the weakest step you are least sure of. Rigour standard: a hostile cross-family reviewer
will check every line; no hand-waving about "typical" behaviour; every probabilistic bound uniform over the
data-dependent path via explicit union bounds or symmetry arguments. Local numerics are allowed (py -3.13; numpy/scipy
available) for falsification.

## 6. UPDATE (lead, 2026-11-09 ~09:50) — corrected target (supersedes the "for every c > 0" in §3)

Numerics (numerics/s3_cc.py, s3_out/) and a direct computation show that near the END of the path (few retained
nulls, imbalance ±1) κ₀|e_T| ≈ H/(s₀ + 1 + (1−ρ_b)/ρ_b) — a fixed fraction of H that does not vanish (≈ 0.14 H for
S5, s₀ = 4). So "κ₀|e| ≤ cH for every c > 0" is FALSE in the end phase. The condition actually needed (and now the
ticket's definition) is size-dependent:

**CC_n(δ):** for every visited T_i (k := |T_i|) and every T′ ∈ {T_i} ∪ {T_i ∖ j : j ∈ T_i ∖ S₀}:
  (H_q + κ₀|e_{T′}|)² ≤ (1 − δ)·(log n + 2 log((2p − k)/(k + 1))),   H_q := √(2 log(2^{q̄} p) + 2 log log n).

In the bulk (k ≍ p) this needs κ₀|e| ≤ (√((1−δ) log n) − H_q) (a fixed fraction of H when α < 1/2); in the end phase
(k = O(polylog)) the right side contains + 2 log p ≈ H², so κ₀|e| up to ≈ (√(1 + 1/(2α)) − 1)·H is allowed — FACB's
end-phase imbalance control (|I| ≤ 1 eventually) is the natural tool there. **KL target: P(CC_n(δ)) → 1 for some fixed
δ > 0, under limsup log p/log n < 1/2 (or any smaller exponent > 1/6 you can reach; state the exponent).**
