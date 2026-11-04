# Scripts (W1-T37R) — what each showed

All seeds fixed inside the scripts; Python 3.11 + numpy. Data regenerated with numpy (not the R benchmark streams).

| script | run | showed |
|---|---|---|
| td_core.py | library | exact F (00_COMMON §1), production best-move local search; checked vs dense marginal likelihood (1e-14) |
| exp1_small_exact.py | `python3 exp1_small_exact.py 20 50 {0,1}`; `25 20 1` | exact R_2 enumeration, n=200, p=20 (s0=4) / p=25 (s0=5): literal TD(1) 0/1800 (Prop 1); TD'_inf ≈ 0.92-0.98, TD'_P ≈ 0.71-0.84 on R_{s0,2}/R_{2,2} given PD & S0 local max; TD'_P(R_{1,1}) = 1.00; path-wise repair ≈ "S0 local max" |
| exp2_prod_scale.py | `python3 exp2_prod_scale.py 6` | n=200, p=500, s0=14: S0 local max 58/72; given that, 1160/1160 sampled R_{2,2} centres repaired certified in ≤ 3 moves; failures = posterior misses (0.2-4.8 nats) |
| exp3_combination_lookalike.py | `python3 exp3_combination_lookalike.py` | COUNTEREXAMPLE: SE (φ0²=0.15) + strong signal, first greedy move = add null in 200/200 at n=3000; TD'_P fails, TD'_∞ holds (3 moves vs Φ=2) |
| summarise.py | `python3 summarise.py results/*.json` | markdown tables in results/*_summary.md |
