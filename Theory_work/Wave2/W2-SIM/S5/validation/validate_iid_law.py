"""Validation of the Bartlett sufficient-statistic simulation (iid_core.IidData with the S5 loading matrix, as used by
s5p_iid.py) against explicit iid Gaussian rows, at small n: two-sample KS tests on Gram/score statistics and on the
LS0 path outcome (iid_core.ls0_path, identical for both data sources).  usage: py -3.13 validate_iid_law.py [reps]"""
import os, sys, math, json, types
sys.path.insert(0, os.environ["IID_CORE_DIR"]); sys.path.insert(1, os.environ["BCS_CORE_DIR"]); sys.path.insert(2, "../scripts")
import numpy as np
from scipy.stats import ks_2samp
import iid_core as IC
import s5p_iid as S

p, n, q, rb, rw = 40, 80, 5, .3, .7
reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
Lam, grp = S.s5_loadings(p, q, rb, rw)
beta = S.BC.layout(p, q, s0=4)
S0 = tuple(int(j) for j in np.flatnonzero(beta))
Sig = Lam @ Lam.T + (1 - rw) * np.eye(p)
Lc = np.linalg.cholesky(Sig)
null = [j for j in range(p) if j not in S0][:2]


def explicit(rng):
    X = rng.standard_normal((n, p)) @ Lc.T
    y = X @ beta + rng.standard_normal(n)
    Xc = X - X.mean(0); yc = y - y.mean()
    sd = np.sqrt((Xc ** 2).sum(0) / (n - 1)); s = math.sqrt(yc @ yc / (n - 1))
    P = types.SimpleNamespace(n=n, p=p, K=min(p, n // 2), nu=0.01 + n / 2, logw=IC.log_prior_w(p, min(p, n // 2)),
                              XtX=(Xc.T @ Xc) / np.outer(sd, sd), Xty=(Xc.T @ yc) / sd / s, yty=n - 1.0)
    return P


def stats(P):
    r = IC.ls0_path(P, list(range(p)), S0)
    return [P.XtX[0, 1], P.XtX[0, 5], P.XtX[0, 39], P.Xty[S0[0]], P.Xty[S0[2]], P.Xty[null[0]], P.Xty[null[1]],
            float(r["final_is_S0"]), len(r["moves"]), len(r["final"])]


names = ["XtX[0,1] same grp", "XtX[0,5] diff grp", "XtX[0,39]", "Xty truth1", "Xty truth3", "Xty null a", "Xty null b",
         "path final=S0", "path #moves", "path final size"]
rng1 = np.random.default_rng(777); rng2 = np.random.default_rng(778)
A = np.array([stats(IC.IidData(Lam, beta, n, rng1, sigma=1.0)) for _ in range(reps)])
B = np.array([stats(explicit(rng2)) for _ in range(reps)])
print("p=%d n=%d q=%d rb=%g rw=%g reps=%d (Bartlett vs explicit rows)" % (p, n, q, rb, rw, reps))
for i, nm in enumerate(names):
    ks = ks_2samp(A[:, i], B[:, i])
    print("%-20s Bartlett mean %.4f sd %.4f | explicit mean %.4f sd %.4f | KS D=%.4f p=%.3f" % (
        nm, A[:, i].mean(), A[:, i].std(), B[:, i].mean(), B[:, i].std(), ks.statistic, ks.pvalue))
