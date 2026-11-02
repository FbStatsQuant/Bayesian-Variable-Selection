"""N1: exact checks of the deterministic statements WS1-WS5 (PROOF.md) on small designs.

Checks (each prints its max absolute error):
  (1) pi0 and pi from the vectorised code equal brute-force definitions (00_COMMON) on p = 8.
  (2) WS1(a) singleton identity 1 + chi2(q_v||q_u) = q_v(S)^2/(q_u(S) q_w(S)) for every S, several (u, v).
  (3) WS1(c) KL(q_v||q_u) = int_u^v (t-u) Var_{q_t}(d) dt; log(1+chi2) = int_u^w (Delta-|t-v|) Var_{q_t}(d) dt.
  (4) WS1(b) Renyi singleton identity exp((a-1) D_a(pi||pi0)) = pi(S)^a pi0(S)^(1-a) / q_a(S).
  (5) WS1(d) set bounds  q_v(A)^2/q_u(A) <= 1+chi2 <= cosh^2(Delta osc_A d / 2) q_v(A)^2/(q_u(A) q_w(A)).
  (6) WS3 (BO): d == d_sigma (explicit formula), d >= 0, mean-field representation by quadrature.
  (7) WS4: |d - d_sigma| <= eta_S whenever eps_S < 1 and xbar_S < 1 - eps_S (non-BO design).
  (8) WS5(a): delta_{U*\\l, l} = theta_tilde_l * ||(I - P_{U*\\l}) x_l||  (random design, X explicit).
Seed fixed: 20261102.
"""
import itertools
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from wstab_core import (A0, B0, Problem, cross_eps, gen_random_design, leakage, log_w, lse,
                        suff_exact_gram)

rng = np.random.default_rng(20261102)
out = []


def rep(name, val):
    out.append(f"{name}: {val:.3e}")
    print(out[-1], flush=True)


# ---------------- (1) brute force on p = 8, random correlated design
p, n = 8, 60
Sig = 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
beta = np.zeros(p); beta[[1, 4, 6]] = [1.0, -0.8, 0.6]
R, r, ex = gen_random_design(Sig, beta, n, 1.0, rng)
P = Problem(R, r, n, blocks=[[0, 1, 2], [3, 4, 5], [6, 7]])
nu = A0 + n / 2


def logm_direct(S):
    S = list(S)
    if not S:
        return -nu * math.log(2 * B0 + n - 1)
    G = (n - 1) * R[np.ix_(S, S)]
    z = (n - 1) * r[S]
    H = (n + 1) * G + np.eye(len(S))
    Q = (n - 1) - n * z @ np.linalg.solve(H, z)
    return -0.5 * (np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(S)))[1]) - nu * math.log(2 * B0 + Q)


err_pi, err_pi0 = 0.0, 0.0
lp = P.lw + P.logbf
lp = lp - lse(lp)
lp0 = P.lg0 - P.lZ0
bf = {}
for k in range(P.K + 1):
    for S in itertools.combinations(range(p), k):
        bf[S] = logm_direct(S) - logm_direct(())
vals0, vals = {}, {}
for S, l in bf.items():
    vals[S] = log_w(len(S), p) + l
    vals0[S] = log_w(len(S), p) + sum(bf[tuple(sorted(set(S) & set(C)))] for C in P.blocks)
Z, Z0 = lse(list(vals.values())), lse(list(vals0.values()))
for S in bf:
    i = P.space.idx(S)
    err_pi = max(err_pi, abs(vals[S] - Z - lp[i]))
    err_pi0 = max(err_pi0, abs(vals0[S] - Z0 - lp0[i]))
rep("(1) max |log pi - brute|", err_pi)
rep("(1) max |log pi0 - brute|", err_pi0)

# ---------------- (2) singleton identity
e2 = 0.0
for (u, v) in [(0, 1), (0, 0.3), (0.2, 0.7), (0.5, 1.0), (-0.4, 0.1)]:
    w = 2 * v - u
    lhs = P.log1pchi2(u, v)
    lqu, lqv, lqw = P.logq(u), P.logq(v), P.logq(w)
    rhs = 2 * lqv - lqu - lqw
    e2 = max(e2, float(np.max(np.abs(rhs - lhs))))
    # direct chi2
    qu, qv = np.exp(lqu), np.exp(lqv)
    e2 = max(e2, abs(math.log(np.sum(qv ** 2 / qu)) - lhs))
rep("(2) singleton identity, max |log err| over all S and 5 (u,v)", e2)

# ---------------- (3) integral formulas
def quad(f, a, b, m=4001):
    x = np.linspace(a, b, m)
    y = np.array([f(t) for t in x])
    return float(np.trapezoid(y, x))


e3 = 0.0
for (u, v) in [(0, 1), (0.3, 0.6)]:
    kl = P.kl(v, u)
    klq = quad(lambda t: (t - u) * P.var_d(t), u, v)
    e3 = max(e3, abs(kl - klq) / max(1e-12, abs(kl)))
    D = v - u
    w = 2 * v - u
    c2 = P.log1pchi2(u, v)
    c2q = quad(lambda t: (D - abs(t - v)) * P.var_d(t), u, w)
    e3 = max(e3, abs(c2 - c2q) / max(1e-12, abs(c2)))
rep("(3) relative error of KL and log(1+chi2) integral formulas (trapezoid, 4001 pts)", e3)

# ---------------- (4) Renyi singleton identity
e4 = 0.0
for a in [0.5, 1.5, 2.0, 3.0]:
    D = P.renyi(a, 1.0, 0.0)
    l1, l0, la = P.logq(1.0), P.logq(0.0), P.logq(a)
    rhs = a * l1 + (1 - a) * l0 - la
    e4 = max(e4, float(np.max(np.abs(rhs - (a - 1) * D))))
rep("(4) Renyi singleton identity", e4)

# ---------------- (5) set bounds
viol = 0
for trial in range(300):
    A = rng.random(len(P.d)) < rng.uniform(0.01, 0.5)
    if not A.any() or A.all():
        continue
    u, v = sorted(rng.uniform(-0.5, 1.2, 2))
    w = 2 * v - u
    D = v - u
    lc = P.log1pchi2(u, v)
    qu, qv, qw = (np.exp(P.logq(x)) for x in (u, v, w))
    lo = math.log(qv[A].sum() ** 2 / qu[A].sum() + qv[~A].sum() ** 2 / qu[~A].sum())
    osc = float(P.d[A].max() - P.d[A].min())
    hi = 2 * math.log(math.cosh(D * osc / 2)) + math.log(qv[A].sum() ** 2 / (qu[A].sum() * qw[A].sum()))
    if lo > lc + 1e-9 or lc > hi + 1e-9:
        viol += 1
rep("(5) set-bound violations in 300 random (A, u, v)", viol)

# ---------------- (6) block-orthogonal: d == d_sigma, d >= 0, mean field
p, n = 12, 80
blocks = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
Sig = np.eye(p)
for C in blocks:
    for a in C:
        for b in C:
            if a != b:
                Sig[a, b] = 0.6
theta = np.zeros(p); theta[[1, 5, 6, 10]] = [0.9, -0.7, 0.5, 1.1]
R, r, ex = suff_exact_gram(Sig, theta, n, 1.0, rng)
P = Problem(R, r, n, blocks=blocks)
nu = A0 + n / 2
Q0 = 2 * B0 + n - 1
xb = np.array([tb / Q0 for tb in P.t_blocks])          # (J, models)
dsig = nu * (np.log1p(-xb).sum(0) - np.log1p(-xb.sum(0)))
rep("(6) BO: max |d - d_sigma|", float(np.max(np.abs(P.d - dsig))))
rep("(6) BO: min d (should be >= 0)", float(np.min(P.d)))
# upper bound d_sigma <= nu sum_{b<c} x_b x_c / (1 - sum x)
pair = 0.5 * (xb.sum(0) ** 2 - (xb ** 2).sum(0))
ub = nu * pair / (1 - xb.sum(0))
rep("(6) BO: max (d_sigma - upper bound) (should be <= 0)", float(np.max(dsig - ub)))
# mean-field: BF(S) = E_lambda prod_b f_b, r_b = E_lambda f_b, tau = 1/sigma^2 ~ Gamma(nu, rate Q0/2)
from math import lgamma
rate = Q0 / 2
# quadrature in log tau around the mode
mode = (nu - 1) / rate
lt = np.linspace(math.log(mode) - 3.0, math.log(mode) + 6.0, 60001)
tt = np.exp(lt)
logdens = nu * math.log(rate) - lgamma(nu) + (nu - 1) * lt - rate * tt + lt   # density in log tau
lwq = logdens + math.log(lt[1] - lt[0])
e6 = 0.0
for i in rng.choice(len(P.d), 50, replace=False):
    t = P.t[i]
    mf = lse(lwq + t * tt / 2) - 0.5 * P.ldD[i]
    if not np.isfinite(mf):
        e6 = float('inf')
    e6 = max(e6, abs(mf - P.logbf[i]))
rep("(6) BO: mean-field log BF by quadrature vs exact (50 models)", e6)

# ---------------- (7) WS4 perturbation bound on a non-BO design
p, n = 12, 400
Sig2 = Sig.copy()
for a in range(p):
    for b in range(p):
        if a // 4 != b // 4:
            Sig2[a, b] = 0.05
R, r, ex = suff_exact_gram(Sig2, theta, n, 1.0, rng)
P = Problem(R, r, n, blocks=blocks)
nu = A0 + n / 2
Q0 = 2 * B0 + n - 1
xb = np.array([tb / Q0 for tb in P.t_blocks])
xbar = xb.sum(0)
viol, checked, worst = 0, 0, 0.0
for i, m in enumerate(P.space.masks):
    S = [j for j in range(p) if (int(m) >> j) & 1]
    eps = cross_eps(R, blocks, S)
    if eps >= 1 or xbar[i] >= 1 - eps:
        continue
    dsig = nu * (np.log1p(-xb[:, i]).sum() - math.log1p(-xbar[i]))
    eta = nu * eps * xbar[i] / ((1 - eps) * (1 - xbar[i] / (1 - eps))) + len(S) * eps ** 2 / (4 * (1 - eps))
    gap = abs(P.d[i] - dsig)
    checked += 1
    worst = max(worst, gap / eta if eta > 0 else 0.0)
    if gap > eta + 1e-9:
        viol += 1
rep(f"(7) WS4 violations over {checked} models", viol)
rep("(7) WS4 worst ratio |d - d_sigma| / eta", worst)

# ---------------- (8) leakage decomposition at the block-completing addition
p, n = 12, 300
Sig3 = Sig2.copy()
Sig3[1, 5] = Sig3[5, 1] = 0.45
R, r, ex = gen_random_design(Sig3, theta, n, 1.0, rng)
X, mu = ex["X"], ex["mu"]
leak = leakage(blocks, R, theta, [1, 5, 6, 10], n)
e8 = 0.0
for lb in leak:
    U = lb["U"]
    for i, l in enumerate(U):
        T = [j for j in U if j != l]
        if T:
            XT = X[:, T]
            res = X[:, l] - XT @ np.linalg.lstsq(XT, X[:, l], rcond=None)[0]
        else:
            res = X[:, l]
        u = res / np.linalg.norm(res)
        delta = float(u @ mu)
        pred = lb["theta_tilde"][i] * float(np.linalg.norm(res))
        e8 = max(e8, abs(delta - pred) / max(1.0, abs(delta)))
rep("(8) delta_{U*-l,l} vs theta_tilde * ||res|| (relative)", e8)

with open(sys.argv[1] if len(sys.argv) > 1 else "/dev/null", "w") as f:
    f.write("\n".join(out) + "\n")
