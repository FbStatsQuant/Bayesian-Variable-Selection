"""W2-UNI numerics N3: falsification probe for key lemma U-LOC (one factor + metric-local, NON-block Psi).

Sigma = lam lam^T + Psi, Psi = D^{1/2} R D^{1/2}, D = diag(1 - lam_j^2), R local (AR(1) on a line, or 2-D exponential),
unit diagonal. gamma = lam xi0 + zeta, xi0 ~ N(0,1), zeta ~ N(0, Psi) independent.
Checks, for random and adversarial (greedy) (T, l):
 (a) exact identity  Z^Sigma_{T,l}(gamma) = [sqrt(psi) Xi + lt/sqrt(1+s) W] / sqrt(psi + lt^2/(1+s))   (max abs error)
 (b) deterministic inequality |Z| <= |Xi| + kap'_{l,T} |xi0|/(1+s) + kap'_{l,T} |F_T| sqrt(s)/(1+s)
 (c) observed sup |Xi_{l,T}| vs sqrt(2 log p); observed sup F_T^2 / (2h log(e p/h) + 4 log(h+1)), h = |T| (singleton strata;
     the lemma's union threshold adds 2 log log n, so values <= 1 are expected up to that allowance)
 (d) kappa' (sup over sampled sets) and c_G (singletons: inf s_T/|T| over sampled sets incl. singletons)
Observations only. Run: py -3.13 -B n3_uloc.py > n3_out.txt
"""
import numpy as np

rng = np.random.default_rng(7)


def make(p, kind):
    lam = rng.uniform(0.4, 0.7, p) * rng.choice([-1, 1], p)
    if kind == "ar1":
        idx = np.arange(p)
        R = 0.6 ** np.abs(idx[:, None] - idx[None, :])
    else:
        m = int(round(np.sqrt(p)))
        x = np.array([(i, j) for i in range(m) for j in range(m)], float)[:p]
        x += rng.uniform(-0.2, 0.2, x.shape)
        dd = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1))
        R = 0.7 * np.exp(-dd / 0.8)
        np.fill_diagonal(R, 1.0)
    Dh = np.sqrt(1 - lam ** 2)
    Psi = Dh[:, None] * R * Dh[None, :]
    Sig = np.outer(lam, lam) + Psi
    return lam, Psi, Sig


def pieces(lam, Psi, Sig, g, xi0, zeta, T, l):
    T = np.asarray(T, int)
    if len(T):
        PT = Psi[np.ix_(T, T)]
        cP = np.linalg.solve(PT, Psi[T, l])
        psi = Psi[l, l] - Psi[l, T] @ cP
        Xi = (zeta[l] - cP @ zeta[T]) / np.sqrt(psi)
        lt = lam[l] - cP @ lam[T]
        a = np.linalg.solve(PT, lam[T])
        s = lam[T] @ a
        F = (a @ zeta[T]) / np.sqrt(s)
        W = (xi0 - a @ zeta[T]) / np.sqrt(1 + s)
        ST = Sig[np.ix_(T, T)]
        cS = np.linalg.solve(ST, Sig[T, l])
        Z = (g[l] - cS @ g[T]) / np.sqrt(Sig[l, l] - Sig[l, T] @ cS)
    else:
        psi, Xi, lt, s, F, W = Psi[l, l], zeta[l] / np.sqrt(Psi[l, l]), lam[l], 0.0, 0.0, xi0
        Z = g[l]
    dec = (np.sqrt(psi) * Xi + lt / np.sqrt(1 + s) * W) / np.sqrt(psi + lt ** 2 / (1 + s))
    kap = abs(lt) / np.sqrt(psi)
    env = abs(Xi) + kap * abs(xi0) / (1 + s) + (kap * abs(F) * np.sqrt(s) / (1 + s) if s > 0 else 0.0)
    return Z, dec, env, Xi, F, s, kap


def run(p, kind, reps=3, n_rand=300, n_greedy=6):
    lam, Psi, Sig = make(p, kind)
    Lc = np.linalg.cholesky(Psi)
    out = dict(id_err=0.0, ineq_viol=0, n=0, supXi=0.0, supF=0.0, kap=0.0, cG=np.inf)
    for _ in range(reps):
        xi0 = rng.standard_normal()
        zeta = Lc @ rng.standard_normal(p)
        g = lam * xi0 + zeta
        def rec(T, l):
            Z, dec, env, Xi, F, s, kap = pieces(lam, Psi, Sig, g, xi0, zeta, T, l)
            out["id_err"] = max(out["id_err"], abs(Z - dec))
            out["ineq_viol"] += int(abs(Z) > env + 1e-9)
            out["n"] += 1
            out["supXi"] = max(out["supXi"], abs(Xi))
            if len(T):
                h = len(T)
                out["supF"] = max(out["supF"], F ** 2 / (2 * h * np.log(np.e * p / h) + 4 * np.log(h + 1)))
                out["cG"] = min(out["cG"], s / len(T))
            out["kap"] = max(out["kap"], kap)
            return abs(Z), abs(Xi)
        for _ in range(n_rand):
            l = int(rng.integers(p))
            oth = np.setdiff1d(np.arange(p), [l])
            k = int(rng.integers(0, p))
            T = rng.choice(oth, size=min(k, oth.size), replace=False)
            rec(T, l)
        for j in range(p):  # singletons for c_G
            out["cG"] = min(out["cG"], lam[j] ** 2 / Psi[j, j])
        # greedy adversarial: maximise |Xi_{l,T}| by single flips from a random start
        for _ in range(n_greedy):
            l = int(rng.integers(p))
            oth = list(np.setdiff1d(np.arange(p), [l]))
            T = set(rng.choice(oth, size=p // 3, replace=False).tolist())
            best = rec(sorted(T), l)[1]
            for sweep in range(2):
                for v in rng.permutation(oth)[:120]:
                    T2 = T ^ {int(v)}
                    val = rec(sorted(T2), l)[1]
                    if val > best:
                        best, T = val, T2
    print(f"{kind:5s} p={p:4d}: pairs={out['n']}, identity max err={out['id_err']:.2e}, inequality violations={out['ineq_viol']}, "
          f"sup|Xi|={out['supXi']:.2f} vs sqrt(2logp)={np.sqrt(2*np.log(p)):.2f}, sup F^2/(2h log(ep/h)+4log(h+1))={out['supF']:.3f}, "
          f"kappa'={out['kap']:.3f}, c_G(sampled inf)={out['cG']:.3f}, kappa={out['kap']/np.sqrt(out['cG']):.3f}")


if __name__ == "__main__":
    for p in (64, 144, 289):
        for kind in ("ar1", "exp2d"):
            run(p, kind)
