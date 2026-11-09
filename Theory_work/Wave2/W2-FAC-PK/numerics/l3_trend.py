"""Trend of min over 'tails2' sets (m nulls with largest |xi|, plus S0) of best deletion gain / log n, p = n - 1,
rho = 0.8, s0 = 1, as n grows; also M_T at those sets.  usage: python l3_trend.py"""
import math, json
import numpy as np
import pk_core as pk
from l3_static import gains
for n in [2000, 8000, 32000, 128000]:
    p = n - 1; th = np.zeros(p); th[2] = 1.0
    P = pk.make_cs(0.8, th, n, 3)
    K = P.K; nulls = np.flatnonzero(np.arange(p) != 2); xs = P.xi
    order = nulls[np.argsort(-np.abs(xs[nulls]))]
    res = []
    for frac in [0.01, 0.05, 0.1, 0.25, 0.5, 0.99]:
        m = max(1, int(frac * (K - 1)))
        gd, d, MT, dw = gains(P, set([2]) | set(int(v) for v in order[:m]))
        res.append(dict(m=m, ratio=round(gd / math.log(n), 3), d=round(d, 2), MT=round(MT, 2)))
    print(json.dumps(dict(n=n, rows=res)), flush=True)
