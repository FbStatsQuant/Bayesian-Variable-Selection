# F-MASKPIP simulation notes (helper, 2026-11-02)

Scripts: `scripts/masked_sim.py` (simulator; the round kernel is W2-T26 `smc_sim.Sim.round`, unchanged),
`scripts/run_all.sh` (runner, 3 processes, BLAS threads = 1), `scripts/summarize.py` (tables).
Raw per-island records: `results/masked_sim.jsonl` (one `setting` line per setting, then one `island` line per
island × rep; per-setting files in `results/raw/`). Seeds are fixed and listed in the masked_sim.py docstring.

## What ran
ALL 24 settings ran to completion; nothing was skipped:
designs {masked (premise_scan, corr(x3,x0) = 0.6), masked8 (own design: corr(x3,x0) = 0.8, beta_3 = -0.8, so the
population covariance of x3 with the mean is exactly 0; see docstring)} × n {640, 5120} × N {2500 (20 reps), 50
(40 reps)} × grids {G1, G2, G3}; 4 islands per rep; p = 18, data seed 0, exact scores.
G3 uses ONE pilot of N iid pi0 draws per setting (seed in the docstring) and bisects the restricted ESS (threshold
0.9) on the distinct states V of that pilot. In every G3 setting S0 was NOT in V; x3 appeared in some V state
(columns V_size, S0_in_V, V_has_x3 in Table A).

Definitions as in the brief: W_r = Zhat_r/Z; f_r = fraction != S0 after the stage-T round; Bbar_r = fraction of
(particle, measured round) pairs whose path, including its start, visits a state != S0; err = max_j |PIPhat_rj -
1{j in S0}|. "Split island" := W_r < 0.05 and err_r < 0.10 (my threshold choice). "mean outside at measured-round
starts" = mean over the 4 measured rounds of the fraction != S0 at the start of the round.

### Table A: setting constants

| design | n | N | grid | T | reps (islands) | delta1 | u_pi | rhobar | pi0(S0) | exact PIP err | G3 pilot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| masked | 640 | 2500 | G1 | 1 | 20 (80) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 |  |
| masked | 640 | 50 | G1 | 1 | 40 (160) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 |  |
| masked | 5120 | 2500 | G1 | 1 | 20 (80) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 |  |
| masked | 5120 | 50 | G1 | 1 | 40 (160) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 |  |
| masked | 640 | 2500 | G2 | 10 | 20 (80) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 |  |
| masked | 640 | 50 | G2 | 10 | 40 (160) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 |  |
| masked | 5120 | 2500 | G2 | 20 | 20 (80) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 |  |
| masked | 5120 | 50 | G2 | 20 | 40 (160) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 |  |
| masked | 640 | 2500 | G3 | 3 | 20 (80) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 | {'V_size': 62, 'S0_in_V': False, 'V_has_x3': True} |
| masked | 640 | 50 | G3 | 3 | 40 (160) | 0.1194 | 0.1355 | 0.1176 | 0.000148 | 0.03908 | {'V_size': 6, 'S0_in_V': False, 'V_has_x3': True} |
| masked | 5120 | 2500 | G3 | 10 | 20 (80) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 | {'V_size': 17, 'S0_in_V': False, 'V_has_x3': True} |
| masked | 5120 | 50 | G3 | 1 | 40 (160) | 0.03683 | 0.03824 | 0.03665 | 6.69e-36 | 0.006716 | {'V_size': 3, 'S0_in_V': False, 'V_has_x3': True} |
| masked8 | 640 | 2500 | G1 | 1 | 20 (80) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 |  |
| masked8 | 640 | 50 | G1 | 1 | 40 (160) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 |  |
| masked8 | 5120 | 2500 | G1 | 1 | 20 (80) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 |  |
| masked8 | 5120 | 50 | G1 | 1 | 40 (160) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 |  |
| masked8 | 640 | 2500 | G2 | 10 | 20 (80) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 |  |
| masked8 | 640 | 50 | G2 | 10 | 40 (160) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 |  |
| masked8 | 5120 | 2500 | G2 | 21 | 20 (80) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 |  |
| masked8 | 5120 | 50 | G2 | 21 | 40 (160) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 |  |
| masked8 | 640 | 2500 | G3 | 8 | 20 (80) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 | {'V_size': 47, 'S0_in_V': False, 'V_has_x3': True} |
| masked8 | 640 | 50 | G3 | 4 | 40 (160) | 0.09505 | 0.105 | 0.09385 | 0.000907 | 0.01374 | {'V_size': 7, 'S0_in_V': False, 'V_has_x3': True} |
| masked8 | 5120 | 2500 | G3 | 1 | 20 (80) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 | {'V_size': 29, 'S0_in_V': False, 'V_has_x3': True} |
| masked8 | 5120 | 50 | G3 | 1 | 40 (160) | 0.04872 | 0.05122 | 0.04839 | 1.06e-48 | 0.009449 | {'V_size': 3, 'S0_in_V': False, 'V_has_x3': True} |

### Table B: evidence ratio and occupancy

| design | n | N | grid | T | mean log W | q05 | q50 | q95 | mean W | frac f_r>1/2 | mean f_r | mean outside at measured-round starts | mean Bbar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masked | 640 | 2500 | G1 | 1 | -2.73 | -4.37 | -4.32 | 1.19 | 0.906 | 0 | 0.204 | 0.12 | 0.223 |
| masked | 640 | 50 | G1 | 1 | -4.18 | -4.61 | -4.35 | -4 | 1.76 | 0 | 0.237 | 0.119 | 0.223 |
| masked | 5120 | 2500 | G1 | 1 | -8.26 | -11.7 | -5.88 | -4.78 | 0.00227 | 0 | 0.217 | 0.0369 | 0.072 |
| masked | 5120 | 50 | G1 | 1 | -11.5 | -11.7 | -11.7 | -11.6 | 0.00175 | 0 | 0.257 | 0.0365 | 0.0719 |
| masked | 640 | 2500 | G2 | 10 | -0.00369 | -0.0354 | -0.00651 | 0.0395 | 0.997 | 0 | 0.119 | 0.119 | 0.223 |
| masked | 640 | 50 | G2 | 10 | 0.00959 | -0.262 | 0.00771 | 0.263 | 1.02 | 0 | 0.12 | 0.122 | 0.227 |
| masked | 5120 | 2500 | G2 | 20 | -0.00441 | -0.0524 | -0.00663 | 0.0389 | 0.996 | 0 | 0.0367 | 0.037 | 0.0725 |
| masked | 5120 | 50 | G2 | 20 | -0.025 | -0.415 | -0.00733 | 0.341 | 1 | 0 | 0.0359 | 0.0364 | 0.0719 |
| masked | 640 | 2500 | G3 | 3 | -0.0108 | -0.166 | -0.0132 | 0.165 | 0.994 | 0 | 0.119 | 0.12 | 0.223 |
| masked | 640 | 50 | G3 | 3 | -0.317 | -1.32 | -0.00622 | 0.82 | 0.992 | 0 | 0.119 | 0.119 | 0.222 |
| masked | 5120 | 2500 | G3 | 10 | -4.74 | -5.29 | -5.13 | -4.56 | 0.898 | 0 | 0.142 | 0.0369 | 0.0725 |
| masked | 5120 | 50 | G3 | 1 | -11.4 | -11.7 | -11.7 | -11.6 | 0.00437 | 0 | 0.267 | 0.0341 | 0.0687 |
| masked8 | 640 | 2500 | G1 | 1 | -0.682 | -4.55 | -0.212 | 0.697 | 0.922 | 0 | 0.119 | 0.0953 | 0.18 |
| masked8 | 640 | 50 | G1 | 1 | -4.2 | -4.94 | -4.56 | -3.67 | 1.01 | 0 | 0.216 | 0.095 | 0.18 |
| masked8 | 5120 | 2500 | G1 | 1 | -10.7 | -10.8 | -10.8 | -10.8 | 0.00351 | 0 | 0.256 | 0.0485 | 0.0943 |
| masked8 | 5120 | 50 | G1 | 1 | -10.8 | -10.8 | -10.8 | -10.7 | 2.08e-05 | 0 | 0.247 | 0.049 | 0.0959 |
| masked8 | 640 | 2500 | G2 | 10 | -0.000183 | -0.0252 | -0.000882 | 0.0376 | 1 | 0 | 0.0949 | 0.0951 | 0.18 |
| masked8 | 640 | 50 | G2 | 10 | 0.0137 | -0.252 | 0.029 | 0.24 | 1.02 | 0 | 0.0939 | 0.0959 | 0.182 |
| masked8 | 5120 | 2500 | G2 | 21 | 0.00243 | -0.0316 | -0.00147 | 0.048 | 1 | 0 | 0.0485 | 0.0486 | 0.0946 |
| masked8 | 5120 | 50 | G2 | 21 | 0.0059 | -0.357 | -0.000922 | 0.367 | 1.04 | 0 | 0.0489 | 0.0473 | 0.0919 |
| masked8 | 640 | 2500 | G3 | 8 | -0.00138 | -0.059 | -0.00439 | 0.0709 | 0.999 | 0 | 0.0955 | 0.0953 | 0.181 |
| masked8 | 640 | 50 | G3 | 4 | -0.123 | -0.761 | -0.146 | 0.564 | 0.967 | 0 | 0.097 | 0.0927 | 0.177 |
| masked8 | 5120 | 2500 | G3 | 1 | -10.8 | -10.8 | -10.8 | -10.8 | 2.08e-05 | 0 | 0.256 | 0.0487 | 0.0948 |
| masked8 | 5120 | 50 | G3 | 1 | -10.8 | -10.8 | -10.8 | -10.7 | 2.09e-05 | 0 | 0.262 | 0.0462 | 0.0912 |

### Table C: PIP accuracy and the three inequalities

| design | n | N | grid | mean island PIP err | mean primary PIP err | MPM correct | (I1) E[W 1{f>1/2}] | 2 delta1 | (I3) E[W err] | delta1+rhobar+u_pi | (I2) max[err-(Bbar+u_pi)] | split islands (W<0.05, err<0.10) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masked | 640 | 2500 | G1 | 0.03908 | 0.03908 | 1 | 0 | 0.2387 | 0.0354 | 0.3724 | -3.078e-01 | 56/80 |
| masked | 640 | 50 | G1 | 0.03907 | 0.03907 | 1 | 0 | 0.2387 | 0.06853 | 0.3724 | -2.366e-01 | 157/160 |
| masked | 5120 | 2500 | G1 | 0.006715 | 0.006715 | 1 | 0 | 0.07366 | 1.522e-05 | 0.1117 | -9.712e-02 | 80/80 |
| masked | 5120 | 50 | G1 | 0.006717 | 0.006717 | 1 | 0 | 0.07366 | 1.178e-05 | 0.1117 | -6.154e-02 | 158/160 |
| masked | 640 | 2500 | G2 | 0.03908 | 0.03908 | 1 | 0 | 0.2387 | 0.03894 | 0.3724 | -3.045e-01 | 0/80 |
| masked | 640 | 50 | G2 | 0.03909 | 0.03909 | 1 | 0 | 0.2387 | 0.04 | 0.3724 | -2.318e-01 | 0/160 |
| masked | 5120 | 2500 | G2 | 0.006716 | 0.006716 | 1 | 0 | 0.07366 | 0.006689 | 0.1117 | -9.703e-02 | 0/80 |
| masked | 5120 | 50 | G2 | 0.006717 | 0.006717 | 1 | 0 | 0.07366 | 0.00672 | 0.1117 | -4.657e-02 | 0/160 |
| masked | 640 | 2500 | G3 | 0.03908 | 0.03908 | 1 | 0 | 0.2387 | 0.03885 | 0.3724 | -3.052e-01 | 0/80 |
| masked | 640 | 50 | G3 | 0.03904 | 0.03904 | 1 | 0 | 0.2387 | 0.03871 | 0.3724 | -2.319e-01 | 0/160 |
| masked | 5120 | 2500 | G3 | 0.006717 | 0.006717 | 1 | 0 | 0.07366 | 0.006028 | 0.1117 | -9.753e-02 | 76/80 |
| masked | 5120 | 50 | G3 | 0.006713 | 0.006713 | 1 | 0 | 0.07366 | 2.932e-05 | 0.1117 | -4.658e-02 | 155/160 |
| masked8 | 640 | 2500 | G1 | 0.01374 | 0.01374 | 1 | 0 | 0.1901 | 0.01267 | 0.2939 | -2.591e-01 | 11/80 |
| masked8 | 640 | 50 | G1 | 0.01374 | 0.01374 | 1 | 0 | 0.1901 | 0.01389 | 0.2939 | -1.766e-01 | 152/160 |
| masked8 | 5120 | 2500 | G1 | 0.009447 | 0.009447 | 1 | 0 | 0.09744 | 3.321e-05 | 0.1483 | -1.277e-01 | 79/80 |
| masked8 | 5120 | 50 | G1 | 0.009458 | 0.009458 | 1 | 0 | 0.09744 | 1.972e-07 | 0.1483 | -7.684e-02 | 160/160 |
| masked8 | 640 | 2500 | G2 | 0.01374 | 0.01374 | 1 | 0 | 0.1901 | 0.01374 | 0.2939 | -2.581e-01 | 0/80 |
| masked8 | 640 | 50 | G2 | 0.01373 | 0.01373 | 1 | 0 | 0.1901 | 0.01407 | 0.2939 | -1.913e-01 | 0/160 |
| masked8 | 5120 | 2500 | G2 | 0.009449 | 0.009449 | 1 | 0 | 0.09744 | 0.009475 | 0.1483 | -1.236e-01 | 0/80 |
| masked8 | 5120 | 50 | G2 | 0.009442 | 0.009442 | 1 | 0 | 0.09744 | 0.009833 | 0.1483 | -6.187e-02 | 0/160 |
| masked8 | 640 | 2500 | G3 | 0.01375 | 0.01375 | 1 | 0 | 0.1901 | 0.01374 | 0.2939 | -2.584e-01 | 0/80 |
| masked8 | 640 | 50 | G3 | 0.01375 | 0.01375 | 1 | 0 | 0.1901 | 0.01329 | 0.2939 | -1.716e-01 | 0/160 |
| masked8 | 5120 | 2500 | G3 | 0.009448 | 0.009448 | 1 | 0 | 0.09744 | 1.968e-07 | 0.1483 | -1.292e-01 | 80/80 |
| masked8 | 5120 | 50 | G3 | 0.009444 | 0.009444 | 1 | 0 | 0.09744 | 1.97e-07 | 0.1483 | -6.687e-02 | 160/160 |

### Grids

- masked n=640 G1 (N=2500): T=1, phi = 0, 1
- masked n=5120 G1 (N=2500): T=1, phi = 0, 1
- masked n=640 G2 (N=2500): T=10, phi = 0, 0.2242, 0.3656, 0.4585, 0.5271, 0.5834, 0.6345, 0.6857, 0.7434, 0.8219, 1
- masked n=5120 G2 (N=2500): T=20, phi = 0, 0.2202, 0.3437, 0.4246, 0.4856, 0.5371, 0.5853, 0.6351, 0.693, 0.7631, 0.8203, 0.8557, 0.8777, 0.8926, 0.9039, 0.9134, 0.9222, 0.9311, 0.9414, 0.9559, 1
- masked n=640 G3 (N=2500): T=3, phi = 0, 0.3377, 0.6937, 1
- masked n=640 G3 (N=50): T=3, phi = 0, 0.3501, 0.7189, 1
- masked n=5120 G3 (N=2500): T=10, phi = 0, 0.2215, 0.3456, 0.4267, 0.4879, 0.5395, 0.5877, 0.6377, 0.697, 0.7879, 1
- masked n=5120 G3 (N=50): T=1, phi = 0, 1
- masked8 n=640 G1 (N=2500): T=1, phi = 0, 1
- masked8 n=5120 G1 (N=2500): T=1, phi = 0, 1
- masked8 n=640 G2 (N=2500): T=10, phi = 0, 0.1888, 0.3126, 0.4002, 0.4692, 0.529, 0.586, 0.6463, 0.7197, 0.8382, 1
- masked8 n=5120 G2 (N=2500): T=21, phi = 0, 0.3032, 0.4606, 0.5511, 0.6117, 0.6583, 0.6982, 0.7358, 0.7746, 0.8162, 0.855, 0.8831, 0.9017, 0.9144, 0.9239, 0.9316, 0.9385, 0.9454, 0.9529, 0.9624, 0.98, 1
- masked8 n=640 G3 (N=2500): T=8, phi = 0, 0.292, 0.5167, 0.6702, 0.7781, 0.8608, 0.9303, 0.9943, 1
- masked8 n=640 G3 (N=50): T=4, phi = 0, 0.3065, 0.5889, 0.8525, 1
- masked8 n=5120 G3 (N=2500): T=1, phi = 0, 1

## Plain findings
1. **No violation of (I1), (I2) or (I3) in any of the 24 settings (3,840 island-runs).** (I2): the largest value of
   err_r - (Bbar_r + u_pi) over all island-reps is -0.0466 (masked, n=5120, N=50, G2), far below 1e-12. (I3): the
   empirical E[W err] is below delta1 + rhobar + u_pi everywhere; the closest is masked n=640 N=50 G1 (0.0685 vs 0.372).
2. **(I1) is NOT stressed by these settings:** no island ever had f_r > 1/2 (max f_r over all island-runs = 0.44), so
   the left side is identically 0. One terminal round at phi = 1 already sends 56-80% of the particles to S0, even
   from pi0 draws with pi0(S0) ~ 1e-36 / 1e-48. A test of (I1) needs a design where the stage-T round does not cross.
3. **The split exists and is large.** With the one-shot grid G1, log W_r has median -4.3 (n=640) and -5.9 to -11.7
   (n=5120); at n=5120 essentially every island has W_r < 0.05, while the island PIP error equals the exact posterior
   PIP error (0.0067 / 0.0094) to 4 digits and MPM is correct in 100% of reps.
4. **The blind (candidate-set) grid G3 also collapses the evidence at n=5120:** masked, N=2500: T=10 (vs 20 for G2),
   median log W = -5.13, 95% of islands W < 0.05, PIPs exact to 4 digits (76/80 split islands). masked8, N=2500: the
   pilot V (29 states, S0 not in V) makes the restricted ESS accept phi = 1 at once (T=1), so G3 = G1 and log W =
   -10.8 for every island. At n=640, G3 behaves like G2 (log W ~ 0).
5. **The full-space ESS grid G2 never collapses** (|median log W| < 0.03 at N=2500), as expected.
6. E[W] = 1 holds only through rare huge islands: in collapsed settings the top 5% of islands carry up to 99-100%
   of the summed W, and in several settings (e.g. masked8 n=5120 G1/G3, N=50) none of the 160 islands showed it:
   mean W = 2e-5. This is consistent with unbiasedness (the mass sits on events of probability ~ pi0-scale) and is
   not a violation of anything.
7. f_r and the measured-round outside fractions sit near delta1 once the population is mixed (G2: f_r ≈ 0.12 ≈
   delta1 at n=640); Bbar_r ≈ 1.9 × (outside fraction), and that slack is why (I2) holds with a wide margin.
