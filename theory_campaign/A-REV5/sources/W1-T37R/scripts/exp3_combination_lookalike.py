"""Exp 3 — COUNTEREXAMPLE to the progress condition TD'_P under SE + BM (combination look-alike).

Design (population exact, built by Gram-Schmidt so the sample Gram equals the target Gram exactly):
  truths x1, x2 orthonormal-ish (corr 0), equal theta; null x3 = a (x1 + x2)/sqrt(2) + sqrt(1 - a^2) z;
  further q independent pure nulls. lambda_min(R_{1,2,3}) = 1 - a  (SE holds with phi0^2 = 1 - a).
  For a^2 > 1/2 the null x3 captures 2 a^2 theta^2 (n-1) > theta^2 (n-1) of mu = theta (x1 + x2):
  the greedy first move from S = {} is 'add null x3' (regressive), for every n, w.p. -> 1.
  We report, over 200 noise draws per n, the frequency of each first move, whether the uncapped greedy still
  reaches S0 (TD'_inf-type repair) and the number of moves (Phi({}) = 2).
Seeds: rng(2026 + n). Output: table to stdout.
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from td_core import Scorer, move_label


def design(n, a, q, rng):
    Z = rng.standard_normal((n, 3 + q))
    Z -= Z.mean(0)
    Qm, _ = np.linalg.qr(Z)          # orthonormal, centred columns
    e = Qm * np.sqrt(n - 1)
    x1, x2, z = e[:, 0], e[:, 1], e[:, 2]
    x3 = a * (x1 + x2) / np.sqrt(2) + np.sqrt(1 - a * a) * z
    return np.column_stack([x1, x2, x3, e[:, 3:]])


def main():
    a, q, theta = 0.85, 5, 0.3
    print(f"a={a} (a^2={a*a:.3f} > 1/2), phi0^2 = 1-a = {1-a:.2f}, theta={theta}, q={q} pure nulls")
    for n in (100, 200, 400, 1000, 3000):
        rng = np.random.default_rng(2026 + n)
        X = design(n, a, q, rng)
        mu = theta * (X[:, 0] + X[:, 1])
        first = {}; reach = 0; moves = []
        for r in range(200):
            eps = rng.standard_normal(n); eps -= eps.mean()
            yr = mu + eps
            y = yr / yr.std(ddof=1)
            sc = Scorer(X, y)
            out = sc.local_search((), ell=50)
            lab0 = move_label(out["kinds"][0], {0, 1}) if out["kinds"] else "none"
            first[lab0] = first.get(lab0, 0) + 1
            if out["final"] == (0, 1):
                reach += 1; moves.append(out["n_moves"])
        print(f"n={n:5d} first-move freq={first} uncapped reach S0: {reach}/200, "
              f"moves (median, max) = {np.median(moves) if moves else None}, {max(moves) if moves else None}")


if __name__ == "__main__":
    main()
