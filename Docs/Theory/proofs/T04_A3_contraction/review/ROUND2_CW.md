# Round 2 — reviewer CW (Claude Work, claudeAgent_claude_work, Opus 5.5 xhigh, read-only plan mode)

- **Task ID:** <taskId>
- **Packet:** <PC_HOME>\review_packets\T04_wave3\CW\
- **Reply (verbatim):**

---

# Review report: T04 (A3), round 2 — PROOF_v2 against STATEMENT.md

**Scope.**
- I read STATEMENT.md, PROOF_v2.tex (in full), CLAIMS_OF_FATAL_FLAWS.md and MY_ROUND1_REPORT.md.
- I diffed `round1_v1/PROOF_v1.tex` against `PROOF_v2.tex`, and `round1_v1/STATEMENT.md` against `STATEMENT.md`. The only changes are the ones listed by the lead (items 1–6); no other mathematical text changed.
- I checked PROOF_v2.pdf pp. 1–4 and 8–14 against the tex. They match, including the equation numbers (1)–(12).
- I ran one read-only computation (no file written) to check Lemmas 1.1(a) and 1.2.

## Status of the round-1 findings

### F1 (gap) — resolved

**Location:** STATEMENT §1 "Model quantities"; PROOF_v2 §0 "Prior and target"; Lemma 1.2.

**The definition now in the packet.** STATEMENT §1 and §0 agree item by item:
- y = Cy^r/s_y;
- z_S = X_Sᵀy;
- Q = yᵀy − n z_SᵀH_S⁻¹z_S;
- a₀ = b₀ = 0.01;
- m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q)^{−ν};
- π = ϖm/Σ_Ω ϖm (= e^F/Z).

This agrees with the 00_COMMON quote in CLAIMS_OF_FATAL_FLAWS.md. The prefactor of m(S) does not depend on S, as Lemma 1.2 now says.

**Well-posedness.** The definition is well posed on {y_c ≠ 0}: there s_y > 0, and Q^{v3}_S = Q_S/s_y² ≥ 0 by Lemma 2.1(b), so 2b₀ + Q^{v3}_S > 0.

**Lemma 1.2, re-derived from the §0 definition.** The algebra holds:
- X = UZ, because CX = X.
- Cy^r = Uy_c, so y = Uy_c/s_y and yᵀy = ‖y_c‖²/s_y².
- z_S = Z_Sᵀy_c/s_y, so n z_SᵀH_S⁻¹z_S = y_cᵀM_Sy_c/s_y².
- Hence Q^{v3}_S = Q_S/s_y² and 2b₀ + Q^{v3}_S = (2b + Q_S)/s_y², with b = b₀s_y². The same s_y appears in y and in b, which is required.
- s_y^{2ν} does not depend on S.
- H_S, D_S, ϖ and Ω are the same objects on both sides, with both laws normalised over Ω.

**Numerical cross-check.** Setting: n = 9, p = 4, K = 4, all 16 models, a random design, SDs with ddof = 1 (so ‖x_j‖² = N = 8).
- π computed from the §0 formula and the weights of Lemma 1.1(a) differ by at most 1.9·10⁻¹⁶.
- π and the S-marginal of Π† differ by at most 1.7·10⁻⁷ (quadrature error). The S-marginal was computed by direct 1-D quadrature over v of N_N(0, vΣ_S) × IG(0.51, b), without Sylvester or Woodbury.

**Conclusion for F1.** The identity "S-marginal of Π† = π" now rests only on the packet. That covers both of its load-bearing uses: H-T02 to discard {|S| > m_n}, and the first claim of (ii) via (2).

### E1 — resolved

Proposition 4.1: log π(S)/π(S₀) < log ϖ(S) + (2s₀+1)ℓ_n + s₀ℓ_n − (3s₀+4)ℓ_n = log ϖ(S) − 3ℓ_n. The added note is correct.

### E2 — resolved

- The renames θ_n → ϑ_n, ξ_j → ζ_j, τ_k → t_k (Lemma 3.2), η → ε₀ and Γ → Υ are applied consistently; a search finds no stale occurrence.
- The only η left is the generic one in Lemma 7.2, which is applied with η = η_n.
- The Notation paragraph is accurate: the centring matrix C occurs only in §0 and in Lemma 1.2; v_S is a squared norm; E ~ χ²_N under P₀.
- Two trivial clashes remain (R2-E2 below).

### E3 — resolved

Remark 9.1 is now accurate:
- §§1–5 use p only through ℓ_n and the union bounds, so their non-asymptotic statements hold for every p.
- The choice of n₁ (m_n + s₀ ≤ ⌊n/2⌋) uses m_n = O(log n), and hence p ≤ n^A. The requirement d_* < m_n needs only m_n ≥ log₂ n.
- Step 3 of Theorem 7.4 uses p ≤ n^A and ℓ_n ≤ A log n.
- H-T02 enters §6 directly, and §8 through Theorem 7.4.
- The bullet on the rate b is now accurate: b enters through Lemmas 1.1–1.2 and (4).

### E4 — resolved

Theorem 7.4, Steps 3–4:
- Ξ̄_n := E₀Ξ_n, and the display is now a bound on it.
- Ξ_n is a finite sum of bounded (truncated) terms, so Ξ̄_n < ∞.
- If Ξ̄_n = 0, then Ξ_n = 0 a.s. and the step is trivial. Otherwise Markov gives P₀(Ξ_n > √Ξ̄_n) ≤ √Ξ̄_n.

### Other changes

- **Theorem 5.1(ii), "if n ≥ 8".** Correct. The interval [1, √(n/8)] is nonempty exactly when n ≥ 8, and √(n/8) ≤ √ν/2 because ν/4 = n/8 + 0.0025. Both applications (§6, §8) take n large, with u′_n = min{u_n, √(n/8)} ≥ 1.
- **G now listed in §7 and Theorem 7.4.** Correct: Proposition 7.3 uses e ~ N_N(0, σ*²I).

## Findings (round 2)

### R2-E1. Q_S and Z mean different things in STATEMENT.md and in the proof

- **Location:** STATEMENT §1 "Model quantities" vs PROOF_v2 §0 "Prior and target", "Data and contrast coordinates", and §1.
- **Severity:** exposition.
- **Claim.** In STATEMENT.md, Q_S is the v3 quantity yᵀy − n z_SᵀH_S⁻¹z_S, and Z is the normaliser Σ_Ω ϖm. In the proof, the v3 quantity is renamed Q^{v3}_S, while Q_S denotes y_cᵀ(I − M_S)y_c (= s_y²·Q^{v3}_S) and Z denotes UᵀX.
- **Evidence.** §0 defines Q^{v3}_S with exactly the formula of the STATEMENT, and the proof never uses Z for the normaliser (it writes the sum out). No step is affected. One sentence in the Notation paragraph would prevent a reader from mismatching them.

### R2-E2. Residual local symbol clashes

- **Location:** Lemma 3.1(b) and §7; Lemma 2.1(b),(f) and Lemma 3.2.
- **Severity:** exposition.
- **Claim.**
  - After the rename, ζ_j meets ζ ~ N(0, s²) of Lemma 3.1(b).
  - t_k (Lemma 3.2) sits next to the vector t ∈ ℝ^k of Lemma 2.1(b),(f).
  - The noise vector e shares its letter with Euler's e (inherited from v1).
- **Evidence.** All the clashing uses are local and separated by scope. None causes an error.

## Re-confirmation of unchanged steps

I re-checked these line by line against the v2 text. All hold.

- **§0.**
  - y_c = μ_c + e, using Uᵀ1 = 0 and UᵀX^r = UᵀCX^r.
  - Equation (1).
  - The rates, d_* and m_n, with m_n(½ log n) = m_n.
  - H-T02 with ω_n = ½ log n gives O_P(n^{−1/2}) → 0.
- **Lemma 1.1.**
  - Sylvester gives det Σ_S = D_S.
  - Woodbury gives Σ_S⁻¹ = I − M_S.
  - 0.51 + N/2 = ν.
  - The conditional law of v is IG(ν, b + Q_S/2).
  - θ_S has precision H_S/(nv) and mean nH_S⁻¹Z_Sᵀy_c.
- **Lemma 1.3(a)–(d).**
  - p·B(k+1, 2p−k) = w(k), and the binomial sum is 1.
  - The monotone factors in (d), with 2p − s₀ − j ≥ p.
- **Lemma 2.1(a)–(i).**
  - The spectral form of M_S.
  - The ridge variational formula (Hessian 2H_S/n).
  - (e) via M_S² ⪯ M_S.
  - The Schur blocks, R₂ ⪯ R₁ ⪯ G_JJ, and interlacing with g nondecreasing.
  - (g): (n+1)N ≥ n.
  - (h): R₂ ⪰ R₀ ⪰ Nφ₀²I and det(R₁ + I) ≤ (N(j+1))^j.
  - (i).
- **Lemmas 3.1 and 3.2.**
  - E e^{ξ/4} = 2^{r/2}.
  - 6k log 2 + 4k log p + 4ℓ_n ≤ 14kℓ_n.
  - The union bounds 1/n and 4/n.
  - t_k ≤ 2(k+1)ℓ_n.
  - Chebyshev for 𝓔₁ and 𝓔₄.
  - 2b ≤ b̄ and 2b + Q_S ≤ (1 + 2b₀/N)‖y_c‖² ≤ nB.
  - 2/N ≤ 3/n.
- **Proposition 4.1.**
  - The AM–GM steps.
  - 22k + 4s₀ + 12 ≤ 22(k + s₀ + 1).
  - log(1+x) ≥ x/(1+x) with x = Δ_S/(2b + Q_{S₀}).
  - ν ≥ n/2, so c₀Δ_S = Δ_S/(2B).
  - c₀ρ(d)/2 − c₀C₁(d + s₀ + 1)ℓ_n = [3(s₀+1)+1]ℓ_n.
- **Theorem 5.1.**
  - ρ(d) ≤ C_a L(d).
  - The constants C_b, C_f, C_c, C_d and C_e; none depends on s₀.
  - Z_Sθ_S − M_Sy_c ~ N(0, vM_S).
  - E[v | S, y] = (2b + Q_S)/(n − 1.98).
  - The Gamma/Chebyshev step and |xg − 1| ≤ 2|x − 1| + |g − 1|.
- **§6.**
  - Lemma 6.1: 2.5/log 2 < 3.61, and L(m_n) ≤ 6nε²_{2,n}.
  - The proofs of (i) and of (iii) under G, R.
- **§7.**
  - n₁, n₂ and (7).
  - Lemma 7.1: the prior ratio is ≤ (2p)^{s₀} and the Occam ratio ≤ (n+1)^{s₀/2}.
  - Lemma 7.2.
  - ϑ_n; η_n ≤ 2ϑ_n + 2.04/N; η_nℓ_n → 0.
  - Proposition 7.3: the fit bound; the denominator Nσ*²(1 − ϑ_n); χ²_J ≤ τ_j on 𝓔₂; the constant 28e³.
  - Theorem 7.4: the map is at most 2^{s₀}-to-one; κ_n; the decomposition into α_n, β_n, γ_n; the log n coefficient −½[(j₀+1) − s₀(2A+1)] ≤ −½; the O(√log n) remainder.
- **§8.**
  - L(d_*) ≤ (2A+3)nε²_{1,n}.
  - SE on T = S ∪ S₀, with |T| < m_n + s₀ and n/N ≤ 2.
  - (iv) via D_x⁻¹ ⪯ d₋⁻¹I.
  - C in (12) dominates every threshold used, and depends only on (σ*², M, φ₀, A), with b₀ fixed.

**Match with the statement.** The proven claims match STATEMENT §3 exactly: the quantifiers (including "every deterministic u_n → ∞"), the dependence of C, and Π† as defined in STATEMENT §1.

## Summary

F1 is closed, and the closure uses only packet material. All other round-1 items are addressed correctly, and none of the v2 changes introduces an error. Only two exposition notes remain (R2-E1, R2-E2). No fatal or gap finding remains.

VERDICT: verified
