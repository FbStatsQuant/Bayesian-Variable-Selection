# T33 — Numerical margins: a floating-point error bound for F(S) and its consequences (W7-SEC)

Run W7-SEC, 2026-11-02. **Candidate proofs, not reviewed, not adopted.** Code: `Scripts/SMC_BVS/core/cpp/v3_score.h`
(identical to commit 9db8748), production flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`
(`Makevars.v3`). Notation: `00_COMMON.md`; W2-BOOK Prop 2(f) and W5-LOCKBOOK's restatement of VAL-FP.

## 0. What is compared with what

- **Stored data.** X̂ (n×p) and ŷ (n) are the doubles the C++ context holds after `v3_preprocess`. All "exact"
  quantities below are computed **exactly from these doubles**: G := X̂ᵀX̂, z := X̂ᵀŷ, y′y := ŷᵀŷ, H_S, A_S := G_S + I,
  Q_S, log m(S), F(S), with the method's exact constants (a₀ = b₀ = 1/100, exact lgamma). Preprocessing error (the
  map raw → stored) is a separate data perturbation; it is not bounded here (see §6).
- **Computed.** Ĝ, ẑ, ŷtŷ (`data_init`), and log m̂(S), F̂(S) from `Scorer::score` (route `chol` unless stated).

**New symbols.** u := 2⁻⁵³; γ_j := ju/(1 − ju); γ′_j := γ_j/(1 − γ_j). For S with |S| = k ≥ 1:
g_S := max_{a∈S} G_aa (= n − 1 for standardised columns); h_S := (n+1)g_S + 1; a_S := g_S + 1;
λ_H := λ_min(H_S), λ_A := λ_min(A_S), κ_H := λ_max(H_S)/λ_H, κ_A likewise; ν = 0.01 + n/2.

**Hypotheses (named).**
- FP: IEEE-754 binary64 with round-to-nearest; the standard model fl(a ∘ b) = (a ∘ b)(1 + δ), |δ| ≤ u, for
  +, −, ×, /, √ (true for the production flags; FMA contraction is off). NOUF: no overflow or underflow occurs.
- LIB(c_L): `std::log` satisfies fl(log x) = log(x)(1 + δ), |δ| ≤ c_L u (glibc documents ≤ 1 ulp, so c_L = 2 is safe).
- SMALL: (n + 3K + 4)u ≤ 10⁻³ (so every γ_j used is ≤ 1.001ju and every product of (1 + γ) factors is ≤ 1.003).
- The constants log C_n and log ϖ(k) computed once in `data_init` have errors η_C := |log Ĉ_n − log C_n| and
  η_π(k) := |log ϖ̂(k) − log ϖ(k)|. They are not bounded a priori (lgamma accuracy is not specified by IEEE); they are
  measured once per (n, p) (≤ 1.8·10⁻¹² at n = 4000 and ≤ 1.1·10⁻¹³ at p ≤ 60 in `results/t33_fp_check.txt`).

**Cited lemmas** (standard; statements as in Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., 2002).
- (H1) Thm 10.3: if Cholesky runs to completion on a symmetric A of order k, the computed factor satisfies
  L̂L̂ᵀ = A + ΔA, |ΔA| ≤ γ_{k+1}|L̂||L̂ᵀ|. (Holds for any order of evaluating the inner products; `chol_inplace` is the
  inner-product (jik/Crout) form.)
- (H2) Thm 8.5: substitution for a triangular system gives (L̂ + ΔL)ŵ = b, |ΔL| ≤ γ_k|L̂|.
- (H3) Thm 10.7 (Demmel): if A is SPD, D = diag(a_ii)^{1/2} and λ_min(D⁻¹AD⁻¹) > kγ_{k+1}/(1 − γ_{k+1}), Cholesky
  runs to completion (barring underflow/overflow).
- (H4) Recursive summation of k terms has absolute error ≤ γ_{k−1}Σ|terms|; an inner product of length n has
  |fl(xᵀy) − xᵀy| ≤ γ_n|x|ᵀ|y|.

---

## 1. Exact-arithmetic facts. **PROVED.**

**Lemma T33-M (= T33(i), generalised).** For every S with |S| = k ≥ 1 and any real data,
I ≼ A_S ≼ (1 + tr G_S)I and I ≼ H_S ≼ (1 + (n+1)tr G_S)I. With standardised columns, tr G_S = (n−1)k, which is
T33(i): I ≼ H_S ≼ [1 + (n+1)(n−1)k]I. Hence κ_H ≤ 1 + (n+1)k g_S and κ_A ≤ 1 + k g_S, **also with duplicate columns**,
and exact Cholesky never fails.
*Proof.* G_S ≽ 0 and λ_max(G_S) ≤ tr G_S. ∎

**Lemma T33-Q (new).** For every S and any real data, Q_S ≥ y′y − (n/(n+1))‖P_Sŷ‖² ≥ y′y/(n+1), where P_S is the
orthogonal projection onto col(X̂_S).
*Proof.* z_S = X̂_Sᵀŷ ∈ range(G_S). For B ≽ A ≽ 0 with B ≻ 0 and v ∈ range(A): vᵀB⁻¹v = sup_x{2xᵀv − xᵀBx} ≤
sup_x{2xᵀv − xᵀAx} = vᵀA⁺v. Take B = H_S ≽ A = (n+1)G_S: z_SᵀH_S⁻¹z_S ≤ z_SᵀG_S⁺z_S/(n+1) = ‖P_Sŷ‖²/(n+1). ∎

**Consequences.** (a) y′y/Q_S ≤ n + 1: the cancellation in Q_S = y′y − n z′H⁻¹z costs at most a factor n + 1.
(b) The engine's switch to the non-negative form (`v3_score.h:219`, Q < 10⁻⁸y′y) is never triggered in exact
arithmetic when n + 1 < 10⁸; in floating point see Corollary T33-NF. (c) Checked: min_S Q_S(n+1)/y′y ranges from
1.0099 (D4, y almost in the span) to 233 over all tested models (`results/t33_fp_check.txt`).

---

## 2. Theorem T33-S (deterministic error bound for one score, Cholesky route). **PROVED** (given H1–H4, FP, NOUF, LIB, SMALL).

Fix S with |S| = k ≥ 1. Define
- ε_H := 1.01·k·h_S·(n + k + 3)u,  ε_A := 1.01·k·a_S·(n + k + 2)u,  ε_Q := 1.02·k·h_S·(n + 3k + 3)u;
- ρ_H := ε_H/λ_H, ρ_A := ε_A/λ_A, ρ_Q := ε_Q/λ_H;
- ω := γ_n·√(n·k·g_S/λ_H);
- r_Q := γ_n + 2.03u + [(ρ_Q + γ_k)/(1 − ρ_Q)](1 + ω)² + 2ω + ω²;  θ_Q := (y′y/Q_S)·r_Q;
- ℓ_H := log(1.01h_S) + 1, ℓ_A := log(1.01a_S) + 1; L_S := |log(2b₀ + Q_S)|; log D_S = log det H_S − log det A_S.

Assume ε_H, ε_A, ε_Q ≤ ½ and θ_Q ≤ ½. Then:
(a) both Cholesky factorisations in `try_chol` (stored-Gram route) run to completion, so `score` returns on route
    `chol` (no refactor, no QR, no numerical_failure);
(b) |l̂dH − log det H_S| ≤ η_H := kρ_H/(1 − ρ_H) + 1.01(k − 1 + c_L)k u ℓ_H, and likewise η_A for A_S;
(c) |Q̂_S − Q_S| ≤ y′y·r_Q, so |Q̂_S/Q_S − 1| ≤ θ_Q ≤ (n+1)r_Q;
(d) |log m̂(S) − log m(S)| ≤ η_m(S) := ½(η_H + η_A) + η_Q + η_asm + η_C, where
    η_Q := ν[θ_Q/(1 − θ_Q) + 1.01u] + 1.01(c_L + 2.01)u·νL_S and η_asm := 1.01u(2|log C_n| + 2 log D_S + νL_S);
(e) |F̂(S) − F(S)| ≤ η_F(S) := η_m(S) + η_π(k) + 1.01u(|log ϖ(k)| + |log m(S)|).
For k = 0, |log m̂(∅) − log m(∅)| ≤ η_C + ν(γ_n + 2.03u)(y′y/(2b₀+y′y)) + 1.01(c_L + 2.01)uνL_∅ + 1.01u|log m(∅)|.

**Condition-number form.** Since h_S ≤ λ_max(H_S) and a_S ≤ λ_max(A_S),
ρ_H ≤ 1.01k(n+k+3)u·κ_H, ρ_A ≤ 1.01k(n+k+2)u·κ_A, ρ_Q ≤ 1.02k(n+3k+3)u·κ_H, so to first order in u
  |log m̂(S) − log m(S)| ≲ ½k²(n+k)u(κ_H + κ_A) + ν(y′y/Q_S)[k(n+3k)uκ_H + nu(1 + 2√(nkg_S/λ_H))] + u(2|log C_n| + 2 log D_S + νL_S) + η_C.
**Universal (data-free) form.** λ_H, λ_A ≥ 1 and y′y/Q_S ≤ n + 1 (Lemmas T33-M, T33-Q) give a bound depending on
(n, k, g_S) only. At n = 200, k = K = 100 it allows η_Q ≈ 4.6·10⁻³ nats (the worst case needs κ_H = kn² and
y′y/Q = n + 1 at once); at n = 1000, K = 500 it is vacuous (≈ 80 nats) (`results/t33_valfp_budget.txt`). The
a-posteriori form with the model's λ_H and y′y/Q_S is the useful one (≈ 10⁻⁹–10⁻⁸ on the tested models, observed
errors ≈ 10⁻¹³–10⁻¹¹; `results/t33_fp_check.txt`).

### Proof

*Step 1 (Gram and response).* By (H4) and Cauchy–Schwarz, |Ĝ_ab − G_ab| ≤ γ_n‖x̂_a‖‖x̂_b‖ ≤ γ_n g_S,
|ẑ_a − z_a| ≤ γ_n√(g_S y′y), |ŷtŷ − y′y| ≤ γ_n y′y. Ĝ is exactly symmetric (computed once and mirrored).

*Step 2 (forming H̃, Ã).* n1 = n + 1 is exact. Off-diagonals fl(n1ĝ) = n1ĝ(1 + δ); diagonals
fl(fl(n1ĝ) + 1) = (n1ĝ(1+δ) + 1)(1 + δ′). So H̃ = H(Ĝ) + E₂, |E₂| ≤ γ₂|H(Ĝ)|, and |H(Ĝ)_ab| ≤ h_S(1 + γ_n);
‖E₂‖₂ ≤ ‖E₂‖_F ≤ kγ₂(1 + γ_n)h_S. For Ã only the diagonal is rounded: ‖E₂^A‖₂ ≤ u(1 + γ_n)a_S.

*Step 3 (Cholesky succeeds).* λ_min(H̃) ≥ λ_H − (n+1)‖Ĝ_S − G_S‖₂ − ‖E₂‖₂ ≥ 1 − ε_H ≥ ½ > 0, so H̃ is SPD, and
max_a H̃_aa ≤ 1.003h_S. Hence λ_min(D⁻¹H̃D⁻¹) ≥ 1/(2.006h_S). Because k ≤ K ≤ n/2 we have k + 1 ≤ n + k + 3, so
2.012k(k+1)u·h_S ≤ 1.99ε_H < 1, i.e. 1/(2.006h_S) > 1.003k(k+1)u ≥ kγ_{k+1}/(1 − γ_{k+1}). (H3) applies. Same for Ã.
`chol_inplace` checks only d > 0 and finiteness, so it returns true; NOUF excludes overflow.

*Step 4 (backward error).* By (H1), L̂L̂ᵀ = H̃ + E₃ with |E₃_ab| ≤ γ_{k+1}‖ℓ_a‖‖ℓ_b‖ (ℓ_a = row a of L̂). From
‖ℓ_a‖² = H̃_aa + E₃,aa we get ‖ℓ_a‖² ≤ H̃_aa/(1 − γ_{k+1}), so |E₃_ab| ≤ γ′_{k+1}(H̃_aaH̃_bb)^{1/2} and
‖E₃‖₂ ≤ ‖E₃‖_F ≤ γ′_{k+1}tr H̃ ≤ γ′_{k+1}·1.003kh_S. Write L̂L̂ᵀ = H_S + E_H. Collecting Steps 1, 2 and 4,
‖E_H‖₂ ≤ kh_S u[1.001n + 2.01 + 1.006(k+1)] ≤ ε_H. Likewise ‖E_A‖₂ ≤ ε_A.

*Step 5 (log-determinants).* Exactly, 2Σ_a log L̂_aa = log det(H_S + E_H). With M := H_S^{−1/2}E_HH_S^{−1/2},
‖M‖₂ ≤ ρ_H < 1, so |log det(H_S + E_H) − log det H_S| = |Σ_i log(1 + μ_i(M))| ≤ kρ_H/(1 − ρ_H). Rounding:
L̂_aa² ∈ [λ_min(L̂L̂ᵀ), (L̂L̂ᵀ)_aa] ⊆ [½, 1.01h_S], so |2 log L̂_aa| ≤ ℓ_H. The code computes 2·fl(Σ_a fl(log L̂_aa)):
error ≤ 2(c_Lu + γ_{k−1}(1 + c_Lu))Σ_a|log L̂_aa| ≤ 1.01(k − 1 + c_L)k u ℓ_H. This proves (b).

*Step 6 (quadratic form).* By (H2), the forward solve gives (L̂ + ΔL)ŵ = ẑ_S, |ΔL| ≤ γ_k|L̂|; so ‖ŵ‖² = ẑ_Sᵀ(H_S + E_Q)⁻¹ẑ_S
with E_Q = E_H + ΔLL̂ᵀ + L̂ΔLᵀ + ΔLΔLᵀ symmetric, and ‖ΔL‖₂ ≤ γ_k‖L̂‖_F, ‖L̂‖_F² = tr(L̂L̂ᵀ) ≤ 1.01kh_S give
‖E_Q‖₂ ≤ ε_H + 2.04k²h_S u ≤ ε_Q. Let q² := z_SᵀH_S⁻¹z_S, so Q_S = y′y − nq², and v := H_S^{−1/2}ẑ_S, q̂ := ‖v‖. Then
(i) |‖ŵ‖² − q̂²| ≤ [ρ_Q/(1 − ρ_Q)]q̂² (the eigenvalues of (I + H^{−1/2}E_QH^{−1/2})⁻¹ lie in [1/(1+ρ_Q), 1/(1−ρ_Q)]);
(ii) |q̂ − q| ≤ e′ := ‖ẑ_S − z_S‖/√λ_H ≤ √k γ_n√(g_S y′y)/√λ_H, so √n e′ = ω√(y′y);
(iii) nq² ≤ y′y·n/(n+1) ≤ y′y (Lemma T33-Q), hence n(q + e′)² ≤ y′y(1 + ω)², 2nqe′ ≤ 2ωy′y, ne′² = ω²y′y;
(iv) quad̂ = fl(Σ_aŵ_a²) has |quad̂ − ‖ŵ‖²| ≤ γ_k‖ŵ‖² (H4), and n‖ŵ‖² ≤ y′y(1 + ω)²/(1 − ρ_Q).
So n|quad̂ − q²| ≤ y′y{[(ρ_Q + γ_k)/(1 − ρ_Q)](1 + ω)² + 2ω + ω²}.
(v) Q̂ = (ŷtŷ − n·quad̂(1 + δ₁))(1 + δ₂): the two roundings cost ≤ 2.03u·y′y (both operands are ≤ 1.01y′y and
nonnegative), and |ŷtŷ − y′y| ≤ γ_n y′y. Summing, |Q̂ − Q_S| ≤ y′y·r_Q. This proves (c).

*Step 7 (the log Q term).* With θ_Q ≤ ½, min(Q̂, Q_S) ≥ Q_S(1 − θ_Q), so |log(2b₀ + Q̂) − log(2b₀ + Q_S)| ≤ θ_Q/(1 − θ_Q).
fl(2b₀ + Q̂) costs ≤ 1.01u (including 2b₀'s representation error ≤ 0.02u/(2b₀+Q̂)); fl(log ·) costs c_LuL_S(1+..);
ν̂ = fl(0.01 + n/2) has |ν̂ − ν| ≤ 1.01uν; the product costs uνL_S. Total ≤ η_Q.

*Step 8 (assembly).* `logm = logCn − 0.5·(ldH − ldA) − nu·log(arg)` is evaluated as three roundings: the difference
(≤ u log D_S·1.01), the first subtraction (≤ u(|log C_n| + ½ log D_S)·1.01) and the second (≤ u|log m|·1.01, with
|log m| ≤ |log C_n| + ½ log D_S + νL_S). Their sum is ≤ η_asm; the constant error adds η_C. This proves (d); (e) adds
the prior constant's error and one more rounding. ∎

### Corollary T33-NF (numerical_failure and the Q fallback are impossible at moderate sizes). **PROVED.**
Under FP, NOUF, LIB, SMALL, suppose for every feasible S (|S| ≤ K) that ε_H, ε_A, ε_Q ≤ ½ and (n+1)r_Q ≤ ½, and that
n + 1 ≤ 10⁷. Then every call of `Scorer::score` returns on route `chol` with `q_recomputed = false`. In particular
**the status numerical_failure can never occur** (the scorer is its only source: `v3_core.cpp` setup tables, V,
inherited and final-run rescoring, and `Engine::eval` all call `Scorer::score`).
*Proof.* (a) of Theorem T33-S gives route chol. By (c) and Lemma T33-Q, Q̂ ≥ y′y(1/(n+1) − r_Q) ≥ y′y/(2(n+1))
≥ 5·10⁻⁸y′y > 10⁻⁸ŷtŷ. Finally log m̂ is finite since every factor diagonal is ≥ ½^{1/2} and arg > 0. ∎
**At the study's sizes** (standardised columns, g_S = n − 1, n = 200, K = 100, any p; worst case λ_H = 1,
y′y/Q = n + 1): ε_H ≤ 1.4·10⁻⁷, ε_A ≤ 6.8·10⁻¹⁰, ε_Q ≤ 2.3·10⁻⁷, (n+1)r_Q ≤ 4.6·10⁻⁵, so the hypotheses hold and
**numerical_failure is impossible at n = 200** (for every p and every y). The a-priori hypotheses hold (worst case)
for n ≤ 1,286 when K = ⌊n/2⌋, n ≤ 4,575 when K = 10 and n ≤ 8,149 when K = 1 (`scripts/t33_valfp_budget.py`). Beyond
that the a-priori argument does not apply: the rounding-error bounds are worst case, and nothing is claimed to fail.
(This answers T33(iii)'s "no probability-zero statement for numerical_failure": under FP/LIB it is not probability
zero but **impossible**, for these sizes.)

---

## 3. Proposition T33-H (HPM decisions and ties on a common scored set). **PROVED.**

Let 𝒮 be a set of models scored with the same computed values in both runs being compared, S* its exact HPM
(00_COMMON tie rule) and η̄′ := max_{S∈𝒮}[η_F(S) − η_C]. (The constant log Ĉ_n is the same double in every score, so
its error cancels from every difference F̂(S) − F̂(S′).)
(a) The computed HPM Ŝ^fp over 𝒮 lies in the near-tie set 𝒩 := {S ∈ 𝒮 : F(S) ≥ F(S*) − 2η̄′}.
(b) If F(S*) − max_{S∈𝒮∖S*}F(S) > 2η̄′ then Ŝ^fp = S*.
(c) Exact ties: if F(S*) = F(S′) for some S′ ≠ S* (e.g. T06 ties, X_SX_Sᵀ = X_{S′}X_{S′}ᵀ), the computed winner is
    decided by rounding, not by the tie rule, unless F̂(S*) and F̂(S′) are bitwise equal. The tie rule is implemented
    faithfully only among bitwise-equal computed scores (the cache and the deterministic scorer guarantee that the
    same model always gets the same bits, `v3_score.h:252–254`).
(d) If S₀ ∈ 𝒮 and F(S₀) − max_{S≠S₀}F(S) ≥ m_n with m_n > 2η̄′, then Ŝ^fp = S₀. T03's candidate margin is
    ½log n − ½log log n − O_P(1). At n = 200 even the data-free bound gives 2η̄′ ≲ 10⁻² for every |S| ≤ 100, and the
    a-posteriori bound gives ~10⁻⁸; so T33(ii)'s requirement η = o(log n) is met with a lot of room wherever
    Theorem T33-S applies with its a-posteriori constants.
*Proof.* |F̂(S) − F̂(S′) − (F(S) − F(S′))| ≤ 2η̄′; the computed rule picks the largest F̂ (then size, then lex). ∎
**Remark (exact-branch certificates, R9).** `v3_exact.R` certifies "global" when F̂(HPM) − η_eng(HPM) >
max_{S≠HPM}[F̂(S) + η_eng(S)], with the engine's heuristic η_eng (`v3_score.h:241–246`). This is a valid certificate
of the exact HPM whenever η_eng(S) ≥ |F̂(S) − F(S)| − η_C for all S; replacing η_eng by η_F − η_C of Theorem T33-S makes
it rigorous. **COUNTEREXAMPLE: η_eng is not a bound.** With y = x₁ + noise (y′y/Q ≈ 10²–10⁴), k ∈ {1, 2},
|log m̂ − log m| / η_eng reaches 1.17 at n = 10⁵ and 6.2 at n = 4·10⁶ (`scripts/t33_engine_bound_stress.py`,
`results/t33_engine_bound_stress.txt`, seed 20261104). The cause: η_eng's Q term ν(y′y/Q)(1 + k cond_H)·64ε has no
factor growing with n, while the rounding of the length-n dot products z_j and y′y in `data_init` grows like √n (in
these tests) relative to y′y and is multiplied by ν·y′y/Q. At n = 200 the heuristic held in every test with
≥ 24× room (`results/t33_fp_check.txt`). Fixes (implementation, not done here): add a term
64ε·ν·(y′y/Q)·√n (or ·n for a worst-case bound) to η_eng, or accumulate the dot products in long double or with
compensated summation.

---

## 4. Proposition T33-Z (the floating-point evidence and VAL-FP). Deterministic part **PROVED**; the a-priori ε part **PROVED but vacuous at the study's budgets**.

Fix a calibration output 𝓒 computed in floating point. 𝓒 is a function of the data and streams 0–9 only (the fp
arithmetic is deterministic), so **T12's frozen-run identities apply to the exact-arithmetic final run R^ex on 𝓒**
(exact scores, exact π₀ and Z̄₀, same grid, same streams 10–13). Calibration agreement between fp and exact runs is
therefore **not** needed; W5-LOCKBOOK's "the exact run shares 𝓒" holds by construction. Let R^fp be the production
final run on the same 𝓒 and streams.

**Agreement event.** G_fp := {every discrete decision of R^fp equals that of R^ex}: each π₀ draw (categorical draws by
inverse cdf), each Gibbs inclusion (u < o_j), each MH acceptance (u < α), each resampling ancestor (inverse cdf on
cumulative weights), and the local-search moves. On G_fp both runs visit, score and resample the same states.

**(Z1) Deterministic part.** On G_fp, for every island r,
  |log Ẑ_r^fp − log Ẑ_r^ex| ≤ η_Z := η_{m0} + η_{Z̄0} + η_d + 2.01u·D_max + T·ρ_stage,
where η_{m0} is the k = 0 bound of Theorem T33-S; η_d := max over states of |d̂ − d| ≤ (J_S + 2)·max η′_m over the
model and its block sub-models (η′_m := η_m − η_C; J_S ≤ |S| = number of blocks met; the common log Ĉ_n cancels in
log m − log m(∅)); η_{Z̄0} ≤ J(2η′_tab + 2ρ_LSE) + max_k η_π(k) + ρ_LSE with η′_tab := max over table models of
η′_m and J the number of blocks; D_max := max |d| over visited states; ρ_LSE(N) := (N/e + 4)u + 1.01Nu_L + 2u·Λ
(u_L = 2⁻⁶⁴ the long-double unit, Λ the largest |value| entering or leaving the log-sum-exp); ρ_stage := ρ_LSE(N) + u·Λ_Z
(Λ_Z := max_t |log Ẑ_{r,t}|). The pooled Ẑ adds one log-sum-exp of 4 terms.
*Proof.* log Ẑ_r = log m(∅) + log Z̄₀ + Σ_t[LSE_i(Δ_t d_i) − log N] (`v3_engine.h:299–322`). On G_fp the particles
agree, the grid is the same doubles, Σ_tΔ_t = 1, and LSE is 1-Lipschitz in the sup norm, so the d-errors cost
Σ_tΔ_tη_d = η_d; fl(φ_t − φ_{t−1}) and fl(Δ_t·d̂) cost ≤ 2.01uΔ_t|d| per stage, summing to ≤ 2.01uD_max. The LSE
rounding: the shift v − m is rounded in double (relative error u|v − m| on a term e^{v−m} ≤ 1, and
Σ_i u|x_i|e^{x_i} ≤ uN/e), the sum is accumulated in long double (≤ γ_N^{(L)}), the log and the final addition cost
≤ 2uΛ. log Z̄₀ is a chain of J log-sum-exp convolutions (`v3_start.h:101–137`) whose inputs are table log-ratios with
error ≤ 2η′_tab (log m(U) − log m(∅), two scores); the 1-Lipschitz property propagates errors additively. ∎

**(Z2) A-priori ε (union bound).** Under EX-S (the uniforms of streams 10–13 are i.i.d. on the 2⁻⁵³ grid of [0,1)),
  P(G_fp^c | 𝓒) ≤ C_dec·(η_γ + 2⁻⁵³ + 4u) + 2N²η_d + T·N·(Nγ_N + 2⁻⁵³) + Q_all·(2η_{π0} + 2⁻⁵³)
where C_dec is the number of Gibbs/MH/independence decisions of the final run (≤ 4N_{e*}m(T + L + 4), T32), η_γ bounds
the error of each decision's log-ratio (≤ 2(max η′_m-based error of log γ_φ) — each log-ratio involves two states),
Q_all is the number of π₀ draws (each draw makes ≤ J + 1 categorical choices; η_{π0} bounds the error of their log
probabilities, ≤ η_{Z̄0} + 2η′_tab), and the resampling term uses Σ_tΔ_t = 1.
*Proof.* Couple both runs through the same uniforms. At the first disagreement the uniform lies between the fp and
exact thresholds. For Gibbs, |ô_j − o_j| ≤ ¼|δ la| + 2u (plogis is ¼-Lipschitz); for MH, |α̂ − α| ≤ |δ la| + 2u
(min(1, eˣ) is 1-Lipschitz); for an inverse-cdf draw on N categories, P(disagree) ≤ Σ_k|Ŵ_k − W_k| ≤ N·max_k|Ŵ_k − W_k|.
For resampling at stage t, the log-weights differ by ≤ Δ_tη_d + 2.01uΔ_t|d|, the normalised cumulative weights by
≤ (e^{2Δ_tη_d} − 1) + Nγ_N (cumulative summation in double), and N draws are made. Given the history the next uniform
is independent and uniform on the grid, so P(it falls in an interval of length ℓ) ≤ ℓ + 2⁻⁵³. Sum over decisions. ∎

**(Z3) VAL-FP and Prop 2(f).** On G_fp, |log Ẑ^fp − log Ẑ^ex| ≤ η_Z. So VAL-FP(η_Z, ε) holds with ε = the bound of (Z2),
and W2-BOOK Prop 2(f) gives P(𝒪_E ∩ {αẐ^fp > Z}) ≤ α·e^{η_Z}·P(𝒜) + ε. **PROVED** (as an implication).

**What the numbers say** (`results/t33_valfp_budget.txt`; n = 200, p ∈ {500, 1000}, both tiers, T ∈ {10, 100, T_e}):
η_Z is 6·10⁻¹¹–4.5·10⁻⁹ with **measured** per-score errors (1.3·10⁻¹³) and ≈ 10⁻⁶ with the **rigorous** per-score
bound of a well-conditioned model (10⁻⁸), so e^{η_Z} − 1 is negligible either way. But the union bound ε is dominated
by C_dec·η_γ, and the final run makes 10⁸–10¹¹ decisions: ε ranges from 2·10⁻³ (tier 0, T = 10) to > 1 (tier 1,
T = 4000) with measured per-score errors, and is ≫ 1 (vacuous) with the rigorous ones. So **ε cannot be certified a
priori** at the study's budgets. It must be measured by replay (W2-BOOK's position stands), or replaced by a
path-free argument (§5, OPEN).

---

## 5. What is not shown (OPEN)

- **Path-free evidence bound.** A perturbed Feynman–Kac argument (the fp run as an exact SMC for slightly wrong
  potentials and kernels) would avoid G_fp. Gibbs and acceptance probabilities are multiplicatively stable
  (|log ô − log o|, |log(1−ô) − log(1−o)| ≤ |δ la|), but the MH self-loop probability 1 − α is not when α ≈ 1, and the
  fp kernels are not exactly invariant for any target. I did not close this.
- **Preprocessing error** (raw → stored X̂, ŷ) is a data perturbation that changes F by a condition-number-weighted
  amount; not bounded here. It does not affect the HPM/evidence comparisons between fp and exact runs **on the same
  stored data**, which is what VAL-FP needs.
- **Probabilistic rounding** (√n instead of n growth of dot-product errors) would make Theorem T33-S ~10²× sharper
  and extend Corollary T33-NF to larger n; not attempted.
