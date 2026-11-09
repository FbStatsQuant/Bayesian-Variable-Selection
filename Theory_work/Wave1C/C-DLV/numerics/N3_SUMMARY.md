# N3 two-model check (numbers only)

Constructions: 51 from 16 fits (designs M,F; (800,108),(1600,135); seeds 1-4).
Replay (psi_enum.build_grid, saved schedule as targets, saved T_e) vs code grid: length mismatches 0, mismatches (length or max abs diff > 1e-12) 0, max abs diff over same-length cases 9.843e-13; replay reason != 'ok': 0.
N_b (replay, steps with rho<0.90): max 10; equals (code intervals - N_p) in 51/51.
M1 == M2: 7/51.
r_max quantiles (0,10,25,50,75,90,100%): 0.1295, 0.1419, 0.2994, 0.5028, 0.8924, 0.9657, 0.9998
fraction r_max <= 0.01: 0.000 (0/51); <= 0.02: 0.000 (0/51).

range [0,2]: quantiles (0,50,90,100%) 0.1295, 0.5028, 0.9657, 0.9998; frac <=0.01: 0.000 (0/51); frac <=0.02: 0.000 (0/51)
range [0,1.5]: quantiles (0,50,90,100%) 0.09488, 0.242, 0.6951, 0.9816; frac <=0.01: 0.000 (0/51); frac <=0.02: 0.000 (0/51)
range [0,1.25]: quantiles (0,50,90,100%) 0.08207, 0.1777, 0.487, 0.8678; frac <=0.01: 0.000 (0/51); frac <=0.02: 0.000 (0/51)

Bound not evaluated (no construction with r_max <= 0.02).

Per (design, n): constructions, median r_max, max r_max, #r_max<=0.02, max N_b, M1==M2 count
```
M n=800: 12, 0.5687, 0.9139, 0, 9, 0
M n=1600: 15, 0.2994, 0.9573, 0, 10, 0
F n=800: 10, 0.7579, 0.9657, 0, 4, 7
F n=1600: 14, 0.6348, 0.9998, 0, 9, 0
```
