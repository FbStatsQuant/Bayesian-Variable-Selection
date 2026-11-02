"""EXP3-R (referee): independent re-check of W1 Exp 3 (combination look-alike) and of the two claims built on it:
  (C3)  SE + BM-inf do not imply PGD; TD'_P(R_{2,1}) fails w.p. -> 1;
  (A5)  'TD'_inf(R_{2,1}) holds without TD'_P' (converse of TD'_P => TD'_inf fails), which W1 supports only by
        the path from {} -- here we test TD'_inf on ALL of R_{2,1}.
Design (own construction): orthonormal centred columns e_1.. scaled to sqrt(n-1); x1 = e1, x2 = e2,
x3 = a (x1 + x2)/sqrt 2 + sqrt(1 - a^2) e3, q pure nulls; mu = theta (x1 + x2); eps ~ N(0, I) fresh per draw,
y standardised. a = 0.85, theta = 0.3, q = 5 (as W1). Seeds: design rng(9000 + n), noise rng(19000 + n).
Population PGD at S = {}: R+ = theta^2 (best truth), R0 = 2 a^2 theta^2 (x3) -> R0 > R+ for a^2 > 1/2.
"""
import numpy as np
from vt_core import Model, standardise, region, phi
from conditions import TDP, TDinf


def design(n, a=0.85, q=5, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((n, 3 + q)); Z -= Z.mean(0)
    E, _ = np.linalg.qr(Z); E *= np.sqrt(n - 1)
    x3 = a * (E[:, 0] + E[:, 1]) / np.sqrt(2) + np.sqrt(1 - a * a) * E[:, 2]
    return np.column_stack([E[:, 0], E[:, 1], x3, E[:, 3:]])


def main(draws=200):
    a, th = 0.85, 0.3
    Xd = design(50, a)
    print("pop. lambda_min(R_123) =", round(float(np.linalg.eigvalsh(np.corrcoef(Xd[:, :3].T)).min()), 4), "(1 - a = %.2f)" % (1 - a))
    print("pop. PGD at {}: R+ = theta^2 = %.4f, R0 = 2 a^2 theta^2 = %.4f" % (th ** 2, 2 * a * a * th ** 2))
    S0 = (0, 1)
    for n in (200, 1000, 3000):
        X = design(n, a, seed=9000 + n); mu = th * (X[:, 0] + X[:, 1])
        rng = np.random.default_rng(19000 + n)
        cnt = dict(first_add3=0, reach_from_empty=0, TDP=0, TDinf=0, TDinf_fail_states={})
        for _ in range(draws):
            Xs, y = standardise(X, mu + rng.standard_normal(n))
            M = Model(Xs, y)
            R = region(S0, list(range(2, M.p)), 2, 1)
            p0 = M.greedy_uncapped(())
            cnt['first_add3'] += len(p0) > 1 and p0[1] == (2,)
            cnt['reach_from_empty'] += p0[-1] == S0
            cnt['TDP'] += not TDP(M, S0, R)
            f = TDinf(M, S0, R)
            cnt['TDinf'] += not f
            for S, _k in f:
                key = str(S) if len(f) < 4 else 'other'
                cnt['TDinf_fail_states'][key] = cnt['TDinf_fail_states'].get(key, 0) + 1
        fs = sorted(cnt['TDinf_fail_states'].items(), key=lambda kv: -kv[1])[:6]
        cnt['TDinf_fail_states'] = fs
        print("n=%d draws=%d" % (n, draws), cnt, flush=True)


if __name__ == "__main__":
    main()
