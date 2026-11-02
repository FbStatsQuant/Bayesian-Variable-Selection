"""EXH-A (referee): exhaustive check of W1 Lemma 2, Theorem A (A1-A5), Prop 1 on small designs.

Designs: p = 15, s0 = 3 (1-based truths 3, 7, 14 -> the gen_dev_data.R truth() rule with step 1),
coefficients (1.4, -1.0, 1.8) * c, scenarios S1-S6 (scenario_covariance of gen_dev_data.R, re-implemented here),
n in {40, 80}, c in {0.25, 0.5, 1.0}, 20 replicates per cell -> 720 datasets.
Seed of dataset = 31_000_000 + 100000*scen + 1000*n + 100*int(4*c) + rep.
On R = R_{3,2} (= R_2, all 8 * 79 = 632 states) we compute M(S) for every state and check, per dataset:
  P1  literal TD(2,0) strict holds?             (Prop 1 predicts never)
  P1b literal TD(0,0) strict on R_0 holds, and does it imply TD'_P(R_0)?   (A5 claim)
  A1  TD'_inf(R) <=> every uncapped path from R stays in R and ends at S0; length <= r_R(S)
  A2  TD'_P(R)  => path from S stays in Lat(S), Phi strictly decreases, #moves = m + e - sigma >= max(m, e)
  A3  TD'_P(R)  => production search with ell = a + d from every S in R returns S0, certified, and every model
                   scored by the search has F <= F(S0)
  A3L lattice version per centre S: (L) and D_{S'} on Lat(S) minus S0  =>  search from S (ell = Phi(S)) certifies S0
  A5b TD'_P(R) => TD'_inf(R)
  L2b NA_2 and TL_2 => M(S0) = None and M(S0 u P) is an extra deletion for every 1 <= |P| <= 2
Output: counts of each premise and of each violation (any violation is printed).
"""
import itertools, sys, json
import numpy as np
from vt_core import Model, standardise, region, phi, mis_ext
from conditions import literal_TD, TDP, TDinf


def cov(s, p):
    g = np.arange(p) // 5
    H = (g[:, None] == g[None, :]).astype(float); I = np.eye(p)
    if s == 1: return I
    if s == 2: i = np.arange(p); return 0.5 ** np.abs(i[:, None] - i[None, :])
    if s == 3: return 0.7 * H + 0.3 * I
    if s == 4: return 0.85 * H + 0.15 * I
    if s == 5: return 0.3 + 0.4 * H + 0.3 * I
    rho = 0.4 + 0.1 * (g % 6); S = H * rho[:, None]; np.fill_diagonal(S, 1.0); return S


def data(s, n, c, seed, p=15):
    rng = np.random.default_rng(seed)
    Xr = rng.standard_normal((n, p)) @ np.linalg.cholesky(cov(s, p)).T
    Xr = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
    S0 = (2, 6, 13); beta = np.zeros(p); beta[list(S0)] = [1.4, -1.0, 1.8]
    y = c * Xr @ beta + rng.standard_normal(n)
    X, y = standardise(Xr, y)
    return X, y, S0


def lattice(S, S0):
    S0s = set(S0); U = [x for x in S if x in S0s]; P = [x for x in S if x not in S0s]
    miss = [x for x in S0 if x not in set(S)]
    out = []
    for k in range(len(miss) + 1):
        for A in itertools.combinations(miss, k):
            for e in range(len(P) + 1):
                for B in itertools.combinations(P, e):
                    out.append(tuple(sorted(U + list(A) + list(B))))
    return out


def D_event(M, S, S0):
    nb, f = M.scan(S)
    prog = [f[t] for t, T in enumerate(nb) if phi(T, S0) < phi(S, S0)]
    non = [f[t] for t, T in enumerate(nb) if phi(T, S0) >= phi(S, S0)]
    if not prog: return False
    return max(prog) > max([M.F(S)] + non)


def scored_by_search(M, S, ell):
    out = M.local_search(S, ell)
    sc = []
    for C in out['path']:
        sc += M.nbrs(C)
    return out, max(M.F(T) for T in sc + out['path'])


def one(s, n, c, rep):
    seed = 31_000_000 + 100000 * s + 1000 * n + 100 * int(4 * c) + rep
    X, y, S0 = data(s, n, c, seed)
    M = Model(X, y)
    nulls = [j for j in range(M.p) if j not in S0]
    a, d = 3, 2
    R = region(S0, nulls, a, d); Rs = set(R)
    R0 = region(S0, nulls, a, 0)
    res = dict(scen=s, n=n, c=c, rep=rep)
    res['litTD2'] = not literal_TD(M, S0, R, 0.0, True)
    res['litTD0'] = not literal_TD(M, S0, R0, 0.0, True)
    res['TDP0'] = not TDP(M, S0, R0)
    tdp = not TDP(M, S0, R); tdi = not TDinf(M, S0, R)
    res['TDP'] = tdp; res['TDinf'] = tdi
    viol = []
    # A1
    allpaths_ok = True
    for S in R:
        path = M.greedy_uncapped(S)
        ok = all(T in Rs for T in path) and path[-1] == S0
        allpaths_ok &= ok
        if tdi:
            rR = sum(1 for T in R if M.F(T) > M.F(S))
            if len(path) - 1 > rR: viol.append(('A1len', S))
        if tdp:
            L = set(lattice(S, S0))
            if not all(T in L for T in path): viol.append(('A2lat', S))
            ph = [phi(T, S0) for T in path]
            if any(ph[i + 1] >= ph[i] for i in range(len(ph) - 1)): viol.append(('A2phi', S))
            m, e = mis_ext(S, S0)
            sig = sum(1 for i in range(len(path) - 1) if len(path[i]) == len(path[i + 1]))
            if len(path) - 1 != m + e - sig or len(path) - 1 < max(m, e): viol.append(('A2count', S))
            out, mx = scored_by_search(M, S, a + d)
            if not (out['returned'] == S0 and out['certified'] and mx <= M.F(S0)): viol.append(('A3', S))
    if allpaths_ok != tdi: viol.append(('A1iff', allpaths_ok, tdi))
    if tdp and not tdi: viol.append(('A5b',))
    # A3 lattice version, per centre
    nlat = 0
    Dc = {}
    for S in R:
        if S == S0: continue
        Dc[S] = D_event(M, S, S0)
    L_ok = M.M(S0) is None
    for S in R:
        if S == S0: continue
        if L_ok and all(Dc[T] for T in lattice(S, S0) if T != S0):
            nlat += 1
            out = M.local_search(S, phi(S, S0))
            if not (out['returned'] == S0 and out['certified']): viol.append(('A3L', S))
    res['n_lattice_centres'] = nlat
    # Lemma 2(b)
    NA = True; TL = True
    sup = [tuple(sorted(S0 + P)) for e in range(d + 1) for P in itertools.combinations(nulls, e)]
    for T in sup:
        nb, f = M.scan(T); FT = M.F(T)
        for U, fu in zip(nb, f):
            added = set(U) - set(T); removed = set(T) - set(U)
            if removed & set(S0):
                if not fu < FT: TL = False
            elif len(U) == len(T) + 1 and len(T) - len(S0) <= d:   # null addition at S0 u P', |P'| <= d
                if not fu < FT: NA = False
    res['NA'] = NA; res['TL'] = TL
    if NA and TL:
        if M.M(S0) is not None: viol.append(('L2b0',))
        for T in sup:
            if T == S0: continue
            U = M.M(T)
            if U is None or not (len(U) == len(T) - 1 and not (set(T) - set(U)) & set(S0)): viol.append(('L2b', T))
    res['viol'] = viol
    return res


def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    out = []
    for s in range(1, 7):
        for n in (40, 80):
            for c in (0.25, 0.5, 1.0):
                for rep in range(reps):
                    r = one(s, n, c, rep); out.append(r)
                    if r['viol']: print('VIOLATION', r, flush=True)
        print('scenario', s, 'done', file=sys.stderr, flush=True)
    keys = ['litTD2', 'litTD0', 'TDP0', 'TDP', 'TDinf', 'NA', 'TL']
    print('datasets', len(out))
    for k in keys:
        print(k, sum(r[k] for r in out))
    print('litTD0 & not TDP0 (A5 counterexamples):', sum(r['litTD0'] and not r['TDP0'] for r in out))
    print('TDinf & not TDP:', sum(r['TDinf'] and not r['TDP'] for r in out))
    print('NA & TL:', sum(r['NA'] and r['TL'] for r in out))
    print('lattice-certified centres (total):', sum(r['n_lattice_centres'] for r in out))
    print('violations:', sum(len(r['viol']) for r in out))
    by = {}
    for r in out:
        key = (r['n'], r['c']); b = by.setdefault(key, [0, 0, 0, 0]); b[0] += 1; b[1] += r['TDP']; b[2] += r['TDinf']; b[3] += r['litTD0'] and not r['TDP0']
    for k in sorted(by): print('n=%d c=%.2f: N=%d TD\'_P(R_2)=%d TD\'_inf(R_2)=%d A5-cex=%d' % (k + tuple(by[k])))
    json.dump(out, open('../results/exhaust_theoremA.json', 'w'), default=str)


if __name__ == '__main__':
    main()
