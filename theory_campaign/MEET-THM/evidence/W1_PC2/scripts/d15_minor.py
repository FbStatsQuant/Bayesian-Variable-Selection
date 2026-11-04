"""PC2: check of R1_C D15-TV first clause: the full production round minorises q_phi by 1/M_phi
(M_phi = max q_phi/pi0), with no 1/m factor, for every realised step order; and the D15-KL mixture form.
Exact transition matrices of the elementary steps (M §6.5) on the actual target, p = 4, n = 20 (K = 4, B = 2, m = 8),
all 8! = 40320 orders, phi in {0.3, 1}.  Then nu K^L = (1-(1-e)^L) pi + (1-e)^L nu_L with nu_L a probability
(checked: residual nonnegative).  Seeds fixed; ~1 minute."""
import itertools
import math
import numpy as np
from bvs_common import suff_from_data, method_sizes, coded_partition, d_table, log_prior_w

rng = np.random.default_rng(15)
p, n = 4, 20
S = np.array([[1, .5, .1, 0], [.5, 1, 0, .2], [.1, 0, 1, .4], [0, .2, .4, 1]])
X = rng.standard_normal((n, p)) @ np.linalg.cholesky(S).T
y = X @ np.array([0.8, 0, -0.5, 0]) + rng.standard_normal(n)
G, z, Y, n = suff_from_data(X, y)
K, B = method_sizes(n, p)
blocks = coded_partition(G, B)
models, d, lbf = d_table(G, z, Y, n, blocks, K)
lp = np.array([log_prior_w(p, len(Sm)) for Sm in models])
lg0 = lp + lbf - d
pi0 = np.exp(lg0 - np.logaddexp.reduce(lg0))
idx = {Sm: i for i, Sm in enumerate(models)}
M = len(models)
sets = [set(Sm) for Sm in models]
dg = np.sqrt(np.diag(G))
Rm = G / np.outer(dg, dg)
rn = math.sqrt(2 * math.log(p) / n)
Nb = {j: set() for j in range(p)}
for j in range(p):
    a = np.abs(Rm[j]).copy()
    a[j] = -1
    order = sorted([l for l in range(p) if l != j], key=lambda l: (-a[l], l))
    part = [l for l in order if a[l] > rn][:B]
    if order[0] not in part:
        part = [order[0]] + part[:B - 1]
    for l in part:
        Nb[j].add(l)
        Nb[l].add(j)
print(f"p={p} n={n} K={K} B={B} blocks={blocks} graph={ {j: sorted(v) for j, v in Nb.items()} }")


def kernels(phi):
    lq = lg0 + phi * d
    q = np.exp(lq - np.logaddexp.reduce(lq))
    Ks = []
    for j in range(p):                      # Gibbs j
        Kj = np.zeros((M, M))
        for i, s in enumerate(sets):
            on, off = tuple(sorted(s | {j})), tuple(sorted(s - {j}))
            if on in idx:
                pr = q[idx[on]] / (q[idx[on]] + q[idx[off]])
                Kj[i, idx[on]] += pr
                Kj[i, idx[off]] += 1 - pr
            else:
                Kj[i, idx[off]] += 1
        Ks.append(Kj)
    Ku = np.zeros((M, M))                    # uniform swap
    for i, s in enumerate(sets):
        if len(s) in (0, p):
            Ku[i, i] = 1
            continue
        out = [l for l in range(p) if l not in s]
        for j in s:
            for l in out:
                t = idx[tuple(sorted((s - {j}) | {l}))]
                a = min(1, q[t] / q[i]) / (len(s) * len(out))
                Ku[i, t] += a
                Ku[i, i] += 1 / (len(s) * len(out)) - a
    Ks.append(Ku)
    Kn = np.zeros((M, M))                    # neighbour swap
    for i, s in enumerate(sets):
        if not s:
            Kn[i, i] = 1
            continue
        for j in s:
            cand = Nb[j] - s
            if not cand:
                Kn[i, i] += 1 / len(s)
                continue
            for l in cand:
                s2 = (s - {j}) | {l}
                t = idx[tuple(sorted(s2))]
                prop = 1 / (len(s) * len(cand))
                a = min(1, q[t] / q[i] * len(cand) / len(Nb[l] - s2))
                Kn[i, t] += prop * a
                Kn[i, i] += prop * (1 - a)
    Ks += [Kn] * B
    Ki = np.zeros((M, M))                    # independence
    for i in range(M):
        for t in range(M):
            a = min(1, math.exp(phi * (d[t] - d[i])))
            Ki[i, t] += pi0[t] * a
            Ki[i, i] += pi0[t] * (1 - a)
    Ks.append(Ki)
    return Ks, q


for phi in (0.3, 1.0):
    Ks, q = kernels(phi)
    for Kk in Ks:
        assert np.allclose(q @ Kk, q)
    Mphi = float((q / pi0).max())
    worst = math.inf
    Kavg = np.zeros((M, M))
    m = len(Ks)
    for order in itertools.permutations(range(m)):
        P = np.eye(M)
        for s in order:
            P = P @ Ks[s]
        Kavg += P
        worst = min(worst, float((P / q[None, :]).min()))
    Kavg /= math.factorial(m)
    eps = 1 / Mphi
    print(f"phi={phi}: 1/M_phi = {eps:.5f}; min over all {math.factorial(m)} orders of min_xy K(x,y)/q(y) = {worst:.5f}"
          f" -> minorisation {'HOLDS' if worst >= eps - 1e-12 else 'FAILS'}; (1/(m M) would be {eps / m:.5f})")
    if phi == 1.0:
        Rk = (Kavg - eps * np.outer(np.ones(M), q)) / (1 - eps)
        print(f"  residual kernel min entry {Rk.min():.3e} (>= 0 means K = e pi + (1-e) R)")
        nu = np.zeros(M)
        nu[0] = 1
        lam = nu.copy()
        for L in range(1, 9):
            lam = lam @ Kavg
            tv = 0.5 * np.abs(lam - q).sum()
            kl1 = float((q * np.log(q / lam)).sum())
            kl2 = float((lam * np.log(np.maximum(lam, 1e-300) / q)).sum())
            qq = (1 - eps) ** L
            ok = tv <= qq + 1e-12 and kl1 <= -math.log(1 - qq) + 1e-12 and kl2 <= qq * math.log(1 / q.min()) + 1e-12
            print(f"  L={L}: TV={tv:.3e} <= q^L={qq:.3e}; KL(pi||lam)={kl1:.3e} <= {-math.log(1 - qq):.3e};"
                  f" KL(lam||pi)={kl2:.3e} <= {qq * math.log(1 / q.min()):.3e}: {'ok' if ok else 'VIOLATION'}")
