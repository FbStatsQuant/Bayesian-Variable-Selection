## N3b: hard corners for L4 (script n3b_corners.py, raw N3b_raw.jsonl): exact CS, production lexicographic tie rule,
p = n/2 - 1 (log p/log n up to 0.94), rho in {0.9, 0.95, 0.99}, s0 in {1, 2}, mixed signs, path from [p].

| rho | s0 | n | p | seed | pure deletion | final = S0 | interval hole | max add gain/log n | max (best swap - best del) | max swap gain vs F(T) | ties |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.9 | 2 | 20001 | 10000 | 0 | True | True | True | -0.500 | -4.95 | -1.21e-09 | 0 |
| 0.9 | 2 | 20001 | 10000 | 1 | True | True | True | -0.500 | -4.95 | -1.06e-10 | 0 |
| 0.9 | 2 | 100001 | 50000 | 0 | True | True | True | -0.500 | -5.76 | -3.99e-11 | 0 |
| 0.9 | 2 | 100001 | 50000 | 1 | True | True | True | -0.452 | -5.31 | -8.24e-12 | 0 |
| 0.95 | 1 | 20001 | 10000 | 0 | True | True | True | -0.402 | -4.19 | -1.19e-09 | 0 |
| 0.95 | 1 | 20001 | 10000 | 1 | True | True | True | -0.346 | -4.01 | -4.91e-10 | 0 |
| 0.95 | 1 | 100001 | 50000 | 0 | True | True | True | -0.450 | -5.38 | -2.64e-11 | 0 |
| 0.95 | 1 | 100001 | 50000 | 1 | True | True | True | -0.376 | -4.44 | -5.06e-11 | 0 |
| 0.99 | 1 | 20001 | 10000 | 0 | True | True | True | -0.383 | -4.00 | -1.15e-09 | 0 |
| 0.99 | 1 | 20001 | 10000 | 1 | True | True | True | -0.326 | -3.81 | -5.02e-10 | 0 |
| 0.99 | 1 | 100001 | 50000 | 0 | True | True | True | -0.452 | -5.40 | -1.17e-10 | 0 |
| 0.99 | 1 | 100001 | 50000 | 1 | True | True | True | -0.353 | -4.18 | -1.24e-10 | 0 |

12 data sets; all pure deletion & final S0 & interval hole: True.
