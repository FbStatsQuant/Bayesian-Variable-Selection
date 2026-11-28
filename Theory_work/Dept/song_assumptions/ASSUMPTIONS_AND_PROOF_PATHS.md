# ASSUMPTIONS AND PROOF PATHS — conjectured assumptions for the TH-SONG targets

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **v1.4 (senior review: completeness, generality and naturalness; converged text in council/V14_CHANGESPEC.md). v1.3 = council round-2 revision (COUNCIL_RECORD.md, council/RESPONSE_R2.md).**
Targets and notation: `THEOREM_DEFINITIONS.md` §4 (R_n(S), Pr_n(d), κ_n, D, N, d, m, J, f₀, β^C, σ_C²). Standardised predictors ζ_j := (x_j − E x_j)/sd(x_j). Level and window: fix M ≥ 1 first. The design assumptions A-SUBG and A-NEC are imposed on sets of size ≤ k_n, a deterministic design order with k_n ≥ q_n(M) at the claimed level (THEOREM_DEFINITIONS §4): for fixed-level statements, sets of size ≤ c·log n for every fixed c suffice across all fixed levels (one fixed level needs only one such window); q_n(M_n) for M = M_n → ∞ (the delivered `thm:dist` range M ≤ √n/log n); the enlarged q_n for TD′. The proof constant is as delivered (or5 `sec:a-dist`): q_n(M) := min{p, ⌈C_q M log n⌉}, C_q := 2(s(A+2)+4)/log 2. price_n := price(s0−1) = Pr_n(1). Four blocks: Model (A-GL, A-SPARSE, A-DIM, A-BS); Design (A-SUBG, A-NEC); Signal (A-MARGIN-H, A-MARGIN-U); Omitted variables (A-MIS(iii) with A-SPARSE-C; A-MOM). **No assumption names a design family or a simulation constant; S1/S2 appear only in the Defence (b) items.** Engine decision (HQ, SMC-PERF closed, memo 1b319090): v3.1.1, g = n, truncated BB(1, p) and MPM confirmed; see §5.
Inputs: advisors `advisors/ASTRA_R1.md` (Astra 6.2) and `advisors/FABLE_R1.md` (Fable 5.2), which were written
independently, and `advisors/ASTRA_R2.md` (Astra's audit of Fable R1 and of v1 of this file; all its substantive points applied); data `SIMULATION_DATA_ANALYSIS.md` (D1); literature `PRECEDENTS_NEW.md` (C2, with the Lead's errata) and
`writing_answers/PRECEDENTS_2026-11-17.md` (verified earlier).

**What "conjectured" means here.** No proof is claimed. Every assumption must pass a dual bar.
- **(a) Proof path.** A sketch names the step that uses the assumption (§3).
- **(b) Defensibility.** The assumption has an exact verified citation (paper, label, page, version), S1/S2 evidence, or both.

Tags used throughout:
- [P]: an advisor gives the inequalities, and a proof at this level should go through once constants are audited.
- [both advisors]: two advisors gave the same route independently.
- [H]: heuristic.
- [C]: conjecture.
- (a) precedent, (b) empirical, (c) mild technical.

Every citation below is either in PRECEDENTS_2026-11-17 (marked "P17") or in PRECEDENTS_NEW (marked "PN"), with its page.

---

## 1. Design decisions (where the two advisors agree, and how disagreements were settled)

| # | question | Astra R1 | Fable R1 | decision |
|---|---|---|---|---|
| D1 | form of the selection margin | √((1−δ)nρ_S) ≥ a_Dm + √(2(1+δ)[B_Dm]₊), where a_Dm is the proxy-search Gaussian width | MARGIN-U: √R/σ ≥ (1+η)[√((2Pr−m log(n/C log p))₊) + √(2m log p)]. Sharp variant MARGIN\* with a leakage set | **v1.4: A-MARGIN-U, population form** (senior review; V14_CHANGESPEC §1): (U1) deletions, (U2a) bases inside a deterministic accounting set Q_n, (U2b) outside nulls priced by their leakage with Astra's geometric coefficient ā; merges Fable's P-U and Astra's finite-ratio form. Lemma W bridges it to the proof. v1.3's conditional-width form (Astra R2 Q2, classes with B_Dm > 0) is kept as the **refined design-conditional form**, a parallel sufficient condition. MARGIN\* is superseded |
| D2 | is the constant 2 sharp? | yes for single deletions. A uniform 2+η for swaps is OPEN. R2: the converse holds given A-NEC on T (two-sided determinant refund) | yes for deletions, with a converse. The width term is attained by a factor-proxy design | constant 2 for deletions plus a converse (needs A-NEC on T). Width term for added nulls; the factor-proxy example shows it is needed at one (d,m), not that every constant is optimal |
| D3 | the memo's literal "2·d·price for every rival" | not provable | counterexample for a fixed number m of added nulls when log n = o(log p) | **rejected**. Recorded as OPEN under p ≤ n^A |
| D4 | covering boundary signals (effects of order √(log p/n)) | covered when c_j²a > 2a+1 with log p/log n → a | fixed-ratio framing: liminf κ_n > 1 | **κ_n framing** (triangular arrays), chosen on **generality grounds**: a scale-free ratio of population residual signal to the coded price, with no design family. The S1 check is in A-MARGIN-U Defence (b) |
| D5 | dimension | keep p ≤ n^A for released statements. R2: Fable's DIM′ route fails at its testing step (at log p = n^{1/3}: sieve log-entropy ≍ n^{2/3} against a testing budget nε² ≍ n^{1/3}) | DIM′: (log p)² = O(n) via the Fubini size tail. log p = o(n) needs a cap c·n/log p | released statements keep **A-DIM**. **TD′ is a conjecture with HIGH proof risk at the proposed rate**; the route needs localisation at size ≈ t/log p or a direct predictive bound. A fixed feasible cap is a distinct, easier case. No impossibility is implied |
| D6 | eigenvalue conditions | drop the fixed floor (including on T). Keep NEC plus relative SUBG | drop EFS and FLOOR-S0. NEC is needed only for the Occam factor | **drop all fixed and sample floors.** Keep A-NEC (used for the Occam factor, the size lemma prop:dist(i) and the TD tests) and Σ-relative A-SUBG [both advisors] |
| D7 | bounded signal | aggregate energy pair (O(n) form) | BS′: βᵀΣβ ≤ M_μσ², s·b̄_n² = o(n) | **A-BS** (as delivered) for TD **and** TS-b/TM-b, because TS-b uses the size lemma prop:dist(i), proved under A-BS (R2). **A-BS′** is a weaker alternative, available once the size lemma is extended |
| D8 | misspecification | option (iii) (independent N(0,σ_C²) residual). Non-Gaussian is high risk. C must be prespecified | three tiers: a0 (fixed p_C, moments, a.s.); (iii); (i′) with a cap. (ii) only as a remark | **TM-a0 + TM-a/TM-b under (iii)**. (i′) and (ii) are remarks |
| D9 | almost-sure versions | Borel–Cantelli with c_H M > 1 (for posterior tails along a fixed-truth sequence) | same, for TD/TS-a/TM-a0 but not for TS-b | **TD-as, TS-a a.s., TM-a0 a.s.** (fixed truth). TS-b stays in probability |
| D10 | Engineering: BB(1,p^u), u < 1 | TH_PREP §3 is wrong: the loss is the size tail | same correction, independently | TH_PREP §3 is **superseded** (§5) |
| D11 | SL Condition 3 | R2: **not** implied by SUBG (Gaussian duplicates are sub-Gaussian with R = 0). SUBG gives only the conversion d_H² ≥ c_L·min{1, R/(nσ²)} | claimed implied by sub-Gaussian rows | SL Condition 3's role is taken by **A-MARGIN-H** (a lower bound on R) plus the SUBG conversion inequality; no separate collinearity condition |

---

## 2. The assumption catalogue

Each row gives the exact statement, where the proof uses it, its defence, and the weaker alternatives considered (the anti-stringency rule).

### A-GL — Gaussian linear model, i.i.d. pairs
- **Statement.** y = α* + xᵀβ* + ε with ε ~ N(0, σ*²) independent of x, σ*² > 0, and (x_i, y_i) i.i.d. The quantities α*, β*, σ* and the law of x may depend on n. This is or5 `asm:dist`(a).
- **Used in.** TD, TS-a, TS-b, and (at candidate level, via A-MIS(iii)) TM-a/TM-b. **Not** TM-a0, which lies outside A-GL.
  - Exact conjugate marginals of the coded score: m_S(y) ∝ π(S)·{det[(n+1)G_S+I]/det[G_S+I]}^{−1/2}·(2b₀ + Q_S)^{−(n/2+a₀)}, G_S the coded (standardised) Gram X_SᵀX_S, b₀ the coded IG rate (the raw-unit rate is b₀s_y²).
  - The Fubini identity for the **normalised fixed-endpoint contrast density**: after passing to raw centred contrasts and sandwiching b₀s_y² between fixed endpoints, E*[m^c_{S,b}/f*] = 1 conditional on X (TD′ step 1). The plug-in score itself does not satisfy this identity; the denominator lower bound carries an extra variance-integration factor ≍ n^{−1/2} and the exceptional event is controlled separately. For non-Gaussian residuals the Gaussian denominator and the fractional-moment localisation steps are what need replacing.
  - The Beta law of RSS ratios for supersets, which needs Gaussian ε (TS-b step 2). With centring, RSS_{S0∪N}/RSS_{S0} ~ Beta((n−1−s0−m)/2, m/2) conditional on full rank.
- **Defence.**
  - (a) Song & Liang (SL) model (1), p. 947 (same model, no intercept). Fixed-design/conditional-on-X Gaussian analogues: NH14 Cond. 4.3, p. 11 (PN A2); YWJ p. 7 (PN E17). Random i.i.d. design with Hellinger distance on joint densities: Jiang 2007 (a GLM paper with bounded covariates; set-up arXiv pp. 2–3 and 6, PN C7).
  - (b) S1/S2 are generated this way.
- **Weaker alternatives.**
  - Non-Gaussian independent ε, i.e. A-MIS(i′): the Beta law and the Fubini size tail fail. Fable's union route *suggests* a sufficient cap K_n ≤ c·n log n/(log p)² and a variance-proxy budget; neither is shown necessary (Astra R2). **Not adopted** as coded, so it stays a remark.
  - Heteroscedastic ε: the Grünwald–van Ommen mechanism applies, so it is a remark with the counter-calculation (TM §4.3).

### A-SPARSE — fixed sparsity
- **Statement.** |S0| ≤ s, with s fixed (or5 `asm:dist`(b)). For TS-b, s0 ≥ 1 is fixed.
- **Used in.** The size of the window q_n; the 2^{s0} deletion directions (TS-b step 1); the superset mass (s0+1)√(log p/n).
- **Defence.**
  - (a) SL strict sparsity (4), p. 950 (used by Thms 2–3 and Thm S; Thm 4 instead assumes a fixed candidate subset and Condition 4, p. 957); NH14 Cond. 4.3, p. 11, "the size of the true model |t| is fixed" (P17).
  - (b) s0 ∈ {5, 10} in S1/S2.
- **Weaker alternatives.**
  - Growing s0. Fable's route suggests s0²·log p = o(n), s0·(log p)² = o(n) and log s0 = o(η² price) (Fable Q5). `rem:sharp`(a) (which requires s ≤ min(K−1, p/2)) bounds how fast s0 may grow for π(S0|y) → 1; the upper rate s√(log p/n) is not a universal necessity for growing s (Astra R2). **Recorded as a growth remark**, not adopted: the owner's targets use fixed s.
  - Approximate sparsity, SL (3): optional corollary TD-A [P, to audit].

### A-DIM — polynomial dimension (released statements)
- **Statement.** 2 ≤ p ≤ n^A for a fixed A ≥ 1 (or5 `asm:dist`(b)).
- **Used in.**
  - TD: hierarchy at fixed M. (1) Coarse window q_n(M): isometry and NEC on q_n-sets; there are exp(O(log² n)) such sets, which an isometry failure probability exp(−cn) absorbs. (2) Localisation (prop:dist(i), fractional Bayes-factor moments, which need p ≤ n^A) to |S| ≤ J := ⌊s + C_s M⌋. (3) Only then the O(M log n) testing budget, on the localised sieve. The testing budget does **not** absorb the coarse count.
  - TS-b: the bounded-size event |S| ≤ J; the R-transfer on (s0+J)-sets; the Occam factor on q_n-sets.
- **Defence.**
  - (a) SBJ comment after Assumption 5, p. 14: "continue to hold when p grows polynomially" (P17 B2). Johnson & Rossell 2012 Thm 1, p. 651: p ≤ n (PN E16). SL Cor S1, SLs p. 16: quasi-polynomial P_n < n^{κ log n}.
  - (b) A = log p/log n is 0.90–1.37 on S1 and 1.50–1.77 on S2; tabulated typical user regimes have A ≤ 1.74, and p ≤ n² holds in every setting and in six typical regimes (D1 E6). These are numerical dimension ratios at finite n, not a test of an asymptotic condition.
- **Weaker alternatives.** See A-DIM′ and A-DIM″ below; the anti-stringency verdict is in §4, item 3.

### A-DIM′ — dimension relaxation (conjecture, TD′)
- **Statement.** log p = o(√n) is the conjecture's regime. Its proof budget is the product form (s+1)·M·log p·log(p∨n) ≤ c_dim·n (the +1 keeps the coarse-window/variance-integration term at s = 0; Neon, Sol), a sufficient **isometry** budget only; the conjectured TD′ statement is given exactly in THEOREM_DEFINITIONS §4.1 (input domain 2 ≤ p with the coded exceptional event; A-SUBG and A-NEC on the enlarged window q_n = min{p, ⌈C′(s+1)M log(p∨n)⌉}; tail exp(−cM log(p∨n)); M ≥ M₀ with M log(p∨n) ≤ c√n) (Sol R2).
- **Used in.** Sample control on q_n-sets, where q_n ≍ min{p, (s+1)·M·log₂(p√n)} is the coarse size window from the Fubini size tail (TD′ step 2).
- **Defence.**
  - (c) Its dimension envelope contains SL Cor S1's quasi-polynomial range p < n^{κ log n} and overlaps the stretched-exponential envelope of SL Cor 1 for α < ½ (overlapping dimension envelopes only: the cap, prior and radius differ, so TD′ would not recover Cor 1 in full).
  - (a) Same type as SBJ Assumption 1, log p = O(n^α), p. 14 (P17 B2), and Jiang 2007 Cor 1, K_n ≤ e^{Cn^ξ}, p. 10 (PN C7).
  - (b) log p/√n is 0.20–0.38 on S1 and 0.69–0.98 on S2 (D1 E6).
- **Risk.** **High at the proposed rate** (Astra R2 Q1). Fable's step 3 fails: at log p = n^{1/3}, A-DIM′ holds but log C(p, q) ≍ n^{2/3} exceeds the testing budget nε² ≍ n^{1/3}. Moreover, the delivered proof localises to sizes s0 + O(t/log n) by fractional Bayes-factor moments whose factor p^{1−λ}n^{−λ/2} is not controlled for super-polynomial p. A proof needs localisation at size ≈ t/log p or a direct predictive bound. **Status: conjecture**, not part of any released statement; no impossibility follows from the failed route.
- **A-DIM″ (an Engineering option, not adopted).** A cap K_n ≤ c·n/log p solves the isometry inequality but **not** the testing inequality (Astra R2), so it does not by itself give TD at log p = o(n). A *fixed* feasible cap ≥ s is a distinct, easier case. Compare the NH14 cap m_n(ν) = p ∧ n/((2+ν) log p), pp. 10–11 (P17 B6).

### A-SUBG — sub-Gaussian rows on sparse directions, relative to their own variance
- **Statement.** Every predictor has positive variance, and E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2) for all λ and all u with at most k_n nonzero entries (the window in the header), ζ_j = (x_j − E x_j)/sd(x_j) (or5 `asm:dist`(c), already Σ-relative). The constant L is common to all window sizes.
- **Used in.**
  - The two-sided sparse isometry (1−δ)n·vᵀΣv ≤ ‖Xv‖² ≤ (1+δ)n·vᵀΣv on (s0+J)-sparse v. This gives the R-transfer (1−δ)R ≤ R̂ ≤ (1+δ)R (TS-b step 4).
  - The conversion inequality d_H² ≥ c_L·min{1, R/(nσ²)} (TS-a): relative SUBG gives E V⁴ ≤ C_L(E V²)² for an affine mean contrast V, hence P(V² ≥ E V²/2) ≥ 1/(4C_L) (Paley–Zygmund), and the Gaussian conditional affinity converts this (Astra R2 Q4). This converts R into Hellinger separation; it does **not** supply a lower bound on R (Gaussian duplicates have R = 0).
- **Defence.**
  - (a) Same type, different normalisation: SL Condition 1, p. 953, is an absolute-scale exponential moment on sparse directions (|a_i| ≤ δ), not Σ-relative; RZ Def. 1.5/Thm 1.6, pp. 5–6 (Σ-relative); NH14 Lemma 6.1, p. 16, is an identity-covariance transfer analogue (P17 B7b).
  - (b) S1/S2 rows are Gaussian.
- **Weaker alternatives.**
  - SL Condition 2 (second moments only). The exact-marginal route needs exponential tails on q_n-sets, so this is **not adopted** in high dimension. It *is* the setting of TM-a0 (fixed p_C).
  - Bounded predictors (SL Thm 1): **not dominated.** Bounded coordinates satisfy the per-coordinate version, but the sparse-direction relative version can fail: x₁ = Z, x₂ = Z + B with Z Rademacher and B ~ Bernoulli(1/n) independent are bounded with variances bounded below, yet the standardised contrast recovering B − EB has ψ₂²/Var growing with n (Sol, Neon, Opus R1). Independent bounded coordinates, or linear mixtures of independent bounded features with bounded standardised range (or5 `asm:dist` remarks), do satisfy A-SUBG.

### A-NEC — no near-exact collinearity (vanishing population floor)
- **Statement.** With the sparse eigenvalue φ_min(k) := min_{1≤|V|≤k} λ_min(Corr(x_V)), n·φ_min(k_n) ≥ c_ψ (or5 `asm:dist`(d), window as in the header). The sparse eigenvalue may vanish, but no faster than the ridge scale τ/n (τ = 1 as coded). Excluding exact duplicates alone does not ensure it: two predictors with correlation 1 − n^{−2} fail it.
- **Used in.** (i) The full Occam factor (n+1)^{−m/2} on added nulls: λ_min(X_TᵀX_T) ≳ 1 relative to the unit ridge (coded determinant ratio det[(n+1)G+I]/det[G+I]); also Q_U − RSS_U = O_P(σ²) uniformly (in-span shrinkage eigenvalues O(1/n)). (ii) The size lemma prop:dist(i) and the TD tests (or5 `asm:dist`(d)); without A-NEC, prop:dist(ii) gives only s + C_s M log n (Opus R1). (iii) The TS-b converse, which needs the two-sided determinant refund d·log(n+1)/2 + O(1) on T (Astra R2 Q3). The *sufficient* direction **of the deletion step (step 1) only** uses the one-sided refund ≤ (n+1)^{d/2}, valid for every design by Cauchy interlacing (Fable (F3)). A-NEC is a sufficient, convenient device; heuristically, a null nearly collinear with the model pays almost no Occam price, but **necessity is unproved** (Astra R2).
- **Defence.**
  - (a) **Comparison of objects, scales and windows — not dominance** (council R1, all three seats). A-NEC is a lower floor on a *population* correlation matrix, on q_n-sets, with a vanishing value c_ψ/n, and it works only together with A-SUBG (for transfer). The precedents differ in object and window:
    - NH14 Cond. 4.5, pp. 11, 17, bounds the minimum **nonzero** *sample* eigenvalue and expressly allows exact dependence (p. 17), which A-NEC excludes; its floor ≳ p_n^{−κ} can be smaller than c_ψ/n at large p, and NH14 also impose an upper bound (P17 B6).
    - SBJ Assumption 4, p. 14, bounds its nonzero-eigenvalue quantity ν_{k*} from (8), indexed through min(n, |k|); we do not claim it expressly allows duplicates (Sol R2).
    - SL (26), SLs p. 15, is a **two-sided sample** tail condition with a vanishing lower and a growing upper threshold (Cor S1 chooses such a pair; l_n ≫ r̄_n log P_n/n, Cor S1 uses l_n = log^{k₂}n/√n) on sets of size r̄_n + |t|; SL call their (22) "hardly satisfied" (SLs pp. 15–16).
    - SL Condition 3's Gaussian sufficient form ch₁{var(x)} ≻ ε_n² (pp. 955–956) is SL's own precedent for a vanishing population floor. A-NEC at the 1/n scale does not supply SL's screening separation, which is A-MARGIN-H's job.
    - BRT09 Assumption 2, p. 9 (c/log n) and MY09 ("slowly vanishing") are sample floors on other windows.
    - **No blanket ordering is claimed** (council R2, all seats). Where the regimes overlap, c_ψ/n is below the BRT09 (c/log n) and MY09 floors and below SL (26)'s lower threshold l_n ≫ r̄_n log P_n/n; NH14's p_n^{−κ} can be smaller still at large p. As *condition sets* (object, normalisation, window) none is uniformly weaker.
  - (b) The population floor (1−ρ)/(1+ρ) is 0.176–1, i.e. n × floor = 8.8–250 (D1 E5); the slack relative to c_ψ/n is this number divided by c_ψ.
- **Weaker alternatives.** For TD: drop A-NEC entirely; the delivered prop:dist(ii) gives TD with radius √(M log n·log(p∨n)/n). For TS-b: none established. A fixed floor delivered on a smaller window (EFS, `thm:omitted`) does not imply A-NEC on the TD window.

### A-BS / A-BS′ — bounded signal
- **A-BS (as delivered, used for TD).** |β*_j|·sd(x_j) ≤ b̄σ* for every j (or5 `asm:dist`(e)).
- **A-BS′ (recorded, not adopted).**
  - Recorded pair: V := Var(xᵀβ*)/σ*² = O(1) and E := Σ_j β*_j² Var(x_j)/(nσ*²) = o(1); at fixed s this is equivalent to v1.3's BS′ ((a) β*ᵀΣβ* ≤ M_μσ*², (b) s·b̄_n² = o(n)).
  - Open target: V = O(1) alone, i.e. population R² = V/(1+V) ≤ 1 − c. With A-NEC on T it gives E ≤ M_μ/c_ψ = O(1). Open: whether the size lemma and the ridge remainder hold at O(1) rather than o(1) energy.
  - TS-b and TM-b use the size lemma prop:dist(i), which is proved under A-BS; A-BS′ becomes usable only once that lemma is extended (Astra R2).
- **Used in.** The Fubini denominator, i.e. the fixed-endpoint lower bound of §3.1 step 1 for the normalised contrast density (order n^{−s0/2} times the variance-integration factor ≍ n^{−1/2}, on a high-probability event; Sol R2); keeping σ̂² in a fixed range; the unit-ridge term ‖β̂_S0‖²/(n+1). **Verify at proof audit** that nothing else uses coordinatewise boundedness (Fable Q5).
- **Defence.**
  - (a) **Direct counterpart: SL approximate sparsity (3), p. 950**: lim Σ_j |β*_j| < ∞, with standardised predictors and fixed σ*, implies A-BS.
  - (a) YWJ (7a), p. 7: "some form of upper bound on the norm ‖β*‖₂ in terms of the g-hyperparameter is required" (P17 B4b); SC11 Assumption 2.7, p. 7. Both bounds grow with n (with g ≍ p^{2α} in YWJ, with φ_n in SC11), whereas A-BS uses a fixed constant b̄; the precedent is for the type of condition, not its strength.
  - (b) max|β|sd/σ ≈ 1.17 (1.175) and ν ≤ 6 in every setting (D1 E4).
- **Weaker alternatives.** The aggregate energy pair (Astra Q5) / A-BS′ (Fable Q5): recorded, not adopted, until the size lemma is re-proved under it. All targets keep A-BS.

### A-MARGIN-H — Hellinger-scale residual signal (TS-a)
- **Statement (diverging ratio).** For the predictor j and **every fixed k**, inf{R_n(S) : j ∉ S, |S| ≤ k}/(σ*² log n) → ∞. This gives screening at every fixed level M; a diverging ratio at an unspecified speed gives nothing uniform for M = M_n → ∞. TS-a is stated first per predictor (any j satisfying its own margin, whatever the other signals do) and then jointly. Same form as delivered `asm:omitted`(c) and Luo & Chen's condition.
  - **Remark (fixed-level form).** At a fixed level M, inf R_n(S)/(σ*² log n) ≥ C_L·M over S with j ∉ S and |S| ≤ min(K, J), J = ⌊s + C_s M⌋ the effective-sieve size, with C_L above the inverse Hellinger-conversion constant, suffices (council R1: Sol, Neon; under A-DIM, log n and log(p∨n) differ by the factor A). It is sharper for finite-ratio signals and gives the a.s. corollary at a large fixed level.
  - The relevant sets satisfy |S ∪ S0| ≤ min(p, s0 + J) ≤ q_n for large n at fixed M (also covering bounded p), inside the A-SUBG window.
- **Used in.** TS-a: by the SUBG conversion, d_H(f, f*)² ≥ c_L·min{1, R_n(S)/(nσ*²)} > ε_n² for every f supported on such an S, so these f lie outside the TD ball; models with |S| > J carry the posterior size tail, which is added to the contraction tail (constant c′_H < c_H in TS-a). A-MARGIN-H is what supplies the lower bound on R; it plays the role of SL Condition 3.
- **Defence.**
  - (a) SL Condition 3, p. 955, and the proof of Thm 3, SLs pp. 5–6: d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}. The same residual-signal form appears in Luo & Chen arXiv v1 p. 7 (PN A4) and NH14 Cond. 4.4, p. 11 (PN A2).
  - (b) **Scale diagnostic only.** D1 E2 (restricted search: exhaustive deletions up to size 3, greedy additions, radius ε_n² = s0 log p/n; residual-variance/radius² ratio) gives a ratio ≥ 1 in only 9 of 136 settings. The companion fixed-variance squared Hellinger ratio, with 1 − (1 + r/4)^{−1/2} an upper bound on the package's optimised squared distance 1 − (1 + r/2)^{−1/4}, never reaches 1 (max 0.21; Sol R2). It cannot certify the theorem margin (C_H unknown). Recovery occurs below it, so TS-a is honestly **not** a boundary-signal result.
- **Weaker alternatives.** The constant is inexplicit by construction. The sharp claim is carried by TS-b, not TS-a.

### A-MARGIN-U — residual-signal margin for exact selection (TS-b, TM-b)
- **Statement (population form; v1.4 headline; canonical text `council/V14_CHANGESPEC.md` §1).** Write T = S0, s = s0. For a rival S ⊉ T, its **base** is B := S ∩ Q_n, N := S ∖ Q_n, d := |T∖B|, and k := |B∖T| + |N| (the number of added predictors).
  - Price: Pr_n(d) := max_{|D|=d} log[π(T∖D)/π(T)] + (d/2)·log(n+1). For BB(1, p) this is Σ_{k=s−d}^{s−1} price(k). For other priors the deletion refund at T need not bound the refund at T ∪ (S∖T), so the statement keeps the coded price; for any other prior, re-derive it.
  - Rival range: m̄_d := ⌈(2A+1)d⌉ + 1 (delivered `asm:margin`(b) with s replaced by d). Leakage ϑ(B, N) := 1 − R_n(B ∪ N)/R_n(B); coefficient ā(B, N) := min{1, √(2(1 − √(1 − ϑ(B, N))))}.
  - Fix η > 0 and a deterministic **accounting set** Q_n ⊇ T with log|Q_n| = o(log n). For all large n:
    - **(U1) Deletions.** R_n(T∖D) ≥ 2(1+η)·σ*²·Pr_n(|D|) for every nonempty D ⊆ T. This is κ_n ≥ 1+η, the case B = T∖D, N = ∅ of (U2a).
    - **(U2a) Bases.** R_n(B) ≥ 2(1+η)·σ*²·Pr_n(d) for every B ⊆ Q_n with B ⊉ T and |B∖T| ≤ m̄_d.
    - **(U2b) Outside nulls.** For every such B and every N ⊆ Q_n^c with 1 ≤ |N| = m and |B∖T| + m ≤ m̄_d:
      √(R_n(B ∪ N)/σ*²) ≥ √(2(1+η)·Pr_n(d)) + ā(B, N)·√(2 log C(p−s, m)).
  - Q_n is an accounting device, not an object to be found. Any such Q_n may be used; enlarging it moves rivals from (U2b) to (U2a). Leakage outside Q_n need not vanish: it is priced by ā.
  - Reading aids: √ϑ ≤ ā ≤ √(2ϑ) for ϑ ≤ 3/4. Within one base, (U2b) for every N is the same as min_N √R_n(B∪N) ≥ … + max_N ā·√(2 log C), since both extremes sit at the maximum-leakage N.
  - Special cases (stated, not separate assumptions): (i) Q_n = T, the "no proxies" case, where every null is priced by its own leakage; (ii) if max_{B,N} ϑ(B, N)·log p → 0 outside Q_n, then (U2a) with η implies (U2b) with every η′ < η for large n; (iii) ā ≡ 1, the structure-free fallback (unit-vector bound; coefficient 1, not √2).
  - Rivals with k > m̄_d need **no** signal condition: for p ≤ n^A their summed prior-plus-Occam odds are ≤ n^{−γ} for some γ > 0 (a TS-b step 2 obligation). Classes satisfy the sieve s − d + k ≤ min(K, J) and k ≤ p − s; (U2) and C-i range only over such feasible rivals.
  - **Population sufficient conditions (corollaries).** (C-i) Strong separation: min R_n(S)/[σ*² log(p∨n)] → ∞ over feasible underfits with |S∖T| ≤ m̄_s implies (U1)–(U2) with Q_n = T. (C-ii) Sparse eigenvalue plus beta-min: let φ² lower-bound λ_min(Corr(x_V)) over |V| ≤ s + m̄_s and θ_min := min_{j∈T}|β*_j|·sd(x_j)/σ*; then θ_min ≥ (1+η)(1 + √m̄_s)·√(2 log(2p√(n+1))/n)/φ implies (U1) and (U2) with ā ≡ 1. For an orthogonal design, a sufficient coordinatewise form of (U1) is β*_j²Var(x_j) ≥ 2(1+η)σ*²·log(2p√(n+1))/n for every j ∈ T; exact (U1) requires n·Σ_{j∈D} β*_j²Var(x_j) ≥ 2(1+η)σ*²·Pr_n(|D|) for each nonempty D.
- **Lemma W (bridge to the proof; low risk) [P].**
  - (W1) For S ⊇ B with positive residuals, ⟨v_S, v_B⟩ = √(R̂(S)/R̂(B)), with v_S = (I−P_S)μ/‖(I−P_S)μ‖; so ‖v_S − v_B‖ = a(ϑ̂) exactly, ϑ̂ the sample leakage.
  - (W2) On the two-sided sparse-isometry event on T ∪ B ∪ N (size ≤ s + m̄_d, relative error δ_n ≍ √(log(n∨p)/n)), ϑ̂ ≤ ϑ + 2δ_n/(1+δ_n). Because of the cap, ā(ϑ̂) ≤ ā(ϑ) + 2√δ_n.
  - (W3) **Simultaneous Gaussian bound.** Let H ≤ 2^s Σ_{b ≤ m̄_s} C(|Q_n|−s, b) = n^{o(1)} be the number of bases and l_n := log(H+1) + t_n, with t_n → ∞ and t_n = o(log n). Conditionally on X, with probability 1 − O(e^{−t_n}), simultaneously over bases and N: −⟨v_S, g⟩ ≤ √(2l_n) + ‖v_S − v_B‖·√(2[log C(p−s, m) + l_n]). By the same union bound, simultaneously, −⟨v_S, g⟩ ≤ √(2[log C(p−s, m) + l_n]) directly; take the minimum of the two bounds before applying W2, so the effective chord coefficient is capped at 1 (the uncapped chord a(ϑ̂) exceeds 1 when ϑ̂ > 3/4). The surplus over ā·√(2 log C) is o_P(√log n), and the root-scale slack absorbs it because Pr_n(d) ≳ log n for d ≥ 1.
  - **Consequence.** The population form implies the **base-indexed** conditional-width condition on a design event of probability 1 − o(1); TS-b step 3 is run per base. For fixed D each null set gives exactly one S, so the containing-model odds are summed once at the total null size k, with no multiplier of order H.
  - **Not claimed.** The population form does not imply the v1.3 class-level conditional-width condition when Q_n ≠ T: across bases, the smallest residual and the largest width can occur at different bases.
- **Refined design-conditional form (parallel sufficient condition; the v1.3 headline).** Fix an admissible M and J := ⌊s + C_s M⌋. There are fixed 0 < δ < 1, γ > 0 and t_n → ∞ such that, for all large n and every class (D, m) with D ≠ ∅, 0 ≤ m ≤ p − s, s − d + m ≤ min(K, J) and B_Dm > 0,
  √((1−δ)·min_{|N|=m} R_n(S)/σ*²) ≥ w_Dm + t_n + √(2(1+δ)·B_Dm),   B_Dm := Pr_n(d) − (m/2)·log(n/(C log p)) + γ log n,
  with **C = 1 by convention** (the multiplier of the superset step is carried in the tight remainder). B_Dm is a summed class bound, distinct from the single-rival price Pr_n(d, m). Classes with B_Dm ≤ 0 need no signal condition (containing-model credit; Neon B1, Opus B1). w_Dm(X) = E_g max_{|N|=m}(−⟨v_S, g⟩) is the one-sided conditional Gaussian width, with w_D0 = 0; use the worst case over D, a deterministic bound holding with design probability 1 − o(1), or w_Dm ≤ √(2 log C(p−s0, m)) outright, and state the condition on a design event of probability 1 − o(1). TS-b also holds under this form (§3.3, step 3′). The combinatorial width and the squared form R_n(S) ≥ 2(1+η)²(√d+√m)²σ*²·price_n are worst-case (factor-proxy) forms. The multiplicative form √R/σ ≥ (1+η)[w + √(2B)] + a_n is equivalent after choosing δ small relative to η and t_n ≤ a_n/3.
- **Used in.** TS-b steps 1–3 (step 3 per base via Lemma W, step 4 for the transfer). The converse (with A-NEC on T) shows the constant 2 is sharp for deletions.
- **Defence.**
  - (a) Same object, a projection residual of the true mean:
    - NH14 Cond. 4.4, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n), over models of size < K|t| that miss a true
      predictor (PN A2). **Comparison, not dominance:** NH14 multiply by |t| for every such model and use constant 5(1+δ);
      ours is per missed predictor with constant 2(1+η) for deletions, but adds the leakage-priced term for nulls outside Q_n and
      works over a different model range and prior. Neither condition contains the other uniformly (Astra R2).
    - Luo & Chen Consistency Condition, arXiv v1 p. 7: Δ_n(s)/(p₀ ln p) → ∞ (PN A4). Ours needs a fixed ratio for deletions,
      not → ∞; corollary C-i is exactly this diverging-ratio form.
    - Rossell 2022's non-centrality λ_tm, arXiv v7 p. 10 (PN D13).
    - **Genre.** Corollary C-ii is the standard sparse-eigenvalue plus beta-min pair; (U2b) adds only the projection-geometry coefficient ā, a function of a population variance share (no design family).
  - (a) Necessity of the log p order: Wainwright 2009 Thm 2, arXiv v2 p. 4 (Gaussian design, averaged error; PN B5).
    Fletcher–Rangan–Goyal Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor (constant derived by C2; PN B6).
  - (b) **Deletion part (m = 0): S1 brackets κ = 1.** κ_multi (= κ_pop on S1, since κ_swap = κ_del there) is 0.64–0.70 at
    SNR 1 (0/100 exact in every cell) and 2.54–2.80 at SNR 2 (92–96/100). Multi-deletions bind on S1 in all 16 settings
    (D1 E1). The data κ uses d·price(s0−1) (P1 convention, log((2p−1−s0)/s0) + ½log(n+1), one off from the exact
    price(s0−1) = log((2p−s0)/s0) + ½log(n+1)); the theorem's κ_n uses Pr_n(d) = Σ adjacent prices over all 1,023
    nonempty D: the exact κ_n is 0.626–0.693 at SNR 1 and 2.505–2.771 at SNR 2, 1.1–1.7% below the restricted data proxy, with
    the minimum at d = 6 (p = 500) or d = 3 (p = 5,000) (Sol R2; reproduced by the Lead). The bracket around 1 is unchanged. This brackets a finite-sample
    transition at this scale; it does not test the full A-MARGIN-U inequality.
  - (b) **U2a check on S1** (`.rc_tmp/lead_v14/u2a_check.py`). Over all 1,023 deletions D, with B = (T∖D) plus at most two of the five tested proxies (the five nulls nearest S0), the minimum of R_n(B)/(2σ²Pr_n(d)) equals the exact κ_n: 2.505–2.771 at SNR 2 and 0.626–0.693 at SNR 1. The binding D retain x_10, which screens every null.
  - (b) **Outside leakage on S1.** For the endpoint deletion (retained true predictors on one side), a single outside null at distance k beyond the deleted endpoint, with the intervening nulls not in the base, leaks ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}) (0.265, 0.087, 0.030, 0.011 at ρ = 0.6 for k = 1–4). Special case (ii) needs the uniform bound max ϑ·log p → 0, which L_n → ∞ alone does not give: with Q_n = T plus the L_n nearest nulls, the worst outside leakage over d ≤ 3, up to 2 inside proxies and up to 3 outside nulls is ≈ 0.25ρ^{2L_n} (unit coefficients; `.rc_tmp/lead_v14/leak_uniform.py`), so choosing L_n with ρ^{2L_n}·log p → 0 (L_n of order log log p plus a slowly diverging term, keeping log|Q_n| = o(log n)) puts the S1 sequence in special case (ii). The fallback ā ≡ 1 alone: on the evaluated classes (d ≤ 3, selected D for d ≥ 2; m ≤ 2 at p = 500, m = 1 at p = 5,000) at η = 0, it fails at SNR 2 (minimum surplus −0.692 at d = 1, m = 1; −2.008 at m = 2) and holds at SNR 3 (minimum 1.412, d = 1, m = 2); m up to m̄_d is not evaluated (population computation on `tables/e9b_width_ext_s1.tsv` with the combinatorial width √(2 log C(p−s, m))).
  - (b) **E9 and E9b: diagnostics of the refined design-conditional form only** (`scripts/e9_width_mc.py`, `scripts/e9b_width_mc_ext.py`, `tables/e9_width_s1.tsv`, `tables/e9b_width_ext_s1.tsv`; 4 simulated S1 designs × 300 Gaussian draws, no fits). They estimate the zero-slack surplus √(min_N R_n/σ²) − w̄_Dm − √(2[B_Dm]₊) with the four-design mean width w̄_Dm, at δ = γ = t_n = 0. Four designs at zero slack establish no 1 − o(1) design event and do not test the positive-slack inequality. E9b's 3 D per (cell, d, m) are **selected examples**, chosen by population residual. Mean widths are 0.10–0.47 (m = 1) and 0.22–0.59 (m = 2); E9b's range is 0.142–0.426, against the combinatorial 3.52–4.13 (m = 1) and 4.84 (m = 2).
    - E9 (all ten single deletions, C = 1): m = 1 in all four S1 cells and m = 2 in the two p = 500 cells; minimum surplus 3.2946 at SNR 2 and 6.6961 at SNR 3 (`tables/e9_width_s1.tsv`).
    - E9b (rerun with the raw-centred mean μ as in harness/generate.R; the v1 coded-mean table is kept as `tables/e9b_width_ext_s1_v1_codedmu.tsv`; d = 1 identical, d = 2, 3 change by ≤ 0.0015). Exact minimum surplus at SNR 2, for C = 1 / C = 121 (a sensitivity setting) / no credit: d = 1 3.2896 / 2.3862 / 2.4889; d = 2 4.2658 / 3.6228 / 3.6867; d = 3 4.2987 / 3.8030 / 3.7921. At SNR 3: d = 1 6.7098 / 5.8065 / 5.9091; d = 2 9.1027 / 8.4597 / 8.5237; d = 3 9.8397 / 9.3440 / 9.3332.
    - **Not evaluated:** m = 2 at p = 5,000; m ≥ 3; d ≥ 4 and the non-binding D for d ≥ 2; designs other than S1's AR(1).
    - The population minimum over N searched the 40 nulls nearest S0. By the Gaussian AR(1) Markov property this contains an exact minimiser: if max D < 10 the retained x_10 screens every null, and if 10 ∈ D the nearest null x_11 screens the farther ones (Sol R2). The width itself ranges over all nulls.
  - (b) **Deletion check on the data.** P1's min t² > 2·price has sensitivity 1.000 on S1 and 0.985 on S2 (sample). When it
    fails, recovery is 0/800 on S1 and 9/10,666 = 0.00084 on S2 (sample check; 9/11,466 pooled); the population κ_del ≤ 1
    row gives 0 on both. Consistent with the converse; not an exact necessity statement.
- **Weaker alternatives evaluated.**
  - The memo's uniform "2·d·price" for every rival: rejected (D3); OPEN under p ≤ n^A.
  - Λ(S) → ∞ with multiplicity m·log p: neither sufficient nor necessary (Fable Q1(1)). On the data it ranks worse than
    κ_del (AUC 0.967 vs 0.980 on S2; D1 E1).
  - The delivered c_id > c1(s0, A) with a large explicit constant: replaced, because the threshold is now 2(1+δ) for
    deletions and the converse shows nothing below 2 works for deletions.
  - MARGIN\* (2+η with a leakage set, Fable Q1(3c)): **superseded** by the population form ((U2a) charges every base inside Q_n the full deletion price, whereas M1 let inside proxies pay for their entry, as in the weaker-variant remark below; the leakage-priced (U2b) replaces M2).
  - **Weaker variant, not adopted: proxies pay their own price.** (U2a) could be weakened to the single-rival price [log π(B)/π(T) + ((s−|B|)/2)log(n+1)]₊ for |B| < s, to R_n(B)/(σ*²(1+log|Q_n|)) → ∞ for |B| = s, and to no condition for |B| > s. This needs step 2 on the bases T ∪ (B∖T), which is not written. The headline (U2a) is therefore conservative: by a factor (1+ρ²)/(1−ρ²) on the signal when both AR(1) neighbours of an isolated true predictor are proxies, and similarly for block designs (worked cases, DOSSIER).
  - γ = 0: the rate display would contain n⁰; consistency would need a separate o_P(1) argument retaining a diverging surplus.
    Not adopted for the headline.

### A-MIS — the working residual (TM-a, TM-b)
- **A-MIS(iii), headline.** The candidate set C is fixed before the analysis sample is drawn, or chosen on independent data (Sol R2), and Σ_CC is nonsingular (full candidate rank, so β^C = Σ_CC⁻¹Cov(x_C, y) is unique; the sparse floor A-NEC alone does not give this, e.g. Σ_CC ∝ I − 11ᵀ/p_C). The working residual u = y − α_C − x_Cᵀβ^C is independent of x_C and u ~ N(0, σ_C²). The other TD/TS-b assumptions are imposed on (x_C, β^C, σ_C²). The misspecification is then *omission relative to the full regression* only: conditional on x_C the data are exactly Gaussian linear.
  - **Primitive form (equivalent, by Cramér's decomposition).** For the omitted true predictors O, x_Oᵀβ*_O = a + x_Cᵀγ + e with e ~ N(0, τ²) independent of x_C, τ² ≥ 0. Then β^C = β*_C + γ and σ_C² = σ*² + τ². Uniqueness comes from a sparse representation together with A-NEC; full rank is a sufficient version.
  - All TM statements are **conditional on each admissible C**, with the candidate dimension p_C in the cap, price, window and prior. An unconditional statement needs common constants and a common validity threshold over admissible candidate sets, and then adds + P(C inadmissible), which vanishes identically under almost-sure admissibility; the a.s. corollary needs summable exception probabilities.
- **Used in.** It makes the candidate-only data an instance of A-GL, so TD and TS-b apply verbatim with f₀ in place of f*.
- **Defence.**
  - (a) SL Thm 4/Cor 2, p. 957, use the same f₀ (17)/(19). Rossell 2022 Prop. 6, arXiv v7 pp. 16–17, is a fixed-design misspecified-mean analogue (omitted W; PN D13). Jointly Gaussian (x_C, x_omitted) satisfies (iii) (supplement `ex:omitted`).
  - (b) **In-sample illustration only.** E[σ²|y, MPM]/σ_C² has median 0.99 on S1 and 0.84–0.98 on S2 (D1 E7), but C = MPM is selected on the same, well-specified data; this illustrates the residual-energy calculation and does not test independence, Gaussianity or concentration at a prespecified-C pseudo-truth. Adjacent-null shares among failed fits are selected-group summaries (0.1–1.6%, up to 2.97% in the S2 bt1, ρ = 0.7 cell) and say nothing about hidden columns.
- **Weaker alternatives evaluated.**
  - (i′) Independent non-Gaussian residual: a *suggested* route with a cap and a variance-proxy budget, neither shown necessary. Remark (Fable Q6(3c)).
  - (ii) Moments only, E[x_C u] = 0: in high dimension the Grünwald–van Ommen mechanism applies heuristically, and nulls gain ϱ·χ²₁; Fable's budget (ϱ̄−1)·log p < ½ log n is a heuristic sufficient budget, not an established iff (Astra R2). Remark only. The Grünwald–van Ommen setting is heteroscedastic "in-liers" with a homoscedastic working model, and it is empirical only (arXiv v3 pp. 4–5; PN D12); it does not establish the proposed dimension threshold here.
  - Fixed p_C with moments only: this *is* adopted, as TM-a0.
  - Full candidate rank (Sol R2): it can be relaxed. Density transfer needs a sparse representation of the L² projection, and selection transfer needs its support identified on the localised sieve, where A-NEC separates distinct bounded-size representations. Recorded; the fixed-rank form stays the sufficient headline.

### A-SPARSE-C — sparse pseudo-true support (TM-a, TM-b)
- **Statement.** |supp β^C| ≤ s_C with s_C fixed (the candidate-problem version of A-SPARSE).
- **Used in.** TD and TS-b applied to the candidate problem (§3.5): the window, the deletion directions and the superset mass, with s_C in place of s.
- **Defence.**
  - (a) SL Thm 4/Cor 2 take a fixed candidate subset, so the pseudo-true support is automatically bounded there (p. 957).
  - (c) Holds under Markov-type separation: in a Gaussian AR(1) (a Markov chain), the nearest retained candidates on each side separate an omitted predictor from all other candidates, so it projects on at most two of them. Local covariance dependence alone need not give a sparse regression. Fails under pervasive factors, where the projection of an omitted predictor is dense.
- **Weaker alternatives.** Approximate pseudo-true sparsity via TD-A (a change of measure to a sparse surrogate); not adopted.

### A-MOM — moments for TM-a0
- **Statement.** **One fixed i.i.d. law** along a nested sample sequence (not an n-dependent truth: with β_n = 1/n even fixed-p support selection fails); p_C ≥ 2 fixed (the coded posterior is undefined with fewer than two retained predictors; such data sets, and a constant sample response or column, are counted in the exceptional event, which is eventually empty a.s. since nonconstant columns and response have positive sample variance eventually); E‖x_C‖² < ∞, E y² < ∞; σ_C² = E u² > 0; Σ_CC nonsingular; the coded, fixed BB(1, p_C) prior, eventually untruncated (K = p_C once n ≥ 2p_C); f₀ for a discrete y is defined by expected Gaussian log score. Second moments alone give **inclusion** of the pseudo-true support (TM-a0-inc, the direct counterpart of SL Cor 2). For exact support selection (exclusion), add the mixed second moments of the scores E[Z_j² u²] < ∞, Z = (1, x_Cᵀ)ᵀ (not marginal fourth moments). TM-a0 lies outside A-GL.
- **Defence.** (a) For density consistency: SL Condition 4, p. 957, with "only a fixed number of possible models" in their proof, SLs p. 7 (SL assume a Gaussian parent model and positive priors; Condition 4 alone does not state the response/score moments). (c) For the exact-support extension: the SLLN/LIL argument of §3.4 (E[Z_j²u²] < ∞ is our addition).

---

## 3. Proof-path sketches (no proof claimed; each step names the assumptions it uses)

### 3.1 TD (delivered) and its extensions
**TD as delivered** is proved and independently checked; we only record where each assumption enters.
- A-GL gives exact marginals and the Fubini identity for the normalised fixed-endpoint contrast density (§2 A-GL).
- Fix M first. A-SUBG + A-NEC on the coarse window q_n(M) give the isometry; the exp(O(log² n)) coarse sets are absorbed by
  an isometry failure probability exp(−cn).
- prop:dist(i) localises to |S| ≤ J = ⌊s + C_s M⌋ by fractional Bayes-factor moments (needs A-DIM, A-NEC, A-BS); the
  O(M log n) testing budget is then spent on the localised sieve.
- A-BS gives the prior-mass/denominator lower bound (with the n^{−1/2} variance-integration factor).
- Undefined posteriors (fewer than two retained predictors, constant response) are counted in the exceptional event (or6 l.116).

**TD-as.** P*(E_n) ≤ n^{−c_H M}, summable when c_H M > 1, so Borel–Cantelli applies. [both advisors]

**TD′ (conjecture, HIGH proof risk at the proposed rate) [Fable Q3; refuted as a proof route by Astra R2 Q1].**
1. **Coarse size cutoff by Fubini** (valid). Conditional on X, after passing to raw centred contrasts and sandwiching the
   outcome-dependent IG rate b₀s_y² between fixed endpoints, E*[m^c_{S,b}/f*] = 1 for the normalised fixed-endpoint
   density. Markov on the numerator plus separate control of the denominator event (lower bound ≍ D_T^{−1/2}n^{−1/2}e^{−Λ}
   in noise units) gives the coarse cutoff s0 + ⌈[s0 log(2p) + (s0+2)log(n+1)/2 + 3t]/log 2⌉ (as in the delivered W3-DIST
   lemma X4(a)). This uses the BB(1,p) 2^{−k} size tail.
2. **Sample control on q_n-sets.** Isometry under A-SUBG holds when q_n·log p ≤ c·n with q_n ≍ min{p, (s+1)M log₂(p√n)}, which A-DIM′ gives (the +1 covers s = 0).
3. **Tests and entropy — this step FAILS as stated.** At log p = n^{1/3}, log C(p, q_n) ≍ n^{2/3} while the testing budget is
   nε_n² = M log(p∨n) ≍ n^{1/3}. The delivered proof avoids this at polynomial p by localising to s0 + O(t/log n) through
   fractional Bayes-factor moments (X4(b,c)), whose factor p^{1−λ}n^{−λ/2} is uncontrolled for super-polynomial p.
- **What a proof would need:** localisation at a testing-compatible size (≈ t/log p), or a prior-weighted/direct
  predictive-risk bound that avoids paying full entropy. A cap c·n/log p fixes step 2, not step 3. A fixed cap is easier.

**TD-A (optional) [to audit].** Requires a change of measure for the **entire** data law, not one-observation Hellinger
closeness: for a Gaussian mean perturbation r(x), E_sur[(dP_truth/dP_sur)²] = (E exp(r(x)²/σ²))^n; control it by
exp(O(c₀t)) with c₀ small and use Cauchy–Schwarz on the exceptional events (intercept/mean accounted for). Then apply TD.

### 3.2 TS-a
1. **Conversion inequality** (A-SUBG). For every f supported on S ∌ j with free (β_S, σ_S), d_H²(f, f*) ≥ c_L·min{1,
   R_n(S)/(nσ*²)}. Gaussian x, exact: maximising the squared affinity gives 2στ/(σ²+τ²+R/(2n)), optimised at
   τ² = σ² + R/(2n), so d_H² ≥ 1 − (1 + R/(2nσ²))^{−1/4} (Fable Q2, confirmed by Astra R2). Sub-Gaussian x: relative SUBG gives
   E V⁴ ≤ C_L(E V²)² for the affine mean contrast V, so P(V² ≥ E V²/2) ≥ 1/(4C_L), and the Gaussian conditional affinity
   converts this (Astra R2 Q4).
2. **Effective sieve.** Posterior sizes are ≤ J = ⌊s + C_s M⌋ outside the prop:dist(i) tail, so only feasible S with
   |S| ≤ min(K, J) matter, and then |S ∪ S0| ≤ min(p, s0 + J) ≤ q_n for large n (inside the SUBG window). **Uses the TD assumptions.**
3. **Margin.** By A-MARGIN-H at the fixed size k = J (the diverging ratio exceeds any C_L·M eventually; or directly by its fixed-level form), c_L·R/(nσ²) > ε_n², so {S ∌ j, |S| ≤ J} lies outside the TD ball. Add the
   posterior large-size tail to the contraction tail: Π(j ∉ S | D_n) ≤ 2n^{−c_H M} ≤ n^{−c′_H M} on the TD event, for any
   fixed c′_H < c_H and large n. **A-MARGIN-H supplies the lower bound on R; SUBG alone does not** (Gaussian duplicates
   have R = 0).
4. The a.s. version (posterior tails, fixed truth) follows from Borel–Cantelli when c′_H M > 1.
5. **Per predictor, then jointly.** Steps 1–3 use only j's own margin, so TS-a(a) holds for each such j whatever the other signals do; TS-a(b) is the union over the s0 predictors.

### 3.3 TS-b (steps 1–4: same structure in Astra R1 Q1 and Fable Q1(3a)–(3c); details per Astra R2 Q2; v1.4 per-base step 3)
Let T = S0, λ̂_S = R̂(S)/σ² (R̂ is the sample residual signal; raw centred design with raw coefficients, or
equivalently the standardised design with sample-scaled coefficients in raw response units). **M is fixed independently
of n**, J = ⌊s + C_s M⌋ is a fixed integer, and work is on the bounded-size event |S| ≤ J (prop:dist(i), under A-BS);
empty classes are omitted. Rivals are indexed by their base B = S ∩ Q_n and N = S∖Q_n, with d = |T∖B| and k = |B∖T| + |N|, on the sieve s − d + k ≤ min(K, J), k ≤ p − s. The coded determinant is det[(n+1)G+I]/det[G+I]. Under A-MARGIN-U (population form) the slack η is fixed; choose δ, γ > 0 small relative to η, which is possible on the root scale because Pr_n(d) ≳ log n for d ≥ 1.
1. **Pure deletions** (B = T∖D, N = ∅; 2^{s0} − 1 rivals; also the k = 0 case of step 3).
   - (RSS_S − RSS_T)/σ² = (√λ̂_D + z_D)² + χ²_{d−1}; max_D |z_D| ≤ t_n with high probability (finitely many directions).
   - The deleted prior × determinant refund against T is ≤ exp(Pr_n(d)) for every design (monotone adjacent deletion
     price + Cauchy interlacing). **No floor is needed for sufficiency.**
   - Odds → 0 at rate n^{−γ} when √((1−δ)R_n/σ²) ≥ t_n + √(2(1+δ)[Pr_n(d) + γ log n]), which (U1) gives for large n. **Uses A-MARGIN-U (U1).
     All D are needed, not only singletons.**
2. **Pure supersets** (d = 0) **and large added sets** (k > m̄_d). For U = T ∪ N, RSS_U/RSS_T ~ Beta((n−1−s0−m)/2, m/2) conditional on full rank (A-GL). The likelihood-ratio
   tail is Pareto-like with infinite mean, so Markov is applied to **truncated** sums (Sol R1 sketch): truncate
   −(n/2)log(Beta) at c_m log p with c_m large; the Beta density gives an integrated truncated exponential moment
   O((log p)^{m/2}), and the excess over the truncation has a union tail over the C(p−s0, m) subsets; multiply by the prior ×
   Occam factor O(p^{−m}n^{−m/2}) (A-NEC gives Q_U − RSS_U = O_P(σ²) uniformly, since in-span shrinkage eigenvalues are O(1/n)
   and the centred response energy is O_P(nσ²)). This gives the containing-model sum O_P((C log p/n)^{m/2}) per m, with **C = 1 by
   convention** and the multiplier carried in the tight remainder; at bounded p use tightness directly. Because M is fixed, J is a fixed integer and
   simultaneous control over m ≤ J is a **finite** union and sum. One-null mass is O_P((s0+1)√(log p/n)) (the order of the
   `rem:sharp`(b) lower bound, which is for witness designs). **Obligation (k > m̄_d):** for p ≤ n^A the summed prior-plus-Occam odds of rivals with more than m̄_d added predictors are ≤ n^{−γ} for some γ > 0, with no signal condition; this is to be written out. **Uses A-NEC (full Occam factor) and A-DIM.** If M or J were
   allowed to grow, a genuinely uniform summation would be an additional obligation.
3. **Mixed rivals, per base** (d ≥ 1, k ≥ 1; coded-likelihood form per Sol R2, accounting per Opus/Neon R2 and the v1.4 senior review). Fix a base B ⊆ Q_n, B ⊉ T, and the outside null size m. For each N ⊆ Q_n^c with |N| = m, compare S = B ∪ N termwise against its containing model U_N := T ∪ (B∖T) ∪ N (|U_N| ≤ min(p, s0 + J), inside the sparse window for large n).
   - **Width (Lemma W).** On the W3 event, simultaneously over bases and N, −⟨v_S, g⟩ ≤ min{√(2[log C(p−s, m) + l_n]), √(2l_n) + a(ϑ̂)·√(2[log C(p−s, m) + l_n])} (W1 and the direct bound of W3), so the effective coefficient is min{1, a(ϑ̂)} ≤ ā(ϑ) + 2√δ_n on the isometry event (W2). With (U2b) (or (U2a) when N = ∅) and the R-transfer (step 4), W := (√λ̂_S − width)₊² ≥ 2(1+δ)[Pr_n(d) + γ log n] with probability → 1, simultaneously over the H = n^{o(1)} bases.
   - **Odds.** Using Q_S ≥ RSS_S (no uniform upper ridge bound on arbitrary underfits is needed), the uniform ridge bound
     Q_U − RSS_U = O_P(σ²) on U_N (A-NEC), RSS_{U_N} ≤ RSS_{T∪(B∖T)}, and the deleted prior × refund against U_N ≤ exp(Pr_n(d)) (the BB(1, p)
     price is decreasing in model size):
       log Σ_{|N|=m} π(S | y)/π(T | y) ≤ Pr_n(d) − (n/2 + a₀)·log(1 + W/V_n) + log Σ_{|N|=m} π(U_N | y)/π(T | y) + O_P(1),  V_n := (RSS_T + 2b₀s_y²)/σ² = n(1 + o_P(1)).
     For fixed D each null set gives exactly one S, so the containing-model odds are summed **once** at the total null size k (step 2), with no multiplier of order H; that sum is O_P(1).
   - Since log(1 + W/V_n) increases in W, evaluate it at W = 2(1+δ)[Pr_n(d) + γ log n] = O(log n): (n/2 + a₀)log(1 + W/V_n) ≥ (1+δ)[Pr_n(d) + γ log n](1 − o_P(1)), so each base contributes O_P(n^{−γ}), and the H = n^{o(1)} bases together O_P(n^{−γ+o(1)}).
   The full log-likelihood term is kept, so nothing is linearised at the actual residual (which can be of order n). The
   uniform lower bound on RSS_U needed for the tight remainder holds on the superset truncation event of step 2. The O_P(1) collects the Q_U − RSS_U and IG-rate terms. **Uses A-MARGIN-U ((U2a), (U2b)), Lemma W and A-NEC.** The width term is needed: in a factor-proxy design a single swap beats S0 unless
   R ≥ 2(1+ρ)² log p (Fable [P][N]); this shows necessity at one (d, m), not optimality of every constant.
3′. **Refined design-conditional form (parallel route).** Under the refined form of §2 (classes (D, m), C = 1), define H_Dm := B_Dm − γ log n and, on the event max_N(−⟨v_S, g⟩) ≤ w_Dm + t_n, W := (min_{|N|=m} √λ̂_S − w_Dm − t_n)₊². The v1.3 bound log Σ_{|N|=m} π(S | y)/π(T | y) ≤ H_Dm − (n/2 + a₀)·log(1 + W/V_n) + O_P(1) applies: classes with B_Dm ≤ 0 take W = 0, and classes with B_Dm > 0 get W ≥ 2(1+δ)B_Dm, so each class mass is O_P(n^{−γ}).
4. **R-transfer.** (1−δ)R_n(S) ≤ R̂(S) ≤ (1+δ)R_n(S) uniformly over sets with |S ∪ S0| ≤ min(p, s0+J) ≤ q_n (large n, fixed M), from a two-sided sparse isometry under A-SUBG
   when (s0+J) log p ≤ cδ²n. **Uses A-SUBG and A-DIM; no eigenvalue floor.** (Fixed T sets: relative transfer O_P(n^{−1/2}).)
5. **Large models** (|S| > J): handled by the size lemma prop:dist(i) (Fubini coarse cutoff + fractional-moment
   localisation), proved under A-BS and A-DIM.
6. **Rate.** 1 − π(S0|y) = O_P((s0+1)√(log p/n) + n^{−γ} + n^{−c_H M}) with γ > 0. PIP and HPM/MPM follow by `lem:summaries`.
   It is an asymptotic statement: at S1's (n, p) the term (s0+1)√(log p/n) is 0.87–1.44, so the display is not informative at those sizes (Opus R1).

**Linearisation.** The TS-b bound (step 3) keeps (n/2 + a₀)log(1 + W/V_n) and uses monotonicity at W = O(log n), where (n/2)log(1 + W/n) = W/2 − O(W²/n); for fixed δ, log p = o(n) suffices, and no linearisation at large residuals is needed (Sol R2). When R_n is comparable to n
(fixed signals) the gain is ≥ c·n ≫ Pr_n and the margin holds trivially, so the asymptotic statement can use R/2. Finite-n
diagnostics use the saturating gain (n/2)log(1 + R/(nσ²)) (D1 E1: P(exact) = ½ at κ_adj_full ≈ 1.0–1.5 on both suites;
post hoc).

**Converse [P, Fable Q2(3); conditions per Astra R2 Q3; minimal set per the v1.4 senior review].** Assume only A-GL, sparse isometry and **A-NEC on T** (giving the
two-sided determinant refund d·log(n+1)/2 + O(1)), and A-BS for the ridge term; Pr_n(1) = O(log n) holds under A-DIM. The forward margin is not assumed. For the minimising D, with subthreshold
R_n/σ² = O(log n), Q − RSS = O_P(σ²), relative sample transfer and the noncentral χ²_d increment give
log(F_{T∖D}/F_T) = Pr_n(d) − R_n/(2σ²) + o_P(Pr_n(d)) → +∞ when limsup κ_n < 1, so π(S0|y) → 0. At a single-deletion
boundary √R_j/σ − √(2Pr_n(1)) → c, the probability that this rival beats T tends to Φ(−c), hence
**liminf P(π(S0|y) ≤ ½) ≥ Φ(−c)** (equality would need control of all other odds). Boundary remainder: log odds = Pr_n(1) − (√λ̂ + Z)²/2 + O_P(1) at λ = O(log n), with V_n/n = 1 + O_P(n^{−1/2}) and λ̂ − λ = o_P(1) by fixed-support relative transfer (relative error O_P(n^{−1/2}) on T, from A-DIM and relative A-SUBG on T); the O_P(1) remainder suffices because the leading fluctuation is √(2Pr_n)·(c+Z).

**Finite-n diagnostic (NOT a proposition; Astra R2 Q3).** In the idealised χ² score approximation, the expected number of
one-null extensions beating S0 is E K₁ ≈ (p−s0)·2Φ(−√L) ≈ (s0+1)/√(2πL(n+1)), L = 2log((2p−s0−1)/(s0+1)) + log(n+1).
At S1's (n, p) the displayed formula gives 0.031–0.050 ((p−s0)·2Φ(−√L) gives 0.029–0.047; Fable's exact-Beta tail gives
0.033–0.056, FABLE_R1 Q1(3f)), the same order as the observed S1 shortfall (2–8% at SNR ≥ 2); 40 of 41 S1 failures at
SNR ≥ 2 are supersets, 39 with exactly one added null (D1 E7). E K₁ is a **mode-type diagnostic** (it counts rivals beating T in exact score, an HPM event; MPM failure is a separate event; Sol R2): it scales as
(s0+1)/√(nL), a factor ≍ L below the posterior-mass rate term (s0+1)√(L/n), and the two measure different events, so it
does **not** "match the order" of the TS-b rate (Opus R1). This is **consistent with** the superset term being the main
S1 failure mode at SNR ≥ 2; it is not a proved ceiling or lower bound on success (P(K₁ ≥ 1) ≤ E K₁ bounds one failure
type only; correlated nulls, swaps, higher-order rivals, ridge/IG terms and the HPM/MPM/sampler distinction are not
controlled by it).

### 3.4 TM-a0 [P, Fable Q6(3a); confirmed with fixes by Astra R2 Q4]
One fixed i.i.d. law; p_C ≥ 2; the fixed BB(1, p_C) prior. "Raw units with an intercept" means the coded centring (plug-in ȳ, x̄; no intercept parameter with a prior), with draws mapped back by β_j = s_y b_j/s_{x_j}, σ² = s_y² v; Z = (1, x_Cᵀ)ᵀ.
1. There are 2^{p_C} models. RSS_S/n → σ_S² := min_b E(y − Z_Sᵀb)² a.s. (SLLN); Q_S − RSS_S = O(1) a.s. eventually;
   b₀s_y² = O(1); log D_S = |S|·log(n+1) + O(1). **Uses A-MOM.**
2. Models missing supp β^C have σ_S² > σ_C² and lose (n/2)log(σ_S²/σ_C²) + o(n).
3. Density consistency: each of the finitely many containing models has consistent fitted parameters and a concentrating
   conditional posterior, so Hellinger convergence to f₀ a.s. follows **even without** the score moments (their relative
   masses need not converge).
4. Exact support: E[Zu] = 0 and finite coordinate score variances give ‖Σ_i Z_i u_i‖ = O_a.s.(√(n log log n)) (LIL); the
   residualised Gram inverse is O_a.s.(1/n); so the extra fitted sum of squares is O_a.s.(log log n), against (m/2)log n.
   **Uses E[Z_j²u²] < ∞.**
5. **TM-a0-inc** uses steps 1–2 only: full rank and finitely many underfits give a positive risk gap min_S (σ_S² − σ_C²) > 0 over S ⊉ S0^C, which the SLLN turns into a loss of order n against the O(log n) Occam and prior terms, so Π(S ⊇ S0^C | data) → 1 a.s. under second moments only.

### 3.5 TM-a, TM-b
Under A-MIS(iii) and A-SPARSE-C, and **conditional on each admissible C** (candidate dimension p_C in the cap, price, window and prior), the candidate-only data satisfy A-GL with parameters (α_C, β^C, σ_C²). Apply TD (3.1, with TD's M-window; a.s. corollary for posterior tails) and TS-b (3.3) verbatim, with f₀ in place of f* and A-MARGIN-U in σ_C² units on μ_C = X_Cβ^C. C must be fixed before the analysis sample is drawn, or selected on independent data; selecting C from the same design before seeing y is not enough for the i.i.d. transfer without a further uniform or conditional argument (Sol R2). TM-b assumes a nonempty pseudo-support S0^C ≠ ∅ (the converse needs it; the forward steps would also go through with S0^C = ∅, where the deletion and mixed classes are empty, but that case is not claimed). The delivered `thm:omitted` is a **previously delivered analogue** (Gaussian rows, a fixed floor on its own window, diverging per-coefficient signal, an expectation bound), not a special case (Neon R2, Sol R2).

---

## 4. Anti-stringency ledger (each restrictive v3.1.1 assumption → weaker alternative → verdict)

| # | v3.1.1 assumption | why too strong | weaker alternative evaluated (with Fable/Astra) | verdict |
|---|---|---|---|---|
| 1 | c_id > c1(s0, A), an explicit constant (`asm:margin`) | large proof constant. S1 recovers at κ ≈ 2.5–2.8 (D1), far below c1 | A-MARGIN-U with constant 2(1+η) for deletions, plus the leakage-priced term for added nulls. The converse (with A-NEC on T) shows 2 is sharp for deletions | **adopted** |
| 2 | FSb: fixed b_lo ≤ \|β\| | S1 has β ∝ √(log p/n), so FSb is false as a sequence (D1 E4) | κ_n framing over triangular arrays | **adopted** |
| 3 | p ≤ n^A | excludes exponential p, which SL cover (Cor 1) | DIM′ (log p)² = o(n) (Fable); log p = o(n) with a cap (A-DIM″) | **conjecture TD′, high proof risk** (Astra R2: the testing step fails at log p = n^{1/3}); a cap fixes isometry, not testing. p ≤ n^A stays for released statements |
| 4 | EF: sample sparse eigenvalue floor (`thm:post-fixed`) | vacuous on S2: greedy floor 1e−5 to 2e−4 at m2 (D1 E5); SL call (22) "hardly satisfied" | population A-NEC (c_ψ/n) plus the A-SUBG isometry | **adopted** (sample floors demoted to a remark) |
| 5 | EFS / FLOOR-S0: fixed population floor | unnecessary: R_n(S0∖{j}) = nβ_j²Var(x_j \| rest) already enters the margin | drop it (both advisors) | **adopted** |
| 6 | A-BS per coordinate | "why bounded signals?" | A-BS′ aggregate energy | **recorded, not adopted** until the size lemma prop:dist(i) is re-proved under it (Astra R2) |
| 7 | memo MARGIN (uniform 2·d·price) | actually too *weak* in one direction (proxy counterexample) and too strong in another (charges d·price to swaps) | MARGIN-U; v1.4 population form (MARGIN\* superseded) | **replaced** by A-MARGIN-U (population form) |
| 8 | s0 fixed | — | growth remark: s0²·log p = o(n) (heuristic) | remark |
| 9 | Gaussian residual for TM | excludes non-Gaussian misspecification | (i′) with a cap; (ii) with a budget | remarks; TM-a0 covers moments-only at fixed p_C |
| 10 | SL Condition 3 as a separate assumption | its role is a lower bound on residual signal | A-MARGIN-H (lower bound on R) + the SUBG conversion inequality (SUBG alone does **not** imply it) | **replaced by A-MARGIN-H** |
| 11 | A-MARGIN-U over every m ≤ J | stronger than the proof path needs | v1.4: rivals with k > m̄_d need no signal (summed prior-plus-Occam odds); the refined form keeps the v1.3 restriction to B_Dm > 0 (council R1) | **adopted** |
| 12 | A-MARGIN-H over \|S\| ≤ q_n | stronger than needed and outside the SUBG window at \|S\| = q_n | v1.4: diverging ratio for every fixed size k; fixed-level remark on \|S\| ≤ min(K, J) | **adopted** |

---

## 5. Engineering sensitivity (corrected; supersedes TH_PREP §3 on the size prior)

**Engine decision (HQ, SMC-PERF closed, memo 1b319090).** v3.1.1, g = n, truncated BB(1, p) and MPM are **confirmed**. Fix E (output-only) and C1 (compute-only) do not touch the theorems. Proof writing and Lean stay on hold. The table below is therefore a contingency note only; no row is triggered.

Per-model prior odds of adding a variable at size k under BB(1, b): (k+1)/(p−k−1+b). The size-marginal ratio is (p−k)/(p−k−1+b).

| change | form invariant? | what moves | new condition |
|---|---|---|---|
| g (slab scale) | yes | price_g(k) = log[(2p−1−k)/(k+1)] + ½log(1+g). The TS-b threshold moves with it. Superset mass ≍ (s0+1)√(log p/g). The misspecification budget ϱ̄ < 1 + log(1+g)/(2 log p) | heuristic: s0²·log p = o(g). Small g also enlarges the slab loss O(n/g), so the nominal price alone does not describe a g change (Astra R2). Fixed g can prevent selection. g = n → c·n shifts the price by ½log[(1+cn)/(1+n)] at fixed k |
| g = max(n, p²) | yes | when p² ≥ n, price ≈ 2 log p at fixed small k and growing p: more signal needed, fewer supersets; when p² < n, g = n and the price is unchanged | none |
| g = 4n or 9n (Engineering trials) | yes | the superset margin ω = price − log p rises by ½log g, so S1 superset losses fall. The empty-model margin on S2 falls | none. Matches perf/JOINT_PLAN: S1 losses fixed, 92–170 of 2,400 S2 fits lost (D1 E8) |
| BB(1, p^u), u < 1 | yes | price changes by ≤ log 2. **The 2^{−k} size tail is lost** | a size cap (Fable's union route suggests K_n ≤ c·n log n/(log p)²; sufficient, not shown necessary). Sound for fixed small k (Astra R2) |
| BB(1, p^u), u > 1 | yes | price + (u−1)log p; size tail p^{−(u−1)k} | none |
| Bernoulli(p^{−u}) independent prior | yes | per-variable price deficit (1−u)log p | (1−u)A < ½ (the TH_PREP condition belongs here) |
| PIP threshold q / HPM | yes | no universal single-model log-score shift for marginal PIPs | HPM = S0 once 1 − π(S0\|y) < ½. MPM_q = S0 once max_j \|PIP_j − 1{j∈S0}\| < min(q, 1−q) |
| cap K | yes | — | a fixed cap ≥ s0 preserves S0 and only removes competitors; the delivered results use K = n/2. K ≤ c·n/log p fixes isometry but not testing (A-DIM″) |
| IG(a₀, b₀) | yes | constants only | none |
| data-free slab V = τ²I | **no** for the coded-score route (TD, TS-b, TM-a/b) | breaks the proof's exact coded-score reduction (n(G+I)⁻¹, data-scaled σ² rate); it cannot break the conditional data-law identity in A-MIS(iii) | re-derive TD, TS-b, TM-a/b for the new score |

"Form invariant" refers to the statements only. Price and prior algebra may transfer, but the conclusions need re-checking: a fixed g can prevent selection, and model-space changes can alter the result (Sol R2).

---

## 6. Open items and risks
1. **TD′.** Astra R2 refuted Fable's route at the testing step; TD′ is a conjecture with high proof risk. A proof needs localisation at size ≈ t/log p or a direct predictive bound.
2. **MARGIN\* is superseded** by the population form of A-MARGIN-U (v1.4). Its dichotomy lemma ("separated proxies imply a joint proxy", Fable Q1(3d)) is no longer needed: pervasive-factor designs fail (U2a) for small Q_n and fall back to the interpolated (U2b) with Q_n = T, a real dichotomy stated as such.
3. **Proof obligations for TS-b**: at fixed M the summation is a finite union; still to be written are the truncated superset sum (Beta moment bound per m with constants), the coded mixed odds **per base** (step 3, with Lemma W), the size lemma under A-BS (and its extension if A-BS′ is wanted), and the k > m̄_d step. Also c_L (TS-a) and the Cramér range for TM (i′). A growing M or J would need a genuinely uniform summation. Polynomial p and fixed s remain, against SL Cor 1.
4. **Proofs not seen by Fable.** thm:dist and prop:dist: check that the size tail there is the Fubini argument and that A-BS is used only as in §2.
5. **Literature still NOT VERIFIED (PN).** The Chen & Chen 2008 primary text (paywalled; second-hand via Luo & Chen p. 7 and SBJ p. 14); the Bayesian Analysis 2017 labels of Grünwald–van Ommen; Song–Liang's "Lemma A.2" (not in the supplement we hold).
6. **Cheap evidence that would strengthen the package** (Fable): S1 cells at SNR 1.25 and 1.5 (κ just above 1); a factor-proxy toy cell (ρ = 0.8). These need fits, so they need HQ approval and are not run here.
7. **Mixed-rival evidence.** The headline (U2a) is checked on S1 over all 1,023 deletions with at most two of the five tested proxies (the U2a check; larger proxy sets not tested); the outside-leakage decay is closed-form. E9/E9b are a zero-slack diagnostic of the refined form only, with mean widths for d ≤ 3 (selected D for d ≥ 2), m = 1 (all S1 cells) and m = 2 (p = 500 only), on four S1 AR(1) designs. m = 2 at p = 5,000, m ≥ 3 and d ≥ 4 are not evaluated there.
8. **No necessity result for (U2b).** The constant 2 is sharp only for deletions, and the common-base bound is conservative when many null sets leak in nearly the same direction.
9. **The high-dimensional TM tier** assumes a Gaussian-linear candidate law (A-MIS(iii)). Only TM-a0/TM-a0-inc tolerate a wrong response law.
10. **TD′** must pay an O(M log p) testing budget on a sieve with a much larger entropy, so it stays a high-risk conjecture (item 1).
