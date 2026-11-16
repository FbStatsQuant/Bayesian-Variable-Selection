# SL_PDF_CHECK_card: claims-card sentences about Song & Liang (2015), checked against the published PDF

- **Paper:** Song, Q. and Liang, F. (2015), "A split-and-merge Bayesian variable selection approach for ultrahigh dimensional regression", *J. R. Statist. Soc. B* 77(5), 947–972.
- **File:** `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/32_2015_Song_Liang_A_split_and_merge_Bayesian_variable_selection_approach_for_ultrahigh_dimensional_regression.pdf` (no supplement).
- **Page convention:** journal pages (printed running heads). Journal page = PDF page + 946.
- **Method:** `pdftotext -layout` to stdout, plus visual rendering of journal pp. 947, 955, 956 to read symbols that pdftotext drops (≫, ≻, ≤, ∉). Quotes were reused from `SL_PDF_CHECK.md` (S-items) only after re-reading them in the PDF. Math is typed in plain Unicode.
- **Date:** 2026-11-16. Read-only check. Only this file was written.
- **Notation (p. 950):** "b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0", so a ≺ b means a = o(b).
- **Not checked:** the online supplement (proofs, Theorem S on MAP consistency, Lemma 1.2) is not in this PDF.
- **Scope:** only what each sentence says about Song–Liang (SL) is judged. Claims about our own results are taken as given.

---

### C1. Row 1.1 (:41): "Song–Liang-type selection consistency for the shipped prior with an explicit, design-uniform expectation rate and exact HPM/MPM; no tuning"
**VERDICT: PARTLY.** SL's main-text selection theorem (Theorem 3) is **sure screening only**. It controls the marginal inclusion probability of each identifiable true predictor; specificity is not controlled. Full-model (MAP = HPM) consistency is in the supplement only (Theorem S, not checked). SL have no expectation statement, no MPM result, and no result on π(t | D_n) for the whole true model. So "Song–Liang-type selection consistency" undersells the difference: our row is a full-model result, theirs is sensitivity only.
- p. 956, Theorem 3 (sure screening): "Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c₁nε_n²)] < exp(−c₁nε_n²)".
- p. 956, same theorem: "Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c₁nε_n²)] = 0."
- p. 956: "Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection."
- p. 956: "Theorem S in the on-line supplementary material establishes the consistency of MAP models." Also: "the MAP model might not capture all true predictors although it is consistent in theory."
- **MPM:** SL threshold the inclusion probabilities at a q chosen by multiple testing, not at 1/2. p. 956: "Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} … To determine the threshold value q, we adopt the multiple-hypothesis testing procedure that was used in Liang et al. (2013)".
- **Rate:** Theorem 3 has an explicit exponential form, exp(−c₁nε_n²), with c₁ unspecified. Its ε_n is limited by (9)–(14) (strictly slower than √(log n/n); see C6). It is a high-probability statement, not an expectation. (An expectation bound per predictor would follow trivially, but SL do not state one.)
- **Tuning (contrast only):** p. 959: "The prior distribution of the SAM approach contains an important hyperparameter, namely r_n." There is also rule (20) for γ (p. 959) and FDR levels α₁, α₂ at the two stages (p. 959).
- **Proposed wording:** "Full-model selection consistency (SL Thm 3 gives sure screening only: sensitivity → 1, specificity not controlled; MAP consistency only in their supplement) for the shipped prior, with an explicit, design-uniform expectation rate and exact HPM/MPM; no tuning".

### C2. Row 1.1 (:41): "Thm 1′ uses a residual-signal identifiability condition (Narisetty–He style) instead of eigenvalue floors off the truth." (implicit claim about SL)
**VERDICT: PARTLY.** If the line is read as contrasting with SL, it is misleading. SL's selection theorem already uses an **identifiability condition** (Condition 3), not an eigenvalue floor. SL give an eigenvalue floor only as a **sufficient** condition for Condition 3. SL's Theorems 1–2 have no design eigenvalue condition at all; their eigenvalue bounds are on the prior covariance V_ξ (see `SL_PDF_CHECK.md` S10).
- p. 955, Condition 3: "A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j₁, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ, E[exp{−(x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i})²}] ≤ 1 − δ_n, δ_n ≻ ε_n²".
- p. 955: "This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it."
- p. 955 (sufficient condition, bounded mean-zero predictors): "Hence, if ch′₁{var(x̃)} ≻ r̄_n ε_n² for any choice of x̃, x_t is identifiable." Here ch′₁ is the smallest eigenvalue and x̃ = (x_k, x_{j₁}, …, x_{j_{r̄_n}})ᵀ.
- p. 956 (Gaussian predictors): "all predictors are identifiable if ch′₁{var(x)} ≻ ε_n²."
- **What Condition 3 requires:** a population condition (an expectation over the random x). It is imposed per true predictor x_t against every set of r̄_n other predictors, with margin δ_n ≻ ε_n². Theorem 3 requires it only for the true predictor whose inclusion it controls. It is the same idea as ours ("no small set of other columns mimics a truth"). It is stated at the population level, not as a residual-signal bound on the sample design.
- **Proposed wording:** "Thm 1′ replaces eigenvalue floors off the truth by a residual-signal identifiability margin (Narisetty–He style; cf. SL's population-level identifiability Condition 3 for their Thm 3)."

### C3. Row 1.1 (:41): "Narrower in dimension ($n^A$ vs $e^{Cn^\alpha}$)."
**VERDICT: MATCH** (in substance). The citation should point to Corollary 1 and (10), not to Theorem 3.
- p. 954, Corollary 1: "Consider a strict sparse model, i.e. condition (4) holds. Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ Br_n^v and B̃_n ≤ Bn^v". It continues: "Then the convergence rate in theorem 2 can be taken as …".
- p. 952, Theorem 1, (10): "r̄_n ln(P_n) ≺ nε_n²". This is the only place the dimension enters Theorems 1–3. With ε_n → 0, it forces ln P_n = o(n).
- p. 956, Theorem 3: "Assume that all the conditions of theorem 2 hold." Theorem 3 does not mention P_n itself.
- **Does Theorem 3 hold up to e^{Cn^α}?** Yes, by combination, but SL do not state it. Corollary 1 shows that Theorem 2's conditions hold for P_n < exp(Cn^α), with ε_n² = O{n^{−(1−α)} log^k n}. Theorem 3 assumes exactly Theorem 2's conditions. It therefore applies in that regime, provided the predictor satisfies Condition 3 with δ_n ≻ ε_n² for that ε_n.
- **Citation to use:** "SL Cor 1 (p. 954): P_n < exp(Cn^α), α ∈ (0, 1), via (10); their Thm 3 inherits this through Thm 2's conditions."
- **Proposed wording (citation precision only):** "Narrower in dimension ($n^A$ vs SL's $P_n<e^{Cn^\alpha}$, $\alpha<1$: Cor 1 via (10), inherited by Thm 3)."

### C4. Row 1.2 (:42): "Song–Liang's random-design setting; $p\gg n$."
**VERDICT: MATCH.**
- p. 950: "Let D_n = {y; x₁, …, x_{P_n}} denote a data set of n observations drawn from model (1). Let x = (x₁, …, x_{P_n})ᵀ denote a generic observation of the P_n predictors … Let ν_x denote the probability measure of x."
- p. 950, (2): "f*(y, x) dx dy = … = φ(y; xᵀβ*, σ*) ν_x(dx) dy".
- p. 947: "In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh."
- p. 950 (standing assumption): "we assume that P_n ≻ n^θ for some θ > 0".
- **Notes:**
  - SL never write "i.i.d." The rows are "n observations drawn from model (1)" with a common law ν_x, and independence is implicit.
  - SL do not assume Gaussian x. They use bounded predictors (Thm 1), Condition 1 (exponential moments, Thm 2) or Condition 2 (second moments, (16)). p. 953: "If x follows a Gaussian process with zero mean and var(x_i) = 1, … condition 1 holds."
  - So our i.i.d. Gaussian rows are a special case of SL's setting.
- **Optional precision (not required):** "Song–Liang's random-design setting (rows i.i.d.; here Gaussian, theirs any law under their Conditions 1/2); $p\gg n$."

### C5. Row 1.4 (:44): "Analogue of Song–Liang (2015) Theorem 4 and Corollary 2 in their omitted-Gaussian-predictor setting, where the candidate-only conditional model is correctly specified: exact selection of the best candidate predictor's support with rate $\sqrt{\log n/n}$, no condition on how Σ, β, σ² vary with n"
**VERDICT: MISMATCH** (re-confirms `SL_PDF_CHECK.md` S12). SL's setting is **not** Gaussian and **not** correctly specified. SL call the candidate-only model misspecified and assume only finite second moments of x_s. "Exact selection … with rate" is ours. SL's Corollary 2 gives containment (screening) of the support, in probability, with no rate.
- p. 956: "Let D_nˢ = {y, X_s} denote a fixed subset of observations, where s ⊂ {1, 2, …, P_n} and X_s contains only s = |s| < P_n predictors … Assume that X_s does not include all of the true predictors of model (1)."
- p. 956: "Therefore, the model y = X_s β_s + ε is misspecified." Also: "It is obvious that f* ∉ P_s." And (17): "f₀ = arg min_{f∈P_s} ∫ ln(f*/f) f*".
- p. 957, Condition 4: "There is a constant δ > 0 such that for any a = (a₁, …, a_s)ᵀ ∈ ℝ^s, with |a_i| ≤ δ for i = 1, …, s, we have E{(aᵀx_s)²} < ∞". This is a second-moment condition only.
- p. 957: "To prove theorem 4, π(ξ) does not need to be specified, which is only required to be positive for all possible models". The slab and σ² priors are as before: "π(σ²) ∼ IG(a₀, b₀), π(β_ξ | ξ, σ²) ∼ N(0, σ²V_ξ)".
- p. 957, Theorem 4: "Assume that condition 4 holds for a given subset s. Under the prior setting as described above, for any ε > 0, π[{f ∈ P_s : d(f₀, f) > ε} | D_nˢ] → 0, almost surely, (18)". This is for a fixed ε, almost surely, with no rate.
- p. 957: "f₀ = φ(y; β₀ᵀx_s, σ₀) ν(x_s)" (from supplement Lemma 1.2), "β₀ = arg min_{β_s} E(β_sᵀx_s − β*ᵀx)², i.e. β₀ᵀx_s is the projection of β*ᵀx." Also "(19) β₀ = Σ_s⁻¹Σ_{s,t}β_t* = Σ_s⁻¹cov(x_s, y)".
- p. 957, Corollary 2: "Assume that the conditions of theorem 4 hold. If x_s does not have exact multicollinearity … then for the posterior probability of model ξ, conditioned on the subset D_nˢ, we have π(s̃ ⊂ ξ | D_nˢ) →ᵖ 1." Here s̃ is "the subset of s corresponding to non-zero entries of β₀".
- **What SL conclude:**
  - Thm 4: Hellinger consistency (joint (y, x_s) density) at the KL projection f₀, for each fixed ε, almost surely.
  - Cor 2: the support s̃ of the population L2 projection β₀ (= our "best candidate predictor's support") is contained in the sampled model with posterior probability →ᵖ 1. This is screening only: no exclusion of other candidates, no rate, no HPM/MPM.
- **What SL assume:** a fixed candidate subset s that misses some true predictors; Condition 4 (second moments of x_s); a positive model prior; the conjugate Gaussian slab with IG(a₀, b₀) on σ²; for Cor 2, no exact multicollinearity in x_s. There is no Gaussian assumption on x. Gaussianity or linearity of y given x_s is never claimed.
- **Proposed wording:** "Analogue of SL (2015) Thm 4/Cor 2 (candidate set missing true predictors; their model is misspecified, with x_s under second moments only; Cor 2: π(s̃ ⊂ ξ) →ᵖ 1, containment, no rate). Here, with Gaussian candidate rows and a Gaussian linear response given the candidates, the candidate-only model is correctly specified: exact selection of the best candidate predictor's support s̃ at rate $\sqrt{\log n/n}$, no condition on how Σ, β, σ² vary with n".

### C6. Row 2.1 (:50, text being replaced): "Joint (x,y) Hellinger contraction of the posterior at rate √(log n/n), exponential form (Song–Liang Theorems 1–2 analogue)" and "Song–Liang Theorems 1–2 parity"
**VERDICT: MATCH** for "joint (x,y) Hellinger" and "exponential form". The parity is in distance and form, not in rate: SL's Theorems 1–2 cannot reach √(log n/n).
- Joint (x,y) Hellinger: see `SL_PDF_CHECK.md` S1 (p. 950, (2); p. 952 definition of d; p. 952 Theorem 1's d² with ν_x(dx)). SL's d has no factor ½, so d = √2·d_H.
- Exponential form: see `SL_PDF_CHECK.md` S2. p. 952, (15): "P*[π{d(f, f*) > ε_n | D_n} > exp(−c₁nε_n²)] < exp(−c₁nε_n²)". The same display, unnumbered, is in Theorem 2 (p. 953).
- p. 954: "Under condition 1, π{d(f, f*) > ε_n | D_n} converges in L1 exponentially, whereas result (16) implies only convergence in probability."
- **Rate caveat:**
  - Theorem 1 needs (10) "r̄_n ln(P_n) ≺ nε_n²", with r̄_n ≥ 1 and P_n ≻ n^θ. Hence ε_n² ≫ log n/n strictly.
  - Theorem 2 adds r_n ≻ 1. Hence ε_n² ≫ r̄_n log n/n with r̄_n → ∞ (see `SL_PDF_CHECK.md` S4). Cor 1's best rate is ε_n = O{n^{−(1−α)/2} log^{k/2} n} (S5).
  - So "at rate √(log n/n)" describes ours only. SL's Theorems 1–2 give strictly slower rates.
- **No change required.** Optional precision: "(Song–Liang Theorems 1–2 analogue, at a faster rate than theirs)".

### C7. Row 2.2 (:51): "Partial Song–Liang parity" (fixed-design, in-sample average Hellinger contraction of the parameter posterior)
**VERDICT: PARTLY.** SL have **no** fixed-design or in-sample Hellinger result. Every distance in SL integrates over the predictor law. The parity is only in kind (Hellinger contraction of the posterior), not in setting.
- p. 952: "For two density functions f₁(x, y) and f₂(x, y), the Hellinger distance is defined as d(f₁, f₂) = √(∫∫ {f₁^{1/2}(x, y) − f₂^{1/2}(x, y)}² dx dy)."
- p. 952, Theorem 1: "d²(f, f*) = ∫∫ |φ^{1/2}(y; xᵀβ*, σ*) − φ^{1/2}(y; xᵀβ, σ)|² ν_x(dx) dy".
- p. 957 (misspecified case): "f₀ = φ(y; β₀ᵀx_s, σ₀) ν(x_s)". This is again a joint density with the x-law.
- Searching the whole paper finds no fixed-design, conditional-on-X, or in-sample (empirical average over observed x_i) version of any theorem.
- **Proposed wording:** "Fixed-design (in-sample) counterpart of SL's joint-(x,y) Hellinger contraction (SL have no fixed-design result; parity in kind only); input to 2.1."

### C8. Card :139: "1.1–1.4, 3.6, 3.7 read like Song–Liang-level statements"
**VERDICT: NOT A CITATION.** This is the lead's readability verdict, not a claim about the paper's content.
- **Comparator for 1.1–1.4:** SL's theorem statements are asymptotic statements about the exact posterior: Theorems 1–4 and Corollaries 1–2, pp. 952–957. Summary, p. 947: "Under mild conditions, we show that the approach proposed is consistent".
- **No comparator for 3.6 and 3.7:** SL have no theorem about sampler or software output (C9). For these rows, "Song–Liang-level" can only mean the style of statement, not a comparable result.
- **Optional wording:** "1.1–1.4 read like Song–Liang-level statements; 3.6, 3.7 are stated at the same level (SL have no sampler-output result to compare with)".

### C9. Rows 3.1/3.6/3.7 (implicit): "no comparable result for an SMC/MCMC BVS implementation known to us"; row 3.6 "ties the theory to every number the software prints"
**VERDICT: MATCH** (as regards SL). SL prove nothing about the output of SAMC or of the split-and-merge procedure. Every theorem is about the exact posterior π(· | D_n) or π(· | D_nˢ) (`SL_PDF_CHECK.md` S11). The only link between the theory and the two-stage procedure is one informal sentence.
- p. 959 (end of §3.1), the informal sentence: "Clearly, it follows from the theory that was developed in Section 2 that the SAM approach will lead to a consistent selection of true predictors."
- p. 959, §3.2: "the stochastic approximation Monte Carlo (SAMC) algorithm (Liang et al., 2007) was used in this paper." Also: "As shown in Liang (2009), the SAMC algorithm is essentially a dynamic importance sampling algorithm, and quantities of interest can be estimated by averaging the samples with respect to their importance weights."
- p. 969: "SAM is not a standard Bayesian approach, as it does not process all data altogether and thus only provides an approximate quantification of uncertainty for each predictor through marginal inclusion probabilities."
- p. 970: "section 2 describes the SAMC algorithm and its implementation for high dimensional regression". The supplement's theory sections are the proofs of Theorems 1–4 (§1) and MAP consistency (§3). No section is about SAMC output.
- **Caveats:**
  1. The p. 959 sentence is not backed by a theorem. Theorem 4 / Corollary 2 are for "a fixed subset" (p. 956), whereas the stage-2 merged set S̃ (p. 959) is data-dependent.
  2. SL cite general SAMC convergence theory (Liang et al., 2007; Liang, 2009). So "no comparable result" should be read as no result tying BVS output to the posterior theory, not as no convergence theory for SAMC.

---

## MISMATCHES

| Item | Verdict | Proposed corrected wording |
|---|---|---|
| C1 | PARTLY | "Full-model selection consistency (SL Thm 3 gives sure screening only: sensitivity → 1, specificity not controlled; MAP consistency only in their supplement) for the shipped prior, with an explicit, design-uniform expectation rate and exact HPM/MPM; no tuning" |
| C2 | PARTLY | "Thm 1′ replaces eigenvalue floors off the truth by a residual-signal identifiability margin (Narisetty–He style; cf. SL's population-level identifiability Condition 3 for their Thm 3)." |
| C3 | MATCH (cite) | "Narrower in dimension ($n^A$ vs SL's $P_n<e^{Cn^\alpha}$, $\alpha<1$: Cor 1 via (10), inherited by Thm 3)." |
| C5 | MISMATCH | "Analogue of SL (2015) Thm 4/Cor 2 (candidate set missing true predictors; their model is misspecified, with x_s under second moments only; Cor 2: π(s̃ ⊂ ξ) →ᵖ 1, containment, no rate). Here, with Gaussian candidate rows and a Gaussian linear response given the candidates, the candidate-only model is correctly specified: exact selection of the best candidate predictor's support s̃ at rate $\sqrt{\log n/n}$, no condition on how Σ, β, σ² vary with n" |
| C7 | PARTLY | "Fixed-design (in-sample) counterpart of SL's joint-(x,y) Hellinger contraction (SL have no fixed-design result; parity in kind only); input to 2.1." |
| C8 | NOT A CITATION | Optional: "1.1–1.4 read like Song–Liang-level statements; 3.6, 3.7 are stated at the same level (SL have no sampler-output result to compare with)". |

C4, C6 and C9 are MATCH.
- C4, optional precision: "rows i.i.d.; here Gaussian, theirs any law under their Conditions 1/2".
- C6, optional precision: SL's Theorems 1–2 rates are strictly slower than √(log n/n), so the parity is in form and distance, not in rate.
- C9: SL's only statement about the procedure's output is the informal p. 959 sentence. SL cite general SAMC convergence theory, but none of it is about BVS output.
