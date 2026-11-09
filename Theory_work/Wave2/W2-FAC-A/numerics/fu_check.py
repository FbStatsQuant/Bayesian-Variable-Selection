"""fu_check.py -- falsification numerics for Lemma U (lemmas/L1_uniform_add.md).
F-U1: exact decomposition identity  Z = [sqrt(psi) Xi + (lt/sqrt(1+s)) W]/sqrt(psi + lt^2/(1+s))  (to 1e-10),
      for random class members (singleton groups CS, block CS, random block-diagonal Psi with random loadings).
F-U2: the deterministic inequality (U2) |Z| <= |Xi| + (|lt|/sqrt psi)(|xi0|/(1+s_T) + sqrt(sum_{hit} Q_g) sqrt(s_T)/(1+s_T))
      on random, one-sided (top-m by zeta / by g) and greedy-adversarial sets.
F-U3: the probabilistic envelope sup_{T,l}|Z| vs sqrt(2 log(p 2^gbar)) + kappa sqrt(2 log(e gbar p/|T|)) (+ slack) at large p.
F-U4: perturbation: R-hat from iid rows vs Sigma: max over sampled (T,l) of |Z^Rhat - Z^Sigma(coupled)| vs C delta sqrt(p).
usage: py -3.13 fu_check.py  -> prints and writes FU_out.txt"""
import itertools, math, sys
import numpy as np


def make_class(kind, G, gs, rng):
    p = G * gs
    groups = [list(range(i * gs, (i + 1) * gs)) for i in range(G)]
    if kind == "CS":
        a = 0.3
        lam = np.full(p, math.sqrt(a)); Psi = (1 - a) * np.eye(p)
    elif kind == "BCS":
        rb, rw = 0.3, 0.7
        lam = np.full(p, math.sqrt(rb)); Psi = (rw - rb) * np.kron(np.eye(G), np.ones((gs, gs))) + (1 - rw) * np.eye(p)
    else:  # random loadings and random PD blocks, then rescale to a correlation matrix
        lam = rng.uniform(0.3, 0.8, size=p) * rng.choice([-1, 1], size=p)
        Psi = np.zeros((p, p))
        for g in groups:
            A = rng.standard_normal((len(g), len(g)))
            B = A @ A.T / len(g) + 0.3 * np.eye(len(g))
            Psi[np.ix_(g, g)] = B
        d = np.sqrt(lam ** 2 + np.diag(Psi))
        lam = lam / d; Psi = Psi / np.outer(d, d)
    return lam, Psi, groups


def innov(Sig, gvec, T, l):
    T = list(T)
    if not T:
        return gvec[l] / math.sqrt(Sig[l, l])
    c = np.linalg.solve(Sig[np.ix_(T, T)], Sig[T, l])
    v = Sig[l, l] - Sig[l, T] @ c
    return (gvec[l] - c @ gvec[T]) / math.sqrt(v)


def decomp(lam, Psi, gid, groups, xi0, zeta, T, l):
    T = list(T)
    U = [j for j in T if gid[j] == gid[l]]
    if U:
        cU = np.linalg.solve(Psi[np.ix_(U, U)], Psi[U, l])
        psi = Psi[l, l] - Psi[l, U] @ cU
        Xi = (zeta[l] - cU @ zeta[U]) / math.sqrt(psi)
        lt = lam[l] - cU @ lam[U]
    else:
        psi = Psi[l, l]; Xi = zeta[l] / math.sqrt(psi); lt = lam[l]
    if T:
        PinvL = np.linalg.solve(Psi[np.ix_(T, T)], lam[T])
        s = float(lam[T] @ PinvL)
        W = (xi0 - PinvL @ zeta[T]) / math.sqrt(1 + s)
    else:
        s, W = 0.0, xi0
    Z = (math.sqrt(psi) * Xi + lt / math.sqrt(1 + s) * W) / math.sqrt(psi + lt ** 2 / (1 + s))
    # U2 bound
    hit = sorted({gid[j] for j in T})
    Q = 0.0
    for h in hit:
        g = groups[h]
        Q += float(zeta[g] @ np.linalg.solve(Psi[np.ix_(g, g)], zeta[g]))
    bound = abs(Xi) + abs(lt) / math.sqrt(psi) * (abs(xi0) / (1 + s) + math.sqrt(Q) * math.sqrt(s) / (1 + s))
    return Z, bound, Xi


def kappa_cmin(lam, Psi, groups):
    cmin, kap, kp = np.inf, 0.0, 0.0
    for g in groups:
        for r in range(1, len(g) + 1):
            for U in itertools.combinations(g, r):
                U = list(U); cmin = min(cmin, float(lam[U] @ np.linalg.solve(Psi[np.ix_(U, U)], lam[U])))
        for l in g:
            rest = [j for j in g if j != l]
            for r in range(0, len(rest) + 1):
                for U in itertools.combinations(rest, r):
                    U = list(U)
                    if U:
                        c = np.linalg.solve(Psi[np.ix_(U, U)], Psi[U, l]); lt = lam[l] - c @ lam[U]; ps = Psi[l, l] - Psi[l, U] @ c
                    else:
                        lt, ps = lam[l], Psi[l, l]
                    kp = max(kp, abs(lt) / math.sqrt(ps))
    return kp / math.sqrt(cmin), cmin, kp


def main():
    out = []
    rng = np.random.default_rng(2026)
    # F-U1, F-U2
    maxerr, viol, ntest = 0.0, 0, 0
    for kind, G, gs in (("CS", 40, 1), ("BCS", 10, 5), ("RND", 12, 3), ("RND", 8, 4)):
        for rep in range(20):
            lam, Psi, groups = make_class(kind, G, gs, rng)
            p = len(lam); gid = np.repeat(np.arange(G), gs)
            Sig = np.outer(lam, lam) + Psi
            xi0 = rng.standard_normal(); zeta = np.linalg.cholesky(Psi) @ rng.standard_normal(p)
            gvec = lam * xi0 + zeta
            sets = []
            for _ in range(30):
                m = int(rng.integers(0, p)); sets.append(sorted(rng.choice(p, size=m, replace=False).tolist()))
            order = np.argsort(-zeta)
            for m in (1, 2, 4, 8, p // 2, p - 2):
                sets.append(sorted(order[:m].tolist())); sets.append(sorted(np.argsort(-gvec)[:m].tolist()))
            # greedy adversarial: grow T to maximise |Z_{T,l*}| for l* = argmin zeta
            lstar = int(np.argmin(zeta)); T = []
            for _ in range(min(p - 1, 25)):
                best, bj = -1, None
                for j in range(p):
                    if j == lstar or j in T: continue
                    z = abs(innov(Sig, gvec, T + [j], lstar))
                    if z > best: best, bj = z, j
                T = T + [bj]; sets.append(sorted(T))
            for T in sets:
                outs = [j for j in range(p) if j not in T]
                for l in outs[:: max(1, len(outs) // 8)] + ([lstar] if lstar not in T else []):
                    z1 = innov(Sig, gvec, T, l)
                    z2, b, _ = decomp(lam, Psi, gid, groups, xi0, zeta, T, l)
                    maxerr = max(maxerr, abs(z1 - z2)); ntest += 1
                    if abs(z1) > b + 1e-9: viol += 1
    out.append("F-U1 exact decomposition: tests %d, max |Z_direct - Z_formula| = %.3e" % (ntest, maxerr))
    out.append("F-U2 deterministic bound (U2): violations %d / %d" % (viol, ntest))
    # F-U3 envelope at larger p: CS and BCS, sup over one-sided / greedy sets
    for kind, G, gs in (("CS", 2000, 1), ("BCS", 400, 5)):
        lam, Psi, groups = make_class(kind, G, gs, rng)
        p = len(lam); gid = np.repeat(np.arange(G), gs)
        kap, cmin, kp = kappa_cmin(lam[:2 * gs] if gs > 1 else lam[:2], Psi[:2 * gs, :2 * gs] if gs > 1 else Psi[:2, :2], [list(range(gs)), list(range(gs, 2 * gs))])
        worst = 0.0
        for rep in range(10):
            xi0 = rng.standard_normal()
            Lc = np.linalg.cholesky(Psi[:gs, :gs])
            zeta = np.concatenate([Lc @ rng.standard_normal(gs) for _ in range(G)])
            order = np.argsort(-zeta); lstar = int(np.argmin(zeta))
            for m in (1, 3, 10, 30, 100, 300, p // 4, p // 2):
                T = [int(j) for j in order[:m]]
                z, b, Xi = decomp(lam, Psi, gid, groups, xi0, zeta, T, lstar)
                env = math.sqrt(2 * math.log(p * 2 ** gs)) + kap * math.sqrt(2 * math.log(math.e * gs * p / m))
                worst = max(worst, abs(z) / env)
        out.append("F-U3 %s p=%d kappa=%.4f: max over one-sided sets of |Z|/envelope = %.3f (envelope w/o loglog slack)" % (kind, p, kap, worst))
    # F-U4 perturbation (iid rows)
    for kind, G, gs, n in (("CS", 30, 1, 20000), ("BCS", 8, 5, 20000)):
        lam, Psi, groups = make_class(kind, G, gs, rng)
        p = len(lam); Sig = np.outer(lam, lam) + Psi
        X = rng.standard_normal((n, p)) @ np.linalg.cholesky(Sig).T
        X -= X.mean(0); X /= np.sqrt((X ** 2).sum(0) / (n - 1))
        R = X.T @ X / (n - 1)
        delta = np.linalg.norm(R - Sig, 2)
        w, V = np.linalg.eigh(R); Rmh = (V / np.sqrt(w)) @ V.T
        w2, V2 = np.linalg.eigh(Sig); Sh = (V2 * np.sqrt(w2)) @ V2.T
        worst = 0.0
        for rep in range(5):
            gh = np.linalg.cholesky(R) @ rng.standard_normal(p)
            gam = Sh @ Rmh @ gh
            for _ in range(200):
                m = int(rng.integers(0, p)); T = sorted(rng.choice(p, size=m, replace=False).tolist())
                outs = [j for j in range(p) if j not in T]
                l = outs[int(rng.integers(0, len(outs)))]
                worst = max(worst, abs(innov(R, gh, T, l) - innov(Sig, gam, T, l)))
        out.append("F-U4 %s p=%d n=%d: ||R-Sigma||op=%.4f, max|Z^R - Z^Sigma| = %.4f, ratio to delta*sqrt(p) = %.3f" % (kind, p, n, delta, worst, worst / (delta * math.sqrt(p))))
    txt = "\n".join(out)
    print(txt)
    with open("FU_out.txt", "w") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    main()
