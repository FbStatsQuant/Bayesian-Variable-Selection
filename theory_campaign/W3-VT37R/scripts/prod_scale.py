"""PROD (referee): independent production-scale re-run (n = 200, p = 500, s0 = 14, truth() of gen_dev_data.R, S1-S6,
c in {1, 0.5}). Own generator (numpy; NOT the benchmark's R streams and NOT W1's seeds), own scorer (vt_core).
Seed of dataset = 52_000_000 + 10000*scen + 100*int(10*c) + rep; centre rng = seed + 7.

Per dataset:
  (L)   is S0 a strict local max of the flip/swap neighbourhood? which class beats it?
  R20   all states S0 - A, |A| in {1, 2} (105 states): class of M(S) (progress / non-progress / None)
        and whether literal TD(1) at S holds (best truth addition beats every other move) and whether it is improving.
  CEN   12 sampled centres S = (S0 - A) u P, |A| in {1,2}, |P| in {0,1,2}, P look-alikes (same 5-group as a missing
        truth) or uniform nulls: production local search, ell = 10. Record: E_LS (F(S0) > F(S_c)); reached S0;
        certified; local_limit; all moves progress; #moves vs Phi; if not reached: F(end) - F(S0) (>= 0 means the
        CEX-2 pattern: E_LS held but the search ended at a model at least as good as S0).
Exact score ties are checked for (none expected); best move = argmax with lexicographic tie rule.
Usage: python3 prod_scale.py <reps> > ../results/prod_scale.json
"""
import sys, json, time
import numpy as np
from vt_core import Model, standardise
from exhaust_theoremA import cov


def truth500():
    s0, step = 14, 7
    pos = [3, 2, 4, 1, 5, 3]; pat = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0); block = 1 + step * k
    act = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1
    return act, np.array([pat[i % 6] for i in k])


def gen(s, c, seed, n=200, p=500):
    rng = np.random.default_rng(seed)
    Xr = rng.standard_normal((n, p)) @ np.linalg.cholesky(cov(s, p)).T
    Xr = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
    act, b = truth500(); beta = np.zeros(p); beta[act] = b
    eps = rng.standard_normal(n)
    X, y = standardise(Xr, c * Xr @ beta + eps)
    return X, y, tuple(sorted(int(a) for a in act))


class Fast(Model):
    def scan_arr(self, S):
        S = np.array(sorted(S), dtype=int); k = len(S); p = self.p
        mask = np.ones(p, bool); mask[S] = False; out = np.nonzero(mask)[0]
        rows, ii, jj = [], [], []
        if k < self.K:
            rows.append((np.concatenate([np.repeat(S[None, :], len(out), 0), out[:, None]], 1), np.full(len(out), -1), out))
        if k > 0:
            rows.append((np.array([np.delete(S, t) for t in range(k)]).reshape(k, k - 1), S.copy(), np.full(k, -1)))
            for t in range(k):
                rest = np.delete(S, t)
                rows.append((np.concatenate([np.repeat(rest[None, :], len(out), 0), out[:, None]], 1), np.full(len(out), S[t]), out))
        F, I, J = [], [], []
        for idx, i, j in rows:
            idx = np.sort(idx, 1)
            F.append(self.Fmany([tuple(r) for r in idx]) if idx.shape[1] > 0 else self.Fmany([()] * len(idx)))
            I.append(i); J.append(j)
        return np.concatenate(F), np.concatenate(I), np.concatenate(J)

    def best(self, S):
        f, i, j = self.scan_arr(S)
        mx = f.max(); F0 = self.F(S)
        if not mx > F0:
            return None, f, i, j
        cand = np.nonzero(f == mx)[0]
        res = [apply(S, i[t], j[t]) for t in cand]
        t = cand[int(np.argmin([0 for _ in res]))] if len(cand) == 1 else cand[min(range(len(res)), key=lambda u: res[u])]
        return t, f, i, j


def apply(S, i, j):
    S = set(S)
    if i >= 0: S.discard(int(i))
    if j >= 0: S.add(int(j))
    return tuple(sorted(S))


def lab(i, j, S0s):
    ti = None if i < 0 else (int(i) in S0s); tj = None if j < 0 else (int(j) in S0s)
    if ti is None: return 'add_truth' if tj else 'add_null'
    if tj is None: return 'del_truth' if ti else 'del_extra'
    return {(True, True): 'swap_t->t', (True, False): 'swap_t->null', (False, True): 'swap_x->t', (False, False): 'swap_n->n'}[(ti, tj)]


PROG = {'add_truth', 'del_extra', 'swap_x->t'}


def search(M, S, S0s, ell):
    labs = []; moves = 0
    while True:
        t, f, i, j = M.best(S)
        if t is None:
            return S, True, False, labs
        if moves >= ell:
            return apply(S, i[t], j[t]), False, True, labs
        labs.append(lab(i[t], j[t], S0s)); S = apply(S, i[t], j[t]); moves += 1


def one(s, c, rep):
    seed = 52_000_000 + 10000 * s + 100 * int(10 * c) + rep
    X, y, S0 = gen(s, c, seed)
    M = Fast(X, y); S0s = set(S0); p = M.p
    rec = dict(scen=s, c=c, rep=rep, seed=seed, ell=M.ell)
    t, f, i, j = M.best(S0)
    rec['S0_locmax'] = t is None
    rec['S0_beaten_by'] = None if t is None else lab(i[t], j[t], S0s)
    # R20
    cls = {}; td1 = 0; td1_pos = 0; td1_nonpos = 0
    for a in (1, 2):
        import itertools
        for A in itertools.combinations(S0, a):
            S = tuple(x for x in S0 if x not in A)
            t, f, i, j = M.best(S)
            L = 'none' if t is None else lab(i[t], j[t], S0s)
            cls[L] = cls.get(L, 0) + 1
            # literal TD(1): best truth addition strictly beats every other move
            labs = [lab(a_, b_, S0s) for a_, b_ in zip(i, j)]
            ta = [u for u in range(len(f)) if labs[u] == 'add_truth']
            u = max(ta, key=lambda q: f[q]); others = np.delete(f, u)
            if f[u] > others.max():
                td1 += 1
                if f[u] > M.F(S): td1_pos += 1
                else: td1_nonpos += 1
    rec['R20_classes'] = cls; rec['R20_litTD1'] = td1; rec['R20_litTD1_nonimproving'] = td1_nonpos
    # centres
    rng = np.random.default_rng(seed + 7); g = np.arange(p) // 5
    nulls = np.array([q for q in range(p) if q not in S0s])
    cen = []
    for a in (1, 2):
        for e in (0, 1, 2):
            for kind in (('look', 'unif') if e else ('none',)):
                for _ in range(2 if e else 1):
                    A = [int(x) for x in rng.choice(S0, a, replace=False)]
                    if kind == 'look':
                        cand = [q for q in nulls if g[q] in {g[x] for x in A}]
                    else:
                        cand = list(nulls)
                    P = [int(x) for x in rng.choice(cand, min(e, len(cand)), replace=False)] if e else []
                    cen.append((a, e, kind, tuple(sorted([x for x in S0 if x not in A] + P))))
    F0 = M.F(S0); out = []
    for a, e, kind, S in cen:
        end, cert, lim, labs = search(M, S, S0s, M.ell)
        out.append(dict(a=a, e=e, kind=kind, ELS=bool(F0 > M.F(S)), reached=end == S0, certified=cert, limit=lim,
                        allprog=all(l in PROG for l in labs), moves=len(labs), Phi=a + e, end_minus_S0=M.F(end) - F0,
                        labs=labs))
    rec['centres'] = out
    return rec


def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    res = []; t0 = time.time()
    for s in range(1, 7):
        for c in (1.0, 0.5):
            for rep in range(reps):
                r = one(s, c, rep); res.append(r)
                print('S%d c=%.1f rep=%d %.0fs locmax=%s reached=%d/%d' % (s, c, rep, time.time() - t0, r['S0_locmax'],
                      sum(x['reached'] for x in r['centres']), len(r['centres'])), file=sys.stderr, flush=True)
    json.dump(res, sys.stdout, default=float)


if __name__ == '__main__':
    main()
