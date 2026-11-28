# COUNCIL R1 — OPUS seat (TH-SONG-ASSUMPTIONS, package v1.1, commit 5b62aaa9, branch dept/theory)

Reviewer: Opus 5.5 (independent seat; high effort). Read: the four package files, ASTRA_R1/R2, FABLE_R1 (the parts cited),
PRECEDENTS_NEW (errata first), S1_SL_CITATION_CHECK, `tables/`, `scripts/e1_margin.R`, SL main/supplement text and page
images, and manuscript `supplement.tex` (prop:dist, rem:sharp). Read-only apart from this file. Ran no R and no jobs; only
python3 arithmetic, with nothing written to disk.

## 1. Score table

| assumption | D | R | one-line reason |
|---|---|---|---|
| A-GL | 9 | 9 | Standard (SL (1) p. 947, NH14 4.3 p. 11, verified). Used everywhere, and the weaker forms are correctly demoted to remarks. |
| A-SPARSE | 9 | 9 | SL (4) p. 950 verified. The growth remark agrees with rem:sharp(a) (π(S) ≤ (1+(\|S\|+1)/(3√n))⁻¹ ⇒ s0 = o(√n)). |
| A-DIM | 9 | 8 | SBJ p. 14 and JR12 Thm 1 p. 651 verified. Needed for prop:dist(i) and the TD union bounds, and honestly kept for released statements. |
| A-DIM′ (conj.) | 8 | 5 | Honest: Astra R2's testing-step failure is reported, and the risk is marked high. The containment claims (Cor S1 range, Cor 1 for α < ½) check out. Sufficiency is unsupported by construction, which is correctly labelled. |
| A-SUBG | 7 | 8 | The proof-path role is right (isometry + conversion, not Cond. 3). The claim "bounded + variance bounded below ⇒ SUBG" is false on sparse directions (S4). SL Cond. 1 is absolute-scale, not Σ-relative. |
| A-NEC | 7 | 7 | It is a sufficient device and its necessity is honestly flagged as unproved. The "weaker than SL (26)/SBJ/NH14/BRT09" claims compare population with sample objects (S5). "Used in" omits the size lemma (S6). |
| A-BS (/A-BS′) | 8 | 8 | YWJ (7a) p. 7 verified (the ellipsis drops "in terms of the g-hyperparameter"). Correctly kept for TS-b because prop:dist(i) is proved under it. A-BS′ is honestly not adopted. |
| A-MARGIN-H | 8 | 8 | SL Cond. 3 p. 955 and the SLs p. 6 bound verified. The conversion formula 1−(1+R/(2nσ²))^{−1/4} is correct (I re-derived it). The data are honestly reported as weak. E2 uses a different d_H² formula (S7). |
| **A-MARGIN-U** | **6** | **5** | It has the right structure, and the deletion part (m = 0) is well supported and sharp. **But as written it is provably stronger than its own proof path needs for (D,m) with B_Dm ≤ 0. With the advertised width/squared forms it fails on S1 at SNR 2 and SNR 3. The data test only m = 0 (BLOCKER B1).** S2, S3 and S8 also hit D. |
| A-MIS(iii) | 8 | 8 | The reduction to A-GL is exact. The SL f₀ ((17)/(19), p. 957) and the centred/intercept reading are correct. The evidence is correctly limited (no hidden-column test). |
| A-MOM | 8 | 8 | SL Cond. 4 p. 957 and "fixed number of possible models" SLs p. 7 verified. The SLLN/LIL path is sound (O(log log n) against (m/2) log n). The n-dependent truth is excluded correctly. |

**Targets.** TD and TD-as hold up. TD′ is honestly a high-risk conjecture. TS-a and TM-a0 are low risk, as claimed. TM-a and TM-b
are low–medium risk given (iii). The TS-b converse is fine under A-NEC on T. TS-b's forward margin needs B1 fixed. TS-b* is
medium risk.

## 2. Overall score: **7.0 / 10**

The package is unusually honest about status, and it propagates the Astra R2 corrections consistently across all four files.
Its citations are accurate (every spot check passed except one page nuance). The 1-to-1 SL map (THEOREM_DEFINITIONS §2–§3)
is **complete**: Thms 1–4, Cors 1–2, Conds 1–5, Thm S, Cor S1, Lemma S2, Lemma 1.1/1.2, posterior (7)/EBIC, §6 and SAMC are all
present. It is **correct**, with the S1 audit fixes applied. One mapping statement needs softening: the claim "weaker than
SL's own replacement (26)" (S5). The score is held below 8 by one blocker on the central assumption (B1). There is also one
false evidence claim (S2) and one wrong count (S3).

## 3. SUBSTANTIVE / BLOCKER list

**B1 — BLOCKER. A-MARGIN-U is stronger than needed, and its advertised simple forms do not cover S1.**
Locations: ASSUMPTIONS §2 A-MARGIN-U (statement, the "squared form" bullet, (b) evidence); THEOREM_DEFINITIONS §4.2 TS-b
display and §3 row SL-6/7 ("covers S1 boundary signals"); DOSSIER A-MARGIN-U Q1 "plain form" and Q4.
- (i) *Stronger than needed.* Step 3 of §3.3 bounds the log odds of the class (D,m) by
  B_Dm − ½(√λ̂_S − w_Dm − t_n)₊² (in the package's notation, with B_Dm already containing +γ log n). If B_Dm ≤ 0, the class
  mass is O_P(n^{−γ}) with **no condition on R at all**: the containing-model credit (C log p/n)^{m/2} beats the deletion price.
  The stated condition √((1−δ)R/σ²) ≥ w_Dm + t_n + √(2(1+δ)[B_Dm]₊) still demands √R ≥ w_Dm + t_n when [B_Dm]₊ = 0. That
  quantifies the margin over every m ≤ J = s + C_s M. So the assumption depends on the inexplicit proof constant C_s and grows
  with M.
- (ii) *The advertised forms fail on S1.* At S1 (500, 500), SNR 2, the binding single deletion has R/σ² = 2·3.04·7.70 = 46.8
  (√ = 6.84), and Pr_n(1) = 7.70. With C = 1 and δ, γ, t_n → 0, using the combinatorial width √(2 log C(490, m)) that the package
  says "one may use outright":
  - m = 1: 3.52 + 3.32 = 6.84, which is equality, so it fails once t_n, δ, γ > 0;
  - m = 2: 4.84 + 2.58 = 7.42 > 6.84, so it fails.

  At SNR 3 (√R = 10.26) the combinatorial form fails for m ≥ 12 because of the m ≤ J quantifier. The "squared form"
  R ≥ 2(1+η)²(√d+√m)²σ²price fails at m = 3 even at SNR 3. The dossier's plain form "w ≈ √(2m log p)" therefore implies that S1
  is **not** covered. That contradicts THEOREM_DEFINITIONS §3 ("covers S1 boundary signals") and the dossier ("strongest
  evidence in the package").
- (iii) *Evidence covers only m = 0.* D1 computed κ_del, κ_multi and κ_swap/Λ heuristics (d·price, m log p), never w_Dm or
  the A-MARGIN-U inequality. "Holds on our data" is evidence for the deletion part only.
- **Fix.**
  - (a) Restate the quantifier as "for every (D,m) with D ≠ ∅ and B_Dm > 0": (√((1−δ)R_n/σ²) − w_Dm − t_n)₊ ≥ √(2(1+δ)B_Dm).
    Classes with B_Dm ≤ 0 are dispatched by the containing-model credit, inside the already-listed uniform-summation
    obligation. This bounds m by m*(d) ≈ 2Pr_n(d)/log(n/(C log p)) (for S1 (500, 500), d = 1: m ≤ 3) and removes the
    dependence on J and C_s. With the corrected quantifier and combinatorial widths, S1 at SNR 3 passes for d = 1, m = 1–3
    (6.84, 7.42 and 7.27 against 10.26). SNR 2 still needs the actual widths.
  - (b) Say plainly that the combinatorial and squared forms are worst-case (factor-proxy) forms and do not cover S1 at SNR 2.
    Coverage there rests on the design-specific conditional width, which is plausibly small for AR(1) because v_S barely
    depends on far-away N.
  - (c) Either compute w_D1, w_D2 and w_D3 on S1 by Monte Carlo over X and g (no fits needed; ≪ 1 CPU-h, a D1-type job), or
    label the mixed-rival part "not evaluated on S1/S2".
  - (d) Change "w_Dm ≈ √(2m log p)" in the plain forms to "w_Dm ≤ √(2 log C(p−s0, m)) ≈ √(2m log p) in the worst case".

**S2 — SUBSTANTIVE. "E K₁ matches the order of the (s0+1)√(log p/n) rate term" is false.**
Locations: SIMULATION Lead synthesis 2, last sub-bullet; DOSSIER A-MARGIN-U Q4 ("It matches the order of the
(s0+1)√(log p/n) term in TS-b's rate").
- E K₁ ≈ (s0+1)/√(2πL(n+1)) scales as (s0+1)/√(nL). The rate term, and the rem:sharp(b) lower bound
  (s0+1)√(log(p√n/(s0+1))/(πn)), scale as (s0+1)√(L/n). They differ by a factor ≍ L.
- On S1, (s0+1)√(log p/n) = 0.87–1.44 while E K₁ = 0.03–0.06. That is a 20–40× gap, so the TS-b mass display is vacuous at
  S1 sizes.
- They measure different events: posterior mass versus the count of extensions whose score beats S0.
- **Fix.** Delete the "matches the order" sentences. Say that the TS-b mass bound is not informative at S1's (n, p), and that
  E K₁ is a mode-type (HPM/MPM) diagnostic.

**S3 — SUBSTANTIVE (number). DOSSIER A-MARGIN-U Q4: "9 of 11,466 fits on S2" should be "9 of 10,666".**
`e1_2x2_predictors.tsv`, S2, P1_sample: no_exact 9 + no_notexact 10,657 = 10,666, so P = 0.00084, matching the "≤ 0.0008"
elsewhere.

**S4 — SUBSTANTIVE. "Bounded predictors with variance bounded below imply A-SUBG" is false for the Σ-relative sparse-direction form.**
Locations: ASSUMPTIONS A-SUBG "Weaker alternatives"; DOSSIER A-SUBG Q6.
- A-SUBG bounds ψ₂(uᵀζ)² by L²·Var(uᵀζ) for q_n-sparse u. A-NEC allows Var(uᵀζ) ≥ c_ψ/n only.
- A bounded contrast such as x₁ − x₂ (rare large values, tiny variance) has unbounded ψ₂²/Var.
- Even with a fixed sparse floor ψ, Hoeffding gives only L² ≲ q_n B²/ψ, which grows with q_n ≍ log n. TD needs a fixed L.
- **Fix.** Replace the claim with "bounded predictors satisfy the per-coordinate version. The sparse-direction relative version
  needs a further condition (e.g. independent coordinates, or Gaussian-type dependence)." In the defence line, also note that
  SL Condition 1 is an absolute-scale exponential moment with \|a_i\| ≤ δ, not Σ-relative: "same type, different normalisation".

**S5 — SUBSTANTIVE (mischaracterised comparison). The A-NEC "weaker than" claims are stated as dominance.**
Locations: ASSUMPTIONS A-NEC Defence (a) ×2; DOSSIER A-NEC Q3 ("weaker than every verified precedent"); THEOREM_DEFINITIONS §3
row SL-6/7 ("weaker than SL's own replacement (26)").
- SL (26), SBJ A4 and NH14 4.5 are sample (or two-sided) spectral conditions, on other set sizes, and they do not separately
  require sub-Gaussian rows.
- Ours is a population lower floor that only works together with A-SUBG (for transfer). As a *floor value* c_ψ/n is smaller:
  λ_min concavity gives a population floor ≥ l_n ≫ log P_n/n from (26) + (23). As a *condition set* it is not a dominance, which
  is the same caution Astra R2 gave for NH14.
- **Fix.** Use "a weaker floor value on a population object, used together with A-SUBG; not a uniform dominance" (the dossier's
  §"SL's Theorem S" wording already does this).

**S6 — SUBSTANTIVE (relevance accounting). A-NEC "Used in" omits the size lemma.**
- prop:dist(i) (supplement.tex l. 161ff.) is proved under asm:dist including (d) = A-NEC. Without it, prop:dist(ii) gives
  s + C_s M log n, not s + C_s M.
- So TS-b's bounded-size event, and the TD sieve, use A-NEC. "No floor is needed for sufficiency" is true only for step 1.
- **Fix.** Add "(iii) the size lemma prop:dist(i) and the TD tests" to A-NEC "Used in" (ASSUMPTIONS §2, DOSSIER Q2). Scope the
  "no floor" sentence to the deletion step.

**S7 — SUBSTANTIVE (minor; conclusion unchanged). E2's "Gaussian d_H² version" is not the package's conversion formula.**
- `scripts/e1_margin.R:89` uses 1 − (1 + r/4)^{−1/2}, which is the fixed-variance (τ = σ) affinity.
- TS-a §3.2 (correctly) uses the variance-optimised 1 − (1 + r/2)^{−1/4}, which is smaller. So the E2 ratios 0.006–0.21
  overstate the separation.
- **Fix.** Relabel the column "τ = σ (upper bound)", or recompute with the optimised formula. The weak-evidence verdict only
  strengthens.

**S8 — SUBSTANTIVE (minor). The data κ is not the theorem's κ_n.**
- D1's κ(S) = R/(2σ²·d·price(s0−1)), and κ_pop also includes swaps scored without width or credit.
- THEOREM_DEFINITIONS defines κ_n with Pr_n(d) = Σ price(k) over deletions only. Since price(k) decreases in k, κ_n ≤ κ_data;
  on S1 (d = 3) the difference is ≈ 1.4% (e.g. Pr_n(3) = 23.44 against 3·7.70 = 23.11 at (500, 500)).
- **Fix.** Add one sentence in SIMULATION §0 and ASSUMPTIONS A-MARGIN-U (b): "data κ uses d·price(s0−1); κ_n is ≤ 2% smaller
  on S1; the bracket (0.64–0.70, 2.54–2.80) is unchanged". Call the S1 numbers κ_multi (κ_swap = κ_del on S1), not κ_pop, when
  comparing with κ_n.

No other blocker. TD′, TS-b*, the converse, TM-a0 and the Engineering-sensitivity corrections (§5) are stated with correct
status and risk.

## 4. NITPICK list (no score effect)

1. THEOREM_DEFINITIONS header still says "Draft v1"; the other three files say v1.1.
2. SIMULATION E1 table caption says "Medians over settings", but the cells are min–max ranges.
3. SIMULATION Lead synthesis 2: "P(exact | κ_del ≤ 1) = 0 (S1) / ≤ 0.0008 (S2, sample)" mixes the population κ_del row with
   the P1-sample row. The population row gives 0 on S2 too.
4. "8.8–250× c_ψ/n" (ASSUMPTIONS, DOSSIER, SIMULATION) presumes c_ψ = 1. Say "n × floor = 8.8–250".
5. THEOREM_DEFINITIONS §1: "price … on S1/S2 this is 7.5–10 nats". The recomputed range is 7.3–10.4.
6. SIMULATION uses ε_n = √(s0 log p/n) (P2's choice), not the TD radius √(M log n/n). Add a label where ratios to ε_n² are
   quoted as evidence for A-MARGIN-H.
7. A-GL defence: Jiang (2007) is a GLM paper with bounded covariates. The i.i.d. random-design description is on arXiv
   pp. 2–3 and 6; p. 7 is Thm 1.
8. YWJ quote: restore "in terms of the g-hyperparameter" or mark the elision. YWJ's bound is relative to g.
9. TM-a0 "raw units with an intercept": clarify that this means the coded centring (the plug-in ȳ, x̄; there is no intercept
   parameter with a prior).
10. The A-MARGIN-U constant C in log(n/(C log p)) is never pinned. Name it as the truncation constant of the superset step.
11. SIMULATION "Files produced" names `SIMULATION_DATA_ANALYSIS_draft.md` (a stale name). The DOSSIER cites
    `COUNCIL_RECORD.md`, which does not exist yet.
12. Optional (from the S1 audit): give SLs Lemma 1.2 (De Blasi–Walker) its own SL-map row.
13. Optional: A-MARGIN-U takes w_Dm(X) conditional on the design. State once that the assumption is "with design probability
    1 − o(1)", so readers do not take it as a population condition, unlike R_n.

## 5. Spot checks

**Citations** (against `.rc_tmp/song/papers/*.txt` with form-feed page counting; journal page = PDF page + 946; images where noted)

| # | claim in package | result |
|---|---|---|
| 1 | SL p. 950: P_n ≻ n^θ, a lower bound (Lead erratum E1) | ✓ "Pn ≻ nθ … bn ≻ an means an/bn → 0" |
| 2 | SL Cond. 3, p. 955, j_i ≠ k, δ_n ≻ ε_n² | ✓ PDF p. 9 = journal 955 |
| 3 | SL Cond. 4 / Thm 4 / Cor 2 (unnumbered display) / (19), p. 957; Cond. 5 and remark (b), p. 958 | ✓ all on the stated pages; the Cor 2 display is unnumbered; the "if and only if β0,t ≠ 0" prose follows it |
| 4 | SLs p. 6: d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}; Lemma 1.2 p. 6; SLs p. 7 "fixed number of possible models" | ✓ |
| 5 | SLs p. 15 "(22) is hardly satisfied"; (26) p. 15; Fan & Lv A.7 and "Lemma A.2 of the Appendix" p. 16; Cor S1 P_n < n^{κ log n} p. 16 | ✓ (Lemma A.2 absent from the supplement, as the package says) |
| 6 | SL p. 960: γ = 0.75, a₀ = b₀ = 1, τ = 0.01 | ✓ |
| 7 | NH14 Cond. 4.4 p. 11, 5σ²\|t\|(1+δ)log(√n ∨ p_n); Lemma 6.1 p. 16 | ✓ |
| 8 | JR12 Thm 1 p. 651, p ≤ n | ✓ (page image; note JR12 also assumes a fixed eigenvalue floor λ_p(X′X) > nc) |
| 9 | SBJ p. 14 "continue to hold when p grows polynomially" | ✓ |
| 10 | Wainwright 2009 Thm 2 p. 4; FRG Thm 1 p. 4 (constant derived) | ✓ (FRG display (6) is in measurement form; the 2σ² log p reading is C2's derivation and is correctly flagged) |
| 11 | YWJ (7a) p. 7 | ✓ (the quote is elided; nitpick 8) |
| 12 | Rossell non-centrality, arXiv v7 p. 10; Luo & Chen Consistency Condition p. 7 | ✓ |
| 13 | Jiang 2007 p. 7 for i.i.d. random design | partial (nitpick 7) |

**Numbers** (against `tables/`, plus my own recomputation)

| # | number in package | table / recomputation | result |
|---|---|---|---|
| 1 | κ_pop 0.64–0.70 (SNR 1), 2.54–2.80 (SNR 2); exact 92–96/100 | `e1_s1_cells.tsv`: 0.636/0.664/0.677/0.700; 2.543/2.657/2.708/2.801; 0.92/0.94/0.96/0.94 | ✓ |
| 2 | AUC κ_pop 0.958 vs κ_del 0.980 (S2); Λ 0.967; 0.845 vs 0.923 (ν ≥ 2.07) | `e1_auc.tsv`: 0.9583, 0.9798, 0.9666, 0.8447, 0.9230 | ✓ |
| 3 | P1-sample S2: "9 of 11,466" (DOSSIER) / "≤ 0.0008" | `e1_2x2_predictors.tsv`: 9/(9+10,657) = 9/10,666 = 0.00084 | ✗ in the DOSSIER (S3); ✓ elsewhere |
| 4 | max\|β\|sd/σ ≤ 1.17 (S1), 1.10 (S2); ν ≤ 6 | `summ_E4.tsv`: 1.1746, 1.0954, 3.94/6.00 | ✓ |
| 5 | n × floor 8.8–250 | `summ_E5.tsv`: 8.82 … 250 | ✓ |
| 6 | κ_eff 0.13–0.22 (S1), 0.33–0.45 (S2) | `e6_S1S2_regimes.tsv`: 0.130–0.221; 0.326, 0.451 | ✓ |
| 7 | 40/41 S1 failures at SNR ≥ 2 are supersets (39 with one null) | `e7_failure_composition.tsv`: 0.9756 × 41 = 40; 0.9512 × 41 = 39 | ✓ |
| 8 | screening ratio ≥ 1 in 9/136 | `e1_margin_by_setting.tsv`, e2_over_eps2 ≥ 1: 9 of 136 | ✓ |
| 9 | ω = price − log p = 1.49–1.84 | recomputed: 1.49, 1.50, 1.83, 1.84 | ✓ |
| 10 | E K₁ = 0.033–0.056 "from" (s0+1)/√(2πL(n+1)) | not in `tables/`. The displayed formula gives 0.031–0.050, and (p−s0)·2Φ(−√L) gives 0.029–0.047. 0.033–0.056 is Fable's exact-Beta value (FABLE_R1 l. 165) | ✗ attribution: cite the exact-Beta computation, or quote 0.03–0.05 (fold into S2) |
