# OWNER DEFENSIBILITY DOSSIER: assumption-by-assumption Q&A

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **v1.4 (senior review: completeness, generality and naturalness; see COUNCIL_RECORD.md and council/V14_CHANGESPEC.md).**

This file is for the owner's grilling. Each assumption gets the same six questions:
1. What exactly is assumed?
2. Why is it needed, and which proof step uses it?
3. Is it standard?
4. Does it hold on our data?
5. Can it be weakened, and what happens if it fails?
6. What a hostile referee will say, and our answer.

Sources and conventions:
- **Citations.** "P17" means `writing_answers/PRECEDENTS_2026-11-17.md` and "PN" means `PRECEDENTS_NEW.md`. Both were verified against the PDFs; page numbers are those of the version named there. SL means Song & Liang (2015) main text (journal pages) and SLs its supplement (printed pages).
- **Numbers.** All numbers come from `SIMULATION_DATA_ANALYSIS.md` (D1, sections E0–E8; Lead, E9).
- **Proofs.** No proofs are claimed. Proof paths are in `ASSUMPTIONS_AND_PROOF_PATHS.md` §3, and targets are defined in `THEOREM_DEFINITIONS.md` §4.

**Score card (Lead's summary; the council's scores are in COUNCIL_RECORD.md).**

| assumption | theorems | standard? | holds on S1/S2? | weaker form evaluated |
|---|---|---|---|---|
| A-GL | TD, TS, TM-a/b (not TM-a0) | yes (SL (1); NH14, YWJ are fixed-design analogues) | by construction | non-Gaussian / heteroscedastic noise: remarks |
| A-SPARSE | all | yes (SL (4), NH14 4.3) | s0 = 5, 10 | growth remark |
| A-DIM | TD, TS, TM | yes (SBJ p. 14, JR12, SL Cor S1) | A ≤ 1.77 | A-DIM′ (TD′, conjecture, high proof risk) |
| A-SUBG | TD, TS, TM-a/b | yes (SL Cond. 1, RZ, NH14 L6.1) | Gaussian rows | moments-only in TM-a0 |
| A-NEC (n·φ_min(k_n) ≥ c_ψ) | TD, TS, TM-a/b | same type; a comparison with SBJ, NH14, BRT09, SL (26), not dominance | n × floor = 8.8–250 | for TD: drop it at a √log p cost (prop:dist(ii)); for TS-b sufficient, necessity unproved |
| A-BS / BS′ | TD, TS, TM-a/b | yes (YWJ (7a), SC11 2.7; SL (3), p. 950, is the direct counterpart) | ≈ 1.17σ (1.175) | recorded pair V = O(1), E = o(1) (BS′): not adopted; open target V = O(1) alone |
| A-MARGIN-H (diverging ratio, every fixed k) | TS-a | SL Cond. 3 + Thm 3 proof | residual ratio ≥ 1 in only 9/136 (scale diagnostic) | fixed-level form (remark); not needed for the sharp claim |
| A-MARGIN-U (population form: (U1), (U2a), (U2b); accounting set Q_n) | TS-b, TM-b | same type as NH14 4.4, Luo–Chen (comparison, not dominance) | (U1) = κ_n: S1 brackets κ = 1; (U2a) minimum = exact κ_n on S1 (checked); mixed rivals: E9/E9b are diagnostics of the refined form only | corollaries C-i, C-ii; the refined design-conditional form is a parallel sufficient condition; constant 2 sharp for deletions (converse, with A-NEC on T) |
| A-MIS(iii) (primitive form) | TM-a, TM-b | SL f₀; Rossell 2022 Prop. 6 (fixed-design analogue) | in-sample illustration only: σ² ratio 0.99 (S1), 0.84–0.98 (S2) | (i′), (ii) as remarks; TM-a0 moments-only |
| A-SPARSE-C (\|supp β^C\| ≤ s_C, fixed) | TM-a, TM-b | new label; omitted-variable analogue of A-SPARSE | holds when nearest retained neighbours separate each omitted predictor (Gaussian AR(1)); not tested on data | fails under pervasive factors; relaxation TD-A |
| TM-a0-inc (target) | fixed-dimension inclusion | SL Cor 2 counterpart | trivially (Gaussian rows) | second moments only; score moments needed only for exclusion (TM-a0 exact) |

**Assumption blocks (how the assumptions group).**
1. **Model:** A-GL, A-SPARSE, A-DIM, A-BS.
2. **Design:** A-SUBG, A-NEC.
3. **Signal:** A-MARGIN-H for screening, A-MARGIN-U for exact selection.
4. **Omitted variables:** A-MIS(iii) with A-SPARSE-C; A-MOM for the fixed-dimension result.

---

## A-GL: Gaussian linear model with i.i.d. pairs
1. **Assumed.** y = α* + xᵀβ* + ε with ε ~ N(0, σ*²) independent of x, σ*² > 0, and (x_i, y_i) i.i.d. All parameters may depend on n. It is used by TD, TS-a, TS-b and (at candidate level) TM-a/TM-b, but **not** by TM-a0.
2. **Why needed.** The posterior is computed exactly from conjugate marginals.
   - RSS ratios of nested models then have exact Beta laws. TS-b's superset step relies on this, because that tail is Pareto-like and cannot be bounded by expectations.
   - The Fubini identity, which bounds the posterior size, holds for the normalised fixed-endpoint contrast density (not the plug-in score itself) and needs the likelihood to be correctly specified.
3. **Standard?** Yes.
   - SL model (1), p. 947, is the same model without an intercept.
   - NH14 Cond. 4.3, p. 11 (PN A2), and YWJ p. 7 (PN E17) are fixed-design (conditional-on-X) Gaussian analogues.
   - Jiang (2007) uses i.i.d. random design and Hellinger distance on joint densities (a GLM paper with bounded covariates; set-up arXiv pp. 2–3 and 6; PN C7).
4. **Holds on our data?** S1/S2 are generated exactly this way.
5. **Weaker forms.**
   - Non-Gaussian independent errors are remark (i′). A suggested sufficient set (not shown necessary) is a size cap K_n ≤ c·n log n/(log p)² plus a variance-proxy budget, because the Fubini size tail fails under misspecification.
   - Heteroscedastic errors are remark (ii). A heuristic variance-proxy budget suggests selection survives when (ϱ̄ − 1)·log p < ½ log n; this is not an iff and not a theorem.
6. **Referee: "Gaussian noise is unrealistic."** Answer:
   - It is the model the method's likelihood assumes, and SL make the same assumption.
   - The misspecification tier (TM) says what happens when the fitted model is wrong.
   - Remarks (i′) and (ii) indicate (heuristically) where non-Gaussian and heteroscedastic noise begin to bite. This is the Grünwald–van Ommen mechanism, and their examples are heteroscedastic "in-liers" (arXiv v3 pp. 4–5; PN D12).

## A-SPARSE: at most s true predictors, with s fixed
1. **Assumed.** |S0| ≤ s, with s fixed. TS-b also needs s0 ≥ 1.
2. **Why needed.**
   - It keeps the posterior size window small.
   - There are only 2^{s0} ways to delete true predictors, so their noise terms are uniformly bounded.
   - The one-null superset mass is (s0+1)√(log p/n).
3. **Standard?** SL strict sparsity (4), p. 950, used by SL Thms 2–3 (Thm 4 instead fixes a candidate subset, Condition 4, p. 957); NH14 Cond. 4.3, p. 11, "the size of the true model |t| is fixed" (P17).
4. **Holds on our data?** s0 = 10 on S1 and 5 or 10 on S2.
5. **Weaker forms.**
   - Growing s0: Fable's route *suggests* TS-b survives if s0²·log p = o(n), s0·(log p)² = o(n) and log s0 = o(η²·price). This is a growth remark, not a proved extension.
   - The delivered `rem:sharp`(a) (valid for s ≤ min(K−1, p/2)) shows π(S0|y) → 1 is impossible unless s0 = o(√n), whatever the proof. The rate s√(log p/n) itself is not claimed as a universal necessity for growing s (Astra R2).
   - Approximate sparsity in the style of SL (3) is the optional corollary TD-A.
6. **Referee: "Fixed s is restrictive."** Answer: it is standard (SL, NH14). Growth rates are stated in a remark, and `rem:sharp`(a) shows that s0 cannot grow as fast as √n for this conclusion with *any* proof (for s ≤ min(K−1, p/2)).

## A-DIM: p ≤ n^A (released statements)
1. **Assumed.** 2 ≤ p ≤ n^A for a fixed A ≥ 1.
2. **Why needed.**
   - TD works in three layers at fixed M. (1) On the coarse window q_n(M) ≍ M log n there are exp(O(log² n)) model sets; this count is absorbed by the isometry failure probability exp(−cn), **not** by the testing budget. (2) The delivered size lemma prop:dist(i) (fractional Bayes-factor moments, proved at p ≤ n^A) localises the posterior to |S| ≤ J = ⌊s + C_s·M⌋. (3) Only then is the O(M log n) testing budget spent, on the localised sieve.
   - TS-b tests every rival class on the same bounded-size event |S| ≤ J.
3. **Standard?**
   - SBJ p. 14: results "continue to hold when p grows polynomially" (P17 B2).
   - Johnson & Rossell (2012) Thm 1, p. 651, require p ≤ n (PN E16).
   - SL's own MAP corollary (Cor S1, SLs p. 16) is quasi-polynomial, P_n < n^{κ log n} with κ < ¼ (page image checked).
4. **Holds on our data?**
   - A = log p/log n is 0.90–1.37 on S1 and 1.50–1.77 on S2.
   - The typical user regimes we tabulated (from n = 100, p = 10³ to n = 10⁴, p = 5·10⁵) have A ≤ 1.74, so p ≤ n² everywhere (E6). These are finite-n ratios, not a test of an asymptotic condition.
5. **Weaker forms.**
   - **A-DIM′**: log p = o(√n) is the conjecture's regime. The product form (s+1)·M·log p·log(p∨n) ≤ c·n (the +1 covers s = 0) is its **proof budget**; they are different conditions (at fixed M, log p ∼ a√n with small a > 0 meets the budget but not the regime). TD′ under A-DIM′ is a **conjecture with high proof risk**.
     - Fable's route (Fubini size tail + isometry) fails at the testing step (Astra R2): at log p = n^{1/3} the entropy of the size window is ≍ n^{2/3} against a testing budget ≍ n^{1/3}.
     - A proof would need localisation at size ≈ t/log p or a direct predictive bound. If it worked, it would cover SL Cor S1's range and SL Cor 1 for α < ½.
   - **log p = o(n)** with a model-size cap K_n ≤ c·n/log p (NH14 uses p ∧ n/((2+ν) log p), pp. 10–11): the cap fixes the isometry step, not the testing step, so this too is open. It would also be an Engineering decision, because the code uses K = n/2.
6. **Referee: "SL handle exponential p; you don't."** Answer:
   - SL's exponential range (Cor 1) relies on their model-size cap r̄_n and the prior conditions (9)–(10), which would fail at our K = n/2.
   - Beyond p ≤ n^A we state a conjecture (TD′) and say honestly that our best route fails at the testing step. We release nothing beyond p ≤ n^A.
   - SL's own *selection* result (Cor S1) is only quasi-polynomial, P_n < n^{κ log n}, and all our S1/S2 settings and tabulated user regimes have p ≤ n².

## A-SUBG: sub-Gaussian predictors on sparse directions
1. **Assumed.** Every predictor has positive variance, and for all u with at most k_n nonzero entries, E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2), where ζ_j = (x_j − E x_j)/sd(x_j). The scale is the direction's own variance, so this is relative and allows correlated designs.
   - **Window.** k_n is a deterministic design order with k_n ≥ q_n(M) at the claimed level. For fixed-level statements it suffices, across all fixed levels, to impose it on sets of size ≤ c·log n for every fixed c; a single fixed level needs only one such window. For M = M_n → ∞ (the delivered `thm:dist` range M ≤ √n/log n) it is q_n(M_n). For TD′ it is the enlarged q_n. The constants L and c_ψ are common to A-SUBG and A-NEC.
2. **Why needed.**
   - (i) A two-sided sparse isometry on (s0+J)-sparse directions: the sample residual signal R̂(S) is within (1 ± δ) of the population R_n(S). This is how population margins transfer to the data.
   - (ii) A conversion inequality d_H² ≥ c_L·min{1, R/(nσ²)} for any model that misses signal R (relative SUBG gives E V⁴ ≤ C_L(E V²)², then Paley–Zygmund and Gaussian conditional affinity; Astra R2 Q4). This converts R into Hellinger separation; it does **not** imply SL's Condition 3 (Gaussian duplicates are sub-Gaussian with R = 0). The lower bound on R is supplied separately by A-MARGIN-H.
3. **Standard?** Same type, different normalisation: SL Condition 1, p. 953, is an *absolute-scale* exponential moment on sparse directions, not Σ-relative; RZ Def. 1.5/Thm 1.6, pp. 5–6 is Σ-relative; NH14 Lemma 6.1, p. 16 is an identity-covariance transfer analogue (P17 B7b).
4. **Holds on our data?** S1/S2 rows are Gaussian AR(1), so it holds with L = 1.
5. **Weaker forms.**
   - Second moments only (SL Condition 2), plus a mixed second moment of the scores for exact support, is adopted in fixed dimension as TM-a0.
   - In growing dimension the exact-marginal route needs exponential tails, so we do not claim it there.
6. **Referee: "Binary or heavy-tailed predictors?"** Answer:
   - A rare binary predictor is not sub-Gaussian at its own scale (P17 B7b note), so this is a real limitation, and it is stated.
   - Bounded predictors are **not** automatically covered (council R1 correction). Counterexample: x₁ = Z, x₂ = Z + B with Z Rademacher and B ~ Bernoulli(1/n) independent are bounded with variances bounded below, yet the standardised contrast that recovers B − EB has ψ₂²/Var growing with n. Independent bounded coordinates, or linear mixtures of independent bounded features with bounded standardised range, are covered.

## A-NEC: no near-exact collinearity (a vanishing floor)
1. **Assumed.** Let φ_min(k) := min_{1≤|V|≤k} λ_min(Corr(x_V)), the population sparse eigenvalue. Then n·φ_min(k_n) ≥ c_ψ, on the same window k_n as A-SUBG (a deterministic order with k_n ≥ q_n(M); L and c_ψ common). The sparse eigenvalue **may vanish, but no faster than the ridge scale** τ/n (τ = 1 as coded).
   - Excluding exact duplicates alone does not ensure it. Example: two predictors with correlation 1 − n^{−2} have λ_min = n^{−2} ≪ c_ψ/n, so they fail it.
2. **Why needed.** It is a **sufficient, convenient** route to determinant and shrinkage control; its necessity as stated is unproved (Astra R2).
   - Superset step: adding a null predictor must cost the full Occam factor (n+1)^{−1/2}, and the in-span shrinkage term Q_U − RSS_U must stay O_P(σ²). Heuristically, a null nearly collinear with the current model would pay almost nothing, and supersets would keep posterior mass.
   - The delivered size lemma prop:dist(i) and the TD tests use it; without it, prop:dist(ii) only localises to s + C_s·M·log n (council R1).
   - Converse: A-NEC on T gives the two-sided refund d·log(n+1)/2 + O(1), which the converse needs.
   - Forward deletion step (step 1 only): needs **no** floor, because the Occam refund is ≤ (n+1)^{d/2} for any design (Cauchy interlacing).
3. **Standard?** Same type; a comparison of object, scale and window, **not** a dominance claim (council R1, all three seats):
   - **NH14** Cond. 4.5, pp. 11, 17, bounds the minimum **nonzero sample** eigenvalue. It expressly allows exact dependence through its nonzero convention, which A-NEC excludes. Its floor ≳ p_n^{−κ} can be below c_ψ/n at large p, and NH14 also impose an upper bound.
   - **SBJ** Assumption 4, p. 14 ((8)) is a minimum-nonzero-eigenvalue condition on a sample quantity indexed through min(n, |k|). We do **not** say SBJ allows duplicates.
   - **SL (26)**, SLs p. 15, is a two-sided **sample** condition on sets of size r̄_n + |t|: a **vanishing** lower threshold (l_n ≫ r̄_n log P_n/n) and a **growing** upper threshold, and Cor S1 chooses such a pair. It was introduced because their (22) "is hardly satisfied" (SLs pp. 15–16).
   - **SL Condition 3, Gaussian sufficient form** (pp. 955–956): ch₁{var(x)} ≻ ε_n² is the precedent for vanishing floors. A-NEC at 1/n does not supply SL's screening separation; that is A-MARGIN-H's job.
   - BRT09 Assumption 2, p. 9 (c/log n) and MY09 "slowly vanishing" (P17 B6) are sample floors on other windows.
   - **No blanket ordering** (Sol R2): c_ψ/n lies below SL's l_n and BRT09's c/log n where the regimes overlap, but NH14's p_n^{−κ} can be smaller than c_ψ/n, and as a *condition set* (population object, k_n window, together with A-SUBG) A-NEC is not uniformly weaker than any of them.
4. **Holds on our data?**
   - Population floors are (1−ρ)/(1+ρ) = 0.176–1, i.e. n × floor = 8.8–250 (E5); the slack relative to c_ψ/n is this divided by c_ψ.
   - Sample sparse floors at the delivered fixed-design set sizes are vacuous on S2 (1e−5 to 2e−4). This is why we **dropped every sample floor and every fixed floor**.
5. **Weaker forms.** For TD: drop A-NEC entirely; the delivered prop:dist(ii) still gives TD, with one extra √log(p∨n) factor in the radius. For TS-b: no weaker form is established. A fixed floor on a smaller window does not imply A-NEC on a larger window.
6. **Referee: "Eigenvalue conditions are uncheckable."** Answer:
   - Ours is a population condition with a floor that tends to zero.
   - It fails only for exact or near-exact duplicates and linear dependences (one-hot coding, compositions), which users remove anyway.

## A-BS / A-BS′: bounded signal
1. **Assumed.**
   - A-BS (as delivered; used for TD **and** TS-b/TM-b): |β*_j|·sd(x_j) ≤ b̄σ*.
   - A-BS′ (recorded, **not adopted**): the recorded pair is V := Var(xᵀβ*)/σ*² = O(1) and E := Σ_j β*_j² Var(x_j)/(nσ*²) = o(1). At fixed s it is equivalent to the stated BS′ (β*ᵀΣβ* ≤ M_μσ*² and max_j |β*_j|sd(x_j) ≤ b̄_nσ* with s·b̄_n² = o(n)).
     - The **open target** is V = O(1) alone, i.e. population R² = V/(1+V) ≤ 1 − c. With A-NEC on T it gives E ≤ M_μ/c_ψ = O(1) (the A-NEC energy bound).
     - Open: whether the size lemma prop:dist(i) and the ridge remainder hold at O(1) rather than o(1) energy.
2. **Why needed.**
   - It gives a lower bound on the true model's marginal likelihood relative to the truth, which is the denominator of the Fubini size bound.
   - It keeps the estimated noise variance in a fixed range.
   - It controls the unit-ridge shrinkage term.
3. **Standard?** **Direct counterpart: SL (3), p. 950**: lim Σ_j |β*_j| < ∞, with standardised predictors and fixed σ*, implies A-BS.
   - In type: YWJ (7a), p. 7: "some form of upper bound on the norm ‖β*‖₂ in terms of the g-hyperparameter is required" (P17 B4b); SC11 Assumption 2.7, p. 7. Both their bounds grow with n (via g ≍ p^{2α} in YWJ, via φ_n in SC11), whereas A-BS uses a fixed b̄, so the precedent is for the type of condition, not its strength.
4. **Holds on our data?** Max |β|sd/σ ≈ 1.17 (1.175) and βᵀΣβ/σ² ≤ 6 in every setting (E4).
5. **Weaker forms.** A-BS′ is the aggregate form. All targets keep A-BS, because TS-b uses the size lemma prop:dist(i), which is proved under A-BS. Astra R1's energy pair is the O(n) form and is not identical to A-BS′(b).
6. **Referee: "Why bound signals from above at all?"** Answer:
   - It is a technical device for the Fubini denominator and the ridge term, and YWJ need the same.
   - A very large single coefficient is easy to *select* but makes the prior-mass bound loose.
   - We flag for proof audit that nothing else uses it.

## A-MARGIN-H: Hellinger-scale residual signal (TS-a, sure screening)
1. **Assumed.** For the predictor j and **every fixed k**, inf{R_n(S) : j ∉ S, |S| ≤ k}/(σ*² log n) → ∞ (a diverging ratio). Here R_n(S) is n times the linear-projection risk of the true signal on x_S. This gives screening at every fixed level M. A diverging ratio at an unspecified speed gives nothing uniform for M = M_n → ∞.
   - **TS-a is stated first per predictor** (any j satisfying its own margin, whatever the other signals do) and **then jointly** over the true predictors.
   - **Remark (fixed-level form).** At a fixed level M, inf R_n(S)/(σ*² log n) ≥ C_L·M over S with j ∉ S and |S| ≤ min(K, J(M)), J = ⌊s + C_s·M⌋, with C_L above the inverse Hellinger-conversion constant, suffices. It is sharper for finite-ratio signals and gives the a.s. corollary at a large fixed level. Larger models are handled by the posterior size tail.
2. **Why needed.** Every such model's predictive law is then farther than the TD radius from the truth, so TD contraction forces j into the model.
3. **Standard?** It is exactly the SL Theorem 3 route.
   - SL Condition 3, p. 955 (A-MARGIN-H plays its role; A-SUBG only converts R into Hellinger separation).
   - SL's proof (SLs pp. 5–6) gives d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}.
   - The same residual-signal object appears in NH14 Cond. 4.4, p. 11, and Luo & Chen, arXiv v1 p. 7.
4. **Holds on our data?** Only partly, and we say so.
   - As a **scale diagnostic only** (restricted search; radius ε_n² = s0 log p/n), the residual-variance/radius² ratio is ≥ 1 in only 9 of 136 settings (the fixed-variance squared Hellinger ratio never reaches 1), yet S1 at SNR 2 recovers 92–96% with a ratio of 0.75 (E2). This cannot certify the theorem's margin (C_H is unknown).
   - TS-a has an inexplicit constant by construction, so it is **not** claimed at boundary signal levels.
5. **Weaker forms.** None is needed. The sharp, data-relevant claim is carried by TS-b.
6. **Referee: "Your sure-screening constant is unknown."** Answer: so is SL's (c₁). TS-a is the per-predictor counterpart of SL Thm 3, and the explicit threshold is in TS-b.

## A-MARGIN-U: the identifiability margin for exact selection (TS-b, TM-b) — the central assumption
1. **Assumed.**
   - **Plain English first.** Dropping true predictors must leave more unexplained signal than **twice** the prior-plus-Occam price of those predictors, with a little room (η). When nulls are added in their place, the rival also gets an allowance for how well the added nulls can imitate the dropped signal. Inside a small accounting set Q_n of "proxy" predictors, that allowance is already paid by the same inequality on the base model. Outside Q_n, each added set pays in proportion to its **leakage share** ϑ, the share of the omitted signal that the added nulls explain beyond the base, times a Gaussian union-bound term √(2 log C(p−s, m)).
   - **Notation.** T = S0, s = |T|. For a rival S ⊉ T: B := S ∩ Q_n (its **base**), N := S ∖ Q_n, d := |T∖B|, k := |B∖T| + |N| (the number of added predictors). R_n(S) := n·E[(x_Tᵀβ*_T − L(x_Tᵀβ*_T | x_S))²], n × the population **linear projection error** of the true signal on x_S; the Schur form n·β*_Dᵀ Σ_{DD·S} β*_D holds for any design with finite second moments. ϑ(B, N) := 1 − R_n(B ∪ N)/R_n(B). Coded coefficients are θ, raw coefficients β*.
   - **Price.** For the coded prior, Pr_n(d) := max_{|D|=d} log[π(T∖D)/π(T)] + (d/2)·log(n+1); for BB(1, p) this is Σ_{k=s−d}^{s−1} price(k). For any other prior, re-derive it (the deletion refund at T need not bound the refund at T ∪ (S∖T)).
   - **Rival range.** m̄_d := ⌈(2A+1)d⌉ + 1. Rivals with more added predictors k > m̄_d need no signal condition: for p ≤ n^A their summed prior-plus-Occam odds are ≤ n^{−γ} for some γ > 0 (writing this out is part of TS-b step 2).
   - **Exact form.** Fix η > 0 and a deterministic **accounting set** Q_n ⊇ T with log|Q_n| = o(log n). For all large n:
     - **(U1) Deletions.** R_n(T∖D) ≥ 2(1+η)·σ*²·Pr_n(|D|) for every nonempty D ⊆ T. This is κ_n ≥ 1+η, and it is the case B = T∖D, N = ∅ of (U2a).
     - **(U2a) Bases.** R_n(B) ≥ 2(1+η)·σ*²·Pr_n(d) for every B ⊆ Q_n with B ⊉ T and |B∖T| ≤ m̄_d.
     - **(U2b) Outside nulls.** For every such B and every N ⊆ Q_n^c with 1 ≤ |N| = m and |B∖T| + m ≤ m̄_d: √(R_n(B ∪ N)/σ*²) ≥ √(2(1+η)·Pr_n(d)) + ā(B, N)·√(2 log C(p−s, m)), where ā(B, N) := min{1, √(2(1 − √(1 − ϑ(B, N))))}.
   - **Q_n is an accounting device, not an object to be found.** Any such Q_n may be used. Enlarging it moves rivals from (b) to (a). Leakage outside Q_n need not vanish; it is priced by ā.
   - **Reading aids.** √ϑ ≤ ā ≤ √(2ϑ) for ϑ ≤ 3/4. Within one base, (U2b) for every N is the same as min_N √R_n(B∪N) ≥ … + max_N ā·√(2 log C), since both extremes sit at the maximum-leakage N.
   - **Special cases** (stated, not separate assumptions):
     - (i) Q_n = T is the "no proxies" case: every null is priced by its own leakage.
     - (ii) If max_{B,N} ϑ(B, N)·log p → 0 outside Q_n, then (U2a) with η implies (U2b) with every η′ < η for large n.
     - (iii) ā ≡ 1 is the structure-free fallback (unit-vector bound). The coefficient is 1, not √2.
   - For pure deletions, liminf κ_n > 1 gives (U1) with some η > 0, where κ_n = min_D R_n(S0∖D)/(2σ²Pr_n(d)).
   - No numbers from S1 or S2 appear in the assumption. The form is chosen on generality grounds, and S1 is checked against it (item 4).
2. **Why needed.** The posterior odds of a rival against S0 are exp{Pr_n − ½·(gain in fit)}, and the gain in fit is (√R + noise)².
   - If R is below 2·Pr, the rival wins. That is the **converse** (target, under A-NEC on T): if limsup κ_n < 1, then π(S0|y) → 0; at a single-deletion boundary, liminf P(π(S0|y) ≤ ½) ≥ Φ(−c).
   - The constant 2 for deletions is therefore not a proof artefact. It is the threshold.
   - **Lemma W (bridge to the proof; low risk), in plain words.**
     - (W1) The **leakage share** controls how far the added nulls can move the residual direction. For S ⊇ B, the sample residual directions satisfy ⟨v_S, v_B⟩ = √(R̂(S)/R̂(B)), so ‖v_S − v_B‖ = a(ϑ̂) exactly.
     - (W2) On the two-sided sparse-isometry event on T ∪ B ∪ N (size ≤ s + m̄_d, relative error δ_n ≍ √(log(n∨p)/n)), ϑ̂ ≤ ϑ + 2δ_n/(1+δ_n), and ā(ϑ̂) ≤ ā(ϑ) + 2√δ_n.
     - (W3) **Per base, a simultaneous Gaussian bound.** There are H ≤ 2^s Σ_{b ≤ m̄_s} C(|Q_n|−s, b) = n^{o(1)} bases. With l_n := log(H+1) + t_n, t_n → ∞ and t_n = o(log n), conditionally on X and with probability 1 − O(e^{−t_n}), simultaneously over bases and N, −⟨v_S, g⟩ ≤ √(2l_n) + ‖v_S − v_B‖·√(2[log C(p−s, m) + l_n]). By the same union bound, simultaneously, −⟨v_S, g⟩ ≤ √(2[log C(p−s, m) + l_n]) directly; take the minimum of the two bounds before applying W2, so the effective chord coefficient is capped at 1 (the uncapped chord a(ϑ̂) exceeds 1 when ϑ̂ > 3/4). The surplus over ā·√(2 log C) is o_P(√log n), and the root-scale slack absorbs it because Pr_n(d) ≳ log n for d ≥ 1.
     - **Consequence.** The population form implies the **base-indexed** conditional-width condition. TS-b step 3 is run per base. For fixed D, each null set gives exactly one S, so the containing-model odds are summed once at the total null size k, with no multiplier of order H.
     - **Not implied.** The population form does not imply the v1.3 class-level conditional-width condition when Q_n ≠ T: across bases, the smallest residual and the largest width can occur at different bases. That condition is kept as a **parallel sufficient condition**, the "refined design-conditional form" (ASSUMPTIONS §3.3), and E9/E9b are diagnostics of it.
3. **Standard?** Yes in type. A comparison with NH14, **not** a dominance claim (different model ranges, priors and normalisation, and ours carries a leakage-priced term for added nulls outside Q_n; Astra R2):
   - **NH14 Cond. 4.4**, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n) for every model of size < K|t| that misses a true predictor (PN A2).
     - NH14 multiply by |t| even when one predictor is missed; ours charges per missed predictor for deletions.
     - NH14's constant is 5(1+δ); ours is 2(1+η) for deletions, plus ā·√(2 log C(p−s, m)) for added nulls outside Q_n.
   - **Luo & Chen** (EBIC consistency condition, arXiv v1 p. 7): Δ_n(s)/(p₀ ln p) → ∞, which they describe as a variant of Chen & Chen (2008)'s condition (PN A4). That is a diverging ratio; ours is a fixed ratio above 1.
   - Per-coefficient beta-min versions: YWJ (8), p. 9, C_β² ≥ c₀(L + L̃ + α + κ)σ²log p/n with unspecified c₀ (P17); Fan & Lv Cond. 3, p. 25 (PN E15).
   - **Necessity of the log p order for any method:**
     - Wainwright (2009) Thm 2, arXiv v2 p. 4: Gaussian design, averaged over random supports, unspecified C′ (PN B5).
     - Fletcher, Rangan & Goyal (2009) Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor. This constant is C2's derivation from their display (6) (PN B6).
   - **SL themselves state no margin.** Their MAP proof treats min|β_t| as a fixed constant (SLs p. 15) and needs the "hardly satisfied" sample condition (22).
4. **Holds on our data?** This is the strongest evidence in the package.
   - **S1 is consistent with κ = 1 as the threshold.** κ is 0.64–0.70 at SNR 1, with 0 of 100 exact in every (n, p) cell, and 2.54–2.80 at SNR 2, with 92–96 of 100 exact (E1). The transition is bracketed, not located.
   - **The data are consistent with the necessary direction.** P1's check min t² > 2·price has sensitivity 1.000 on S1 and 0.985 on S2 (sample). When it fails, recovery is 0 of 800 fits on S1 and 9 of 10,666 = 0.00084 on S2 (9 of 11,466 pooled); the population κ_del ≤ 1 row gives 0 on both. (P1's price numerator is one off from the exact price(s0−1); the exact all-deletion κ_n is 0.626–0.693 at SNR 1 and 2.505–2.771 at SNR 2, 1.1–1.7% below the data proxy, so the bracket is unchanged.)
   - **(U2a) check (Lead, `.rc_tmp/lead_v14/u2a_check.py`; population, no fits).** Over all 1,023 deletions D, with B = (T∖D) plus at most two of the five tested proxies (the five nulls nearest S0), the minimum of R_n(B)/(2σ²Pr_n(d)) **equals the exact κ_n**: 2.505–2.771 at SNR 2 and 0.626–0.693 at SNR 1. The binding D retain x_10, which screens every null. So on S1, (U2a) at these proxy sets is no tighter than (U1).
   - **Leakage decay on S1's AR(1) designs.** For the endpoint deletion (retained true predictors on one side), a single outside null at distance k beyond the deleted endpoint, with the intervening nulls not in the base, leaks ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}) (0.265, 0.087, 0.030, 0.011 at ρ = 0.6 for k = 1–4). Special case (ii) needs the uniform bound max ϑ·log p → 0, which L_n → ∞ alone does not give: with Q_n = T plus the L_n nearest nulls, the worst outside leakage over d ≤ 3, up to 2 inside proxies and up to 3 outside nulls is ≈ 0.25ρ^{2L_n} (unit coefficients; `.rc_tmp/lead_v14/leak_uniform.py`), so choosing L_n with ρ^{2L_n}·log p → 0 (L_n of order log log p plus a slowly diverging term, keeping log|Q_n| = o(log n)) puts the S1 sequence in special case (ii).
   - **The structure-free fallback (ā ≡ 1):** on the evaluated classes (d ≤ 3, selected D for d ≥ 2; m ≤ 2 at p = 500, m = 1 at p = 5,000) at η = 0, it fails at SNR 2 (minimum surplus −0.692 at d = 1, m = 1; −2.008 at m = 2) and holds at SNR 3 (minimum 1.412, d = 1, m = 2); m up to m̄_d is not evaluated (population computation on `tables/e9b_width_ext_s1.tsv` with the combinatorial width √(2 log C(p−s, m))).
   - **Mixed part, refined form only: E9/E9b are zero-slack diagnostics of the refined design-conditional form, not of the population form.** They use selected D (the 3 with smallest population residual per (cell, d, m)) on four simulated designs, at zero slack, so they establish no 1 − o(1) event. The estimated conditional width is 0.10–0.47 (m = 1) and 0.22–0.59 (m = 2). The exact minimum surplus at SNR 2 is **2.3862** with C = 121 (a sensitivity setting, not an implied constant) and **2.4889** with no credit, and 3.2896 at C = 1 (E9b, raw-centred mean; Monte Carlo, 4 designs × 300 draws, no fits). Not evaluated: m = 2 at p = 5,000, m ≥ 3, d ≥ 4.
   - **Multi-predictor deletions bind on S1** in all 16 settings, which is why the margin quantifies over all subsets D.
   - **The sufficiency gap is consistent with the superset term.**
     - At SNR ≥ 2, 40 of the 41 S1 failures are supersets of S0 (39 with exactly one extra null). A heuristic diagnostic, the expected number of one-null extensions beating S0, E K₁ ≈ (s0+1)/√(2πL(n+1)), is 0.031–0.050 at S1's (n, p) (0.033–0.056 under the exact Beta tail), the same order as the observed 2–8% shortfall.
     - This is consistent with, not a proof of, the superset term being the main failure mode. E K₁ bounds one failure type only and is not a ceiling on success (Astra R2). It is a mode-type diagnostic (rivals beating S0 in exact score, an HPM event; MPM failure is separate); it does **not** match TS-b's mass-rate term (s0+1)√(log p/n), which is 0.87–1.44 at S1's sizes and so not informative there.
   - **S2 is not an asymptotic regime** (s0 log p/n = 0.69). The finite-n diagnostics use the saturating gain, which puts the transition at κ ≈ 1.0–1.5 on both suites (post hoc, flagged).
5. **Weaker forms evaluated.**
   - (i) The old explicit constant c1(s0, A): replaced, since it is far above the S1 transition.
   - (ii) A fixed beta-min (FSb): it is false along S1, where β ∝ √(log p/n), so it was replaced by the fixed-ratio κ_n.
   - (iii) The memo's uniform "constant 2 for every rival": rejected. Fable built a counterexample with nulls that jointly imitate a true predictor when log n = o(log p). It remains open under p ≤ n^A.
   - (iv) Λ → ∞ with an m·log p multiplicity charge: neither sufficient nor necessary, and it ranks worse on the data (AUC 0.967 vs 0.980).
   - (v) The v1.3 class-level conditional-width form (a design-conditional width w_Dm(X) and a containing-model credit): kept as the **parallel sufficient condition** (ASSUMPTIONS §3.3), not implied by the population form when Q_n ≠ T. Its credit constant is C = 1 by convention (multiplier in the tight remainder).
   - (vi) MARGIN\*, a sharper constant for swaps under a "bounded leakage" condition: **superseded** by the population form, whose leakage share ϑ and ā make it explicit. Unlike MARGIN\*'s M1, (U2a) charges every base inside Q_n the full deletion price; letting inside proxies pay for their entry is the weaker variant (viii).
   - (vii) **Corollaries of the population form.**
     - **(C-i) Strong separation.** min R_n(S)/[σ*² log(p∨n)] → ∞ over feasible underfits with |S∖T| ≤ m̄_s implies (U1)–(U2) with Q_n = T.
     - **(C-ii) Sparse eigenvalue plus beta-min.** Let φ² lower-bound λ_min(Corr(x_V)) over |V| ≤ s + m̄_s, and θ_min := min_{j∈T} |β*_j|·sd(x_j)/σ*. Then θ_min ≥ (1+η)·(1 + √m̄_s)·√(2 log(2p√(n+1))/n)/φ implies (U1) and (U2) with ā ≡ 1. For an orthogonal design, a sufficient coordinatewise form of (U1) is β*_j²Var(x_j) ≥ 2(1+η)σ*²·log(2p√(n+1))/n for every j ∈ T; exact (U1) requires n·Σ_{j∈D} β*_j²Var(x_j) ≥ 2(1+η)σ*²·Pr_n(|D|) for each nonempty D.
   - (viii) **Weaker variant (recorded, not adopted): proxies pay their own price.** (U2a) could be weakened to the single-rival price [log π(B)/π(T) + ((s−|B|)/2)log(n+1)]₊ for |B| < s; R_n(B)/(σ*²(1+log|Q_n|)) → ∞ for |B| = s; and no condition for |B| > s. This needs TS-b step 2 on the bases T ∪ (B∖T), which is not written. The headline (U2a) is therefore conservative, by a factor (1+ρ²)/(1−ρ²) on the signal when both AR(1) neighbours of an isolated true predictor are proxies, and similarly for block designs.
6. **Referees.**
   - **"Your condition is uncheckable."** Answer: R_n(S) is a population projection residual, the same object as NH14's Δ_n and Rossell's non-centrality λ_tm (arXiv v7 p. 10). For any assumed Σ and β it is computable in closed form, as D1 did for all 136 settings. We also give worked cases: orthogonal, AR(1), block, equicorrelated.
   - **"Why a width term for swaps?"** Answer: it is needed in some designs. In a factor-proxy design a single swap beats S0 unless R ≥ 2(1+ρ)²log p (Fable, numerical check). That shows necessity of the worst-case form at one (d, m), not optimality of every constant. The population form prices each added null by its own leakage, so where leakage is small the condition is close to the deletion threshold; on S1's AR(1) designs (estimated) the leakage decays geometrically with distance.
   - **"Your condition depends on the design."** Answer: it is a population condition on (Σ, β*), with no design event. The refined design-conditional form (a parallel sufficient condition) is stated on a design event of probability 1 − o(1). The structure-free fallback (ā ≡ 1) is always available, at the cost of not covering boundary signals at SNR 2.
   - **"How do I construct Q_n?"** Answer: you do not. Q_n is an **accounting device**: any deterministic Q_n ⊇ T with log|Q_n| = o(log n) may be used, and a larger Q_n only moves rivals from (U2b) to (U2a). Q_n = T is always allowed.
   - **"Why this width?"** Answer: the width is ā·√(2 log C(p−s, m)), where ā is a function of the leakage share ϑ. ā is exactly 0 when ϑ = 0 (orthogonal, screened nulls). At the structure-free fallback the coefficient is 1 and the width allowance is √(2 log C(p−s, m)). See the worked cases below.

## Worked cases for A-MARGIN-U (closed forms)
Each case gives the conditioning set and the coefficients; leakage depends on both for multi-deletions. All four were checked numerically in `.rc_tmp/lead_v14/worked_cases.py`.
1. **Orthogonal design.** R_n(T∖D) = n·Σ_{j∈D} β*_j² Var(x_j), and the leakage is 0. Conditioning set: Q_n = T. (U1) is the whole condition, and ā = 0 for every outside null.
2. **AR(1) with correlation ρ.**
   - Deleting an interior predictor whose two neighbours are retained gives Var(x_j | rest) = (1−ρ²)/(1+ρ²) per unit β², and leakage 0 (screened by the retained neighbours).
   - Deleting an endpoint gives 1−ρ².
   - Conditioning set: the retained true predictors on one side of a deleted endpoint. A single outside null at distance k beyond the endpoint (intervening nulls not in the base) leaks ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}), which decays geometrically. Accounting set: Q_n = T plus the L_n nearest nulls on each side, with ρ^{2L_n}·log p → 0 for special case (ii) (or Q_n = T, with every null priced by its own leakage).
3. **Block design, fixed block size b, equicorrelation within blocks.** Only same-block nulls leak. Conditioning set: Q_n = the blocks of T, so |Q_n| ≤ s·b, a constant.
4. **Equicorrelation ρ (one factor).** One omitted true predictor, b retained, m added nulls: leakage = mρ²/[(1+bρ)(1+(b+m−1)ρ)], which is ρ²/(1+bρ)² at m = 1 and tends to ρ/(1+bρ) as m grows. Every null leaks equally, so no small Q_n makes outside leakage vanish. Q_n = T is admissible even with positive leakage, and (U2b) is priced by ā. The formula describes the equal-loading one-factor case.

**Reading.**
- Cases 1–3 are where a **small Q_n exists**: leakage outside Q_n is zero or decays, special case (ii) applies, and (U2b) follows from (U2a).
- Case 4 is where the **interpolated form operates**: Q_n = T, ϑ is bounded away from 0, and ā(ϑ) sits strictly between 0 and the unit-vector value 1 whenever ϑ < 3/4. The condition then charges less than the structure-free fallback and more than the screened case.
- The structure-free fallback (ā ≡ 1) is the worst case over all of these.

## A-MIS(iii): the working residual for misspecification (TM-a, TM-b)
1. **Assumed (primitive form).**
   - The candidate set C is fixed before the analysis sample is drawn, or chosen on independent data (choosing it from the same design before seeing y is not enough). The statement is **conditional on each admissible C**, with the candidate dimension in the cap, price, window and prior.
   - For the omitted true predictors O, x_Oᵀβ*_O = a + x_Cᵀγ + e with e ~ N(0, τ²) independent of x_C, τ² ≥ 0. Then β^C = β*_C + γ and σ_C² = σ*² + τ². This is equivalent to the v1.3 statement (Cramér decomposition).
   - Uniqueness of the projection β^C comes from a sparse representation together with A-NEC; Σ_CC full rank is a sufficient version (A-NEC alone does not give it).
   - The working residual u = y − α_C − x_Cᵀβ^C is then independent of x_C and Gaussian N(0, σ_C²). The other assumptions hold for the candidate problem, including A-SPARSE-C below.
2. **Why needed.** The candidate-only data are then exactly a correctly specified Gaussian linear model with parameters (β^C, σ_C²), so TD and TS-b apply verbatim with SL's f₀ in place of f*.
   - TM-a / TM-b are corollaries of TD and TS-b **conditional on each admissible C**. An unconditional statement needs common constants and a common validity threshold over admissible candidate sets, and then adds + P(C inadmissible), which vanishes identically under almost-sure admissibility. The a.s. corollary needs summable exception probabilities.
3. **Standard?**
   - SL Thm 4/Cor 2 (p. 957) use the same f₀ ((17) and (19)).
   - Rossell (2022) Prop. 6 (arXiv v7 pp. 16–17) is a fixed-design misspecified-mean analogue with omitted variables (PN D13).
   - Jointly Gaussian candidates and omitted predictors satisfy (iii) (supplement `ex:omitted`).
4. **Holds on our data?**
   - Only illustrated. The posterior σ² against σ_C² has median 0.99 on S1 and 0.84–0.98 on S2 (E7), consistent with the noise variance absorbing omitted signal. But C there is the MPM selected on the same, well-specified data, so this is an in-sample illustration, not a test of independence, Gaussianity or of a prespecified C.
   - Hidden-column tests need refits, which have not been run and require HQ approval.
5. **Weaker forms.**
   - **TM-a0** (one fixed law, fixed number of candidates, second moments for density consistency, plus a mixed second moment of the scores for *exact* support selection, almost sure) is the literal SL Thm 4 counterpart and is stronger than SL Cor 2. It lies outside A-GL.
   - Independent non-Gaussian residual: remark (i′), a suggested sufficient cap and budget.
   - Heteroscedastic residual: remark (ii), a heuristic budget and the Grünwald–van Ommen link (their evidence is empirical and does not establish our proposed threshold).
6. **Referee: "This isn't real misspecification."** Answer:
   - TM-a0 covers arbitrary second-moment misspecification at fixed dimension, which is SL's own setting.
   - In high dimension we target the independent-Gaussian-residual case, and our heuristic remark (ii) suggests heteroscedastic misspecification can break selection once p exceeds about n^{1/(2(ϱ̄−1))}. This threshold is ours and heuristic; it is in the spirit of Grünwald & van Ommen's empirical finding that the general theorems (Kleijn–van der Vaart 2006, De Blasi–Walker 2013) need a fixed model class (GvO arXiv v3 pp. 46–47; PN D10–D12).

## A-SPARSE-C: the candidate-level projection is sparse (new label)
1. **Assumed.** |supp β^C| ≤ s_C, with s_C fixed. This is A-SPARSE applied to the candidate projection β^C = β*_C + γ of A-MIS(iii).
2. **Why needed.** TD and TS-b are run on the candidate problem, so the same sparsity arguments (small posterior size window, finitely many deletions, one-null superset mass) need the candidate truth to be sparse. It also supports uniqueness of β^C together with A-NEC.
3. **Standard?** It is the candidate-level form of A-SPARSE (SL (4), p. 950; NH14 Cond. 4.3, p. 11). SL Thm 4 fixes a candidate subset (Condition 4, p. 957) and so is in the same spirit.
4. **Holds on our data?** Not tested. It **holds under Markov-type separation**: in a Gaussian AR(1) (a Markov chain), the nearest retained candidates on each side separate an omitted predictor from all other candidates, so it projects on at most two of them. Local covariance dependence alone need not give a sparse regression. So γ has at most 2 nonzero entries per omitted predictor. S1/S2 have no hidden columns, so this is a structural statement, not a check.
5. **Weaker forms.** The relaxation is TD-A (approximate sparsity, in the style of SL (3)). It **fails under pervasive factors**, where the projection of an omitted predictor on the candidates is dense.
6. **Referee: "Omitted variables are rarely local."** Answer: agreed. Under a pervasive factor the sparsity of β^C fails, and then only the approximate-sparsity corollary TD-A is claimed. Designs in which a few candidates separate each omitted predictor from the rest (Markov-type dependence, as for neighbouring markers or adjacent time points) are the case covered.

## A-MOM: moments for TM-a0
1. **Assumed.** One fixed i.i.d. law along a nested sample sequence; a fixed number p_C ≥ 2 of candidates (the coded posterior is undefined with fewer than two retained predictors; such data sets, and constant columns or response, form an exceptional event that is eventually empty a.s.); coded centring (no intercept parameter in the prior), Z = (1, x_Cᵀ)ᵀ for the scores; E‖x_C‖² < ∞, E y² < ∞, σ_C² > 0; Σ_CC nonsingular; the fixed coded BB(1, p_C) prior. For exact selection, also E[Z_j²u²] < ∞ (a mixed second moment of the scores, not fourth moments of x and y).
2. **Why needed.** The strong law makes each model's residual variance converge, and the law of the iterated logarithm, ‖Σ_i Z_i u_i‖ = O_a.s.(√(n log log n)), controls spurious gains (O(log log n) against the (m/2) log n penalty). An n-dependent truth is excluded: with β_n = 1/n even fixed-p support selection fails.
3. **Standard?** For density consistency it is SL Condition 4 (p. 957), and SL's proof relies on "a fixed number of possible models" (SLs p. 7); SL also assume a Gaussian parent model and positive priors. For exact support selection the score moment E[Z_j²u²] < ∞ and the SLLN/LIL argument are our addition.
4. **Holds on our data?** Trivially, since all rows are Gaussian.
5–6. This is SL's own setting. **Second moments suffice for inclusion**: TM-a0-inc (new target, the SL Cor 2 counterpart) states Π(S ⊇ S0^C | data) → 1 a.s. under the second moments only; full rank and finitely many underfits give a positive risk gap. The score moments E[Z_j²u²] < ∞ are needed **only for exclusion** (TM-a0 exact). The improvement over SL is exact selection instead of inclusion.

---

## Questions about what we *removed* or *did not assume*
- **"Where is the eigenvalue floor on the true model?"** No *fixed* floor is needed. R_n(S0∖{j}) = n β_j² Var(x_j | rest) already enters the margin, so a fixed floor would only add a stronger condition (Astra and Fable, independently). The vanishing floor A-NEC on T is still used by the converse.
- **"Where is SL's identifiability Condition 3?"** Its role is taken by A-MARGIN-H, an explicit lower bound on the residual signal R. Sub-Gaussian rows do **not** imply it (Gaussian duplicates have R = 0); they only convert R into Hellinger separation, d_H² ≥ c_L·min{1, R/(nσ²)}. In Gaussian AR(1) it holds with δ_SL = 0.23–0.42, but SL's requirement ε_n² = o(δ_SL) fails numerically on S2 (E3).
- **"Why no sample sparse eigenvalue condition, as in Thm S?"** On S2 it is vacuous (1e−5). SL themselves call theirs "hardly satisfied" and replace it with a random-design version (SLs pp. 15–16).
- **"SL's Theorem S / Cor S1: how do we compare?"**
  - Our conclusion is stronger: π(S0|y) → 1 with a rate, versus pairwise MAP odds.
  - Our conditions are different and, on the points checked, milder: a population vanishing floor versus a sample floor, and an explicit margin versus an implicit fixed beta-min. We do not claim uniform dominance.
  - Audit flags on SL, which we report but do not use:
    - their proof bounds a max where a min is needed;
    - Cor S1's endpoint does not follow from Thm S's printed √(log P_n) condition;
    - the ridge "Lemma A.2" is absent from the supplement.
- **"Does changing g or the size prior break anything?"**
  - The form of every statement is invariant; the price in the margin moves (g = n → c·n shifts it by ½log[(1+cn)/(1+n)] at fixed k), and a small g also enlarges the slab loss O(n/g). Any fixed cap K ≥ s0 preserves S0.
  - **Engine decision (HQ, SMC-PERF closed, memo 1b319090):** v3.1.1, g = n, truncated BB(1, p) and MPM are confirmed; Fix E (output-only) and C1 (compute-only) do not touch the theorems. Proof writing and Lean stay on hold.
  - One correction to our own earlier note (TH_PREP §3): BB(1, p^u) with u < 1 does not cause a price deficit. It loses the 2^{−k} size tail, so a size cap would be needed. Both advisors found this independently; Astra R2 confirms it for fixed small k.

## Known weak points (stated before the owner finds them)
1. **TD′** (beyond p ≤ n^A) is a conjecture with **high proof risk**: Astra R2 showed Fable's route fails at the testing step. Nothing is released beyond p ≤ n^A.
2. **TS-a** is not a boundary-signal result (inexplicit constant).
3. **MARGIN\*** (sharper swap constant) is **superseded by the population form** of A-MARGIN-U; no separate refinement is open under that name.
4. **Evidence on S1** brackets the transition with only two informative SNR levels. SNR 1.25 and 1.5 cells would locate it, but they need fits and HQ approval.
5. **TS-b proof obligations** (Astra R2, council R1, senior review): TS-b is a target, not a theorem. Still to be written: the truncated superset sum, the coded mixed odds **per base** (the base-indexed step 3, Lemma W), the size lemma under A-BS, and the **k > m̄_d step** (rivals with more than m̄_d added predictors, step 2). Polynomial p and fixed s remain, against SL Cor 1. A-NEC necessity is unproved.
6. **Literature.** The Chen & Chen (2008) primary text is unverified (paywalled; attested second-hand via Luo & Chen p. 7 and SBJ p. 14). Grünwald–van Ommen are verified on the 2014 arXiv text, not the Bayesian Analysis 2017 pagination.
7. **Mixed-rival evidence is partial.** E9/E9b are zero-slack diagnostics of the **refined design-conditional form only** (selected D, four simulated S1 designs, mean widths; no 1 − o(1) event) for d ≤ 3, m = 1 (all S1 cells) and m = 2 (p = 500). The population form is checked only by the (U2a) minimum, which equals κ_n at ≤ 2 inside proxies. m = 2 at p = 5,000, m ≥ 3 (active at S1's sizes), d ≥ 4 and S2 designs are not evaluated.
8. **No necessity result for (U2b).** The constant 2 is sharp only for deletions, and the common-base bound is conservative when many null sets leak in nearly the same direction.
9. **The high-dimensional TM tier assumes a Gaussian-linear candidate law.** Only TM-a0 and TM-a0-inc tolerate a wrong response law.
10. **TD′ must pay an O(M log p) testing budget** on a sieve with a much larger entropy, so it stays a high-risk conjecture (see item 1).
