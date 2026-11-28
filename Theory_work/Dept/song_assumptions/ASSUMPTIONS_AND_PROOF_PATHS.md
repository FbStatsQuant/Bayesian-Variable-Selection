# ASSUMPTIONS AND PROOF PATHS — conjectured assumptions for the TH-SONG targets

Theory Department, mission TH-SONG-ASSUMPTIONS, 2026-11-27. Task Lead: Opus 5.5. **Draft v1 (pre-council).**
Targets and notation: `THEOREM_DEFINITIONS.md` §4 (R_n(S), Pr_n(d,m), κ_n, D, N, d, m, j0(n), f₀, β^C, σ_C²).
Inputs: advisors `advisors/ASTRA_R1.md` (Astra 6.2) and `advisors/FABLE_R1.md` (Fable 5.2), which were written
independently; data `SIMULATION_DATA_ANALYSIS.md` (D1); literature `PRECEDENTS_NEW.md` (C2, with the Lead's errata) and
`writing_answers/PRECEDENTS_2026-11-17.md` (verified earlier).

**What "conjectured" means here.** No proof is claimed. Every assumption must pass a dual bar.
- **(a) Proof path.** A sketch names the step that uses the assumption (§3).
- **(b) Defensibility.** The assumption has an exact verified citation (paper, label, page, version), S1/S2 evidence, or both.

Tags used throughout:
- [P]: an advisor gives the inequalities, and a proof at this level should go through once constants are audited.
- [P2]: two advisors gave the same route independently.
- [H]: heuristic.
- [C]: conjecture.
- (a) precedent, (b) empirical, (c) mild technical.

Every citation below is either in PRECEDENTS_2026-11-17 (marked "P17") or in PRECEDENTS_NEW (marked "PN"), with its page.

---

## 1. Design decisions (where the two advisors agree, and how disagreements were settled)

| # | question | Astra R1 | Fable R1 | decision |
|---|---|---|---|---|
| D1 | form of the selection margin | √((1−δ)nρ_S) ≥ a_Dm + √(2(1+δ)[B_Dm]₊), where a_Dm is the proxy-search Gaussian width | MARGIN-U: √R/σ ≥ (1+η)[√((2Pr−m log(n/C log p))₊) + √(2m log p)]. Sharp variant MARGIN\* with a leakage set | **A-MARGIN-U** (the same condition, [P2]) is the headline. MARGIN\* becomes the TS-b\* refinement |
| D2 | is the constant 2 sharp? | yes for single deletions. A uniform 2+η for swaps is OPEN | yes for deletions, with a converse. The width term is attained by a factor-proxy design | constant 2 for deletions plus a converse. Width term for added nulls |
| D3 | the memo's literal "2·d·price for every rival" | not provable | counterexample for fixed j0 when log n = o(log p) | **rejected**. Recorded as OPEN under p ≤ n^A |
| D4 | covering the S1 boundary signals | covered when c_j²a > 2a+1 with log p/log n → a | fixed-ratio framing: liminf κ_n > 1 | **κ_n framing** (triangular arrays). S1 brackets κ = 1 |
| D5 | dimension | keep p ≤ n^A for released statements. log p = o(n) needs a cap or a sieve tail | DIM′: (log p)² = O(n) via the Fubini size tail. log p = o(n) needs a cap c·n/log p | released statements keep **A-DIM**. **A-DIM′** is a conjecture (TD′), [P] by Fable, not yet re-checked by Astra |
| D6 | eigenvalue conditions | drop the fixed floor (including on T). Keep NEC plus relative SUBG | drop EFS and FLOOR-S0. NEC is needed only for the Occam factor | **drop all fixed and sample floors.** Keep A-NEC and Σ-relative A-SUBG [P2] |
| D7 | bounded signal | aggregate energy pair | BS′: βᵀΣβ ≤ M_μσ², s·b̄_n² = o(n) | **A-BS** as delivered for TD (no re-issue). **A-BS′** for TS-b/TM-b (new statements) |
| D8 | misspecification | option (iii) (independent N(0,σ_C²) residual). Non-Gaussian is high risk. C must be prespecified | three tiers: a0 (fixed p_C, moments, a.s.); (iii); (i′) with a cap. (ii) only as a remark | **TM-a0 + TM-a/TM-b under (iii)**. (i′) and (ii) are remarks |
| D9 | almost-sure versions | Borel–Cantelli with c_H M > 1 | same, for TD/TS-a/TM-a0 but not for TS-b | **TD-as, TS-a a.s., TM-a0 a.s.** TS-b stays in probability |
| D10 | Engineering: BB(1,p^u), u < 1 | TH_PREP §3 is wrong: the loss is the size tail | same correction, independently | TH_PREP §3 is **superseded** (§5) |
| D11 | SL Condition 3 | — | implied by sub-Gaussian rows: d_H² ≥ c(L)·min{1, R/(nσ²)} | not assumed. Only the size of R is assumed (A-MARGIN-H) |

---

## 2. The assumption catalogue

Each row gives the exact statement, where the proof uses it, its defence, and the weaker alternatives considered (the anti-stringency rule).

### A-GL — Gaussian linear model, i.i.d. pairs
- **Statement.** y = α* + xᵀβ* + ε with ε ~ N(0, σ*²) independent of x, σ*² > 0, and (x_i, y_i) i.i.d. The quantities α*, β*, σ* and the law of x may depend on n. This is or5 `asm:dist`(a).
- **Used in.** Every theorem.
  - Exact conjugate marginals: m_S(y) ∝ (2b₀ + Q_S)^{−(n/2+a₀)}·|I + X_SᵀX_S|^{−1/2}·(n+1)^{…}.
  - The Fubini identity E*[m_S/f*] = 1.
  - The Beta law of RSS ratios for supersets, which needs Gaussian ε (TS-b step 2).
- **Defence.**
  - (a) Song & Liang (SL) model (1), p. 947 (same model, no intercept); NH14 Cond. 4.3, p. 11 (PN A2); YWJ p. 7 (PN E17); Jiang 2007, p. 7 (PN C7).
  - (b) S1/S2 are generated this way.
- **Weaker alternatives.**
  - Non-Gaussian independent ε, i.e. A-MIS(i′): the Beta law and the Fubini size tail fail. It would need a cap K_n ≤ c·n log n/(log p)² and a variance-proxy budget (Fable Q6(3c), Astra Q6). **Not adopted** as coded, so it stays a remark.
  - Heteroscedastic ε: the Grünwald–van Ommen mechanism applies, so it is a remark with the counter-calculation (TM §4.3).

### A-SPARSE — fixed sparsity
- **Statement.** |S0| ≤ s, with s fixed (or5 `asm:dist`(b)). For TS-b, s0 ≥ 1 is fixed.
- **Used in.** The size of the window q_n; the 2^{s0} deletion directions (TS-b step 1); the superset mass (s0+1)√(log p/n).
- **Defence.**
  - (a) SL strict sparsity (4), p. 950 (Thms 2–4 use it); NH14 Cond. 4.3, p. 11 (P17); SC11.
  - (b) s0 ∈ {5, 10} in S1/S2.
- **Weaker alternatives.**
  - Growing s0. TS-b needs s0²·log p = o(n), s0·(log p)² = o(n) and log s0 = o(η² price) (Fable Q5). `rem:sharp` already forces s0 = o(√n) for π(S0|y) → 1. **Recorded as a growth remark**, not adopted: the owner's targets use fixed s.
  - Approximate sparsity, SL (3): optional corollary TD-A [P, to audit].

### A-DIM — polynomial dimension (released statements)
- **Statement.** 2 ≤ p ≤ n^A for a fixed A ≥ 1 (or5 `asm:dist`(b)).
- **Used in.**
  - TD: the window q_n ≍ log n and union bounds over q_n-sets.
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
- **Risk.** Low–medium. The route is [P] from one advisor. Astra asks for the sieve-entropy and size-tail budget to be written out first. **Status: conjecture**, not part of any released statement.
- **A-DIM″ (an Engineering option, not adopted).** A cap K_n ≤ c·n/log p would give log p = o(n). This is the NH14 cap m_n(ν) = p ∧ n/((2+ν) log p), pp. 10–11 (P17 B6).

### A-SUBG — sub-Gaussian rows on sparse directions, relative to their own variance
- **Statement.** Every predictor has positive variance, and E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2) for all λ and all u with at most q_n nonzero entries (or5 `asm:dist`(c), already Σ-relative).
- **Used in.**
  - The lower sparse isometry ‖Xv‖² ≥ (1−δ)n·vᵀΣv on (s0+j0)-sparse v. This gives the R-transfer (1−δ)R ≤ R̂ ≤ (1+δ)R (TS-b step 4).
  - The Hellinger separation d_H² ≥ c(L)·min{1, R/(nσ²)} by Paley–Zygmund (TS-a).
- **Defence.**
  - (a) SL Condition 1, p. 953 (exponential moments on sparse directions); RZ Def. 1.5/Thm 1.6, pp. 5–6; NH14 Lemma 6.1, p. 16 (P17 B7b).
  - (b) S1/S2 rows are Gaussian.
- **Weaker alternatives.**
  - SL Condition 2 (second moments only). The exact-marginal route needs exponential tails on q_n-sets, so this is **not adopted** in high dimension. It *is* the setting of TM-a0 (fixed p_C).
  - Bounded predictors (SL Thm 1): these are dominated, since bounded with variance bounded below implies SUBG.

### A-NEC — no near-exact collinearity (vanishing population floor)
- **Statement.** λ_min(Corr(x_T)) ≥ c_ψ/n for every |T| ≤ q_n (or5 `asm:dist`(d)).
- **Used in.** Only the full Occam factor (n+1)^{−m/2} on added nulls: λ_min(X_TᵀX_T) ≳ 1 relative to the unit ridge. Deletions need no floor, because the refund is ≤ (n+1)^{d/2} for every design by Cauchy interlacing (Fable (F3)). Without A-NEC, a null nearly collinear with the model pays almost no Occam price and supersets keep mass; this is why A-NEC is not removable.
- **Defence.**
  - (a) Weaker than SBJ A4 (ν ≻ τ/n), p. 14; NH14 Cond. 4.5, pp. 11, 17; BRT09 Assumption 2, p. 9 (P17 B6).
  - (a) Weaker than SL (26), SLs p. 15. SL themselves call their sample condition (22) "hardly satisfied" (SLs p. 15–16).
  - (b) The population floor (1−ρ)/(1+ρ) is 0.176–1. The margin over c_ψ/n is n × floor = 8.8–250 (D1 E5).
- **Weaker alternatives.** Drop A-NEC entirely: the delivered prop:dist(ii) gives TD with radius √(M log n·log(p∨n)/n). That route stays available.

### A-BS / A-BS′ — bounded signal
- **A-BS (as delivered, used for TD).** |β*_j|·sd(x_j) ≤ b̄σ* for every j (or5 `asm:dist`(e)).
- **A-BS′ (for TS-b and TM-b, new statements).**
  - (a) β*ᵀΣβ* ≤ M_μσ*².
  - (b) max_j |β*_j|sd(x_j) ≤ b̄_nσ*, with s·b̄_n² = o(n).
- **Used in.** The Fubini denominator m_S0/f* ≥ c·n^{−s0/2}; keeping σ̂² in a fixed range; the unit-ridge term ‖β̂_S0‖²/(n+1). **Verify at proof audit** that nothing else uses coordinatewise boundedness (Fable Q5).
- **Defence.**
  - (a) YWJ (7a), p. 7: "some form of upper bound on ‖β*‖ … is required" (P17 B4b); SC11 Assumption 2.7, p. 7.
  - (b) max|β|sd/σ ≤ 1.17 and ν ≤ 6 in every setting (D1 E4).
- **Weaker alternatives.** The aggregate energy pair (Astra Q5). Adopted as A-BS′ for the new statements only; TD keeps A-BS so that prop:dist(i) need not be re-issued.

### A-MARGIN-H — Hellinger-scale residual signal (TS-a)
- **Statement.** For each j ∈ S0: inf{R_n(S) : j ∉ S, |S| ≤ q_n} ≥ C_H(L)·M·σ*²·log(p∨n).
- **Used in.** TS-a: d_H(f, f*)² ≥ c(L)·R_n(S)/(nσ*²) > ε_n² for every f supported on such an S, so these f lie outside the TD ball.
- **Defence.**
  - (a) SL Condition 3, p. 955, and the proof of Thm 3, SLs pp. 5–6: d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}. The same residual-signal form appears in Luo & Chen arXiv v1 p. 7 (PN A4) and NH14 Cond. 4.4, p. 11 (PN A2).
  - (b) The screening margin divided by ε_n² is ≥ 1 in only 9 of 136 settings (D1 E2). Recovery occurs below it, so TS-a is honestly **not** a boundary-signal result.
- **Weaker alternatives.** The constant is inexplicit by construction. The sharp claim is carried by TS-b, not TS-a.

### A-MARGIN-U — residual-signal margin for exact selection (TS-b, TM-b)
- **Statement.** There are η > 0, γ ≥ 0 and a_n → ∞ such that, for all large n and every S with D ≠ ∅ and m ≤ j0(n),
  √R_n(S)/σ* ≥ (1+η)[w_m + √(2[Pr_n(d) − (m/2)log(n/(C log p)) + γ log n]₊)] + a_n,
  with w_m ≤ √(2 log C(p−s0, m)). A simpler sufficient form is R_n(S) ≥ 2(1+η)²(√d+√m)²σ*²·price_n. For m = 0 the condition is liminf κ_n > 1.
- **Used in.** TS-b steps 1 and 3; the converse shows the constant is sharp for deletions.
- **Defence.**
  - (a) Same object, a projection residual of the true mean:
    - NH14 Cond. 4.4, p. 11 (page image): Δ_n(K) > 5σ²|t|(1+δ) log(√n ∨ p_n), over models of size < K|t| that miss a true predictor (PN A2). Ours is **weaker**: it is per missed predictor rather than times |t|, and it has constant 2(1+η) instead of 5(1+δ).
    - Luo & Chen Consistency Condition, arXiv v1 p. 7: Δ_n(s)/(p₀ ln p) → ∞ (PN A4). Ours needs a fixed ratio, not → ∞.
    - Rossell 2022's non-centrality λ_tm, arXiv v7 p. 10 (PN D13).
  - (a) Necessity of the log p order: Wainwright 2009 Thm 2, arXiv v2 p. 4 (Gaussian design, averaged error; PN B5). Fletcher–Rangan–Goyal Thm 1, arXiv v1 p. 4: ML fails below ≈ 2σ² log p per predictor (constant derived by C2; PN B6).
  - (b) **S1 brackets κ = 1.** κ_pop is 0.64–0.70 at SNR 1 (0/100 exact in every cell) and 2.54–2.80 at SNR 2 (92–96/100). Multi-deletions bind on S1 in all 16 settings (D1 E1).
  - (b) **Necessity on the data.** P1's min t² > 2·price has sensitivity 1.000 on S1 and 0.985 on S2, and P(exact | no) ≤ 0.0008.
- **Weaker alternatives evaluated.**
  - The memo's uniform "2·d·price" for every rival: rejected (D3).
  - Λ(S) → ∞ with multiplicity m·log p: neither sufficient nor necessary (Fable Q1(1)). On the data it ranks worse than κ_del (AUC 0.967 vs 0.980 on S2; D1 E1).
  - The delivered c_id > c1(s0, A) with a large explicit constant: replaced, because the threshold is now 2(1+η) for deletions and the converse shows nothing below 2 works.
  - TS-b\* (MARGIN\*: 2+η with a leakage set): a refinement, medium risk.

### A-MIS — the working residual (TM-a, TM-b)
- **A-MIS(iii), headline.** The candidate set C is fixed in advance or chosen on independent data. The working residual u = y − α_C − x_Cᵀβ^C is independent of x_C and u ~ N(0, σ_C²). The other TD/TS-b assumptions are imposed on (x_C, β^C, σ_C²).
- **Used in.** It makes the candidate-only data an instance of A-GL, so TD and TS-b apply verbatim with f₀ in place of f*.
- **Defence.**
  - (a) SL Thm 4/Cor 2, p. 957, use the same f₀ (17)/(19). Rossell 2022 Prop. 6, arXiv v7 pp. 16–17 (Gaussian truth with omitted variables W; PN D13). Jointly Gaussian (x_C, x_omitted) satisfies (iii) (supplement `ex:omitted`).
  - (b) E[σ²|y, MPM]/σ_C² has median 0.99 on S1 and 0.84–0.98 on S2 (D1 E7). Proxy behaviour in well-specified data is near zero (0.1–1.6% of failures), which says nothing about hidden columns.
- **Weaker alternatives evaluated.**
  - (i′) Independent non-Gaussian residual: needs a cap and a variance-proxy budget. Remark (Fable Q6(3c)).
  - (ii) Moments only, E[x_C u] = 0: in high dimension the Grünwald–van Ommen mechanism applies, and nulls gain ϱ·χ²₁. Remark only. The Grünwald–van Ommen setting is heteroscedastic "in-liers" with a homoscedastic working model, and it is empirical only (arXiv v3 pp. 4–5; PN D12).
  - Fixed p_C with moments only: this *is* adopted, as TM-a0.

### A-MOM — moments for TM-a0
- **Statement.** p_C is fixed; E‖x_C‖² < ∞, E y² < ∞; Σ_CC is nonsingular; π(S) > 0 for every S ⊆ C. For exact support selection, add E[x_j²u²] < ∞.
- **Defence.** (a) SL Condition 4, p. 957, together with "only a fixed number of possible models" in their proof, SLs p. 7.

---

## 3. Proof-path sketches (no proof claimed; each step names the assumptions it uses)

### 3.1 TD (delivered) and its extensions
**TD as delivered** is proved and independently checked; we only record where each assumption enters.
- A-GL gives exact marginals.
- A-SUBG + A-NEC on q_n-sets give tests and a sieve.
- A-BS gives the prior-mass lower bound.
- A-DIM makes the union bounds over q_n-sets polynomial.

**TD-as.** P*(E_n) ≤ n^{−c_H M}, summable when c_H M > 1, so Borel–Cantelli applies. [P2]

**TD′ (conjecture) [P, Fable Q3].**
1. **Size tail by Fubini.** E*[m_S(y)/f*(y)] = 1 for each S. On an event of probability → 1, m_S0/f* ≥ c·n^{−s0/2} (by A-BS). Hence E*Π(|S| ≥ q | y) ≲ Π(|S| ≥ q)·p^{s0}n^{s0/2}/π-normalisation ≍ 2^{−q}p^{s0}n^{s0/2}, and model sizes are ≤ q_n ≍ s0·log₂(p√n) for every p. This uses the BB(1,p) 2^{−k} size tail.
2. **Sample control on q_n-sets.** Isometry under A-SUBG holds when q_n·log p ≤ c·n. This is exactly A-DIM′.
3. **Tests and entropy** on the q_n-sieve, as in TD, with log-entropy ≍ q_n log p ≤ nε_n².
- **Gap to close before release (Astra).** Write the sieve-entropy and remaining-mass budget at K = n/2 explicitly.

**TD-A (optional) [P, to audit].** If the tail is sub-Gaussian with variance ≤ c₀σ²M log n/n, a change of measure puts the truth within Hellinger distance c·ε_n of the s-sparse surrogate; then apply TD. Check that this does not silently need p ≤ n^A.

### 3.2 TS-a
1. **Hellinger separation.** For every f supported on S ∌ j with free (β_S, σ_S), d_H²(f, f*) ≥ c(L)·min{1, R_n(S)/(nσ*²)}. For Gaussian x this is exact: d_H² ≥ 1 − (1 + R/(2nσ²))^{−1/4} (Fable Q2 [P]). For sub-Gaussian x it follows by Paley–Zygmund [P, constant to audit]. **Uses A-SUBG.** It replaces SL Condition 3.
2. Posterior sizes are ≤ s + C_s M (prop:dist(i), delivered). So only S with |S| ≤ q_n matter. **Uses the TD assumptions.**
3. By A-MARGIN-H, c(L)·R/(nσ²) > M log(p∨n)/n = ε_n². So {S ∌ j} lies outside the TD ball, and Π(j ∉ S | D_n) ≤ n^{−c_H M} on the TD event. **Uses A-MARGIN-H.**
4. The a.s. version follows from Borel–Cantelli when c_H M > 1.

### 3.3 TS-b (Astra Q1 steps 1–5 = Fable Q1(3a)–(3c), [P2])
The log posterior odds of S against S0 are Pr_n(d,m) − ½(RSS_S − RSS_S0)/σ̂²·(1+o(1)), plus Occam and ridge corrections.
1. **Pure deletions** (m = 0; 2^{s0} − 1 rivals).
   - (RSS_S − RSS_S0)/σ² = (√R̂_D + z_D)² + χ²_{d−1}.
   - max_D |z_D| ≤ a_n with high probability, because there are finitely many directions.
   - The Occam refund is ≤ (n+1)^{d/2} for any design (Cauchy interlacing). **No floor is needed.**
   - So the odds → 0 iff √R̂_D/σ − √(2Pr_n(d)) → ∞. **Uses A-MARGIN-U (m = 0), i.e. liminf κ_n > 1. All D are needed, not only singletons.**
2. **Pure supersets** (d = 0).
   - RSS_S/RSS_S0 ~ Beta((n−s0−m)/2, m/2) exactly (A-GL). The likelihood-ratio tail is Pareto-like with infinite mean, so the argument uses Markov on **truncated** sums.
   - One-null mass is O_P((s0+1)√(log p/n)), which matches the `rem:sharp` lower bound.
   - The m-null mass is ≲ [C(s0+m)√(log p/n)]^m/m! · e^{O(m)}, given (s0+m)·price ≤ c·n.
   - **Uses A-NEC** (the full Occam factor) **and A-DIM.**
3. **Mixed rivals** (d ≥ 1, 1 ≤ m ≤ j0).
   - On the event max_N |z_S| ≤ w_m + a_n (Gaussian width of the residual directions over |N| = m), Σ_N odds ≤ exp{Pr_n(d) − ½(min_N √R̂(S) − w_m − a_n)²} × Σ_N exp{−m prices + ½ω²_N}.
   - The last sum is O_P((C log p/n)^{m/2}) by step 2. This produces the −(m/2)log(n/(C log p)) credit in A-MARGIN-U.
   - **Uses A-MARGIN-U and A-NEC.**
   - The width term is attained: in the factor-proxy design a swap beats S0 unless R ≥ 2(1+ρ)² log p (Fable [P][N]).
4. **R-transfer.** (1−δ)R_n(S) ≤ R̂(S) ≤ (1+δ)R_n(S) uniformly over (s0+j0)-sets, from a lower sparse isometry under A-SUBG when (s0+j0) log p ≤ cδ²n. **Uses A-SUBG and A-DIM; no eigenvalue floor.**
5. **Large rivals** (m > j0(n)).
   - Controlled without any signal: exp(d·price)·(C log p/n)^{m/2} → 0 once m > 2s0·price/log(n/(C log p)).
   - Sizes ≥ q_n are handled by the Fubini size tail (3.1, step 1).
   - **Uses A-DIM (j0 fixed) and BB(1,p)'s size tail.**
6. **Rate.** 1 − π(S0|y) = O_P((s0+1)√(log p/n) + n^{−γ} + n^{−c_H M}). PIP and HPM/MPM follow by `lem:summaries`.

**Linearisation.** (n/2)log(1 + W/n) = W/2 − W²/(4n) + …. For fixed η, log p = o(n) suffices. When R_n is comparable to n (fixed signals) the gain is ≥ c·n ≫ Pr_n, so the margin holds trivially. The asymptotic statement can therefore use R/2, while the finite-n companion uses the saturating gain (n/2)log(1 + R/(nσ²)). This is the D1 E1 finding: the saturating gain fits the S2 transition (P(exact) = 0.5 at κ_adj_full ≈ 1.2–1.5, and 1.50 on S1).

**Converse [P2].** Take the minimising D. Then χ′²_d(R̂_D) ≤ R̂_D + O_P(√R̂_D + d), so log odds(S0∖D : S0) ≥ (1 − κ_n + o_P(1))·Pr_n(d) → +∞ when limsup κ_n < 1. If √R_j − √(2 price) → c, then P(π(S0|y) ≤ ½) → Φ(−c).

**Finite-n companion [H → P target].**
- P(report = S0) ≳ [1 − (s0+1)/√(2πL(n+1))]·Π_D Φ(√R̂_D/σ − √(2Pr_n(d))).
- The superset term gives a ceiling of 0.94–0.97 for S1-like (n, p) (Fable [N]). Observed exact recovery is 0.92–0.98. **40 of the 41 S1 failures at SNR ≥ 2 are supersets of S0** (D1 E1/E7), so the residual "sufficiency gap" is this term, not a missing assumption.

### 3.4 TM-a0 [P, Fable Q6(3a)]
1. There are 2^{p_C} models. log m_S(y) = −(n/2 + a₀)log(2b₀ + Q_S) − (|S|/2)log(n+1) + O(1).
2. Q_S/n → σ_S² := min_b E(y − x_Sᵀb)² a.s. by the SLLN. **Uses A-MOM.**
3. Models missing supp β^C have σ_S² > σ_C² and lose exponentially fast.
4. Supersets: n(σ̂²_S − σ̂²_{S∪N})/σ̂² = O(log log n) a.s. by the LIL (needs E[x_j²u²] < ∞), against (m/2) log n.
5. Within the selected model, the conjugate N–IG posterior concentrates at (β^C, σ_C²). This gives Hellinger convergence to f₀ a.s. (SL's conclusion), plus exact selection.

### 3.5 TM-a, TM-b
Under A-MIS(iii), the candidate-only data satisfy A-GL with parameters (α_C, β^C, σ_C²). Apply TD (3.1) and TS-b (3.3) verbatim, with f₀ in place of f* and A-MARGIN-U in σ_C² units on μ_C = X_Cβ^C. C must not depend on the outcome data. The delivered `thm:omitted` is the special case with Gaussian rows, a fixed floor and diverging per-coefficient signal.

---

## 4. Anti-stringency ledger (each restrictive v3.1.1 assumption → weaker alternative → verdict)

| # | v3.1.1 assumption | why too strong | weaker alternative evaluated (with Fable/Astra) | verdict |
|---|---|---|---|---|
| 1 | c_id > c1(s0, A), an explicit constant (`asm:margin`) | large proof constant. S1 recovers at κ ≈ 2.5–2.8 (D1), far below c1 | A-MARGIN-U with constant 2(1+η) for deletions, plus the width term for added nulls. The converse shows 2 is sharp | **adopted** |
| 2 | FSb: fixed b_lo ≤ \|β\| | S1 has β ∝ √(log p/n), so FSb is false as a sequence (D1 E4) | κ_n framing over triangular arrays | **adopted** |
| 3 | p ≤ n^A | excludes exponential p, which SL cover (Cor 1) | DIM′ (log p)² = o(n) [P, Fable]; log p = o(n) with a cap (A-DIM″) | **conjecture TD′**. A-DIM″ needs an Engineering decision |
| 4 | EF: sample sparse eigenvalue floor (`thm:post-fixed`) | vacuous on S2: greedy floor 1e−5 to 2e−4 at m2 (D1 E5); SL call (22) "hardly satisfied" | population A-NEC (c_ψ/n) plus the A-SUBG isometry | **adopted** (sample floors demoted to a remark) |
| 5 | EFS / FLOOR-S0: fixed population floor | unnecessary: R_n(S0∖{j}) = nβ_j²Var(x_j \| rest) already enters the margin | drop it [P2] | **adopted** |
| 6 | A-BS per coordinate | "why bounded signals?" | A-BS′ aggregate energy | **adopted for new statements**; TD unchanged |
| 7 | memo MARGIN (uniform 2·d·price) | actually too *weak* in one direction (proxy counterexample) and too strong in another (charges d·price to swaps) | MARGIN-U / MARGIN\* | **replaced** |
| 8 | s0 fixed | — | growth remark: s0²·log p = o(n) | remark |
| 9 | Gaussian residual for TM | excludes non-Gaussian misspecification | (i′) with a cap; (ii) with a budget | remarks; TM-a0 covers moments-only at fixed p_C |
| 10 | SL Condition 3 as a separate assumption | redundant | implied by A-SUBG | **not assumed** |

---

## 5. Engineering sensitivity (corrected; supersedes TH_PREP §3 on the size prior)

Per-model prior odds of adding a variable at size k under BB(1, b): (k+1)/(p−k−1+b). The size-marginal ratio is (p−k)/(p−k−1+b).

| change | form invariant? | what moves | new condition |
|---|---|---|---|
| g (slab scale) | yes | price_g(k) = log[(2p−1−k)/(k+1)] + ½log(1+g). The TS-b threshold moves with it. Superset mass ≍ (s0+1)√(log p/g). The misspecification budget ϱ̄ < 1 + log(1+g)/(2 log p) | s0²·log p = o(g). Fixed g can prevent selection |
| g = max(n, p²) | yes | price ≈ 2 log p: more signal needed, fewer supersets | none |
| g = 4n or 9n (Engineering trials) | yes | the superset margin ω = price − log p rises by ½log g, so S1 superset losses fall. The empty-model margin on S2 falls | none. Matches perf/JOINT_PLAN: S1 losses fixed, 92–170 of 2,400 S2 fits lost (D1 E8) |
| BB(1, p^u), u < 1 | yes | price changes by ≤ log 2. **The 2^{−k} size tail is lost** | a cap K_n ≤ c·n log n/(log p)² (union route) |
| BB(1, p^u), u > 1 | yes | price + (u−1)log p; size tail p^{−(u−1)k} | none |
| Bernoulli(p^{−u}) independent prior | yes | per-variable price deficit (1−u)log p | (1−u)A < ½ (the TH_PREP condition belongs here) |
| PIP threshold q / HPM | yes | an O(1) shift log(q/(1−q)) | HPM: δ_post < ½. MPM_q: max\|PIP − 1\| < min(q, 1−q) |
| cap K | yes | — | K ≥ s0 + j0(n). K ≤ c·n/log p unlocks A-DIM″ |
| IG(a₀, b₀) | yes | constants only | none |
| data-free slab V = τ²I | **no** for TM | breaks the exact candidate reduction | re-derive |

---

## 6. Open items and risks
1. **TD′.** Astra has not re-checked Fable's DIM′ route; it stays a conjecture.
2. **TS-b\*.** The dichotomy lemma behind MARGIN\* ("separated proxies imply a joint proxy") is [C] (Fable Q1(3d)).
3. **Constants to audit.** The Paley–Zygmund constant c(L) (TS-a), the truncated-sum superset bound (TS-b step 2), and the Cramér range for TM (i′).
4. **Proofs not seen by Fable.** thm:dist and prop:dist: check that the size tail there is the Fubini argument and that A-BS is used only as in §2.
5. **Literature still NOT VERIFIED (PN).** The Chen & Chen 2008 primary text (paywalled; second-hand via Luo & Chen p. 7 and SBJ p. 14); the Bayesian Analysis 2017 labels of Grünwald–van Ommen; Song–Liang's "Lemma A.2" (not in the supplement we hold).
6. **Cheap evidence that would strengthen the package** (Fable): S1 cells at SNR 1.25 and 1.5 (κ just above 1); a per-cell comparison with the companion bound; a factor-proxy toy cell (ρ = 0.8). These need fits, so they need HQ approval and are not run here.
