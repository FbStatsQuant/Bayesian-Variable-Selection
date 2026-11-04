# Round 1: reviewer CW (Claude Work, claudeAgent_claude_work, Opus 5.5 xhigh, read-only plan mode)

- **Task ID:** <taskId>
- **Packet:** <PC_HOME>\review_packets\T04_wave3\CW\ (STATEMENT.md, PROOF_v1.tex, PROOF_v1.pdf)
- **Prompt:** <PC_HOME>\review_packets\T04_wave3\REVIEW_PROMPT_TEMPLATE.md, with PACKET set to the CW folder.

The reviewer's reply follows, verbatim.

---

# Review report — T04 (A3), PROOF_v1, against STATEMENT.md

**Scope.** I read STATEMENT.md and PROOF_v1.tex in full, and I spot-checked PROOF_v1.pdf (pp. 1–4 and 12–13). The pages I checked match the tex, including the equation numbering ((12) is the final constant). I checked every displayed inequality and constant line by line. All steps not listed below check out; the main ones are listed in the verification log at the end.

## Findings

### F1. Lemma 1.2 and §0 "Prior and target": the formula for π is imported from outside the packet
- **Severity:** gap. It concerns packet scope only; the step is load-bearing but probably easy to repair.
- **Claim.** The proof takes the formula π(S) ∝ ϖ(S) D_S^{-1/2} (2b₀ + Q^{v3}_S)^{-ν} from "00_COMMON §1". It also takes from there Q^{v3}_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S, y = Cy^r/s_y and z_S = X_Sᵀ y. Neither STATEMENT.md nor the proof defines this formula: §0 writes π(S) ∝ ϖ(S) m(S) and never defines m(S). So I cannot confirm from the packet that this formula is the v3 posterior.
- **Why it matters.** The identity "S-marginal of Π† = π" is load-bearing in two places:
  - H-T02 is a statement about π, and the proof uses it to discard {|S| > m_n} under Π†.
  - The first claim of (ii) is about π, and Theorem 7.4 proves it via (2), which comes from Lemma 1.1(a) through Lemma 1.2.
- **Evidence.**
  - Given the quoted formula, the algebra in Lemma 1.2 is correct: Cy^r = U y_c, so y = U y_c / s_y and z_S = Z_Sᵀ y_c / s_y. Hence Q^{v3}_S = Q_S / s_y² and 2b₀ + Q^{v3}_S = (2b + Q_S)/s_y². The factor s_y^{2ν} does not depend on S.
  - The formula is consistent with the quantities STATEMENT §1 lists (D_S, ν = 0.01 + n/2, b₀).
  - It is also consistent with the T01(i) remark: the map θ = s_y β, v = s_y² σ² sends IG(0.51, b₀) to IG(0.51, b₀ s_y²) and N(0, nσ²(G_S + I)⁻¹) to N(0, nv(G_S + I)⁻¹).
- **Suggested repair.** Quote the 00_COMMON §1 definition verbatim, in §0 or in the packet. A one-line comparison then closes the gap.

### E1. Proposition 4.1: the bound is correct but looser than what is shown
- **Severity:** exposition.
- **Claim.** The stated bound π(S)/π(S₀) < ϖ(S) e^{−ℓ_n} is correct, but the displayed estimates give more:

  log π(S)/π(S₀) < log ϖ(S) + (2s₀+1)ℓ_n + s₀ℓ_n − (3s₀+4)ℓ_n = log ϖ(S) − 3ℓ_n.

  This is harmless.

### E2. Notation clashes throughout
- **Severity:** exposition.
- **Claim.** Several symbols have two meanings:
  - C is both the centring matrix and the final constant in (12).
  - θ_n (a deterministic sequence, §7) sits next to θ and θ*.
  - ξ is a χ² variable in Lemmas 3.1 and 7.2, while ξ_j is a deterministic quantity.
  - η is the tolerance in the proofs of (i) and (iii), while η_n is a sequence.
  - W_S (the cross term) sits next to W_K (the prior normaliser).
  - B is a constant, while 𝓑(d) is a set.
  - M is a constant, while M_S and 𝓜 are a matrix and a set.

  None of these causes an error. Several are inherited from STATEMENT.md.

### E3. Remark 9.1: "Sections 2–6 hold for every p"
- **Severity:** exposition.
- **Claim.** This holds for Sections 2–5, but not for Section 6:
  - Section 6's conclusions use H-T02, which is assumed only in R1 (p ≤ n^A).
  - The existence of n₁ in §7 also uses p ≤ n^A, through m_n = O(log n).

  The remark is imprecise, but no argument depends on it.

### E4. Theorem 7.4, Steps 3–4: what Ξ̄_n denotes in the Markov step
- **Severity:** exposition.
- **Claim.** Ξ̄_n is defined as E₀Ξ_n, but the proof only shows that an upper bound of it tends to 0. Markov's step, P₀(Ξ_n > √Ξ̄_n) ≤ √Ξ̄_n, uses E₀Ξ_n itself, and the case Ξ̄_n = 0 is trivial. The logic is fine; the notation conflates the expectation with its bound.

## Verification log (checked, no issue)

- **§0 and the statement.**
  - Π† is defined exactly as in STATEMENT §1. So are the rates, d_*, m_n, and the use of H-T02 with ω_n = ½ log n.
  - C depends only on (σ*², M, φ₀, A), with b₀ fixed.
  - All four parts are proved with the quantifiers of the STATEMENT, including "every deterministic u_n → ∞".
- **Lemma 1.1.**
  - Sylvester's identity gives det Σ_S = D_S.
  - Woodbury gives Σ_S⁻¹ = I − M_S.
  - 0.51 + N/2 = ν.
  - The IG(ν, b + Q_S/2) conditional checks.
  - The marginal ∝ D_S^{-1/2}(2b + Q_S)^{-ν} checks.
  - The θ_S conditional checks: precision H_S/(nv), mean nH_S⁻¹Z_Sᵀy_c.
- **Lemma 1.3.** The Beta identity p·B(k+1, 2p−k) = w(k) and the sum = 1 check. So do (b)–(d), including the monotonicity of the factors and 2p − s₀ − j ≥ p.
- **Lemma 2.1.**
  - (a): the spectral form of M_S.
  - (b): the ridge variational formula (Hessian 2H_S/n), and a_S ≤ δ for S ⊇ S₀.
  - (c)–(e).
  - (f): the Schur blocks R₁, R₂ and R₂ ⪯ R₁; the lower bound via Cauchy interlacing, with g nondecreasing.
  - (g): (n+1)N ≥ n.
  - (h): R₀ ⪰ Nφ₀²I and det(R₁ + I) ≤ (Nj + 1)^j.
  - (i).
- **Lemmas 3.1 and 3.2.**
  - E e^{ξ/4} = 2^{r/2}.
  - The constant 14: 6k log 2 + 4k log p + 4ℓ_n ≤ 14kℓ_n.
  - The union bounds 1/n and 4/n, using τ_k ≤ 2(k+1)ℓ_n and v_S ≤ a_S.
  - 2/N ≤ 3/n, 2b ≤ b̄, and 2b + Q_S ≤ nB.
- **Proposition 4.1.** The AM–GM steps (4√(xy) ≤ x/2 + 8y), 22k + 4s₀ + 12 ≤ 22(k + s₀ + 1), log(1+x) ≥ x/(1+x), ν ≥ n/2, and −log ϖ(S₀) ≤ (2s₀+1)ℓ_n all check.
- **Theorem 5.1.**
  - The constants C_b, C_f, C_c, C_d, C_e.
  - The Markov step with E[v | S, y] = (2b + Q_S)/(n − 1.98), and n/(n − 1.98) ≤ 2.
  - The Gamma step: u ≤ √(n/8) ≤ √ν/2, |ν/Γ − 1| ≤ 2√2·u/√n ≤ 1, and |xg − 1| ≤ 2|x − 1| + |g − 1|.
- **§6.** Lemma 6.1 (2.5/log 2 < 3.61, and L(m_n) ≤ 6nε²_{2,n}), and the truncation u′_n = min{u_n, √(n/8)}.
- **§7.**
  - n₁ exists, and (7) holds.
  - Lemma 7.1: the prior ratio is ≤ (2p)^{s₀} and the Occam ratio is ≤ (n+1)^{s₀/2}.
  - Lemma 7.2: Γ(x+1) ≥ x^x e^{−x}.
  - θ_n and η_n: η_n ≤ 2θ_n + 2.04/N, and η_nℓ_n → 0.
  - Proposition 7.3:
    - the fit bound, via P_{S₀} − M_{S₀} ⪯ ((1 + φ₀⁻²)/n) P_{S₀};
    - the denominator Nσ*²(1 − θ_n), term by term;
    - χ²_J ≤ τ_j on 𝓔₂;
    - the expectation constant 28e³.
  - Theorem 7.4:
    - the map S ↦ S ∪ S₀ is at most 2^{s₀}-to-one;
    - κ_n = 168e³(s₀+1)³ℓ_n²/(nφ₀²);
    - the ψ_j decomposition into α_n, β_n, γ_n;
    - the log n coefficient −½[(j₀+1) − s₀(2A+1)] ≤ −½;
    - the remainder is O(√log n).
- **§8.**
  - (11): L(d_*) ≤ (2A+3)nε²_{1,n}.
  - The coefficient step via SE on T = S ∪ S₀, with |T| ≤ m_n + s₀ and n/N ≤ 2.
  - (iv) via D_x⁻¹ ⪯ d₋⁻¹I.
  - C in (12) dominates every threshold used.

## Summary

Apart from F1, I found no fatal or gap findings. Every step checks, conditional on the formula quoted in Lemma 1.2 being the 00_COMMON §1 definition of π. F1 alone is why the verdict below is "not verified".

VERDICT: not verified
