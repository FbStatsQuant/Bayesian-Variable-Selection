# A4 outline: decisions after STYLE_A4_R1 (2026-11-17)

All of R1 is adopted:
- Seams: §3 closes with "What the results use from the method" (replaces D2 §2.2). Results are named "Result k (short name)" throughout §5. One sentence on the simulation studies goes in §1 and in §5.2. Code-level notes go from §2 to §3/App. B. Every cross-reference is a \ref.
- Vocabulary: "the method" = the algorithm; "the software" = the shipped code; "reported" for every output (not "printed").
- Notation renames on the method side:
  - burn-in rounds L → L_bi;
  - temperature φ → ξ, grid ξ_[t];
  - number of steps T → T_s, step ceiling T_i → T^max_i;
  - block table r_b → h_b;
  - discrepancy d(S) → Δ(S).
- Q1: results before assumptions; one "Scope" line per theorem, pointing to §5.4.
- Q2: shared assumptions in §4.1.
- Q3: Algorithm 1 goes to the supplement; the main text keeps five lines (frozen before the final run; a function of the data and its own random numbers; "succeeds").
- Q4: title "Consistency of a sequential Monte Carlo method for Bayesian variable selection, as implemented"; §3 heading "The method, as coded".
- Budget: 25 pp counted WITH status boxes on. Cuts as listed in (c)1–6. D1's six-predictor leakage example stays in §3.3, and its leakage set Q is named there.
- Repetition:
  - the scope of Results 3–4 lives in §5.4 only;
  - the mechanism is told once, in §3.3;
  - unbiasedness is stated only in §4;
  - §6 has no statuses;
  - each smaller duplicate is said once.
- Introduction: the seven items of (e).
- Gap for HQ: a reference list for related work (selection consistency, MCMC for BVS, SMC on binary spaces). No claims about uncited papers are drafted.
