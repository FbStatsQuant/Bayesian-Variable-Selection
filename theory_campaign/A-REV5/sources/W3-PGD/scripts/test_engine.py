"""Brute-force check of pgd_core.Engine on random small correlation matrices (seed 1)."""
import itertools, numpy as np
from pgd_core import Engine, region_batches, penalties

rng = np.random.default_rng(1)

def Delta(Sig, th, T):
    T = list(T); S0 = np.flatnonzero(th)
    tSt = th @ Sig @ th
    if not T: return tSt
    b = Sig[:, S0] @ th[S0]
    return tSt - b[T] @ np.linalg.solve(Sig[np.ix_(T, T)], b[T])

worst = 0.0
for rep in range(30):
    c = 9
    A = rng.standard_normal((40, c)) @ np.diag(rng.uniform(.3, 1, c)) + rng.standard_normal((40, 1)) * rng.uniform(0, 1.5)
    Sig = np.corrcoef(A, rowvar=False)
    tp = np.sort(rng.choice(c, 3, replace=False))
    th = np.zeros(c); th[tp] = rng.uniform(.5, 2, 3) * rng.choice([-1, 1], 3)
    n = 200
    E = Engine(Sig, th, tp, n=n, sigma2=1.0, p_prior=c)
    extras = [x for x in range(c) if x not in tp]
    pen = penalties(n, c)
    for idx in region_batches(tp, extras, 3, 2):
        out = E.batch(idx, want_erc=True, want_fbar=True)
        for b, S in enumerate(idx):
            S = list(S); Sset = set(S); DS = Delta(Sig, th, S)
            prog, non, fprog, fnon = [], [], [], []
            def Fb(D, k): return -E.nu*np.log((E.N-k)/E.N + D) - pen[k]
            fnon.append(Fb(DS, len(S)))
            for x in range(c):
                if x in Sset: continue
                T = sorted(S + [x]); r = DS - Delta(Sig, th, T)
                (prog if th[x] != 0 else non).append(r); (fprog if th[x] != 0 else fnon).append(Fb(DS - r, len(T)))
            for i in S:
                T = [y for y in S if y != i]; r = DS - Delta(Sig, th, T)
                (non if th[i] != 0 else prog).append(r); (fnon if th[i] != 0 else fprog).append(Fb(DS - r, len(T)))
                for x in range(c):
                    if x in Sset: continue
                    T2 = sorted(T + [x]); r = DS - Delta(Sig, th, T2)
                    isprog = (th[i] == 0 and th[x] != 0)
                    (prog if isprog else non).append(r); (fprog if isprog else fnon).append(Fb(DS - r, len(T2)))
            Rp, R0 = max(prog) if prog else -np.inf, max(non) if non else -np.inf
            worst = max(worst, abs(Rp - out['Rp'][b]) if np.isfinite(Rp) else 0, abs(R0 - out['R0'][b]) if np.isfinite(R0) else 0,
                        abs(DS - out['Delta'][b]))
            if fprog:
                worst = max(worst, abs((max(fprog) - max(fnon)) - out['Fbar_margin'][b]))
            # GERC brute force
            M = [t for t in tp if t not in Sset]
            if M:
                def res(Sig, S, u, v):
                    if not S: return Sig[u, v]
                    return Sig[u, v] - Sig[u, S] @ np.linalg.solve(Sig[np.ix_(S, S)], Sig[S, v])
                ercs = []
                for l in extras:
                    if l in Sset: continue
                    RMM = np.array([[res(Sig, S, j, k) for k in M] for j in M])
                    RMl = np.array([res(Sig, S, j, l) for j in M])
                    cf = np.linalg.solve(RMM, RMl)
                    ercs.append(np.sum(np.abs(cf) * np.sqrt(np.diag(RMM))) / np.sqrt(res(Sig, S, l, l)))
                if ercs: worst = max(worst, abs(max(ercs) - out['GERC'][b]))
print("max abs discrepancy engine vs brute force:", worst)
