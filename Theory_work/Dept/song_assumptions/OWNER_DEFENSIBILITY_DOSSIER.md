# OWNER DEFENSIBILITY DOSSIER: assumption-by-assumption Q&A

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v1.1 (pre-council; Astra round-2 corrections applied).**

This file is for the owner's grilling. Each assumption gets the same six questions:
1. What exactly is assumed?
2. Why is it needed, and which proof step uses it?
3. Is it standard?
4. Does it hold on our data?
5. Can it be weakened, and what happens if it fails?
6. What a hostile referee will say, and our answer.

Sources and conventions:
- **Citations.** "P17" means `writing_answers/PRECEDENTS_2026-11-17.md` and "PN" means `PRECEDENTS_NEW.md`. Both were verified against the PDFs; page numbers are those of the version named there. SL means Song & Liang (2015) main text (journal pages) and SLs its supplement (printed pages).
- **Numbers.** All numbers come from `SIMULATION_DATA_ANALYSIS.md` (D1, sections E0–E8).
- **Proofs.** No proofs are claimed. Proof paths are in `ASSUMPTIONS_AND_PROOF_PATHS.md` §3, and targets are defined in `THEOREM_DEFINITIONS.md` §4.

**Score card (Lead's self-assessment before the council; the council scores independently in COUNCIL_RECORD.md).**

| assumption | theorems | standard? | holds on S1/S2? | weaker form evaluated |
|---|---|---|---|---|
| A-GL | all | yes (SL (1), NH14, YWJ) | by construction | non-Gaussian / heteroscedastic noise: remarks |
| A-SPARSE | all | yes (SL (4), NH14 4.3) | s0 = 5, 10 | growth remark |
| A-DIM | TD, TS, TM | yes (SBJ p. 14, JR12, SL Cor S1) | A ≤ 1.77 | A-DIM′ (TD′, conjecture, high proof risk) |
| A-SUBG | all | yes (SL Cond. 1, RZ, NH14 L6.1) | Gaussian rows | moments-only in TM-a0 |
| A-NEC | all | weaker than SBJ, NH14, BRT09, SL (26) | margin 8.8–250× | for TD: drop it at a √log p cost (prop:dist(ii)); for TS-b sufficient, necessity unproved |
| A-BS / BS′ | all | yes (YWJ (7a), SC11 2.7) | ≤ 1.17σ | aggregate energy (BS′): recorded, not adopted |
| A-MARGIN-H | TS-a | SL Cond. 3 + Thm 3 proof | ≥ 1 in only 9/136 | not needed for the sharp claim |
| A-MARGIN-U | TS-b, TM-b | same type as NH14 4.4, Luo–Chen (comparison, not dominance) | S1 consistent with κ = 1 (bracketed) | constant 2 sharp for deletions (converse, with A-NEC on T) |
| A-MIS(iii) | TM-a, TM-b | SL f₀; Rossell 2022 Prop. 6 | σ² ratio 0.99 | (i′), (ii) as remarks; TM-a0 moments-only |

---

## A-GL: Gaussian linear model with i.i.d. pairs
1. **Assumed.** y = α* + xᵀβ* + ε with ε ~ N(0, σ*²) independent of x, and (x_i, y_i) i.i.d. All parameters may depend on n.
2. **Why needed.** The posterior is computed exactly from conjugate marginals.
   - RSS ratios of nested models then have exact Beta laws. TS-b's superset step relies on this, because that tail is Pareto-like and cannot be bounded by expectations.
   - The Fubini identity E*[m_S/f*] = 1, which bounds the posterior size, needs the likelihood to be correctly specified.
3. **Standard?** Yes.
   - SL model (1), p. 947, is the same model without an intercept.
   - NH14 Cond. 4.3, p. 11 (PN A2), and YWJ p. 7 (PN E17).
   - Jiang (2007) uses i.i.d. random design and Hellinger distance on joint densities (p. 7; PN C7).
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
3. **Standard?** SL strict sparsity (4), p. 950, used by SL Thms 2–4; NH14 Cond. 4.3, p. 11, "the size of the true model |t| is fixed" (P17).
4. **Holds on our data?** s0 = 10 on S1 and 5 or 10 on S2.
5. **Weaker forms.**
   - Growing s0 is possible for TS-b if s0²·log p = o(n) and s0·(log p)² = o(n).
   - The delivered `rem:sharp`(a) (valid for s ≤ min(K−1, p/2)) shows π(S0|y) → 1 is impossible unless s0 = o(√n), whatever the proof. The rate s√(log p/n) itself is not claimed as a universal necessity for growing s (Astra R2).
   - Approximate sparsity in the style of SL (3) is the optional corollary TD-A.
6. **Referee: "Fixed s is restrictive."** Answer: it is standard (SL, NH14). Growth rates are stated in a remark, and `rem:sharp`(a) shows that s0 cannot grow as fast as √n for this conclusion with *any* proof (for s ≤ min(K−1, p/2)).

## A-DIM: p ≤ n^A (released statements)
1. **Assumed.** 2 ≤ p ≤ n^A for a fixed A ≥ 1.
2. **Why needed.**
   - Union bounds over model sets of size up to the window q_n ≍ log n stay manageable: there are exp(O(log² n)) such sets (not polynomially many), which the testing budget absorbs.
   - The delivered size lemma prop:dist(i) (Fubini coarse cutoff plus fractional-moment localisation) is proved at p ≤ n^A. It gives the bounded-size event |S| ≤ J = s + C_s·M on which TS-b tests every rival class.
3. **Standard?**
   - SBJ p. 14: results "continue to hold when p grows polynomially" (P17 B2).
   - Johnson & Rossell (2012) Thm 1, p. 651, require p ≤ n (PN E16).
   - SL's own MAP corollary (Cor S1, SLs p. 16) is quasi-polynomial, P_n < n^{κ log n} with κ < ¼ (page image checked).
4. **Holds on our data?**
   - A = log p/log n is 0.90–1.37 on S1 and 1.50–1.77 on S2.
   - The typical user regimes we tabulated (from n = 100, p = 10³ to n = 10⁴, p = 5·10⁵) have A ≤ 1.77, so p ≤ n² everywhere (E6).
5. **Weaker forms.**
   - **A-DIM′**: s·M·log p·log(p∨n) ≤ c·n, i.e. (log p)² = o(n). TD′ under A-DIM′ is a **conjecture with high proof risk**.
     - Fable's route (Fubini size tail + isometry) fails at the testing step (Astra R2): at log p = n^{1/3} the entropy of the size window is ≍ n^{2/3} against a testing budget ≍ n^{1/3}.
     - A proof would need localisation at size ≈ t/log p or a direct predictive bound. If it worked, it would cover SL Cor S1's range and SL Cor 1 for α < ½.
   - **log p = o(n)** with a model-size cap K_n ≤ c·n/log p (NH14 uses p ∧ n/((2+ν) log p), pp. 10–11): the cap fixes the isometry step, not the testing step, so this too is open. It would also be an Engineering decision, because the code uses K = n/2.
6. **Referee: "SL handle exponential p; you don't."** Answer:
   - SL's exponential range (Cor 1) relies on their model-size cap r̄_n and the prior conditions (9)–(10), which would fail at our K = n/2.
   - Beyond p ≤ n^A we state a conjecture (TD′) and say honestly that our best route fails at the testing step. We release nothing beyond p ≤ n^A.
   - SL's own *selection* result (Cor S1) is only quasi-polynomial, P_n < n^{κ log n}, and all our S1/S2 settings and tabulated user regimes have p ≤ n².

## A-SUBG: sub-Gaussian predictors on sparse directions
1. **Assumed.** For all u with at most q_n nonzero entries, E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2). The scale is the direction's own variance, so this is relative and allows correlated designs.
2. **Why needed.**
   - (i) A lower sparse isometry: the sample residual signal R̂(S) is within (1 ± δ) of the population R_n(S) on small sets. This is how population margins transfer to the data.
   - (ii) A conversion inequality d_H² ≥ c_L·min{1, R/(nσ²)} for any model that misses signal R (relative SUBG gives E V⁴ ≤ C_L(E V²)², then Paley–Zygmund and Gaussian conditional affinity; Astra R2 Q4). This converts R into Hellinger separation; it does **not** imply SL's Condition 3 (Gaussian duplicates are sub-Gaussian with R = 0). The lower bound on R is supplied separately by A-MARGIN-H.
3. **Standard?** SL Condition 1, p. 953 (exponential moments on sparse directions); RZ Def. 1.5/Thm 1.6, pp. 5–6; NH14 Lemma 6.1, p. 16 (P17 B7b).
4. **Holds on our data?** S1/S2 rows are Gaussian AR(1), so it holds with L = 1.
5. **Weaker forms.**
   - Second moments only (SL Condition 2), plus a mixed second moment of the scores for exact support, is adopted in fixed dimension as TM-a0.
   - In growing dimension the exact-marginal route needs exponential tails, so we do not claim it there.
6. **Referee: "Binary or heavy-tailed predictors?"** Answer:
   - A rare binary predictor is not sub-Gaussian at its own scale (P17 B7b note), so this is a real limitation, and it is stated.
   - Bounded predictors with variance bounded below are covered.

## A-NEC: no near-exact collinearity (a vanishing floor)
1. **Assumed.** The smallest eigenvalue of the population correlation matrix of every set of at most q_n predictors is ≥ c_ψ/n. This floor tends to zero.
2. **Why needed.** It is a **sufficient, convenient** route to determinant and shrinkage control; its necessity as stated is unproved (Astra R2).
   - Superset step: adding a null predictor must cost the full Occam factor (n+1)^{−1/2}. Heuristically, a null nearly collinear with the current model would pay almost nothing, and supersets would keep posterior mass.
   - Converse: A-NEC on T gives the two-sided refund d·log(n+1)/2 + O(1), which the converse needs.
   - Forward deletion step: needs **no** floor, because the Occam refund is ≤ (n+1)^{d/2} for any design (Cauchy interlacing).
3. **Standard?** It is *weaker* than every verified precedent:
   - SBJ Assumption 4 (ν ≻ τ/n), p. 14;
   - NH14 Cond. 4.5, pp. 11, 17;
   - BRT09 Assumption 2, p. 9 (c/log n);
   - MY09 "slowly vanishing" (P17 B6);
   - SL's (26), SLs p. 15, which is a fixed-type sample floor that SL themselves introduce because their (22) "is hardly satisfied" (SLs p. 15).
4. **Holds on our data?**
   - Population floors are (1−ρ)/(1+ρ) = 0.176–1, i.e. 8.8–250 times c_ψ/n (E5).
   - Sample sparse floors at the delivered fixed-design set sizes are vacuous on S2 (1e−5 to 2e−4). This is why we **dropped every sample floor and every fixed floor**.
5. **Weaker forms.** For TD: drop A-NEC entirely; the delivered prop:dist(ii) still gives TD, with one extra √log(p∨n) factor in the radius. For TS-b: no weaker form is established. A fixed floor on a smaller window does not imply A-NEC on a larger window.
6. **Referee: "Eigenvalue conditions are uncheckable."** Answer:
   - Ours is a population condition with a floor that tends to zero.
   - It fails only for exact or near-exact duplicates and linear dependences (one-hot coding, compositions), which users remove anyway.

## A-BS / A-BS′: bounded signal
1. **Assumed.**
   - A-BS (as delivered; used for TD **and** TS-b/TM-b): |β*_j|·sd(x_j) ≤ b̄σ*.
   - A-BS′ (recorded, **not adopted**): β*ᵀΣβ* ≤ M_μσ*² and max_j |β*_j|sd(x_j) ≤ b̄_nσ* with s·b̄_n² = o(n). It becomes usable only once the size lemma prop:dist(i) is re-proved under it (Astra R2).
2. **Why needed.**
   - It gives a lower bound on the true model's marginal likelihood relative to the truth, which is the denominator of the Fubini size bound.
   - It keeps the estimated noise variance in a fixed range.
   - It controls the unit-ridge shrinkage term.
3. **Standard?** YWJ (7a), p. 7: "some form of upper bound on the norm ‖β*‖₂ … is required" (P17 B4b); SC11 Assumption 2.7, p. 7.
4. **Holds on our data?** Max |β|sd/σ ≤ 1.17 and βᵀΣβ/σ² ≤ 6 in every setting (E4).
5. **Weaker forms.** A-BS′ is the aggregate form. All targets keep A-BS, because TS-b uses the size lemma prop:dist(i), which is proved under A-BS. Astra R1's energy pair is the O(n) form and is not identical to A-BS′(b).
6. **Referee: "Why bound signals from above at all?"** Answer:
   - It is a technical device for the Fubini denominator and the ridge term, and YWJ need the same.
   - A very large single coefficient is easy to *select* but makes the prior-mass bound loose.
   - We flag for proof audit that nothing else uses it.

## A-MARGIN-H: Hellinger-scale residual signal (TS-a, sure screening)
1. **Assumed.** For each true j, every model of size ≤ q_n that omits j leaves residual signal R_n(S) ≥ C_H·M·σ*²·log(p∨n). Here R_n(S) is n times the linear-projection risk of the true signal on x_S.
2. **Why needed.** Every such model's predictive law is then farther than the TD radius from the truth, so TD contraction forces j into the model.
3. **Standard?** It is exactly the SL Theorem 3 route.
   - SL Condition 3, p. 955 (A-MARGIN-H plays its role; A-SUBG only converts R into Hellinger separation).
   - SL's proof (SLs pp. 5–6) gives d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}.
   - The same residual-signal object appears in NH14 Cond. 4.4, p. 11, and Luo & Chen, arXiv v1 p. 7.
4. **Holds on our data?** Only partly, and we say so.
   - The per-variable screening margin divided by ε_n² is ≥ 1 in only 9 of 136 settings, yet S1 at SNR 2 recovers 92–96% with a ratio of 0.75 (E2).
   - TS-a has an inexplicit constant by construction, so it is **not** claimed at boundary signal levels.
5. **Weaker forms.** None is needed. The sharp, data-relevant claim is carried by TS-b.
6. **Referee: "Your sure-screening constant is unknown."** Answer: so is SL's (c₁). TS-a is the per-predictor counterpart of SL Thm 3, and the explicit threshold is in TS-b.

## A-MARGIN-U: the identifiability margin for exact selection (TS-b, TM-b) — the central assumption
1. **Assumed.**
   - Exact form (Astra R2), for every rival S that misses d ≥ 1 true predictors and adds m ≤ J = s + C_s·M nulls, with fixed 0 < δ < 1, γ > 0 and t_n → ∞:
     √((1−δ)R_n(S)/σ*²) ≥ w_Dm + t_n + √(2(1+δ)[B_Dm]₊), B_Dm = Pr_n(d) − (m/2)log(n/(C log p)) + γ log n.
     w_Dm is the one-sided conditional Gaussian width of the m added nulls (w_D0 = 0; one may always use w_Dm ≤ √(2 log C(p−s0, m)) ≈ √(2m log p)).
   - Plain form: dropping true predictors must leave more unexplained signal than **twice** the prior-plus-Occam price of those predictors, with a little room. When nulls are added in their place, there is an extra allowance w_Dm ≈ √(2m log p) for the best-looking nulls among the p candidates.
   - For pure deletions, liminf κ_n > 1 implies the condition for some small δ, γ > 0, where κ_n = min_D R_n(S0∖D)/(2σ²Pr_n(d)).
2. **Why needed.** The posterior odds of a rival against S0 are exp{Pr_n − ½·(gain in fit)}, and the gain in fit is (√R + noise)².
   - If R is below 2·Pr, the rival wins. That is the **converse** (target, under A-NEC on T): if limsup κ_n < 1, then π(S0|y) → 0; at a single-deletion boundary, liminf P(π(S0|y) ≤ ½) ≥ Φ(−c).
   - The constant 2 for deletions is therefore not a proof artefact. It is the threshold.
3. **Standard?** Yes in type. A comparison with NH14, **not** a dominance claim (different model ranges, priors and normalisation, and ours carries a positive width term for mixed rivals; Astra R2):
   - **NH14 Cond. 4.4**, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n) for every model of size < K|t| that misses a true predictor (PN A2).
     - NH14 multiply by |t| even when one predictor is missed; ours charges per missed predictor for deletions.
     - NH14's constant is 5(1+δ); ours is 2(1+δ) for deletions, plus w_Dm for added nulls.
   - **Luo & Chen** (EBIC consistency condition, arXiv v1 p. 7): Δ_n(s)/(p₀ ln p) → ∞, which they describe as a variant of Chen & Chen (2008)'s condition (PN A4). That is a diverging ratio; ours is a fixed ratio above 1.
   - Per-coefficient beta-min versions: YWJ (8), p. 9, C_β² ≥ c₀(L + L̃ + α + κ)σ²log p/n with unspecified c₀ (P17); Fan & Lv Cond. 3, p. 25 (PN E15).
   - **Necessity of the log p order for any method:**
     - Wainwright (2009) Thm 2, arXiv v2 p. 4: Gaussian design, averaged over random supports, unspecified C′ (PN B5).
     - Fletcher, Rangan & Goyal (2009) Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor. This constant is C2's derivation from their display (6) (PN B6).
   - **SL themselves state no margin.** Their MAP proof treats min|β_t| as a fixed constant (SLs p. 15) and needs the "hardly satisfied" sample condition (22).
4. **Holds on our data?** This is the strongest evidence in the package.
   - **S1 is consistent with κ = 1 as the threshold.** κ is 0.64–0.70 at SNR 1, with 0 of 100 exact in every (n, p) cell, and 2.54–2.80 at SNR 2, with 92–96 of 100 exact (E1). The transition is bracketed, not located.
   - **The necessary direction is exact in the data.** min t² > 2·price has sensitivity 1.000 on S1, and on S2 it is 1.000 in population and 0.985 in sample. Recovery when it fails is 0 on S1 and 9 of 11,466 fits on S2.
   - **Multi-predictor deletions bind on S1** in all 16 settings, which is why the margin quantifies over all subsets D.
   - **The sufficiency gap is consistent with the superset term.**
     - At SNR ≥ 2, 40 of the 41 S1 failures are "S0 plus a null". A heuristic diagnostic, the expected number of one-null extensions beating S0, E K₁ ≈ (s0+1)/√(2πL(n+1)), is 0.033–0.056 at S1's (n, p), the same order as the observed 2–8% shortfall.
     - This is consistent with, not a proof of, the superset term being the main failure mode. E K₁ bounds one failure type only and is not a ceiling on success (Astra R2). It matches the order of the (s0+1)√(log p/n) term in TS-b's rate (`rem:sharp`(b) gives a lower bound of that order for witness designs).
   - **S2 is not an asymptotic regime** (s0 log p/n = 0.69). The finite-n diagnostics use the saturating gain, which puts the transition at κ ≈ 1.0–1.5 on both suites (post hoc, flagged).
5. **Weaker forms evaluated.**
   - (i) The old explicit constant c1(s0, A): replaced, since it is far above the S1 transition.
   - (ii) A fixed beta-min (FSb): it is false along S1, where β ∝ √(log p/n), so it was replaced by the fixed-ratio κ_n.
   - (iii) The memo's uniform "constant 2 for every rival": rejected. Fable built a counterexample with nulls that jointly imitate a true predictor when log n = o(log p). It remains open under p ≤ n^A.
   - (iv) Λ → ∞ with an m·log p multiplicity charge: neither sufficient nor necessary, and it ranks worse on the data (AUC 0.967 vs 0.980).
   - (v) TS-b\*, a sharper constant 2 + η for swaps under a "bounded leakage" condition, is a medium-risk refinement.
6. **Referees.**
   - **"Your condition is uncheckable."** Answer: R_n(S) is a population projection residual, the same object as NH14's Δ_n and Rossell's non-centrality λ_tm (arXiv v7 p. 10). For any assumed Σ and β it is computable in closed form, as D1 did for all 136 settings. We also give worked cases: orthogonal, AR(1), block, equicorrelated.
   - **"Why √(2m log p) for swaps?"** Answer: it is needed in some designs. In a factor-proxy design a single swap beats S0 unless R ≥ 2(1+ρ)²log p (Fable, numerical check). That shows necessity at one (d, m), not optimality of every constant; the sharper leakage form is TS-b\*.

## A-MIS(iii): the working residual for misspecification (TM-a, TM-b)
1. **Assumed.**
   - The candidate set C is chosen before seeing the outcome, or on independent data.
   - The working residual u = y − α_C − x_Cᵀβ^C is independent of x_C and Gaussian N(0, σ_C²).
   - The other assumptions hold for the candidate problem.
2. **Why needed.** The candidate-only data are then exactly a correctly specified Gaussian linear model with parameters (β^C, σ_C²), so TD and TS-b apply verbatim with SL's f₀ in place of f*.
3. **Standard?**
   - SL Thm 4/Cor 2 (p. 957) use the same f₀ ((17) and (19)).
   - Rossell (2022) Prop. 6 (arXiv v7 pp. 16–17) treats exactly a Gaussian truth with omitted variables (PN D13).
   - Jointly Gaussian candidates and omitted predictors satisfy (iii) (supplement `ex:omitted`).
4. **Holds on our data?**
   - Partly testable. The posterior σ² against σ_C² has median 0.99 on S1 and 0.84–0.98 on S2, so the noise variance absorbs the omitted signal as predicted (E7).
   - Hidden-column tests need refits, which have not been run and require HQ approval.
5. **Weaker forms.**
   - **TM-a0** (one fixed law, fixed number of candidates, second moments for density consistency, plus a mixed second moment of the scores for *exact* support selection, almost sure) is the literal SL Thm 4 counterpart and is stronger than SL Cor 2. It lies outside A-GL.
   - Independent non-Gaussian residual: remark (i′), a suggested sufficient cap and budget.
   - Heteroscedastic residual: remark (ii), a heuristic budget and the Grünwald–van Ommen link.
6. **Referee: "This isn't real misspecification."** Answer:
   - TM-a0 covers arbitrary second-moment misspecification at fixed dimension, which is SL's own setting.
   - In high dimension we target the independent-Gaussian-residual case, and our heuristic remark (ii) suggests heteroscedastic misspecification can break selection once p exceeds about n^{1/(2(ϱ̄−1))}. This matches Grünwald & van Ommen's empirical finding that the general theorems (Kleijn–van der Vaart 2006, De Blasi–Walker 2013) need a fixed model class (GvO arXiv v3 pp. 46–47; PN D10–D12).

## A-MOM: moments for TM-a0
1. **Assumed.** One fixed i.i.d. law along a nested sample sequence; fixed number of candidates; raw units with an intercept, Z = (1, x_Cᵀ)ᵀ; E‖x_C‖² < ∞, E y² < ∞, σ_C² > 0; Σ_CC nonsingular; positive prior on every submodel. For exact selection, also E[Z_j²u²] < ∞ (a mixed second moment of the scores, not fourth moments of x and y).
2. **Why needed.** The strong law makes each model's residual variance converge, and the law of the iterated logarithm, ‖Σ_i Z_i u_i‖ = O_a.s.(√(n log log n)), controls spurious gains (O(log log n) against the (m/2) log n penalty). An n-dependent truth is excluded: with β_n = 1/n even fixed-p support selection fails.
3. **Standard?** It is SL Condition 4 (p. 957), and SL's proof relies on "a fixed number of possible models" (SLs p. 7).
4. **Holds on our data?** Trivially, since all rows are Gaussian.
5–6. This is SL's own setting. The improvement is exact selection instead of inclusion.

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
  - One correction to our own earlier note (TH_PREP §3): BB(1, p^u) with u < 1 does not cause a price deficit. It loses the 2^{−k} size tail, so a size cap would be needed. Both advisors found this independently; Astra R2 confirms it for fixed small k.

## Known weak points (stated before the owner finds them)
1. **TD′** (beyond p ≤ n^A) is a conjecture with **high proof risk**: Astra R2 showed Fable's route fails at the testing step. Nothing is released beyond p ≤ n^A.
2. **TS-a** is not a boundary-signal result (inexplicit constant).
3. **TS-b\*** relies on a conjectured "separated proxies imply a joint proxy" lemma.
4. **Evidence on S1** brackets the transition with only two informative SNR levels. SNR 1.25 and 1.5 cells would locate it, but they need fits and HQ approval.
5. **TS-b proof obligations** (Astra R2): a uniform summation over m ≤ J of the superset/mixed classes; A-NEC necessity is unproved.
6. **Literature.** The Chen & Chen (2008) primary text is unverified (paywalled; attested second-hand via Luo & Chen p. 7 and SBJ p. 14). Grünwald–van Ommen are verified on the 2014 arXiv text, not the Bayesian Analysis 2017 pagination.
