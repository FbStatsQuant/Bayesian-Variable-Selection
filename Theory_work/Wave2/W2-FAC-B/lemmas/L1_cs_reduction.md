# L1 — Compound symmetry: exact one-dimensional reduction of the score and of every LS0 scan

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high, reviews/R03_L1L2L3_check_sol.md):
VERIFIED-WITH-AMENDMENTS (items 1, 2), applied. Falsification numerics: numerics/cs_selftest.py → cs_selftest_out.txt
(closed form = general exact-Gram scorer to 5·10⁻⁷ at n = 10⁶ (relative 10⁻¹³), and the closed-form LS0 path has the
same endpoint and move count as the general scanner's path in 4/4 cases — intermediate moves are not compared; R07 item 9); numerics/fac_selftest_out.txt (general exact-Gram scorer = direct
n × p scoring to 4·10⁻¹⁴; closed-form Schur scans = direct to 1.4·10⁻¹²).

Setting: STATEMENT §1–2, hypotheses G, (CS). Throughout, T ⊆ [p], k := |T|, a := n² − 1, a′ := n − 1.

## L1.0 Sign flips

Let Υ be a diagonal ±1 matrix. Replacing X by XΥ and θ* by Υθ* leaves μ = Xθ* unchanged and maps, for every A,
G_A ↦ Υ_AG_AΥ_A and z_A ↦ Υ_Az_A. Hence det H_A, det(G_A + I) and z_AᵀH_A⁻¹z_A are unchanged, so log m(A), F(A),
every block table r_b(U), γ₀ and every LS0 scan are unchanged; |r̂_{jk}| and hence the partition are unchanged.
All conclusions of this ticket concern only these objects. **We therefore take Υ_n = I** and write ϑ for the truth
coefficients (STATEMENT (θ)).

## L1.1 Exact-Gram representation of the data

X has centred columns with XᵀX = (n − 1)Σ, Σ = (1 − ρ)I + ρ11ᵀ, nonsingular (eigenvalues 1 − ρ and 1 − ρ + pρ).
Let e := Cε (C the centring projector). Since Xᵀ1 = 0, Xᵀe = Xᵀε ~ N(0, σ²(n − 1)Σ). Put g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ),
P_X := X(XᵀX)⁻¹Xᵀ and r := ‖(C − P_X)ε‖²/σ². Then (Gaussian projections onto orthogonal subspaces of 1^⊥) g and r are
independent, r ~ χ²_{n−1−p}, and ‖e‖² = σ²(gᵀΣ⁻¹g + r). Every quantity used by the method is a function of
(XᵀX, Xᵀy, yᵀy), and with Y := Cy^r = μ + e, s² := ‖Y‖²/(n − 1), y = Y/s:

  z := Xᵀy = [(n − 1)Σθ* + σ√(n − 1) g]/s,  yᵀy = n − 1,  (n − 1)s² = (n − 1)θ*ᵀΣθ* + 2σ√(n − 1)θ*ᵀg + ‖e‖².

Since Σ = ρ11ᵀ + (1 − ρ)I, we may (enlarging the probability space, which changes no probability of an event
measurable in (g, r)) write

  g = √ρ η 1 + √(1 − ρ) ξ,   η ~ N(0, 1), ξ ~ N(0, I_p), η, ξ, r independent.

With θ̄ := Σ_{j∈S₀}θ*_j = ϑ(S₀) and (Σθ*)_j = ρθ̄ + (1 − ρ)θ*_j:

  z_j = κ_c + κ₁ξ_j + λ₁θ*_j,  κ_c := [(n − 1)ρθ̄ + σ√((n − 1)ρ) η]/s,  κ₁ := σ√((n − 1)(1 − ρ))/s,  λ₁ := (n − 1)(1 − ρ)/s.

(For a null j, θ*_j = 0.)

## L1.2 Closed form of F

For |U| = u ≥ 1, Σ_UU = (1 − ρ)I_u + ρJ_u, so H_U = (n + 1)(n − 1)Σ_UU + I = αI_u + βJ_u and
G_U + I = α′I_u + β′J_u with

  α := a(1 − ρ) + 1, β := aρ, α′ := a′(1 − ρ) + 1, β′ := a′ρ.

By Sherman–Morrison, (αI + βJ_u)⁻¹ = α⁻¹(I − γ_uJ_u), γ_u := β/(α + uβ), and det(αI + βJ_u) = α^{u−1}(α + uβ).
Hence, with A_U := Σ_{j∈U}z_j² and B_U := Σ_{j∈U}z_j,

  quad_U := z_UᵀH_U⁻¹z_U = (A_U − γ_uB_U²)/α,  Q_U = (n − 1) − n quad_U,
  L_u := log det H_U − log det(G_U + I) = (u − 1)log(α/α′) + log[(α + uβ)/(α′ + uβ′)]  (L_0 := 0),
  F(U) = log w(u) − ½L_u − ν log(0.02 + Q_U) + const.

So F(U) depends on U only through (u, A_U, B_U).

**Identities.** γ_{u−1}/(1 + γ_{u−1}) = γ_u and γ_{u+1}/(1 − γ_{u+1}) = γ_u (both equal β/(α + uβ)), i.e.
γ_u(1 + γ_{u−1}) = γ_{u−1} and γ_{u+1}(1 + γ_u) = γ_u. Also γ_u = 1/(u + κ_n) with κ_n := (1 − ρ)/ρ + 1/(ρa).

## L1.3 Every neighbour of T in closed form

Fix T with |T| = k ≥ 1, put c_T := γ_kB_T and t_j := z_j − c_T for every j ∈ [p] (in or out of T). Then

* deletion of j ∈ T:  quad_{T∖j} = quad_T − (1 + γ_{k−1}) t_j²/α;
* addition of l ∉ T:  quad_{T∪l} = quad_T + (1 − γ_{k+1}) t_l²/α;
* swap (j ∈ T out, l ∉ T in): quad_{T∖j∪l} = quad_T + [t_l² − t_j² − γ_k(t_l − t_j)²]/α.

*Proof.* Deletion: α(quad_{T∖j} − quad_T) = −z_j² − γ_{k−1}(B − z_j)² + γ_kB² = −(1 + γ_{k−1})z_j² + 2γ_{k−1}Bz_j
− (γ_{k−1} − γ_k)B², and −(1 + γ_{k−1})(z_j − γ_kB)² expands to the same expression because (1 + γ_{k−1})γ_k = γ_{k−1}
and (1 + γ_{k−1})γ_k² = γ_{k−1}γ_k = γ_{k−1} − γ_k. Addition: α(quad_{T∪l} − quad_T) = (1 − γ_{k+1})z_l² − 2γ_{k+1}Bz_l
+ (γ_k − γ_{k+1})B², which equals (1 − γ_{k+1})(z_l − γ_kB)² because (1 − γ_{k+1})γ_k = γ_{k+1} and γ_{k+1}γ_k = γ_k − γ_{k+1}.
Swap (size stays k): α(quad′ − quad_T) = z_l² − z_j² − γ_k[2B(z_l − z_j) + (z_l − z_j)²]
= (t_l² − γ_k²B²) − (t_j² − γ_k²B²) − γ_k(t_l − t_j)². ∎

(The case k = 0 needs only additions: quad_{{l}} = (1 − γ₁)z_l²/α, consistent with c_∅ := 0.)

**Gains.** Write ψ_T := 0.02 + Q_T (> 0, since Q_U ≥ yᵀy/(n + 1) > 0 — H_U ⪰ (n + 1)G_U gives n z_UᵀH_U⁻¹z_U ≤
(n/(n + 1))yᵀP_Uy) and ε_n := n/α. Then the F-gain of every neighbour is, exactly,

  del(j):  Δ_k − ν log(1 + ε_n(1 + γ_{k−1})t_j²/ψ_T),         Δ_k := log[(2p − k)/k] + ½(L_k − L_{k−1}),
  add(l):  −Δ_{k+1} − ν log(1 − ε_n(1 − γ_{k+1})t_l²/ψ_T),
  swap(j,l): −ν log(1 − ε_n[t_l² − t_j² − γ_k(t_l − t_j)²]/ψ_T),

(w(k − 1)/w(k) = (2p − k)/k; the arguments of the logarithms are Q_{neighbour}/Q_T-type ratios of positive numbers).
Each gain is a strictly monotone function of a single scalar: deletions are ordered by |t_j| (smaller is better),
additions by |t_l| (larger is better), and all of them share the **same centre c_T**.

## L1.4 The centre in ξ-units

For T ⊇ S₀ put s_T := Σ_{j∈T}ξ_j. Then B_T = kκ_c + κ₁s_T + λ₁θ̄ and, for every j,

  t_j = κ₁(ξ_j − x_T) + λ₁θ*_j,   x_T := γ_k s_T − r_k,
  r_k := [κ_c(1 − kγ_k) − γ_kλ₁θ̄]/κ₁ = [√(n − 1) ρθ̄/(σ√(1 − ρ)) + √(ρ/(1 − ρ)) α η]/(α + kβ).

*Proof.* t_j = κ_c + κ₁ξ_j + λ₁θ*_j − γ_k(kκ_c + κ₁s_T + λ₁θ̄). With 1 − kγ_k = α/(α + kβ):
κ_cα − βλ₁θ̄ = [(n − 1)ρθ̄α + σ√((n − 1)ρ)ηα − a ρ (n − 1)(1 − ρ)θ̄]/s = [(n − 1)ρθ̄ + σ√((n − 1)ρ)αη]/s, since
α − a(1 − ρ) = 1; divide by κ₁(α + kβ) = σ√((n − 1)(1 − ρ))(α + kβ)/s. ∎

Consequences: (i) for **nulls** t_j = κ₁(ξ_j − x_T): the scan is a one-dimensional problem in the fixed numbers
ξ_j with the moving centre x_T; (ii) for **truths** t_j = κ₁(ξ_j − x_T + √(n − 1)√(1 − ρ)θ*_j/σ); (iii)
|r_k| ≤ √(ρ/(1 − ρ))|η|·α/(α + kβ) + √(n − 1)ρ|θ̄|/(σ√(1 − ρ)(α + kβ)), so |r_k| ≤ C(|η| + 1)/(k + κ_n)
with C depending on ρ only, once n ≥ n₀(ρ, θ̄, σ), by the exact identity α/(α + kβ) = (1 − ρ + 1/a)/(ρ(k + κ_n)) (the
deterministic part times (k + κ_n) is √(n − 1)|θ̄|/(σ√(1 − ρ)a) → 0) [R03 item 1];
(iv) x_T = (s_T − r_k(k + κ_n))/(k + κ_n) is a shrunk mean of the ξ's in T.

## L1.5 Size-only terms and the effective multiplier

(a) L_u − L_{u−1} = log(α/α′) + log[(α + uβ)/(α′ + uβ′)] − log[(α + (u − 1)β)/(α′ + (u − 1)β′)] and, since
α = (n + 1)(α′ − 1) + 1, (α + vβ)/(α′ + vβ′) = (n + 1) − n/(α′ + vβ′) for v ≥ 0:
|L_u − L_{u−1} − log(n + 1)| ≤ 6/((n − 1)(1 − ρ)) for n ≥ n₀(ρ). Hence Δ_k = log[(2p − k)/k] + ½log(n + 1) + δ_{n,k},
|δ_{n,k}| ≤ 3/((n − 1)(1 − ρ)).

(b) **Q versus RSS.** For T ⊇ S₀ let RSS_T := ‖(I − P_T)Y‖² = ‖e‖² − σ²Φ(T), Φ(T) := g_TᵀΣ_TT⁻¹g_T (because μ ∈ span X_T).
Then RSS_T/s² ≤ Q_T ≤ RSS_T/s² + 1 + 1/((n − 1)(1 − ρ)).
*Proof.* (n − 1) − z_TᵀG_T⁻¹z_T = RSS_T/s². nH_T⁻¹ = (n/(n + 1))(G_T + I/(n + 1))⁻¹ ⪯ G_T⁻¹ gives the lower bound;
(G + I/(n + 1))⁻¹ ⪰ G⁻¹ − G⁻²/(n + 1), z_TᵀG_T⁻²z_T ≤ h/λ_min(G_T) with h := z_TᵀG_T⁻¹z_T ≤ yᵀy = n − 1 and
λ_min(G_T) ≥ (n − 1)(1 − ρ) give n z_TᵀH_T⁻¹z_T ≥ (n/(n + 1)) h [1 − 1/((n + 1)(n − 1)(1 − ρ))]. Hence
0 ≤ Q_T − RSS_T/s² ≤ h/(n + 1) + n h/((n + 1)²(n − 1)(1 − ρ)) ≤ (n − 1)/(n + 1) + n/((n + 1)²(1 − ρ))
≤ 1 + 1/((n − 1)(1 − ρ)). ∎ [R03 item 2]

(c) In the gains the data enter through ν ε_n κ₁²/ψ_T = ν n(n − 1)(1 − ρ)σ²/(α s² ψ_T). Define
m_T := nσ²/(2(RSS_T + s²c_ρ)), c_ρ := 1.02 + 1/((n − 1)(1 − ρ)). By (b), with n(n − 1)(1 − ρ)/α ∈ [1 − 2/n, 1] for
n ≥ n₀(ρ) (an eventual bound, uniform in T):

  m_T(1 − 2/n) ≤ ν ε_n κ₁²/ψ_T ≤ (1 + 1/n) nσ²/(2RSS_T).

All later lemmas use only L1.3–L1.5.
