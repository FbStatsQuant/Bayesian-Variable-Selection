"""Unit checks for track C (brute force on tiny cases with known answers).  python3 c_test.py  -> prints PASS/FAIL."""
import itertools
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_designs import make_design, draw_X, standardize, DESIGNS   # noqa: E402
import c_proxies as P                                                # noqa: E402

FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    if not ok:
        FAIL.append(name)


rng = np.random.default_rng(1)

# 1. designs: sigma_rows symmetric unit-diagonal PSD; matvec agrees; draws have covariance Sigma; lam_min_pop
for did in DESIGNS:
    p = 60
    d = make_design(did, p)
    S = d.sigma_rows(np.arange(p))
    v = rng.standard_normal(p)
    ok = np.allclose(S, S.T) and np.allclose(np.diag(S), 1) and np.allclose(S @ v, d.sigma_matvec(v))
    lm = np.linalg.eigvalsh(S)[0]
    ok = ok and lm > 0 and abs(lm - d.lam_min_pop()) < 1e-6 * max(1, abs(lm)) + (1e-6 if did not in (2, 3, 4, 8, 9) else 0)
    X = draw_X(d, 40000, 1)
    C = np.cov(X, rowvar=False)
    err = np.abs(C - S).max()
    check(f"design D{did:02d} {d.name}: Sigma/matvec/lam_min/draw-cov", ok and err < 0.05, f"lam_min={lm:.4f} cov err={err:.3f}")
# eigsh route of lam_min_pop for p > 3000 vs analytic / dense
for did, ref in ((1, 1.0), (5, 0.3), (14, 0.5), (16, 0.3)):
    d = make_design(did, 3200)
    check(f"lam_min_pop eigsh/analytic D{did:02d} p=3200", abs(d.lam_min_pop() - ref) < 1e-3, f"{d.lam_min_pop():.5f} vs {ref}")
d = make_design(3, 3200); d_small = make_design(3, 2000)
lmA = d.lam_min_pop(); lmD = d_small.lam_min_pop()
check("lam_min_pop symbol-bound AR0.8 p=3200 ~ (1-r)/(1+r) and <= dense p=2000", lmA <= lmD + 1e-6 and abs(lmA - 0.2 / 1.8) < 2e-3,
      f"{lmA:.5f}, dense2000 {lmD:.5f}, limit {0.2 / 1.8:.5f}")
d = make_design(18, 5000)
S = d.sigma_rows(np.arange(5000)[:300]); check("RIBO tiling p=5000: copy-0/1 cross block zero", np.allclose(S[:, 4088:4200], 0) and not np.allclose(S[:, :4088], 0))

# 2. bordered_lmin vs brute force
for trial in range(5):
    n, p = 30, 25
    Z = standardize(rng.standard_normal((n, p)) @ rng.standard_normal((p, p)) * 0.3 + rng.standard_normal((n, p)))
    R = Z.T @ Z
    S = list(rng.choice(p, 4, replace=False))
    vals, d0 = P.bordered_lmin(R[np.ix_(S, S)], R[S], exclude=S)
    bf = np.array([np.linalg.eigvalsh(R[np.ix_(S + [c], S + [c])])[0] if c not in S else np.inf for c in range(p)])
    check(f"bordered_lmin min/argmin (trial {trial})", abs(vals.min() - bf.min()) < 1e-9 and int(np.argmin(vals)) == int(np.argmin(bf))
          and abs(d0 - np.linalg.eigvalsh(R[np.ix_(S, S)])[0]) < 1e-12)

# 3. greedy chain vs exact enumeration, and chunk_pass Gershgorin <= exact, degrees
n, p = 40, 18
d = make_design(3, p); Z = standardize(draw_X(d, n, 1)); R = Z.T @ Z
so = P.SampleOracle(Z)
cp = P.chunk_pass(Z, 6, (0.3, 0.5), chunk=7)
A = np.abs(R); np.fill_diagonal(A, 0)
i, j = np.unravel_index(np.argmax(A), A.shape)
check("chunk_pass top pair", abs(cp["top"][0] - A.max()) < 1e-12 and {cp["top"][1], cp["top"][2]} == {i, j})
check("chunk_pass degrees", np.array_equal(cp["deg"][0], (A > 0.3).sum(1)))
_, lam = P.greedy_chain(so, [i, j], 7)
for k in range(2, 8):
    ex = min(np.linalg.eigvalsh(R[np.ix_(c, c)])[0] for c in itertools.combinations(range(p), k))
    check(f"k={k}: Gershgorin LB <= exact <= greedy UB", cp["gersh"][k] <= ex + 1e-12 and ex <= lam[k] + 1e-12,
          f"LB {cp['gersh'][k]:.3f} exact {ex:.4f} greedy {lam[k]:.4f}")
# anchored chain: step 1 exact
S0 = [0, 5, 10, 15]
_, lamA = P.greedy_chain(so, S0, 6)
ex1 = min(np.linalg.eigvalsh(R[np.ix_(S0 + [c], S0 + [c])])[0] for c in range(p) if c not in S0)
check("anchored chain k=1 is exact", abs(lamA[5] - ex1) < 1e-9)

# 4. IND: sparse eigenvalues ~ 1 at large n (known answer), population layer exact
n, p = 4000, 50
d = make_design(1, p); Z = standardize(draw_X(d, n, 1)); so = P.SampleOracle(Z)
_, lam = P.greedy_chain(so, [0, 12, 24, 36], 20)
check("IND n=4000 p=50: anchored floor at k=16 within 1 - 4*sqrt(20/n)", lam[20] > 1 - 4 * math.sqrt(20 / n) and lam[20] < 1, f"{lam[20]:.4f}")
po = P.PopOracle(d)
_, lamp = P.greedy_chain(po, [0, 12, 24, 36], 20)
check("IND population chain == 1", abs(lamp[20] - 1) < 1e-12)
theta = np.array([1.4, -1.0, 1.8, -1.2]); S0 = [0, 12, 24, 36]
GS = po.rows(S0); gmu = GS.T @ theta; vmu = float(theta @ GS[:, S0] @ theta)
g = P.leakage_scores(po, p, S0, theta, gmu, vmu)
check("IND population leakage: g_l = 0 off S0 (Q = S0)", np.all(g[np.isfinite(g)] < 1e-12))
vis = [P.visibility_path(po, p, S0, theta, j, GS[jj], gmu, vmu)[0].min() for jj, j in enumerate(S0)]
check("IND population visibility = theta_j^2 (masking cannot hide)", np.allclose(vis, [min(theta ** 2)] * 0 + [t ** 2 for t in theta]) or
      abs(min(vis) - min(theta ** 2)) < 1e-12, f"{np.round(vis, 4)}")

# 5. visibility / margin vs explicit projections (sample)
n, p = 60, 30
d = make_design(6, p); X = draw_X(d, n, 2); sd = X.std(0, ddof=1); Z = standardize(X); so = P.SampleOracle(Z)
Xs = Z * math.sqrt(n - 1)
S0 = [0, 1, 2, 3]; theta = np.array([1.4, 1.0, 1.8, 1.2]) * sd[S0]
mu = Xs[:, S0] @ theta
GS = so.rows(S0); gmu = GS.T @ theta; vmu = float(theta @ GS[:, S0] @ theta)


def proj(M):
    if M.shape[1] == 0:
        return np.zeros((n, n))
    Q_, _ = np.linalg.qr(M); return Q_ @ Q_.T


path, U = P.visibility_path(so, p, S0, theta, 2, GS[2], gmu, vmu, 6)
ok = True
for k in range(len(path)):
    Uk = U[:k]
    d2 = mu @ (proj(Xs[:, Uk + [2]]) - proj(Xs[:, Uk])) @ mu
    ok &= abs((n - 1) * path[k] - d2) < 1e-6 * max(1, d2)
check("visibility delta2 along the greedy path == ||(P_{U+j} - P_U) mu||^2", ok)
# greedy step is the true best single addition
k = 2; Uk = U[:k]
best = min((mu @ (proj(Xs[:, Uk + [c, 2]]) - proj(Xs[:, Uk + [c]])) @ mu, c) for c in range(p) if c not in Uk + [2])
check("visibility greedy step = best single masking column", best[1] == U[k], f"{best} vs {U[k]}")
mg = P.margin_path(so, p, S0, theta, 1, gmu, vmu, 5)
cd_U = [0, 2, 3]
rss = mu @ (np.eye(n) - proj(Xs[:, cd_U])) @ mu
check("margin path <= RSS at S0\\j and > 0", (n - 1) * mg <= rss + 1e-8 and mg > 0, f"{(n - 1) * mg:.3f} <= {rss:.3f}")

# 6. Occam terms vs determinants
n, p = 30, 12
d = make_design(5, p); Z = standardize(draw_X(d, n, 3)); Xs = Z * math.sqrt(n - 1)
S0 = [0, 1, 6, 7]


def D(S):
    G = Xs[:, S].T @ Xs[:, S]
    return np.linalg.det((n + 1) * G + np.eye(len(S))) / np.linalg.det(G + np.eye(len(S)))


others = [l for l in range(p) if l not in S0]
t1 = (5) / (2 * p - 1 - 4) * sum(math.sqrt(D(S0) / D(S0 + [l])) for l in others)
t2 = 5 * 6 / ((2 * p - 5) * (2 * p - 6)) * sum(math.sqrt(D(S0) / D(S0 + list(c))) for c in itertools.combinations(others, 2))
a1, a2 = P.occam_terms(Z, S0, top=200)
check("Occam j=1 and j=2 terms vs determinants", abs(a1 - t1) < 1e-8 * t1 and abs(a2 - t2) < 1e-6 * t2, f"{a1:.6g}/{t1:.6g} {a2:.6g}/{t2:.6g}")

# 7. local regressions / width vs direct
n, p = 50, 20
d = make_design(3, p); Z = standardize(draw_X(d, n, 4)); so = P.SampleOracle(Z)
T = np.array([0, 3, 7, 9])
r = np.random.default_rng(5)
nu, nu99, l1, w0, tm, tq = P.local_and_width(Z, so.rows, [T], 3, r)
r = np.random.default_rng(5); Gg = r.standard_normal((n, 3))
best = np.full(3, -np.inf); nmax = 0
for l in range(p):
    if l in T:
        continue
    c, *_ = np.linalg.lstsq(Z[:, T], Z[:, l], rcond=None)
    res = Z[:, l] - Z[:, T] @ c; u = res / np.linalg.norm(res)
    a0 = math.sqrt(math.log(n + 1) + 2 * math.log(p / 5))
    best = np.maximum(best, np.abs(u @ Gg) - a0)
    s = np.sort(np.abs(c))[::-1]
    nmax = max(nmax, next(v for v in range(5) if s[v:].sum() <= 0.1))
check("local regressions nu_hat and width w0 vs direct lstsq", nu[0.1] == nmax and abs(w0 - best.mean()) < 1e-9, f"{nu[0.1]} {nmax} {w0:.4f} {best.mean():.4f}")

# 8. op norm
n, p = 100, 40
d = make_design(2, p); Z = standardize(draw_X(d, n, 1))
ref = np.abs(np.linalg.eigvalsh(Z.T @ Z - d.sigma_rows(np.arange(p)))).max()
check("op_norm_diff vs dense", abs(P.op_norm_diff(Z, d.sigma_matvec) - ref) < 1e-3 * ref)

# 9. msharp sanity (monotone in n at fixed p/n, within [s0, K])
ms = [P.msharp(n, 10 * n, 4) for n in (200, 400, 800, 1600)]
check("msharp within [s0, n/2]", all(4 <= m <= n // 2 for m, n in zip(ms, (200, 400, 800, 1600))), str(ms))

print("\nSUMMARY:", "ALL PASS" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
