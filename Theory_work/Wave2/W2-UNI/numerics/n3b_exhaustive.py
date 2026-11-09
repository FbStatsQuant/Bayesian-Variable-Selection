"""W2-UNI numerics N3b: EXHAUSTIVE small-p falsification of U-LOC (a), (b), the LOCL variance identity, and the exact
constants c_G (singleton and block partitions) and kappa', per R01's optional suggestion.

p = 10 (all l, all T subset of [p]\\{l}: 10 * 512 pairs per draw), 5 noise draws per design. Designs (unit-diagonal Sigma
= lam lam^T + Psi, Psi = D^{1/2} R D^{1/2}, D = diag(1 - lam^2), arbitrary loading signs):
  A  R = AR(1) rho 0.6 on a line (Sigma-branch)
  B  R from a GMRF precision on a path, Theta-branch
  C  pseudometric with zero-distance clusters {0,1},{2,3,4},{5},{6,7},{8,9} plus small positive distances 0.3 between
     consecutive clusters: R_jk = 0.5 exp(-2 delta) off-diagonal (clusters at delta 0 get 0.5), then spectrum checked
  D  block-diagonal R (blocks of size 2 with within-block 0.4): FACA's class, with the block partition as G
Checks: (a) identity max error; (b) inequality violations; LOCL variance identity
  psi_{l|A} = psi_{l|T} + Delta^T Psi Delta, A = T cap B(l,r), for r in {0, 0.5, 1, 2} (max abs error);
  exact c_G (singletons; and blocks for D), exact kappa', kappa and alpha0.
Run: py -3.13 -B n3b_exhaustive.py > n3b_out.txt
"""
import itertools
import numpy as np

rng = np.random.default_rng(11)
p = 10


def build(kind):
    lam = rng.uniform(0.3, 0.75, p) * rng.choice([-1, 1], p)
    idx = np.arange(p)
    if kind == "A":
        R = 0.6 ** np.abs(idx[:, None] - idx[None, :]); dl = np.abs(idx[:, None] - idx[None, :]).astype(float); groups = [[i] for i in idx]
    elif kind == "B":
        Th = np.eye(p) + np.diag(-0.4 * np.ones(p - 1), 1) + np.diag(-0.4 * np.ones(p - 1), -1)
        R = np.linalg.inv(Th); s = np.sqrt(np.diag(R)); R = R / s[:, None] / s[None]
        dl = np.abs(idx[:, None] - idx[None, :]).astype(float); groups = [[i] for i in idx]
    elif kind == "C":
        cl = [0, 0, 1, 1, 1, 2, 3, 3, 4, 4]
        pos = np.array([0.0, 0.3, 0.6, 0.9, 1.2])[cl]
        dl = np.abs(pos[:, None] - pos[None, :])
        R = 0.5 * np.exp(-2 * dl); np.fill_diagonal(R, 1.0); groups = [[i] for i in idx]
    else:
        R = np.eye(p)
        for b in range(0, p, 2):
            R[b, b + 1] = R[b + 1, b] = 0.4
        dl = np.where(np.abs(idx[:, None] // 2 - idx[None, :] // 2) == 0, 0.0, float(p)); groups = [[b, b + 1] for b in range(0, p, 2)]
    Dh = np.sqrt(1 - lam ** 2)
    Psi = Dh[:, None] * R * Dh[None]
    assert np.linalg.eigvalsh(Psi).min() > 0
    return lam, Psi, np.outer(lam, lam) + Psi, dl, groups


def run(kind):
    lam, Psi, Sig, dl, groups = build(kind)
    gid = np.empty(p, int)
    for gi, g in enumerate(groups):
        gid[g] = gi
    all_sets = [list(T) for k in range(p + 1) for T in itertools.combinations(range(p), k)]  # incl. T = [p] (R03-3)
    # exact c_G and kappa'
    cG_single, cG_grp, kap = np.inf, np.inf, 0.0
    for T in all_sets:
        if T:
            s = lam[T] @ np.linalg.solve(Psi[np.ix_(T, T)], lam[T])
            cG_single = min(cG_single, s / len(T)); cG_grp = min(cG_grp, s / len(set(gid[T])))
        for l in range(p):
            if l in T:
                continue
            if T:
                bT = np.linalg.solve(Psi[np.ix_(T, T)], Psi[T, l]); psi = Psi[l, l] - Psi[l, T] @ bT; lt = lam[l] - bT @ lam[T]
            else:
                psi, lt = Psi[l, l], lam[l]
            kap = max(kap, abs(lt) / np.sqrt(psi))
    L = np.linalg.cholesky(Psi)
    id_err, viol, var_err, npairs = 0.0, 0, 0.0, 0
    for draw in range(5):
        xi0 = rng.standard_normal(); zeta = L @ rng.standard_normal(p); g = lam * xi0 + zeta
        for T in all_sets:
            for l in range(p):
                if l in T:
                    continue
                npairs += 1
                if T:
                    PT = Psi[np.ix_(T, T)]; bT = np.linalg.solve(PT, Psi[T, l]); psi = Psi[l, l] - Psi[l, T] @ bT
                    Xi = (zeta[l] - bT @ zeta[T]) / np.sqrt(psi); lt = lam[l] - bT @ lam[T]
                    a = np.linalg.solve(PT, lam[T]); s = lam[T] @ a; F = (a @ zeta[T]) / np.sqrt(s)
                    W = (xi0 - a @ zeta[T]) / np.sqrt(1 + s)
                    cS = np.linalg.solve(Sig[np.ix_(T, T)], Sig[T, l])
                    Z = (g[l] - cS @ g[T]) / np.sqrt(Sig[l, l] - Sig[l, T] @ cS)
                    env = abs(Xi) + kap * abs(xi0) + kap * abs(F) / np.sqrt(s)
                    if draw == 0:
                        full = np.zeros(p); full[T] = bT
                        for r in (0.0, 0.5, 1.0, 2.0):
                            A = [v for v in T if dl[l, v] <= r]
                            bA = np.zeros(p)
                            if A:
                                bA[A] = np.linalg.solve(Psi[np.ix_(A, A)], Psi[A, l])
                            psiA = Psi[l, l] - Psi[l] @ bA
                            Dl = full - bA
                            var_err = max(var_err, abs(psiA - (psi + Dl @ Psi @ Dl)))
                else:
                    psi, Xi, lt, s, W = Psi[l, l], zeta[l] / np.sqrt(Psi[l, l]), lam[l], 0.0, xi0
                    Z = g[l] / np.sqrt(Sig[l, l]); env = abs(Xi) + kap * abs(xi0)
                dec = (np.sqrt(psi) * Xi + lt / np.sqrt(1 + s) * W) / np.sqrt(psi + lt ** 2 / (1 + s))
                id_err = max(id_err, abs(Z - dec)); viol += int(abs(Z) > env + 1e-10)
    k1 = kap / np.sqrt(cG_single); k2 = kap / np.sqrt(cG_grp)
    a0 = lambda k: 1 / (2 * max(k, 1) * (max(k, 1) + 2))
    print(f"design {kind}: pairs={npairs} identity_err={id_err:.2e} ineq_viol={viol} LOCL_var_identity_err={var_err:.2e} "
          f"kappa'={kap:.3f} c_G(single)={cG_single:.3f} kappa(single)={k1:.3f} alpha0={a0(k1):.4f} | "
          f"c_G(groups)={cG_grp:.3f} kappa(groups)={k2:.3f} alpha0={a0(k2):.4f}")


if __name__ == "__main__":
    for kind in "ABCD":
        run(kind)
    # block compound symmetry sanity: kappa = 1 with the group partition (FACA Lemma kappa)
    lam = np.full(p, np.sqrt(0.3)); Psi = 0.3 * np.eye(p)
    for b in range(0, p, 5):
        Psi[b:b + 5, b:b + 5] += 0.4
    gid = np.arange(p) // 5
    cg, kp = np.inf, 0.0
    for k in range(1, p + 1):  # incl. T = [p] (R03-3)
        for T in itertools.combinations(range(p), k):
            T = list(T); s = lam[T] @ np.linalg.solve(Psi[np.ix_(T, T)], lam[T]); cg = min(cg, s / len(set(gid[T])))
    for k in range(0, p):
        for T in itertools.combinations(range(p), k):
            T = list(T)
            for l in range(p):
                if l in T:
                    continue
                if T:
                    bT = np.linalg.solve(Psi[np.ix_(T, T)], Psi[T, l]); psi = Psi[l, l] - Psi[l, T] @ bT; lt = lam[l] - bT @ lam[T]
                else:
                    psi, lt = Psi[l, l], lam[l]
                kp = max(kp, abs(lt) / np.sqrt(psi))
    print(f"S5-type block CS (rho_b=.3, rho_w=.7, groups of 5): c_G(groups)={cg:.4f} (FACA c_min=0.3/0.7={0.3/0.7:.4f}), kappa'={kp:.4f}, kappa={kp/np.sqrt(cg):.4f}")
