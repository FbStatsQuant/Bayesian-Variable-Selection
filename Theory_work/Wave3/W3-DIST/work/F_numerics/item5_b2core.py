"""Item 5: B2-core.  p=200, q in {2,4}, n in {200,2000}, laws: Gaussian AR(0.9) and independent Rademacher.
For each sample compute  min over q-sparse u and a of  R(a,u) = [n^-1 sum_i (a+u'z_i)^2] / [a^2 + Var(u'z)]  (z standardised, Var(u'z)=u'Sigma u).
For a fixed support S the minimum over (a,u_S) is EXACT: lambda_min of the pencil (N_S, D_S),  N_S=[[1,m_S'],[m_S,M_SS]] (m = sample mean of z, M = n^-1 sum z z'),
D_S = blockdiag(1, Sigma_SS).   q=2: all C(200,2)=19900 supports enumerated (exact).   q=4: random restarts + best-swap hill climbing over supports
(an UPPER bound on the true minimum, so the frequency below 1/2 is a LOWER bound).
usage: python3 -B item5_b2core.py NWORK R NRESTART      DRAFT (by this seat, unchecked)"""
import sys, time, itertools, pickle
from multiprocessing import Pool
from fcommon import *
P = 200

def make_law(law):
    if law == "AR0.9":
        Sig = ar_sigma(P, 0.9)
        return Sig, np.linalg.cholesky(Sig)
    return np.eye(P), np.eye(P)

def sample_z(law, n, L, rng):
    if law == "AR0.9":
        return rng.standard_normal((n, P)) @ L.T
    return rng.choice([-1.0, 1.0], size=(n, P))

def ratio_batch(idx, m, M, Sig):
    """idx (b,q) -> min over (a,u) on support of R  (b,)"""
    b, q = idx.shape
    N = np.empty((b, q + 1, q + 1))
    N[:, 0, 0] = 1.0
    N[:, 0, 1:] = m[idx]; N[:, 1:, 0] = m[idx]
    N[:, 1:, 1:] = M[idx[:, :, None], idx[:, None, :]]
    Ss = Sig[idx[:, :, None], idx[:, None, :]]
    L = np.linalg.cholesky(Ss)
    Li = np.linalg.inv(L)
    T = np.zeros((b, q + 1, q + 1)); T[:, 0, 0] = 1.0; T[:, 1:, 1:] = Li
    A = T @ N @ np.transpose(T, (0, 2, 1))
    return np.linalg.eigvalsh(A)[:, 0]

def one(args):
    law, n, q, rep, nrest = args
    rng = np.random.default_rng([20261116, 5, n, q, 0 if law == "AR0.9" else 1, rep])
    Sig, L = make_law(law)
    Z = sample_z(law, n, L, rng)
    m = Z.mean(0); M = Z.T @ Z / n
    if q == 2:
        pairs = np.array(list(itertools.combinations(range(P), 2)))
        r = ratio_batch(pairs, m, M, Sig)
        k = int(np.argmin(r))
        return dict(law=law, n=n, q=q, rep=rep, minratio=float(r[k]), S=pairs[k], exact=True, n_below_half_supports=int((r < 0.5).sum()))
    best = (np.inf, None)
    for s in range(nrest):
        if s == 0:
            S = np.argsort(-np.abs(m))[:q]
        elif s == 1:
            j = int(rng.integers(0, P - q)); S = np.arange(j, j + q)
        else:
            S = rng.choice(P, size=q, replace=False)
        S = np.array(S)
        cur = ratio_batch(S[None, :], m, M, Sig)[0]
        for it in range(30):
            cand = []
            for k in range(q):
                others = np.setdiff1d(np.arange(P), S)
                C_ = np.repeat(S[None, :], len(others), 0); C_[:, k] = others
                cand.append(C_)
            cand = np.vstack(cand)
            rv = ratio_batch(cand, m, M, Sig)
            j = int(np.argmin(rv))
            if rv[j] < cur - 1e-12:
                cur, S = rv[j], cand[j].copy()
            else:
                break
        if cur < best[0]:
            best = (cur, S.copy())
    return dict(law=law, n=n, q=q, rep=rep, minratio=float(best[0]), S=best[1], exact=False, n_below_half_supports=-1)

if __name__ == "__main__":
    nw, R, nrest = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tasks = [(law, n, q, r, nrest) for q in (2, 4) for n in (200, 2000) for law in ("AR0.9", "Rademacher") for r in range(R)]
    t0 = time.time()
    with Pool(nw) as pool:
        res = pool.map(one, tasks, chunksize=2)
    pickle.dump(res, open("out/item5.pkl", "wb"))
    print("done", time.time() - t0)
