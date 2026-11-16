"""Item 4: Lemma T search.  p_raw=50, d in {1,2,3}, n in {100,1000}, laws gauss / t_{2.1} / atom(mass 1-1/n at x=0, else N(0,I)).
Maximise  F(a,u,c) = E_x min{1,(a+u'x)^2/c} - 2 n^-1 sum_i min{1,(a+u'x_i)^2/c}  over a, u (d-sparse), c>0.
Reduction: g depends only on w=(a,u)/sqrt(c), g = min{1,(w0+w'x_S)^2}; so the search is over the support S and w in R^{d+1}.
Population expectation: fresh sample of NF rows (atom law: exact atom part + fresh non-atom rows, weight 1/n).
Search = random restarts (4 initialisations) + Nelder-Mead + support-swap rounds.  Reports max over restarts (a LOWER bound for the sup).
Compare with eta^2_n(d, 0.05) = (4/n)[d log(e p/d) + 2(d+1) log(2 e n/(d+1)) + log(4/delta)].
usage: python3 -B item4_lemmaT.py NWORK NDS NRESTART      DRAFT (by this seat, unchecked)"""
import sys, time, math, pickle
from multiprocessing import Pool
from fcommon import *
from scipy.optimize import minimize
P = 50
NF = 40000
DELTA = 0.05

def eta2(n, d, delta=DELTA, p=P):
    return 4.0 / n * (d * math.log(math.e * p / d) + 2 * (d + 1) * math.log(2 * math.e * n / (d + 1)) + math.log(4 / delta))

def gen(law, m, n, rng, nonatom_only=False):
    if law == "gauss":
        return rng.standard_normal((m, P))
    if law == "t2.1":
        return rng.standard_t(2.1, size=(m, P))
    if law == "atom":
        Z = rng.standard_normal((m, P))
        if nonatom_only:
            return Z
        keep = rng.random(m) < 1.0 / n
        return Z * keep[:, None]
    raise ValueError

class Obj:
    def __init__(self, X, Fr, law, n):
        self.X, self.F, self.law, self.n = X, Fr, law, n
        self.watom = (1 - 1.0 / n) if law == "atom" else 0.0
        self.wf = 1.0 / n if law == "atom" else 1.0
    def val(self, S, w):
        xs = self.X[:, S]; fs = self.F[:, S]
        gs = np.minimum(1.0, (w[0] + xs @ w[1:]) ** 2)
        gf = np.minimum(1.0, (w[0] + fs @ w[1:]) ** 2)
        Pg = self.wf * gf.mean() + self.watom * min(1.0, w[0] ** 2)
        return Pg - 2 * gs.mean()

def nm(obj, S, w0, maxfev=250):
    f = lambda w: -obj.val(S, w)
    r = minimize(f, w0, method="Nelder-Mead", options=dict(maxfev=maxfev, xatol=1e-4, fatol=1e-6, adaptive=True))
    return -r.fun, r.x

def init_w(obj, S, kind, rng, d):
    X = obj.X
    if kind == 0:     # hyperplane through d random sample rows, narrow slab
        rows = rng.choice(len(X), size=d, replace=False)
        A = np.column_stack([np.ones(d), X[np.ix_(rows, S)]])
        _, _, Vt = np.linalg.svd(A)
        w = Vt[-1]
        if d > 1 or True:
            w = w + 0.0
        sc = math.exp(rng.uniform(-1.0, 3.0))
        w = w / np.linalg.norm(w[1:]) * sc
        return w
    if kind == 1:     # random narrow slab
        u = rng.standard_normal(d); u /= np.linalg.norm(u)
        sc = math.exp(rng.uniform(0.0, 4.0))
        a = rng.standard_normal() * 0.5
        return np.concatenate([[a * sc], u * sc])
    if kind == 2:     # slab centred at the sample median of the projection, width ~ sample spread
        u = rng.standard_normal(d); u /= np.linalg.norm(u)
        pr = X[:, S] @ u
        m, s = np.median(pr), pr.std() + 1e-9
        sc = rng.uniform(0.5, 3.0) / s
        return np.concatenate([[-m * sc], u * sc])
    if kind == 3:     # slab through the atom (w0 = 0), random direction
        u = rng.standard_normal(d); u /= np.linalg.norm(u)
        sc = math.exp(rng.uniform(0.0, 5.0))
        return np.concatenate([[0.0], u * sc])
    # kind 4: w0 = 0, u orthogonal to the d-1 sample rows of largest norm on S (kills g on them), large scale
    nr = np.linalg.norm(X[:, S], axis=1)
    top = np.argsort(-nr)[:d - 1]
    if d == 1:
        u = np.ones(1)
    else:
        _, _, Vt = np.linalg.svd(X[np.ix_(top, S)])
        u = Vt[-1]
    sc = math.exp(rng.uniform(1.0, 5.0))
    return np.concatenate([[0.0], u * sc])

def one(args):
    law, n, d, rep, nrest = args
    rng = np.random.default_rng([20261116, 4, n, d, hash(law) % 9973, rep])
    X = gen(law, n, n, rng)
    Fr = gen(law, NF, n, rng, nonatom_only=True).astype(np.float64)
    obj = Obj(X, Fr, law, n)
    best = (-9.0, None, None)
    results = []
    # heavy-tail / atom helpful supports: columns with the most extreme sample values
    ext = np.argsort(-np.abs(X).max(0))
    for r in range(nrest):
        S = np.sort(rng.choice(P, size=d, replace=False)) if r % 3 else np.sort(ext[rng.choice(10, size=d, replace=False)])
        w0 = init_w(obj, S, r % 5, rng, d)
        v, w = nm(obj, S, w0)
        # support-swap rounds (evaluate same w with one coordinate replaced, polish the best)
        for _ in range(2):
            cand = []
            for k in range(d):
                for j in range(P):
                    if j in S: continue
                    S2 = S.copy(); S2[k] = j
                    cand.append((obj.val(S2, w), S2))
            vb, S2 = max(cand, key=lambda t: t[0])
            if vb > v - 0.002:
                v2, w2 = nm(obj, S2, w, maxfev=150)
                if v2 > v:
                    v, w, S = v2, w2, S2
        results.append(v)
        if v > best[0]:
            best = (v, S.copy(), w.copy())
    return dict(law=law, n=n, d=d, rep=rep, best=best[0], S=best[1], w=best[2], med_restart=float(np.median(results)),
                eta2=eta2(n, d))

if __name__ == "__main__":
    nw, nds, nrest = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tasks = [(law, n, d, r, nrest) for n in (100, 1000) for d in (1, 2, 3) for law in ("gauss", "t2.1", "atom") for r in range(nds)]
    t0 = time.time()
    with Pool(nw) as pool:
        res = pool.map(one, tasks, chunksize=1)
    pickle.dump(res, open("out/item4.pkl", "wb"))
    print("done", time.time() - t0)
