# TH-SONG-ASSUMPTIONS — design memo R0 for the expert advisors (Fable 5.2, Astra 6.2)

Task Lead (Opus 5.5), 2026-11-27. Purpose: get your independent, adversarial input on the **target theorems** and the
**conjectured assumptions** before the draft package is written. We are NOT writing proofs yet; we must (a) state each
target theorem exactly, (b) give a concrete proof path showing where each assumption is used, (c) make every assumption
defensible to a top-journal referee (precedent with exact citation AND/OR S1/S2 evidence), and (d) avoid stringent/toy
assumptions. Where v3.1.1 assumptions look too strong (large proof constants vs S1 boundary signals, vacuous sample sparse
eigenvalues on S2, p ≤ n^A vs exponential p), propose weaker, still-provable alternatives.

## 0. Sources (all readable inside the worktree `/home/fb31/BVS-wt/THEORY-DEPT/`)
- Song & Liang (2015) main text and supplement: `.rc_tmp/song/papers/32.txt`, `32b.txt` (pdftotext) and the PDFs next to
  them. Page numbers below are the journal's printed pages (main, 947–972) and the supplement's printed pages (1–20).
- Our current statements (v3.1.1 manuscript, read-only copies): `.rc_tmp/song/ms/or6_theorems.tex`
  (thm:post-random l.71, thm:dist l.125), `.rc_tmp/song/ms/supplement.tex` (thm:post-fixed, asm:margin/thm:post-margin
  l.85–120, asm:omitted/thm:omitted l.122–155, prop:dist, thm:dist-param), `s4_results.tex`, `s5_assumptions.tex`.
- Baseline prep with the coded model, sensitivity map and S1/S2 evidence so far: `Theory_work/Dept/prep/TH_PREP.md`
  (§1 model as coded, §2 statement sheet, §3 sensitivity, §4a–4b P1/P2 evidence).
- Verified precedents: `Theory_work/Dept/writing_answers/PRECEDENTS_2026-11-17.md`.

## 1. The method as coded (v3.1.1) — what every theorem is about
Standardised X, y (centred; column SD 1 with divisor n−1); no intercept parameter. Slab β_S | S, σ² ~ N(0, nσ²(X_SᵀX_S+I)⁻¹)
(g = n, unit ridge — this is exactly Song–Liang's own SAM prior V_ξ⁻¹ = (X_ξᵀX_ξ+τI)/n, main p. 959, with τ = 1 instead of
0.01). σ² ~ IG(0.01, 0.01). Model prior BB(1,p) truncated at K = min(p, ⌊n/2⌋): per-model weight ½/C(2p−1,|S|), so the
size marginal decays like 2^{−k} and the per-model prior carries a p^{−k} multiplicity penalty. Price of adding one variable
to a size-k model: price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1) (prior + Occam). Report: MPM (PIP > ½); HPM stored. Sampler:
SMC (particle-limit results are DEFERRED by owner scope ruling; the three targets are about the exact posterior).

## 2. Song & Liang (2015) — what they prove (read directly by the Lead)
| SL result | statement (short) | key conditions |
|---|---|---|
| Thm 1 (p. 952) | P*[π{d(f,f*) > ε_n | D_n} > e^{−c₁nε_n²}] < e^{−c₁nε_n²}, Hellinger, random (x,y) | bounded predictors |x_i| ≤ 1; approximate sparsity (3) Σ|β_j| < ∞; (8)–(14): Δ(r_n) ≺ ε_n, r̄_n ln(1/ε_n²) ≺ nε_n², r̄_n ln P_n ≺ nε_n², r̄_n ln(nε_n² B̃_n) ≺ nε_n², 1 ≤ r_n ≤ r̄_n < P_n, r_n ≺ P_n, B(r_n) ≺ nε_n²; P_n ≻ n^θ (p. 950) |
| Thm 2 (p. 953) | same conclusion | Condition 1 (p. 953: E exp{(Σ_{i≤r} a_i x_{j_i}/r)²} ≤ e^M for r ≤ r̄_n, |a_i| ≤ δ — a sub-Gaussian-on-sparse-directions condition); strict sparsity (4); (9)–(14); r_n ≻ 1 |
| Cor 1 (p. 954) | ε_n = O(n^{−(1−α)/2} log^{k/2} n) or O(n^{−min{1−α−q,1−vq}/2}) | P_n < exp(Cn^α), α ∈ (0,1); B(r_n) ≤ Br_n^v, B̃_n ≤ Bn^v; r̄_n ≺ log^k n or n^q |
| Condition 2 → (16) (p. 954) | in-probability version of Thm 2 | second moments only |
| Thm 3 (p. 956) | sure screening: P*[π{t ∈ ξ | D_n} < 1 − e^{−c₁nε_n²}] < e^{−c₁nε_n²} for each identifiable true x_t | Thm 2 conditions + Condition 3 (p. 955, identifiability: E exp{−(x_k + Σ_{i≤r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n, δ_n ≻ ε_n²; for Gaussian x ⇔ var(x_k + Σ b_i x_{j_i}) ≻ ε_n², a VANISHING residual-variance floor). Proof (supp. §1.2, pp. 5–6): any f omitting x_t has d²(f*,f) ≥ min{δ_n, β_t*²δ_n/(20σ*²), 1−√0.8} — i.e. a residual-signal margin at the Hellinger scale, combined with contraction |
| Thm S (supp. p. 13) | MAP consistency: max_{k≠t} π(k|D_n)/π(t|D_n) →_P 0 (pairwise, NOT π(t|D_n) → 1) | fixed design; (12); sample eigen-structure (22) n l_n < ch'₁(X_ζᵀX_ζ) ≤ ch₁ < n l'_n on |ζ| = min{|t|+r̄_n, n}; (23) r̄_n log P_n ≺ n l_n; for V⁻¹ = XᵀX/n: n l_n ≻ l'_n and log(√n/r_n) ≻ √(log P_n). Proof (pp. 14–15) uses noncentrality ≥ n l_n c², c = min|β*_t|, needing n l_n c² ≫ log r̄_n + r̄_n log P_n (diverging-multiple beta-min × floor). SL themselves (p. 15): "(22) is hardly satisfied"; they propose the random-design replacement (26) (P[eigen bounds fail] < e^{−nC}), true for Gaussian designs with bounded population eigenvalues (Fan & Lv 2008, App. A.7) |
| Cor S1 (supp. p. 16) | MAP consistency | P_n < n^{κ log n}, κ ∈ (0, 1/4) (quasi-polynomial p), V⁻¹ = XᵀX/n (+τI/n), l'_n = l_n⁻¹ = √n/log^{k₂} n |
| Thm 4 (p. 957) | misspecified fixed subset s: π[{f ∈ P_s : d(f₀,f) > ε} | D_n^s] → 0 a.s., f₀ = KL projection | Condition 4 (p. 957: E(aᵀx_s)² < ∞ for |a_i| ≤ δ); π(ξ) > 0 for all ξ; s fixed (proof, supp. §1.3 p. 6–7, via De Blasi & Walker 2013 Cor 1 = supp. Lemma 1.2); f₀ = φ(y; β₀ᵀx_s, σ₀), β₀ = Σ_s⁻¹Σ_{s,t}β*_t, σ₀² = σ*² + E(β₀ᵀx_s − β*ᵀx)² |
| Cor 2 (p. 957) | π(s̃ ⊂ ξ | D_n^s) →_P 1, s̃ = supp β₀ (inclusion, not exact) | Thm 4 + no exact multicollinearity in x_s; withdrawn under a binding size cap (p. 958 (c)) |
| Condition 5 (p. 958) | |cov(x_t, y)| > 0 for every true x_t — makes the iterative screening keep all true predictors | — |
| SAM consistency (p. 959, §3.1) | "Clearly, it follows from the theory … that the SAM approach will lead to a consistent selection" (informal) | — |
| §6 time complexity; supp. §2 SAMC q̂_j → q_j a.s. | algorithmic | — |

## 3. Proposed target theorems (Lead's R0 conjecture) and candidate assumptions

Common notation: S0 = supp β*, s0 = |S0|; μ = Xβ* (sample) or μ(x) = xᵀβ* (population); for S ⊆ [p],
R_n(S) := n·Var(xᵀβ* | x_S) (population residual signal; = n β_Dᵀ Σ_{DD·S} β_D with D = S0∖S) and its sample twin
‖(I−P_S)μ‖². price_n := log(2p/s0) + ½ log(n+1) (per-variable cost; exact form price(k) above).

### T-DIST (distribution consistency; SL Thm 1/2/Cor 1 counterpart). Delivered as `thm:dist` (proved & checked).
P*[Π(d_H(f,f*) > √(M log n/n) | D_n) > n^{−c_H M}] ≤ n^{−c_H M} for M₀ ≤ M ≤ √n/log n.
Assumptions (asm:dist): GL (i.i.d. pairs, Gaussian noise); SPARSE (≤ s nonzero, s fixed); DIM (2 ≤ p ≤ n^A); SUBG (sub-Gaussian
along q_n-sparse directions, q_n ≍ M log n — compare SL Condition 1); NEC (λ_min(Corr(x_T)) ≥ c_ψ/n, |T| ≤ q_n — a vanishing
floor); BS (|β*_j| sd(x_j) ≤ b̄σ*). No beta-min, no fixed eigenvalue floor. Note SL's own (9)–(10) would FAIL for our cap
K = n/2 (r̄_n ≍ n); we instead use the prior's 2^{−k} size tail (Jiang 2007 §7 device that SL p. 951 mention).
**R0 candidate relaxation DIM′:** log p ≤ C n^α with α < α₀ (α₀ = ½? 1/3?) and rate √(M log(p∨n)/n). Question Q3.

### T-SEL (true-model selection; SL Thm 3 + Thm S counterpart). Delivered `thm:post-random` uses FIXED |β*_j| ∈ [b_lo,b_hi]
(FSb) + population floor EFS on sets of size 5(A+1)(s0+1)log n — S1 coefficients β ∝ √(log p/n) violate FSb as a sequence;
`thm:post-fixed`/`thm:post-margin` (fixed design) use sample floors (vacuous on S2: greedy proxy ≈ 1e−4/1e−5) and constants
c0, c1(s0,A) = max{4C*, 32[s0(A+1)+2]}-type, far above the empirical transition.
**R0 proposal (to be stress-tested):** two tiers, both random design:
- **T-SEL-a (sure screening, SL Thm 3 route):** under the T-DIST assumptions plus
  **MARGIN-H (order form):** for each j ∈ S0, inf{R_n(S) : j ∉ S, |S| ≤ q_n} / (σ*² M log n) → ∞ (or ≥ C_H, explicit),
  conclude Π(j ∈ S | D_n) ≥ 1 − n^{−c_H M} with probability ≥ 1 − n^{−c_H M}. Proof path: Hellinger lower bound for any f
  omitting j (SL supp. pp. 5–6 computation in our Gaussian random-design setting: d_H² ≥ c·min{1, R_n(S)/(nσ²)}-type) +
  T-DIST + prop:dist size tail.
- **T-SEL-b (exact selection, Thm S counterpart, stronger: π(S0|y) → 1):** assumptions GL, DIM, SPARSE(s0 fixed),
  SUBG, NEC, BS, FLOOR-S0 (λ_min(Σ_S0) ≥ φ0² fixed, or implied by the margin), and
  **MARGIN (sharp, per missed predictor):** for every S with S0 ⊄ S and |S∖S0| ≤ j0 (j0 fixed, from the size tail):
  R_n(S) ≥ (2+η) σ*² |S0∖S| price_n, fixed η > 0 [order form: (R_n(S) − 2σ²|S0∖S|price_n)/log n → ∞ is the
  constant-free variant]. Conclusions: P(HPM = MPM = S0) → 1, 1 − π(S0|y) = O_P(√(log(p∨n)/n) + n^{−c η}).
  Proof path (sketch): (1) size tail Π(|S| > s0 + j0) small (prop:dist(ii)); (2) supersets S0 ∪ N: prior p^{−m}
  multiplicity × Occam (n+1)^{−m/2} vs Σ_N exp(½χ²_{m,N}) ≈ (p√log p)^m/m! ⇒ mass O_P(s0√(log p)/√n) (cf. `rem:sharp`
  lower bound, which shows this rate is attained); (3) rivals missing D ≠ ∅: log odds ≈ −½χ'²_d(R(S)/σ²) + ½χ²_m
  + (d−m)price; MARGIN beats d·price; sample-to-population transfer of R uniformly over |S| ≤ s0 + j0 by sub-Gaussian
  concentration on sparse sets (RZ/RWY-type), needs (s0+j0) log p/n → 0; (4) lem:summaries for HPM/MPM/PIPs.
  Existing thm:post-random is the corollary FSb + EFS ⇒ MARGIN for n large. MARGIN with c = 2 is NECESSARY for single
  deletions (odds of S0∖{j} vs S0 ≈ exp(−½t_j² + price)) — P1 found min t² > 2·price is a near-perfect necessary
  condition on S1/S2 (9 of 11,466 fits below it recover S0), but not sufficient (P(exact|yes) = 0.95 S1, 0.45 S2).
  The worker is now computing a swap-aware κ_pop = min_S R(S)/(2σ²|S0∖S|price) and an odds margin
  Λ(S) = ½R(S)/σ² − (d−m)price − m log p to see if it closes the sufficiency gap.
  **Precedents for MARGIN:** SL Condition 3 + their Thm 3 proof (residual signal ≥ ε_n-scale), Chen & Chen (2008)
  EBIC identifiability, NH14 Condition 4.4 (being verified now); information-theoretic necessity of √(log p/n) signals
  (Wainwright 2009, IEEE-IT) — being verified.

### T-MIS (misspecification; SL Thm 4 + Cor 2 counterpart). Delivered `thm:omitted` / C-MIS MIS(i)–(iii): candidate-only
rerun; asm:omitted (a) Gaussian candidate rows and a Gaussian, linear, homoscedastic working residual given x_C
(true under jointly Gaussian (x_C, x_M) — Example ex:omitted), (b) floor on 3(A+1)(s_C+1)log n sets, (c) bounded projected
signal + n min Σ_jj(β^C_j)²/(σ_C² log n) → ∞. Gives exact selection of S0^C = supp β^C at rate (stronger than SL Cor 2's
inclusion), but no literal SL Thm 4 (density consistency to the KL projection).
**R0 proposal:**
- **T-MIS-a (density):** Π(d_H(f, f₀) > √(M log n/n) | D_n^C) → 0 at the T-DIST rate, f₀ = φ(y; β^{Cᵀ}x_C, σ_C) ⊗ ν(x_C)
  = SL's f₀ (supp. p. 6). Proof path: when the working model is correctly specified for (x_C, y) [jointly Gaussian case],
  this is literally T-DIST applied to the candidate data with (β^C, σ_C²) — conditions SUBG/NEC/BS/SPARSE on the
  candidates. For non-Gaussian designs the conditional law of y | x_C is not Gaussian-linear: then we need a genuinely
  misspecified contraction theorem (Kleijn & van der Vaart 2006; De Blasi & Walker 2013), and Grünwald & van Ommen (2017)
  show Bayesian linear-model inconsistency under heteroscedastic misspecification — Question Q6.
- **T-MIS-b (selection of the pseudo-true support):** exact selection of S0^C under MARGIN applied to (μ_C = x_Cᵀβ^C, σ_C²)
  — i.e. the same assumption set as T-SEL-b on the candidate problem, with the noise variance inflated to σ_C². Already
  supported by S2 data: E[σ²|y, MPM]/σ_C² has median 0.99 (S1), 0.94 (S2) (TH_PREP §4b E6).

## 4. Questions for you (answer each; be adversarial; say "unprovable as stated" when it is)
Q1. **MARGIN form.** Is "R_n(S) ≥ (2+η)σ²|S0∖S|·price_n for all S missing a true predictor with |S∖S0| ≤ j0" sufficient
    for T-SEL-b with fixed η > 0, or does the cross term ⟨(I−P_S)μ, ε⟩ maximised over the C(p,m) choices of N (and
    the noise gain ½χ²_m of the added nulls) force either (i) a larger constant, (ii) an extra "local entropy /
    bounded confounding" condition (how many N can reduce R(S) appreciably — O(1) on AR(1)/banded designs, many on
    equicorrelated ones), or (iii) the odds-margin form Λ(S) = ½R(S)/σ² − (d−m)price − m log p → ∞? Give the
    cleanest SUFFICIENT condition you believe is provable, with the proof step where it bites, and the cleanest
    NECESSARY condition. Is constant 2 sharp for single deletions?
Q2. **Order form vs explicit constant.** SL's conditions are all order conditions (≻). Is it defensible to state the
    asymptotic theorems with constant-free order conditions (e.g. MARGIN-H with ratio → ∞; MARGIN with
    (R − 2σ²d·price)/log n → ∞) and give a separate non-asymptotic/explicit-constant companion calibrated on S1/S2?
    Does the order form cover S1's boundary signals in a meaningful asymptotic sense (S1: β_j = c·SNR·√(log p/n), so
    R/log n is a fixed constant along the S1 sequence)? What is the right asymptotic framing so S1 is covered?
Q3. **Dimension.** (a) For T-SEL-b, is log p = o(n) (with s0 fixed) enough given the per-model p^{−k} prior penalty, or does
    something (union over sparse sets for sample–population transfer, the IG/σ² envelope, the (n/2)log RSS
    linearisation) force log p = O(n^α) with α < 1/2 or p ≤ n^A? (b) Same for T-DIST (our proof uses q_n ≍ M log n sets and
    p ≤ n^A in union bounds; SL Thm 2 allows r̄_n log P_n ≺ nε_n²). (c) Same for T-MIS. Propose DIM′ per theorem.
Q4. **Eigenvalue conditions.** Can T-SEL-b drop the fixed population floor on O(log n)-size sets (EFS) and keep only the
    vanishing floor NEC (c_ψ/n) + a fixed floor on S0 (or nothing beyond MARGIN)? SL's Thm S itself needs (22) on
    |t|+r̄_n sets and remarks it is "hardly satisfied" (supp. p. 15), replacing it by random-design (26). Which is the
    weakest refereeable form?
Q5. **Sparsity and signal size.** s0 fixed (SL (4), NH14 Cond 4.3) vs s0 → ∞ with s0 log p = o(n): what breaks (the rate,
    the size-tail constant 2^{−k} vs s0 growth)? Is BS (bounded signal |β_j|sd_j ≤ b̄σ) truly needed for T-SEL-b /
    T-DIST, and is there a weaker form (e.g. βᵀΣβ ≤ M σ² or log-growth)?
Q6. **Misspecification.** What is the weakest defensible T-MIS-a assumption beyond the jointly-Gaussian case? Options:
    (i) working residual u = y − x_Cᵀβ^C independent of x_C and sub-Gaussian (homoscedastic, non-Gaussian); (ii) only
    E[u x_C] = 0 with bounded conditional variance; (iii) keep Gaussian-linear-homoscedastic (current). Which exclude
    Grünwald–van Ommen's phenomenon, and which can our proof route (exact g-prior marginal, quasi-likelihood) reach?
    Can T-MIS-b (exact pseudo-true support selection) survive option (i)?
Q7. **SL items we may be missing.** Any SL result in §2 above whose counterpart we should state that we have not (e.g.
    approximate sparsity (3) for T-DIST; SL's a.s. mode in Thm 4; Condition 5's iterative guarantee; Condition 2's
    second-moment-only result)? For each, say "state as target", "note as non-target with reason", or "dominated".
Q8. **Engineering sensitivity.** Engineering may change: slab g (smaller g or g = max(n,p²)), size prior BB(1,p^u)
    (u < 1 lighter), reporting rule (PIP threshold q, HPM), cap K. For each, which assumption changes (form invariant
    vs constant vs new condition)? Note MARGIN is stated in terms of price_n, so its FORM is invariant and its constant moves
    with g and the size prior; superset control needs price ≥ (1+ε) log p, i.e. a DIM-type condition for u < 1 or small g.

## 5. Deliverable from you
Write your answer to `Theory_work/Dept/song_assumptions/advisors/<FABLE|ASTRA>_R1.md`: for each Q, (1) verdict, (2) the
precise assumption you recommend (math), (3) the proof step where it is used and why it suffices (sketch, no hand-waving),
(4) referee risk (low/medium/high) and why, (5) precedent if you know one (mark "to verify" — do not invent pages).
End with your recommended FINAL assumption list per theorem (T-DIST, T-SEL-a, T-SEL-b, T-MIS-a, T-MIS-b), each
assumption tagged (a) precedent / (b) empirical / (c) mild technical. ≤ 700 lines.
