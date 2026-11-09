# R07 disposition (exhaustive sweep, Codex Sol xhigh: 0 fatal / 1 major / 5 minor / 5 editorial)
Reviewer reply verbatim: reviews/R07_sweep_sol.md; scratch reviews/R07_scratch/. All 11 fixed:
1 (MAJOR) implementation handoff: METHOD_REQUIREMENTS "Implementation" rewritten as option plumbing (v3_run.R:101 distinct
  values; v3_core.cpp:394,404 enum/string; 473 cap; 479 label; v3_fit.R:44 and call sites 114–115, 145 rule-specific
  worst case) or explicit global replacement.
2 (MINOR) example rule now max(ℓ_n, ⌈1.001|S̃₀|⌉) in STATEMENT (P5).
3 (MINOR) table wording: "largest of the linear-in-mode allowances; dominates when |S̃₀| = K".
4 (MINOR) L2.5 remark: observed M_W ≈ 0.484–2.723, separated from the asymptotic bound.
5 (MINOR) 24-hour outcome labelled as extrapolation from the recorded charge (STATEMENT (P6), METHOD_REQUIREMENTS).
6 (MINOR) "ŝ_K grows with K" removed (dependence on K not measured).
7 (EDITORIAL) METHOD_REQUIREMENTS cites STATEMENT v3.1.
8 (EDITORIAL) REPORT.md written (status inventory §3, p ≫ n heuristic §5, design-agnostic ingredients §6).
9 (EDITORIAL) L2 numerics header: existing scripts cited with their limits (t_n never reached at simulable n).
10 (EDITORIAL) L1.4(3) labelled a sketch, not a proved implementation property; (PB) stays a hypothesis.
11 (EDITORIAL) NEG quantifier ∃ a ∈ ℤ_{≥0}.
