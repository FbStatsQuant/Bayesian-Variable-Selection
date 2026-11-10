# Council C1 disposition (lead)

Seat A (gpt-6-astra high, `C1_council_astra.md`): 7.5, G1/G2/G3/G5 FAIL, G4/G6 PASS; 0 FATAL / 2 MAJOR / 6 MINOR / 1 NIT.
Seat B (Opus 5.5 high, `C1_council_opus.md`): 8.4, all gates PASS; 0 FATAL / 0 MAJOR / 4 MINOR / 7 NIT.
Round C1: NOT PASSED. Both seats: no defect in the proof chain, Lemma 1a′, or item 6's no-beta-min extension.

| # | Finding | Action |
|---|---|---|
| A-F1 MAJOR | rate optimality and the YWJ comparison overclaimed | FIXED: YWJ paragraph rewritten from arXiv:1505.07925 pp. 6–9 (prior (5), Assumptions A–D, Thm 1 uses D(s*) with no cap, Thm 2 the cap; rate 1 − c₁p⁻¹); growing-p optimality labelled CONJECTURE; NEW Proposition LB (`lemmas/LB_rate_lower_bound.md`) proves the deterministic lower bound 1 − π(S₀) ≥ (1 + √(n+1))⁻¹, so "sharp up to √log n" is now a theorem; falsification `numerics/lb_check_out.txt` (min ratio 1.013 over 34 920 cases). |
| A-F2 MAJOR | NH14 misrepresented | FIXED: rewritten from arXiv:1405.6545 pp. 5–6, 10–12 (Conditions 4.1–4.5 as printed; 4.4 residual-signal identifiability, 4.5 minimum NONZERO eigenvalue, singularity allowed; signal scale log(√n ∨ p_n); Thm 4.1). |
| A-F3 MINOR | Song–Liang qualifications | FIXED: Thm 1 vs Thm 2 settings separated; bounded/Gaussian qualifications for the Condition 3 eigenvalue implication; centred predictors for Condition 1; Condition 2 only analogous; cap objection restricted to p ≥ n/2; "prior alone" → "exact prior tail and reference-model bound". |
| A-F4 MINOR | REPORT drops coefficient / reference-size conditions | FIXED in REPORT v2 §1, §3 (θ_hi for automatic energy; t-based cutoff, O(log n) for fixed t; upper/lower bounds in the bridge and implication list). |
| A-F5 MINOR | numerical labels (medians, ranges, raw vs standardised coefficients) | FIXED: numerics regenerate the signal after standardising X (θ literal); all quotes are medians/frequencies over seeds, ranges re-read from the new output. |
| A-F6 MINOR | p = 12 exceeds the p ≤ 10 enumeration cap (Wave1 PROTOCOL:18) | FIXED: P_DEF = 10, full re-run; all quotes re-synced. |
| A-F7 MINOR | design family inside Theorem 1 | FIXED: item 6 is now the interface form; Gaussian rows moved to Corollary 1R (bridge example). |
| A-F8 MINOR | benchmark boundary terms | FIXED: n^{a+½−c/2+o_P(1)}; obstructions stated with a fixed margin; boundary cases not claimed; "deletion obstruction", not sufficiency. |
| A-F9 NIT | citecheck coverage overstated | FIXED: docstring now says "selected checks", lists exactly what is and is not checked. |
| B-F1 MINOR | stale numbers after the p = 10 re-run | FIXED (with A-F5/F6). |
| B-F2 MINOR | heuristic sharpness stated as fact | FIXED: beta-min order labelled "numerical + leading-order heuristic, not proved"; rate claim now rests on Proposition LB (proved) + conjecture for √log n. |
| B-F3 MINOR | p ≥ 2 unstated | FIXED: R1 is 2 ≤ p ≤ n^A; Lemma 1a assumes p ≥ 2. |
| B-F4 MINOR | counterexample unlabelled, weak analytic support | FIXED: labelled "COUNTEREXAMPLE (numerical, E5; leading-order analytic sketch, unchecked)"; leading-order computation for E5's own design added (proxy margin ≥ 0.48 log n); R03 §5A cited as mechanism only. |
| B-N1 | over-tight quotes | FIXED with re-sync (≤ 1.1·10⁻³; ranges from the p = 10 output). |
| B-N2 | cutoff sum without K | FIXED in REPORT. |
| B-N3 | missing qualifiers in REPORT | FIXED (θ_hi; (E) real for growing s₀; q_n condition). |
| B-N4 | L1a′ status line stale | FIXED: check record added; status word unchanged. |
| B-N5 | J_n(c) design-measurable | FIXED: sentence added to Corollary 1R(b). |
| B-N6 | "r_n ≻ 1" attribution | FIXED: now attributed to Theorem 2 (p. 953, where it is printed). |
| B-N7 | design family in Thm 1; "30–60×" basis | FIXED (A-F7); now "32–64× the rate obstruction 2a + 2 ∈ [2, 4]". |
