# Precedent notes for the posterior theorems (core 1 = rows 1.1/1.2, core 2 = row 2.1) — 2026-11-17

Author: Theory Dept research helper (Sonnet 5.5). For: Theory Dept manager / Writing. Status: **notes, not a theorem**; nothing here is a registered result.

**Scope.** The assumptions of Theorem 1 (row 1.1), Theorem 2 (row 1.2) and Theorem 9 (row 2.1) that TRACK_B v1.4.1 does **not** label "the same as Song–Liang (2015)": B2, B4, B5, B6, B7 (B4 and B7 are split in two). B1 (Gaussian model) and B3 (fixed sparsity) are "the same" there and are not treated; B3 gets one extra line at the end because the owner named fixed sparsity. B8–B11 belong to core 3/4 and are out of scope. Our assumption texts are those of `W3-READER/READER_VERSIONS.md` §1, §2, §9 (v0.4); the comparison with Song–Liang is TRACK_B v1.4.1 (`W3-AUDIT/.../TRACK_B.md`).

**Verification rule.** Every citation below was checked against the paper itself: I downloaded the arXiv PDF, extracted the text, and matched each quote (whitespace-insensitive) on the page given; formulas whose text extraction was garbled (inequality signs, √) were read off the rendered page image and are marked "(page image)". Page numbers are the page numbers printed on the arXiv PDF (for the Annals/IMS reprints these are the article's own pages 1, 2, …, not the volume pages). "VERIFIED" = the quote and location were seen in the PDF. Where a published journal version differs from the arXiv version I did not read it; this is stated per paper. The Opus re-check is recorded in the last section.

**Versions read.**

| Short name | Paper (arXiv PDF read) | Version |
|---|---|---|
| ZH08 | Zhang & Huang, *The sparsity and bias of the LASSO selection in high-dimensional linear regression*, Ann. Statist. 36(4) 1567–1594 — <https://arxiv.org/abs/0808.0967> | arXiv v1 (IMS reprint pagination; header shows Ann. Statist. 2008) |
| BRT09 | Bickel, Ritov & Tsybakov, *Simultaneous analysis of Lasso and Dantzig selector* — <https://arxiv.org/abs/0801.1095> | arXiv v3 (9 Nov 2010) |
| MY09 | Meinshausen & Yu, *Lasso-type recovery of sparse representations for high-dimensional data*, Ann. Statist. 37(1) 246–270 — <https://arxiv.org/abs/0806.0145> | arXiv v2 (IMS reprint) |
| CSV15 | Castillo, Schmidt-Hieber & van der Vaart, *Bayesian linear regression with sparse priors*, Ann. Statist. 43(5) 1986–2018 — <https://arxiv.org/abs/1403.0735> | arXiv v3 (14 Oct 2015; IMS reprint pagination) |
| NH14 | Narisetty & He, *Bayesian variable selection with shrinking and diffusing priors*, Ann. Statist. 42(2) 789–817 — <https://arxiv.org/abs/1405.6545> | arXiv v1 (IMS reprint pagination) |
| YWJ15 | Yang, Wainwright & Jordan, *On the computational complexity of high-dimensional Bayesian variable selection* — <https://arxiv.org/abs/1505.07925> | arXiv v1 (only version on arXiv); a later journal version was not read, so numbering may differ there |
| SBJ | Shin, Bhattacharya & Johnson, *Scalable Bayesian variable selection using nonlocal prior densities in ultrahigh-dimensional settings* — <https://arxiv.org/abs/1507.07106> | arXiv v4 (18 Jan 2017); the journal version was not read |
| SC11 | Shang & Clayton, *Consistency of Bayesian linear model selection with a growing number of parameters* — <https://arxiv.org/abs/1102.0826> | arXiv v2 (2 Feb 2012) |
| RWY | Raskutti, Wainwright & Yu, *Minimax rates of estimation for high-dimensional linear regression over ℓq-balls* — <https://arxiv.org/abs/0910.2042> | arXiv v1 (11 Oct 2009); this is the paper whose Proposition 1 is read; the separate RE-for-correlated-Gaussians paper of the same authors was not read |
| W09 | Wainwright, *Sharp thresholds for high-dimensional and noisy recovery of sparsity* — <https://arxiv.org/abs/math/0605740> | arXiv v1 (UC Berkeley technical report, May 2006); the later journal version was not read |
| RZ | Rudelson & Zhou, *Reconstruction from anisotropic random measurements* — <https://arxiv.org/abs/1106.1151> | arXiv v1 (6 Jun 2011); the journal version was not read |

Search was targeted, not exhaustive: for each assumption I give the best 2–3 precedents I could verify, mostly Bayesian variable-selection papers plus the Lasso literature where the condition originates.

---

## B2. Polynomial dimension, p ≤ n^A (Thm 1, 2; Thm 9: 2 ≤ p_raw ≤ n^A)

**Ours.** The number of predictors is at most a fixed power of n (p ≫ n allowed); it enters through union bounds over models of size O(log n).

**Precedents.**
1. **SBJ, Assumption 1 and the comment after Assumption 5** (p. 14): "There exists α ∈ (0, 1) such that log p = O(n^α)." and "Our theoretical results continue to hold when p grows polynomially in n, i.e., at the rate O(n^γ) for some γ > 1." — VERIFIED (<https://arxiv.org/pdf/1507.07106v4>, p. 14).
2. **NH14, Condition 4.1** (p. 10): "p_n = e^{n d_n} for some d_n → 0 as n → ∞, that is, log p_n = o(n)." — VERIFIED (<https://arxiv.org/pdf/1405.6545v1>, p. 10; the quoted tail "that is, log p_n = o(n)" matched in the text; the displayed formula read as printed).
3. **SC11, Assumption 2.5** (p. 6): "p_n → ∞, s_n ≤ p_n ≤ n and p_n log p_n = o(n)." — VERIFIED (<https://arxiv.org/pdf/1102.0826v2>, p. 6, page image).

**How ours compares.** For p → ∞ our cap lies inside the sub-exponential ranges of SBJ and NH14 (polynomial p is stated explicitly only by SBJ, and only implied by NH14's log p = o(n)) and is wider than SC11's p log p = o(n); unlike NH14 and SC11, ours also admits bounded p. I found no Bayesian selection theorem that states "p ≤ n^A" itself as the hypothesis (the closest is the SBJ remark), so the polynomial cap is best described as a convenience of our proof technique, as TRACK_B B2 already says.

---

## B4a. Nonzero coefficients not too small — beta-min (Thm 1 (A6): θ*_min ≥ C_β σ√(log n/n) or ≫ √(log n/n); Thm 2 (A2): |β*_j| ≥ b_lo fixed; none in Thm 9, but Thm 9B (A6b): b_n² n/log n → ∞ in standard-deviation units)

**Ours.** The smallest nonzero coefficient is above a threshold of order σ√(log n/n); in Theorem 2 it is a fixed constant, far above that scale.

**Precedents.**
1. **CSV15, Theorem 5 and Corollary 1** (pp. 13–14): the third display of Thm 5 (page image) gives the detection threshold |β⁰_i| ≥ M√(log p)/‖X‖ when the compatibility numbers are ≥ c₀ and |S₀| ≤ d₀ mc(X)⁻¹ (mutual coherence), with ‖X‖ the largest column norm; and "A nonzero coordinate of β⁰ that is too close to zero cannot be detected as being nonzero by any method." (p. 13); "… consistently selects the correct model if all nonzero coordinates of β⁰ are bounded away from 0 by the thresholds given in Theorem 5." (pp. 13–14). — VERIFIED (<https://arxiv.org/pdf/1403.0735v3>, pp. 13–14).
2. **YWJ15, Theorem 1, display (8)** (p. 9): C_β² ≥ c₀(L + L̃ + α + κ) σ₀² (log p)/n; "We refer to it as the β_min-condition in the rest of the paper." — VERIFIED (<https://arxiv.org/pdf/1505.07925v1>, p. 9; the formula was read from the extracted text and the quote matched). The theorem recovers the set S(C_β) = {j : |β*_j| ≥ C_β} of "influential" coordinates; smaller nonzero coordinates are allowed but bounded (their Assumption A).
3. **MY09, Corollary 2** (p. 12): sign consistency of the hard-thresholded Lasso under "min_{k: β_k ≠ 0} |β_k| ≫ σ t_n √(log p_n / n)". — VERIFIED (<https://arxiv.org/pdf/0806.0145v2>, p. 12; the displayed inequality matched after allowing for the extraction's separate √ sign; the text before it, "Assume furthermore", is on the same page).

**How ours compares.** CSV15 needs every nonzero coefficient to exceed a constant multiple of √(log p/n) (with column norms ≍ √n), YWJ15 needs this only for the coordinates it recovers (smaller ones are allowed but bounded), and MY09 a diverging multiple (t_n → ∞); when p ≥ n^a for some a > 0 our σ√(log n/n) has the same order as CSV15's and YWJ15's thresholds and is below MY09's, and when log p = o(log n) it is a larger requirement than CSV15's and YWJ15's; our second form of (A6), θ*_min√(n/log n) → ∞, is MY09's type. Theorem 9 itself has no such condition (it concerns the fitted distribution, not selection); only Theorem 9B has one.

---

## B4b. Signal bounded above (Thm 1 (A3): max_j |θ*_j| ≤ θ̄, i.e. ‖Xθ*‖² ≤ n s₀² θ̄²; Thm 2 (A2): |β*_j| ≤ b_hi; Thm 9 (A5): |β*_j| sd(x_j) ≤ b̄ σ_*)

**Ours.** The signal is bounded above in units of the noise, which keeps the posterior of σ² on scale; some bound is necessary for the size-tail step (explicit counterexample in READER §1).

**Precedents.**
1. **YWJ15, Assumption A ("Full β* condition", (7a))** (p. 7, page image): ‖(1/√n) Xβ*‖₂² ≤ g σ₀² (log p)/n, with the remark "some form of upper bound on the norm ‖β*‖₂ in terms of the g-hyperparameter is required in order to prove Bayesian model selection consistency". — VERIFIED (<https://arxiv.org/pdf/1505.07925v1>, p. 7).
2. **SC11, Assumption 2.7** (p. 7): "There is a positive sequence φ_n such that k_n = O(φ_n) and min_j c_j ≥ φ_n, where k_n = ‖β⁰_{γ⁰}‖²₂" — the squared norm of the true signal is bounded by the prior-variance scale of the nonzero coefficients. — VERIFIED (<https://arxiv.org/pdf/1102.0826v2>, p. 7).
*Not the same type (removed after the Opus check):* NH14, Condition 4.3 (p. 11) bounds only the inactive, near-sparse part, "b₀ := ‖X_{t^c} β_{t^c}‖₂ = O(1)", and puts no upper bound on the active coefficients (their Condition 4.4 is a lower bound); it is a different kind of condition, so it is not counted as a precedent.

**How ours compares.** Same type (an upper bound on the signal size, which YWJ15 say their proof requires and our size-tail step requires), but in YWJ15 and SC11 the bound is tied to a prior hyperparameter (g, or the slab variances c_j), whereas ours is a fixed constant in noise units because the coded prior has no tuning. Only two verified precedents for this assumption.

---

## B5. Eigenvalue floor on small sets (Thm 1 (A4): λ_min(R̂_S) ≥ φ₀² for |S| ≤ 2(A+1)s₀+2; Thm 2 (A3): λ_min(Σ_S) ≥ φ² for |S| ≤ 5(A+1)(s₀+1) log n; Thm 9B (A6a))

**Ours.** A fixed lower bound on the smallest eigenvalue of the (sample or population) correlation matrix of every small set of columns, with set size a multiple of s₀ (Thm 1) or O(log n) (Thm 2); no upper bound.

**Precedents.**
1. **ZH08, sparse Riesz condition (SRC), (2.13)** (p. 6, page image): "The sparse Riesz condition controls the range of eigenvalues of covariate matrices of subsets of a fixed number of design vectors x_j", i.e. c_* ≤ ‖X_A v‖²/(n‖v‖²) ≤ c^* for all A with |A| = q^*; Remark 5 (δ = 1/3) makes Theorem 1 applicable "if 10q + 1 ≤ q^*" (q = true sparsity). — VERIFIED (<https://arxiv.org/pdf/0808.0967v1>, p. 6; Remark 5 is on p. 13).
2. **CSV15, Definition 2.3 and the sentence after it** (p. 7): the smallest scaled sparse singular value of dimension s; "For recovery we shall impose that these numbers for s equal to (a multiple of) the dimension of the true parameter vector are bounded away from zero." — VERIFIED (<https://arxiv.org/pdf/1403.0735v3>, p. 7).
3. **YWJ15, Assumption B, RE(s)** (p. 8): "Lower restricted eigenvalue (RE(s)): min_{|γ|≤s} λ_min(X_γ'X_γ/n) ≥ ν", used with s = K s* in Theorem 1 ("The lower restricted eigenvalue condition is a mild requirement."). — VERIFIED (<https://arxiv.org/pdf/1505.07925v1>, p. 8; Theorem 1 states "Assumption B with s = Ks*", p. 9).
*See also* BRT09, Assumption RE(s, c₀) (p. 7) — the cone-restricted version of the same idea — and Assumption 2 (p. 8): "Only bounds on the minimal and maximal eigenvalues of 'small' submatrices of the Gram matrix Ψ_n are involved." — VERIFIED (<https://arxiv.org/pdf/0801.1095v3>, pp. 7–8).

**How ours compares.** Same type and, for Theorem 1 (A4), set sizes of the same order (a fixed multiple of the sparsity) and a fixed floor, as in ZH08, CSV15 and YWJ15; Theorem 2 (A3) asks the floor on larger O(log n) sets. Neither (A4) nor (A3) bounds the largest eigenvalue, unlike ZH08 (c^*) and BRT09's Assumption 2 (φ_max), so pervasive factors (top eigenvalue of order p) are allowed; CSV15 and YWJ15 do not bound it either.

---

## B6. No near-exact collinearity on O(log n) sets — a vanishing floor (Thm 1 (A5): λ_min(X_S'X_S) ≥ g₀ for |S| ≤ 3(A+1)(s₀+1) log n, i.e. λ_min(X_S'X_S/n) ≥ g₀/n; Thm 9 (A4): λ_min(Corr(x_T)) ≥ c_ψ/n for |T| ≤ q_n ≍ log n)

**Ours.** The smallest eigenvalue on every set of O(log n) columns may be as small as c/n (not bounded away from zero), so predictors may be correlated up to 1 − c/n; this keeps the prior's penalty per extra variable (factor ≈ n^{-1/2}) in force.

**Precedents.**
1. **SBJ, Assumption 4** (p. 14, page image): min over |k| ≤ q_n of the smallest nonzero eigenvalue ν_{k*} of X_k'X_k/n satisfies ν_{k*} ≻ τ_{n,p}/n (with log p ≺ τ_{n,p} ≺ n and q_n ≺ τ_{n,p}/log p); "the minimum of the minimum eigenvalue of (X_k'X_k)/n over all submodels k with |k| ≤ q_n is allowed to decrease with increasing n and p. Assumption 4 is called the sparse Riesz condition …" (≻ means "much larger than" in their notation, page 14.) — VERIFIED (<https://arxiv.org/pdf/1507.07106v4>, p. 14).
2. **NH14, Condition 4.5** (p. 11, page image): the minimum nonzero eigenvalue λ_m^n(ν) ≽ (n ∨ p_n^{2+2δ})/(nτ²_{1n}) ∨ p_n^{-κ} (≽ = "at least of the order of", their p. 5; the condition also bounds the maximal eigenvalue, λ_M^n ≺ (nτ²_{0n})^{-1} ∧ nτ²_{1n}), over all models of size ≤ m_n(ν) = p_n ∧ n/((2+ν) log p_n); and (p. 17) "Condition 4.5 allows the minimum eigenvalue to be exactly zero to allow even perfect correlation among inactive (or active) covariates." — VERIFIED (<https://arxiv.org/pdf/1405.6545v1>, pp. 11, 17).
3. **BRT09, Assumption 2 and the paragraph after it** (pp. 8–9): taking s + m = s log n and φ_max bounded, Assumption 2 "is equivalent to φ_min(s log n) > c/log n"; they note that "the corresponding slightly stronger assumption in [18] [Meinshausen–Yu] … lim inf φ_min(s_n log n) > 0". — VERIFIED (<https://arxiv.org/pdf/0801.1095v3>, p. 9).
*See also* MY09, §2.2.2 (p. 9): incoherence holds "if the minimal eigenvalue of a selection of s_n(log n)² variables is vanishing slowly for n → ∞", and "Sparse eigenvalues can even converge slowly to zero in our setting." — VERIFIED (<https://arxiv.org/pdf/0806.0145v2>, p. 9).

**How ours compares.** Same type — a floor on the smallest eigenvalue over small or moderate column sets (s log n in BRT09, s_n(log n)² in MY09, q_n ≺ τ/log p in SBJ, up to n/log p in NH14) that is allowed to vanish. Ours, g₀/n on O(log n) sets, is lower than BRT09's c/log n (given bounded φ_max), MY09's "slowly vanishing" and SBJ's ≫ log p/n; NH14's floor (of the order of p^{-κ}, or larger) may be lower than ours when p is large. NH14 and SBJ both use the minimum *nonzero* eigenvalue (SBJ, (8), p. 14), so those conditions do not themselves exclude exact duplicates (NH14 say so explicitly, p. 17, leaving it to their identifiability Condition 4.4; SBJ's Assumption 5 excludes them only inside the true model), while our (A5)/(A4) excludes them; also ours is on the population correlation matrix in Thm 9 and on the sample Gram matrix in Thm 1, while SBJ and NH14 are on the sample Gram matrix.

---

## B7a. Gaussian rows (Thm 2: rows of X i.i.d. N_p(m_n, Σ_n), Σ_n a correlation matrix)

**Ours.** Gaussian rows are used only to transfer the population small-set floor (A3) to the sample floors (A4)–(A5) by entrywise concentration; the mean m_n is free (the model has an intercept).

**Precedents.**
1. **ZH08, Proposition 2(i)** (p. 14): rows i.i.d. copies of a subvector of a zero-mean random sequence satisfying the Riesz condition (4.5); "(i) Suppose {ξ_k, k ≥ 1} is a Gaussian sequence" then c_*(m), c^*(m) of the sample Gram matrix stay within τ_*ρ_* and τ^*ρ^* with probability ≥ 1 − 2e^{-nε₄} for m ≤ min(p, ε₁²n), log (p choose m) ≤ ε₃n (page image). — VERIFIED (<https://arxiv.org/pdf/0808.0967v1>, p. 14).
2. **RWY, Proposition 1** (p. 10): "Consider a random design matrix X ∈ R^{n×d} formed by drawing each row X_i ∈ R^d i.i.d. from an N(0, Σ) distribution", then ‖Xv‖₂/√n ≥ ½‖Σ^{1/2}v‖₂ − 6√(ρ(Σ) log d/n)‖v‖₁ for all v, with probability 1 − c₁exp(−c₂n) (ρ(Σ) = max_j Σ_jj). — VERIFIED (<https://arxiv.org/pdf/0910.2042v1>, p. 10).
3. **W09, Theorem 1 and its set-up** (pp. 8–9): "each row x_k is chosen as an i.i.d. Gaussian random vector with covariance matrix Σ", Σ with unit diagonal and Λ_min(Σ_SS) ≥ C_min (condition (17), with also Λ_max(Σ) ≤ C_max). — VERIFIED (<https://arxiv.org/abs/math/0605740>, v1, p. 8 for the quote and (17), Theorem 1 runs over pp. 8–9; this is the technical-report version).

**How ours compares.** Same type: i.i.d. mean-zero Gaussian rows with a population covariance condition (global in ZH08, on the support plus a global ceiling in W09, none in RWY's inequality itself); ZH08 and RWY pass it to the sample Gram matrix (W09 is a Lasso theorem, not a transfer result). Ours additionally allows a nonzero mean and needs no upper eigenvalue bound (ZH08 and W09 assume one; RWY need only the maximal variance, which is 1 for a correlation matrix).

---

## B7b. Sub-Gaussian rows on sparse directions (Thm 9 (A3): E exp(λ u'z) ≤ exp(L²λ² Var(u'z)/2) for every u with ≤ q_n nonzero entries, z the standardised predictors)

**Ours.** The predictors are sub-Gaussian at the scale of their own standard deviation, along sparse directions only; Gaussian rows satisfy it with L = 1.

**Precedents.**
1. **RZ, Definition 1.5 and Theorem 1.6** (pp. 5–6): a random vector Y is "ψ₂ with a constant α if for every y ∈ R^p, ‖⟨Y, y⟩‖_{ψ₂} := inf{t : E exp(⟨Y, y⟩²/t²) ≤ 2} ≤ α‖y‖₂" (together with isotropy); Theorem 1.6: "Let Ψ be an n × q matrix whose rows are independent isotropic ψ₂ random vectors in R^q with constant α" and n ≥ (2000 m α⁴/δ²) log(60ep/(mδ)) ⇒ RE holds for (1/√n)ΨA with probability ≥ 1 − 2 exp(δ²n/2000α⁴) (exponent sign as printed). — VERIFIED (<https://arxiv.org/pdf/1106.1151v1>, pp. 5–6).
2. **NH14, Lemma 6.1** (p. 16): "Suppose that the rows of X_{n×p_n} are independent isotropic sub-Gaussian random vectors in R^{p_n}. Then there exists a ν > 0 such that, with probability greater than 1 − exp(−w'n), inf_{|k|≤m_n(ν)} φ_min(X_k'X_k/n) > 0." — VERIFIED (<https://arxiv.org/pdf/1405.6545v1>, p. 16).
*Not our type (demoted after the Opus check):* ZH08, Proposition 2(ii) (p. 14) uses bounded covariates, "Suppose max_{j≤p} ‖ξ_{k_j}‖_∞ ≤ K_n < ∞." — VERIFIED (<https://arxiv.org/pdf/0808.0967v1>, p. 14), but bounded covariates are not sub-Gaussian at their own standard deviation (a bounded binary predictor with P(x = 1) → 0 violates our (A3), TRACK_B B7), so it is not counted as a precedent.

**How ours compares.** Same type: for centred rows, RZ's anisotropic model X = ΨΣ^{1/2} with Ψ isotropic ψ₂ gives "⟨x, y⟩ sub-Gaussian at the scale of its own standard deviation" (up to constants), the dense-direction analogue of our (A3), and NH14's Lemma 6.1 is the same sub-Gaussian-rows-to-sample-eigenvalue transfer in a Bayesian selection paper; for centred rows ours is weaker, asking sub-Gaussianity only along q_n-sparse directions, while RZ ask it along all directions and NH14 assume identity covariance.

---

## Extra line — B3 (fixed sparsity), already "the same as Song–Liang"

**NH14, Condition 4.3** (p. 11): "the size of the true model |t| is fixed." — VERIFIED (<https://arxiv.org/pdf/1405.6545v1>, p. 11). Ours (s₀ fixed) is of the same type; TRACK_B B3 shows (Theorem 3(a)) that the rate forces s₀ = O(√log n).

---

## Summary

| Assumption | Precedents (all verified) |
|---|---|
| B2 p ≤ n^A | SBJ, NH14, SC11 |
| B4a beta-min | CSV15, YWJ15, MY09 |
| B4b bounded signal | YWJ15, SC11 (NH14 removed: different type) |
| B5 small-set eigenvalue floor | ZH08, CSV15, YWJ15 (+ BRT09) |
| B6 vanishing floor on O(log n) sets | SBJ, NH14, BRT09 (+ MY09) |
| B7a Gaussian rows | ZH08, RWY, W09 |
| B7b sub-Gaussian sparse directions | RZ, NH14 (ZH08 Prop 2(ii) demoted: bounded covariates, not our type) |

Counts: 7 assumptions; 21 precedent citations kept, all VERIFIED (including 2 "see also"), none NOT VERIFIED; 2 citations dropped as the wrong type (NH14 Cond. 4.3 for B4b, ZH08 Prop. 2(ii) for B7b); B3 extra line (NH14 Cond. 4.3) kept.

Not verified / not read: published journal versions of YWJ15, SBJ, W09, RZ, RWY (arXiv versions read as listed); Johnson & Rossell (2012) and Jiang (2007) were looked at only as background and are not cited.

## Opus check

One Opus subagent (model opus, one-shot) re-checked all 26 citations against the rendered PDF pages (not the text extraction) and our assumption texts. Result: every citation exists where cited; the checker applied 8 factual fixes, which I accepted: CSV15 Thm 5 third display also needs |S₀| ≤ d₀ mc(X)⁻¹ and ‖X‖ is the largest column norm; ZH08 Remark 5 is on p. 13; SBJ quote extended with "…"; NH14 Condition 4.5 prints ≽ (not ≻) and also bounds the maximal eigenvalue; ZH08 Prop. 2(i) condition is log C(p, m) ≤ ε₃n; W09 quote and (17) are on p. 8 and Thm 1 runs over pp. 8–9; RZ exponent sign "as printed"; MY09 Cor. 2 matched. It found **two citations of the wrong type** (NH14 Cond. 4.3 as an upper bound on the signal; ZH08 Prop. 2(ii) as sub-Gaussian) and **six comparison sentences that over-claimed** (B2 bounded p; B4a diverging multiple t_n in MY09 and the log p ≍ log n step; B4b NH14 clause; B5 unit-diagonal non sequitur; B6 set sizes and the SBJ nonzero-eigenvalue point; B7a "population condition on small sets passed to the sample"). All of these were corrected in the text above using the checker's proposed wording, lightly edited. Not re-checked a second time.


---
Comparison sentences re-checked by an independent Opus reader (2026-11-17): 3 OK, 5 fixed as proposed (B4a, B4b, B5, B6, B7b). All citations VERIFIED against arXiv versions (journal versions of YWJ, SBJ, W09, RZ, RWY not read).
