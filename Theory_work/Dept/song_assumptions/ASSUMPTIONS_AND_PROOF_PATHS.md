# ASSUMPTIONS AND PROOF PATHS — conjectured assumptions for the TH-SONG targets

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v1.1 (after Astra R2 cross-check of Fable R1 and of this integration; pre-council).**
Targets and notation: `THEOREM_DEFINITIONS.md` §4 (R_n(S), Pr_n(d,m), κ_n, D, N, d, m, j0(n), f₀, β^C, σ_C²).
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
| D1 | form of the selection margin | √((1−δ)nρ_S) ≥ a_Dm + √(2(1+δ)[B_Dm]₊), where a_Dm is the proxy-search Gaussian width | MARGIN-U: √R/σ ≥ (1+η)[√((2Pr−m log(n/C log p))₊) + √(2m log p)]. Sharp variant MARGIN\* with a leakage set | **A-MARGIN-U** in Astra's transparent form (R2 Q2): conditional one-sided width w_Dm, slack δ for sample transfer, γ > 0. Same structure in both advisors ([both advisors] for steps 1–4 only). MARGIN\* becomes the TS-b\* refinement |
| D2 | is the constant 2 sharp? | yes for single deletions. A uniform 2+η for swaps is OPEN. R2: the converse holds given A-NEC on T (two-sided determinant refund) | yes for deletions, with a converse. The width term is attained by a factor-proxy design | constant 2 for deletions plus a converse (needs A-NEC on T). Width term for added nulls; the factor-proxy example shows it is needed at one (d,m), not that every constant is optimal |
| D3 | the memo's literal "2·d·price for every rival" | not provable | counterexample for fixed j0 when log n = o(log p) | **rejected**. Recorded as OPEN under p ≤ n^A |
| D4 | covering the S1 boundary signals | covered when c_j²a > 2a+1 with log p/log n → a | fixed-ratio framing: liminf κ_n > 1 | **κ_n framing** (triangular arrays). S1 brackets κ = 1 |
| D5 | dimension | keep p ≤ n^A for released statements. R2: Fable's DIM′ route fails at its testing step (at log p = n^{1/3}: sieve log-entropy ≍ n^{2/3} against a testing budget nε² ≍ n^{1/3}) | DIM′: (log p)² = O(n) via the Fubini size tail. log p = o(n) needs a cap c·n/log p | released statements keep **A-DIM**. **TD′ is a conjecture with HIGH proof risk at the proposed rate**; the route needs localisation at size ≈ t/log p or a direct predictive bound. A fixed feasible cap is a distinct, easier case. No impossibility is implied |
| D6 | eigenvalue conditions | drop the fixed floor (including on T). Keep NEC plus relative SUBG | drop EFS and FLOOR-S0. NEC is needed only for the Occam factor | **drop all fixed and sample floors.** Keep A-NEC and Σ-relative A-SUBG [both advisors] |
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
- **Used in.** Every theorem.
  - Exact conjugate marginals: m_S(y) ∝ (2b₀ + Q_S)^{−(n/2+a₀)}·|I + X_SᵀX_S|^{−1/2}·(n+1)^{…}.
  - The Fubini identity E*[m_S/f*] = 1.
  - The Beta law of RSS ratios for supersets, which needs Gaussian ε (TS-b step 2). With centring, RSS_{S0∪N}/RSS_{S0} ~ Beta((n−1−s0−m)/2, m/2) conditional on full rank.
- **Defence.**
  - (a) Song & Liang (SL) model (1), p. 947 (same model, no intercept); NH14 Cond. 4.3, p. 11 (PN A2); YWJ p. 7 (PN E17); Jiang 2007, p. 7 (PN C7).
  - (b) S1/S2 are generated this way.
- **Weaker alternatives.**
  - Non-Gaussian independent ε, i.e. A-MIS(i′): the Beta law and the Fubini size tail fail. Fable's union route *suggests* a sufficient cap K_n ≤ c·n log n/(log p)² and a variance-proxy budget; neither is shown necessary (Astra R2). **Not adopted** as coded, so it stays a remark.
  - Heteroscedastic ε: the Grünwald–van Ommen mechanism applies, so it is a remark with the counter-calculation (TM §4.3).

### A-SPARSE — fixed sparsity
- **Statement.** |S0| ≤ s, with s fixed (or5 `asm:dist`(b)). For TS-b, s0 ≥ 1 is fixed.
- **Used in.** The size of the window q_n; the 2^{s0} deletion directions (TS-b step 1); the superset mass (s0+1)√(log p/n).
- **Defence.**
  - (a) SL strict sparsity (4), p. 950 (Thms 2–4 use it); NH14 Cond. 4.3, p. 11 (P17); SC11.
  - (b) s0 ∈ {5, 10} in S1/S2.
- **Weaker alternatives.**
  - Growing s0. Fable's route suggests s0²·log p = o(n), s0·(log p)² = o(n) and log s0 = o(η² price) (Fable Q5). `rem:sharp`(a) (which requires s ≤ min(K−1, p/2)) bounds how fast s0 may grow for π(S0|y) → 1; the upper rate s√(log p/n) is not a universal necessity for growing s (Astra R2). **Recorded as a growth remark**, not adopted: the owner's targets use fixed s.
  - Approximate sparsity, SL (3): optional corollary TD-A [P, to audit].

### A-DIM — polynomial dimension (released statements)
- **Statement.** 2 ≤ p ≤ n^A for a fixed A ≥ 1 (or5 `asm:dist`(b)).
- **Used in.**
  - TD: the window q_n ≍ log n and union bounds over q_n-sets (exp(O(log² n)) sets, controlled by the exponential tail bounds).
  - TS-b: j0(n) stays fixed; the R-transfer on (s0+j0)-sets; the Occam factor on q_n-sets.
- **Defence.**
  - (a) SBJ comment after Assumption 5, p. 14: "continue to hold when p grows polynomially" (P17 B2). Johnson & Rossell 2012 Thm 1, p. 651: p ≤ n (PN E16). SL Cor S1, SLs p. 16: quasi-polynomial P_n < n^{κ log n}.
  - (b) A = log p/log n is 0.90–1.37 on S1 and 1.50–1.77 on S2. Typical user regimes have A ≤ 1.77, and p ≤ n² holds in every setting and in six typical regimes (D1 E6).
- **Weaker alternatives.** See A-DIM′ and A-DIM″ below; the anti-stringency verdict is in §4, item 3.

### A-DIM′ — dimension relaxation (conjecture, TD′ and a TS-b′ variant)
- **Statement.** s·M·log p·log(p∨n) ≤ c_dim·n. The headline form is (log p)² = o(n) for fixed s and M.
- **Used in.** Sample control on q_n-sets, where q_n ≍ s·M·log₂(p√n) is the size window from the Fubini size tail (TD′ step 2).
- **Defence.**
  - (c) It contains SL Cor S1's range p < n^{κ log n}, and it covers SL Cor 1 for α < ½.
  - (a) Same type as SBJ Assumption 1, log p = O(n^α), p. 14 (P17 B2), and Jiang 2007 Cor 1, K_n ≤ e^{Cn^ξ}, p. 10 (PN C7).
  - (b) log p/√n is 0.20–0.38 on S1 and 0.69–0.98 on S2 (D1 E6).
- **Risk.** **High at the proposed rate** (Astra R2 Q1). Fable's step 3 fails: at log p = n^{1/3}, A-DIM′ holds but log C(p, q) ≍ n^{2/3} exceeds the testing budget nε² ≍ n^{1/3}. Moreover, the delivered proof localises to sizes s0 + O(t/log n) by fractional Bayes-factor moments whose factor p^{1−λ}n^{−λ/2} is not controlled for super-polynomial p. A proof needs localisation at size ≈ t/log p or a direct predictive bound. **Status: conjecture**, not part of any released statement; no impossibility follows from the failed route.
- **A-DIM″ (an Engineering option, not adopted).** A cap K_n ≤ c·n/log p solves the isometry inequality but **not** the testing inequality (Astra R2), so it does not by itself give TD at log p = o(n). A *fixed* feasible cap ≥ s is a distinct, easier case. Compare the NH14 cap m_n(ν) = p ∧ n/((2+ν) log p), pp. 10–11 (P17 B6).

### A-SUBG — sub-Gaussian rows on sparse directions, relative to their own variance
- **Statement.** Every predictor has positive variance, and E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2) for all λ and all u with at most q_n nonzero entries (or5 `asm:dist`(c), already Σ-relative).
- **Used in.**
  - The lower sparse isometry ‖Xv‖² ≥ (1−δ)n·vᵀΣv on (s0+j0)-sparse v. This gives the R-transfer (1−δ)R ≤ R̂ ≤ (1+δ)R (TS-b step 4).
  - The conversion inequality d_H² ≥ c_L·min{1, R/(nσ²)} (TS-a): relative SUBG gives E V⁴ ≤ C_L(E V²)² for an affine mean contrast V, hence P(V² ≥ E V²/2) ≥ 1/(4C_L) (Paley–Zygmund), and the Gaussian conditional affinity converts this (Astra R2 Q4). This converts R into Hellinger separation; it does **not** supply a lower bound on R (Gaussian duplicates have R = 0).
- **Defence.**
  - (a) SL Condition 1, p. 953 (exponential moments on sparse directions); RZ Def. 1.5/Thm 1.6, pp. 5–6; NH14 Lemma 6.1, p. 16 (P17 B7b).
  - (b) S1/S2 rows are Gaussian.
- **Weaker alternatives.**
  - SL Condition 2 (second moments only). The exact-marginal route needs exponential tails on q_n-sets, so this is **not adopted** in high dimension. It *is* the setting of TM-a0 (fixed p_C).
  - Bounded predictors (SL Thm 1): these are dominated, since bounded with variance bounded below implies SUBG.

### A-NEC — no near-exact collinearity (vanishing population floor)
- **Statement.** λ_min(Corr(x_T)) ≥ c_ψ/n for every |T| ≤ q_n (or5 `asm:dist`(d)).
- **Used in.** (i) The full Occam factor (n+1)^{−m/2} on added nulls: λ_min(X_TᵀX_T) ≳ 1 relative to the unit ridge (coded determinant ratio det[(n+1)G+I]/det[G+I]). (ii) The TS-b converse, which needs the two-sided determinant refund d·log(n+1)/2 + O(1) on T (Astra R2 Q3). The *sufficient* direction for deletions uses only the one-sided refund ≤ (n+1)^{d/2}, valid for every design by Cauchy interlacing (Fable (F3)). A-NEC is a sufficient, convenient device; heuristically, a null nearly collinear with the model pays almost no Occam price, but **necessity is unproved** (Astra R2).
- **Defence.**
  - (a) Weaker than SBJ A4 (ν ≻ τ/n), p. 14; NH14 Cond. 4.5, pp. 11, 17; BRT09 Assumption 2, p. 9 (P17 B6).
  - (a) Weaker than SL (26), SLs p. 15. SL themselves call their sample condition (22) "hardly satisfied" (SLs p. 15–16).
  - (b) The population floor (1−ρ)/(1+ρ) is 0.176–1. The margin over c_ψ/n is n × floor = 8.8–250 (D1 E5).
- **Weaker alternatives.** Drop A-NEC entirely: the delivered prop:dist(ii) gives TD with radius √(M log n·log(p∨n)/n). That route stays available.

### A-BS / A-BS′ — bounded signal
- **A-BS (as delivered, used for TD).** |β*_j|·sd(x_j) ≤ b̄σ* for every j (or5 `asm:dist`(e)).
- **A-BS′ (weaker alternative, not yet usable).**
  - (a) β*ᵀΣβ* ≤ M_μσ*².
  - (b) max_j |β*_j|sd(x_j) ≤ b̄_nσ*, with s·b̄_n² = o(n).
  - TS-b and TM-b use the size lemma prop:dist(i), which is proved under A-BS; A-BS′ becomes usable only once that lemma is extended (Astra R2). Note Astra R1's energy pair is the O(n) form, not identical to (b).
- **Used in.** The Fubini denominator m_S0/f* ≥ c·n^{−s0/2}; keeping σ̂² in a fixed range; the unit-ridge term ‖β̂_S0‖²/(n+1). **Verify at proof audit** that nothing else uses coordinatewise boundedness (Fable Q5).
- **Defence.**
  - (a) YWJ (7a), p. 7: "some form of upper bound on ‖β*‖ … is required" (P17 B4b); SC11 Assumption 2.7, p. 7.
  - (b) max|β|sd/σ ≤ 1.17 and ν ≤ 6 in every setting (D1 E4).
- **Weaker alternatives.** The aggregate energy pair (Astra Q5) / A-BS′ (Fable Q5): recorded, not adopted, until the size lemma is re-proved under it. All targets keep A-BS.

### A-MARGIN-H — Hellinger-scale residual signal (TS-a)
- **Statement.** For each j ∈ S0: inf{R_n(S) : j ∉ S, |S| ≤ q_n} ≥ C_H(L)·M·σ*²·log(p∨n).
- **Used in.** TS-a: by the SUBG conversion, d_H(f, f*)² ≥ c_L·min{1, R_n(S)/(nσ*²)} > ε_n² for every f supported on such an S (S from the effective posterior sieve, |S ∪ S0| ≤ q_n), so these f lie outside the TD ball. A-MARGIN-H is what supplies the lower bound on R; it plays the role of SL Condition 3.
- **Defence.**
  - (a) SL Condition 3, p. 955, and the proof of Thm 3, SLs pp. 5–6: d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}. The same residual-signal form appears in Luo & Chen arXiv v1 p. 7 (PN A4) and NH14 Cond. 4.4, p. 11 (PN A2).
  - (b) The screening margin divided by ε_n² is ≥ 1 in only 9 of 136 settings (D1 E2). Recovery occurs below it, so TS-a is honestly **not** a boundary-signal result.
- **Weaker alternatives.** The constant is inexplicit by construction. The sharp claim is carried by TS-b, not TS-a.

### A-MARGIN-U — residual-signal margin for exact selection (TS-b, TM-b)
- **Statement (Astra R2 Q2 form).** Fix M and let J := s + C_s M be the bounded posterior size from prop:dist(i). There are
  fixed 0 < δ < 1, γ > 0 and t_n → ∞ such that, for all large n and every S with D ≠ ∅ and |S∖S0| = m ≤ J,
  √((1−δ)R_n(S)/σ*²) ≥ w_Dm + t_n + √(2(1+δ)[B_Dm]₊),   B_Dm := Pr_n(d) − (m/2)·log(n/(C log p)) + γ log n.
  - w_Dm is the **one-sided conditional Gaussian width** of the residual directions: with v_S = (I−P_S)μ/‖(I−P_S)μ‖ and g
    standard Gaussian in the centred observation space, w_Dm(X) = E_g max_{|N|=m}(−⟨v_S, g⟩). Use the worst case over D, a
    deterministic upper bound holding with design probability 1 − o(1), or the combinatorial bound
    w_Dm ≤ √(2 log C(p−s0, m)) outright (choosing a smaller number is not enough). w_D0 = 0.
  - For m = 0 the condition reduces to liminf κ_n > 1, which permits *some* small γ, δ > 0 because Pr_n(d) ≳ log n.
  - The multiplicative form √R/σ ≥ (1+η)[w + √(2B)] + a_n is equivalent after choosing δ small relative to η and t_n ≤ a_n/3.
    The squared form R_n(S) ≥ 2(1+η)²(√d+√m)²σ*²·price_n is a simpler sufficient condition with spare slack.
- **Used in.** TS-b steps 1, 3 and 4. The converse (with A-NEC on T) shows the constant 2 is sharp for deletions.
- **Defence.**
  - (a) Same object, a projection residual of the true mean:
    - NH14 Cond. 4.4, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n), over models of size < K|t| that miss a true
      predictor (PN A2). **Comparison, not dominance:** NH14 multiply by |t| for every such model and use constant 5(1+δ);
      ours is per missed predictor with constant 2(1+δ) for deletions, but adds the width term w_Dm for mixed rivals and
      works over a different model range and prior. Neither condition contains the other uniformly (Astra R2).
    - Luo & Chen Consistency Condition, arXiv v1 p. 7: Δ_n(s)/(p₀ ln p) → ∞ (PN A4). Ours needs a fixed ratio for deletions,
      not → ∞.
    - Rossell 2022's non-centrality λ_tm, arXiv v7 p. 10 (PN D13).
  - (a) Necessity of the log p order: Wainwright 2009 Thm 2, arXiv v2 p. 4 (Gaussian design, averaged error; PN B5).
    Fletcher–Rangan–Goyal Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor (constant derived by C2; PN B6).
  - (b) **S1 brackets κ = 1.** κ_pop is 0.64–0.70 at SNR 1 (0/100 exact in every cell) and 2.54–2.80 at SNR 2 (92–96/100).
    Multi-deletions bind on S1 in all 16 settings (D1 E1).
  - (b) **Necessity on the data.** P1's min t² > 2·price has sensitivity 1.000 on S1 and 0.985 on S2, and P(exact | no) ≤ 0.0008.
- **Weaker alternatives evaluated.**
  - The memo's uniform "2·d·price" for every rival: rejected (D3); OPEN under p ≤ n^A.
  - Λ(S) → ∞ with multiplicity m·log p: neither sufficient nor necessary (Fable Q1(1)). On the data it ranks worse than
    κ_del (AUC 0.967 vs 0.980 on S2; D1 E1).
  - The delivered c_id > c1(s0, A) with a large explicit constant: replaced, because the threshold is now 2(1+δ) for
    deletions and the converse shows nothing below 2 works for deletions.
  - TS-b\* (MARGIN\*: 2+η with a leakage set): a refinement, medium risk.
  - γ = 0: the rate display would contain n⁰; consistency would need a separate o_P(1) argument retaining a diverging surplus.
    Not adopted for the headline.

### A-MIS — the working residual (TM-a, TM-b)
- **A-MIS(iii), headline.** The candidate set C is fixed in advance or chosen on independent data. (Raw units with an intercept; for a possibly discrete response, f₀ is the optimiser of the expected Gaussian log score, which is the KL minimiser under integrability.) The working residual u = y − α_C − x_Cᵀβ^C is independent of x_C and u ~ N(0, σ_C²). The other TD/TS-b assumptions are imposed on (x_C, β^C, σ_C²).
- **Used in.** It makes the candidate-only data an instance of A-GL, so TD and TS-b apply verbatim with f₀ in place of f*.
- **Defence.**
  - (a) SL Thm 4/Cor 2, p. 957, use the same f₀ (17)/(19). Rossell 2022 Prop. 6, arXiv v7 pp. 16–17 (Gaussian truth with omitted variables W; PN D13). Jointly Gaussian (x_C, x_omitted) satisfies (iii) (supplement `ex:omitted`).
  - (b) E[σ²|y, MPM]/σ_C² has median 0.99 on S1 and 0.84–0.98 on S2 (D1 E7). Proxy behaviour in well-specified data is near zero (0.1–1.6% of failures), which says nothing about hidden columns.
- **Weaker alternatives evaluated.**
  - (i′) Independent non-Gaussian residual: needs a cap and a variance-proxy budget. Remark (Fable Q6(3c)).
  - (ii) Moments only, E[x_C u] = 0: in high dimension the Grünwald–van Ommen mechanism applies heuristically, and nulls gain ϱ·χ²₁; Fable's budget (ϱ̄−1)·log p < ½ log n is a heuristic sufficient budget, not an established iff (Astra R2). Remark only. The Grünwald–van Ommen setting is heteroscedastic "in-liers" with a homoscedastic working model, and it is empirical only (arXiv v3 pp. 4–5; PN D12).
  - Fixed p_C with moments only: this *is* adopted, as TM-a0.

### A-MOM — moments for TM-a0
- **Statement.** **One fixed i.i.d. law** along the sample sequence (not an n-dependent truth: with β_n = 1/n even fixed-p support selection fails); p_C fixed; E‖x_C‖² < ∞, E y² < ∞; σ_C² = E u² > 0; Σ_CC nonsingular; π(S) > 0 for every S ⊆ C. For exact support selection, add the mixed second moments of the scores E[Z_j² u²] < ∞, Z = (1, x_Cᵀ)ᵀ (not marginal fourth moments). TM-a0 lies outside A-GL.
- **Defence.** (a) SL Condition 4, p. 957, together with "only a fixed number of possible models" in their proof, SLs p. 7.

---

## 3. Proof-path sketches (no proof claimed; each step names the assumptions it uses)

### 3.1 TD (delivered) and its extensions
**TD as delivered** is proved and independently checked; we only record where each assumption enters.
- A-GL gives exact marginals.
- A-SUBG + A-NEC on q_n-sets give tests and a sieve.
- A-BS gives the prior-mass lower bound.
- A-DIM makes the union bounds over q_n-sets polynomial.

**TD-as.** P*(E_n) ≤ n^{−c_H M}, summable when c_H M > 1, so Borel–Cantelli applies. [both advisors]

**TD′ (conjecture, HIGH proof risk at the proposed rate) [Fable Q3; refuted as a proof route by Astra R2 Q1].**
1. **Coarse size cutoff by Fubini** (valid). Conditional on X, after passing to raw centred contrasts and sandwiching the
   outcome-dependent IG rate b₀s_y² between fixed endpoints, E*[m^c_{S,b}/f*] = 1 for the normalised fixed-endpoint
   density. Markov on the numerator plus separate control of the denominator event (lower bound ≍ D_T^{−1/2}n^{−1/2}e^{−Λ}
   in noise units) gives the coarse cutoff s0 + ⌈[s0 log(2p) + (s0+2)log(n+1)/2 + 3t]/log 2⌉ (as in the delivered W3-DIST
   lemma X4(a)). This uses the BB(1,p) 2^{−k} size tail.
2. **Sample control on q_n-sets.** Isometry under A-SUBG holds when q_n·log p ≤ c·n, which A-DIM′ gives.
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
2. **Effective sieve.** Posterior sizes are ≤ s + C_s M (prop:dist(i), delivered), so only S with |S ∪ S0| ≤ q_n matter
   (or enlarge the SUBG window). **Uses the TD assumptions.**
3. **Margin.** By A-MARGIN-H, c_L·R/(nσ²) > ε_n², so {S ∌ j} lies outside the TD ball. Add the posterior large-size tail to
   the contraction tail (absorbing a factor 2 in the exponent): Π(j ∉ S | D_n) ≤ 2n^{−c_H M} on the TD event. **A-MARGIN-H
   supplies the lower bound on R; SUBG alone does not** (Gaussian duplicates have R = 0).
4. The a.s. version (posterior tails, fixed truth) follows from Borel–Cantelli when c_H M > 1.

### 3.3 TS-b (steps 1–4: same structure in Astra R1 Q1 and Fable Q1(3a)–(3c); details per Astra R2 Q2)
Let T = S0, U = T ∪ N, λ̂_S = R̂(S)/σ². Work on the bounded-size event |S| ≤ J = s + C_s M (prop:dist(i), under A-BS); every
rival class with m ≤ J is tested (Astra R1), so no separate j0 summation is needed. The coded determinant is
det[(n+1)G+I]/det[G+I].
1. **Pure deletions** (m = 0; 2^{s0} − 1 rivals).
   - (RSS_S − RSS_T)/σ² = (√λ̂_D + z_D)² + χ²_{d−1}; max_D |z_D| ≤ t_n with high probability (finitely many directions).
   - The deleted prior × determinant refund against T is ≤ exp(Pr_n(d)) for every design (monotone adjacent deletion
     price + Cauchy interlacing). **No floor is needed for sufficiency.**
   - Odds → 0 at rate n^{−γ} when √((1−δ)R_n/σ²) ≥ t_n + √(2(1+δ)[Pr_n(d) + γ log n]). **Uses A-MARGIN-U (m = 0).
     All D are needed, not only singletons.**
2. **Pure supersets** (d = 0). RSS_U/RSS_T ~ Beta((n−1−s0−m)/2, m/2) conditional on full rank (A-GL). The likelihood-ratio
   tail is Pareto-like with infinite mean, so Markov is applied to **truncated** sums. One-null mass is
   O_P((s0+1)√(log p/n)) (the order of the `rem:sharp`(b) lower bound, which is for witness designs). For bounded m the
   containing-model sum is O_P((C log p/n)^{m/2}); summing over all m ≤ J needs a **uniform** bound, not a per-m O_P (Astra R2;
   to be written in the proof). **Uses A-NEC (full Occam factor) and A-DIM.**
3. **Mixed rivals** (d ≥ 1, 1 ≤ m ≤ J). On the event max_N(−⟨v_S, g⟩) ≤ w_Dm + t_n (Gaussian concentration), the RSS loss
   against U is ≥ σ²(√λ̂_S − w_Dm − t_n)₊², with a bounded ridge correction; the deleted prior and refund against U is
   ≤ exp(Pr_n(d)); the containing-model sum supplies the −(m/2)log(n/(C log p)) credit. This gives O_P(n^{−γ}) per class.
   **Uses A-MARGIN-U and A-NEC.** The width term is needed: in a factor-proxy design a single swap beats S0 unless
   R ≥ 2(1+ρ)² log p (Fable [P][N]); this shows necessity at one (d, m), not optimality of every constant.
4. **R-transfer.** (1−δ)R_n(S) ≤ R̂(S) ≤ (1+δ)R_n(S) uniformly over (s0+J)-sets, from a lower sparse isometry under A-SUBG
   when (s0+J) log p ≤ cδ²n. **Uses A-SUBG and A-DIM; no eigenvalue floor.** (Fixed T sets: relative transfer O_P(n^{−1/2}).)
5. **Large models** (|S| > J): handled by the size lemma prop:dist(i) (Fubini coarse cutoff + fractional-moment
   localisation), proved under A-BS and A-DIM.
6. **Rate.** 1 − π(S0|y) = O_P((s0+1)√(log p/n) + n^{−γ} + n^{−c_H M}) with γ > 0. PIP and HPM/MPM follow by `lem:summaries`.

**Linearisation.** (n/2)log(1 + W/n) = W/2 − W²/(4n) + …; for fixed δ, log p = o(n) suffices. When R_n is comparable to n
(fixed signals) the gain is ≥ c·n ≫ Pr_n and the margin holds trivially, so the asymptotic statement can use R/2. Finite-n
diagnostics use the saturating gain (n/2)log(1 + R/(nσ²)) (D1 E1: P(exact) = ½ at κ_adj_full ≈ 1.0–1.5 on both suites;
post hoc).

**Converse [P, Fable Q2(3); conditions per Astra R2 Q3].** Assume the TS-b regularity **with A-NEC on T** (giving the
two-sided determinant refund d·log(n+1)/2 + O(1)) but not the forward margin. For the minimising D, with subthreshold
R_n/σ² = O(log n), Q − RSS = O_P(σ²), relative sample transfer and the noncentral χ²_d increment give
log(F_{T∖D}/F_T) = Pr_n(d) − R_n/(2σ²) + o_P(Pr_n(d)) → +∞ when limsup κ_n < 1, so π(S0|y) → 0. At a single-deletion
boundary √R_j/σ − √(2Pr_n(1)) → c, the probability that this rival beats T tends to Φ(−c), hence
**liminf P(π(S0|y) ≤ ½) ≥ Φ(−c)** (equality would need control of all other odds).

**Finite-n diagnostic (NOT a proposition; Astra R2 Q3).** In the idealised χ² score approximation, the expected number of
one-null extensions beating S0 is E K₁ ≈ (p−s0)·2Φ(−√L) ≈ (s0+1)/√(2πL(n+1)), L = 2log((2p−s0−1)/(s0+1)) + log(n+1).
This gives 0.033–0.056 for S1's (n, p) (Fable [N]), the same order as the observed S1 shortfall (2–8% at SNR ≥ 2), and
40 of 41 S1 failures at SNR ≥ 2 are supersets (D1 E1/E7). This is **consistent with** the superset term being the main
S1 failure mode at SNR ≥ 2; it is not a proved ceiling or lower bound on success (P(K₁ ≥ 1) ≤ E K₁ bounds one failure
type only; correlated nulls, swaps, higher-order rivals, ridge/IG terms and the HPM/MPM/sampler distinction are not
controlled by it).

### 3.4 TM-a0 [P, Fable Q6(3a); confirmed with fixes by Astra R2 Q4]
One fixed i.i.d. law; raw units with an intercept, Z = (1, x_Cᵀ)ᵀ.
1. There are 2^{p_C} models. RSS_S/n → σ_S² := min_b E(y − Z_Sᵀb)² a.s. (SLLN); Q_S − RSS_S = O(1) a.s. eventually;
   b₀s_y² = O(1); log D_S = |S|·log(n+1) + O(1). **Uses A-MOM.**
2. Models missing supp β^C have σ_S² > σ_C² and lose (n/2)log(σ_S²/σ_C²) + o(n).
3. Density consistency: each of the finitely many containing models has consistent fitted parameters and a concentrating
   conditional posterior, so Hellinger convergence to f₀ a.s. follows **even without** the score moments (their relative
   masses need not converge).
4. Exact support: E[Zu] = 0 and finite coordinate score variances give ‖Σ_i Z_i u_i‖ = O_a.s.(√(n log log n)) (LIL); the
   residualised Gram inverse is O_a.s.(1/n); so the extra fitted sum of squares is O_a.s.(log log n), against (m/2)log n.
   **Uses E[Z_j²u²] < ∞.**

### 3.5 TM-a, TM-b
Under A-MIS(iii), the candidate-only data satisfy A-GL with parameters (α_C, β^C, σ_C²). Apply TD (3.1, with TD's M-window; a.s. corollary for posterior tails) and TS-b (3.3) verbatim, with f₀ in place of f* and A-MARGIN-U in σ_C² units on μ_C = X_Cβ^C. C must not depend on the outcome data. The delivered `thm:omitted` is the special case with Gaussian rows, a fixed floor and diverging per-coefficient signal.

---

## 4. Anti-stringency ledger (each restrictive v3.1.1 assumption → weaker alternative → verdict)

| # | v3.1.1 assumption | why too strong | weaker alternative evaluated (with Fable/Astra) | verdict |
|---|---|---|---|---|
| 1 | c_id > c1(s0, A), an explicit constant (`asm:margin`) | large proof constant. S1 recovers at κ ≈ 2.5–2.8 (D1), far below c1 | A-MARGIN-U with constant 2(1+δ) for deletions, plus the width term for added nulls. The converse (with A-NEC on T) shows 2 is sharp for deletions | **adopted** |
| 2 | FSb: fixed b_lo ≤ \|β\| | S1 has β ∝ √(log p/n), so FSb is false as a sequence (D1 E4) | κ_n framing over triangular arrays | **adopted** |
| 3 | p ≤ n^A | excludes exponential p, which SL cover (Cor 1) | DIM′ (log p)² = o(n) (Fable); log p = o(n) with a cap (A-DIM″) | **conjecture TD′, high proof risk** (Astra R2: the testing step fails at log p = n^{1/3}); a cap fixes isometry, not testing. p ≤ n^A stays for released statements |
| 4 | EF: sample sparse eigenvalue floor (`thm:post-fixed`) | vacuous on S2: greedy floor 1e−5 to 2e−4 at m2 (D1 E5); SL call (22) "hardly satisfied" | population A-NEC (c_ψ/n) plus the A-SUBG isometry | **adopted** (sample floors demoted to a remark) |
| 5 | EFS / FLOOR-S0: fixed population floor | unnecessary: R_n(S0∖{j}) = nβ_j²Var(x_j \| rest) already enters the margin | drop it (both advisors) | **adopted** |
| 6 | A-BS per coordinate | "why bounded signals?" | A-BS′ aggregate energy | **recorded, not adopted** until the size lemma prop:dist(i) is re-proved under it (Astra R2) |
| 7 | memo MARGIN (uniform 2·d·price) | actually too *weak* in one direction (proxy counterexample) and too strong in another (charges d·price to swaps) | MARGIN-U / MARGIN\* | **replaced** |
| 8 | s0 fixed | — | growth remark: s0²·log p = o(n) | remark |
| 9 | Gaussian residual for TM | excludes non-Gaussian misspecification | (i′) with a cap; (ii) with a budget | remarks; TM-a0 covers moments-only at fixed p_C |
| 10 | SL Condition 3 as a separate assumption | its role is a lower bound on residual signal | A-MARGIN-H (lower bound on R) + the SUBG conversion inequality (SUBG alone does **not** imply it) | **replaced by A-MARGIN-H** |

---

## 5. Engineering sensitivity (corrected; supersedes TH_PREP §3 on the size prior)

Per-model prior odds of adding a variable at size k under BB(1, b): (k+1)/(p−k−1+b). The size-marginal ratio is (p−k)/(p−k−1+b).

| change | form invariant? | what moves | new condition |
|---|---|---|---|
| g (slab scale) | yes | price_g(k) = log[(2p−1−k)/(k+1)] + ½log(1+g). The TS-b threshold moves with it. Superset mass ≍ (s0+1)√(log p/g). The misspecification budget ϱ̄ < 1 + log(1+g)/(2 log p) | heuristic: s0²·log p = o(g). Small g also enlarges the slab loss O(n/g), so the nominal price alone does not describe a g change (Astra R2). Fixed g can prevent selection. g = n → c·n shifts the price by ½log[(1+cn)/(1+n)] at fixed k |
| g = max(n, p²) | yes | price ≈ 2 log p: more signal needed, fewer supersets | none |
| g = 4n or 9n (Engineering trials) | yes | the superset margin ω = price − log p rises by ½log g, so S1 superset losses fall. The empty-model margin on S2 falls | none. Matches perf/JOINT_PLAN: S1 losses fixed, 92–170 of 2,400 S2 fits lost (D1 E8) |
| BB(1, p^u), u < 1 | yes | price changes by ≤ log 2. **The 2^{−k} size tail is lost** | a size cap (Fable's union route suggests K_n ≤ c·n log n/(log p)²; sufficient, not shown necessary). Sound for fixed small k (Astra R2) |
| BB(1, p^u), u > 1 | yes | price + (u−1)log p; size tail p^{−(u−1)k} | none |
| Bernoulli(p^{−u}) independent prior | yes | per-variable price deficit (1−u)log p | (1−u)A < ½ (the TH_PREP condition belongs here) |
| PIP threshold q / HPM | yes | no universal single-model log-score shift for marginal PIPs | HPM = S0 once 1 − π(S0\|y) < ½. MPM_q = S0 once max_j \|PIP_j − 1{j∈S0}\| < min(q, 1−q) |
| cap K | yes | — | a fixed cap ≥ s0 preserves S0 and only removes competitors; the delivered results use K = n/2. K ≤ c·n/log p fixes isometry but not testing (A-DIM″) |
| IG(a₀, b₀) | yes | constants only | none |
| data-free slab V = τ²I | **no** for TM | breaks the exact candidate reduction | re-derive |

---

## 6. Open items and risks
1. **TD′.** Astra R2 refuted Fable's route at the testing step; TD′ is a conjecture with high proof risk. A proof needs localisation at size ≈ t/log p or a direct predictive bound.
2. **TS-b\*.** The dichotomy lemma behind MARGIN\* ("separated proxies imply a joint proxy") is [C] (Fable Q1(3d)).
3. **Proof obligations for TS-b** (Astra R2): a **uniform** summation over m ≤ J of the superset/mixed classes at the claimed rate; extension of the size lemma if A-BS′ is wanted; constants c_L (TS-a), the truncated-sum superset bound, and the Cramér range for TM (i′).
4. **Proofs not seen by Fable.** thm:dist and prop:dist: check that the size tail there is the Fubini argument and that A-BS is used only as in §2.
5. **Literature still NOT VERIFIED (PN).** The Chen & Chen 2008 primary text (paywalled; second-hand via Luo & Chen p. 7 and SBJ p. 14); the Bayesian Analysis 2017 labels of Grünwald–van Ommen; Song–Liang's "Lemma A.2" (not in the supplement we hold).
6. **Cheap evidence that would strengthen the package** (Fable): S1 cells at SNR 1.25 and 1.5 (κ just above 1); a factor-proxy toy cell (ρ = 0.8). These need fits, so they need HQ approval and are not run here.
