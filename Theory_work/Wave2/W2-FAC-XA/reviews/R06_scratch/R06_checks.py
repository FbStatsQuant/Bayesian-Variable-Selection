"""R06 reviewer checks for L5 (RN-log) and L6 (OT/ORDER/CS-OLS centre). Diagnostics only, not proofs."""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS'):
    os.environ[_k] = '1'
import numpy as np, json, math
from pathlib import Path
from scipy.special import gammaln
from scipy.optimize import brentq

out = {}


def sym(S, f):
    w, v = np.linalg.eigh(S)
    return (v * f(w)) @ v.T


# ---- C0: scalar Chernoff / net / derivative constants used in L5
u = np.linspace(1e-6, 1 - 1e-6, 200001)
out['C0_upper_min_ratio_(u-log1p(u))/(u^2/4)'] = float(np.min((u - np.log1p(u)) / (u ** 2 / 4)))
out['C0_lower_min_ratio_(-u-log(1-u))/(u^2/4)'] = float(np.min((-u - np.log1p(-u)) / (u ** 2 / 4)))
out['C0_net_C_needed_for_2exp(-t)'] = math.sqrt(8 * max(math.log(9), 1))
out['C0_max_abs_derivative_x^-1/2_on_[1/2,3/2]'] = 0.5 * 0.5 ** -1.5

# ---- C1: RN chain on CS and one-factor; factorization bound; slack of the lambda_max<=p step
rows = []
for kind in ('CS', 'F1'):
    for n, p in [(2000, 25), (2000, 100), (8000, 100), (8000, 400)]:
        for seed in range(3):
            rng = np.random.default_rng(1000 * seed + p + n)
            if kind == 'CS':
                Sig = .5 * np.eye(p) + .5 * np.ones((p, p))
            else:
                lam = rng.uniform(.3, .9, p)
                Sig = np.diag(1 - lam ** 2) + np.outer(lam, lam)
            w = np.linalg.eigvalsh(Sig)
            c = w[0]
            A = sym(Sig, np.sqrt)
            Ai = np.linalg.inv(A)
            raw = rng.normal(size=(n, p)) @ A + 3.0
            raw -= raw.mean(0)
            d = n - 1
            S = raw.T @ raw / d
            Dm = np.diag(1 / np.sqrt(np.diag(S)))
            R = Dm @ S @ Dm
            E0 = Ai @ S @ Ai - np.eye(p)
            Q = Dm - np.eye(p)
            F = Ai @ Q @ A
            eR = np.linalg.norm(Ai @ R @ Ai - np.eye(p), 2)
            nE0 = np.linalg.norm(E0, 2)
            nF = np.linalg.norm(F, 2)
            nQ = np.linalg.norm(Q, 2)
            bound = 2 * nF + nF ** 2 + (1 + nF) ** 2 * nE0
            rows.append(dict(kind=kind, n=n, p=p, seed=seed, eR=eR, bound=bound, ok=bool(eR <= bound + 1e-12),
                             eR_over_sqrt_p_d=eR / math.sqrt(p / d), E0_over_sqrt_p_d=nE0 / math.sqrt(p / d),
                             F_over_sqrt_plogp_d=nF / math.sqrt(p * math.log(p + 1) / d),
                             F_over_sqrt_p_d=nF / math.sqrt(p / d),
                             F_over_crude=nF / (math.sqrt(w[-1] / c) * nQ),
                             maxdiag_over_sqrt_8log2p_d=np.max(np.abs(np.diag(S) - 1)) / math.sqrt(8 * math.log(2 * p) / d)))
out['C1_rn_rows'] = rows
out['C1_all_bound_ok'] = all(r['ok'] for r in rows)


# ---- production score (D0 with capped BB(1,p) prior; K=p here since p<=n/2)
def make_score(X, Y, p):
    n = X.shape[0]
    V = Y @ Y
    nu = n / 2 + .01

    def lw(k):
        return -math.log(2) - gammaln(2 * p) + gammaln(k + 1) + gammaln(2 * p - k)

    def F(T):
        U = X[:, T]
        G = U.T @ U
        v = U.T @ Y
        H = (n + 1) * G + np.eye(len(T))
        Qr = V - n * v @ np.linalg.solve(H, v)
        return lw(len(T)) - .5 * (np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(T)))[1]) \
            - nu * np.log(.02 + (n - 1) / V * Qr)
    return F, lw, V, nu


def Zstat(X, e, T, j, sigma=1.0):
    Tm = [i for i in T if i != j]
    Qm = np.linalg.qr(X[:, Tm], mode='reduced')[0]
    v = X[:, j] - Qm @ (Qm.T @ X[:, j])
    return v @ e / (sigma * np.linalg.norm(v)), v


# ---- C2: OT remainder vs 1/(c n) for strongly correlated CS (small c); spread of the j-dependent part
rows = []
for rho in (.5, .9, .97):
    for n, p in [(400, 12), (1600, 12), (1600, 40)]:
        rng = np.random.default_rng(int(rho * 100) + n + p)
        Sig = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
        A = sym(Sig, np.sqrt)
        raw = rng.normal(size=(n, p)) @ A
        raw -= raw.mean(0)
        X = raw / raw.std(0, ddof=1)
        th = np.zeros(p)
        th[:2] = [1, -.7]
        eps = rng.normal(size=n)
        eps -= eps.mean()
        Y = X @ th + eps
        F, lw, V, nu = make_score(X, Y, p)
        c = np.linalg.eigvalsh(X.T @ X / (n - 1))[0]
        T = list(range(p))
        ft = F(T)
        Qf = np.linalg.qr(X, mode='reduced')[0]
        RSS = V - np.linalg.norm(Qf.T @ Y) ** 2
        W0 = RSS + (V - RSS) / (n + 1) + .02 * V / (n - 1)
        b = n / ((n + 1) * W0)
        Ac = lw(p - 1) - lw(p) + .5 * math.log(n + 1)
        r = []
        for j in range(2, p):
            Z, _ = Zstat(X, eps, T, j)
            r.append(F([i for i in T if i != j]) - ft - (Ac - nu * math.log1p(b * Z ** 2)))
        r = np.array(r)
        rows.append(dict(rho=rho, n=n, p=p, c_hat=c, max_n_c_abs_r=float(np.max(np.abs(r)) * n * c),
                         spread_n_c=float((r.max() - r.min()) * n * c), spread_n=float((r.max() - r.min()) * n)))
out['C2_remainder_rows'] = rows

# ---- C3: near-tie: tune noise so Z_j^2 = Z_l^2 exactly; then gain difference = r_j - r_l
rng = np.random.default_rng(7)
n, p, rho = 300, 10, .9
Sig = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
A = sym(Sig, np.sqrt)
raw = rng.normal(size=(n, p)) @ A
raw -= raw.mean(0)
X = raw / raw.std(0, ddof=1)
th = np.zeros(p)
th[:2] = [1, -.7]
e = rng.normal(size=n)
e -= e.mean()
T = list(range(p))
j, l = 3, 7
_, vj = Zstat(X, e, T, j)
_, vl = Zstat(X, e, T, l)
uj = vj / np.linalg.norm(vj)
ul = vl / np.linalg.norm(vl)


def tie(s):
    ee = e + s * (uj - ul)
    return (uj @ ee) ** 2 - (ul @ ee) ** 2


ss = np.linspace(-6, 6, 241)
vals = [tie(s) for s in ss]
res = []
for i in range(240):
    if vals[i] * vals[i + 1] < 0:
        s = brentq(tie, ss[i], ss[i + 1])
        ee = e + s * (uj - ul)
        Y = X @ th + ee
        F, lw, V, nu = make_score(X, Y, p)
        gj = F([t for t in T if t != j]) - F(T)
        gl = F([t for t in T if t != l]) - F(T)
        res.append(dict(s=s, Zj=float(uj @ ee), Zl=float(ul @ ee), n_gain_diff=float(n * (gj - gl))))
out['C3_tie_rows'] = res

# ---- C4: exact-CS OLS formula and ridge-vs-OLS centre gap (FAC-B L1.4 constants)
rows = []
for rho in (.3, .6, .9):
    for n in (100, 1000, 10000, 100000):
        rng = np.random.default_rng(int(rho * 10) + n)
        p = 20
        k = 12
        T = list(range(k))
        sigma = 1.3
        thbar = 2.1
        eta = rng.normal()
        xi = rng.normal(size=p)
        g = math.sqrt(rho) * eta + math.sqrt(1 - rho) * xi
        SigT = (1 - rho) * np.eye(k) + rho * np.ones((k, k))
        Si = np.linalg.inv(SigT)
        Zdir = (Si @ g[T]) / np.sqrt(np.diag(Si))
        q = k + (1 - rho) / rho
        xo = (xi[T].sum() - math.sqrt((1 - rho) / rho) * eta) / q
        Zf = math.sqrt(q / (q - 1)) * (xi[T] - xo)
        a = n * n - 1
        alpha = a * (1 - rho) + 1
        beta = a * rho
        kap = (1 - rho) / rho + 1 / (rho * a)
        varrho = (math.sqrt(n - 1) * rho * thbar / (sigma * math.sqrt(1 - rho)) + math.sqrt(rho / (1 - rho)) * alpha * eta) / beta
        xr = (xi[T].sum() - varrho) / (k + kap)
        rows.append(dict(rho=rho, n=n, ols_formula_err=float(np.max(np.abs(Zdir - Zf))),
                         centre_gap=abs(xr - xo), centre_gap_times_n15=abs(xr - xo) * n ** 1.5))
out['C4_centre_rows'] = rows

# ---- C5: end-to-end exact-Gram CS design; production null-deletion order vs |xi-x_OLS| and |xi-x_ridge|
rows = []
for seed in range(5):
    rng = np.random.default_rng(50 + seed)
    n, p, rho, sigma = 500, 30, .6, 1.0
    Sig = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
    one = np.ones(n) / math.sqrt(n)
    M = rng.normal(size=(n, p))
    M -= np.outer(one, one @ M)
    O = np.linalg.qr(M)[0]
    X = math.sqrt(n - 1) * O @ sym(Sig, np.sqrt)
    assert np.allclose(X.T @ X, (n - 1) * Sig) and np.allclose(X.sum(0), 0)
    th = np.zeros(p)
    th[:2] = [1, .8]
    eps = sigma * rng.normal(size=n)
    Yr = X @ th + eps
    Y = Yr - Yr.mean()
    e = eps - eps.mean()
    g = X.T @ e / (sigma * math.sqrt(n - 1))
    Si = np.linalg.inv(Sig)
    one_p = np.ones(p)
    cv = math.sqrt(rho) * one_p @ Si
    mean_eta = cv @ g
    var_eta = 1 - math.sqrt(rho) * cv @ one_p
    eta = mean_eta + math.sqrt(max(var_eta, 0)) * rng.normal()
    xi = (g - math.sqrt(rho) * eta) / math.sqrt(1 - rho)
    F, lw, V, nu = make_score(X, Y, p)
    T = list(range(p))
    k = p
    ft = F(T)
    gains = np.array([F([i for i in T if i != j]) - ft for j in range(2, p)])
    q = k + (1 - rho) / rho
    xo = (xi[T].sum() - math.sqrt((1 - rho) / rho) * eta) / q
    a = n * n - 1
    alpha = a * (1 - rho) + 1
    beta = a * rho
    kap = (1 - rho) / rho + 1 / (rho * a)
    thbar = th.sum()
    varrho = (math.sqrt(n - 1) * rho * thbar / (sigma * math.sqrt(1 - rho)) + math.sqrt(rho / (1 - rho)) * alpha * eta) / beta
    xr = (xi[T].sum() - varrho) / (k + kap)
    Zs = np.array([Zstat(X, e, T, j, sigma)[0] for j in range(2, p)])
    dO = np.abs(xi[2:] - xo)
    dR = np.abs(xi[2:] - xr)
    rows.append(dict(seed=seed, order_gain_vs_ridge=bool(np.array_equal(np.argsort(-gains), np.argsort(dR))),
                     order_gain_vs_ols=bool(np.array_equal(np.argsort(-gains), np.argsort(dO))),
                     max_Z_formula_err=float(np.max(np.abs(np.abs(Zs) - math.sqrt(q / (q - 1)) * dO))),
                     centre_gap=abs(xr - xo)))
out['C5_exactCS_rows'] = rows

Path(__file__).with_name('R06_checks_out.json').write_text(json.dumps(out, indent=1, default=float))
print(json.dumps({k: v for k, v in out.items() if not k.endswith('rows')}, indent=1))
for key in ('C2_remainder_rows', 'C3_tie_rows', 'C4_centre_rows', 'C5_exactCS_rows'):
    print(key)
    for r in out[key]:
        print(r)
import pandas as pd
print(pd.DataFrame(out['C1_rn_rows']).drop(columns=['seed']).groupby(['kind', 'n', 'p']).agg('max').round(3).to_string())
