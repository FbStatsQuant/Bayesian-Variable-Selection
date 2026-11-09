# X1 — Iid compound-symmetric rows: exact representation, reference statistic and exact gain formulas

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high): VERIFIED-WITH-AMENDMENTS (one MINOR
wording item, applied). Falsification numerics: numerics/iid_selftest_out.txt (Bartlett
sufficient statistics: law check against explicit rows; incremental exact scorer = direct closed-form scan to
≤ 4.5·10⁻⁸ at n ≤ 10⁷ (worst 4.447e−08)); numerics/N1X_summary.md (an empirical proxy of the perturbation size).

Setting: STATEMENT §1–2 (model R, (CS-R), (P-½), (θ)). Sign flips: replacing X^r by X^rΥ and β by Υβ leaves the
data, every score and every partition unchanged (FACB L1.0 verbatim, it uses only Gram/score invariances), so
**Υ_n = I**. Notation: V := 1^⊥ ⊂ ℝⁿ (dim n − 1), C the projector onto V, N := n − 3, ℓ := √(ρ/(1 − ρ)),
L_n := log log n. For a finite set T, k := |T|.

## X1.1 Exact rotation representation

Represent the rows as x^r_i = m + √ρ F_i 1 + √(1 − ρ)U_i with F_i ~ N(0, 1), U_i ~ N_p(0, I) iid (this is exactly
N_p(m, Σ)). Centring gives, for every column j, g_j := Cx^r_{·j} = √ρ f + √(1 − ρ)u_j with f := CF, u_j := CU_{·j};
e := Cε. The n-vectors f, u_1, …, u_p, e/σ are iid N(0, C) (standard Gaussian in V), independent.

Define e₁ := e/‖e‖, η := fᵀe₁, f_⊥ := f − ηe₁, φ := ‖f_⊥‖, e₂ := f_⊥/φ, and for every j:
ξ_j := u_jᵀe₁, a_j := u_jᵀe₂, u_j^⊥ := u_j − ξ_je₁ − a_je₂ ∈ V₃ := V ∩ {e₁, e₂}^⊥ (dim N).

**Lemma X1.1.** ‖e‖, η, φ, ξ = (ξ_j), a = (a_j) are mutually independent, ‖e‖²/σ² ~ χ²_{n−1}, η ~ N(0, 1),
φ² ~ χ²_{n−2}, ξ_j, a_j iid N(0, 1); and W := (u_j^⊥ᵀu_l^⊥)_{j,l≤p} ~ W_p(N, I) is independent of
(‖e‖, η, φ, ξ, a).

*Proof.* e/σ is standard Gaussian in V: ‖e‖ and e₁ are independent, e₁ uniform on the unit sphere of V. Given e₁,
f is standard Gaussian in V, so η = fᵀe₁ ~ N(0, 1) and f_⊥ (standard Gaussian in the (n − 2)-dimensional space
V ∩ e₁^⊥) are conditionally independent; the conditional joint law of (η, φ) is N(0, 1) ⊗ χ_{n−2}, which does not depend
on e₁ (the ambient vector f_⊥ itself is of course not independent of e₁ — R03 X1 item 1); given (e₁, φ), e₂ is uniform on
the unit sphere of V ∩ e₁^⊥. Given
(e₁, e₂, ‖e‖, η, φ), the u_j are iid standard Gaussian in V; writing V = span(e₁) ⊕ span(e₂) ⊕ V₃ (orthonormal,
determined by the conditioning), the coordinates ξ_j, a_j and the components u_j^⊥ are independent, ξ_j, a_j ~ N(0, 1),
u_j^⊥ standard Gaussian in V₃. The conditional law of (ξ, a, W) given (e₁, e₂, ‖e‖, η, φ) therefore does not depend on
the conditioning values (the Gram matrix of p iid standard Gaussian vectors in an N-dimensional space is W_p(N, I)
whatever the space), which gives all independence claims. ∎

Coordinates: g_j = v1_j e₁ + v2_j e₂ + √(1 − ρ)u_j^⊥, with v1_j := √ρη + √(1 − ρ)ξ_j, v2_j := √ρφ + √(1 − ρ)a_j.
Whitened: ṽ1 := v1/√(1 − ρ) = ξ + ℓη1, ṽ2 := v2/√(1 − ρ) = ℓφ1 + a.

The method's design is X = [g_j/sd_j]_j with sd_j² = ‖g_j‖²/(n − 1); μ = Xθ* = Σ_{j∈S₀}β_jg_j (θ* = D_xβ);
Y = μ + e; y = Y/s. Every score uses only (G = XᵀX, z = Xᵀy, yᵀy = n − 1) (SoP `04_theory.tex:69-74`).

## X1.2 RSS and partial-regression statistics for T ⊇ S₀

Let P_T be the orthogonal projector onto span{g_j : j ∈ T} = span X_T (column scaling does not change spans); for
T ⊇ S₀, μ ∈ span X_T, so RSS_T := ‖(I − P_T)Y‖² = ‖(I − P_T)e‖² = ‖e‖²(1 − ‖P_Te₁‖²).

For T ⊆ [p] with |T| ≤ N put A_T := W_T + ṽ2_Tṽ2_Tᵀ (positive definite whenever W_T is, which holds on the event
λ_min(W) > 0 of X2) and q_T := ṽ1_TᵀA_T⁻¹ṽ1_T (q_∅ := 0).

**Lemma X1.2.** (a) ‖P_Te₁‖² = q_T/(1 + q_T); hence RSS_T = ‖e‖²/(1 + q_T) for T ⊇ S₀.
(b) For j ∈ T: q_T − q_{T∖j} = ω_j(T)², ω_j(T) := (A_T⁻¹ṽ1_T)_j/√((A_T⁻¹)_jj).
(c) For T ⊇ S₀ and a null j ∈ T: RSS_{T∖j} − RSS_T = ‖e‖²ω_j(T)²/((1 + q_T)(1 + q_{T∖j})).

*Proof.* (a) The Gram matrix of g_T is G^r_T = (1 − ρ)[ṽ1ṽ1ᵀ + ṽ2ṽ2ᵀ + W_T] = (1 − ρ)[ṽ1ṽ1ᵀ + A_T] and
g_Tᵀe₁ = √(1 − ρ)ṽ1_T, so ‖P_Te₁‖² = ṽ1ᵀ(ṽ1ṽ1ᵀ + A)⁻¹ṽ1 = q/(1 + q) (Sherman–Morrison). (b) The standard identity
vᵀA⁻¹v − v_{−j}ᵀ(A_{−j,−j})⁻¹v_{−j} = (A⁻¹v)_j²/(A⁻¹)_jj for positive definite A, with A_{T∖j} = (A_T)_{−j,−j}.
(c) For a null j ∈ T ⊇ S₀ also T ∖ j ⊇ S₀; subtract the two instances of (a). ∎

## X1.3 Reference statistic (W = NI, a = 0) — FACB's one-dimensional scan

Put κ := N/(ℓ²φ²), ϱ := Nη/(ℓφ²) (random, **T-independent**, independent of ξ), γ_k := 1/(k + κ), and for S₀ ⊆ T:
x_T := (Σ_{j∈T}ξ_j − ϱ)/(k + κ), which satisfies the **exact drift identity** x_{T∖j} = x_T − (ξ_j − x_T)/(k − 1 + κ)
and x_{T∪l} = x_T + (ξ_l − x_T)/(k + 1 + κ).

**Lemma X1.3.** If W_T is replaced by NI_k and (a_j)_{j∈T} by 0, then A_T⁻¹ṽ1_T = N⁻¹(ξ_j − x_T)_{j∈T} and
(A_T⁻¹)_jj = N⁻¹(1 − γ_k); so √N √(1 − γ_k) ω_j(T) = ξ_j − x_T.

*Proof.* A⁰ = NI + ℓ²φ²11ᵀ, (A⁰)⁻¹ = N⁻¹(I − γ_k11ᵀ) since ℓ²φ²/(N + kℓ²φ²) = 1/(κ + k). Then
N(A⁰)⁻¹ṽ1 = ξ + ℓη1 − γ_k(s_T + kℓη)1 and ℓη − γ_k(s_T + kℓη) = −γ_k(s_T − κℓη) with κℓη = ϱ. ∎

This is FACB's centre: FACB L4.0(a) has x_T = (s_T − ϱ_B)/(k + κ_B) with κ_B = (1 − ρ)/ρ + 1/(ρ(n² − 1)) and
ϱ_B = √((1 − ρ)/ρ)η + O(n^{−1/2}); here κ = ((1 − ρ)/ρ)·N/φ² and ϱ = √((1 − ρ)/ρ)η·N/φ² (the same up to factors
1 + O_P(n^{−1/2})). The algebraic/geometric template of FACB (scan structure, drift identity, gap and balance arguments) uses only
κ ∈ [κ_∞/2, 2κ_∞ + 1] (κ_∞ := (1 − ρ)/ρ), |ϱ| ≤ C(|η| + 1) and the drift identity, which hold for this (κ, ϱ) on the
event φ²/N ∈ [½, 2] (X2). FACB's specific end-phase constant c_D = ½ − 1/(s₀ + 1 + κ_∞) additionally needs
κ = κ_∞ + o(1), which D3 supplies (X4.5; R06 item 1). The perturbed score formulas below are not FACB's exact formulas.

**Definition.** For S₀ ⊆ T and j ∈ T: τ̂_j(T) := √N √(1 − γ_k) ω_j(T) and δ_j(T) := τ̂_j(T) − (ξ_j − x_T).
X2 bounds δ.

## X1.4 Exact gains in terms of τ̂ (all nulls; T ⊇ S₀)

Write G_T = X_TᵀX_T, ε₁ := 1/(n + 1), H_T = (n + 1)(G_T + ε₁I), ψ_T := 0.02 + Q_T, Q_T = (n − 1) − n z_TᵀH_T⁻¹z_T,
LD(T) := log det H_T − log det(G_T + I), and (prior) log w(k − 1) − log w(k) = log((2p − k)/k). Assume (design event
of X2) λ_min(G_T) ≥ c₀(n − 1) for every T (c₀ := (1 − ρ)/5), ‖e‖²/σ² ∈ [n/2, 2n], s² ∈ [s_min², s_max²] (FACB L2.2),
q_T ≤ 1/10 and ω_j(T)² ≤ 1/10 for every T and j used.

**(g1) Size terms.** For j ∈ T: LD(T ∖ j) − LD(T) = log (H_T⁻¹)_jj − log ((G_T + I)⁻¹)_jj = −log(n + 1) + e¹_j(T),
|e¹_j(T)| ≤ 3/(c₀(n − 1)).
*Proof.* det M_T = det M_{T∖j}/(M_T⁻¹)_jj for positive definite M. For t ∈ {ε₁, 1}, (G + tI)⁻¹ = G⁻¹ − tG⁻¹(G + tI)⁻¹
gives G⁻¹ − tG⁻² ⪯ (G + tI)⁻¹ ⪯ G⁻¹, and (G⁻²)_jj ≤ (G⁻¹)_jj/λ_min(G); so ((G + tI)⁻¹)_jj/(G⁻¹)_jj ∈
[1 − t/λ_min, 1]; and (H⁻¹)_jj = ε₁((G + ε₁I)⁻¹)_jj. Take logarithms (|log(1 − u)| ≤ 2u for u ≤ ½). ∎

**(g2) Data terms.** For j ∈ T null: Q_{T∖j} − Q_T = (n/(n + 1))P^{ε₁}_j(T), P^t_j := ((G + tI)⁻¹z)_j²/((G + tI)⁻¹)_jj
(ridge partial statistic; Schur identity as in X1.2(b) applied to H_T = (n + 1)(G_T + ε₁I)). The OLS value is
P⁰_j(T) = ‖(P_T − P_{T∖j})y‖² = (RSS_{T∖j} − RSS_T)/s². With b(t) := (G + tI)⁻¹z: b(t) − b(0) = −t(G + tI)⁻¹b(0),
so |b(ε₁)_j − b(0)_j| ≤ ε₁‖b(0)‖/λ_min; b(0) = θ*_T/s + G_T⁻¹X_Tᵀe/s has ‖b(0)‖ ≤ ‖θ*‖/s + ‖e‖/(s√λ_min) ≤ C_b
(C_b depends on ρ, σ, ϑ only, on the design event; ‖θ*‖ ≤ 2‖ϑ‖ there). With (G⁻¹)_jj ≥ 1/G_jj = 1/(n − 1) and
((G + ε₁I)⁻¹)_jj ∈ [(1 − ε₁/λ_min)(G⁻¹)_jj, (G⁻¹)_jj]:
|√P^{ε₁}_j − √P⁰_j| ≤ C_b ε₁ √(n − 1)/(λ_min√(1 − ε₁/λ_min)) + √P⁰_j·ε₁/λ_min ≤ C n^{−3/2}(1 + √P⁰_j), hence
  Q_{T∖j} − Q_T = (n/(n + 1))(‖e‖²/s²)·ω_j(T)²/((1 + q_T)(1 + q_{T∖j})) + r_j(T),  |r_j(T)| ≤ C n^{−3/2}(1 + P⁰_j(T)).

**(g3) Deletion gain.** Put M_T := ν(n/(n + 1))(‖e‖²/s²)/(N(1 + q_T)²ψ_T) and 1 + ε^d_j(T) := (1 + q_T)/(1 + q_{T∖j})
∈ [1, 1 + 2ω_j(T)²] (q_{T∖j} = q_T − ω_j²). Since ω_j² = τ̂_j²/(N(1 − γ_k)) and 1/(1 − γ_k) = 1 + γ_{k−1}, exactly
  G_del(j; T) := F(T ∖ j) − F(T) = Δ_k − ½e¹_j(T) − ν log(1 + (1 + γ_{k−1})M_T(1 + ε^d_j)τ̂_j(T)²/ν + r_j(T)/ψ_T),
Δ_k := log((2p − k)/k) + ½log(n + 1). Bounds on the design event: ψ_T ≥ RSS_T/s² ≥ ‖e‖²/(s²(1 + q_T)) (Q_T ≥ RSS_T/s²:
FACB L1.5(b), which uses only H_T ⪰ (n + 1)G_T ≻ 0) and ψ_T ≤ RSS_T/s² + 1.1 (same reference, λ_min(G_T) ≥ c₀(n − 1));
hence |r_j/ψ_T| ≤ C n^{−5/2}(1 + τ̂_j²) and
  ½(1 − 3q_T − C n^{−1/3}) ≤ M_T ≤ ½(1 + C/n)
(ν = n/2 + 0.01, N = n − 3, ‖e‖²/s² ≥ n/(4s_max²/σ²)). **This is FACB's L4.0(b) deletion formula with τ_j replaced by
τ̂_j(T)**, up to the j-dependent errors e¹_j (≤ 3/(c₀n), outside the logarithm) and ε^d_j, r_j (inside). Compared
with FACB L4.0(d) (M_T ∈ [¼, 1 + n^{−1/4}]) the bound is sharper because q_T ≤ 1/10 here.

**(g4) Additions.** For a null l ∉ T: G_add(l; T) = −G_del(l; T ∪ l) (T ∪ l ⊇ S₀), so by (g3) at T ∪ l and log(1 + u) ≤ u:
  G_add(l; T) ≤ −Δ_{k+1} + 3/(c₀n) + (1 + γ_k)M_{T∪l}(1 + ε^d)τ̂_l(T ∪ l)² + C n^{−5/2}(1 + τ̂²)ν,
and by the drift identity the reference value of τ̂_l(T ∪ l) is ξ_l − x_{T∪l} = (1 − γ_{k+1})(ξ_l − x_T), so that
(1 + γ_k)(1 − γ_{k+1})²(ξ_l − x_T)² = (1 − γ_{k+1})(ξ_l − x_T)² — FACB's addition statistic.
(The ν-multiplied remainder is ≤ C n^{−3/2}(1 + τ̂²), negligible.)

**(g5) Swaps.** For a null-out swap (j ∈ T null out, l ∉ T null in, T′ := T ∖ j ∪ l, |T′| = k):
LD(T′) − LD(T) = [LD(T ∖ j) − LD(T)] + [LD(T′) − LD(T′ ∖ l)] = −e¹_l(T′) + e¹_j(T) (the ±log(n + 1) cancel), so
  G_sw(j, l) = ½(e¹_l(T′) − e¹_j(T)) − ν log(1 − M_T V̂_{jl}/ν),  V̂_{jl} := (ν/M_T)(Q_T − Q_{T′})/ψ_T.
Q_T − Q_{T′} = (Q_{T′∖l} − Q_{T′}) − (Q_{T∖j} − Q_T) with T′ ∖ l = T ∖ j; apply (g2)–(g3) to (T′, l) and (T, j):
  V̂_{jl} = (1 + γ_{k−1})[(M_{T′}ψ_{T′}/(M_Tψ_T))(1 + ε^d_l(T′))τ̂_l(T′)² − (1 + ε^d_j(T))τ̂_j(T)²] + O(n^{−3/2}(1 + H̄²)),
with M_{T′}ψ_{T′}/(M_Tψ_T) = (1 + q_T)²/(1 + q_{T′})² = 1 + O(ω²) (q_T − q_{T′} = ω_j(T)² − ω_l(T′)²). The reference values
are τ_j := ξ_j − x_T and ξ_l − x_{T′} = (1 − γ_k)(ξ_l − x_{T∖j}) = (1 − γ_k)(τ_l + γ_{k−1}τ_j), τ_l := ξ_l − x_T (drift
identities), and the algebraic identity
  (1 + γ_{k−1})[(1 − γ_k)²(τ_l + γ_{k−1}τ_j)² − τ_j²] = τ_l² − τ_j² − γ_k(τ_l − τ_j)² =: V_{jl}
(use (1 + γ_{k−1})(1 − γ_k) = 1, (1 − γ_k)γ_{k−1} = γ_k, γ_kγ_{k−1} − γ_{k−1} = −γ_k) shows that V_{jl} is FACB's exact swap
quantity (L4.0(b)). Hence, whenever |τ_j|, |τ_l|, |τ̂| ≤ 3H̄:
  |V̂_{jl} − V_{jl}| ≤ 12H̄(|δ_j(T)| + |δ_l(T′)|) + 4(δ_j² + δ_l²) + C H̄⁴ max(ω²) + C n^{−3/2}(1 + H̄²).
Truth moves (deletion of j ∈ S₀, or a swap removing a truth) are not covered by (g2) and are treated in X4 directly.

**Remark (what changes vs FACB).** FACB's scan is the case δ ≡ 0, e¹ ≡ r ≡ 0. X2 shows that on the relevant sets
|δ_j(T)| ≤ ϖ_n ≤ n^{−c} (with the band-count absorption of X4); X3–X4 show that FACB's L4 survives ϖ_n-perturbations of
the null partial statistics; truth moves are treated separately (X4.6).
