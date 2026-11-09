# L0 — Imports from W2-FAC-B L1 and their validity for K < p ≤ n − 1

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol xhigh, reviews/R03_L0L1L2_check_sol.md):
VERIFIED-WITH-AMENDMENTS (items 1, 4), applied (re-reading of FACB `lemmas/L1_cs_reduction.md`, whose own status is
"PROVED (by this seat, unchecked)"; lemma check FACB R03 VERIFIED-WITH-AMENDMENTS, applied; FAC-CS council passed).
Falsification numerics: numerics/pk_selftest_out.txt — the closed-form start mode (pk_core.py) equals the general exact-Gram start mode, and the closed-form path has the
same move count, endpoint and sequence of move types (not compared: intermediate variable identities) [R03-4] as (bvs_core.py / fac_core.py, no closed form) on small data
sets, including data sets with p > K (tests "start_mode"/"path" with p > n/2), and reproduce FACB N2 (n = 600,
p = 500 > K = 300, obtained by FACB with the general scorer) exactly.

FACB L1 is stated under FACB's hypotheses, which include p ≤ ⌊n/2⌋. We list every statement used here and check that
its proof uses only p ≤ n − 1. Notation as FACB L1: a = n² − 1, a′ = n − 1, α = a(1 − ρ) + 1, β = aρ,
γ_u = β/(α + uβ) = 1/(u + κ), κ = α/β = (1 − ρ)/ρ + 1/(ρa); κ_c, κ₁, λ₁ as FACB L1.1; ν = 0.01 + n/2.

* **L0.1 (FACB L1.0, L1.1).** Sign flips: unchanged. Representation: X has centred columns with XᵀX = (n − 1)Σ,
  Σ nonsingular; this needs p ≤ n − 1 only. g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ), r := ‖(C − P_X)ε‖²/σ² ~ χ²_{n−1−p} independent
  of g (r ≡ 0 when p = n − 1: the projection is onto the zero space), ‖e‖²/σ² = gᵀΣ⁻¹g + r ~ χ²_{n−1} for every p ≤ n − 1.
  g = √ρη1 + √(1 − ρ)ξ with η ~ N(0, 1), ξ ~ N(0, I_p), η, ξ, r independent; z_j = κ_c + κ₁ξ_j + λ₁θ*_j. Unchanged.
* **L0.2 (FACB L1.2).** F(U) = log w(u) − ½L_u − ν log(0.02 + Q_U), Q_U = (n − 1) − n quad_U,
  quad_U = (A_U − γ_uB_U²)/α, for every U ⊆ [p]: pure algebra (Sherman–Morrison on the u × u block); no condition on p.
* **L0.3 (FACB L1.3).** For **every** T ⊆ [p] with |T| = k ≥ 1, with t_j := z_j − γ_kB_T (j ∈ [p]):
  quad_{T∖j} = quad_T − (1 + γ_{k−1})t_j²/α, quad_{T∪l} = quad_T + (1 − γ_{k+1})t_l²/α,
  quad_{T∖j∪l} = quad_T + [t_l² − t_j² − γ_k(t_l − t_j)²]/α (pure algebra), and the exact gains with ψ_T := 0.02 + Q_T > 0:
  G_del(j) = Δ_k − ν log(1 + n(1 + γ_{k−1})t_j²/(αψ_T)), Δ_k := log[(2p − k)/k] + ½(L_k − L_{k−1});
  G_add(l) = −Δ_{k+1} − ν log(1 − n(1 − γ_{k+1})t_l²/(αψ_T)); G_sw(j, l) = −ν log(1 − n[t_l² − t_j² − γ_k(t_l − t_j)²]/(αψ_T)).
  The prior ratio w(k − 1)/w(k) = (2p − k)/k holds for 1 ≤ k ≤ K ≤ p; ψ_T > 0 because Q_U ≥ yᵀy/(n + 1) (FACB L1.3).
  No condition on p beyond p ≥ K.
* **L0.4 (FACB L1.4).** For T ⊇ S₀, |T| = k: t_j = κ₁(ξ_j − x_T) + λ₁θ*_j with x_T = (s_T − ϱ)/(k + κ), s_T = Σ_{j∈T}ξ_j,
  ϱ = [√(n − 1)ρθ̄/(σ√(1 − ρ)) + √(ρ/(1 − ρ))αη]/β (FACB L4.0(a) form), |ϱ| ≤ C_ρ(|η| + 1) for n ≥ n₀: algebra plus
  n large; no condition on p. Drift identity x_{T∖j} = x_T − (ξ_j − x_T)/(k − 1 + κ) **for null j ∈ T** (so T ∖ j ⊇ S₀): algebra [R03-1]. (Not used in
  L1–L3.)
* **L0.5 (FACB L1.5).** (a) |L_u − L_{u−1} − log(n + 1)| ≤ 6/((n − 1)(1 − ρ)) for every u ≥ 1, n ≥ n₀(ρ): uses only the
  closed form of L_u. Hence Δ_k = log[(2p − k)/k] + ½log(n + 1) + δ_{n,k}, |δ_{n,k}| ≤ 3/((n − 1)(1 − ρ)).
  (b) For T ⊇ S₀: RSS_T/s² ≤ Q_T ≤ RSS_T/s² + 1 + 1/((n − 1)(1 − ρ)), RSS_T = ‖e‖² − σ²Φ(T), Φ(T) = g_TᵀΣ_TT⁻¹g_T: uses
  μ ∈ span X_T, λ_min(G_T) ≥ (n − 1)(1 − ρ) and z_TᵀG_T⁻¹z_T ≤ yᵀy; no condition on p. (c) With
  M_T := νnκ₁²/(αψ_T) (the multiplier of FACB L4.0(b)) and m_T := nσ²/(2(RSS_T + s²c_ρ)), c_ρ := 1.02 + 1/((n − 1)(1 − ρ)):
  m_T(1 − 2/n) ≤ M_T ≤ (1 + 1/n)nσ²/(2RSS_T) for n ≥ n₀(ρ) (uses n(n − 1)(1 − ρ)/α ∈ [1 − 2/n, 1]); no condition on p.
* **L0.6 (τ-form of the gains, FACB L4.0(b)).** For T ⊇ S₀ and nulls j ∈ T, l ∉ T, with τ := t/κ₁ = ξ − x_T:
  G_del(j) = Δ_k − ν log(1 + (1 + γ_{k−1})M_Tτ_j²/ν), G_add(l) = −Δ_{k+1} − ν log(1 − (1 − γ_{k+1})M_Tτ_l²/ν),
  G_sw(j, l) = −ν log(1 − M_TV_{jl}/ν), V_{jl} := τ_l² − τ_j² − γ_k(τ_l − τ_j)² (substitute t = κ₁τ in L0.3:
  n t²/(αψ_T) = M_Tτ²/ν). Since −log(1 − v) ≥ v for v < 1: **G_sw(j, l) ≥ M_TV_{jl}** whenever the swap is feasible.

**Not imported:** FACB L1's uses of p ≤ n/2 occur only downstream (FACB L3 E2: r ≥ (n − 1 − p)(1 − n^{−1/3}) with
n − 1 − p ≥ n/2 − 1, and FACB L4.0(d)'s bulk bound M_T ≤ 1 + n^{−1/4}). Neither is used in this ticket. Bounds on M_T used:
the lower bound of L0.5(c) with RSS_T ≤ ‖e‖² (L2, L3), and two upper bounds in L3 — the uniform floor (E4)/(M1), proved
there for p ≤ n − 1, and FACB L4.0(d)'s small-energy refinement (M2), whose proof uses only RSS_T = ‖e‖² − σ²Φ(T) and
E2 (no condition on p) [R04-4].
