## Item 5 — B2-core: smallest value over q-sparse u and a of [n⁻¹Σ(a+u'z_i)²]/[a²+Var(u'z)]

p = 200. For a fixed support the minimum over (a, u_S) is exact (smallest generalised eigenvalue). q = 2: all 19 900 supports enumerated (exact minimum). q = 4: 40 restarts of best-swap hill climbing over supports (an UPPER bound on the true minimum, so `freq < ½` is a LOWER bound). R = 200 samples per cell.

| q | n | law | min over samples | q0.01 | q0.1 | median of the sample minima | freq(min < ½) | freq(min < 0.6) | search |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 200 | AR0.9 | 0.536 | 0.553 | 0.595 | 0.636 | 0.000 (0/200) | 0.135 | exact |
| 2 | 200 | Rademacher | 0.590 | 0.610 | 0.637 | 0.666 | 0.000 (0/200) | 0.005 | exact |
| 2 | 2000 | AR0.9 | 0.836 | 0.845 | 0.859 | 0.875 | 0.000 (0/200) | 0.000 | exact |
| 2 | 2000 | Rademacher | 0.867 | 0.869 | 0.880 | 0.890 | 0.000 (0/200) | 0.000 | exact |
| 4 | 200 | AR0.9 | 0.408 | 0.441 | 0.475 | 0.510 | 0.350 (70/200) | 1.000 | hill-climb |
| 4 | 200 | Rademacher | 0.456 | 0.474 | 0.500 | 0.522 | 0.100 (20/200) | 1.000 | hill-climb |
| 4 | 2000 | AR0.9 | 0.787 | 0.797 | 0.809 | 0.824 | 0.000 (0/200) | 0.000 | hill-climb |
| 4 | 2000 | Rademacher | 0.816 | 0.818 | 0.824 | 0.834 | 0.000 (0/200) | 0.000 | hill-climb |

q = 2: samples with at least one support below ½: 0; for those, the number of supports below ½ (of 19 900): none.