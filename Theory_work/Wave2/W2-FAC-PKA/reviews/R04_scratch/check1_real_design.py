"""R04: real centred standardized exact-CS X, direct linear algebra vs closed forms; identities; brute LS0 path."""
import sys; sys.dont_write_bytecode = True
import math, json, itertools, numpy as np
from fastcs import Model, scan
out = {}
def design(n, p, rng):
    C = np.eye(n) - 1 / n
    Z = C @ rng.standard_normal((n, p))
    Qm, _ = np.linalg.qr(Z)                       # orthonormal, orthogonal to 1
    Sig = .5 * np.eye(p) + .5
    w, V = np.linalg.eigh(Sig)
    X = math.sqrt(n - 1) * Qm @ (V * np.sqrt(w)) @ V.T
    return X, Sig, C
def direct_F(X, y, U, n, p, K):
    from scipy.special import gammaln
    k = len(U); h = n - 1
    lw = -math.log(2) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    if k == 0:
        return lw - (.01 + n / 2) * math.log(.02 + y @ y)
    XU = X[:, list(U)]; G = XU.T @ XU; z = XU.T @ y; H = (n + 1) * G + np.eye(k)
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    return lw - .5 * (np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]) - (.01 + n / 2) * math.log(.02 + Q)
rng = np.random.default_rng(404)
errs = dict(Fclosed=0., zrep=0., s2rep=0., Lk=0., del_id=0., swap_id=0., QRSS_viol=0, Qpos_viol=0)
for trial in range(6):
    n, p = (30, 20) if trial < 3 else (60, 44)
    s0 = 1 + trial % 2
    X, Sig, C = design(n, p, rng)
    assert np.allclose(X.T @ X, (n - 1) * Sig) and np.allclose(X.mean(0), 0)
    theta = np.zeros(p); theta[:s0] = 1
    eps = rng.standard_normal(n); e = C @ eps
    Y = X @ theta + e; s2 = Y @ Y / (n - 1); y = Y / math.sqrt(s2); h = n - 1
    g = X.T @ e / math.sqrt(h); PX = X @ np.linalg.solve(X.T @ X, X.T); r = e @ e - e @ PX @ e
    gSg = g @ np.linalg.solve(Sig, g)
    s2rep = (h * theta @ Sig @ theta + 2 * math.sqrt(h) * theta @ g + gSg + r) / h
    errs['s2rep'] = max(errs['s2rep'], abs(s2rep - s2) / s2)
    gSg2 = 2 * (g @ g - g.sum() ** 2 / (p + 1)); errs['s2rep'] = max(errs['s2rep'], abs(gSg2 - gSg) / gSg)
    z = X.T @ y; zrep = (h * Sig @ theta + math.sqrt(h) * g) / math.sqrt(s2)
    errs['zrep'] = max(errs['zrep'], np.abs(z - zrep).max() / np.abs(z).max())
    m = Model(n, p, s0, np.random.default_rng(0)); m.b = 0.0; m.u = z.copy(); m.d = math.sqrt(h / 2 / s2); m.sd = math.sqrt(s2)
    K = n // 2; al, be = m.al, m.be
    for _ in range(40):
        k = int(rng.integers(1, K + 1)); U = np.sort(rng.choice(p, k, replace=False))
        Fd = direct_F(X, y, U, n, p, K); Fc, Qc = m.F(k, z[U].sum(), (z[U] ** 2).sum())
        errs['Fclosed'] = max(errs['Fclosed'], abs(Fd - float(Fc)) / abs(Fd))
        G = X[:, U].T @ X[:, U]; H = (n + 1) * G + np.eye(k)
        Lk = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
        errs['Lk'] = max(errs['Lk'], abs(Lk - m.Lk[k]))
        gam = be / (al + k * be); cT = gam * z[U].sum(); t = z - cT
        quad = lambda W: (np.sum(z[W] ** 2) - be / (al + len(W) * be) * np.sum(z[W]) ** 2) / al
        j = U[0]; Wd = U[1:]
        gm1 = be / (al + (k - 1) * be)
        errs['del_id'] = max(errs['del_id'], abs((quad(Wd) - quad(U)) - (-(1 + gm1) * t[j] ** 2 / al)) / (abs(quad(U)) + 1e-300))
        outs = np.setdiff1d(np.arange(p), U); l = outs[0]; Ws = np.r_[U[1:], l]
        errs['swap_id'] = max(errs['swap_id'], abs((quad(Ws) - quad(U)) - (t[l] ** 2 - t[j] ** 2 - gam * (t[l] - t[j]) ** 2) / al) / (abs(quad(U)) + 1e-300))
        Qd = y @ y - n * quad(U)
        if Qd <= 0: errs['Qpos_viol'] += 1
        if set(range(s0)) <= set(U):
            PU = X[:, U] @ np.linalg.solve(G, X[:, U].T); RSS = Y @ Y - Y @ PU @ Y
            diff = Qd - RSS / s2
            if not (-1e-8 <= diff <= 1 + 2 / (n - 1) + 1e-8): errs['QRSS_viol'] += 1
out['identity_errors'] = errs
# brute-force production LS0 path on real X vs fast path (singleton start)
paths = []
for trial in range(4):
    n, p = 40, 30; s0 = 1 + trial % 2; K = n // 2
    X, Sig, C = design(n, p, rng)
    theta = np.zeros(p); theta[:s0] = 1; e = C @ rng.standard_normal(n); Y = X @ theta + e
    y = Y / math.sqrt(Y @ Y / (n - 1)); z = X.T @ y
    # exact singleton start by brute force over prefix sizes of top |z| (and confirm against random subsets)
    Fs = lambda U: direct_F(X, y, U, n, p, K)
    # start target gamma0: log w(|S|)+sum log BF_j; BF_j = m({j})/m(empty)
    from scipy.special import gammaln
    lw = lambda k: -math.log(2) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lbf = np.array([Fs([j]) - lw(1) - (Fs([]) - lw(0)) for j in range(p)])
    order = np.argsort(-lbf); vals = [lw(k) + lbf[order[:k]].sum() for k in range(K + 1)]
    kb = int(np.argmax(vals)); start = sorted(order[:kb].tolist())
    startK = (kb == K)
    topz = set(start) == set(np.argsort(-z ** 2)[:kb].tolist())
    # brute path, production rules
    T = list(start); centres = [tuple(T)]
    while True:
        FT = Fs(T); best = None
        nb = []
        for j in range(p):
            if j in T: nb.append(sorted(set(T) - {j}))
            elif len(T) < K: nb.append(sorted(T + [j]))
        for j in T:
            for l in range(p):
                if l not in T: nb.append(sorted((set(T) - {j}) | {l}))
        vals = [(Fs(W), W) for W in nb]
        bv = max(v for v, _ in vals)
        if not bv > FT: break
        T = min(W for v, W in vals if v == bv); centres.append(tuple(T))
        if len(centres) > 400: break
    # fast path from same z
    m = Model(n, p, s0, np.random.default_rng(0)); m.b = 0.0; m.u = z.copy(); m.d = math.sqrt((n - 1) / 2) / math.sqrt(Y @ Y / (n - 1))
    inT = np.zeros(p, bool); inT[start] = True; fc = [tuple(start)]
    while True:
        r = scan(m, inT); best = max(r['del'], r['add'], r['swap'])
        if not best > r['FT']: break
        if best == r['swap']: j, l = r['swap_arg']; inT[j] = False; inT[l] = True
        elif best == r['del']: inT[r['del_arg']] = False
        else: inT[r['add_arg']] = True
        fc.append(tuple(np.flatnonzero(inT).tolist()))
    paths.append(dict(s0=s0, start=kb, K=K, startK=startK, topz=topz, brute_len=len(centres) - 1, fast_len=len(fc) - 1, identical=[tuple(c) for c in centres] == fc,
                      final_truth=set(centres[-1]) == set(range(s0))))
out['paths'] = paths
print(json.dumps(out, indent=1, default=float))
json.dump(out, open('check1_out.json', 'w'), indent=1, default=float)
