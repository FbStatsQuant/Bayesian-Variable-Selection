# L3 — Combes–Thomas in ℝ^d, conditional decay, and the ℓ¹ regression bound

Status: **PROVED (by this seat, unchecked)**. Model: APP `lemmas/L2_CT.md` (Lemma CT, CD; d = 1, integer positions;
R02 VERIFIED). Falsification numerics: `numerics/n4_nar_check.py` Part 1 → `numerics/n4_out.txt` (2-D grids,
exp(−‖Δ‖/φ), φ ∈ {0.8, 1.2, 2}; worst ratio |(A⁻¹)_ij|/bound over Σ and 29 random principal submatrices ≤ 0.32;
observed sup ‖β_A‖₁ ≤ 1.27; the printed "L0" there is a TRUNCATED (m ≤ 4000) lower approximation of the analytic L₀,
and the t* root search uses the truncated series — the numerics are a falsification probe of CT_d and sampled regression
norms only, not a certificate; the analytic proofs below are the certificate [R02-4]). Check record: R02 (Codex
gpt-6.1-sol high, `reviews/R02_L1L3_check_sol.md`): VERIFIED-WITH-AMENDMENTS; amendments 1, 4, 5 applied
(`reviews/R02_disposition.md`).

**Notation [R01-3].** In LOC_d(c, C, K, a) and Lemma CT_d the letter K is the decay-envelope constant (K_dec in
STATEMENT); the method's model-size cap is K_n = min(p, ⌊n/2⌋).

## L3.0 Sites and packing
A *site map* is x : I → ℝ^d (I finite) with ‖x_i − x_j‖ ≥ 1 for i ≠ j (Euclidean norm; d ≥ 1 fixed); d_ij := ‖x_i − x_j‖.
**Packing fact.** For every i and R > 0, #{j : d_ij < R} ≤ (2R + 1)^d; hence for every integer m ≥ 1,
#{j : m ≤ d_ij < m + 1} ≤ (2m + 3)^d.
*Proof.* The balls B(x_j, ½) are pairwise disjoint (separation ≥ 1); for d_ij < R they lie in B(x_i, R + ½). Comparing
volumes, the count is ≤ ((R + ½)/½)^d = (2R + 1)^d; for the shell take R = m + 1. ∎
(Integer positions on a line, d = 1, give #{j : d_ij = m} ≤ 2; the packing bound (2m+3) is weaker but sufficient.)

## L3.1 Lemma CT_d
Let A be real symmetric on I with λ_min(A) ≥ α > 0 (no upper spectral bound needed) [R07-14], and |A_ij| ≤ K e^{−a d_ij} for i ≠ j (K, a > 0). For
0 ≤ t < a put
  S(t) := K Σ_{m≥1} (2m + 3)^d e^{−(a−t)m}(1 − e^{−t(m+1)}).
S is finite, continuous and nondecreasing on [0, a), S(0) = 0, and S(t) → ∞ as t ↑ a. Let
t* = t*(α, K, a, d) := max{t ∈ [0, a) : S(t) ≤ α/2} ∈ (0, a). Then for all i, j ∈ I:  |(A⁻¹)_ij| ≤ (2/α)e^{−t*d_ij}.

*Proof.* (i) Each term is continuous, nondecreasing in t and the series converges uniformly on [0, a − ε] (terms
≤ K(2m + 3)^d e^{−εm}), giving finiteness, continuity, monotonicity and S(0) = 0; as t ↑ a, for any M the partial sum
up to M tends to K Σ_{m≤M}(2m + 3)^d(1 − e^{−a(m+1)}) ≥ K(1 − e^{−2a})Σ_{m≤M}(2m+3)^d, which is unbounded in M; so
S → ∞. Hence {S ≤ α/2} = [0, t*] with 0 < t* < a (continuity at 0 gives t* > 0).
(ii) Fix j and φ(y) := ‖y − x_j‖ (1-Lipschitz). D := diag(e^{t*φ(x_i)}), A_t := DAD⁻¹ (entries A_ik e^{t*(φ(x_i)−φ(x_k))}),
E := A_t − A. E_ii = 0, and for i ≠ k, |E_ik| ≤ |A_ik|(e^{t*|φ(x_i)−φ(x_k)|} − 1) ≤ K e^{−a d_ik}(e^{t*d_ik} − 1)
(|e^s − 1| ≤ e^{|s|} − 1, and |φ(x_i) − φ(x_k)| ≤ d_ik).
(iii) Schur test. For fixed i, group k by the shell m ≤ d_ik < m + 1 (m ≥ 1 since d_ik ≥ 1). On such a shell,
e^{−ad}(e^{t*d} − 1) = e^{−(a−t*)d}(1 − e^{−t*d}) ≤ e^{−(a−t*)m}(1 − e^{−t*(m+1)}). With the packing fact,
Σ_k |E_ik| ≤ S(t*) ≤ α/2; the bound is symmetric in (i, k), so column sums obey it too; ‖E‖₂ ≤ √(‖E‖₁‖E‖_∞) ≤ α/2.
(iv) ‖A⁻¹‖₂ ≤ 1/α, so A_t = A(I + A⁻¹E) is invertible with ‖A_t⁻¹‖₂ ≤ 2/α; A_t⁻¹ = DA⁻¹D⁻¹ has (i, j) entry
(A⁻¹)_ij e^{t*(φ(x_i)−φ(x_j))} = (A⁻¹)_ij e^{t*d_ij} (φ(x_j) = 0), and entries are bounded by the spectral norm. ∎
Remarks. No upper spectral bound is used. The bound is uniform in |I| and in the site map. Any norm on ℝ^d works with (2m+3)^d replaced by
the corresponding packing constant; we fix the Euclidean norm.

## L3.2 Class LOC_d and Lemma CD_d
**Definition.** LOC_d(c, C, K, a): unit-diagonal Σ on [p] with spectrum in [c, C] (0 < c ≤ 1 ≤ C) and a site map
x : [p] → ℝ^d (separation ≥ 1) such that either (LOC_d-Σ) |Σ_jk| ≤ K e^{−a d_jk} (j ≠ k), or (LOC_d-Θ) Θ := Σ⁻¹ obeys
|Θ_jk| ≤ K e^{−a d_jk} (j ≠ k). For sequences the constants are fixed; the site maps may vary with n.

**Lemma CD_d.** Let Σ ∈ LOC_d(c, C, K, a), W ~ N(0, Σ). Define
  (LOC_d-Σ): t₁ := t*(c, K, a, d), K₁ := 2/c;   (LOC_d-Θ): t₁ := a, K₁ := K;   t₂ := t*(1/C, K₁, t₁, d), K₂ := 2C.
Then for every U ⊆ [p] and distinct j, k ∉ U:
 (a) |Cov(W_j, W_k | W_U)| ≤ K₂e^{−t₂d_jk};
 (b) c ≤ Var(W_j | W_U) ≤ 1, and for every V ⊆ [p] ∖ U the conditional covariance matrix Cov(W_V | W_U) has
     spectrum in [c, C];
 (c) under (LOC_d-Θ), Σ obeys (LOC_d-Σ) with constants (2C, t*(1/C, K, a, d)); under (LOC_d-Σ), Θ obeys (LOC_d-Θ)
     with (2/c, t*(c, K, a, d)).
*Proof* [R02-1]. As APP L2_CT Lemma CD with Lemma CT replaced by Lemma CT_d. Under either branch, |Θ_jk| ≤ K₁e^{−t₁d_jk}
(j ≠ k): under (LOC_d-Σ) by CT_d applied to Σ (α = c), under (LOC_d-Θ) by assumption; this with CT_d applied to Θ
(α = 1/C) also gives (c). Let H := [p] ∖ U (the FULL unconditioned complement). For Gaussian W, block inversion gives
Cov(W_H | W_U) = (Θ_HH)⁻¹. Θ_HH is a principal submatrix of Θ: spectrum in [1/C, 1/c], off-diagonal entries
≤ K₁e^{−t₁d}, with the restricted (still separated) site map. CT_d (α = 1/C) gives (a) for j, k ∈ H, and the spectrum of
(Θ_HH)⁻¹ lies in [c, C]. For an arbitrary V ⊆ H, Cov(W_V | W_U) is a principal submatrix of Cov(W_H | W_U) (NOT (Θ_VV)⁻¹,
which would condition on H ∖ V as well), so by interlacing its spectrum lies in [c, C]; in particular Var(W_j | W_U) ≥ c,
and Var(W_j | W_U) ≤ Var(W_j) = 1. ∎

## L3.3 Lemma RB (ℓ¹ bound for population regression coefficients)
Let Σ ∈ LOC_d(c, C, K, a). Let (K_Σ, t_Σ) := (K, a) under (LOC_d-Σ) with t_Σ′ := t*(c, K, a, d), and under (LOC_d-Θ)
(K_Σ, t_Σ) := (2C, t*(1/C, K, a, d)) (CD_d(c)) with t_Σ′ := t*(c, 2C, t_Σ, d). For l ∈ [p] and A ⊆ [p] ∖ {l}, let
β_A(l) := Σ_AA⁻¹Σ_{Al} (coefficients of E[W_l | W_A] = W_Aβ_A(l)). Then
  |β_A(l)_v| ≤ (2/c)e^{−t_Σ′ d_lv}  (v ∈ A),    ‖β_A(l)‖₁ ≤ L₀ := (2/c) Σ_{m≥1}(2m + 3)^d e^{−t_Σ′ m} < ∞.
*Proof.* B := Σ_{A∪{l}} is a principal submatrix: spectrum in [c, C], off-diagonal entries ≤ K_Σe^{−t_Σ d}. Let
Ψ := B⁻¹. Block inversion gives β_A(l)_v = −Ψ_vl/Ψ_ll and Ψ_ll = 1/Var(W_l | W_A) ≥ 1. Lemma CT_d applied to B
(α = c, constants (K_Σ, t_Σ)) gives |Ψ_vl| ≤ (2/c)e^{−t_Σ′d_vl}. Sum over shells with the packing fact
(d_lv ≥ 1). ∎

## L3.4 Lemma TAIL (far conditioning)
Let Σ ∈ LOC_d, l ∈ [p], T ⊆ [p] ∖ {l}, r > 0, T′ := {v ∈ T : d_lv ≤ r}. Then
 (a) Var(E[W_l | W_T] − E[W_l | W_{T′}]) ≤ κ(r) := (K₂²/c) Σ_{m ≥ ⌊r⌋, m≥1} (2m + 3)^d e^{−2t₂m}, and κ(r) → 0 as r → ∞;
 (b) Var(W_l | W_{T′}) = Var(W_l | W_T) + Var(E[W_l | W_T] − E[W_l | W_{T′}]).
*Proof.* (b) e_T := W_l − E[W_l | W_T] is uncorrelated with every linear function of W_T, in particular with
D := E[W_l | W_T] − E[W_l | W_{T′}]; e_{T′} = e_T + D. (a) As in APP L3.6 Step 3: with V := W_{T∖T′} − E[W_{T∖T′} | W_{T′}],
D = Cov(e_{T′}, V)M⁻¹V, M := Cov(W_{T∖T′} | W_{T′}), so Var D = bᵀM⁻¹b ≤ ‖b‖²/c with b_v := Cov(W_l, W_v | W_{T′})
[R02-5: vector renamed]. By CD_d(b) (V = T ∖ T′ ⊆ [p] ∖ T′), λ_min(M) ≥ c; by CD_d(a), |b_v| ≤ K₂e^{−t₂d_lv} with d_lv > r for v ∈ T ∖ T′; group by shells m ≤ d_lv < m + 1
(m ≥ ⌊r⌋, m ≥ 1) and use the packing fact. κ(r) → 0 as the tail of a convergent series. ∎
