"""CEX-1 (referee): literal TD(0, 0) STRICT holds, yet the greedy search from the centre {} (which is in R_0)
stops at {} -- so W1 Theorem A(A5) 'literal TD(d,0) strict => TD'_P(R_d)' is false, and so is the ORIGINAL T37(i)
at d = 0. Mechanism: literal TD(1) only asks that the best missing-truth addition beat every OTHER move; it never
asks that it be an IMPROVEMENT. A suppressor pair (two correlated truths with opposite signs) makes every
single-truth addition from {} non-improving while S0 is the global HPM.

Deterministic construction (no randomness in the conclusion; the seed only builds an orthonormal basis):
  n = 100, columns e_1..e_{q+3} orthonormal, centred, scaled to norm sqrt(n-1).
  x1 = e1, x2 = r e1 + sqrt(1-r^2) e2 (r = 0.95), nulls x_{3..} = e_3.. (q = 10), mu = th1 x1 - th2 x2,
  eps = sigma * sqrt(n-1) * e_last (orthogonal to every column), y = mu + eps, then standardised (scale only).
Prints: literal TD(0,0) strict failures (expect none), M({}) (expect None), the production local search from {},
the global HPM by full enumeration of 2^12 models (expect S0), and the gains at {}.
"""
import itertools, numpy as np
from vt_core import Model, region, standardise
from conditions import literal_TD, TDP, TDinf


def build(n=100, q=10, r=0.95, th1=3.0, th2=2.8, sigma=1.0, seed=11):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((n, q + 3)); Z -= Z.mean(0)
    E, _ = np.linalg.qr(Z); E *= np.sqrt(n - 1)
    x1 = E[:, 0]; x2 = r * E[:, 0] + np.sqrt(1 - r * r) * E[:, 1]
    X = np.column_stack([x1, x2] + [E[:, 2 + i] for i in range(q)])
    y = th1 * x1 - th2 * x2 + sigma * E[:, q + 2]
    return standardise(X, y)


def main():
    X, y = build()
    M = Model(X, y)
    S0 = (0, 1); nulls = list(range(2, M.p))
    R0 = region(S0, nulls, 2, 0)
    print("R_0 =", R0)
    print("literal TD(0,0) strict failures:", literal_TD(M, S0, R0, 0.0, True))
    print("TD'_P(R_0) failures:", TDP(M, S0, R0), " TD'_inf(R_0) failures:", TDinf(M, S0, R0))
    nb, f = M.scan(())
    g = f - M.F(())
    print("gains at {}: add x1 %.3f, add x2 %.3f, best null add %.3f" % (g[0], g[1], g[2:].max()))
    print("F(S0) - F({}) = %.3f" % (M.F(S0) - M.F(())))
    print("M({}) =", M.M(()))
    print("production local search from {}:", M.local_search(()))
    allS = [S for k in range(M.p + 1) for S in itertools.combinations(range(M.p), k)]
    F = M.Fset(allS)
    print("global HPM by enumeration:", allS[int(np.argmax(F))], " pi(S0) = %.4f" % np.exp(M.F(S0) - (F.max() + np.log(np.exp(F - F.max()).sum()))))
    lam = np.linalg.eigvalsh(np.corrcoef(X[:, :2].T)).min()
    print("lambda_min(R_S0) = %.3f" % lam)


if __name__ == "__main__":
    main()
