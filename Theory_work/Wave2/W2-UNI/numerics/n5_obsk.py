"""W2-UNI numerics N5: falsification probe for Lemma OBS-k (lemmas/L6_frontier.md L6.1; STATEMENT (iii')(a)) [R05a-15].

Claim probed: fix k >= 2 and m >= 1 (independent of n). If p -> inf, loading rows ||Lambda_j|| <= L and Psi >= c I, then
  inf_{m <= |T| <= p} lambda_min(Lambda_T' Psi_TT^{-1} Lambda_T) / |T|  -> 0.
The proof is constructive: cover S^{k-1} by cells of diameter eta/L_*; a cell holding the orthogonal directions u_j of m
rows gives T with lambda_min/|T| <= eta^2/c. This script
  (1) builds T exactly as in the proof (cells = angular sectors for k = 2, a regular grid on the sphere for k = 3 via
      binning normalised u_j), for p in {50, 200, 800, 3200}, m in {1, 2, k, k + 1, 5};
  (2) records the information ratio I(T) := lambda_min(Lambda_T' Psi_TT^{-1} Lambda_T)/|T| for that T, the proof's
      intermediate bound c^{-1} sum_{j in T} (Lambda_j' u)^2 / |T| for the u used, and checks
      I(T) <= that bound <= eta_eff^2 / c (eta_eff := L_* x observed cell diameter) -- inequality violations are counted;
  (3) reports the full-set ratio I([p]) for comparison (the obstruction concerns small/fixed-size subsets, not [p]);
  (4) the R01 item-7 example k = 2, Lambda_j in {sqrt(a) e1, sqrt(a) e2} alternating: I([p]) bounded below while
      I(T) = 0 for T of m rows of one type (m >= 1), consistent with the scope sentence of L6.1.
Psi: AR(1) correlation (rho = 0.5) scaled by 0.6 plus 0.4 I  (so Psi >= c I with c = lambda_min reported), i.e. a non-diagonal
metric-local Psi. Loadings: iid uniform direction, norm uniform in [0.2, 1] (L = 1), seeded.
Observations only (a falsification probe; the proof is the certificate).
Run: py -3.13 -B n5_obsk.py > n5_obsk_out.txt
"""
import itertools
import numpy as np

rng = np.random.default_rng(20261109 + 5)


def psi_mat(p):
    idx = np.arange(p)
    return 0.6 * 0.5 ** np.abs(idx[:, None] - idx[None, :]) + 0.4 * np.eye(p)


def info(Lam, Psi, T):
    T = np.asarray(T)
    LT = Lam[T]
    M = LT.T @ np.linalg.solve(Psi[np.ix_(T, T)], LT)
    return np.linalg.eigvalsh(M).min() / len(T)


def orth_dir(v):
    """a unit vector orthogonal to v (k >= 2), deterministic"""
    k = len(v)
    if k == 2:
        u = np.array([-v[1], v[0]])
    else:
        e = np.zeros(k); e[np.argmin(np.abs(v))] = 1.0
        u = e - (e @ v) / (v @ v) * v
    return u / np.linalg.norm(u)


def cells(U, k, ncell):
    """bin unit vectors into cells: sectors (k = 2) or a sign/angle grid on the cube projection (k = 3)"""
    if k == 2:
        ang = np.mod(np.arctan2(U[:, 1], U[:, 0]), 2 * np.pi)
        return np.floor(ang / (2 * np.pi) * ncell).astype(int)
    # k = 3: project to the cube face of largest |coordinate|, then grid that face
    a = np.argmax(np.abs(U), axis=1)
    s = np.sign(U[np.arange(len(U)), a])
    face = a * 2 + (s > 0)
    V = U / np.abs(U[np.arange(len(U)), a])[:, None]  # coordinates in [-1, 1]
    others = np.array([[1, 2], [0, 2], [0, 1]])[a]
    c1 = np.floor((V[np.arange(len(U)), others[:, 0]] + 1) / 2 * ncell).clip(0, ncell - 1)
    c2 = np.floor((V[np.arange(len(U)), others[:, 1]] + 1) / 2 * ncell).clip(0, ncell - 1)
    return (face * ncell * ncell + c1 * ncell + c2).astype(int)


def run(k, p, m, ncell):
    Psi = psi_mat(p)
    c = np.linalg.eigvalsh(Psi).min()
    D = rng.standard_normal((p, k)); D /= np.linalg.norm(D, axis=1, keepdims=True)
    Lam = D * rng.uniform(0.2, 1.0, (p, 1))
    Lstar = max(1.0, np.linalg.norm(Lam, axis=1).max())
    U = np.array([orth_dir(Lam[j]) for j in range(p)])
    lab = cells(U, k, ncell)
    vals, cnt = np.unique(lab, return_counts=True)
    ok = vals[cnt >= m]
    if len(ok) == 0:
        return None
    best = None
    for cl in ok:
        members = np.where(lab == cl)[0]
        # choose the m members with the tightest directions around the first member's u (proof: any m in the cell)
        u = U[members[0]]
        T = members[np.argsort(np.linalg.norm(U[members] - u, axis=1))[:m]]
        diam = max(np.linalg.norm(U[a_] - U[b_]) for a_, b_ in itertools.combinations(T, 2)) if m > 1 else 0.0
        IT = info(Lam, Psi, T)
        mid = np.sum((Lam[T] @ u) ** 2) / c / len(T)
        eta = Lstar * diam
        rec = (IT, mid, eta ** 2 / c, IT <= mid * (1 + 1e-10) + 1e-14, mid <= eta ** 2 / c * (1 + 1e-10) + 1e-14)
        if best is None or rec[0] < best[0]:
            best = rec
    full = info(Lam, Psi, np.arange(p)) if p <= 800 else float("nan")
    return c, best, full


print("OBS-k probe: I(T) = lambda_min(Lam_T' Psi_TT^-1 Lam_T)/|T| for the proof's T; checks I(T) <= mid <= eta^2/c")
viol = 0
for k in (2, 3):
    for m in sorted({1, 2, k, k + 1, 5}):
        for p in (50, 200, 800, 3200):
            ncell = max(4, int(round((p / (4 * m)) ** (1 / (k - 1)))))  # cells shrink as p grows
            r = run(k, p, m, ncell)
            if r is None:
                print(f"k={k} m={m} p={p:5d}: no cell with >= m members (ncell={ncell})"); continue
            c, (IT, mid, bnd, ok1, ok2), full = r
            viol += (not ok1) + (not ok2)
            print(f"k={k} m={m} p={p:5d} ncell={ncell:4d} c={c:.3f}: I(T)={IT:.3e} mid={mid:.3e} eta^2/c={bnd:.3e} "
                  f"chain_ok={ok1 and ok2}  I([p])={full:.3e}")
print(f"total chain violations: {viol}")

# R01 item-7 example: k = 2, alternating sqrt(a) e1 / sqrt(a) e2 rows
a = 0.5
for p in (50, 200, 800):
    Psi = psi_mat(p)
    Lam = np.zeros((p, 2)); Lam[0::2, 0] = np.sqrt(a); Lam[1::2, 1] = np.sqrt(a)
    print(f"R01-7 example p={p}: I([p])={info(Lam, Psi, np.arange(p)):.4f}; "
          + "; ".join(f"I(T, m={m} rows of type e1)={info(Lam, Psi, np.arange(0, 2 * m, 2)):.2e}" for m in (1, 2, 3, 5)))
