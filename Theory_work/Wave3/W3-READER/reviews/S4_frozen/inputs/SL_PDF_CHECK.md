# SL_PDF_CHECK: claims about Song & Liang (2015) checked against the published PDF

- **Paper:** Song, Q. and Liang, F. (2015), "A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression", *J. R. Statist. Soc. B* 77(5), 947–972.
- **File:** `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/32_2015_Song_Liang_A_split_and_merge_Bayesian_variable_selection_approach_for_ultrahigh_dimensional_regression.pdf` (26 PDF pages, no supplement).
- **Page convention:** all page numbers are **journal pages** (printed running heads). Journal page = PDF page + 946 (p. 950 = PDF p. 4).
- **Method:** `pdftotext -layout` to stdout, plus visual rendering of journal pp. 950–957 to read the symbols (≺, ≻, ε_n, ∉) that pdftotext drops. The quotes are transcribed from the rendered pages. Math is typed in plain Unicode.
- **Date:** 2026-11-16. Read-only check. No other files were written.
- **Notation (p. 950):** "where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0". So a_n ≺ b_n means a_n = o(b_n).
- **Not checked:** the online supplement (the proofs, Theorem S on MAP consistency, Lemma 1.2) is not in this PDF.

---

### S1. Hellinger distance on the joint (x, y) density, with the x-marginal shared
**VERDICT: MATCH**
- p. 950, eq. (2): "f*(y, x) dx dy = … = φ(y; xᵀβ*, σ*) ν_x(dx) dy", with "Let ν_x denote the probability measure of x."
- p. 952, §2.1.2: "For two density functions f₁(x, y) and f₂(x, y), the Hellinger distance is defined as d(f₁, f₂) = √( ∫∫ {f₁^{1/2}(x, y) − f₂^{1/2}(x, y)}² dx dy )."
- p. 952, Theorem 1 (after (15)): "d²(f, f*) = ∫∫ |φ^{1/2}(y; xᵀβ*, σ*) − φ^{1/2}(y; xᵀβ, σ)|² ν_x(dx) dy", where "f is the density function for a model simulated from the posterior".
- **Note:** their d has no factor ½. So d² = ∫(√f − √f*)² = 2 − 2∫√(f f*) = **2 d_H²** under our d_H² := 1 − ∫√(fg). Equivalently d = √2 · d_H. Both densities use the same ν_x, so the x-marginal is shared.

### S2. The forms of (15) and (16), and the conditions each needs
**VERDICT: PARTLY.** The forms match exactly. The attribution "(15) under Condition 1" is not exact.
- p. 952, Theorem 1, eq. (15): "P*[π{d(f, f*) > ε_n | D_n} > exp(−c₁nε_n²)] < exp(−c₁nε_n²)", "for sufficiently large n".
- p. 953, Theorem 2 (same display, **unnumbered**): "P*[π{d(f, f*) > ε_n | D_n} > exp(−c₁nε_n²)] < exp(−c₁nε_n²)."
- p. 954, eq. (16): "lim_{n→∞} P*[π{d(f, f*) > ε_n | D_n} > exp(−c₁nε_n²)] = 0." It is introduced by: "if condition 2 holds, a slightly weaker result of theorem 2 can be obtained as follows". The proof is in the supplement. It is not a numbered theorem.
- **Conditions:**
  - (15) is stated **inside Theorem 1**: bounded predictors "|x_i| ≤ 1", approximate sparsity (3), and conditions (8)–(14).
  - The Condition-1 version is the unnumbered display of Theorem 2. It needs (4), (9)–(14) and r_n ≻ 1.
  - (16) inherits Theorem 2's setting, with Condition 1 replaced by Condition 2.
- **Proposed wording:** "(15) (Thm 1: bounded predictors, (3), (8)–(14)), and its unnumbered analogue in Thm 2 (Condition 1, (4), (9)–(14), r_n ≻ 1); (16): the limit form under Condition 2 (second moments), with Thm 2's other conditions."

### S3. The prior family, and why BB(1, p) capped at min(p, ⌊n/2⌋) is not covered
**VERDICT: PARTLY.** The conclusion holds: BB(1, p) is not covered. One part of the description of their prior is wrong ("slab with envelopes").
- p. 951, §2.1.1, eq. (6):
  - "each predictor has a prior probability λ_n = r_n/P_n, independent of other predictors, to be included in the model ξ."
  - "|ξ| ≤ r̄_n, where the upper bound r̄_n is prespecified"
  - "π(ξ) ∝ λ_n^{|ξ|}(1 − λ_n)^{P_n−|ξ|} I(|ξ| ≤ r̄_n)."
- p. 951: "σ² ∼ IG(a₀, b₀)" and "β_ξ | ξ, σ² ∼ N_{|ξ|}(0, σ²V_ξ), where V_ξ is a positive definite matrix depending on ξ."
- p. 952, Theorem 1 conditions:
  - (9) "r̄_n ln(1/ε_n²) ≺ nε_n²"
  - (10) "r̄_n ln(P_n) ≺ nε_n²"
  - (11) "r̄_n ln(nε_n² B̃_n) ≺ nε_n²"
  - (12) "1 ≤ r_n ≤ r̄_n < P_n"
  - (13) "r_n ≺ P_n"
  - (14) "B(r_n) ≺ nε_n²"
  - Here B(r_n) = sup_{|ξ|=r_n} ch₁(V_ξ⁻¹) and B̃_n = sup_{|ξ|≤r̄_n} ch₁(V_ξ) are the largest eigenvalues.
- p. 953, Theorem 2 adds: "and r_n ≻ 1".
- p. 951: the cap "can be removed by imposing an additional condition, say, there exists r̄_n such that π(|ξ| > r̄_n) → 0 with an appropriate rate". This is a remark that points to Jiang (2007), §7. It is not proved here.
- p. 951: "For a fully Bayesian variable selection approach, λ_n is usually subject to a beta prior". However, they then "assume that λ_n → 0". No theorem covers a beta mixture over λ_n.
- **Why our reading holds:**
  - Take r̄_n = ⌊n/2⌋. Then (10) would need ε_n² ≫ ln P_n, which is impossible. (9) would need ε_n²/ln(1/ε_n²) → ∞, which is impossible for ε_n < 1.
  - (11) fails for any V_ξ with B̃_n bounded below. The paper's examples, cI and the ridge prior, both are.
  - The mean model size under BB(1, p) is p/(p+1) = O(1). This is the analogue of r_n, so "r_n ≻ 1" fails.
  - (6) has a deterministic λ_n. It is not a beta-binomial.
- **Correction:** their slab is not "a slab with envelopes". It is the conjugate Gaussian N(0, σ²V_ξ) with σ² ∼ IG(a₀, b₀). It is controlled only through the eigenvalue bounds B(r_n) and B̃_n in (11) and (14).
- **Proposed wording:** "one prior family: independent Bernoulli(r_n/P_n) inclusion, hard cap |ξ| ≤ r̄_n, conjugate N(0, σ²V_ξ) slab with σ² ∼ IG, subject to (9)–(14) [(8) also for Thm 1]".

### S4. At polynomial p, Theorem 2 gives ε_n² = ω_n log n / n
**VERDICT: PARTLY.** The reduction is right for the main term but drops (14), (11) and (12)–(13).
- p. 953, Theorem 2: "Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds".
- The conditions (9)–(14) are listed under S3 (p. 952).
- **Check, for P_n polynomial:**
  - By the standing assumption P_n ≻ n^θ, ln P_n ≍ log n. So (10) becomes r̄_n log n ≺ nε_n².
  - (9) follows from (10), because ln(1/ε_n²) ≤ ln n once nε_n² ≥ 1.
  - (11) also follows from (10) when B̃_n is at most polynomial in n.
  - **(14) B(r_n) ≺ nε_n² is a separate condition.** With B(r_n) ≤ B r_n^v and v > 1, it does not follow from r̄_n log n ≺ nε_n². It is automatic for V_ξ = cI, where B(r_n) is constant.
  - So ε_n² = ω_n log n / n with ω_n/r̄_n → ∞. Since r̄_n ≥ r_n → ∞, ω_n → ∞. Also need ε_n → 0, i.e. r̄_n log n = o(n).
- **Proposed wording:** "any ε_n → 0 with r_n → ∞, r_n ≤ r̄_n < P_n, r_n = o(P_n), r̄_n log n = o(nε_n²) and B(r_n) = o(nε_n²) (and (11), automatic if B̃_n is polynomial in n); i.e. ε_n² = ω_n log n/n with ω_n/r̄_n → ∞."

### S5. Corollary 1 rate: ε_n² or ε_n?
**VERDICT: PARTLY.** The printed display is for **ε_n**, not ε_n², and it has **no equation number**. Squaring it gives our ε_n² (as an O-bound).
- p. 954, Corollary 1:
  - "Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ Br_n^v and B̃_n ≤ Bn^v for some positive constants B and v."
  - "Take r_n < r̄_n ≺ log^k(n), or r_n < r̄_n ≺ n^q, for some k > 0 or some 0 < q < min{1 − α, 1/v}."
  - "Then the convergence rate in theorem 2 can be taken as ε_n = O{n^{−(1−α)/2} log^{k/2}(n)}, or ε_n = O(n^{−(min{1−α−q, 1−vq})/2})."
- **Proposed wording:** "Corollary 1 (p. 954, unnumbered display) gives ε_n = O{n^{−(1−α)/2} log^{k/2} n}, i.e. ε_n² = O{n^{−(1−α)} log^k n}, under P_n < exp(Cn^α), r_n < r̄_n ≺ log^k n, B(r_n) ≤ Br_n^v, B̃_n ≤ Bn^v."

### S6. Dimension: p up to exp(Cn^α), and P_n ≻ n^θ
**VERDICT: MATCH**
- p. 950: "we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0." This is a lower growth bound. It is a standing assumption of §2.1, not part of the theorem statements.
- p. 954, Corollary 1: "Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1)".
- **Note:** exp(Cn^α) appears **only in Corollary 1**. Theorems 1–2 limit P_n only through (10), "r̄_n ln(P_n) ≺ nε_n²", together with (12)–(13). Since ε_n → 0 and r̄_n ≥ 1, this forces ln P_n = o(n).

### S7. Theorem 1 covers approximate sparsity with bounded predictors; Theorem 2 is for strict sparsity
**VERDICT: MATCH**
- p. 950, eq. (3): "lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞". Eq. (4): "lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞".
- p. 952: "Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds."
- Theorem 1 itself states "all predictors |x_i| ≤ 1" and "(8) Δ(r_n) ≺ ε_n", where "Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|".
- p. 953, Theorem 2: "the model is strictly sparse, i.e. condition (4) holds".
- (3) appears in the sentence that introduces Theorem 1, not inside the theorem statement.

### S8. Tail conditions on the predictors
**VERDICT: MATCH**
- p. 952, Theorem 1: "all predictors |x_i| ≤ 1".
- p. 953, Condition 1: "There are some constants M > 0 and δ > 0 such that for any subvector of x, (x_{j₁}, …, x_{j_r})ᵀ with 1 ≤ j₁ < … < j_r ≤ P_n, r ≤ r̄_n, and |a_i| ≤ δ …, we have E[exp{(Σ_{i=1}^r a_i x_{j_i}/r)²}] ≤ exp(M)".
- p. 954, Condition 2 (same quantifiers): "E(Σ_{i=1}^r a_i x_{j_i}/r)² ≤ M." The paper adds: "Condition 2 imposes conditions on only the second moments of predictors."

### S9. The true model size s may grow with n
**VERDICT: MISMATCH**
- p. 950, eq. (4) and the text after it: "the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size."
- p. 953–954: "condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4)."
- **Theorems 2–3 and Corollary 1:** (4) requires lim Σ 1{β*_j ≠ 0} < ∞. A finite limit of an integer sequence means |t| is eventually constant. So **s does not grow**. The paper has no "|ξ*| ≤ r_n"-type condition. "r_n > |t|" is a consequence of r_n ≻ 1 with |t| bounded.
- **Theorem 1:** under (3), the number of nonzero β*_j may grow. However, the ℓ₁ norm must have a finite limit, and the ℓ₁ mass outside the best r_n coordinates must be o(ε_n) by (8). This is approximate sparsity with bounded ℓ₁ norm, not a growing support s_n.
- **Theorem 4 / Corollary 2:** a fixed subset s; the size of the true model plays no role.
- **Proposed wording:** "In SL Thms 2–3/Cor 1 the true model size is bounded (|t| finite by (4)); only Thm 1 (approximate sparsity (3), bounded predictors) allows a growing number of nonzero coefficients, with Σ|β*_j| bounded and Δ(r_n) = o(ε_n)."

### S10. No design-geometry condition in Theorems 1–2; identifiability (Condition 3) only for selection
**VERDICT: PARTLY.** It is true that Theorems 1–2 have no condition on the design or population covariance, and no identifiability condition. But they **do** contain eigenvalue conditions, on the *prior* covariance V_ξ.
- p. 952: "Define B(r_n) = sup_{ξ:|ξ|=r_n} ch₁(V_ξ⁻¹), … B̃_n = sup_{ξ:|ξ|≤r̄_n} ch₁(V_ξ)". These enter through (11) and (14).
- p. 953: "The validity of this theorem depends on the choice of the prior covariance matrix V_ξ or, more precisely, the largest eigenvalues of V_ξ and V_ξ⁻¹."
- If V_ξ⁻¹ = E(x_ξᵀx_ξ) (ridge or g-type), these become bounds on the population covariance (p. 953).
- p. 955, Condition 3: "A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j₁, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ, E[exp{−(x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i})²}] ≤ 1 − δ_n, δ_n ≻ ε_n²". It is used in Theorem 3 (p. 956).
- **Proposed wording:** "Thms 1–2 impose no eigenvalue/identifiability condition on the design (only tail/moment conditions on x and eigenvalue bounds on the prior covariance V_ξ via (11), (14)); identifiability (Condition 3) enters only Thm 3."

### S11. Exact posterior only; nothing about sampler output; no parametric rate
**VERDICT: MATCH**
- Every theorem (1–4, Corollaries 1–2) is stated for the posterior π(· | D_n) or π(· | D_n^s).
- SAMC is described only computationally. p. 959: "the stochastic approximation Monte Carlo (SAMC) algorithm (Liang et al., 2007) was used in this paper." No theorem covers the output of SAMC or MCMC.
- The supplement, §2, "describes the SAMC algorithm and its implementation" (p. 970–971). The theory in the supplement consists of the proofs of Theorems 1–4 and the MAP consistency result.
- The only statement about the SAM procedure as a whole is informal. p. 959: "Clearly, it follows from the theory that was developed in Section 2 that the SAM approach will lead to a consistent selection of true predictors." Also p. 969: "the SAM approach does not work in a standard Bayesian way".
- **No parametric rate:**
  - Theorem 1 requires "nε_n² ≻ 1" and Theorem 2 requires "nε_n² → ∞", so ε_n ≫ n^{−1/2}.
  - Corollary 1's best rate is n^{−(1−α)/2} up to logarithmic factors, with α > 0.
  - Theorem 4 is for a fixed ε > 0, with no rate.

### S12. Theorem 4 and Corollary 2: the misspecified (omitted-predictor) setting
**VERDICT: PARTLY.** The Hellinger consistency around the KL minimizer and the screening statement match. "Omitted-**Gaussian**-predictor" is not the paper's setting. The paper calls the candidate-only model misspecified and never says it is correctly specified.
- p. 956:
  - "Let D_n^s = {y, X_s} denote a fixed subset …"
  - "Assume that X_s does not include all of the true predictors of model (1). Therefore, the model y = X_s β_s + ε is misspecified."
  - "It is obvious that f* ∉ P_s."
  - Eq. (17): "f₀ = arg min_{f∈P_s} ∫ ln(f*/f) f*".
- p. 957:
  - "To prove theorem 4, π(ξ) does not need to be specified, which is only required to be positive for all possible models".
  - Condition 4: "E{(aᵀx_s)²} < ∞". This is a second-moment condition only. There is no Gaussian assumption on x.
- p. 957, Theorem 4: "Assume that condition 4 holds for a given subset s. Under the prior setting as described above, for any ε > 0, π[{f ∈ P_s : d(f₀, f) > ε} | D_n^s] → 0, almost surely, (18)".
- p. 957: "f₀ = φ(y; β₀ᵀx_s, σ₀) ν(x_s)" (citing supplement Lemma 1.2), with "β₀ = arg min_{β_s} E(β_sᵀx_s − β*ᵀx)²".
- p. 957, Corollary 2: "If x_s does not have exact multicollinearity … then … π(s̃ ⊂ ξ | D_n^s) →ᵖ 1", where "s̃ denote[s] the subset of s corresponding to non-zero entries of β₀". This statement holds in probability, for a fixed s, with no rate.
- **Correct specification:** the paper does not claim that the conditional model of y given x_s is Gaussian-linear. This would hold only if E[x_{t∖s} | x_s] were linear and the residual Gaussian and homoscedastic, for example when the omitted predictors and x_s are jointly Gaussian. The paper does not impose this.
- **Proposed wording:** "SL Thm 4/Cor 2: fixed candidate subset s missing some true predictors (model explicitly misspecified, f* ∉ P_s), x_s with finite second moments; posterior Hellinger-consistent at the KL projection f₀ = φ(y; β₀ᵀx_s, σ₀)ν(x_s) (fixed ε, a.s., no rate); Cor 2: π(s̃ ⊂ ξ | D_n^s) →ᵖ 1. The candidate-only conditional model is correctly specified only under extra (e.g. joint-Gaussian) assumptions that SL do not make."

### S13. Theorem 3 (sure screening): sensitivity → 1, for dimension up to e^{Cn^α}
**VERDICT: PARTLY.** The conclusion and the condition names match. The dimension "up to e^{Cn^α}" is not stated in Theorem 3; it comes from Corollary 1.
- p. 956, Theorem 3 (sure screening): "Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c₁nε_n²)] < exp(−c₁nε_n²)". It adds: "Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[…] = 0."
- p. 956: "it follows from theorem 3 that π(t ⊂ ξ_q) →ᵖ 1 if all true predictors are identifiable."
- p. 956: "theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled)". MAP consistency is Theorem S, in the supplement (not checked).
- The conditions are: Theorem 2's conditions (Condition 1, (4), (9)–(14), r_n ≻ 1), plus Condition 3 (identifiability) for x_t. Condition 2 gives the limit form.
- **Proposed wording:** "SL Thm 3: under Thm 2's conditions plus identifiability (Condition 3), each identifiable true predictor has posterior inclusion probability ≥ 1 − e^{−c₁nε_n²} w.p. ≥ 1 − e^{−c₁nε_n²} (sensitivity → 1; specificity not controlled); the dimension is limited by (10), r̄_n ln P_n = o(nε_n²), which allows P_n up to exp(Cn^α) as in Cor 1."

---

## MISMATCHES

| Item | Verdict | Proposed corrected wording |
|---|---|---|
| S2 | PARTLY | (15) is Thm 1's display (bounded predictors, (3), (8)–(14)). Thm 2 restates the same form, unnumbered, under Condition 1 + (4) + (9)–(14) + r_n ≻ 1. (16) is the limit form under Condition 2 with Thm 2's other conditions. |
| S3 | PARTLY | Prior = independent Bernoulli(r_n/P_n) inclusion, hard cap \|ξ\| ≤ r̄_n, conjugate N(0, σ²V_ξ) slab with σ² ∼ IG, under (9)–(14) (and (8) for Thm 1); not a "slab with envelopes". The BB(1, p) conclusion stands. |
| S4 | PARTLY | Any ε_n → 0 with r_n → ∞, r_n ≤ r̄_n < P_n, r_n = o(P_n), r̄_n log n = o(nε_n²) **and B(r_n) = o(nε_n²)** ((11) is automatic if B̃_n is polynomial). So ε_n² = ω_n log n/n with ω_n/r̄_n → ∞. |
| S5 | PARTLY | Cor 1 (p. 954, unnumbered) prints ε_n = O{n^{−(1−α)/2} log^{k/2} n}, i.e. ε_n² = O{n^{−(1−α)} log^k n}. |
| S9 | MISMATCH | In Thms 2–3 and Cor 1 the true model size is bounded (\|t\| finite by (4)). Only Thm 1 (approximate sparsity (3)) allows a growing number of nonzeros, with Σ\|β*_j\| bounded and Δ(r_n) = o(ε_n). |
| S10 | PARTLY | No eigenvalue/identifiability condition on the design in Thms 1–2. There are eigenvalue bounds on the prior covariance V_ξ ((11), (14)) and tail/moment conditions on x. Condition 3 enters only Thm 3. |
| S12 | PARTLY | The setting is a fixed candidate subset missing true predictors; the model is explicitly misspecified (f* ∉ P_s), with only second moments on x_s (no Gaussian assumption). Thm 4 gives consistency at the KL projection (fixed ε, a.s.). Cor 2 gives π(s̃ ⊂ ξ \| D_n^s) →ᵖ 1. Correct specification of the conditional model is not claimed. |
| S13 | PARTLY | Thm 3 (Thm 2's conditions + Condition 3) gives sensitivity → 1 only. e^{Cn^α} is not in Thm 3; it comes via (10) / Cor 1. |

S1, S6, S7 and S8 are MATCH. S11 is MATCH: every result is about the exact posterior, none about sampler output, and none has a parametric rate.
