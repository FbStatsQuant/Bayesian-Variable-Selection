# L2 — Theorem MIS (iii): jointly Gaussian rows (Proposition P, Lemma GD)

Status (per claim): Proposition P — R02 VERIFIED, R04-requested wording (marginal-vector precision, fixed τ²) R05 VERIFIED;
GD(a) — R02 VERIFIED; GD(b) (optional) — R02 VERIFIED-WITH-AMENDMENTS (applied); Example E1 — added after R04, R05
VERIFIED-WITH-AMENDMENTS (applied). GD(b) uses one cited standard inequality (DS below). Sweep R06 fixes applied. Council pending.

Setting. Rows (x^r_{𝒞,i}, x^r_{𝓜,i}), i = 1..n, iid N(m, Σ), independent of ε ~ N_n(0, σ²I). Since ω = X^r_𝓜β_𝓜 depends
only on the omitted columns with β ≠ 0, we take 𝓜 := S₀ ∖ 𝒞 (the omitted *signal* columns) and Σ the covariance of the
**marginal** vector (x_𝒞, x_𝓜) (blocks Σ_𝒞𝒞, Σ_𝒞𝓜, Σ_𝓜𝓜); Θ in (c)–(d) is the inverse of this marginal Σ, **not** a block
of the precision of a larger vector containing inactive omitted variables (marginalising them out can create edges: R04's
example 𝒞 = {1}, omitted {2, 3}, β = (0,1,0), full precision with Θ₁₂ = 0 still gives γ₁ = 1/3). The block identities of
(a)–(c) also hold verbatim with any larger omitted set. Σ and m may depend on n (triangular array).

## Proposition P

(a) If Σ_𝒞𝒞 ≻ 0, then at each n the GR decomposition holds with
  γ = Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜,  a = (m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹m_𝒞)ᵀβ_𝓜,  τ² = β_𝓜ᵀ Σ_{𝓜·𝒞} β_𝓜,  Σ_{𝓜·𝒞} := Σ_𝓜𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹Σ_𝒞𝓜,
and ξ, given X^r_𝒞, has iid N(0, τ²) entries, independent of ε; ε′ = ε + ξ is N_n(0, σ_𝒞²I) and independent of X^r_𝒞.
Here τ² = τ_n² may depend on n through (Σ, β); GR in the sense of Theorem MIS (fixed τ²) holds iff τ_n² is constant —
an extra requirement, met in GD(a) (fixed parameters) and imposed in GD(b).
(b) β^𝒞 = β_𝒞 + γ = Σ_𝒞𝒞⁻¹ cov(x_𝒞, y), the population least-squares *slope with an intercept* of y on x_𝒞; for centred
rows (m = 0) it is Song–Liang's β₀ := argmin E(β_sᵀx_s − β*ᵀx)² (their model has no intercept; for non-centred predictors
their minimiser uses second moments and can differ: x, z iid N(1,1), candidate x, omitted z, y = z + ε gives slope 0 here
but E[xz]/E[x²] = ½ there — sweep R06 item 1)
(SL eq. (19), with their s = 𝒞); hence S₀^𝒞 = SL's s̃.
(c) If Σ ≻ 0 and Θ := Σ⁻¹ (blocks Θ_𝒞𝒞, Θ_𝒞𝓜, Θ_𝓜𝓜), then Σ_𝒞𝒞⁻¹Σ_𝒞𝓜 = −Θ_𝒞𝓜Θ_𝓜𝓜⁻¹ and Σ_{𝓜·𝒞} = Θ_𝓜𝓜⁻¹;
so γ = −Θ_𝒞𝓜Θ_𝓜𝓜⁻¹β_𝓜, τ² = β_𝓜ᵀΘ_𝓜𝓜⁻¹β_𝓜, and supp γ ⊆ {j ∈ 𝒞 : Θ_jk ≠ 0 for some k ∈ 𝓜}.
(d) One omitted variable k (𝓜 = {k}, β_k ≠ 0): γ = −(β_k/Θ_kk)Θ_𝒞k, so **supp γ = N_Θ(k) := {j ∈ 𝒞 : Θ_jk ≠ 0}**
(the neighbours of k in the Gaussian graph of (x_𝒞, x_k)); with several omitted variables only the inclusion in (c)
holds (weighted contributions can cancel); and
  S₀^𝒞 = [(S₀ ∩ 𝒞) ∖ N_Θ(k)] ∪ {j ∈ N_Θ(k) : β_j ≠ β_kΘ_jk/Θ_kk}.
Coefficient criterion: a candidate j that is **null in the full model** (β_j = 0) is in S₀^𝒞 iff Θ_jk ≠ 0, i.e. iff its
partial correlation with x_k given the other candidates is nonzero — whatever its marginal correlation (e.g.
cov(x_j, x_k) ≠ 0 with Θ_jk = 0 gives j ∉ S₀^𝒞; with a single candidate, marginal and partial correlation coincide). A
true candidate (β_j ≠ 0) stays in S₀^𝒞 unless it is cancelled. Membership in S₀^𝒞 yields selection only under (H-MIS),
in particular beta-min on β^𝒞.

*Intercept:* a = m_𝓜ᵀβ_𝓜 − m_𝒞ᵀγ (same as the display in (a)).

*Proof.* (a) Gaussian conditioning: the conditional law of x_{𝓜,i} given x_{𝒞,i} is
N(m_𝓜 + Σ_𝓜𝒞Σ_𝒞𝒞⁻¹(x_{𝒞,i} − m_𝒞), Σ_{𝓜·𝒞}); rows are independent, so given X^r_𝒞 the vectors
ζ_i := x_{𝓜,i} − m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹(x_{𝒞,i} − m_𝒞) are iid N(0, Σ_{𝓜·𝒞}) and their law does not depend on X^r_𝒞,
i.e. ζ is independent of X^r_𝒞. Then ω_i = x_{𝓜,i}ᵀβ_𝓜 = a + x_{𝒞,i}ᵀγ + ξ_i with ξ_i := ζ_iᵀβ_𝓜 iid N(0, τ²).
ε is independent of X^r (hence of (X^r_𝒞, ζ)), so given X^r_𝒞, ξ and ε are independent and ε + ξ ~ N_n(0, σ_𝒞²I),
a law free of X^r_𝒞. (b) cov(x_𝒞, y) = Σ_𝒞𝒞β_𝒞 + Σ_𝒞𝓜β_𝓜 (ε independent of x), so
Σ_𝒞𝒞⁻¹cov(x_𝒞, y) = β_𝒞 + γ. (c) From ΣΘ = I, the (𝒞, 𝓜) block: Σ_𝒞𝒞Θ_𝒞𝓜 + Σ_𝒞𝓜Θ_𝓜𝓜 = 0, so
Θ_𝒞𝓜 = −Σ_𝒞𝒞⁻¹Σ_𝒞𝓜Θ_𝓜𝓜; Θ_𝓜𝓜 ≻ 0 (principal block of Θ ≻ 0) is invertible, giving the first identity. The
(𝓜, 𝓜) block: Σ_𝓜𝒞Θ_𝒞𝓜 + Σ_𝓜𝓜Θ_𝓜𝓜 = I; substituting Θ_𝒞𝓜 gives Σ_{𝓜·𝒞}Θ_𝓜𝓜 = I. The support claim: the j-th
entry of Θ_𝒞𝓜v (v := Θ_𝓜𝓜⁻¹β_𝓜) is Σ_k Θ_jk v_k, zero if Θ_jk = 0 for all k ∈ 𝓜. (d) Specialise (c):
Θ_𝓜𝓜 = Θ_kk > 0 scalar, so γ_j = −β_kΘ_jk/Θ_kk, nonzero iff Θ_jk ≠ 0 (β_k ≠ 0). Then β^𝒞_j = β_j + γ_j: for
j ∉ N_Θ(k), β^𝒞_j = β_j; for j ∈ N_Θ(k), β^𝒞_j = β_j − β_kΘ_jk/Θ_kk. Coefficient criterion: if β_j = 0 then
β^𝒞_j = γ_j ≠ 0 iff Θ_jk ≠ 0. Partial correlation: for Θ ≻ 0, corr(x_j, x_k | all other variables of (x_𝒞, x_k)) =
−Θ_jk/√(Θ_jjΘ_kk), so Θ_jk ≠ 0 iff that partial correlation is nonzero. ∎

## Lemma GD (design hypotheses with probability → 1)

(a) **|𝒞| = p fixed** (SL's regime). Assume Σ_𝒞𝒞 ≻ 0 and m, Σ, β fixed in n, β^𝒞 ≠ 0. Let ρ_min := λ_min(corr(Σ_𝒞𝒞)) > 0,
φ₀² := ρ_min/2, g₀ := 1, s := |S₀^𝒞| ≥ 1, M := 2β^𝒞ᵀΣ_𝒞𝒞β^𝒞 + 1, κ := ½min_{j∈S₀^𝒞}Σ_jj(β^𝒞_j)² > 0, any A ≥ 1,
M_n := κnφ₀²/(σ_𝒞² log n). Let 𝒜_n be the set of candidate designs x with λ_min(R̂_𝒞(x)) ≥ φ₀²,
‖C x β^𝒞‖² ≤ Mn and min_{j∈S₀^𝒞} σ̂_j(x)²(β^𝒞_j)² ≥ κ. Then P(X^r_𝒞 ∈ 𝒜_n) → 1, and for n ≥ max(2p, n₃) every
x ∈ 𝒜_n satisfies (H-MIS) with these constants and BM-∞ with M_n → ∞. Hence Theorem MIS (ii) applies: with p_𝒞 fixed
and jointly Gaussian rows, 1 − π_𝒞(S₀^𝒞 | y) = O_P(√(log n/n)) under the joint law (S₀^𝒞 = SL's s̃ for centred rows) — the Song–Liang Corollary 2
conclusion, with a rate, for the shipped prior.

*Proof.* SLLN: the sample covariance and SDs converge a.s. to Σ_𝒞𝒞 and diag(Σ_𝒞𝒞)^{1/2}, so R̂_𝒞 → corr(Σ_𝒞𝒞),
(1/n)‖Cxβ^𝒞‖² → β^𝒞ᵀΣ_𝒞𝒞β^𝒞 and σ̂_j² → Σ_jj a.s.; λ_min is continuous; hence each defining inequality of 𝒜_n
(each has slack) holds eventually a.s., so P(𝒜_n) → 1. On 𝒜_n: R1 (s fixed; p ≤ n^A for n ≥ p; s ≤ K = p for
n ≥ 2p); R: ‖μ^𝒞‖² = ‖Cxβ^𝒞‖² ≤ Mn (μ^𝒞 = Xθ^𝒞 = CX^rβ^𝒞) and λ_min(R̂_{S₀^𝒞}) ≥ λ_min(R̂_𝒞) ≥ φ₀²
(interlacing, T03R Lemma I `PROOF.md:136`); SE_λ(j₀): every S₀^𝒞 ∪ J ⊆ 𝒞, same interlacing; SE_w(m♯_n; g₀):
λ_min(X_TᵀX_T) = (n − 1)λ_min(R̂_T) ≥ (n − 1)φ₀² ≥ 1 = g₀ for n ≥ n₃ := 1 + 1/φ₀²; BM-∞:
θ^𝒞_j² = σ̂_j²(β^𝒞_j)² ≥ κ, so θ^𝒞²_min nφ₀²/(σ_𝒞² log n) ≥ M_n → ∞. GR holds by Proposition P(a). ∎

(b) **Growing p_𝒞 ≤ n^A** (optional; conditional on the stated population assumptions). Assume, along n, besides
Σ_𝒞𝒞 ≻ 0 and **σ_𝒞² = σ² + τ² fixed in n** (inherited from GR; without it the claim is false — R02 counterexample: an
omitted Gaussian column of variance n² makes σ²_𝒞,n = 1 + n² and the BM ratio → 0): λ_min(Σ_TT) ≥ c_pop > 0 for every T ⊆ 𝒞 with |T| ≤ k_n :=
s + max(j₀, m♯_n); max_{j∈𝒞}Σ_jj ≤ C₀; β^𝒞ᵀΣ_𝒞𝒞β^𝒞 ≤ M₀; s = |S₀^𝒞| ≥ 1 fixed; and
n·min_{j∈S₀^𝒞}Σ_jj(β^𝒞_j)²/log n ≥ M′_n → ∞ (deterministic). Then with φ₀² := c_pop/(8C₀), g₀ := 1,
M := 2M₀ + 1, M_n := M′_nφ₀²/(2σ_𝒞²), let 𝒜_n be the set of candidate designs satisfying at that n the finite-n
inequalities of MIS (ii) (energy ≤ Mn, anchored normalised floor φ₀² on S₀^𝒞 ∪ J for |J| ≤ j₀, unnormalised floor
g₀ on S₀^𝒞 ∪ J for |J| ≤ m♯_n) and θ^𝒞²_min ≥ ½min_{S₀^𝒞}Σ_jj(β^𝒞_j)² (which gives the envelope M_n). Then
P(X^r_𝒞 ∈ 𝒜_n) → 1, the starting index being max(2s, ⌈1 + 1/φ₀²⌉, n₀(s, A, c_pop, C₀, M₀) (a single threshold depending on all fixed constants, including through k_n = s + max(j₀, m♯_n))); hence MIS (ii)–(iii) applies.

*Cited input (DS).* For an N × k matrix Z with iid N(0, 1) entries and N ≥ k, t ≥ 0:
P(s_min(Z) ≤ √N − √k − t) ≤ 2e^{−t²/2} (Vershynin 2012, *Introduction to the non-asymptotic analysis of random
matrices*, Cor. 5.35, printed two-sided form; Davidson–Szarek 2001, Thm II.13). We use the printed factor 2.
Standard; cited, not re-proved here.

*Proof.* Contrast coordinates: with U (n × N, UᵀU = I, UUᵀ = C), W := UᵀX^r_𝒞 has iid N(0, Σ_𝒞𝒞) rows
(X^r_𝒞 = 1m_𝒞ᵀ + ZΣ_𝒞𝒞^{1/2} with Z iid N(0,1), Uᵀ1 = 0, and UᵀZ has iid N(0,1) entries by orthogonal invariance of
each column's law). G_T := X_TᵀX_T = D̂_T⁻¹W_TᵀW_TD̂_T⁻¹ with D̂ = diag(σ̂_j), σ̂_j² = ‖w_j‖²/N.
(1) SDs: ‖w_j‖²/Σ_jj ~ χ²_N. By [P3] lem:chi(a) with x = (A + 2)log n and a union bound over p_𝒞 ≤ n^A columns,
with probability ≥ 1 − 2n^{−2}: N − 2√(Nx) ≤ ‖w_j‖²/Σ_jj ≤ N + 2√(Nx) + 2x for all j, so ½Σ_jj ≤ σ̂_j² ≤ 2Σ_jj
for n ≥ n₀(A).
(2) Sparse eigenvalues: for fixed T, |T| = k ≤ k_n, W_T has the law of Z_TΣ_TT^{1/2} (Z_T N × k iid N(0,1)), so
λ_min(W_TᵀW_T) ≥ λ_min(Σ_TT)s_min(Z_T)² ≥ c_pop s_min(Z_T)². With t_k := √(2(k log p_𝒞 + 2 log n)) and (DS), a union
bound over ≤ p_𝒞^k sets of each size 1 ≤ k ≤ min(p_𝒞, k_n) gives failure probability ≤ 2k_n n^{−2} → 0
(k_n = O(log n): j₀ fixed and m♯_n ≤ C_m log n by T03R E2(i), `PROOF.md:52`). On the complement,
s_min(Z_T) ≥ √N − √k_n − t_{k_n} ≥ √N/√2 for n ≥ n₀ (√k_n + t_{k_n} = O(log n)). Hence λ_min(W_TᵀW_T) ≥ c_popN/2 and,
with (1), λ_min(R̂_T) = λ_min(G_T)/N ≥ (c_pop/2)/(2C₀) ≥ φ₀² and λ_min(G_T) ≥ Nφ₀² ≥ 1 = g₀, for all |T| ≤ k_n.
This gives SE_λ(j₀), SE_w(m♯_n; g₀) and λ_min(R̂_{S₀^𝒞}) ≥ φ₀².
(3) Energy: ‖μ^𝒞‖² = ‖Wβ^𝒞‖² (μ^𝒞 in contrast coordinates), and Wβ^𝒞 ~ N_N(0, (β^𝒞ᵀΣ_𝒞𝒞β^𝒞)I_N); by
lem:chi(a), ‖Wβ^𝒞‖² ≤ 2NM₀ ≤ Mn with probability ≥ 1 − 1/n (n ≥ n₀).
(4) BM: by (1), θ^𝒞_j² = σ̂_j²(β^𝒞_j)² ≥ ½Σ_jj(β^𝒞_j)², so θ^𝒞²_min nφ₀²/(σ_𝒞² log n) ≥ M′_nφ₀²/(2σ_𝒞²) =: M_n → ∞.
(5) R1: p_𝒞 ≤ n^A, s fixed, s ≤ K eventually (K = min(p_𝒞, ⌊n/2⌋) ≥ s for n ≥ 2s, as p_𝒞 ≥ s).
Total failure probability ≤ 2n^{−2} + 2k_n n^{−2} + n^{−1} → 0.
GR: Proposition P(a). The constants are fixed and M_n is deterministic, so Theorem MIS (ii) applies. ∎

**Remark (what (b) asks of Σ).** A lower restricted eigenvalue of the *population* candidate covariance at sparsity
O(log n), bounded variances, bounded projected signal energy, and a beta-min on the population projection.
Examples via Proposition P(d): (i) a stationary Gaussian AR(1) sequence x_1, …, x_{p+1} with one omitted interior
variable k has tridiagonal Θ, so N_Θ(k) = {k − 1, k + 1} and s₀^𝒞 ≤ s₀ + 1 stays bounded (proxies = the two
neighbours); (ii) a one-factor design Σ = D + λλᵀ (D diagonal ≻ 0) has Θ = D⁻¹ − D⁻¹λλᵀD⁻¹/(1 + λᵀD⁻¹λ), so
Θ_jk ≠ 0 whenever λ_jλ_k ≠ 0: for an omitted loading variable, γ is dense on the loading candidates; if the number of
loading candidates that are null in the full model tends to infinity (e.g. β_𝒞 = 0), each of them is a proxy, s₀^𝒞 grows
with p_𝒞, and (H-MIS) (fixed s₀^𝒞) fails — outside the theorem. (Numerics N1 builds x_k = X_𝒞a + z with equicorrelated
candidates; there Θ_jk ≠ 0 exactly for j ∈ supp a, so γ is sparse although every candidate is marginally correlated
with x_k.)

## Example E1 (analytic separation of the targets)

x₁, x₂, x₃, z iid N(0, 1) (fixed in n), 𝒞 = {1, 2, 3}, one omitted column x_k := −x₁ + x₂ + z, true model
y^r = x₁ + x_k + ε = x₂ + z + ε, ε ~ N(0, σ²I) independent. Full truth S₀ = {1, k}, S₀ ∩ 𝒞 = {1}.
GR: ω = x_k = X^r_𝒞γ + ξ with γ = (−1, 1, 0), ξ = z ~ N(0, I): τ² = 1 fixed. β^𝒞 = β_𝒞 + γ = (1, 0, 0) + (−1, 1, 0)
= (0, 1, 0), S₀^𝒞 = {2}, σ_𝒞² = σ² + 1. (Prop P: the marginal vector (x₁, x₂, x₃, x_k) has Θ_{1k} = 1, Θ_{2k} = −1, Θ_{3k} = 0,
Θ_kk = 1, so γ = −Θ_𝒞k = (−1, 1, 0) ✓.) GD(a) applies (p_𝒞 = 3, Σ_𝒞𝒞 = I, β^𝒞 ≠ 0 fixed), so by MIS (ii)
π_𝒞({2} | y) → 1 in probability under the joint law. Hence π_𝒞({1} | y) → 0 (the retained truth S₀ ∩ 𝒞 is the wrong
target: candidate 1 is cancelled, candidate 2 is a proxy). The sample projection of the realised mean x₂ + z on
[1, A], A := X^r_𝒞, has candidate slopes β̂_proj = v + (AᵀCA)⁻¹AᵀCz, v := (0, 1, 0)ᵀ (equivalently, in standardised
columns X_𝒞 = CAD_x⁻¹: θ̂_proj = D_xv + (X_𝒞ᵀX_𝒞)⁻¹X_𝒞ᵀCz). Conditionally on A (full centred column rank a.s. for
n ≥ 4), the noise part is Gaussian with covariance (AᵀCA)⁻¹ ≻ 0 (z independent of A), so each coordinate has a
nondegenerate continuous law and is nonzero almost surely; the dense model is feasible once n ≥ 6. Hence the
sample-projection support is {1, 2, 3} a.s. and receives posterior mass ≤ 1 − π_𝒞({2} | y) → 0. ∎
