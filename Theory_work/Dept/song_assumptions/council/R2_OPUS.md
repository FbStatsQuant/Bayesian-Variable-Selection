# COUNCIL R2 — OPUS seat (TH-SONG-ASSUMPTIONS, package v1.2, commit 7c7ca30f, branch dept/theory)

Reviewer: Opus 5.5 (independent seat; high effort).
- **Read:** COUNCIL_RECORD.md, my R1_OPUS.md, the four package files in full, `scripts/e9_width_mc.py`, `tables/e9_width_s1.tsv`,
  `logs/e9_width_mc.log`, the harness `generate.R` copy (`.rc_tmp/song/s1s2_ro/`), P17 B6, and the SL/NH14/YWJ/LC13/Rossell texts.
- **Writes:** read-only apart from this file.
- **Run:** one single-threaded extension of E9 (`nice -n 10`, OMP/OPENBLAS = 1, ≈ 1 CPU-min). Script
  `.rc_tmp/opus_r2/e9x.py`, output `.rc_tmp/opus_r2/e9x_snr2.tsv`. It covers d = 1–3, m = 1–2, at three values of the credit
  constant C.

## 1. Score table (nitpicks excluded from scores)

| assumption | D | R | one-line reason |
|---|---|---|---|
| A-GL | 9 | 9 | Exact score, Fubini (fixed-endpoint contrast density) and Beta law are correctly separated. Scope "not TM-a0" is right. Fixed- vs random-design precedents are distinguished. |
| A-SPARSE | 9 | 9 | SL (4) p. 950. Thm 4 is correctly said to use a fixed subset plus Cond. 4, not (4). The growth claim is hedged. |
| A-DIM | 9 | 9 | The TD hierarchy (coarse window absorbed by the isometry exp(−cn), then localisation to J, then testing) is now explicit and correct. E6 is labelled as finite-n ratios. |
| A-DIM′ (conj.) | 9 | 9 | Status (high-risk conjecture; the route fails at testing; no impossibility) and reasons are correct. (s+1) fixes s = 0. The containment claims check out ((log p)² = κ²(log n)⁴ = o(n) on Cor S1's range). |
| A-SUBG | 9 | 9 | The counterexample is correct: Var(B) ≍ 1/n while ψ₂²(B) ≍ 1/log n, so ψ₂²/Var → ∞. SL Cond. 1 is absolute-scale ("\|a_i\| ≤ δ", p. 953, re-read). Two-sided isometry on (s0+J)-sets. |
| A-NEC | 8.5 | 9 | "Used in" is now complete: Occam factor, size lemma, TD tests, converse. The comparison is reframed correctly, but one sentence contradicts the NH14 bullet just above it (S-2). |
| A-BS / A-BS′ | 9 | 9 | The YWJ quote is restored ("in terms of the g-hyperparameter", p. 7, re-read). The growth caveat for YWJ/SC11 is stated. A-BS′ "recorded, not adopted" is the correct status, for the correct reason (size lemma). |
| A-MARGIN-H | 9 | 9 | The window is min(K, J), inside the SUBG window. c′_H < c_H. E2 is relabelled as a τ = σ upper bound and a restricted-search scale diagnostic. |
| **A-MARGIN-U** | **8.5** | **8.5** | The B_Dm > 0 quantifier is right, the worst-case forms are labelled, and E9 is honest and reproducible. Two fixable points remain. Step 3's log-odds display does not give the B_Dm ≤ 0 dispatch as written (S-1). The "m ≤ 3 active" example and the E9 surpluses use C = 1, but the package's own step 2 implies C ≍ (s0+1)² (S-3). My rerun shows the conclusion survives. |
| A-MIS(iii) | 9 | 9 | Σ_CC nonsingularity is added, with the I − 11ᵀ/p_C example. Omission-only. E7 is in-sample on the selected MPM. GvO scope is corrected. |
| A-MOM | 9 | 9 | One fixed law, p_C ≥ 2, eventually untruncated BB(1, p_C), coded centring. The exceptional event is eventually empty a.s. (Borel–Cantelli on constant columns). Mixed score moment E[Z_j²u²]. |

**Targets.** TD, TD-as, TS-a and TM-a0 are low risk, as stated. TM-a and TM-b are low–medium. The TS-b converse is correct under A-NEC on T.
TS-b forward is sound once S-1 is fixed. TD′ is correctly labelled a high-risk conjecture. MARGIN\* is correctly demoted.

## 2. Overall score: **8.6 / 10** (R1: 7.0)

The revision fixes all five R1 blockers, carries every adopted point into all four files, and introduces no new blocker.
The **1-to-1 SL map** (THEOREM_DEFINITIONS §2–§3) is **complete**: SL-0 … SL-13, with Thms 1–4, Cors 1–2, S1, Conds 1–5, Thm S,
Lemma 1.1/1.2, Lemma S2, (7)/EBIC, §6 and SAMC. It is **correct**: the SL-3/SL-4 partial-analogue labels, the SL-6/7 non-dominance
wording and the SL-9 "inclusion only" reading are all right. I accept the decline of the separate Lemma 1.2 row: it is
catalogued inside SL-8 and SL-8's mapping is unaffected. Three substantive points remain, all minor and each fixable in 1–3
lines (§3).

## 3. Blocker resolution (R1 B-1 … B-5)

| # | blocker | verdict | reason (checked where) |
|---|---|---|---|
| B-1 | A-MARGIN-U binds on B_Dm ≤ 0 classes; C unnamed | **Resolved** (with S-1) | The quantifier is "D ≠ ∅, m ≤ J, B_Dm > 0" in ASSUMPTIONS §2, DEFINITIONS TS-b, DOSSIER Q1 and §4 row 11. The dispatch argument is correct: S ⊂ U gives RSS_S ≥ RSS_U, Q_U − RSS_U = O_P(σ²), the deletion refund against U is ≤ e^{Pr_n(d)}, and the containing-model sum is O_P((C log p/n)^{m/2}). C is named as the truncation constant of step 2. §3.3 step 3 states the bound with the wrong accounting (S-1). |
| B-2 | the worst-case forms fail on S1 at SNR 2; evidence only for m = 0 | **Resolved** (with S-3) | Both forms are labelled worst-case and the R1 arithmetic is quoted. The design-event quantifier is stated. E9 exists, runs in ≈ 2 CPU-min and matches its table (§5). I checked the inputs against `generate.R`: S0 = 1..10, σ² = 1, AR(1) ρ = 0.6, the COEF pattern. The width code computes E_g max_N(−⟨v_S, g⟩) exactly as defined. d ≥ 2 and m = 3 are honestly marked not evaluated. My rerun covers d = 2, 3 (m ≤ 2): surplus ≥ 3.5 (§3 S-3). |
| B-3 | A-NEC "weaker than every precedent"; SL (26) "fixed-type" | **Resolved** (with S-2) | The object/scale/window comparison is in ASSUMPTIONS A-NEC (a), DOSSIER Q3 and DEFINITIONS SL-6/7. The descriptions of SBJ A4 (minimum nonzero sample eigenvalue, P17 B6), NH14 4.5 ("exactly zero" allowed, p. 17, re-read) and SL (26) ("vanishing two-sided sample", SLs p. 15, re-read) are accurate. One leftover sentence contradicts the NH14 bullet (S-2). |
| B-4 | raw-unit map; input domain; TM-a0 p_C = 1; prior convention | **Resolved** | The DEFINITIONS §1 raw-unit map β_j = s_y b_j/s_{x_j}, σ² = s_y²v is correct for the coded scaling. Undefined posteriors are placed in the exceptional event (TD path, TM-a0). TM-a0/A-MOM have p_C ≥ 2, K = p_C once ⌊n/2⌋ ≥ p_C, and coded centring. |
| B-5 | TS-b\* has no testable statement | **Resolved** | It is demoted to "MARGIN\* (open refinement)" in DEFINITIONS §4.2, ASSUMPTIONS §2 / §6.2 / §4 row 7, and DOSSIER weak point 3. No file lists it as a target. |

R1 substantive points S2–S8 (mine) are all applied correctly in all files: E K₁ no longer "matches the order";
9/10,666; the bounded⇏SUBG counterexample; the "Used in" size lemma; the E2 τ = σ label; the κ_n vs data-κ (≤ 1.4%) note.
**Concession:** my R1 nitpick N5 ("7.3–10.4") was wrong. The P1 price over the actual settings is 7.60–10.36
(`e1_margin_by_setting.tsv`); its minimum is at S2 n = 100, s0 = 10. The Lead's partial decline was right.

### New / remaining SUBSTANTIVE points (no BLOCKER)

**S-1 — SUBSTANTIVE (proof-path display; minor). TS-b step 3 bounds the class log odds by "B_Dm − ½(√λ̂_S − w_Dm − t_n)₊²", but
B_Dm already contains +γ log n.**
- *Location:* ASSUMPTIONS §3.3 step 3 (first sentence), together with the step's B_Dm ≤ 0 clause.
- *Problem:* as written, the display gives log odds ≤ 0 (mass O_P(1)) on classes with B_Dm ≤ 0. On classes with B_Dm > 0 it gives
  only −δB_Dm, i.e. a rate n^{−δγ}. Neither is the claimed O_P(n^{−γ}). The *statement* of A-MARGIN-U (§2: "their mass is
  O_P(n^{−γ})") is correct, so this is an accounting slip in the sketch, not in the assumption. It matters because this sentence is
  exactly the B-1 dispatch.
- *Fix:* write the bound as Pr_n(d) − (m/2)log(n/(C log p)) − ½(√λ̂_S − w_Dm − t_n)₊² + O_P(1) = B_Dm − γ log n − ½(…)₊² + O_P(1).
  - B_Dm ≤ 0 then gives ≤ −γ log n + O_P(1).
  - B_Dm > 0 with A-MARGIN-U and the R-transfer gives ½(…)² ≥ (1+δ)B_Dm, hence ≤ −γ log n − δB_Dm + O_P(1).
  - The O_P(1) collects the Q_U − RSS_U and IG-rate terms.

**S-2 — SUBSTANTIVE (wrong statement introduced in the B-3 fix; minor). "As a floor value on full-rank sets, c_ψ/n is smaller
than each of these."**
- *Location:* ASSUMPTIONS A-NEC Defence (a), last sub-bullet; DOSSIER A-NEC Q3, last bullet.
- *Problem:* two lines earlier, both files say correctly that NH14's floor ≳ p_n^{−κ} "can be smaller than c_ψ/n at large p"
  (also P17 B6: "may be lower than ours when p is large"). The summary sentence contradicts them.
- *Fix:* "…is smaller than the BRT09, MY09, SBJ and SL (26) floors; NH14's p_n^{−κ} can be smaller still at large p."

**S-3 — SUBSTANTIVE (evidence calibration; does not change the conclusion). The "active m" example and the E9 surpluses use
C = 1, but the package's own superset step implies C ≍ (s0+1)².**
- *Locations:*
  - ASSUMPTIONS A-MARGIN-U statement ("e.g. m ≤ 3 for d = 1 at S1's (500, 500)") and (b) E9 bullet ("surplus ≥ 3.29");
  - DOSSIER A-MARGIN-U Q1 and Q4;
  - DEFINITIONS TS-b ("surplus ≥ 3.29");
  - SIMULATION E9 ("B_D3 > 0 at S1's sizes") and synthesis 2.
  The example is mine (R1 B1 fix (a), with C = 1), so this corrects my own R1 arithmetic.
- *Problem:*
  - Step 2 gives a one-null mass O_P((s0+1)√(log p/n)), and the same step defines C through the sum O_P((C log p/n)^{m/2}).
    At m = 1 these agree only if C ≍ (s0+1)², i.e. ≈ 121 on S1, before the truncation factor.
  - Then log(n/(C log p)) = −0.41, +0.29, −0.72, −0.03 at (500, 500), (1000, 500), (500, 5000), (1000, 5000). At S1 sizes the
    containing-model credit is therefore ≈ 0 or negative. This is the same fact as "the rate term is 0.87–1.44, not informative
    at S1".
  - Consequences: B_Dm > 0 for every m ≤ J, so the m*(d) cap is an asymptotic statement, not a description of S1. The m ≥ 3
    classes are active and unevaluated on S1. The quoted surpluses are optimistic by ≈ 0.6 (m = 1) and ≈ 1.4 (m = 2).
- *My rerun* (`.rc_tmp/opus_r2/e9x.py`; 4 designs × 200 draws; the 3 lowest-√minR D per (d, m)). At SNR 2, the minimum surplus
  √(min R/σ²) − w_Dm − √(2B_Dm) over all four cells is:

  | (d, m) | C = 1 | C = 121 | no credit (B = Pr_n(d)) | w_Dm(X) range |
  |---|---|---|---|---|
  | (1, 1) | 3.25 | 2.59 | 2.58 | 0.08–0.34 |
  | (1, 2) (p = 500) | 3.85 | 2.40 | 2.50 | 0.23–0.41 |
  | (2, 1) | 4.25 | 3.81 | 3.79 | 0.14–0.33 |
  | (2, 2) (p = 500) | 4.50 | 3.58 | 3.64 | 0.31–0.45 |
  | (3, 1) | 4.22 | 3.87 | 3.85 | 0.14–0.37 |
  | (3, 2) (p = 500) | 4.52 | 3.78 | 3.81 | 0.27–0.41 |

  My C = 1, d = 1 values reproduce E9 within Monte Carlo error (e.g. j = 3, m = 1 at (500, 500): 3.25 vs 3.33).
- *Fix:*
  - (a) Say that the m ≤ 3 example and the E9 surpluses are at C = 1, γ = 0. Add "at S1 sizes the credit is ≈ 0
    (C ≍ (s0+1)²), so all m ≤ J are active there; the cap m*(d) is asymptotic".
  - (b) Quote E9's surplus also at no credit (≥ 2.4 at SNR 2 for d ≤ 3, m ≤ 2, from this rerun or a rerun of `e9_width_mc.py`
    with B = Pr_n(d)). Keep "m ≥ 3 not evaluated".
  - (c) In the DOSSIER Q1 plain form ("on realistic correlated designs") and the DEFINITIONS plain English ("much smaller on
    typical designs"), say "on S1's AR(1) designs". E9 tests one design family.

No other new error found. In particular: the B_Dm ≤ 0 dispatch logic, the m*(d) formula, the E9 code, the E K₁ numbers
(0.031–0.050 recomputed), the rate-term range (0.87–1.44 recomputed), the A-SUBG counterexample and the TM-a0 domain are all
correct.

## 4. NITPICK list (no score effect)

1. SIMULATION E9 table: the (500, 500) SNR 2, m = 1 minimum surplus is printed 3.30, but the TSV has 3.2946 (the text says ≥ 3.29).
   The (1000, 500) m = 1 width range is printed 0.11–0.32, but the TSV minimum is 0.1046.
2. "≥ 6.7 at SNR 3": the TSV minimum is 6.696. Use "≥ 6.69" or "≈ 6.7".
3. A-MARGIN-U w_Dm bullet: the phrase "(choosing a smaller number is not enough)" is unclear. Suggest "(a bound must hold on the
   design event; a heuristic estimate does not suffice)".
4. E9 reading "because v_S barely depends on far-away nulls": the mechanism is generic, not AR(1)-specific. With no null
   population-correlated with the residual direction, v_S moves by O(√(log p/n)) across N, and a heuristic gives
   w_D1 ≈ (log p)/√n (≈ 0.28 at (500, 500)), which matches E9. This is optional and would support the S-3(c) wording.
5. DEFINITIONS TS-b bullet 2 still says "Proof obligation: a uniform summation over m ≤ J", while ASSUMPTIONS §3.3 step 2 and
   §6.3 say it is a finite union at fixed M. Align the wording.
6. COUNCIL_RECORD B-2 row: "≥ 3.29 … for every d = 1 class" should read "for every d = 1, m ≤ 2 class", since m = 3 is not evaluated.

## 5. Spot checks

**Citations** (text extraction with form-feed page counting, journal page = PDF page + 946; PDF pages for the arXiv texts)

| # | claim | result |
|---|---|---|
| 1 | SL Cond. 1, p. 953: absolute-scale, "\|a_i\| ≤ δ", r ≤ r̄_n (A-SUBG "same type, different normalisation") | ✓ |
| 2 | SL Cor 1, p. 954: P_n < exp(Cn^α), α ∈ (0, 1), strict sparsity (4) | ✓ |
| 3 | SL Cond. 4 and Thm 4, p. 957: E{(aᵀx_s)²} < ∞ for \|a_i\| ≤ δ; Thm 4 for a fixed subset | ✓ |
| 4 | SL p. 960: a₀ = b₀ = 1, τ = 0.01, λ_s = \|s\|^{−γ} | ✓ |
| 5 | SLs p. 15: "(22) is hardly satisfied" and the feasible (26) condition on \|ζ\| = r̄_n + \|t\| with failure probability e^{−nC} | ✓ |
| 6 | SLs p. 7: "only a fixed number of possible models" (A-MOM defence) | ✓ |
| 7 | SLs p. 16: "Lemma A.2 of the Appendix" (ridge variant); Cor S1 P_n < n^{κ log n}, κ ∈ (0, ¼) | ✓ |
| 8 | NH14 Cond. 4.4, PDF p. 11: Δ_n(K) > 5σ²\|t\|(1+δ)log(√n ∨ p_n); Cond. 4.5 p. 11; "exactly zero" p. 17 | ✓ |
| 9 | YWJ p. 7: "…in terms of the g-hyperparameter is required" | ✓ (now quoted in full) |
| 10 | Luo & Chen consistency condition, PDF p. 7; Rossell non-centrality, PDF p. 10 | ✓ |

**Numbers** (against `tables/`, plus my own recomputation)

| # | number in package | table / recomputation | result |
|---|---|---|---|
| 1 | S2 sample P1 "no": 9/10,666 = 0.00084; pooled 9/11,466 | `e1_2x2_predictors.tsv`: S2 9 + 10,657; "all" 9 + 11,457; 0.000844 | ✓ |
| 2 | price range 7.6–10.4 (P1 convention) | `e1_margin_by_setting.tsv` `price`: 7.600–10.361 | ✓ (my R1 N5 was wrong) |
| 3 | n × floor 8.8–250 | `summ_E5.tsv`: 8.82 (S2 ρ = 0.7) … 250 (S1) | ✓ |
| 4 | max\|β\|sd/σ ≤ 1.17 / 1.10; ν ≤ 3.94 / 6 | `summ_E4.tsv`: 1.1746, 1.0954; 3.938, 6 | ✓ |
| 5 | κ at SNR 1 (500, 500) 0.66, exact 0 | `e1_s1_cells.tsv` S1_02: κ_pop 0.6644, exact_share 0 | ✓ |
| 6 | E9 widths 0.10–0.47 (m = 1), 0.22–0.59 (m = 2); SD ≤ 0.12; surplus ≥ 3.29 (SNR 2); w_comb 3.52/4.13/4.84 | `e9_width_s1.tsv`: 0.1046–0.4703; 0.2156–0.5937; max SD 0.1208; min 3.2946; ✓ | ✓ (rounding nitpicks 1–2) |
| 7 | Pr_n(3) = 23.44 at (500, 500); m*(1) = 3 at C = 1 | recomputed 23.442; 2·7.703/log(500/6.215) = 3.51 → 3 | ✓ (at C = 1 only; S-3) |
| 8 | E K₁ 0.031–0.050; rate term 0.87–1.44 | recomputed 0.0503 (500, 500), 0.0306 (1000, 5000); 0.867, 1.436 | ✓ |
| 9 | √(min R/σ²) binding = 6.84 (p = 500), 8.01 (p = 5000) at SNR 2 | 2·0.1115²·4·500·0.4706 = 46.8 → 6.84; TSV 8.0081 | ✓ |
