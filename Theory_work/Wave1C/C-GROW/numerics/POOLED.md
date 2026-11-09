## Pooled counts (script build_pooled.py <- RAW_*_raw.csv)

| subset | runs | uncapped reaches S0 | only +T/-N tokens | +T before all -N | tau <= |symdiff| | max(tau-|symdiff|) | runs with a swap before tau | #swaps | #+N | #-T |
|---|---|---|---|---|---|---|---|---|---|---|
| all runs | 517 | 508 | 452 | 452 | 491 | 3 | 56 | 73 | 0 | 0 |
| S2 p=100 | 160 | 158 | 155 | 155 | 158 | 0 | 3 | 3 | 0 | 0 |
| S2 p=200 | 35 | 34 | 34 | 34 | 34 | 0 | 0 | 0 | 0 | 0 |
| S2 p=400 | 65 | 61 | 58 | 58 | 61 | 0 | 3 | 3 | 0 | 0 |
| S5 p=100 | 160 | 160 | 138 | 138 | 151 | 1 | 22 | 24 | 0 | 0 |
| S5 p=200 | 50 | 50 | 38 | 38 | 48 | 1 | 12 | 15 | 0 | 0 |
| S5 p=400 | 47 | 45 | 29 | 29 | 39 | 3 | 16 | 28 | 0 | 0 |

Token counts up to tau over all runs reaching S0: +T: 85, -N: 4775, swN>N: 24, swN>T: 49
Swap tokens: position (leading block of swaps vs after a non-swap move): swN>N first: 24, swN>T first: 46, swN>T later: 3

### D1 pooled

runs: 517; runs with F(S0) < max F over LS-scored models: 12; incl. MC3-proposed: 13; runs with a better one-flip/swap neighbour than S0: 12; MC3 best visited = S0: 504
beaten runs by (scen, p, n): S2 p=100 c=1 n=200 seed=19 (-1.19, best symdiff to S0 = 1), S2 p=100 c=0.5 n=200 seed=19 (-1.41, best symdiff to S0 = 1), S5 p=100 c=1 n=200 seed=12 (-0.09, best symdiff to S0 = 1), S5 p=100 c=0.5 n=200 seed=12 (-0.22, best symdiff to S0 = 1), S5 p=200 c=1 n=200 seed=3 (-0.95, best symdiff to S0 = 1), S2 p=200 c=1 n=200 seed=6 (-0.46, best symdiff to S0 = 1), S5 p=400 c=1 n=200 seed=5 (-0.76, best symdiff to S0 = 1), S5 p=400 c=0.5 n=200 seed=5 (-0.94, best symdiff to S0 = 1), S2 p=400 c=1 n=3200 seed=7 (-0.55, best symdiff to S0 = 1), S2 p=400 c=1 n=800 seed=8 (-0.69, best symdiff to S0 = 1), S2 p=400 c=0.5 n=3200 seed=7 (-0.57, best symdiff to S0 = 1), S2 p=400 c=0.5 n=800 seed=8 (-0.76, best symdiff to S0 = 1), S2 p=400 c=0.5 n=200 seed=3 (-0.07, best symdiff to S0 = 0)
max over runs of the symmetric difference between S0 and the best model found (LS union): 1; of those beating S0: [0, 1]
MC3 fraction of the second half at supersets of S0: min over all runs 0.458
