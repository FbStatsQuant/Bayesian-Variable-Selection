# L2 — Combes–Thomas bound and uniform conditional-covariance decay

Status: **PROVED (by this seat, unchecked)**. Check record: R02 (Codex gpt-6.1-sol high,
`reviews/R02_L1L2_check_sol.md`): VERIFIED (one NIT, applied in §L2.3).
Falsification numerics: `numerics/ct_check.py` → `numerics/ct_check_out.txt`.

## L2.1 Combes–Thomas lemma (finite matrices on integer positions)

**Lemma CT.** Let I be a finite index set and x : I → ℤ injective ("positions"); write d_ij := |x_i − x_j|. Let A be
a real symmetric matrix on I with spectrum in [α, β], α > 0, and |A_ij| ≤ K e^{−a d_ij} for all i ≠ j, with K > 0,
a > 0. Put
  u := [α/(4K) + 1/(e^a − 1)]⁻¹,   t* := a − log(1 + u)  (so 0 < t* < a).
Then for all i, j ∈ I:  |(A⁻¹)_ij| ≤ (2/α) e^{−t* d_ij}.

*Proof.* (i) *The constant.* For 0 ≤ t < a let S(t) := 2K Σ_{d≥1} e^{−ad}(e^{td} − 1) = 2K[1/(e^{a−t} − 1) − 1/(e^a − 1)],
continuous and strictly increasing on [0, a), S(0) = 0, S(t) → ∞ as t ↑ a. Solving S(t) = α/2 gives
1/(e^{a−t} − 1) = α/(4K) + 1/(e^a − 1) = 1/u, i.e. t = t*. Since 1/u > 1/(e^a − 1), u < e^a − 1, so t* > 0; and
u > 0 gives t* < a. Hence S(t*) = α/2.
(ii) *Conjugation.* Fix t ∈ {t*, −t*} and D := diag(e^{t x_i}). A_t := DAD⁻¹ has entries A_ij e^{t(x_i − x_j)}.
E := A_t − A has zero diagonal and |E_ij| = |A_ij| |e^{t(x_i − x_j)} − 1| ≤ K e^{−a d_ij}(e^{t* d_ij} − 1), using
|e^{s} − 1| ≤ e^{|s|} − 1 for real s.
(iii) *Schur test.* For every i, since x is injective at most two j satisfy d_ij = d for each d ≥ 1, so
Σ_j |E_ij| ≤ S(t*) = α/2; the same bound holds for column sums (the bound is symmetric in i, j). Hence
‖E‖₂ ≤ √(‖E‖₁‖E‖_∞) ≤ α/2.
(iv) *Inverse.* A is symmetric with λ_min(A) ≥ α, so ‖A⁻¹‖₂ ≤ 1/α and ‖A⁻¹E‖₂ ≤ ½. Thus A_t = A(I + A⁻¹E) is
invertible and ‖A_t⁻¹‖₂ ≤ ‖A⁻¹‖₂/(1 − ½) ≤ 2/α. Since A_t⁻¹ = DA⁻¹D⁻¹, its (i, j) entry is (A⁻¹)_ij e^{t(x_i − x_j)},
and every entry of a matrix is bounded in absolute value by its spectral norm. Choosing the sign of t so that
t(x_i − x_j) = t* d_ij gives |(A⁻¹)_ij| e^{t* d_ij} ≤ 2/α. ∎

Remarks. (1) β is not used: only the lower spectral bound and the off-diagonal decay matter. (2) The bound is
uniform in |I| and in the particular positions (only injectivity into ℤ is used). (3) Diagonal entries satisfy the
sharper |(A⁻¹)_ii| ≤ 1/α.

## L2.2 Uniform conditional decay for the class LOC

**Definition (class LOC(c, C, K, a)).** A unit-diagonal p × p covariance matrix Σ with spectrum in [c, C]
(0 < c ≤ 1 ≤ C < ∞) for which there is a bijection π : [p] → [p] such that **either** (LOC-Σ) |Σ_jk| ≤ K e^{−a|π(j) − π(k)|}
for j ≠ k, **or** (LOC-Θ) the precision Θ := Σ⁻¹ satisfies |Θ_jk| ≤ K e^{−a|π(j) − π(k)|} for j ≠ k. Write
d(j, k) := |π(j) − π(k)|. For a sequence Σ_n the constants (c, C, K, a) are fixed; π = π_n may vary with n.

**Lemma CD (conditional decay).** Let Σ ∈ LOC(c, C, K, a) and W ~ N(0, Σ). Define
  under (LOC-Σ): t₁ := t*(α = c, K, a), K₁ := 2/c;   under (LOC-Θ): t₁ := a, K₁ := K;
  t₂ := t*(α = 1/C, K₁, t₁),  K₂ := 2C.
Then for every U ⊆ [p] and all distinct j, k ∉ U:
  (a) |Cov(W_j, W_k | W_U)| ≤ K₂ e^{−t₂ d(j,k)};
  (b) c ≤ Var(W_j | W_U) ≤ 1, and every conditional covariance matrix Cov(W_V | W_U) (V ⊆ [p] ∖ U) has spectrum in
      [c, C];
  (c) under (LOC-Θ), Σ itself satisfies (LOC-Σ) with constants (2C, t*(1/C, K, a)); under (LOC-Σ), Θ satisfies
      (LOC-Θ) with (2/c, t*(c, K, a)).
The constants (K₂, t₂) depend only on (c, C, K, a), not on p, U, j, k or π.

*Proof.* Θ has spectrum in [1/C, 1/c]. Under (LOC-Σ), Lemma CT applied to Σ (positions π, α = c) gives
|Θ_jk| ≤ (2/c)e^{−t₁ d(j,k)} for all j, k; this is (c) second half. Under (LOC-Θ) the bound |Θ_jk| ≤ K e^{−a d} holds
by assumption for j ≠ k, and Lemma CT applied to Θ (α = 1/C) gives (c) first half. In both cases |Θ_jk| ≤ K₁e^{−t₁ d(j,k)}
for j ≠ k. Let V := [p] ∖ U. For Gaussian W, Cov(W_V | W_U) = (Θ_VV)⁻¹ (block inversion). Θ_VV is a principal
submatrix of Θ, so its spectrum lies in [1/C, 1/c] (Rayleigh quotients); its off-diagonal entries obey the same bound
with positions π|_V (still injective). Lemma CT with α = 1/C gives (a). For (b): the spectrum of (Θ_VV)⁻¹ lies in
[c, C]; in particular Var(W_j | W_U) = ((Θ_VV)⁻¹)_jj ≥ c, and Var(W_j | W_U) ≤ Var(W_j) = 1. For sub-vectors
V′ ⊆ V, Cov(W_{V′} | W_U) is a principal submatrix of Cov(W_V | W_U), so its spectrum lies in [c, C] too. ∎

## L2.3 Sufficient conditions (used in L4_families)

(i) **Banded Σ** (|Σ_jk| = 0 for d(j,k) > b) with spectrum in [c, C]: (LOC-Σ) holds with K := e^{ab} for any a > 0
(take a = 1, K = e^{b}), because |Σ_jk| ≤ 1 ≤ e^{b − d} for d ≤ b. (ii) **Banded Θ** (Gaussian Markov random field
on a line with range b, e.g. causal AR(b)) with spectrum of Σ in [c, C]: (LOC-Θ) with a = 1, K := e^{b}/c
(|Θ_jk| ≤ ‖Θ‖ ≤ 1/c). (iii) **Block-diagonal** Σ with blocks of size ≤ g, ordered consecutively by π: banded with
b = g − 1. (iv) **Stationary Toeplitz** Σ_jk = γ(|j − k|)/γ(0) with |γ(h)/γ(0)| ≤ K′ρ^h (ρ < 1) and spectrum in [c, C]:
(LOC-Σ) with a = log(1/ρ), K = K′ (normalisation aligned with L4 (c), C1-Opus-8). For AR(1) with parameter 0 < |ρ| < 1 (ρ = 0 is Σ = I: LOC with any fixed K, a > 0; sequences need fixed |ρ| bounded
away from 1 — no unit-root limits) [R02-5]: Σ_jk = ρ^{|j−k|}, spectrum in
[(1 − |ρ|)/(1 + |ρ|), (1 + |ρ|)/(1 − |ρ|)] (GROW L5 (P1)), K = 1, a = log(1/|ρ|).
