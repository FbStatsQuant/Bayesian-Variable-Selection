"""Falsification numerics for L3(c): small m (1 <= m <= log^2 n), adversarial sets maximising the nearest distance d_T:
balanced extremes (m/2 largest and m/2 smallest xi), one-sided extremes, extremes + central.  Tight constants:
s0 = 1, rho in {0.95, 0.8, 0.5}.  Claim: best deletion gain >= (c_D - eps) log n - O(loglog n), c_D = 1/2 - 1/(s0+1+kappa).
Also checks that S0 itself is a strict local maximum (best addition gain < 0).  usage: python l3_small.py OUT.jsonl"""
import sys, json, math
import numpy as np
import pk_core as pk
from l3_static import gains
out = open(sys.argv[1], "w")
for rho in [0.95, 0.8, 0.5]:
    for n in [2000, 20000, 200000]:
        p = int(0.9 * n); th = np.zeros(p); th[2] = 1.0
        P = pk.make_cs(rho, th, n, 1)
        nulls = np.flatnonzero(np.arange(p) != 2); xs = P.xi; ln = math.log(n)
        kap = (1 - rho) / rho; cD = 0.5 - 1 / (2 + kap)
        hi = nulls[np.argsort(-xs[nulls])]; lo = nulls[np.argsort(xs[nulls])]; ab = nulls[np.argsort(-np.abs(xs[nulls]))]
        worst = (9, None)
        for m in [1, 2, 3, 4, 6, 10, 20, int(ln ** 2)]:
            kinds = {"balanced": np.concatenate([hi[:(m + 1) // 2], lo[:m // 2]]), "top": hi[:m], "bottom": lo[:m], "absmax": ab[:m]}
            for nm, R in kinds.items():
                gd, d, MT, dw = gains(P, set([2]) | set(int(v) for v in R))
                r = gd / ln
                if r < worst[0]: worst = (r, (m, nm, round(d, 2)))
                out.write(json.dumps(dict(rho=rho, n=n, m=m, kind=nm, ratio=r, d=d, MT=MT, cD=cD)) + "\n")
        # S0 local max: best addition
        z = P.z; k = 1; A = z[2] ** 2; B = z[2]; al, be, nu = P.al, P.be, P.nu
        g = lambda u: be / (al + u * be); quad = (A - g(1) * B * B) / al; psi = 0.02 + n - 1 - n * quad
        tout = z[nulls] - g(1) * B
        LD = float(pk._ldet(P, 1)); aw = P.lw[2] - P.lw[1] - 0.5 * (float(pk._ldet(P, 2)) - LD)
        Ga = aw - nu * np.log1p(-n * (1 - g(2)) * tout ** 2 / (al * psi))
        print(json.dumps(dict(rho=rho, n=n, cD=round(cD, 4), worst_ratio=round(worst[0], 4), worst_at=worst[1],
                              S0_best_add_over_logn=round(float(Ga.max()) / ln, 3))), flush=True)
