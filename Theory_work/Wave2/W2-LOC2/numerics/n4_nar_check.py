r"""n4_nar_check.py -- falsification numerics for Lemma CT_d / CD_d (L3_CTd.md) and the key Lemma NA-R (L2_NAR.md).

Part 1 (CT_d): 2-D grids, Sigma = exp(-|dx|_2/phi); t* solves S(t) = alpha/2 with
  S(t) = K sum_{m>=1} (2m+3)^d e^{-(a-t)m} (1 - e^{-t(m+1)});
check |(A^{-1})_ij| <= (2/alpha) e^{-t* d_ij} for A = Sigma and for random principal submatrices; report the worst ratio.
Also the regression l1 bound sup_A ||beta_A(l)||_1 <= L0 := (2/c) sum_m (2m+3)^d e^{-t1 m} (t1 = t*(c, K, a)).
Part 2 (NA-R): raw W ~ N(0, Sigma) rows, eps ~ N(0, I); for T in the lattice [S0, Q] (random T + T on a greedy path) and
all l not in T: Z (sample), Z_pop = (C e_T)'eps/||C e_T|| (population residual), the exact identity
(I-P_T)x_l parallel to (I-P_T)C e_T, the NA-R decomposition (reference + atoms) and its bound
  |Z_pop| <= (||C r||/||C e||) * sup_{frame} + ||lambda||_1 * max_a |a'C eps| / ||C e||.
Designs: G2E (2-D exp, phi = 1.2; reference = residual on window T cap B(l, r)), EBM (compound symmetry rho = .5 blocks,
reference frame (F_G, xi_l), atoms xi_v).  Output: n4_out.txt."""
import math, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(np.random.SeedSequence([20261111, 4]))
out = open(os.path.join(HERE, "n4_out.txt"), "w")


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.write(s + "\n"); out.flush()


def tstar(alpha, K, a, d, M=4000):
    m = np.arange(1, M + 1)
    def S(t):
        return K * np.sum((2 * m + 3.0) ** d * np.exp(-(a - t) * m) * (1 - np.exp(-t * (m + 1))))
    lo, hi = 0.0, a * (1 - 1e-9)
    for _ in range(200):
        mid = (lo + hi) / 2
        if S(mid) <= alpha / 2: lo = mid
        else: hi = mid
    return lo


def grid(m):
    i = np.arange(m * m)
    return np.stack([i // m, i % m], 1).astype(float)

# ---------------- Part 1
pr("== Part 1: CT_d on 2-D grids ==")
for phi in (0.8, 1.2, 2.0):
    m = 22
    xy = grid(m)
    D2 = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(-1))
    S = np.exp(-D2 / phi)
    ev = np.linalg.eigvalsh(S)
    c, a, K = ev.min(), 1 / phi, 1.0
    t = tstar(c, K, a, 2)
    worst = 0.0
    for rep in range(30):
        if rep == 0:
            idx = np.arange(m * m)
        else:
            idx = np.sort(rng.choice(m * m, size=rng.integers(20, m * m), replace=False))
        A = S[np.ix_(idx, idx)]
        Ai = np.linalg.inv(A)
        d = D2[np.ix_(idx, idx)]
        bound = (2 / c) * np.exp(-t * d)
        worst = max(worst, float((np.abs(Ai) / bound).max()))
    t1 = t
    mm = np.arange(1, 4001)
    L0 = (2 / c) * np.sum((2 * mm + 3.0) ** 2 * np.exp(-t1 * mm))
    l1max = 0.0
    for rep in range(200):
        l = int(rng.integers(m * m))
        others = np.setdiff1d(np.arange(m * m), [l])
        A = np.sort(rng.choice(others, size=rng.integers(1, 150), replace=False))
        beta = np.linalg.solve(S[np.ix_(A, A)], S[A, l])
        l1max = max(l1max, float(np.abs(beta).sum()))
    pr("phi=%.1f lambda_min=%.4f a=%.3f t*=%.4g worst |Ainv|/bound=%.3g (<=1 required)  max||beta||_1=%.3f  L0=%.3g"
       % (phi, c, a, t, worst, l1max, L0))

# ---------------- Part 2
pr("== Part 2: NA-R components ==")


def run(design, n, reps=3):
    if design == "G2E":
        m = 20; p = m * m; xy = grid(m)
        D2 = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(-1))
        Dinf = np.abs(xy[:, None] - xy[None]).max(-1)
        S = np.exp(-D2 / 1.2)
        S0 = [4 * m + 4, 10 * m + 14, 15 * m + 5]
        dS0 = Dinf[:, S0].min(1)
        Qx = [v for v in np.argsort(dS0, kind="stable") if v not in S0][:80]
        Lc = np.linalg.cholesky(S)
    else:
        p, g, rho = 400, int(math.ceil(3 * math.log(n))), 0.5
        gid = np.arange(p) // g
        S = np.where(gid[:, None] == gid[None], rho, 0.0); np.fill_diagonal(S, 1.0)
        S0 = [g * 1 + g // 2, g * 6 + g // 2, g * 11 + g // 2]
        Qx = [v for v in range(p) if gid[v] in {gid[j] for j in S0} and v not in S0]
    q = len(Qx) + 3
    worst = dict(onemcos=0, zdiff=0, maxZ2=0, maxZpop2=0, bound_ok=True, bound_slack=1e9, ratio=0)
    for rep in range(reps):
        if design == "G2E":
            W = rng.standard_normal((n, p)) @ Lc.T
        else:
            F = rng.standard_normal((n, p // g + 1)); xi = rng.standard_normal((n, p))
            W = math.sqrt(rho) * F[:, gid] + math.sqrt(1 - rho) * xi
        eps = rng.standard_normal(n)
        Ce = eps - eps.mean()
        Wc = W - W.mean(0)
        X = Wc / np.sqrt((Wc ** 2).sum(0) / (n - 1))
        Ts = []
        for k in range(8):
            Ts.append(sorted(S0 + [v for v in Qx if rng.random() < rng.choice([0.2, 0.5, 0.9])]))
        Ts.append(sorted(S0 + list(Qx)))
        Ts.append(sorted(S0))
        for T in Ts:
            T = np.array(T)
            Xt = X[:, T]
            Qm, _ = np.linalg.qr(Xt)
            ls = [l for l in (list(Qx) + list(rng.choice(p, 30))) if l not in set(T.tolist())][:60]
            PtEps = Qm @ (Qm.T @ Ce)
            for l in ls:
                beta = np.linalg.solve(S[np.ix_(T, T)], S[T, l])
                eT = W[:, l] - W[:, T] @ beta
                CeT = eT - eT.mean()
                xl = X[:, l]
                h1 = xl - Qm @ (Qm.T @ xl)
                h2 = CeT - Qm @ (Qm.T @ CeT)
                cosang = abs(h1 @ h2) / np.linalg.norm(h1) / np.linalg.norm(h2)
                Z = h1 @ eps / np.linalg.norm(h1)
                Zp = CeT @ eps / np.linalg.norm(CeT)
                worst["zdiff"] = max(worst["zdiff"], abs(abs(Z) - abs(Zp)))
                worst["onemcos"] = max(worst["onemcos"], 1 - cosang)
                worst["maxZ2"] = max(worst["maxZ2"], Z * Z); worst["maxZpop2"] = max(worst["maxZpop2"], Zp * Zp)
                # NA-R decomposition
                if design == "G2E":
                    xyl = xy[l]
                    r = max(2, int(math.ceil(math.log(math.log(n)))) + 1)
                    win = np.array([v for v in T if np.abs(xy[v] - xyl).max() <= r], dtype=int)
                    if len(win):
                        bw = np.linalg.solve(S[np.ix_(win, win)], S[win, l])
                        ref = W[:, l] - W[:, win] @ bw
                    else:
                        bw = np.zeros(0); ref = W[:, l].copy()
                    lam = beta.copy()
                    pos = {v: i for i, v in enumerate(T)}
                    for i, v in enumerate(win):
                        lam[pos[v]] -= bw[i]
                    atoms = W[:, T]
                    Cref = ref - ref.mean()
                    sup_ref = abs(Cref @ eps) / np.linalg.norm(Cref)
                else:
                    G = gid[l]
                    A = np.array([v for v in T if gid[v] == G], dtype=int)
                    b = math.sqrt(rho)
                    if len(A):
                        bA = beta[[i for i, v in enumerate(T) if gid[v] == G]]
                    else:
                        bA = np.zeros(0)
                    ref = (b - b * bA.sum()) * F[:, G] + math.sqrt(1 - rho) * xi[:, l]
                    lam = bA * math.sqrt(1 - rho)
                    atoms = xi[:, A] if len(A) else np.zeros((n, 0))
                    Cref = ref - ref.mean()
                    Fr = np.stack([F[:, G] - F[:, G].mean(), xi[:, l] - xi[:, l].mean()], 1)
                    Qf, _ = np.linalg.qr(Fr)
                    sup_ref = np.linalg.norm(Qf.T @ eps)
                Ca = atoms - atoms.mean(0)
                amax = np.abs(Ca.T @ eps).max() if Ca.shape[1] else 0.0
                bound = (np.linalg.norm(Cref) * sup_ref + np.abs(lam).sum() * amax) / np.linalg.norm(CeT)
                if abs(Zp) > bound + 1e-8:
                    worst["bound_ok"] = False
                worst["bound_slack"] = min(worst["bound_slack"], bound - abs(Zp))
                worst["ratio"] = max(worst["ratio"], np.linalg.norm(Cref) / np.linalg.norm(CeT))
    pr(design, "n=%d p=%d q=%d" % (n, p, q), "max(1-cos identity)=%.2g max ||Z|-|Zpop||=%.3g (|Q|/sqrt n=%.3g)" % (worst["onemcos"], worst["zdiff"], q / math.sqrt(n)),
       "max Z^2=%.2f max Zpop^2=%.2f 2log p=%.2f" % (worst["maxZ2"], worst["maxZpop2"], 2 * math.log(p)),
       "NA-R bound holds:", worst["bound_ok"], "min slack %.3g" % worst["bound_slack"], "max ||Cr||/||Ce||=%.4f" % worst["ratio"])


for design in ("G2E", "EBM"):
    for n in (3200, 12800):
        run(design, n)
out.close()
