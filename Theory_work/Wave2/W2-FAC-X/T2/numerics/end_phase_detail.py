"""end_phase_detail.py -- the end phase of exact-Gram multi-class paths versus FACB L4.4 (E-side).
FACB (one class): when the kept nulls are imbalanced, the deleted null is on the majority side, so |I| never grows.
Multi-class analogue tested here: the deleted null j at T has sign(xi_j) = sign(X_T) ("majority side" w.r.t. the
centre shift).  For each run we count end-phase steps (m <= 40) with sign(xi_j) != sign(X_T) and |X_T| > 0.05 Hbar
("minority deletions"), and the steps at which the weighted imbalance |W|, W := X_T D'_T / Hbar
= (sum_{kept nulls} l'_i zeta_i - varrho)/Hbar, INCREASES (in FACB, |W| = |I| + o(1) never increases when |I| >= 1).
The first run (per design) containing a minority deletion is printed in detail (end-phase steps around it).
Usage: py -3.13 end_phase_detail.py > end_phase_detail_out.txt"""
import math
import numpy as np
import eg_core as eg
from run_t2 import build, DESIGNS


def main():
    detail_done = set()
    print("design          truth n      p    | end steps  minority-del  |W|-increases  max l_hi|X|/Hbar  final_S0")
    for design in ["cs05", "r2_06_08", "r2_03_09", "r2_02_095", "r2_02_095_lo", "r2_01_098", "r3_02_06_095"]:
        for truth in ["s1lo", "s3mix"]:
            for n, p in [(10 ** 6, 1500)]:
                tot_end = tot_min = tot_inc = 0; crmax = 0.0; allS0 = True
                for seed in range(4):
                    rng = np.random.default_rng(424242 + 17 * seed + p)
                    lam, th = build(design, p, truth, rng)
                    P = eg.EGData(lam, th, n, rng)
                    out = eg.eg_path(P, range(p))
                    allS0 &= out["final_is_S0"]
                    st, mv, H = out["steps"], out["moves"], out["Hbar"]
                    vals = np.unique(lam); lhi = (vals / np.sqrt(1 - vals ** 2)).max()
                    rows = []
                    for i, (s, m_) in enumerate(zip(st, mv)):
                        k, m, X, cr, viol, J, Dp = s
                        if m > 40 or m_[0] != "delN":
                            continue
                        j = m_[1]; sj = 1 if P.xi[j] > 0 else -1
                        minority = (abs(X) > 0.05 * H) and (sj != (1 if X > 0 else -1))
                        W = X * Dp / H
                        Wn = st[i + 1][2] * st[i + 1][6] / H if i + 1 < len(st) else 0.0
                        inc = (abs(W) >= 1.0) and abs(Wn) > abs(W) + 1e-12
                        tot_end += 1; tot_min += minority; tot_inc += inc
                        crmax = max(crmax, lhi * abs(X) / H)
                        rows.append((m, X / H, W, int(m_[4]), sj, minority, inc, Dp))
                    mins = [ii for ii, rr in enumerate(rows) if rr[5]]
                    if design not in detail_done and mins:
                        detail_done.add(design)
                        i0 = mins[0]
                        print("    detail (%s, %s, seed %d): m, X/Hbar, W, deleted class (0 = lowest loading), sign, flags, D'" % (design, truth, seed))
                        for r_ in rows[max(0, i0 - 4): i0 + 8]:
                            print("     m=%3d X/H=%+.3f W=%+.3f  del c%d%s %s %s D'=%.2f" % (
                                r_[0], r_[1], r_[2], r_[3], "+" if r_[4] > 0 else "-", "MINORITY" if r_[5] else "", "|W|up" if r_[6] else "", r_[7]))
                print("%-14s %-5s n=%-6g p=%-5d| %4d       %4d          %4d           %.2f              %s  (|W|>=1 steps counted for |W|-increases)" % (
                    design, truth, n, p, tot_end, tot_min, tot_inc, crmax, allS0))


if __name__ == "__main__":
    main()
