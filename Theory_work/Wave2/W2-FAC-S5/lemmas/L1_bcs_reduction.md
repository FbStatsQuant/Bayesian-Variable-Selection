# L1 — Block compound symmetry: exact two-level reduction of the score and of every LS0 move

Status: **PROVED-CHECKED** (Tier 1: lemma checks, mid-point CONTINUE, sweep fixed, council round 2 passed — R09 Sol 8.8, R10 Opus 8.8, all gates PASS); lemma check R02 (Codex Sol high, reviews/R02_L1L2L3_check_sol.md): FAILED as
written (item 1: the leakage error rate) — repaired here per R02's fix (two-term ε bound; R02_disposition.md).
Falsification numerics: numerics/l1_identities.py → l1_identities_out.txt (400 generated random BCS instances with
variable group sizes, 361 retained after the |T| ≥ 2 filter, every retained j ∈ T: normal equation, residual decomposition, variance formula and independence exact to
≤ 1.5·10⁻¹⁴; the bound |τ| ≤ |A| + κ₀|e| never violated; these test L1.3 only — the field `score_tau` is unused);
numerics/l1_leak.py → l1_leak_out.txt (exact reconstruction t̃ = (σ√(n−1)/s)(τ + ε); the signal-leakage component
√(n−1)σ_j/(σ√ṽ), computed stably as σ_j = a⁻¹β̃ᵀϑ^R, is O(n^{−3/2}) and below its bound √k‖ϑ‖√(n−1)/(adσ√ṽ); the ratio of
the total |ε| to the two-term bound is reported);
numerics/bcs_selftest_out.txt (closed form = FACB's general exact-Gram scanner: every flip gain and the best exhaustive
swap gain, 5 instances, to ≤ 9·10⁻⁷ absolute at n ≤ 10⁸);
numerics/S3_summary.txt (exact deletion gain = Δ_k − ½τ² up to ≤ 1.8·10⁻³ log n along the 15 deletion paths with
n ≥ 10⁶; 18 paths in total, the three n = 10⁴ paths have errors up to 0.043 log n; R06 item 6).

Setting: STATEMENT §1–2 (G, BCS, θ). a := n² − 1, a′ := n − 1. Throughout T ⊆ [p], k := |T|.

## L1.0 Sign flips
Exactly FACB L1.0 (the argument uses only G_A ↦ Υ_AG_AΥ_A, z_A ↦ Υ_Az_A): every score, block table, start-mode
probability and LS0 scan is unchanged by Υ_n. We take Υ_n = I and write ϑ for the sign-corrected truth coefficients.

## L1.1 Data representation
As FACB L1.1 with Σ in place of the CS matrix (the argument there uses only XᵀX = (n − 1)Σ, Σ ≻ 0, Xᵀ1 = 0):
g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ), r := ‖(C − P_X)ε‖²/σ² ~ χ²_{n−1−p} independent of g, ‖e‖² = σ²(gᵀΣ⁻¹g + r) (e := Cε),
z := Xᵀy = [(n − 1)Σθ* + σ√(n − 1) g]/s, yᵀy = n − 1, (n − 1)s² = (n − 1)θ*ᵀΣθ* + 2σ√(n − 1)θ*ᵀg + ‖e‖².
Under (BCS) we may (enlarging the probability space) write g_j = h + y_j, h := √ρ_b η, y_j := √b ζ_{g(j)} + √d ξ_j with
η, (ζ_g)_g, (ξ_j)_j iid N(0, 1), independent of r: the covariance of the right side is ρ_b11ᵀ + ⊕(bJ + dI) = Σ.

## L1.2 Algebra of Σ_TT
For T ⊆ [p] put U_g := T ∩ G_g, u_g := |U_g|. Then Σ_TT = ρ_b11ᵀ + ⊕_g(bJ_{u_g} + dI_{u_g}).
(a) λ_min(Σ_TT) ≥ d for nonempty T (Σ_TT − dI is positive semidefinite). Conventions for T = ∅ (R06 item 17): empty
inverse products and quadratic forms are 0, det H_∅ = det(G_∅ + I) = 1, quad_∅ = 0, and a maximum over no occupied
groups is 0.
(b) **Inverse M-matrix.** With M := ⊕(dI + bJ_{u_g}), M⁻¹ = ⊕ d⁻¹(I − γ_{u_g}J), γ_u := b/(d + ub), and
Σ_TT⁻¹ = M⁻¹ − ρ_bM⁻¹11ᵀM⁻¹/(1 + ρ_b1ᵀM⁻¹1), M⁻¹1 = (φ_g1)_g, φ_g := 1/(d + u_gb) > 0. Off-diagonal entries:
within a group −γ_u/d − ρ_bφ_g²/(1 + ρ_bΣ_gu_gφ_g) < 0; across groups −ρ_bφ_gφ_{g′}/(1 + ρ_bΣu_gφ_g) < 0. Hence for
distinct l, i ∉ U: Cov(x_l, x_i | x_U) > 0 (population conditional covariances, Σ-scale). *Proof:* with W := U ∪ {l, i},
the conditional covariance matrix of (l, i) given U is the inverse of the {l, i} block of Σ_WW⁻¹; that block has a
negative off-diagonal entry (W is again of BCS form, apply the display), and the inverse of a positive definite 2 × 2
matrix with negative off-diagonal has positive off-diagonal. ∎
(c) Σ̃ := Σ + a⁻¹I is again of BCS form with d replaced by d̃ := d + 1/a (so (a), (b) hold for Σ̃ with d̃ ≥ d), and
H_T = (n + 1)G_T + I = aΣ̃_TT, G_T + I = a′Σ_TT + I.

## L1.3 Gaussian conditioning identities (noise level)
Fix T and j ∈ [p]; put R := T ∖ {j}, U := R ∩ G_{g(j)}, u := |U|, c_u := d/(ub + d), s_u² := d(d + (u + 1)b)/(d + ub),
κ₀ := (1 − ρ_b)^{−1/2}. All conditional expectations are Gaussian linear predictions under N(0, Σ).
(i) **Global error.** e_R := h − E[h | g_R] satisfies, with ω_g := u_g/(u_gb + d) and ȳ_g the mean of y over U_g
(groups with u_g ≥ 1; computed on R), the normal equation e_R(1/ρ_b + Σ_gω_g) = h/ρ_b − Σ_gω_gȳ_g. In particular e_R is
a convex combination of h and of the −ȳ_g, so |e_R| ≤ |h| + max_g|ȳ_g| (R = ∅: e_∅ = h). V_R := Var(e_R) = 1/(1/ρ_b + Σ_gω_g).
*Proof:* given h, the observed group means m_g := h + ȳ_g are independent N(h, b + d/u_g) = N(h, 1/ω_g) and sufficient
for h in g_R (R06 item 16); the
posterior of h (prior N(0, ρ_b)) has mean Σω_g(h + ȳ_g)/(1/ρ_b + Σω_g) and variance V_R; rearrange. ∎
(ii) **Residual decomposition.** r_j(T) := g_j − E[g_j | g_R] = a_j(U) + c_u e_R with a_j(U) := y_j − (1 − c_u)ȳ_U
(ȳ_∅ := 0); a_j(U) ~ N(0, s_u²) and a_j(U) is independent of (h, g_R); v_j := Var(g_j | g_R) = s_u² + c_u²V_R.
*Proof:* given (h, g_R), group g(j) is independent of the other groups, and within it y_j given y_U (exchangeable,
covariance bJ + dI) has mean (ub/(ub + d))ȳ_U and variance s_u²; so E[g_j | h, g_R] = h + (1 − c_u)ȳ_U and a_j(U) is the
corresponding prediction error, independent of (h, g_R). With m_U := h + ȳ_U (the mean of g over U, g_R-measurable
when u ≥ 1; when u = 0 its coefficient 1 − c_0 vanishes), E[g_j | h, g_R] = c_uh + (1 − c_u)m_U, so
E[g_j | g_R] = c_uE[h | g_R] + (1 − c_u)m_U and g_j − E[g_j | g_R] = (h + y_j) − c_uE[h | g_R] − (1 − c_u)(h + ȳ_U)
= a_j(U) + c_u(h − E[h | g_R]). The variance follows from the independence of a_j(U) and e_R. ∎
(iii) **Standardised statistics.** τ_j(T) := r_j(T)/√v_j, A_j(U) := a_j(U)/s_u ~ N(0, 1). Since c_u/s_u =
√(d/((ub + d)(d + (u + 1)b))) is decreasing in u with value κ₀ at u = 0, and √v_j ≥ s_u:
  |τ_j(T)| ≤ |A_j(U)| + κ₀|e_R|.   (L1.3.1)
For j ∉ T the same holds with R = T (τ_j(T) is then the statistic of adding j to T).
(iv) **Rotation identity** (any Gaussian vector, any T, l ∉ T, j ∈ T): with Φ(T) := g_TᵀΣ_TT⁻¹g_T,
Φ(T) − Φ(T ∖ j) = τ_j(T)², Φ(T ∪ l) − Φ(T) = τ_l(T)², and τ_l(T ∖ j)² = τ_l(T)² + τ_j(T)² − τ_j(T ∪ l)². (Not used in the
Tier-1 proofs; recorded for the frontier.)

## L1.4 Exact score increments
Notation: quad_T := z_TᵀH_T⁻¹z_T (so Q_T = (n − 1) − n quad_T), H_T := (n + 1)G_T + I = aΣ̃_TT.
For T and j ∈ T, R := T ∖ {j} (Schur complement): quad_T − quad_R = t̃_j²/a with
t̃_j := (z_j − β̃ᵀz_R)/√ṽ_j, β̃ := Σ̃_RR⁻¹Σ̃_Rj = Σ̃_RR⁻¹Σ_Rj, ṽ_j := Σ̃_jj − Σ_jRβ̃. Additions of l ∉ T are the same formula at
T ∪ {l}; a swap (j out, l in) is F(T ∖ j ∪ l) − F(T) = [F(T ∖ j) − F(T)] + [F(T ∖ j ∪ l) − F(T ∖ j)] exactly.
**Gains.** With ψ_T := 0.02 + Q_T, Q_T = (n − 1) − n quad_T, ν = 0.01 + n/2, L(T) := log det H_T − log det(G_T + I):
  G_del(j | T) := F(T ∖ j) − F(T) = Δ(T, j) − ν log(1 + n t̃_j²/(aψ_T)),
  G_add(l | T) := F(T ∪ l) − F(T) = −Δ(T ∪ l, l) − ν log(1 − n t̃_l²/(aψ_T)),
  Δ(T, j) := log[(2p − k)/k] + ½[L(T) − L(T ∖ j)]  (w(k − 1)/w(k) = (2p − k)/k).
**Size term.** If λ_1..λ_k are the eigenvalues of Σ_TT (all ≥ d), L(T) = Σ_i f(λ_i), f(λ) := log[(aλ + 1)/(a′λ + 1)] =
log(n + 1) + log(1 − n/((n + 1)(a′λ + 1))) ∈ [log(n + 1) − 2/((n − 1)d), log(n + 1)] once (n − 1)d ≥ 2. Hence
  |L(T) − L(T ∖ j) − log(n + 1)| ≤ 2k/((n − 1)d).   (L1.4.1)
(Under (P_α), α < 1, this is ≤ 2n^α/((n − 1)d) ≤ 4n^{α−1}/d → 0 uniformly in T; R06 item 3.)
**Signal and regularisation, j null and T ⊇ S₀ (so S₀ ⊆ R).** Write z_j − β̃ᵀz_R = ((n − 1)/s)·σ_j + (σ√(n − 1)/s)·ρ̃_j
with σ_j := (Σθ*)_j − β̃ᵀ(Σθ*)_R and ρ̃_j := g_j − β̃ᵀg_R. Since (Σθ*)_R = Σ_{R S₀}ϑ = Σ̃_{R S₀}ϑ − a⁻¹ϑ^R (ϑ^R := ϑ on S₀,
0 on R ∖ S₀) and Σ̃_{jR}Σ̃_RR⁻¹Σ̃_{R S₀} = Σ̃_{jS₀} = Σ_{jS₀} (j ∉ S₀): σ_j = a⁻¹β̃ᵀϑ^R, and ‖β̃‖ ≤ ‖Σ̃_RR⁻¹‖‖Σ_Rj‖ ≤
√k/d (entries of Σ are ≤ 1), so |σ_j| ≤ √k‖ϑ‖/(ad). With β := Σ_RR⁻¹Σ_Rj: β̃ − β = −a⁻¹Σ̃_RR⁻¹Σ_RR⁻¹Σ_Rj, ‖β̃ − β‖ ≤
√k/(ad²), so |ρ̃_j − r_j(T)| ≤ k·max_i|g_i|/(ad²) and |ṽ_j − v_j| ≤ 1/a + k/(ad²); v_j ≥ d.
Consequently, with G_n^obs := max_i|g_i|, for j null and T ⊇ S₀, t̃_j = (σ√(n − 1)/s)·(τ_j(T) + ε_j) with the exact
  ε_j = (√(v_j/ṽ_j) − 1)τ_j(T) + (β − β̃)ᵀg_R/√ṽ_j + √(n − 1)σ_j/(σ√ṽ_j),
so (R02 item 1; the last, signal-leakage term is of order √k/n^{3/2}, not k/n²)
  |ε_j| ≤ C_d[(1 + |τ_j(T)| + G_n^obs)·k/n² + √k/n^{3/2}]  (C_d depends on d, ‖ϑ‖, σ),
and the same with k + 1 for an outside null l (statistic of adding l to T ⊇ S₀).
**The multiplier.** Put M_T := ν n(n − 1)σ²/(a s² ψ_T); then n t̃_j²/(aψ_T) = M_T(τ_j + ε_j)²/ν. For T ⊇ S₀: as in FACB
L1.5(b) (its proof uses only λ_min(G_T) ≥ (n − 1)d and μ ∈ span X_T), RSS_T/s² ≤ Q_T ≤ RSS_T/s² + 1 + 1/((n − 1)d), with
RSS_T = ‖e‖² − σ²Φ(T), 0 ≤ Φ(T) ≤ gᵀΣ⁻¹g. For every T (no S₀ condition) Q_T ≥ RSS_T/s² (same proof, lower bound only).
On the event E2 of L3 (‖e‖²/σ² ∈ [n − 1 − n^{2/3}, n − 1 + n^{2/3}], gᵀΣ⁻¹g ≤ p + n^{2/3}) and for p ≤ n^α, α < 1:
  M_T = ½(1 + η_T), |η_T| ≤ η_n := 8n^{−min(1−α, 1/3)}  for every T ⊇ S₀, n ≥ n₀(α, d, θ, σ).   (L1.4.2)
(Derivation: M_T = (n/2 + 0.01)(n/(n + 1))σ²/(s²ψ_T) and s²ψ_T ∈ [RSS_T + 0.02s², RSS_T + s²(1.02 + 1/((n − 1)d))] with
RSS_T/σ² ∈ [n − 1 − p − 2n^{2/3}, n − 1 + n^{2/3}], and s² = θ*ᵀΣθ* + σ² + O(n^{−1/3}) is bounded above and below on E2.)
**Elementary bounds** (x ≥ 0): x − x²/(2ν) ≤ ν log(1 + x/ν) ≤ x; −ν log(1 − x/ν) ≤ x + x²/ν for x ≤ ν/2. Hence
  G_del(j | T) ≥ Δ(T, j) − M_T(τ_j + ε_j)²,  G_add(l | T) ≤ −Δ(T ∪ l, l) + M_T(τ_l + ε_l)²(1 + 2M_T(τ_l + ε_l)²/ν),
the latter provided x := M_T(τ_l + ε_l)² ≤ ν/2 (R06 item 2; L4.2 gives x = O(log n)).
All later lemmas use only L1.2–L1.4.
