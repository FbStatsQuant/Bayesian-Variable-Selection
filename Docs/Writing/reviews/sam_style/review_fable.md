# SAM_STYLE (B): review of the assumptions A1–A10 and C1–C3

Reviewer: Fable (independent). 2026-11-25. Read-only review; nothing committed.

**What was read.**
- Ours: `short/smc_bvs_short.tex` (section "The assumptions" and the theorems), checked against `spec/sections/sp5_assumptions.tex`.
- Song and Liang (2015), "SAM": main paper pp. 949–960, 962, 964; supplement pp. 5–6 and 13–17. Page numbers below are journal pages; "supp. p." is a page of the supplement PDF.
- Earlier comparison: `sections/appendix_sl_or.tex`, `sections/or5_assumptions.tex`, `sections/s5_assumptions.tex`.
- Designs: BENCH_DESIGN `REPORT.md` §6.1, `CITE_CHECK.md`, `shared/sim_designs_cite.tex`, HQ_DECISIONS entry of 11-24.

**How to read the S1/S2/S3 lines.**
- The assumptions are statements about a sequence in n. "Holds" means: the design, continued in n with its structure fixed, satisfies it.
- Where the assumption contains explicit numbers that our actual n, p, s0 violate, I say so separately ("at our n").
- Numbers marked [calc] are my own computations for this review, not taken from a source.

**Short text against sp5 (sp5 wins).** The statements agree. Two small differences:
- The short text's C2 contains C1 and the lifted integer limits. sp5 keeps three conventions: C1, C2 and C2′ (key C2p). Theorem 3 uses all three.
- sp5 has a numbered assumption WIT (witness designs) for Theorem 6(b). The short text states it inside the theorem and gives it no number.

**Label clash.** In `or5_assumptions.tex` and `s5_assumptions.tex`, "S1–S6" are the old designs (independent, blocks, factor). They are not the S1–S3 fixed on 11-24. The "Reasonable?" column of the short table still describes the old suite.

---

## A1. Gaussian linear model (GL). Feeds Theorems 1, 4, 6(b).

- **Origin.** SAM. Their model (1), p. 947, and density (2), p. 950. Ours is the same. We add an intercept and say that the noise variance is fixed; they leave that implicit.
- **Pushback.** Low. It is the working model of the whole literature. A referee may ask what happens with non-Gaussian errors; the planned "wrong model" result is the answer.
- **S1.** Holds. Gaussian noise, σ = 1.
- **S2.** Holds. σ² = β0ᵀΣβ0/ν changes from cell to cell but is fixed inside a cell.
- **S3.** Plausibly holds. The sources do not state σ for S3.

## A2. Dimension, p ≤ n^A (DIM). Feeds Theorems 1, 3 (and 2 through A7(b)).

- **Origin.** Not SAM. SAM asks P_n ≻ n^θ (p. 950) and allows P_n < exp(Cn^α) for the density rate (Corollary 1, p. 954). For selection (their Theorem S) they need log(√n/r_n) ≻ √(log P_n) (supp. p. 13), and Corollary S1 states P_n < n^{κ log n} with κ < 1/4 (supp. p. 16). Polynomial p is the assumption of Bühlmann, Kalisch and Maathuis (2010), (D2): p_n = O(n^a) (arXiv v3, p. 8). Ours is not comparable with SAM: narrower at the top, wider at the bottom (we allow bounded p). Against Theorem S, the SAM result that matches our Theorem 1, the gap at the top is small.
- **Pushback.** Low. A referee may ask for log p = o(n), which several papers allow. The answer is that A may be any fixed number.
- **S1.** Holds. A = 1 at p = 500; A = 1.37 at (n, p) = (500, 5000); A = 1.23 at (1000, 5000). [calc]
- **S2.** Holds. A = 1.77 at n = 50; A = 1.5 at n = 100. [calc]
- **S3.** Holds. Same sizes as S1.
- **Note.** A enters the set size 5(A+1)(s0+1) log n of A4 and A6. That size is 684–848 in S1 and S3, and 325 and 633 in S2. It is larger than p when p = 500, and larger than n in S2. So in our designs A4 and A6 are in effect conditions on the whole of Σ. [calc]

## A3. Fixed true model size (SP). Feeds Theorems 1, 6(b).

- **Origin.** SAM. Their strict sparsity (4), p. 950, used by their Theorem 2 (p. 953), Corollary 1 (p. 954), Theorem 3 (p. 956) and Theorem S (supp. p. 13). Ours is the same. Their Theorem 1 allows the weaker condition (3), p. 950.
- **Pushback.** Low to medium. It is usual for exact selection. A referee who knows Yang, Wainwright and Jordan (2016) or Castillo et al. (2015) will note that they let s0 grow. Theorem 6(a) is our answer.
- **S1.** Holds, s0 = 10. By Theorem 6(a) the posterior mass of the true model is at most 0.86 (n = 500) and 0.90 (n = 1000), whatever the signal. [calc]
- **S2.** Holds in the letter, s = 5 and 10. But s0 is not small against n: n/s0 = 10 in both cells. The ceiling of Theorem 6(a) is 0.78 (n = 50) and 0.73 (n = 100). The rate √(log n/n) is 0.28 and 0.21. The limit statements of Theorem 1 say little at these sizes. [calc]
- **S3.** Holds, s0 = 5 or 10. Ceilings 0.92–0.94 (s0 = 5) and 0.86–0.90 (s0 = 10). [calc]

## A4. Law of the rows (SGR, GR). (a) feeds Theorem 1; (b) feeds Theorem 3.

- **Origin.** Not SAM. SAM's Condition 1 (p. 953) bounds E exp{(Σ a_i x_{j_i}/r)²} for r ≤ r̄_n. They also give a weaker Condition 2 (p. 954, second moments only), under which their Theorems 2 and 3 hold in probability (their (16)). Our (a) is the sub-Gaussian row condition of the random-design literature. For centred predictors with unit variance, (a) implies Condition 1 when r̄_n is at most our set size; I rechecked the computation (δ = √(3/8)/L, M = log 2). So (a) is stronger than Condition 1 there, and much stronger than Condition 2. Our (b), exactly Gaussian rows, is stronger than anything SAM assumes: Gaussian rows are only an example for them (pp. 953, 955–956). Bühlmann et al. (2010) assume multivariate normality in (D1) (arXiv v3, p. 8).
- **Pushback.** (a) low. (b) medium to high. Theorem 3 excludes genotypes and all bounded or binary data, which is where the method is aimed. SAM does not need Gaussian rows. A referee will ask whether Gaussianity is needed or is a device of the proof.
- **S1.** Holds, (a) and (b). Rows are N(0, Σ) with unit variances.
- **S2.** Holds, (a) and (b). Same.
- **S3.** Holds, (a) and (b). Same.
- **Gap in the short text.** Its list of SAM conditions omits Condition 2.

## A5. Fixed signals (FSb raw scale, FSt standardised scale). (a) feeds Theorem 1; (b) feeds Theorem 3.

- **Origin.** SAM states no lower bound, but their proofs use fixed nonzero coefficients. Proof of their Theorem 3 (supp. pp. 5–6): the bound is min{δ_n, β_t*²δ_n/(20σ*²), 1−√0.8}, and the conclusion uses only δ_n ≻ ε_n². Proof of Theorem S (supp. p. 15): c = min |β_i*| enters as a constant. So (a) is the same as SAM in substance, and ours is explicit. Outside SAM the usual condition is weaker: a lower bound that shrinks with n. Fan and Lv (2008), Condition 3: min |β_i| ≥ c2 n^{−κ} (arXiv v2, p. 25). Bühlmann et al. (2010) describe their (D4) as "slightly stronger" than a "detectability-threshold" on the coefficients (arXiv v3, p. 10). Against that standard ours is stronger. Form (b), coefficients fixed on the sample-standardised scale, is ours alone: it makes the response depend on the sample means and standard deviations.
- **Pushback.** (a) medium. A referee will ask for a lower bound of order σ√(log p/n). We have one in the supplement (BM), but its constant is large: C_β·φ0 > 30 for s0 = 10 and A = 1.37 [calc from Definition "Explicit constants"]. (b) high. No data set is generated that way, and the short text itself says that no design satisfies both (a) and (b) (planned result 3).
- **S1.** (a) fails, by construction. β* = SNR·√(log p/n)·(±2, ±3), so the smallest coefficient is 2·SNR·√(log p/n): from 0.08 to 0.78 over the cells, and it shrinks with n. [calc] This is the short text's own example of failure. Its sentence "It holds when the effects are fixed numbers, as in our simulations" is no longer true. The supplement's beta-min theorem has the right form for S1, but S1's constant is C_β = 2·SNR·√(log p/log n) ≤ 7, well below 30. By my rough count the weakest true predictors gain about 0.9·SNR²·log p in log marginal likelihood, against a price of about log p + ½ log n. So SNR 0.5 and 1 are below the selection boundary and SNR 2 and 3 are above it. [calc, not from a source] (b) fails for the same reason.
- **S2.** (a) holds in the letter: coefficients are 1 (types 1, 2) or between 0.5 and 10 (type 3), and σ is fixed in each cell. In noise units most cells are weak. For the weakest true predictor, n·β²·Var(x_j given the other true ones)/σ² runs from 0.5 to 60 over the ν grid for type 1; from 0.1 to 6.7 for type 2 at ρ = 0.7; and stays below 0.4 for type 3. Compare 2 log p = 13.8. Only type 1 (and type 2 at ρ = 0) with ν ≥ 2 is in the regime Theorem 1 describes. [calc] (b) fails in the letter (see S3).
- **S3.** (a) not checkable: the sources fix ρ, s0, n and p for S3 but not β* or σ. It holds if the coefficients are fixed numbers and fails if S1's scaling is reused. (b) fails in the letter in all three designs: the simulations draw y from fixed raw coefficients and random Gaussian rows, so θ*_j = β*_j × (sample s.d.) is random, not deterministic. The gap is of relative order n^{−1/2}. I assumed raw-scale generation; I did not read the simulation code.

## A6. Eigenvalue floor (EFS). Feeds Theorems 1, 3.

- **Origin.** Not SAM. It is a sparse-eigenvalue condition of the kind used for the Lasso and in Bayesian selection papers (the precedents listed in `s5_assumptions.tex`; not rechecked). SAM has two counterparts. (i) Condition 3, p. 955, for their Theorem 3: no combination of r̄_n other predictors mimics x_k, with a gap δ_n ≻ ε_n² that may vanish; for Gaussian predictors λ_min(var x) ≻ ε_n² is enough (pp. 955–956). (ii) For Theorem S, (22)–(23), supp. p. 13: lower and upper bounds on the realised Gram matrix on sets of size min(|t| + r̄_n, n), relaxed to (26), supp. p. 15; Corollary S1 allows the floor to vanish like log^{k2}(n)/√n (supp. p. 16). Ours asks a fixed floor (stronger), no ceiling (weaker), on sets of another size. Stronger than Condition 3 when our sets cover theirs; not comparable with (22)/(26).
- **Pushback.** Low. A fixed floor on the population matrix, with no ceiling, is mild.
- **S1.** Holds. λ_min(Σ) ≥ (1−0.6)/(1+0.6) = 0.25 for every p. [calc]
- **S2.** Holds. Floors 1, 0.48 and 0.18 for ρ = 0, 0.35, 0.7. [calc]
- **S3.** Holds. λ_min(Σ) = 1−ρ: 0.5 and 0.2. Equicorrelation 0.8 does not break the floor. It breaks A9.
- **Gap in the short text.** Its SAM list omits Theorem S and (22)–(23). Theorem S (MAP model = true model) is the SAM result that matches our Theorem 1, so A6 and A2 should be compared with it, as `appendix_sl_or.tex` does. I checked that appendix against the PDF: its pages and statements for (22)–(23), (26), Corollary S1 and Condition 3 are correct.

## A7. The weaker setting of Theorem 2 (dist). Feeds Theorem 2.

- **Origin.** SAM, and through SAM Jiang (2007): "The theory development and conditions in this subsection follow Jiang (2007) very closely" (p. 950). Our Theorem 2 has the same form as their (15), p. 952: with ε_n² = M log n/n, their exp(−c1·n·ε_n²) is our n^{−cM}. Item by item: (a) their model, with parameters allowed to change with n; (b) their (4) with polynomial p, and s = 0 allowed; (c) compares as A4(a); (d) the floor c_ψ/n has no counterpart under their ridge prior; (e) compares with their (3), p. 950, and (8), p. 952. Their rate must satisfy n·ε_n² ≻ r̄_n log P_n ((10), p. 952); ours is √(M log n/n), paid for by (d) and polynomial p. Overall about the same strength; not comparable in the strict sense.
- **Pushback.** Low. Likely question: the values of M0, n0 and c_H, and whether the bound says anything at n = 50.
- **S1.** Holds, at all four SNR: shrinking coefficients are allowed, rows are Gaussian, the floor is 0.25, and |β_j|/σ ≤ 1.2. Theorem 2 is the one theorem that covers S1 as designed.
- **S2.** Holds. At our n the conclusion is weak: it needs √n/log n ≥ M ≥ M0, and √n/log n is 1.8 (n = 50) and 2.2 (n = 100); the radius √(M log n/n) is at least 0.28 and 0.21, on a distance that is at most 1. Whether n ≥ n0 is not checkable: M0 and n0 have no numerical value in the text. [calc]
- **S3.** Plausibly holds (floor 0.2; β* and σ not stated).
- **Error in the short table.** The A7 row says SAM's density results assume "nothing about collinearity". That is true only for their ridge prior (p. 953). Their conditions (11) and (14), p. 952, bound eigenvalues of the prior covariance, and for a g-type prior these are eigenvalues of the design covariance (B̃_n, B(r_n), pp. 952–953).
- **Small point.** SAM's Hellinger distance is d² = ∫∫(√f1 − √f2)² (p. 952); ours is d² = 1 − ∫√(f f*). They differ by a factor 2 in d².

## A8. Visibility (V). Feeds Theorem 3.

- **Origin.** Not SAM, but not without precedent. SAM's Condition 5, p. 958, is the marginal case with no margin, and it serves their screening step, not a numbered theorem. The condition is a form of *partial faithfulness with a margin*: Bühlmann, Kalisch and Maathuis (2010), Definition 1 and assumption (D4): the partial correlations ρ(Y, X_j | X_S), when nonzero, are at least c_n for all |S| ≤ s0, with c_n^{−1} = O(n^d) (arXiv 0906.3204v3, pp. 3, 8). Marginal form: Fan and Lv (2008), Condition 3, min |cov(β_i^{−1}Y, X_i)| ≥ c3 (arXiv math/0612857v2, p. 25). Conditional form: Barut, Fan and Verhasselt (2016), Condition 1(i), |Cov_L(Y, X_j | X_C)| ≥ c1 n^{−κ} for one given set C (arXiv 1206.1024v2, p. 17). Ours is stronger than SAM's Condition 5 and than Barut et al. (every set of up to 15, fixed margin). Against (D4) it is not comparable: our margin is fixed (stronger), our sets stop at 15 (weaker when s0 > 15).
- **Pushback.** High. Bühlmann et al. say of their own version that it is "restrictive" (arXiv v3, p. 10) and that their assumptions are "virtually impossible to check ... in practice" (p. 8). Ours adds a fixed margin, and the number 15 comes from the code (blocks of 16). It fails by cancellation, which is common with correlated predictors and mixed signs.
- **Correction for Writing.** `s5_assumptions.tex` says "Precedents: None found". The three papers above are precedents. None is in `refs.bib`.
- **S1.** Fails in practice. Write θ* = t·c with c = (2,−3,2,2,−3,3,−2,3,−2,3) and t = SNR·√(log p/n). The smallest value of |Cov(W_j, Wᵀθ* | W_U)| is 0.005·t (j = 5, U = {1, 11}). Others: 0.07·t (j = 7, U = {4, 10}), 0.13·t (j = 9, U = {8}), 0.16·t (j = 2, U empty). Predictor 5 has coefficient −3t and marginal covariance +0.23·t with the signal: the wrong sign. [calc: AR(1) is Markov, so only the nearest member of U on each side matters; I enumerated all such pairs and confirmed with a random search over U.] A margin a > 0 exists for one fixed cell, but it is 0.2% of the coefficient and it shrinks with n. Note: the worst sets U are not blocks the method would form. In an AR design the blocks are contiguous and one block probably holds all ten true predictors. So the assumption asks far more than the method needs here. This is evidence that A8 is too strong, not that the method fails on S1.
- **S2.** Holds. All coefficients are positive and the correlation is nonnegative, so every term has the same sign: the covariance is at least θ_j(1−ρ²)/(1+ρ²), that is 1, 0.78 and 0.34 times θ_j for ρ = 0, 0.35, 0.7. [calc] At n = 50 and 100 the method's blocks have at most 7 and 10 predictors, so the 15 asks more than the method uses.
- **S3.** Depends on the signs, which the sources do not fix. Here Cov(W_j, Wᵀθ* | W_U) = (1−ρ)θ_j + c_m·Σ_{k∈S0∖U} θ_k with c_m = ρ(1−ρ)/(1+(m−1)ρ), m = |U|. With all signs equal it holds: margin 0.53·|θ_j| (ρ = 0.5) and 0.21·|θ_j| (ρ = 0.8). With mixed signs it fails or nearly fails: exactly zero at ρ = 0.5 for alternating ±1 with s0 = 5, and for S1's sign pattern; at ρ = 0.8 the minimum is 0.5% to 2% of the coefficient for the patterns I tried. [calc] Shin et al. (2018), cited for S3, use random signs.

## A9. Small leakage set (reported). Feeds Theorem 3.

- **Origin.** Ours. SAM has only an informal remark (remark (a), p. 958: "if there are p_n predictors correlated with the true predictors X_t, p_n ≺ P_n, then there are at most cp_n predictors to be selected"). It is not a condition of any of their theorems. Part (b) is a floor and compares as A6. Part (c), local regressions, has no counterpart: it serves our greedy search.
- **Pushback.** High. It is long, in three parts, and has constants a reader cannot place (15; b < 1/2; 15·b_H + b < 1/2, so b_H < 1/30). It cannot be checked on data. It excludes every design with a common factor. And it is written for the proof of our own algorithm.
- **S1.** Plausibly holds as a sequence, with Q a neighbourhood of about C log n predictors after the tenth. I did not verify part (c) in full; a sketch works because AR(1) is Markov. Not at our n: the condition K ≥ 2|Q| + 32·s0 + 1 needs K ≥ 341, and K = 250 at n = 500. Also |H_l| ≤ n^{b_H} with b_H < 1/30 gives |H_l| ≤ 1.26 at n = 1000, while H_l must contain the ten true predictors; the literal inequality needs n of about 10^31. [calc] The statement is asymptotic only.
- **S2.** As a sequence: holds at ρ = 0 (Q = S0), plausibly holds at ρ = 0.35 and 0.7. At our n it fails numerically: K = 25 against 171 needed (n = 50), K = 50 against 341 (n = 100). √n is 7.1 and 10. At n = 50, Q can hold at most two predictors beyond S0, while the leak at distance 3 is 0.7³ = 0.34, above √(log n/n) = 0.28. At n = 100 even Q = S0 has 10 = √n members, which is not below n^b for any b < 1/2. [calc] Theorem 3 says nothing at S2's sizes.
- **S3.** Fails, for both ρ. Every null predictor has covariance ρ with every true one, and still 0.031 (ρ = 0.5) or 0.013 (ρ = 0.8) after conditioning on 15 others; neither tends to zero. So Q must be all p predictors, and |Q| < √n ≤ 32 is impossible with p ≥ 500. [calc] The short text says the same about common factors.

## A10. Conditions for certified screening (SCR). Feeds Theorem 4.

- **Origin.** The package is ours; the parts are standard. (a) is a sparse-eigenvalue floor on the observed design, of the same kind as the lower half of SAM's (22), supp. p. 13 (theirs may vanish; ours is fixed; the sets differ). (b) is a lower bound and an ℓ1 bound on the coefficients; SAM uses the first implicitly (supp. p. 15) and has (3), p. 950, for the second. (c) is a sample-size condition with an explicit constant. Not comparable with SAM; of the same kind.
- **Pushback.** Medium. The form is fine. The constant is the problem: with 1/200 in c, condition (c) holds at no practical size, so a referee may call the theorem empty. The short table already admits it is conservative.
- **S1.** (c) fails by orders of magnitude. Since θ_low ≤ M1/s0, c ≤ κ²/(200·s0²). For S1, c·n ≤ 0.03, against (k_n+1) log p + log n ≥ 75 with k_n = 10. It would need n of about 3 × 10^6. [calc] (b) holds in one cell but shrinks with n. (a) not checkable without the realised designs; plausible for small k_n.
- **S2.** (c) fails: c·n is 0.010 (n = 50) and 0.005 (n = 100) against 45 and 81; it would need n of about 2 × 10^5 and 1.6 × 10^6. [calc] (a) not checkable, and doubtful at n = 50 with p = 1000.
- **S3.** (c) fails for the same reason (c ≤ κ²/5000 at s0 = 5, with κ at most about 1−ρ). (a) and (b) not checkable. Theorem 4 is the theorem meant for common-factor designs, but at S3's sizes it is empty.

## C1–C3. The idealised computer. Feed Theorems 3, 4 and Proposition 5.

- **Origin.** Not SAM, and not statistical. C3 is the usual setting for the unbiasedness of the SMC evidence estimate (Del Moral 2004, cited in SMC_LIT REPORT; not rechecked). SAM's statements about their sampler are idealised too: the estimated inclusion probabilities converge "almost surely as N → ∞" (supp. p. 13, citing Liang 2009), and Lemma S2 (supp. pp. 16–17).
- **Pushback.** None to low. Every theorem about an algorithm makes these idealisations.
- **S1, S2, S3.** Not checkable from the design; the same for all three. Exact arithmetic holds on no machine. The resource part of C2 can be checked run by run (did the run finish).

---

## Verdict

**From SAM, the same:** A1, A3. A5(a) is implicit in SAM's proofs. A7 and Theorem 2 are the SAM (Jiang 2007) density result, with a better rate and one extra mild condition.

**Standard, but not from SAM:** A2 (polynomial p), A4(a) (sub-Gaussian rows), A6 (eigenvalue floor), the parts of A10, C1–C3.

**Ours:** A5(b), A9, the constant in A10(c). A8 is ours in this form, but it is a partial-faithfulness condition and should be cited as such.

**Expected pushback:** high for A8, A9 and A5(b); medium to high for A4(b); medium for A5(a) and A10; low for the rest.

**The designs against the assumptions.**

| | S1 | S2 | S3 |
|---|---|---|---|
| A1 | holds | holds | plausibly holds |
| A2 | holds | holds | holds |
| A3 | holds | holds; s0 not small against n | holds |
| A4 (a), (b) | holds | holds | holds |
| A5(a) | **fails** (β* ∝ √(log p/n)) | holds in the letter; most cells weak | not checkable (β* not fixed) |
| A5(b) | **fails** | fails in the letter | fails in the letter |
| A6 | holds (0.25) | holds (0.18 to 1) | holds (0.5, 0.2) |
| A7 | holds | holds; weak at n = 50 | plausibly holds |
| A8 | **fails in practice** (margin 0.2% of the coefficient) | holds | holds if one sign; fails if mixed |
| A9 | as a sequence only; not at n = 500 | as a sequence only; not at n = 50, 100 | **fails** |
| A10 | (c) fails | (c) fails | (c) fails |
| C1–C3 | not checkable | not checkable | not checkable |

**The theorems against the designs.**
- **Theorem 1** (posterior concentration; A1–A6). Does not cover S1: A5(a) fails by design. Covers S2 in the letter, but only the high-ν cells are in its regime and n is 50 or 100. Covers S3 if its coefficients are fixed numbers.
- **Theorem 2** (fitted distribution; A7). Covers all three designs. It is the only one that does. Its constants M0, n0, c_H are not given, so nothing can be said about a particular n.
- **Theorem 3** (reported model; A4(b), A5(b), A6, A8, A9). Covers none of the three. S1: A5(b) and A8. S2: A5(b), and A9's numbers at n = 50 and 100. S3: A9, and A8 unless all signs agree. The old suite (blocks and AR with fixed coefficients) was inside; the suite fixed on 11-24 is not.
- **Theorem 4** (certified screening; A10). Condition (c) fails in every cell by three or more orders of magnitude. The theorem is not wrong, but it is empty at these sizes.
- **Proposition 5** (unbiased evidence; C3). No design condition. Covers all three.
- **Theorem 6.** Part (a) needs nothing and gives the ceilings quoted under A3. Part (b)(ii) fits S2 at ρ = 0 only (independent null columns).

**At risk, in order.**
1. **A5(b) → Theorem 3.** Fails in the letter for any simulation that draws y from raw coefficients. Planned result 3 would repair it.
2. **A8 → Theorem 3.** Near-cancellation in S1; sign-dependent in S3; and the "no precedent" claim is wrong.
3. **A9 → Theorem 3.** Fails in S3; its constants cannot be met at any of our n.
4. **A5(a) → Theorem 1.** S1 uses the √(log p/n) scaling that A5(a) excludes. The supplement's beta-min theorem has the right form, but its constant is not met.
5. **A10(c) → Theorem 4.** Empty at our sizes.
6. **A4(b) → Theorem 3.** Holds in the simulations; the risk is with referees and real data.

**For the owner to decide** (I make no change): either add a design that Theorem 3 covers (for example AR 0.6 with fixed coefficients of one sign, as in the old "s0 = 5 strong" family that BENCH_DESIGN §6.3 keeps as secondary), or say plainly that S1–S3 test the method outside Theorem 3 and that Theorem 2 is the result that covers them.

**Errors and gaps found in the earlier comparison** (short text, `or5_assumptions.tex`, `s5_assumptions.tex`, `appendix_sl_or.tex`).
1. Short text, SAM list: omits Condition 2 (p. 954), and Theorem S with (22)–(23) and (26) (supp. pp. 13, 15).
2. Short table, A7 row: "nothing about collinearity" is true only for SAM's ridge prior (see A7).
3. `s5_assumptions.tex`, visibility: "None found" for precedents is wrong (see A8).
4. Short text, A5: "as in our simulations" is false for S1.
5. Short table, "Reasonable?" column and the rows for A6, A9, A10: they describe the old suite (blocks, factor simulations at n = 100).
6. Checked and found correct: the pages and wording of the six SAM items in the short text (pp. 947, 950, 953, 954, 955, 958); in `appendix_sl_or.tex`, (12)–(13) on p. 952, (22)–(23), (26), Corollary S1, remark (a) on p. 958, and the implicit lower bound at supp. pp. 6 and 15 (the first starts on p. 5).

---

## Not confirmed in a source

1. **S3's coefficients, signs and σ.** Not in REPORT §6.1, the HQ_DECISIONS entry of 11-24, or `sim_designs_cite.tex`. My S3 lines for A1, A5, A7, A8 and A10(b) are conditional on them.
2. **How y is generated in our simulation code.** I assumed fixed raw coefficients, as in the cited papers. I did not read the code.
3. **Which blocks the method forms in S1.** I did not check whether the ten true predictors share a block.
4. **Precedents quoted from `s5_assumptions.tex`, not rechecked:** Narisetty and He (2014), Shin et al., Shang and Clayton (2012), Castillo et al. (2015), Yang, Wainwright and Jordan, Zhang and Huang (2008), Bickel et al. (2009). The beta-min conditions of Castillo et al. and Yang et al. are quoted there from `supplement.tex`; also not rechecked.
5. **Bühlmann et al. (2010), Fan and Lv (2008), Barut et al. (2016).** I read only the quoted statements, in the arXiv versions named (v3, v2, v2). Journal pages not checked. None is in `refs.bib`.
6. **Del Moral (2004) and Schweizer (2012) for C3.** Taken from SMC_LIT REPORT; not rechecked. The two papers that report says "support the form" of A8 and A9 (Mathews and Schmidler 2024; Paulin, Jasra and Thiery 2019) were not read.
7. **Jiang (2007).** Not read; cited through SAM, p. 950.
8. **SAM supplement pp. 1–4, 7–12, 18–20.** Not read. The sampler pages 9–10 and 12 cited in `or5_assumptions.tex` are therefore unchecked.
9. **M0, n0 and c_H of Theorem 2.** No numerical values in the short text, so the finite-n reach of Theorem 2 cannot be judged.
10. **A10(a) on realised designs.** Not computed for any design.
11. **A9(c) for AR designs.** I sketched why it holds; I did not check the department's proof.
12. **Which SNR and ν cells are detectable.** My estimates under A5 are rough counts, not results from a source or from runs.
