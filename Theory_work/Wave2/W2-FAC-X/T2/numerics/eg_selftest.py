"""eg_selftest.py -- checks of eg_core against direct linear algebra and against the general production-path code.
(1) F_closed(U) == F_direct(U) for random U (n up to 1e7).
(2) closed-form neighbour gains used by eg_path == F_direct differences at the start set and at a mid-path set.
(3) eg_path move sequence == iid_core.ls0_path (general exact linear algebra on X'X = (n-1)Sigma) move sequence.
Usage: py -3.13 eg_selftest.py > eg_selftest_out.txt"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "numerics"))
import numpy as np
import eg_core as eg
import iid_core as ic


class Adapter:
    def __init__(self, P):
        self.n, self.p, self.K, self.nu, self.logw = P.n, P.p, P.K, P.nu, P.logw
        Sig = np.outer(P.lam, P.lam) + np.diag(P.psi)
        self.XtX = (P.n - 1) * Sig
        self.Xty = P.z.copy(); self.yty = P.n - 1.0


def design(p, kind, rng):
    if kind == "two02_095":
        lam = np.where(np.arange(p) % 2 == 0, 0.2, 0.95)
    elif kind == "two03_09":
        lam = np.where(np.arange(p) % 2 == 0, 0.3, 0.9)
    elif kind == "three":
        lam = np.array([0.2, 0.6, 0.95])[np.arange(p) % 3]
    else:
        lam = np.full(p, math.sqrt(0.5))
    th = np.zeros(p); idx = rng.choice(p, 3, replace=False); th[idx] = [1.3, -0.9, 1.6]
    return lam, th


def main():
    rng = np.random.default_rng(12345)
    print("(1) F_closed vs F_direct")
    worst = 0.0
    for kind in ["two02_095", "two03_09", "three", "cs"]:
        for n in [10 ** 3, 10 ** 5, 10 ** 7]:
            lam, th = design(40, kind, rng)
            P = eg.EGData(lam, th, n, rng)
            for _ in range(20):
                U = rng.choice(40, rng.integers(0, 40), replace=False)
                a, b = P.F_closed(U), P.F_direct(U)
                worst = max(worst, abs(a - b) / max(1.0, abs(b)))
    print("  max relative |F_closed - F_direct| =", "%.2e" % worst)
    print("(2) closed-form gains vs F_direct differences (first two steps of the path)")
    worst = 0.0
    for kind in ["two02_095", "three"]:
        for n in [10 ** 4, 10 ** 6]:
            lam, th = design(30, kind, rng)
            P = eg.EGData(lam, th, n, rng)
            out = eg.eg_path(P, range(30), max_moves=1)
            T = [j for j in range(30)]
            F0 = P.F_direct(T)
            best_direct = -np.inf; arg = None
            for j in T:
                v = P.F_direct([t for t in T if t != j]) - F0
                if v > best_direct:
                    best_direct, arg = v, ("delN" if th[j] == 0 else "delT", j)
            mv = out["moves"][0]
            worst = max(worst, abs(mv[3] - best_direct))
            print("  %s n=%g: path move %s j=%d gain %.6f | direct best %s j=%d gain %.6f" % (kind, n, mv[0], mv[1], mv[3], arg[0], arg[1], best_direct))
    print("  max |gain diff| = %.2e" % worst)
    print("(3) full path equality: eg_path vs iid_core.ls0_path on explicit X'X")
    nsame = ntot = 0
    for kind in ["two02_095", "two03_09", "three", "cs"]:
        for n in [10 ** 4, 10 ** 6]:
            for p in [40, 120]:
                for seed in range(2):
                    r2 = np.random.default_rng(1000 * seed + p + n % 97)
                    lam, th = design(p, kind, r2)
                    P = eg.EGData(lam, th, n, r2)
                    o1 = eg.eg_path(P, range(p), record=False)
                    A = Adapter(P)
                    o2 = ic.ls0_path(A, range(p), sorted(np.flatnonzero(th)))
                    s1 = [(m[0], m[1], m[2]) for m in o1["moves"]]
                    s2 = [(m[0], m[1], m[2]) for m in o2["moves"]]
                    same = s1 == s2
                    gd = max([abs(a[3] - b[3]) for a, b in zip(o1["moves"], o2["moves"])] + [0.0])
                    ntot += 1; nsame += same
                    print("  %-10s n=%-8g p=%-4d seed=%d moves %d/%d same=%s max|gain diff|=%.1e final_S0 %s/%s" % (
                        kind, n, p, seed, len(s1), len(s2), same, gd, o1["final_is_S0"], o2["final_is_S0"]))
    print("  identical move sequences: %d/%d" % (nsame, ntot))


if __name__ == "__main__":
    main()
