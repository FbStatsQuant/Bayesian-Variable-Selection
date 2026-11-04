# Round 2: reviewer CP (Claude Personal, claudeAgent, Opus 5.5 xhigh, read-only plan mode)

- **Task ID:** `<taskId>`
- **Packet:** `<PC_HOME>\review_packets\T04_wave3\CP\`. It held STATEMENT.md, PROOF_v2, CLAIMS_OF_FATAL_FLAWS.md, the reviewer's own round-1 report, and `round1_v1\`.
- **Reply:** saved verbatim below.

---

# Round-2 review of T04 PROOF_v2 (contraction without beta-min, SMC-BVS v3), reviewer CP

**What I read and did.**
- I read STATEMENT.md, PROOF_v2.tex in full, CLAIMS_OF_FATAL_FLAWS.md, MY_ROUND1_REPORT.md and round1_v1/.
- I diffed PROOF_v1.tex against PROOF_v2.tex, and the round-1 STATEMENT.md against the current one. The diff contains exactly the six changes listed in the brief and nothing else. Apart from the title and the intro sentence, every changed line is a definition, a note, a rename or a hypothesis label.
- I compared PROOF_v2.pdf with the .tex on pages 2–4, 13 and 14. These pages cover §0, the Notation paragraph, Lemmas 1.1–1.3, §8 and the Remarks, and they show the same text as the .tex.
- I ran one throwaway numerical check from stdin, with no file written (see change 1).
- I modified or created no file, and this time no plan file either.

## Check of each change

**1. Definition of π (STATEMENT §1; PROOF §0 "Prior and target"; Lemma 1.2). Correct.**
- The formula in §0 matches STATEMENT §1 term by term:
  - y = Cy^r/s_y and z_S = X_S^⊤y;
  - Q^{v3}_S = y^⊤y − n z_S^⊤H_S^{-1}z_S;
  - a₀ = b₀ = 0.01;
  - m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{-1/2}(2b₀+Q^{v3}_S)^{-ν};
  - π = ϖm/Σ_Ω ϖm (= e^F/Z).
- The prefactor does not depend on S, and m(S) > 0 because D_S ≥ 1 and Q^{v3}_S ≥ 0.
- I checked Lemma 1.2 by hand:
  - Cy^r = UU^⊤y^r = Uy_c, so y = Uy_c/s_y and y^⊤y = ‖y_c‖²/s_y².
  - X_S = UZ_S, so z_S = Z_S^⊤y_c/s_y and n z_S^⊤H_S^{-1}z_S = y_c^⊤M_S y_c/s_y².
  - Hence Q^{v3}_S = Q_S/s_y², and 2b₀ + Q^{v3}_S = (2b + Q_S)/s_y².
  - The factor s_y^{2ν} does not depend on S, and both laws are normalised over the same Ω. This gives exactly Lemma 1.1(a).
- Numerical check: on a random design with n = 9, p = 5, K = 4 (all 31 models in Ω), I computed π from the v3 formula (including its constant) and the S-marginal from Lemma 1.1(a). The largest difference was 2.8·10⁻¹⁶.
- Lemma 1.1 is unchanged, and I rechecked it: Sylvester's identity, Woodbury's identity, 0.51 + N/2 = ν, and the conditionals (b) and (c).
- CW-F1 and my round-1 F1 are closed.

**2. The note in Prop 4.1 ("the same estimates give e^{−3ℓ_n}"). Correct.**
- log(π(S)/π(S₀)) < log ϖ(S) + (2s₀+1)ℓ_n + s₀ℓ_n − (3s₀+4)ℓ_n = log ϖ(S) − 3ℓ_n.

**3. Remark 9.1. Correct.**
- §§1–5 never use p ≤ n^A:
  - Lemma 3.2 needs only log 2 ≤ ℓ_n, log p ≤ ℓ_n and ℓ_n ≥ log n.
  - Prop 4.1 needs −log ϖ(S₀) ≤ (2s₀+1)ℓ_n.
- p ≤ n^A enters in §7, in three places:
  - ℓ_n ≤ A log n;
  - m_n ≤ 5(s₀+1)A log n, which is needed for n₁ (m_n + s₀ ≤ ⌊n/2⌋);
  - the conversion cost (2p)^{s₀}.
- It also enters through H-T02 in §§6–8.
- b enters through Lemma 1.1(b), Lemma 1.2 and (4), with both bounds 0 < 2b ≤ b̄ and 2b + Q_S ≤ nB. Prop 7.3 also uses b > 0, which (4) covers.

**4. Renames and the Notation paragraph. Consistent.**
- A grep finds no leftover θ_n, ξ_j, τ_k (as the Lemma 3.2 quantity), η (as the §6 tolerance) or Γ (as the Gamma variable).
- ϑ_n, ζ_j, t_k, ε₀ and Υ are used consistently at every occurrence.
- Two remaining imprecisions are minor (Findings 2 and 3).

**5. "If n ≥ 8" in Theorem 5.1(ii), and G added to §7 and Theorem 7.4. Correct and harmless.**
- Both applications use u′_n = min{u_n, √(n/8)} ≥ 1 for large n, which already forces n ≥ 8.
- The proof steps u ≤ √(n/8) ≤ √ν/2 and 1/n ≤ u/√n are unchanged.

**6. Ξ̄_n in Theorem 7.4. Correct.**
- Ξ̄_n := E₀Ξ_n is finite, because Ξ_n is a finite sum of truncated (bounded) terms. The displayed quantity is a bound on it.
- If Ξ̄_n = 0, then Ξ_n = 0 a.s. and Step 4 is trivial.
- Otherwise Markov's inequality at √Ξ̄_n gives P₀(Ξ_n > √Ξ̄_n) ≤ √Ξ̄_n.
- The phrase "log Ξ̄_n → −∞" should strictly be read as a statement about the bound. This is harmless.

## Re-confirmation of the rest

The mathematics is unchanged from v1. I re-derived it independently of my round-1 notes.
- **§0:** U^⊤ = U^⊤C, y_c = μ_c + e, and (1).
- **Lemma 1.3(a)–(d):** including the Beta identity and the bound ∏(i+1)/(2p−1−i) ≤ ((s₀+j)/p)^j.
- **Lemma 2.1(a)–(i):**
  - the ridge variational form, and a_S ≤ δ for S ⊇ S₀;
  - the Schur ratio (3), R₂ ⪯ R₁, and interlacing;
  - (g) via (n+1)N ≥ n;
  - (h) via R₂ ⪰ R₀ ⪰ Nφ₀² and det(R₁+I) ≤ (N(j+1))^j.
- **Lemmas 3.1–3.2:**
  - E e^{ξ/4} = 2^{r/2};
  - the constant 14;
  - the union bounds 1/n and 4/n;
  - 2/N ≤ 3/n;
  - b̄ = 8b₀(M+2σ⋆²);
  - (1+2b₀/N) ≤ 1+b₀ (N ≥ 3).
- **Prop 4.1:**
  - both AM–GM steps;
  - C₁ = 22σ⋆² + 2δ̄;
  - log(1+x) ≥ x/(1+x);
  - νΔ_S/(2b+Q_S) ≥ c₀Δ_S;
  - c₀Δ_S > [3(s₀+1)+1]ℓ_n.
- **Theorem 5.1(i):**
  - C_b and C_f;
  - Z_Sθ_S − M_S y_c ~ N(0, vM_S);
  - E[v|S,y] = (2b+Q_S)/(n−1.98);
  - the Markov bound 2B/ℓ_n.
- **Theorem 5.1(ii):**
  - C_c, C_d and C_e;
  - 2ν = N + 1.02;
  - Υ ~ Gamma(ν,1) and Υ ≥ ν/2;
  - |ν/Υ − 1| ≤ 2√2u/√n ≤ 1.
- **§6:** Lemma 6.1 (2.5/log 2 < 3.61), and the proofs of (i) and of (iii) under G, R, including the truncation u′_n.
- **§7:**
  - n₁ and (7);
  - Lemma 7.1;
  - Lemma 7.2 (Γ(x+1) ≥ x^x e^{−x});
  - ϑ_n, and η_n = (1.02 + Nϑ_n)/(N(1−ϑ_n)) ≤ 2ϑ_n + 2.04/N, so η_nℓ_n → 0;
  - Prop 7.3: the prior, Occam, fit and denominator steps (Nσ⋆²(1−ϑ_n) > 0), the assembly with the indicator, and the constant 28e³;
  - Theorem 7.4: the 2^{s₀}-to-one map, κ_n with 168, ψ_j ≤ (α_n+β_n)j + γ_n, the geometric tail, the log-n coefficient −½[(j₀+1) − s₀(2A+1)] ≤ −½, and Step 4.
- **§8:**
  - (11);
  - (ii), the prediction part and the coefficient part (SE on T = S∪S₀ with |T| < m_n + s₀, and n/N ≤ 2);
  - (iii) under SE;
  - (iv);
  - the constant (12).

The proved claims match STATEMENT.md exactly:
- (i)–(iv) hold with "→ 0" in P₀-probability.
- Every deterministic u_n → ∞ is covered.
- C depends only on (σ⋆², M, φ₀, A), with b₀ fixed. It does not depend on s₀, p_n or u_n.
- Π† is used only through its definition, and its S-marginal is shown to equal π.
- H-T02 is used only in the form Π(|S| > m_n | y) → 0, with ω_n = ½ log n.
- No beta-min condition is used.

## Findings

**F1. Notation in STATEMENT.md §1 versus PROOF_v2 §0 and §1. Severity: exposition.**
- **Claim:** The newly quoted definition in STATEMENT §1 uses notation that the proof uses differently.
  - "Q_S" in STATEMENT §1 is the v3 standardised quantity, which the proof calls Q^{v3}_S. The proof's Q_S := y_c^⊤(I − M_S)y_c equals s_y²·Q^{v3}_S.
  - "Z" in STATEMENT §1 is the normaliser Σ_Ω ϖm. In the proof, Z := U^⊤X.
  - §0 now defines y := Cy^r/s_y, while Π†(·|y) is the posterior given y_c. This y does not determine y_c, since ‖y‖² = N always. So the "| y" in Π† is a label, not conditioning on this y.
- **Evidence:** The proof itself is consistent. It writes Q^{v3}_S throughout §0 and Lemma 1.2, and it never uses Z as the normaliser. No step is affected. One sentence in §0 or in STATEMENT §1 ("Q_S there = Q^{v3}_S here") would prevent cross-reading errors.

**F2. PROOF_v2 §0, the Notation paragraph. Severity: exposition.**
- **Claim:** The paragraph says "no confusion arises, since the centring matrix appears only in §0–§1". But the theorem constant C also appears in §0 (in the claim paragraph), so both meanings occur in §0.
- **Evidence:** The centring matrix appears only in §0 and in Lemma 1.2 (checked by grep). The context disambiguates every use.

**F3. Overloads left over or introduced by the renames. Severity: exposition.**
- **Claim:**
  - ζ_j (the deterministic bound in §7) now shares its letter with the Gaussian variable ζ ~ N(0,s²) in Lemma 3.1(b).
  - t_k (Lemma 3.2, a scalar) sits next to the ridge vector t ∈ ℝ^k of Lemma 2.1(b) and (f).
  - e denotes the noise vector, Euler's number (e^{−ℓ_n}, 28e³) and the basis vectors e_i in Lemma 2.1(a). The Notation paragraph does not list it.
- **Evidence:** All uses are local and unambiguous in context. No error results.

## Conclusion

All six changes are correct and introduce no mathematical error. In particular:
- the definition of π in §0 matches STATEMENT §1;
- Lemma 1.2 derives Lemma 1.1(a) from it exactly, which I confirmed by hand and numerically;
- CW-F1 is resolved.

Every other step re-checks as in round 1. The three findings are exposition only. There are no fatal or gap findings.

VERDICT: verified
