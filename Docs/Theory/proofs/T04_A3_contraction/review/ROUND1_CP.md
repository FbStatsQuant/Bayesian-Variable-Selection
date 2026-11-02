# Round 1: reviewer CP (Claude Personal, claudeAgent, Opus 5.5 xhigh, read-only plan mode)

- Task ID: <taskId>
- Packet: <PC_HOME>\review_packets\T04_wave3\CP\ (STATEMENT.md, PROOF_v1.tex, PROOF_v1.pdf)
- Prompt: <PC_HOME>\review_packets\T04_wave3\REVIEW_PROMPT_TEMPLATE.md, with PACKET set to the CP folder.

The reviewer's reply follows, verbatim.

---

# Review of T04 PROOF_v1 (contraction without beta-min, SMC-BVS v3)

I read STATEMENT.md and PROOF_v1.tex in full, and checked that PROOF_v1.pdf is the same text as the .tex. I did not modify any packet file. Plan mode made me write a short summary to the plan file `<PC_CLAUDE_CONFIG>\plans\act-as-the-review-eager-pudding.md`; I wrote nothing else.

I also ran throwaway numerical spot checks on random designs, without writing any files. They confirmed:
- Lemma 1.3(a) and (d);
- Lemma 2.1(a), (d), (f), (g) and (h) (the (h) bound held with slack ≥ 2×);
- the Sylvester and Woodbury identities in Lemma 1.1;
- Lemma 7.2;
- the numeric constants n/(n−1.98) ≤ 2 at n = 4, and 2.5/log 2 ≤ 3.61.

## Scope of what was verified

I checked the following by hand.

- **§0.** The contrast coordinates: U^⊤1 = 0, y_c = μ_c + e, e ~ N_N(0, σ⋆²I_N), and the norm identity (1).
- **Lemma 1.1.**
  - The marginal covariance v·Σ_S, with det Σ_S = D_S and Σ_S⁻¹ = I − M_S.
  - The shape 0.51 + N/2 = ν.
  - The conditional laws (b) and (c): precision H_S/(nv) and mean nH_S⁻¹Z_S^⊤y_c.
- **Lemma 1.3.** The Beta-function identity, the sum ∑_k C(p,k)w(k) = 1, and parts (b)–(d).
- **Lemma 2.1.**
  - The spectral form of M_S and the ridge variational formula.
  - a_S ≤ δ for S ⊇ S₀.
  - The decomposition (c).
  - The Schur-complement determinant ratio, R₂ ⪯ R₁, and the Cauchy-interlacing argument for D_{S'} ≥ D_S.
  - The constants in (g), including (n+1)N ≥ n.
  - In (h): R₂ ⪰ R₀ ⪰ Nφ₀², and det(R₁+I) ≤ (N(j+1))^j.
  - Part (i).
- **Lemmas 3.1 and 3.2.**
  - E e^{ξ/4} = 2^{r/2}.
  - The union bounds 1/n and 4/n.
  - The constant 14 in ℰ₂, and the term 2√(a_S(k+1)ℓ_n) in ℰ₃.
  - The bounds b̄ and nB on ℰ₁.
  - The total 2/N + 5/n ≤ 8/n.
- **Proposition 4.1.**
  - The Δ_S bound, both AM–GM steps, and C₁.
  - The bound via log(1+x) ≥ x/(1+x).
  - c₀Δ_S > [3(s₀+1)+1]ℓ_n.
  - The prior bound −log ϖ(S₀) ≤ (2s₀+1)ℓ_n.
- **Theorem 5.1.**
  - (i): the constants C_b and C_f, the conditional law N(0, vM_S), E[v|S,y] = (2b+Q_S)/(n−1.98), and the Markov bound 2B/ℓ_n.
  - (ii): C_c, C_d and C_e; 2ν = N + 1.02; the Gamma representation; and u ≤ √(n/8) ≤ √ν/2.
- **§6.** Lemma 6.1, and the proofs of (i) and of (iii) under G, R, including the truncation u′_n.
- **§7.**
  - The choice of n₁ and the cap inclusion (7).
  - Lemma 7.1, including the 2^{s₀}-to-one map S ↦ S∪S₀.
  - Lemma 7.2.
  - θ_n, η_n and their rates.
  - Proposition 7.3: the prior, Occam, fit, denominator, assembly and truncation steps, and the expectation constant 28e³.
  - Theorem 7.4: κ_n with constant 168, ψ_j ≤ (α_n+β_n)j + γ_n, the geometric tail, the log-n coefficient −½[(j₀+1) − s₀(2A+1)] ≤ −½, and the Markov step.
- **§8.**
  - The bound (11) on L(d⋆).
  - The coefficient bound via SE on T = S∪S₀, with |T| ≤ m_n + s₀.
  - Part (iv) and the constant (12).

The proved claims match the statement exactly:
- Quantifiers: every deterministic u_n → ∞ is covered, including u_n > √(n/8), through the truncation u′_n.
- C depends only on (σ⋆², M, φ₀, A), with b₀ = 0.01 fixed; it does not depend on s₀, p_n or u_n.
- Π† is used only through its definition.
- H-T02 is used only in the stated form, Π(|S| > m_n | y) → 0.

## Findings

**1. Lemma 1.2 and §0 "Prior and target"**
- **Severity:** exposition. This is an external input that cannot be checked from the packet.
- **Claim:** Lemma 1.2 uses the formula π(S) ∝ ϖ(S)·D_S^{−1/2}·(2b₀ + Q^{v3}_S)^{−ν}, with Q^{v3}_S = y^⊤y − n z_S^⊤H_S⁻¹z_S, y = Cy^r/s_y and z_S = X_S^⊤y. This formula is quoted from 00_COMMON §1, which is not in the packet, so I cannot confirm it. The proof's opening sentence ("No other result is used") does not mention this dependence.
- **Evidence:** Given the formula, the conversion is correct: y = Uy_c/s_y, z_S = Z_S^⊤y_c/s_y, Q^{v3}_S = Q_S/s_y², and the factor s_y^{2ν} cancels. The formula is also consistent with every quantity STATEMENT.md does define: ν = 0.01 + n/2 = 0.51 + N/2, D_S, H_S, b₀ and ϖ.
- **Impact:** The identification "S-marginal of Π† = π" is what lets H-T02 enter (i) and (iii), and it is the subject of (ii)'s first claim. If 00_COMMON's π differed from the formula, that link would fail. I recommend reproducing the formula in STATEMENT.md.

**2. Proposition 4.1**
- **Severity:** exposition.
- **Claim:** The bound actually proved is stronger than the one stated.
- **Evidence:** log(π(S)/π(S₀)) < log ϖ(S) + (2s₀+1)ℓ_n + s₀ℓ_n − (3s₀+4)ℓ_n = log ϖ(S) − 3ℓ_n. So the proof gives e^{−3ℓ_n}, while the proposition states e^{−ℓ_n}. This is harmless.

**3. Remark 9.1**
- **Severity:** exposition.
- **Claim:** Two sentences are slightly inaccurate.
  - "Sections 2–6 hold for every p": the non-asymptotic statements in Sections 2–5 do, but Section 6's conclusions rely on H-T02, which is assumed only in R1 (p ≤ n^A).
  - "b enters only through 0 < 2b ≤ b̄": b also enters through 2b + Q_S ≤ nB in (4), and through Lemma 1.2.

**4. Notation throughout**
- **Severity:** exposition.
- **Claim:** Several symbols are overloaded:
  - M is a constant, M_S a matrix, and ℳ a set of models.
  - θ_n is a deterministic sequence, while θ is the parameter.
  - η is a generic tolerance in §6, while η_n is a sequence in §7.
  - τ_k in Lemma 3.2 is k log p + k log 2 + ℓ_n, while τ_j in §7 is 14(s₀+j)ℓ_n.
  - ξ is a χ² variable in Lemmas 3.1 and 7.2, while ξ_j is a deterministic bound.
  - E is a χ²_N variable, while 𝔼 is expectation.
  - C is the centring matrix and also the final constant.
  - B is a constant and also the Beta function B(·,·).
  - W_K is the prior normaliser, while W_S is a noise term.
  - v_S is a squared norm, while v is the variance.
  - Γ is a Gamma(ν,1) variable and also the Gamma function.
- **Evidence:** None of these causes an error, but they make the proof harder to audit.

**5. Theorem 5.1(ii) and Theorem 7.4**
- **Severity:** exposition.
- **Claim:** Two hypotheses are implicit.
  - The range u ∈ [1, √(n/8)] is empty for n < 8, so Theorem 5.1(ii) implicitly requires n ≥ 8. This is harmless, since it is applied only for large n.
  - Theorem 7.4 is stated "under R, SE and H-T02" without G. G is a standing assumption, used through Lemma 3.2 and Proposition 7.3.

## Conclusion

I found no fatal or gap findings. Every probability bound, constant and use of a hypothesis (R, SE, DX, the cap K, H-T02) checks out. The one input I cannot verify from the packet is the 00_COMMON §1 formula in Finding 1. It is consistent with all the quantities the statement defines, and the derivation from it is correct.

VERDICT: verified
