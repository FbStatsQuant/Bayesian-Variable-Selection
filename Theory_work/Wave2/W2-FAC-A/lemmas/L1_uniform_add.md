# L1 — Key lemma U: a uniform, factor-aware bound on the add statistic over ALL subsets

Status: **PROVED (by this seat, unchecked)**; key-lemma check R02 (Codex gpt-6.1-sol xhigh,
reviews/R02_L1_check_sol.md): VERIFIED-WITH-AMENDMENTS (5 MINOR), all applied — v1.1, 2026-11-09. Falsification
numerics: numerics/fu_check.py → FU_out.txt, fu5_check.py → FU5_out.txt; R02's own exhaustive check (in R02).

Notation: STATEMENT.md §1–§2. For a symmetric positive semidefinite p × p matrix M, T ⊆ [p] and l ∉ T with M_TT ≻ 0
and v_M > 0 (R02 item 3; in particular for every positive definite M) put
c_M := M_TT⁻¹M_{Tl} (c_M := 0 if T = ∅), v_M := M_ll − M_{lT}c_M (Schur complement), and the vector
a_M ∈ ℝ^p with (a_M)_l = 1/√v_M, (a_M)_T = −c_M/√v_M, zero elsewhere. For x ∈ ℝ^p,
  Z^M_{T,l}(x) := a_Mᵀx = (x_l − M_{lT}M_TT⁻¹x_T)/√v_M,
the standardised innovation of x_l given x_T when x ~ N(0, M).

## L1.0 The add statistic is a Gram-only innovation

Under model G with standardised X (centred columns), R̂ := XᵀX/(n − 1) and g := Xᵀε/(σ√(n − 1)). For T ⊆ [p] with
R̂_TT ≻ 0 and l ∉ T with (I − P_T)x_l ≠ 0, the add direction u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖ satisfies

  Z_{T,l} := u_{T,l}ᵀε/σ = Z^{R̂}_{T,l}(g),   and, conditionally on X, g ~ N(0, R̂).                         (0.1)

*Proof.* (I − P_T)x_l = x_l − X_T(X_TᵀX_T)⁻¹X_Tᵀx_l, so (I − P_T)x_lᵀε = σ√(n−1)(g_l − R̂_{lT}R̂_TT⁻¹g_T) and
‖(I − P_T)x_l‖² = (n−1)(R̂_ll − R̂_{lT}R̂_TT⁻¹R̂_{Tl}) = (n−1)v_{R̂}. Since the columns of X are centred, Xᵀε = XᵀCε and
Cov(Xᵀε | X) = σ²XᵀX. ∎

So everything below is a statement about a Gaussian vector and its covariance. We avoid a direct union bound over the
innovation normals indexed by (T, l): we union over the local innovation pairs (l, U) and over subsets of factor groups
with thresholds depending on the number of groups (when all groups are singletons the latter are 2^p − 1 subsets, whose
count is absorbed by the size-dependent threshold); the factor variables W_T (up to 2^p of them) are controlled
simultaneously by the deterministic bound U(b), not by counting (R02 item 4).

## L1.1 Exact decomposition along the residual factor direction (one global factor + block-local part)

**Lemma U(a).** Let Σ = λλᵀ + Ψ with Ψ ≻ 0 block-diagonal with respect to a partition 𝒢 of [p] (λ arbitrary). On a
probability space carrying independent ξ₀ ~ N(0, 1) and ζ ~ N(0, Ψ), put γ := λξ₀ + ζ (so γ ~ N(0, Σ)). For
T ⊆ [p], l ∉ T, U := T ∩ g(l), define

  ψ_{l|U} := Ψ_ll − Ψ_{lU}Ψ_UU⁻¹Ψ_{Ul},   Ξ_{l,U} := (ζ_l − Ψ_{lU}Ψ_UU⁻¹ζ_U)/√ψ_{l|U},
  λ̃_{l|U} := λ_l − Ψ_{lU}Ψ_UU⁻¹λ_U,   s_T := λ_TᵀΨ_TT⁻¹λ_T,   W_T := (ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T)/√(1 + s_T)

(empty-set conventions, R02 item 3: only sums/products over empty index sets vanish; explicitly c_∅ = 0, s_∅ = 0,
W_∅ = ξ₀, ψ_{l|∅} = Ψ_ll, λ̃_{l|∅} = λ_l, Ξ_{l,∅} = ζ_l/√Ψ_ll; Ψ_TT⁻¹ is block-diagonal with blocks Ψ_{T_gT_g}⁻¹,
T_g := T ∩ g). Then
Ξ_{l,U} ~ N(0, 1), W_T ~ N(0, 1), Ξ_{l,U} ⊥ W_T (independent), and

  Z^Σ_{T,l}(γ) = [√ψ_{l|U} Ξ_{l,U} + (λ̃_{l|U}/√(1 + s_T)) W_T] / √(ψ_{l|U} + λ̃²_{l|U}/(1 + s_T)).          (1.1)

*Proof.* Work in L² of the probability space. 𝓗_T := span{γ_j : j ∈ T} ⊆ 𝓚_T := span{ξ₀, ζ_j : j ∈ T}, because
γ_j = λ_jξ₀ + ζ_j. Cov(ξ₀, ζ_T) = diag(1, Ψ_TT) ≻ 0 and Σ_TT ⪰ Ψ_TT ≻ 0, so dim 𝓚_T = |T| + 1 and dim 𝓗_T = |T|;
𝓚_T ⊖ 𝓗_T is one-dimensional. For jointly Gaussian centred variables the conditional expectation equals the L²
projection, so Z^Σ_{T,l}(γ) = (γ_l − P_{𝓗_T}γ_l)/‖γ_l − P_{𝓗_T}γ_l‖_{L²}. Decompose

  γ_l − P_{𝓗_T}γ_l = (γ_l − P_{𝓚_T}γ_l) + (P_{𝓚_T}γ_l − P_{𝓗_T}γ_l),

an orthogonal sum (the first term is ⊥ 𝓚_T ⊇ 𝓗_T, the second lies in 𝓚_T ⊖ 𝓗_T).
*First term.* P_{𝓚_T}γ_l = λ_lξ₀ + P_{𝓚_T}ζ_l, and ζ_l is uncorrelated with ξ₀ and with ζ_j for j ∉ g(l) (Ψ block-
diagonal), so P_{𝓚_T}ζ_l = P_{span(ζ_U)}ζ_l = Ψ_{lU}Ψ_UU⁻¹ζ_U. Hence γ_l − P_{𝓚_T}γ_l = ζ_l − Ψ_{lU}Ψ_UU⁻¹ζ_U
= √ψ_{l|U}Ξ_{l,U}, with variance ψ_{l|U} > 0.
*Second term.* Let ω_T := ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T and c := (1 + s_T)⁻¹Ψ_TT⁻¹λ_T. Then cᵀγ_T = (1 + s_T)⁻¹(s_Tξ₀ +
λ_TᵀΨ_TT⁻¹ζ_T) ∈ 𝓗_T and ξ₀ − cᵀγ_T = (1 + s_T)⁻¹ω_T. For j ∈ T, E[ω_Tγ_j] = λ_j − (λ_TᵀΨ_TT⁻¹Ψ_{Tj}) = λ_j − λ_j = 0,
so ω_T ⊥ 𝓗_T, ω_T ∈ 𝓚_T, and ω_T ≠ 0 (Var ω_T = 1 + s_T ≥ 1). Thus 𝓚_T ⊖ 𝓗_T = span(ω_T) and W_T = ω_T/√(1 + s_T)
is its unit vector. The second term is E[γ_lW_T]W_T with
  E[γ_lW_T] = (λ_l − λ_TᵀΨ_TT⁻¹Ψ_{Tl})/√(1 + s_T) = λ̃_{l|U}/√(1 + s_T),
because Ψ_{Tl} vanishes outside U and (Ψ_TT⁻¹λ_T)_U = Ψ_UU⁻¹λ_U (block-diagonality).
*Assembly.* The two terms are orthogonal, so the innovation variance is ψ_{l|U} + λ̃²_{l|U}/(1 + s_T), which gives
(1.1). Ξ_{l,U} ⊥ 𝓚_T ∋ W_T and both are Gaussian, hence independent. ∎

**Interpretation (route A).** The innovation of x_l given x_T has an idiosyncratic part, which depends on T only
through T ∩ g(l) (at most p·2^{γ̄−1} distinct standard normals over all (T, l)), and one factor part along the
residual factor variable W_T (one normal per T, shared by all l). This is the "Pythagorean split along the residual
factor direction"; the direction count is controlled by the groups and by k = 1, not by the size of the lattice.

## L1.2 Deterministic bound

**Lemma U(b).** In the setting of U(a), let c_min := min{λ_VᵀΨ_VV⁻¹λ_V : ∅ ≠ V ⊆ g ∈ 𝒢} and assume c_min > 0. Put
κ'_{l,U} := |λ̃_{l|U}|/√ψ_{l|U}, κ' := max κ'_{l,U}, κ := κ'/√c_min (= κ(Σ) of STATEMENT §2), and for groups g,
Q_g := ζ_gᵀΨ_gg⁻¹ζ_g. Notation (R02 item 1): κ = κ(λ, Ψ, 𝒢) is representation-dependent; κ'_* := max_{l,U}κ'_{l,U}
= κ√c_min (written κ' below) and κ'_bd := κ̄√c_min ≥ κ'_* whenever κ ≤ κ̄. Note c_min = min_j λ_j²/Ψ_jj (variational
monotonicity with λ in place of ζ) and, in the correlation class, c_min ≤ (1 − ψ₀)/ψ₀, so κ'_bd ≤ κ̄/√ψ₀. For T ≠ ∅
let 𝒢(T) := {g : T ∩ g ≠ ∅}, h_T := |𝒢(T)|. Then for every T ⊆ [p], l ∉ T:

  |Z^Σ_{T,l}(γ)| ≤ |Ξ_{l,U}| + κ'|ξ₀|/(1 + s_T) + κ√( Σ_{g∈𝒢(T)} Q_g / h_T )   (the whole last summand is defined
  as 0 if T = ∅).                                                                                              (1.2)

*Proof.* Write (1.1) as (αΞ + βW)/√(α² + β²), α = √ψ_{l|U} > 0, β = λ̃_{l|U}/√(1 + s_T). Since √(α² + β²) ≥ α,
|Z| ≤ |Ξ| + (|β|/α)|W| = |Ξ| + κ'_{l,U}|ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T|/(1 + s_T). By block-diagonality,
λ_TᵀΨ_TT⁻¹ζ_T = Σ_{g∈𝒢(T)} λ_{T_g}ᵀΨ_{T_gT_g}⁻¹ζ_{T_g}; by Cauchy–Schwarz in the inner product ⟨x, y⟩ = xᵀΨ_{T_gT_g}⁻¹y,
each summand is at most √(s_{T_g}) √(q_{T_g}) in absolute value, with s_{T_g} := λ_{T_g}ᵀΨ_{T_gT_g}⁻¹λ_{T_g},
q_{T_g} := ζ_{T_g}ᵀΨ_{T_gT_g}⁻¹ζ_{T_g}. Monotonicity: for V ⊆ g, q_V = max_{c∈ℝ^V}(2cᵀζ_V − cᵀΨ_VVc) ≤
max_{c∈ℝ^g}(2cᵀζ_g − cᵀΨ_gg c) = Q_g (extend c by zeros). Cauchy–Schwarz over g and s_T = Σ_g s_{T_g}:
|λ_TᵀΨ_TT⁻¹ζ_T| ≤ √s_T · √(Σ_{𝒢(T)} Q_g). Each nonempty T_g has s_{T_g} ≥ c_min, so s_T ≥ c_min h_T and
√s_T/(1 + s_T) ≤ 1/√s_T ≤ 1/√(c_min h_T). Combine, and use κ'_{l,U}/√c_min ≤ κ. ∎

## L1.3 Probability bounds

**Lemma U(c).** In the setting of U(b), let every group have size ≤ γ̄, let G := |𝒢| ≤ p, and fix n ≥ 16 (so
log log n > 0). There is an event E_U(n) with P(E_U(n)ᶜ) ≤ 3/log n on which, for every T ⊆ [p] and l ∉ T,

  |Z^Σ_{T,l}(γ)| ≤ √(2 log(p 2^{γ̄}) + 2 log log n) + κ'√(2 log log n) + κ √(a_{h_T})            (1.3)

(the whole size-dependent summand is defined as 0 for T = ∅, without evaluating its logarithm), where for 1 ≤ h ≤ G,
with r_h := (2 log(h + 1) + log log n)/h,
  a_h := 2 log(eG/h) + 2r_h + γ̄ + 2√(γ̄ (log(eG/h) + r_h)).
In particular, since G ≤ p and h_T ≥ |T|/γ̄, for T ≠ ∅

  √(a_{h_T}) ≤ √(2 log(e γ̄ p/|T|)) + ϱ_n,  ϱ_n := √(2(2 log 2 + log log n) + γ̄ + 2√(γ̄(log(e γ̄ p) + 2 log 2 + log log n))),

and ϱ_n = O((log p)^{1/4} + (log log n)^{1/2}); explicitly, with ℓ := log log n ≥ 1 and b := 2 log 2 + ℓ,
ϱ_n ≤ √(2b) + √γ̄ + √2 γ̄^{1/4}[log(eγ̄p) + b]^{1/4} ≤ C(γ̄)[(log p)^{1/4} + ℓ^{1/2}] (n ≥ 16; γ̄ fixed is material).

*Proof.* (i) For each (l, U), U ⊆ g(l) ∖ {l}, Ξ_{l,U} ~ N(0, 1); there are at most p2^{γ̄−1} such pairs. With
t² := 2 log(p2^{γ̄−1}) + 2 log log n ≥ 2/π and P(|N(0,1)| > t) ≤ √(2/π)e^{−t²/2}/t ≤ e^{−t²/2}, the union bound gives
P(max|Ξ_{l,U}| > t) ≤ 1/log n; and t ≤ √(2 log(p2^{γ̄}) + 2 log log n).
(ii) P(|ξ₀| > √(2 log log n)) ≤ 1/log n (same tail bound; 2 log log n ≥ 2/π for n ≥ 16).
(iii) The (Q_g)_g are independent (ζ_g independent across groups, Ψ block-diagonal) with Q_g ~ χ²_{|g|}. For a set 𝒥
of h groups, Σ_𝒥 Q_g ~ χ²_D with D ≤ hγ̄. Laurent–Massart (2000, Lemma 1; as cited in PXN lemmas/CR_corr_tails.md):
P(χ²_D ≥ D + 2√(Dx) + 2x) ≤ e^{−x}; the threshold is increasing in D, so it may be replaced by hγ̄ + 2√(hγ̄x) + 2x.
Take x_h := log C(G, h) + 2 log(h + 1) + log log n and union over 𝒥 and h: the failure probability is at most
Σ_{h≥1}(h + 1)^{−2}/log n ≤ 1/log n. On the complement, using log C(G,h) ≤ h log(eG/h),
(1/h)Σ_𝒥 Q_g ≤ γ̄ + 2√(γ̄ x_h/h) + 2x_h/h ≤ a_h.
Let E_U(n) be the intersection of the three events; then (1.2) gives (1.3). For the second display:
√(a + b) ≤ √a + √b with a = 2 log(eG/h), and log(eG/h_T) ≤ log(e γ̄ p/|T|), r_h ≤ 2 log 2 + log log n. ∎

## L1.4 Perturbation: approximate factor Gram (fixed designs) and iid rows

**Lemma U(d).** Let Σ ⪰ ψ₀I be a correlation matrix, R a correlation matrix with ‖R − Σ‖_op ≤ δ ≤ ψ₀/4, x ~ N(0, R),
and γ := Σ^{1/2}R^{−1/2}x (so γ ~ N(0, Σ)). Then, for every T ⊆ [p] and l ∉ T,

  |Z^R_{T,l}(x) − Z^Σ_{T,l}(γ)| ≤ L_ψ δ ‖x‖,   L_ψ := C₂ + 2C₃/ψ₀,                                               (1.4)

with m := 3ψ₀/4, B := m^{−1/2}, C₂ := (1 + B)(3 + B²)/(2m^{3/2}), C₃ := (1 + B)/√m (R02 item 2),

and P(‖x‖² > 5(p + 1)u) ≤ e^{−u} for u ≥ 1.

*Proof.* λ_min(R) ≥ 3ψ₀/4. For M ∈ {R, Σ}: v_M ≥ λ_min(M) (Schur complement); c_MᵀM_TTc_M ≤ M_ll = 1, so
‖c_M‖² ≤ 1/λ_min(M) ≤ 4/(3ψ₀). (i) c_R − c_Σ = R_TT⁻¹[(R − Σ)_{Tl} − (R − Σ)_TTc_Σ], so ‖c_R − c_Σ‖ ≤
(4/(3ψ₀))δ(1 + ‖c_Σ‖). (ii) v_M = min_c (e_l − ι_Tc)ᵀM(e_l − ι_Tc) (minimiser c_M), so
v_R ≤ v_Σ + δ(1 + ‖c_Σ‖²) and v_Σ ≤ v_R + δ(1 + ‖c_R‖²): |v_R − v_Σ| ≤ δ(1 + 4/(3ψ₀)). (iii) Hence
‖a_R − a_Σ‖ ≤ ‖c_R − c_Σ‖/√v_R + (1 + ‖c_Σ‖)·|v_R − v_Σ|/(√(v_Rv_Σ)(√v_R + √v_Σ)) ≤ C₂(ψ₀)δ, and
‖a_Σ‖ ≤ (1 + ‖c_Σ‖)/√v_Σ ≤ C₃(ψ₀). (iv) ‖x − γ‖ = ‖(R^{1/2} − Σ^{1/2})R^{−1/2}x‖ ≤ ‖R − Σ‖/(√λ_min(R) + √λ_min(Σ)) ·
‖x‖/√λ_min(R) ≤ (2δ/ψ₀)‖x‖ (for PD A, B: ‖A^{1/2} − B^{1/2}‖ ≤ ‖A − B‖/(√λ_min(A) + √λ_min(B))). (v)
|a_Rᵀx − a_Σᵀγ| ≤ ‖a_R − a_Σ‖‖x‖ + ‖a_Σ‖‖x − γ‖ ≤ (C₂ + 2C₃/ψ₀)δ‖x‖ =: L_ψδ‖x‖. The norm bound: ‖x‖² = wᵀRw with
w ~ N(0, I); Laurent–Massart's weighted form gives P(wᵀRw ≥ tr R + 2√(tr(R²)u) + 2‖R‖u) ≤ e^{−u}; tr R = p,
‖R‖ ≤ tr R = p, tr R² ≤ ‖R‖ tr R ≤ p², so the threshold is ≤ p + 2p√u + 2pu ≤ 5(p + 1)u for u ≥ 1. ∎

Note that ‖Σ‖_op (≈ p λ̄² for a pervasive factor) does not enter L_ψ: only the unit diagonal and λ_min are used.

## L1.5 Consequence used downstream

**Corollary U.** Let X satisfy (AG) (STATEMENT §3) with Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄), and let g = Xᵀε/(σ√(n−1)). Let E_n =
E_n(X, ε) be the original-space event that the following inequality holds for every T ⊆ [p] and l ∉ T (with κ' :=
κ'_bd); then P(E_n | X) ≥ 1 − 4/log n on {δ_n ≤ ψ₀/4} (exact Gram: ≥ 1 − 3/log n):

  |Z_{T,l}| ≤ √(2 log(p 2^{γ̄}) + 2 log log n) + κ'√(2 log log n) + κ̄ (√(2 log(e γ̄ p/|T|)) + ϱ_n)·1{T ≠ ∅}
            + L_ψ δ_n √(5(p + 1) log log n).

*Proof.* (0.1), U(d) with R = R̂, x = g (u = log log n ≥ 1 for n ≥ 16), and U(c) applied to the coupled vector. Fix
X with δ_n ≤ ψ₀/4 and put γ := Σ_n^{1/2}R̂^{−1/2}g. On an enlarged space carrying an independent V ~ N(0, 1), with
b := Σ_n⁻¹λ, set ξ₀ := bᵀγ + √(1 − λᵀΣ_n⁻¹λ)V and ζ := γ − λξ₀ (1 − λᵀΣ_n⁻¹λ > 0 since Ψ ≻ 0). Given X these are
jointly Gaussian with Var ξ₀ = 1, Cov ζ = Ψ, Cov(ξ₀, ζ) = 0, and γ = λξ₀ + ζ exactly; the marginal law of (X, ε) is
unchanged. If A_n is the intersection of the latent U(c) event and the norm event ‖g‖² ≤ 5(p + 1) log log n, then
A_n ⊆ E_n, so P(E_n | X) = P_enl(E_n | X) ≥ P_enl(A_n | X) ≥ 1 − 4/log n. No claim is made that the latent event
belongs to the original σ-field (R02 item 5). Random designs: apply conditionally on X on the design event, then
integrate. ∎

Under (AG), L_ψδ_n√(5(p + 1) log log n) → 0.
