"""O-BGIBBS bg3_popcheck: the deterministic (population) premises of Proposition LH-lock, by exhaustive enumeration.

Population fit of a column set T: f(T) = theta' R[:,T] R[T,T]^{-1} R[T,:] theta  (exact Gram: sample fit = (n-1) f(T)).
gamma_0 fit (block tables with the full response, blocks = groups): f0(T) = sum over groups C of f(T n C).
Checks over every T containing S° (U = {y : y contains S°}):
  C1  lock-del  (gamma_1): min f(T) - f(T - j),            j in S°
  C2  lock-swap (gamma_1): min f(T) - f(T - j + l),        j in S°, l not in T
  C1' lock-del  (gamma_0): min f0(T) - f0(T - j)
  C2' lock-swap (gamma_0): min f0(T) - f0(T - j + l)
  C3  downhill  (gamma_1): min f(T + b) - f(T),            b a masked hub not in T
  C4  extras    (gamma_1): max |f(T) - f(T - j)| over T containing S0 and j not in S0 (should be 0: zero-gain extras)
All of C1, C1', C2, C2', C3 > 0 and C4 = 0 => the score-level statements of LH-lock hold w.p. -> 1 for p fixed.
Usage: python bg3_popcheck.py c   (c = 2: p = 16, g = 4; c = 3: p = 18, g = 3)
"""
import sys
import numpy as np
from bg2_score_rate import lh_design


def main():
    c = int(sys.argv[1]); g = 4 if c == 2 else 3
    R, theta, ha, hb = lh_design(c, g)
    p = R.shape[0]
    groups = [list(range(h * g, (h + 1) * g)) for h in range(p // g)]
    gid = np.array([j // g for j in range(p)])
    Sdeg = sum(1 << j for j in ha)
    S0 = Sdeg | sum(1 << j for j in hb)
    Rt = R @ theta
    nst = 1 << p
    f = np.zeros(nst)
    for m in range(1, nst):
        idx = [j for j in range(p) if (m >> j) & 1]
        v = Rt[idx]
        f[m] = v @ np.linalg.solve(R[np.ix_(idx, idx)], v)
    gmask = [sum(1 << j for j in G) for G in groups]
    allm = np.arange(nst, dtype=np.int64)
    f0 = np.zeros(nst)
    for gm in gmask:
        f0 += f[allm & gm]
    U = allm[(allm & Sdeg) == Sdeg]
    out = {k: np.inf for k in ["C1", "C2", "C1'", "C2'", "C3"]}
    c4 = 0.0
    for T in U:
        for j in ha:
            Tm = T & ~(1 << j)
            out["C1"] = min(out["C1"], f[T] - f[Tm]); out["C1'"] = min(out["C1'"], f0[T] - f0[Tm])
            for l in range(p):
                if not (T >> l) & 1:
                    Ts = Tm | (1 << l)
                    out["C2"] = min(out["C2"], f[T] - f[Ts]); out["C2'"] = min(out["C2'"], f0[T] - f0[Ts])
        for b in hb:
            if not (T >> b) & 1:
                out["C3"] = min(out["C3"], f[T | (1 << b)] - f[T])
        if (T & S0) == S0:
            for j in range(p):
                if (T >> j) & 1 and not (S0 >> j) & 1:
                    c4 = max(c4, abs(f[T] - f[T & ~(1 << j)]))
    print("c=%d p=%d g=%d |U|=%d  ||mu||^2/(n-1)=%.4f" % (c, p, g, len(U), f[S0]))
    for k, v in out.items():
        print("  %-4s min = %.6f" % (k, v))
    print("  C4   max = %.2e" % c4)


if __name__ == "__main__":
    main()
