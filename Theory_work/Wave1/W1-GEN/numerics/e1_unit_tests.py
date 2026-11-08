"""E1: unit tests for bvs_core.
 (a) batched score vs an independent n x n Gaussian-integral implementation (differences vs empty model)
 (b) DP start mode / log Z_0 / pi_0 vs brute force over all |S|<=K  (p<=12, 50 random cases + tie cases + user partitions)
 (c) own complete linkage vs scipy (merge heights), partition invariants
 (d) production local search vs naive re-implementation (brute neighbour list, full re-scoring) on small problems
 (e) population Lambda vs ||(I-P_T) X theta||^2 on exact-Gram designs; block-table helpers vs brute force
"""
import itertools, json, math, sys, time
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from scipy.special import logsumexp
import bvs_core as bc

rng = np.random.default_rng(20261108)
res = {}


def rand_problem(n, p, rho=0.5, s=2):
    S = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
    Xr = rng.standard_normal((n, p)) @ np.linalg.cholesky(S).T
    X = bc.standardize_X(Xr)
    th = np.zeros(p)
    th[rng.choice(p, s, replace=False)] = rng.choice([-1.0, 1.0], s) * rng.uniform(0.3, 1.5, s)
    y = bc.standardize_y(X @ th + rng.standard_normal(n))
    return X, y


# ---------------------------------------------------------------- (a)
maxdiff = 0.0
ncheck = 0
for case in range(12):
    n = int(rng.integers(30, 70))
    p = int(rng.integers(6, 15))
    X, y = rand_problem(n, p)
    prob = bc.Problem(X, y)
    d0 = bc.direct_logm(X, y, [])
    for _ in range(25):
        k = int(rng.integers(1, min(p, 8) + 1))
        U = tuple(sorted(rng.choice(p, k, replace=False).tolist()))
        a = prob.logm(U) - prob.logm0
        b = bc.direct_logm(X, y, U) - d0
        maxdiff = max(maxdiff, abs(a - b))
        ncheck += 1
res["a_score_max_abs_diff"] = maxdiff
res["a_score_ncheck"] = ncheck
print("(a) score: max |batched - independent| over", ncheck, "models:", maxdiff)

# ---------------------------------------------------------------- (b)
def brute_start(prob, blocks, tol=1e-12):
    p, K = prob.p, prob.K
    bid = bc.block_id_array(blocks, p)
    vals = {}
    for k in range(K + 1):
        for S in itertools.combinations(range(p), k):
            vals[S] = bc.log_gamma0(prob, blocks, S, bid)
    mx = max(vals.values())
    cands = [S for S, v in vals.items() if v >= mx - tol]
    mode = min(cands, key=lambda S: (len(S), S))
    logZ = float(logsumexp(np.array(list(vals.values()))))
    return mode, logZ, len(cands), vals


nok = 0
ndiff_Z = 0.0
cases = []
for case in range(50):
    n = int(rng.integers(24, 80))
    p = int(rng.integers(4, 13))
    X, y = rand_problem(n, p, rho=float(rng.uniform(0.0, 0.8)), s=int(rng.integers(1, 4)))
    prob = bc.Problem(X, y)
    if case % 3 == 2:  # user-supplied random partition
        perm = rng.permutation(p).tolist()
        sizes = []
        left = p
        while left > 0:
            s = int(rng.integers(1, min(left, 6) + 1))
            sizes.append(s)
            left -= s
        blocks, pos = [], 0
        for s in sizes:
            blocks.append(sorted(perm[pos:pos + s]))
            pos += s
        kind = "user"
    else:
        blocks = bc.partition(X)
        kind = "method"
    info = bc.start_mode(prob, blocks)
    mode, logZ, ncand, vals = brute_start(prob, blocks)
    ok = (info.mode == mode)
    ndiff_Z = max(ndiff_Z, abs(info.logZ0 - logZ))
    # pi_0 spot check
    S = tuple(sorted(rng.choice(p, int(rng.integers(0, min(prob.K, p) + 1)), replace=False).tolist()))
    pi_dp = bc.log_pi0(prob, info, S)
    pi_bf = vals[S] - logZ
    ndiff_Z = max(ndiff_Z, abs(pi_dp - pi_bf))
    nok += ok
    cases.append(dict(n=n, p=p, K=prob.K, kind=kind, nblocks=len(blocks), ok=bool(ok), nopt=ncand))
res["b_dp_vs_bruteforce_random"] = dict(cases=len(cases), mode_matches=nok, max_abs_diff_logZ_or_logpi=ndiff_Z)
print("(b) DP vs brute force, random cases:", nok, "/", len(cases), " max |dlogZ0 or dlogpi0|:", ndiff_Z)

# tie cases: duplicate columns -> exact ties between models; tie rule smallest size then lex
tie_ok = 0
tie_n = 0
for case in range(10):
    n = int(rng.integers(30, 60))
    p = 8
    X, y = rand_problem(n, p, rho=0.2, s=2)
    j, k = sorted(rng.choice(p, 2, replace=False).tolist())
    X = X.copy()
    X[:, k] = X[:, j]  # exact duplicate column
    y = bc.standardize_y(X @ (np.eye(p)[j] * 1.2) + rng.standard_normal(n))
    prob = bc.Problem(X, y)
    blocks = bc.partition(X) if case % 2 == 0 else [list(range(0, 4)), list(range(4, 8))]
    info = bc.start_mode(prob, blocks)
    mode, logZ, ncand, vals = brute_start(prob, blocks, tol=1e-9)
    tie_n += 1
    tie_ok += (info.mode == mode)
res["b_dp_vs_bruteforce_ties"] = dict(cases=tie_n, mode_matches=tie_ok)
print("(b') duplicate-column tie cases:", tie_ok, "/", tie_n)

# ---------------------------------------------------------------- (c)
mx_h = 0.0
part_ok = 0
for case in range(20):
    n = int(rng.integers(60, 200))
    p = int(rng.integers(5, 40))
    X, y = rand_problem(n, p, rho=float(rng.uniform(0.0, 0.7)))
    R = X.T @ X / (n - 1.0)
    D = 1 - np.abs(R)
    np.fill_diagonal(D, 0.0)
    Z = linkage(squareform(D, checks=False), method="complete")
    root, ch, mem, hts = bc.complete_linkage(R)
    h_own = np.sort(np.array(list(hts.values())))
    h_sp = np.sort(Z[:, 2])
    mx_h = max(mx_h, float(np.abs(h_own - h_sp).max()))
    B = bc.block_size(n, p)
    blocks = bc.partition_from_corr(R, B)
    flat = sorted(j for b in blocks for j in b)
    part_ok += (flat == list(range(p)) and max(len(b) for b in blocks) <= B)
res["c_linkage_max_height_diff_vs_scipy"] = mx_h
res["c_partition_invariants_ok"] = part_ok
print("(c) own linkage vs scipy: max sorted-height diff", mx_h, "; partition invariants ok", part_ok, "/ 20")

# ---------------------------------------------------------------- (d)
def naive_ls(prob, centre, ell):
    """independent naive local search: fresh recomputation of every neighbour by explicit set operations"""
    p, K = prob.p, prob.K
    S = frozenset(centre)
    scored = {tuple(sorted(S))}
    moves = 0
    path = [tuple(sorted(S))]
    while True:
        nb = []
        if len(S) < K:
            nb += [S | {j} for j in range(p) if j not in S]
        nb += [S - {i} for i in S]
        nb += [(S - {i}) | {j} for i in S for j in range(p) if j not in S]
        nbs = [tuple(sorted(T)) for T in nb]
        scored.update(nbs)
        fs = {T: prob.F(T) for T in nbs}
        fS = prob.F(tuple(sorted(S)))
        mx = max(fs.values()) if fs else -np.inf
        if mx > fS:
            if moves >= ell:
                return path, scored, False, True
            S = frozenset(min(T for T in nbs if fs[T] == mx))
            moves += 1
            path.append(tuple(sorted(S)))
        else:
            return path, scored, True, False


d_ok = 0
for case in range(15):
    n = int(rng.integers(40, 100))
    p = int(rng.integers(6, 14))
    X, y = rand_problem(n, p, rho=0.3, s=int(rng.integers(2, 5)))
    prob = bc.Problem(X, y)
    cen = tuple(sorted(rng.choice(p, int(rng.integers(0, 4)), replace=False).tolist()))
    ell = int(rng.integers(1, 5))
    a = bc.local_search(prob, cen, ell)
    path, scored, cert, lim = naive_ls(prob, cen, ell)
    d_ok += (a["path"] == path and a["scored"] == scored and a["certified"] == cert and a["local_limit"] == lim)
res["d_ls_vs_naive"] = d_ok
print("(d) LS vs naive:", d_ok, "/ 15")

# ---------------------------------------------------------------- (e)
mx_l = 0.0
for case in range(6):
    G, g = 4, 5
    Sigma, info = bc.lh_sigma(G, g, 0.5, [0.2], nvis=1)
    n = 120
    X = bc.exact_gram_design(Sigma, n, rng)
    assert np.allclose(X.T @ X, (n - 1) * Sigma, atol=1e-8) and np.allclose(X.mean(0), 0, atol=1e-10)
    th = bc.lh_theta(Sigma.shape[0], info, [0.2], [1.0], 1.0)
    pop = bc.Pop(Sigma, th, n)
    mu = X @ th
    for _ in range(15):
        k = int(rng.integers(0, 9))
        T = sorted(rng.choice(Sigma.shape[0], k, replace=False).tolist())
        if k:
            P = X[:, T] @ np.linalg.solve(X[:, T].T @ X[:, T], X[:, T].T)
            direct = float(mu @ mu - mu @ P @ mu)
        else:
            direct = float(mu @ mu)
        mx_l = max(mx_l, abs(direct - pop.lam(T)))
res["e_pop_lambda_max_abs_diff"] = mx_l
print("(e) Lambda: pop formula vs direct projection, max abs diff:", mx_l)

# block-table helper vs brute force minimiser / VIS / NL on a tiny LH
Sigma, info = bc.lh_sigma(4, 3, 0.5, [0.2], nvis=1)
th = bc.lh_theta(12, info, [0.2], [1.0], 1.0)
pop = bc.Pop(Sigma, th, 500)
blocks = [list(g) for g in info["groups"]]
Us = pop.block_minimisers(blocks)
vis, _ = pop.vis_margin(blocks, Us)
nl, _ = pop.nl_leak(blocks, Us)
# brute
vis_b, nl_b = np.inf, 0.0
for b, C in enumerate(blocks):
    for k in range(len(C) + 1):
        for U in itertools.combinations(C, k):
            if not set(Us[b]) <= set(U):
                gU = pop.lam(U) - pop.lam(tuple(sorted(set(U) | set(Us[b]))))
                v = 1.0 + pop.lam(U) / (pop.n - 1)
                vis_b = min(vis_b, gU / (v * math.log(pop.n)))
            if set(Us[b]) <= set(U):
                for l in C:
                    if l not in U and l not in Us[b]:
                        d2 = pop.lam(U) - pop.lam(tuple(sorted(set(U) | {l})))
                        nl_b = max(nl_b, d2 / math.log(pop.n))
res["e_vis_diff"] = abs(vis - vis_b)
res["e_nl_diff"] = abs(nl - nl_b)
res["e_Ustar"] = [list(u) for u in Us]
print("(e') VIS/NL helper vs brute: ", abs(vis - vis_b), abs(nl - nl_b), " U*=", Us)

# SEP exhaustive vs brute on tiny case
V = [j for g in info["signal_groups"] for j in g]
r = bc.sep_and_decrement(pop, V)
zb, db = 0.0, np.inf
S0 = pop.S0
for k in range(len(V) + 1):
    for S in itertools.combinations(V, k):
        for l in range(12):
            if l not in V:
                zb = max(zb, pop.lam(S) - pop.lam(tuple(sorted(S + (l,)))))
        miss = [j for j in S0 if j not in S]
        if miss:
            db = min(db, max(pop.lam(S) - pop.lam(tuple(sorted(S + (j,)))) for j in miss))
res["e_sep_diff"] = abs(r["zeta"] - zb)
res["e_dec_diff"] = abs(r["dec"] - db)
print("(e'') SEP/decrement sweep vs brute:", abs(r["zeta"] - zb), abs(r["dec"] - db), "dec=", r["dec"], "zeta=", r["zeta"])

json.dump(res, open("E1_results.json", "w"), indent=1)
