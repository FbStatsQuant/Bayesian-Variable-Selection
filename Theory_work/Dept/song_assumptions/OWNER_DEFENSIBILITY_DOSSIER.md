# OWNER DEFENSIBILITY DOSSIER: assumption-by-assumption Q&A

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v1 (pre-council).**

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
| A-DIM | TD, TS, TM | yes (SBJ p. 14, JR12, SL Cor S1) | A ≤ 1.77 | A-DIM′ (TD′, conjecture) |
| A-SUBG | all | yes (SL Cond. 1, RZ, NH14 L6.1) | Gaussian rows | moments-only in TM-a0 |
| A-NEC | all | weaker than SBJ, NH14, BRT09, SL (26) | margin 8.8–250× | drop it, at a √log p cost (prop:dist(ii)) |
| A-BS / BS′ | all | yes (YWJ (7a), SC11 2.7) | ≤ 1.17σ | aggregate energy (BS′) |
| A-MARGIN-H | TS-a | SL Cond. 3 + Thm 3 proof | ≥ 1 in only 9/136 | not needed for the sharp claim |
| A-MARGIN-U | TS-b, TM-b | NH14 4.4 (stronger), Luo–Chen | S1 brackets κ = 1 | constant 2 is sharp (converse) |
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
   - Non-Gaussian independent errors are remark (i′). They need an extra size cap K_n ≤ c·n log n/(log p)² and a variance-proxy budget, because the Fubini size tail fails under misspecification.
   - Heteroscedastic errors are remark (ii). Selection survives only if (ϱ̄ − 1)·log p < ½ log n.
6. **Referee: "Gaussian noise is unrealistic."** Answer:
   - It is the model the method's likelihood assumes, and SL make the same assumption.
   - The misspecification tier (TM) says what happens when the fitted model is wrong.
   - Remarks (i′) and (ii) say precisely where non-Gaussian and heteroscedastic noise begin to bite. This is the Grünwald–van Ommen mechanism, and their examples are heteroscedastic "in-liers" (arXiv v3 pp. 4–5; PN D12).

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
   - The delivered `rem:sharp` already shows π(S0|y) → 1 is impossible unless s0 = o(√n), whatever the proof. The restriction is intrinsic, not an artefact of the proof.
   - Approximate sparsity in the style of SL (3) is the optional corollary TD-A.
6. **Referee: "Fixed s is restrictive."** Answer: it is standard (SL, NH14). Growth rates are stated in a remark, and `rem:sharp` shows that s0 cannot grow faster than √n for this conclusion with *any* proof.

## A-DIM: p ≤ n^A (released statements)
1. **Assumed.** 2 ≤ p ≤ n^A for a fixed A ≥ 1.
2. **Why needed.**
   - Union bounds over model sets of size up to the window q_n ≍ log n stay polynomial.
   - The number j0 of added nulls that a margin must control stays fixed. Rivals with more nulls are beaten without any signal condition.
3. **Standard?**
   - SBJ p. 14: results "continue to hold when p grows polynomially" (P17 B2).
   - Johnson & Rossell (2012) Thm 1, p. 651, require p ≤ n (PN E16).
   - SL's own MAP corollary (Cor S1, SLs p. 16) is quasi-polynomial, P_n < n^{κ log n} with κ < ¼ (page image checked).
4. **Holds on our data?**
   - A = log p/log n is 0.90–1.37 on S1 and 1.50–1.77 on S2.
   - The typical user regimes we tabulated (from n = 100, p = 10³ to n = 10⁴, p = 5·10⁵) have A ≤ 1.77, so p ≤ n² everywhere (E6).
5. **Weaker forms.**
   - **A-DIM′**: s·M·log p·log(p∨n) ≤ c·n, i.e. (log p)² = o(n). This is conjectured for TD (TD′).
     - Route: the Fubini size tail bounds model sizes for any p, and A-DIM′ is what sample control on those sizes costs.
     - It covers SL Cor S1's range and SL Cor 1 for α < ½.
   - **log p = o(n)** would need a model-size cap K_n ≤ c·n/log p (NH14 uses p ∧ n/((2+ν) log p), pp. 10–11). That is an Engineering decision, because the code uses K = n/2.
6. **Referee: "SL handle exponential p; you don't."** Answer:
   - SL's exponential range (Cor 1) comes from their model-size cap r̄_n. We state exactly which cap would give us the same range (A-DIM″).
   - Without a cap, our TD′ conjecture reaches p = exp(o(√n)).
   - SL's own *selection* result (Cor S1) is only quasi-polynomial.

## A-SUBG: sub-Gaussian predictors on sparse directions
1. **Assumed.** For all u with at most q_n nonzero entries, E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2). The scale is the direction's own variance, so this is relative and allows correlated designs.
2. **Why needed.**
   - (i) A lower sparse isometry: the sample residual signal R̂(S) is within (1 ± δ) of the population R_n(S) on small sets. This is how population margins transfer to the data.
   - (ii) A Hellinger lower bound d_H² ≥ c·min{1, R/(nσ²)} for any model that misses signal R. Because this follows from A-SUBG, SL's Condition 3 is not needed as a separate assumption.
3. **Standard?** SL Condition 1, p. 953 (exponential moments on sparse directions); RZ Def. 1.5/Thm 1.6, pp. 5–6; NH14 Lemma 6.1, p. 16 (P17 B7b).
4. **Holds on our data?** S1/S2 rows are Gaussian AR(1), so it holds with L = 1.
5. **Weaker forms.**
   - Second moments only (SL Condition 2) is adopted in fixed dimension as TM-a0.
   - In growing dimension the exact-marginal route needs exponential tails, so we do not claim it there.
6. **Referee: "Binary or heavy-tailed predictors?"** Answer:
   - A rare binary predictor is not sub-Gaussian at its own scale (P17 B7b note), so this is a real limitation, and it is stated.
   - Bounded predictors with variance bounded below are covered.

## A-NEC: no near-exact collinearity (a vanishing floor)
1. **Assumed.** The smallest eigenvalue of the population correlation matrix of every set of at most q_n predictors is ≥ c_ψ/n. This floor tends to zero.
2. **Why needed.** For one step only: adding a null predictor must cost the full Occam factor (n+1)^{−1/2}. A null nearly collinear with the current model would pay almost nothing, and supersets would keep posterior mass.
   - Deleting true predictors needs **no** floor, because the Occam refund is ≤ (n+1)^{d/2} for any design (Cauchy interlacing).
3. **Standard?** It is *weaker* than every verified precedent:
   - SBJ Assumption 4 (ν ≻ τ/n), p. 14;
   - NH14 Cond. 4.5, pp. 11, 17;
   - BRT09 Assumption 2, p. 9 (c/log n);
   - MY09 "slowly vanishing" (P17 B6);
   - SL's (26), SLs p. 15, which is a fixed-type sample floor that SL themselves introduce because their (22) "is hardly satisfied" (SLs p. 15).
4. **Holds on our data?**
   - Population floors are (1−ρ)/(1+ρ) = 0.176–1, i.e. 8.8–250 times c_ψ/n (E5).
   - Sample sparse floors at the delivered fixed-design set sizes are vacuous on S2 (1e−5 to 2e−4). This is why we **dropped every sample floor and every fixed floor**.
5. **Weaker forms.** Drop A-NEC entirely. The delivered prop:dist(ii) still gives TD, with one extra √log(p∨n) factor in the radius.
6. **Referee: "Eigenvalue conditions are uncheckable."** Answer:
   - Ours is a population condition with a floor that tends to zero.
   - It fails only for exact or near-exact duplicates and linear dependences (one-hot coding, compositions), which users remove anyway.

## A-BS / A-BS′: bounded signal
1. **Assumed.**
   - A-BS (TD, as delivered): |β*_j|·sd(x_j) ≤ b̄σ*.
   - A-BS′ (new TS-b/TM-b statements): β*ᵀΣβ* ≤ M_μσ*² and max_j |β*_j|sd(x_j) ≤ b̄_nσ* with s·b̄_n² = o(n).
2. **Why needed.**
   - It gives a lower bound on the true model's marginal likelihood relative to the truth, which is the denominator of the Fubini size bound.
   - It keeps the estimated noise variance in a fixed range.
   - It controls the unit-ridge shrinkage term.
3. **Standard?** YWJ (7a), p. 7: "some form of upper bound on the norm ‖β*‖₂ … is required" (P17 B4b); SC11 Assumption 2.7, p. 7.
4. **Holds on our data?** Max |β|sd/σ ≤ 1.17 and βᵀΣβ/σ² ≤ 6 in every setting (E4).
5. **Weaker forms.** A-BS′ is the aggregate form. TD keeps A-BS so that the proved and checked prop:dist need not be re-issued.
6. **Referee: "Why bound signals from above at all?"** Answer:
   - It is a technical device for the Fubini denominator and the ridge term, and YWJ need the same.
   - A very large single coefficient is easy to *select* but makes the prior-mass bound loose.
   - We flag for proof audit that nothing else uses it.

## A-MARGIN-H: Hellinger-scale residual signal (TS-a, sure screening)
1. **Assumed.** For each true j, every model of size ≤ q_n that omits j leaves residual signal R_n(S) ≥ C_H·M·σ*²·log(p∨n). Here R_n(S) is n times the linear-projection risk of the true signal on x_S.
2. **Why needed.** Every such model's predictive law is then farther than the TD radius from the truth, so TD contraction forces j into the model.
3. **Standard?** It is exactly the SL Theorem 3 route.
   - SL Condition 3, p. 955.
   - SL's proof (SLs pp. 5–6) gives d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}.
   - The same residual-signal object appears in NH14 Cond. 4.4, p. 11, and Luo & Chen, arXiv v1 p. 7.
4. **Holds on our data?** Only partly, and we say so.
   - The per-variable screening margin divided by ε_n² is ≥ 1 in only 9 of 136 settings, yet S1 at SNR 2 recovers 92–96% with a ratio of 0.75 (E2).
   - TS-a has an inexplicit constant by construction, so it is **not** claimed at boundary signal levels.
5. **Weaker forms.** None is needed. The sharp, data-relevant claim is carried by TS-b.
6. **Referee: "Your sure-screening constant is unknown."** Answer: so is SL's (c₁). TS-a is the per-predictor counterpart of SL Thm 3, and the explicit threshold is in TS-b.

## A-MARGIN-U: the identifiability margin for exact selection (TS-b, TM-b) — the central assumption
1. **Assumed.**
   - Exact form, for every rival S that misses d ≥ 1 true predictors and adds m ≤ j0 nulls:
     √R_n(S)/σ* ≥ (1+η)[w_m + √(2[Pr_n(d) − (m/2)log(n/(C log p)) + γ log n]₊)] + a_n.
   - Plain form: dropping true predictors must leave more unexplained signal than **twice** the prior-plus-Occam price of those predictors, with a little room. When nulls are added in their place, there is an extra allowance w_m ≈ √(2m log p) for the best-looking nulls among the p candidates.
   - For pure deletions the condition is liminf κ_n > 1, where κ_n = min_D R_n(S0∖D)/(2σ²Pr_n(d)).
   - Simple sufficient form: R_n(S) ≥ 2(1+η)²(√d+√m)²·σ²·price, with price ≈ log(2p/s0) + ½ log n.
2. **Why needed.** The posterior odds of a rival against S0 are exp{Pr_n − ½·(gain in fit)}, and the gain in fit is (√R + noise)².
   - If R is below 2·Pr, the rival wins. That is the **converse**: if limsup κ_n < 1, then π(S0|y) → 0.
   - The constant 2 is therefore not a proof artefact. It is the exact threshold.
3. **Standard?** Yes in type, and ours is weaker in two ways.
   - **NH14 Cond. 4.4**, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n) for every model of size < K|t| that misses a true predictor (PN A2).
     - NH14 multiply by |t| even when one predictor is missed; ours is per missed predictor.
     - NH14's constant is 5(1+δ); ours is 2(1+η).
   - **Luo & Chen** (EBIC consistency condition, arXiv v1 p. 7): Δ_n(s)/(p₀ ln p) → ∞, which they describe as a variant of Chen & Chen (2008)'s condition (PN A4). That is a diverging ratio; ours is a fixed ratio above 1.
   - Per-coefficient beta-min versions: YWJ (8), p. 9, C_β² ≥ c₀(L + L̃ + α + κ)σ²log p/n with unspecified c₀ (P17); Fan & Lv Cond. 3, p. 25 (PN E15).
   - **Necessity of the log p order for any method:**
     - Wainwright (2009) Thm 2, arXiv v2 p. 4: Gaussian design, averaged over random supports, unspecified C′ (PN B5).
     - Fletcher, Rangan & Goyal (2009) Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor. This constant is C2's derivation from their display (6) (PN B6).
   - **SL themselves state no margin.** Their MAP proof treats min|β_t| as a fixed constant (SLs p. 15) and needs the "hardly satisfied" sample condition (22).
4. **Holds on our data?** This is the strongest evidence in the package.
   - **S1 brackets κ = 1 from both sides.** κ is 0.64–0.70 at SNR 1, with 0 of 100 exact in every (n, p) cell, and 2.54–2.80 at SNR 2, with 92–96 of 100 exact (E1).
   - **The necessary direction is exact in the data.** min t² > 2·price has sensitivity 1.000 on S1, and on S2 it is 1.000 in population and 0.985 in sample. Recovery when it fails is 0 on S1 and 9 of 11,466 fits on S2.
   - **Multi-predictor deletions bind on S1** in all 16 settings, which is why the margin quantifies over all subsets D.
   - **The sufficiency gap is explained.**
     - At SNR ≥ 2, 40 of the 41 S1 failures are "S0 plus a null". The one-null superset term predicts a ceiling of 0.94–0.97 for S1's (n, p), against 0.92–0.98 observed.
     - This is the (s0+1)√(log p/n) term in TS-b's rate, which `rem:sharp` shows cannot be removed. It is not a missing assumption.
   - **S2 is not an asymptotic regime** (s0 log p/n = 0.69). The finite-n companion uses the saturating gain, which puts the transition at κ ≈ 1.0–1.5 on both suites (post hoc, flagged).
5. **Weaker forms evaluated.**
   - (i) The old explicit constant c1(s0, A): replaced, since it is far above the S1 transition.
   - (ii) A fixed beta-min (FSb): it is false along S1, where β ∝ √(log p/n), so it was replaced by the fixed-ratio κ_n.
   - (iii) The memo's uniform "constant 2 for every rival": rejected. Fable built a counterexample with nulls that jointly imitate a true predictor when log n = o(log p). It remains open under p ≤ n^A.
   - (iv) Λ → ∞ with an m·log p multiplicity charge: neither sufficient nor necessary, and it ranks worse on the data (AUC 0.967 vs 0.980).
   - (v) TS-b\*, a sharper constant 2 + η for swaps under a "bounded leakage" condition, is a medium-risk refinement.
6. **Referees.**
   - **"Your condition is uncheckable."** Answer: R_n(S) is a population projection residual, the same object as NH14's Δ_n and Rossell's non-centrality λ_tm (arXiv v7 p. 10). For any assumed Σ and β it is computable in closed form, as D1 did for all 136 settings. We also give worked cases: orthogonal, AR(1), block, equicorrelated.
   - **"Why √(2m log p) for swaps?"** Answer: it is attained. In a factor-proxy design a single swap beats S0 unless R ≥ 2(1+ρ)²log p (Fable, numerical check). No design-free condition can avoid it.

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
   - **TM-a0** (fixed number of candidates, second moments only, almost sure, with *exact* support selection) is the literal SL Thm 4 counterpart and is stronger than SL Cor 2.
   - Independent non-Gaussian residual: remark (i′), needs a cap.
   - Heteroscedastic residual: remark (ii), with a counter-calculation and the Grünwald–van Ommen link.
6. **Referee: "This isn't real misspecification."** Answer:
   - TM-a0 covers arbitrary second-moment misspecification at fixed dimension, which is SL's own setting.
   - In high dimension we prove what is provable, and our remark (ii) shows heteroscedastic misspecification can genuinely break selection once p exceeds n^{1/(2(ϱ̄−1))}. This matches Grünwald & van Ommen's empirical finding that the general theorems (Kleijn–van der Vaart 2006, De Blasi–Walker 2013) need a fixed model class (GvO arXiv v3 pp. 46–47; PN D10–D12).

## A-MOM: moments for TM-a0
1. **Assumed.** Fixed number of candidates; E‖x_C‖² < ∞ and E y² < ∞; Σ_CC nonsingular; positive prior on every submodel. For exact selection, also E[x_j²u²] < ∞.
2. **Why needed.** The strong law makes each model's residual variance converge, and the law of the iterated logarithm controls spurious gains (O(log log n) against the (m/2) log n penalty).
3. **Standard?** It is SL Condition 4 (p. 957), and SL's proof relies on "a fixed number of possible models" (SLs p. 7).
4. **Holds on our data?** Trivially, since all rows are Gaussian.
5–6. This is SL's own setting. The improvement is exact selection instead of inclusion.

---

## Questions about what we *removed* or *did not assume*
- **"Where is the eigenvalue floor on the true model?"** Not needed. R_n(S0∖{j}) = n β_j² Var(x_j | rest) already enters the margin, so a fixed floor would only add a stronger condition (Astra and Fable, independently).
- **"Where is SL's identifiability Condition 3?"** It is implied by sub-Gaussian rows (d_H² ≥ c·min{1, R/(nσ²)}). In Gaussian AR(1) it holds with δ_SL = 0.23–0.42, but SL's requirement ε_n² = o(δ_SL) fails numerically on S2 (E3).
- **"Why no sample sparse eigenvalue condition, as in Thm S?"** On S2 it is vacuous (1e−5). SL themselves call theirs "hardly satisfied" and replace it with a random-design version (SLs pp. 15–16).
- **"SL's Theorem S / Cor S1: do we dominate them?"**
  - Our conclusion is stronger: π(S0|y) → 1 with a rate, versus pairwise MAP odds.
  - Our conditions are weaker: a population vanishing floor versus a sample floor, and an explicit margin versus an implicit fixed beta-min.
  - Audit flags on SL, which we report but do not use:
    - their proof bounds a max where a min is needed;
    - Cor S1's endpoint does not follow from Thm S's printed √(log P_n) condition;
    - the ridge "Lemma A.2" is absent from the supplement.
- **"Does changing g or the size prior break anything?"**
  - The form of every statement is invariant; only the price in the margin moves.
  - One correction to our own earlier note (TH_PREP §3): BB(1, p^u) with u < 1 does not cause a price deficit. It loses the 2^{−k} size tail, so a size cap would be needed. Both advisors found this independently.

## Known weak points (stated before the owner finds them)
1. **TD′** (beyond p ≤ n^A) is a conjecture. One advisor gives a route; the other wants the size-tail budget written out (Astra round 2 is pending).
2. **TS-a** is not a boundary-signal result (inexplicit constant).
3. **TS-b\*** relies on a conjectured "separated proxies imply a joint proxy" lemma.
4. **Evidence on S1** brackets the transition with only two informative SNR levels. SNR 1.25 and 1.5 cells would locate it, but they need fits and HQ approval.
5. **Literature.** The Chen & Chen (2008) primary text is unverified (paywalled; attested second-hand via Luo & Chen p. 7 and SBJ p. 14). Grünwald–van Ommen are verified on the 2014 arXiv text, not the Bayesian Analysis 2017 pagination.
