"""D18 (riboflavin-like) visibility: greedy masking search (float) + exact rational recomputation at the found U."""
import sys, numpy as np
from fractions import Fraction as Fr
L = np.loadtxt(sys.argv[1], delimiter=",")
p0, k = L.shape
S = L @ L.T + 0.1 * np.eye(p0)
print("p0, k:", p0, k, " max|diag-1|:", np.abs(np.diag(S) - 1).max(), " lam_min:", np.linalg.eigvalsh(S)[0])

def greedy(S, truths, theta, j, umax=15):
    """greedy masking (as track C): add the column that most lowers delta2 = cov(j, mu|U)^2 / var(j|U)."""
    p = S.shape[0]; U = []
    best = None
    for step in range(umax + 1):
        if U:
            A = S[np.ix_(U, U)]; Ainv = np.linalg.inv(A)
            G = S - S[:, U] @ Ainv @ S[U, :]
        else:
            G = S.copy()
        mu = G[:, truths] @ theta         # cov(., Y | U) for every column
        vj = G[j, j]; cj = mu[j]; d2 = cj * cj / vj
        if best is None or abs(cj) < best[0]:
            best = (abs(cj), list(U), d2)
        if step == umax: break
        a = G[:, j]; vc = np.diag(G).copy()
        ok = vc > 1e-10; ok[j] = False; ok[U] = False
        num = (cj - a * mu / np.where(ok, vc, 1)) ** 2
        den = np.maximum(vj - a * a / np.where(ok, vc, 1), 1e-15)
        new = np.where(ok, num / den, np.inf)
        U.append(int(np.argmin(new)))
    return best

def exact_cov(S, truths, theta, j, U):
    idx = list(U) + [j] + [t for t in truths if t not in U and t != j]
    M = [[Fr(float(S[a, b])) for b in idx] for a in idx]
    m = len(U)
    # Schur complement of the U block: Gamma = M_rest - M_rU M_UU^{-1} M_Ur, by exact Gaussian elimination
    for piv in range(m):
        pv = M[piv][piv]
        for r in range(piv + 1, len(idx)):
            f = M[r][piv] / pv
            if f:
                for c in range(piv, len(idx)):
                    M[r][c] -= f * M[piv][c]
    # after eliminating the U columns, rows/cols m.. hold the Schur complement (symmetric part in lower-right)
    pos = {t: m + i for i, t in enumerate(idx[m:])}
    th = dict(zip(truths, theta))
    cov = sum(Fr(float(th[t])) * M[pos[j]][pos[t]] for t in truths if t not in U)
    var = M[pos[j]][pos[j]]
    return cov, var

def report(label, truths, theta, Smat):
    print("==", label, "truths", truths, "theta", theta)
    for jj, j in enumerate(truths):
        c, U, d2 = greedy(Smat, truths, np.array(theta), j)
        cov, var = exact_cov(Smat, truths, theta, j, U)
        print(f"  j={j}: greedy min |cov|={c:.3e} (delta2 {d2:.3e}) at |U|={len(U)}; exact: cov={float(cov):.6e}, "
              f"var={float(var):.6f}, cov==0: {cov == 0}")

# clustered: column 0 and its three most correlated partners (population), aligned theta (track C)
r0 = np.abs(S[0]).copy(); r0[0] = -1
clu = [0] + [int(i) for i in np.argsort(-r0)[:3]]
report("clustered (fixed rows of copy 0; every p > 4088)", clu, [1.4, 1.0, 1.8, 1.2], S)
# spread at p = 16000: positions 0, 4000, 8000, 12000 -> copy 0 rows 0, 4000 (shared copy); others in copies 1, 2
# only the shared copy matters for j in {0, 4000}; the other truths have zero covariance with copy 0.
report("spread, p = 16000 (truths 0 and 4000 share copy 0; theta 1.4, -1.0)", [0, 4000], [1.4, -1.0], S)
print("spread, p >= 16352: the four truths lie in four different copies => cov = theta_j Var(W_j|W_U) >= theta_lo * 0.1")
