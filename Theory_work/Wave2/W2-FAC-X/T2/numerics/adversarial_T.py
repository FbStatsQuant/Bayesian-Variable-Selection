"""adversarial_T.py -- the uniform-over-T bounds of Theorem T2-S (L4r.2) on sets that the path does NOT visit.
For each design and data set: T_m := S0 u {the m low-class nulls with the largest positive xi} (the configuration that
makes the class-max centre l_hi X_T ~ R * sqrt(Z_m^2) in L4r.2(b)).  At each T_m compute exactly (closed form):
  X_T, l_hi X_T / Hbar, the best null-deletion gain, the best addition gain, and check
  (L4r.2(a))  some kept null has |tau| <= Hbar + |varrho|/l'_lo   ["exist"],
  (L4r.2(b))  |X_T| <= sqrt(Z_m^2 + 2)/l'_lo + |varrho|          ["Xbound"],
and report max_m (best addition gain)/log n.  Shows: (i) the lemmas hold; (ii) for R large there are sets T >= S0 with
POSITIVE addition gains at moderate log p/log n -- so the uniform route cannot go beyond A_S without path information.
Usage: py -3.13 adversarial_T.py > adversarial_T_out.txt"""
import math
import numpy as np
import eg_core as eg


def gains_at(P, T):
    n, nu, lw = P.n, P.nu, P.logw
    T = np.asarray(sorted(T)); inT = np.zeros(P.p, bool); inT[T] = True; O = np.flatnonzero(~inT)
    k = len(T)
    Q = (n - 1) - n * P.quad_closed(T); psiT = 0.02 + Q
    Dp = 1 + float(P.lp[T] @ P.lp[T]); Dpp = 1 + float(P.lpp2[T].sum())
    X = (float(P.lp[T] @ P.zc[T]) - P.rho0) / Dp
    tau = P.zc[T] - P.lp[T] * X
    gp = P.lp[T] ** 2 / (Dp - P.lp[T] ** 2)
    dL = P.logdr[T] + np.log(Dp) - np.log(Dp - P.lp[T] ** 2) - np.log(Dpp) + np.log(Dpp - P.lpp2[T])
    Gd = (lw[k - 1] - lw[k]) + 0.5 * dL - nu * np.log1p(n * (1 + gp) * P.k1sq * tau ** 2 / psiT)
    tl = P.zc[O] - P.lp[O] * X
    dQa = n * (1 - P.lp[O] ** 2 / (Dp + P.lp[O] ** 2)) * P.k1sq * tl ** 2
    dLa = P.logdr[O] + np.log(Dp + P.lp[O] ** 2) - np.log(Dp) - np.log(Dpp + P.lpp2[O]) + np.log(Dpp)
    Ga = (lw[k + 1] - lw[k]) - 0.5 * dLa - nu * np.log1p(-dQa / psiT)
    isN = ~P.isT[T]
    return X, tau[isN], float(Gd[isN].max()) if isN.any() else -np.inf, float(Ga.max())


def main():
    print("design            n      p    logp/logn  A_S     max_m addgain/logn  (at m, l_hi X/Hbar)   exist_ok  Xbound_ok")
    for vals, tag in [((math.sqrt(0.5), math.sqrt(0.5) + 1e-12), "cs05"), ((0.6, 0.8), "r2_06_08"),
                      ((0.3, 0.9), "r2_03_09"), ((0.2, 0.95), "r2_02_095")]:
        for n, p in [(10 ** 6, 2000), (10 ** 10, 2000), (10 ** 16, 300)]:
            rng = np.random.default_rng(5 + p)
            lam = np.array([vals[i % 2] for i in range(p)]); lam = lam[rng.permutation(p)]
            th = np.zeros(p); th[int(np.flatnonzero(lam == vals[0])[0])] = 1.2   # truth in the low class (kappa_S small)
            P = eg.EGData(lam, th, n, rng)
            ell = P.ell; lo = vals[0]; lhi = ell.max(); lplo = P.lp[~P.isT].min()
            nulls = np.flatnonzero(~P.isT)
            Hbar = math.sqrt(2 * math.log(2 * len(nulls) + 2) + 2 * math.log(math.log(n)))
            low_pos = nulls[(lam[nulls] == lo) & (P.xi[nulls] > 0)]
            low_pos = low_pos[np.argsort(-P.xi[low_pos])]
            S0 = list(P.S0)
            absxi = np.sort(np.abs(P.xi[nulls]))[::-1]
            best = (-np.inf, None, None); ex_ok = xb_ok = True
            for m in sorted(set([1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 300, 500]) & set(range(1, len(low_pos) + 1))):
                T = S0 + list(low_pos[:m])
                X, tauN, gdel, gadd = gains_at(P, T)
                ex_ok &= bool(np.abs(tauN).min() <= Hbar + abs(P.varrho) / lplo)
                Zm2 = float((absxi[:m] ** 2).sum()) / m          # empirical: replaces Z_m^2 + 2 (sum bound)
                xb_ok &= bool(abs(X) <= math.sqrt(Zm2) / lplo + abs(P.varrho))
                if gadd > best[0]:
                    best = (gadd, m, lhi * abs(X) / Hbar)
            As = min(1 / (2 * max(1, lhi ** 2 / (1 + float((ell[P.S0] ** 2).sum())))), 1 / (2 * ((1 + lhi / ell.min()) ** 2 - 1)))
            print("%-12s n=%-6g p=%-5d %.3f      %.4f   %+.3f              (m=%d, %.2f)            %s      %s" % (
                tag, n, p, math.log(p) / math.log(n), As, best[0] / math.log(n), best[1], best[2], ex_ok, xb_ok))


if __name__ == "__main__":
    main()
