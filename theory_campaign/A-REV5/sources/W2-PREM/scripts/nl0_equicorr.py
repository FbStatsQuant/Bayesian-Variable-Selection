"""NL0(1) and UDEL(2) under G, R, SE, BM-inf: partner-graph condition vs equicorrelated nulls (W2-PREM §3).

Quantities (exact v3 scores, exact Gram):
  Lam0    = sum_{l null} o_l(S0)                               (leakage at S0 itself; [B]: automatic)
  Lam1    = NL0(1) = sum_{l null} max_{m null != l} o_l(S0+m)  (sum of sups, as in eta_2)
  edel2   = UDEL(2) = max_{l,m} o_l(S0+m+l)                    (same odds as Lam1, max instead of sum-of-max)
Designs: s0 = 2 truths (theta = 1, 1) independent of the nulls; p-2 nulls either
  EQ : equicorrelated, r = 0.8 (every pair is a partner: PG fails; SE holds with phi0^2 = 0.2)
  BLK: independent groups of 5, within-group r = 0.8 (partner degree D = 4: PG holds)
Sequence p = n^0.9 (so p <= n-2, A = 1).  Prediction (PROOF.md §3): EQ Lam1 ~ p^r n^{-1/2} (grows like n^{0.22}),
BLK Lam1 = O(sqrt(log n / n)).  6 replicates per n (3 at p = 1000), fixed seeds.  Output: results/nl0_equicorr.txt
"""
import numpy as np
from bvs_score import Data

R = 0.8
REPS = 6


def design(p, kind):
    q = p - 2
    S = np.eye(p)
    if kind == "EQ":
        S[2:, 2:] = R
    else:
        for g0 in range(2, p, 5):
            g1 = min(p, g0 + 5)
            S[g0:g1, g0:g1] = R
    np.fill_diagonal(S, 1.0)
    th = np.zeros(p)
    th[:2] = 1.0
    return S, th


def stats(D):
    p = D.p
    S0 = (0, 1)
    nulls = range(2, p)
    F0 = D.F(S0)
    Fm = {m: D.F((0, 1, m)) for m in nulls}
    lam0 = sum(1 / (1 + np.exp(-(Fm[l] - F0))) for l in nulls)
    best = {l: -np.inf for l in nulls}
    emax = -np.inf
    for m in nulls:
        for l in nulls:
            if l <= m:
                continue
            Fml = D.F((0, 1, m, l))
            # odds of adding l at S0+m, and of adding m at S0+l
            a, b = Fml - Fm[m], Fml - Fm[l]
            best[l] = max(best[l], a)
            best[m] = max(best[m], b)
            emax = max(emax, a, b)
    lam1 = sum(1 / (1 + np.exp(-v)) for v in best.values())
    return lam0, lam1, 1 / (1 + np.exp(-emax))


if __name__ == "__main__":
    lines = ["kind | p | n | median Lam0 | median Lam1=NL0(1) | median edel2=UDEL(2) | (L+4)*median Lam1"]
    for p in [60, 120, 250, 500, 1000]:
        n = int(np.ceil(p ** (1 / 0.9))) + 2
        L = int(np.ceil(np.log2(n + 1)))
        for kind in ["EQ", "BLK"]:
            Sg, th = design(p, kind)
            reps = REPS if p <= 500 else 3
            res = np.array([stats(Data(Sg, th, n, np.random.default_rng(1000 * p + r + (0 if kind == "EQ" else 7)))) for r in range(reps)])
            med = np.median(res, axis=0)
            lines.append(f"{kind} | {p} | {n} | {med[0]:.4f} | {med[1]:.4f} | {med[2]:.4f} | {(L + 4) * med[1]:.3f}")
            print(lines[-1], flush=True)
    txt = "\n".join(lines)
    with open(__file__.replace("scripts/nl0_equicorr.py", "results/nl0_equicorr.txt"), "w") as f:
        f.write(txt + "\n")
