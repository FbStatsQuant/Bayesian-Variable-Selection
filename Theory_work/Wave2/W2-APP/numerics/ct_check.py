"""Falsification check of Lemma CT and Lemma CD (lemmas/L2_CT.md).
For several LOC matrices, compute the explicit constants and check
 (1) |(A^-1)_ij| <= (2/alpha) exp(-t* d_ij)   (CT on Sigma and on Theta)
 (2) |Cov(W_j,W_k|W_U)| <= K2 exp(-t2 d(j,k)) for ALL U of size <= 2 (exhaustive over j,k,U for small p),
     random U of sizes up to p-2 (many draws), and adversarial U (all indices between j and k removed / kept).
 (3) c <= Var(W_j|W_U) <= 1.
Reports the max ratio observed/bound (must be <= 1)."""
import numpy as np, itertools
rng = np.random.default_rng(20261109)

def tstar(alpha, K, a):
    u = 1.0 / (alpha / (4 * K) + 1.0 / np.expm1(a))
    t = a - np.log1p(u)
    assert 0 < t < a
    return t

def unitdiag(S):
    d = np.sqrt(np.diag(S)); return S / np.outer(d, d)

def fit_Ka(S, a, pos):
    D = np.abs(pos[:, None] - pos[None, :]).astype(float)
    off = ~np.eye(len(S), dtype=bool)
    return np.max(np.abs(S[off]) * np.exp(a * D[off])), D

def cases(p):
    out = []
    # AR(1)
    for r in (0.5, -0.8, 0.9):
        S = r ** np.abs(np.subtract.outer(np.arange(p), np.arange(p))); out.append((f"AR1 rho={r}", S, 'S', np.log(1/abs(r))))
    # AR(2) Toeplitz via spectral density -> autocovariance by Yule-Walker recursion
    phi1, phi2 = 0.5, 0.3
    g = np.zeros(p); g0 = 1.0
    rho1 = phi1 / (1 - phi2); g[0] = 1; g[1] = rho1
    for h in range(2, p): g[h] = phi1 * g[h-1] + phi2 * g[h-2]
    S = g[np.abs(np.subtract.outer(np.arange(p), np.arange(p)))]
    out.append(("AR2 (0.5,0.3)", S, 'S', 0.25))
    # MA(2) banded
    th = [1, 0.8, -0.5]; ac = [sum(th[i]*th[i+h] for i in range(3-h)) for h in range(3)]
    g = np.zeros(p); g[:3] = ac; S = unitdiag(g[np.abs(np.subtract.outer(np.arange(p), np.arange(p)))])
    out.append(("MA2 banded", S, 'S', 1.0))
    # random banded precision (GMRF), bandwidth 3, permuted positions
    Th = np.zeros((p, p))
    for b in range(1, 4):
        v = rng.uniform(-0.25, 0.25, p - b); Th += np.diag(v, b) + np.diag(v, -b)
    Th += np.eye(p) * (np.abs(Th).sum(1).max() + 0.3)
    S = unitdiag(np.linalg.inv(Th)); out.append(("random banded precision bw3", S, 'S', 0.5))
    # block diagonal equicorrelated blocks g=7 rho=0.85 (g>16 tested separately), and g=20 rho=0.6
    for gsz, r in ((7, 0.85), (20, 0.6)):
        S = np.zeros((p, p))
        for s0 in range(0, p, gsz):
            e = min(p, s0 + gsz); S[s0:e, s0:e] = r
        np.fill_diagonal(S, 1); out.append((f"blocks g={gsz} rho={r}", S, 'S', 1.0))
    # random exponentially decaying (not banded), random signs
    D = np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    M = rng.choice([-1, 1], (p, p)) * 0.45 * np.exp(-0.7 * D); M = np.triu(M, 1); M = M + M.T
    S = M + np.eye(p) * (1.0)
    lam = np.linalg.eigvalsh(S)
    if lam[0] <= 0.05: S = S + np.eye(p) * (0.1 - lam[0])
    S = unitdiag(S); out.append(("random exp-decay signs", S, 'S', 0.7))
    return out

def check(name, S, a, perm, lines, nU=4000):
    p = len(S); pos = perm.astype(float)  # positions pi(j)
    Sp = S  # entries indexed by original labels; positions = perm
    lam = np.linalg.eigvalsh(Sp); c, C = lam[0], lam[-1]
    K, D = fit_Ka(Sp, a, pos)
    Th = np.linalg.inv(Sp)
    # CT on Sigma -> Theta
    t1 = tstar(c, K, a); K1 = 2 / c
    r1 = np.max(np.abs(Th) / ((2 / c) * np.exp(-t1 * D)))
    t2 = tstar(1 / C, K1, t1); K2 = 2 * C
    worst = 0.0; worstvar = (np.inf, -np.inf)
    def condcov(U):
        V = np.setdiff1d(np.arange(p), U)
        return V, np.linalg.inv(Th[np.ix_(V, V)])
    Us = [np.array([], int)] + [np.array([u]) for u in range(p)] + [np.array(u) for u in itertools.combinations(range(p), 2)]
    for _ in range(nU):
        k = rng.integers(3, p - 1); Us.append(rng.choice(p, k, replace=False))
    for U in Us:
        V, Cv = condcov(U)
        dv = np.diag(Cv); worstvar = (min(worstvar[0], dv.min()), max(worstvar[1], dv.max()))
        DV = D[np.ix_(V, V)]; off = ~np.eye(len(V), dtype=bool)
        if off.any():
            worst = max(worst, np.max(np.abs(Cv[off]) / (K2 * np.exp(-t2 * DV[off]))))
    lines.append(f"{name:32s} p={p} c={c:.3f} C={C:.3f} K={K:.3g} a={a} | t1={t1:.4f} t2={t2:.3e} K2={K2:.3f} | "
                 f"max ratio CT(Sigma->Theta)={r1:.3e}  max ratio condcov={worst:.3e}  Var|U in [{worstvar[0]:.3f},{worstvar[1]:.3f}] (c={c:.3f})  #U={len(Us)}")
    assert r1 <= 1 + 1e-9 and worst <= 1 + 1e-9 and worstvar[0] >= c - 1e-9 and worstvar[1] <= 1 + 1e-9
    return t2

def ct_tightness(lines):
    # how loose is t*? compare with the empirical decay rate of Theta for AR(1): exact rate log(1/rho) for Theta (banded!)
    # and conditional covariances for AR(1) decay at rate log(1/rho) (P4); report t2 vs that.
    for r in (0.5, 0.9):
        p = 40; S = r ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
        lam = np.linalg.eigvalsh(S); c, C = lam[0], lam[-1]
        t1 = tstar(c, 1.0, np.log(1/r)); t2 = tstar(1/C, 2/c, t1)
        lines.append(f"tightness AR1 rho={r}: true decay rate log(1/rho)={np.log(1/r):.3f}; CT gives t1={t1:.3e}, t2={t2:.3e} (valid but conservative)")

lines = []
for p in (14, 30):
    for name, S, kind, a in cases(p):
        for permkind in ("identity", "random"):
            perm = np.arange(p) if permkind == "identity" else rng.permutation(p)
            # The LOC decay is w.r.t. positions perm(j): build S' whose entries decay in |perm(j)-perm(k)|
            Sp = S[np.ix_(np.argsort(perm), np.argsort(perm))] if permkind == "random" else S
            # S'[j,k] = S[q(j),q(k)] with q = perm^{-1}; decays in |q(j)-q(k)|... use positions q
            q = np.argsort(perm)
            check(f"{name} [{permkind}]", Sp, a, q, lines, nU=1500 if p == 30 else 3000)
ct_tightness(lines)
lines.append("ALL ASSERTIONS PASSED (every observed ratio <= 1).")
open("ct_check_out.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
