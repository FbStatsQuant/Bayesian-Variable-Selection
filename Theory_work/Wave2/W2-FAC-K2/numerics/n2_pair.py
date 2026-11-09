"""n2_pair.py -- N2: direct test of the predicted LS0 trap. For a truth-free class c with effective kappa_c < 1,
T = S0 u {j, l} with j, l the class-c nulls of largest positive / most negative xi. Full scan of T: is every
neighbour worse (local maximum => LS0 cannot leave T; S0 is not a neighbour)? Also the prediction
G_del ~ Delta_k - (1/2)(2+kappa)/(1+kappa) xi^2  and the asymptotic criterion log p/log n > (1+kappa)/2.
Usage: python n2_pair.py  -> N2_out.txt"""
import sys, math, json, numpy as np
import mc_core as mc

def one(n, p_each, R, truths_cls0, seed, cls_free=1):
    cls = np.concatenate([np.full(p_each, 0), np.full(p_each, 1)])
    D = mc.MCDesign(cls, np.array(R, float))
    p = D.p
    th = np.zeros(p); S0 = []
    for pos, coef in truths_cls0:
        th[pos] = coef; S0.append(pos)
    rng = np.random.default_rng(seed)
    P = mc.MCData(D, th, n, rng)
    nulls_c = np.flatnonzero((cls == cls_free) & (th == 0))
    j = int(nulls_c[np.argmax(P.xi[nulls_c])]); l = int(nulls_c[np.argmin(P.xi[nulls_c])])
    T = sorted(S0 + [j, l])
    sc = P.scan(T, full_swaps=True)
    FT = sc["FT"]
    Tarr = np.array(T)
    gd = sc["del"] - FT; ga = sc["add"] - FT; gs = sc["swap"] - FT
    k = len(T)
    kap = D.kappa_eff(np.array([len(S0), 0.0]))[cls_free]
    Dk = math.log((2 * p - k) / k) + 0.5 * math.log(n + 1)
    pred_j = Dk - 0.5 * (2 + kap) / (1 + kap) * P.xi[j] ** 2
    pred_l = Dk - 0.5 * (2 + kap) / (1 + kap) * P.xi[l] ** 2
    ij = list(T).index(j); il = list(T).index(l)
    best_other = max(ga.max(), gs.max(), gd[[i for i in range(k) if i not in (ij, il)]].max())
    return dict(n=n, p=p, seed=seed, kappa_eff=kap, crit=math.log(p) / math.log(n), thr=(1 + kap) / 2,
                xi_j=float(P.xi[j]), xi_l=float(P.xi[l]), H=math.sqrt(2 * math.log(2 * p_each)),
                g_del_j=float(gd[ij]), g_del_l=float(gd[il]), pred_j=pred_j, pred_l=pred_l,
                best_add=float(ga.max()), best_swap=float(gs.max()), best_other_del=float(gd[[i for i in range(k) if i not in (ij, il)]].max()),
                local_max=bool(max(gd.max(), ga.max(), gs.max()) < 0),
                g_S0_vs_T=float(P.F(S0) - FT))

if __name__ == "__main__":
    truths = [(3, 1.4), (27, -1.0), (54, 1.8), (76, -1.2)]
    out = open("N2_out.txt", "w")
    def log(s):
        print(s); out.write(s + "\n"); out.flush()
    log("N2: pair trap test. T = S0 u {j,l}, j/l = extreme +/- xi of the truth-free class. local_max = all neighbours worse.")
    for R, lab in [([[0.5, 0.0], [0.0, 0.7]], "indep r22=.7"), ([[0.5, 0.3], [0.3, 0.7]], "r12=.3 r22=.7"),
                   ([[0.5, 0.0], [0.0, 0.3]], "indep r22=.3 (control)"), ([[0.5, 0.3], [0.3, 0.9]], "r12=.3 r22=.9")]:
        for n, pe in [(8000, 2000), (20000, 5000), (10 ** 5, 10 ** 4), (10 ** 6, 10 ** 4), (10 ** 6, 2 * 10 ** 4), (10 ** 8, 2 * 10 ** 4)]:
            for seed in [1, 2]:
                r = one(n, pe, R, truths, seed)
                log(f"{lab:24s} n={n:>9d} p={r['p']:>6d} seed={seed} logp/logn={r['crit']:.3f} thr=(1+k)/2={r['thr']:.3f} kappa_eff={r['kappa_eff']:.3f} "
                    f"xi=({r['xi_j']:+.2f},{r['xi_l']:+.2f}) H={r['H']:.2f} | G_del(j)={r['g_del_j']:+.2f} (pred {r['pred_j']:+.2f}) "
                    f"G_del(l)={r['g_del_l']:+.2f} (pred {r['pred_l']:+.2f}) best_add={r['best_add']:+.2f} best_swap={r['best_swap']:+.2f} "
                    f"| LOCAL MAX={r['local_max']}  F(S0)-F(T)={r['g_S0_vs_T']:+.2f}")
    out.close()
