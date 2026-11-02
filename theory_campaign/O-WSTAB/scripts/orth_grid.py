"""Theorem W' check at large (n, p) under ORTH (seed 20261102).

ell(w) = -log q_w(S0) is not computable exactly at these sizes, but it is sandwiched:
  LB(w) <= ell(w) <= SEP(w)
(LB: exact single-chain term, E = top-k nulls of truth-free blocks, max over k; SEP: Lemma SEP, with the nulls
beyond the top K0 replaced by their conditional expectation -- the only approximation).  Prop G then gives
  g_-  >= sup{g : SEP(1+g') <= c - lstar_ub for all g' <= g},
  g_+  <= inf{g : LB(1+g) > c + 2 lstar_ub},          lstar_ub := max(SEP(0), SEP(1)),
and  ceil(log2(1+1/g_+)) <= T_ideal <= ceil(log2(1+1/g_-))  whenever 2 lstar_ub < c.
Prediction (Theorem W'): T_ideal = 1 if 2 A r < 1, = 2 if 2 A r > 1.
"""
import math

import numpy as np
from scipy import integrate, stats

rng = np.random.default_rng(20261102)
A0 = B0 = 0.01
C_ACC = math.log(10 / 9)


def g(z):
    return -np.log1p(-z)


def draw(n, p, theta, sigma=1.0, K0=20000):
    s0 = len(theta)
    m = p - s0
    K0 = min(K0, m)
    if m <= 200000:
        Z2top = np.sort(rng.chisquare(1, size=m))[::-1][:K0]
    else:
        G = np.cumsum(rng.exponential(size=K0))
        Z2top = stats.chi2.isf(G / (m + rng.normal(0, math.sqrt(m))), 1)
    sumZ2 = m + math.sqrt(2 * m) * rng.normal()
    Zt = rng.normal(size=s0)
    nm1 = n - 1.0
    chi_res = max(nm1 - p, 0.0) + (math.sqrt(2 * (nm1 - p)) * rng.normal() if nm1 - p > 1 else 0.0)
    YtY = nm1 * np.sum(theta ** 2) + 2 * math.sqrt(nm1) * sigma * np.sum(theta * Zt) + sigma ** 2 * (sumZ2 + np.sum(Zt ** 2) + chi_res)
    sy2 = YtY / nm1
    Qb = 2 * B0 + nm1
    nu = A0 + n / 2.0
    xt = ((nm1 * theta + sigma * math.sqrt(nm1) * Zt) ** 2 / sy2) / (n * Qb)
    cnull = sigma ** 2 * nm1 / (sy2 * n * Qb)
    return dict(n=n, p=p, m=m, K0=K0, s0=s0, Z2top=Z2top, tau=Z2top[-1], sumZ2=sumZ2, xt=xt, cnull=cnull, nu=nu)


def LB(D, w):
    n, p, s0, nu = D["n"], D["p"], D["s0"], D["nu"]
    s = D["xt"].sum()
    xtop = D["cnull"] * D["Z2top"]
    XE = np.cumsum(xtop)
    ii = np.arange(len(xtop), dtype=float)
    logprior = np.cumsum(np.log((s0 + ii + 1) / (2.0 * p - 1 - s0 - ii)))
    k = ii + 1
    with np.errstate(invalid="ignore"):
        lr = logprior - 0.5 * k * math.log(n) + w * nu * g(XE / (1 - s)) - (w - 1) * nu * np.cumsum(g(xtop))
    lr[XE >= 1 - s] = -np.inf
    return float(np.logaddexp(0, lr.max()))


def SEP(D, w):
    n, p, s0, nu, m, K0 = D["n"], D["p"], D["s0"], D["nu"], D["m"], D["K0"]
    s = D["xt"].sum()
    ubar = D["cnull"] * D["sumZ2"] / (1 - s)
    if ubar >= 1:
        return float("inf")
    beta = 1 / ((1 - s) * (1 - ubar)) if w <= 1 else w / ((1 - s) * (1 - ubar)) - (w - 1)
    c1 = beta * nu * D["cnull"]
    top = np.sum(np.exp(c1 * D["Z2top"] - 0.5 * math.log(n)))
    zt = math.sqrt(D["tau"])
    Ein = integrate.quad(lambda z: 2 * math.exp((c1 - 0.5) * z * z) / math.sqrt(2 * math.pi), 0, zt, limit=400)[0]
    Ein /= stats.chi2.cdf(D["tau"], 1)
    q = (top + max(m - K0, 0) * Ein / math.sqrt(n)) / p
    if q >= 1:
        return float("inf")
    trunc = float(np.sum(np.log1p(2 * p * math.sqrt(n) * np.exp(-nu * D["xt"]))))
    return trunc - (s0 + 1) * math.log1p(-q)


def main():
    th = np.array([3 / math.sqrt(2), 3 / math.sqrt(2)])     # r = 0.9
    r = 0.9
    gs = np.linspace(0, 1, 201)
    lines = [f"{'log10 n':>7} {'A':>5} {'2Ar':>5} {'lstar_ub':>9} {'g- >=':>7} {'g+ <=':>7} {'G_n':>6} {'T in':>8} {'pred':>4}"]
    print(lines[0])
    for A in (0.3, 0.45, 0.65, 0.8, 0.95):
        for e in (8, 12, 16):
            n = 10 ** e
            p = int(n ** A)
            D = draw(n, p, th)
            lst = max(SEP(D, 0.0), SEP(D, 1.0))
            sep = np.array([SEP(D, 1 + x) for x in gs])
            lb = np.array([LB(D, 1 + x) for x in gs])
            okm = sep <= C_ACC - lst
            gm = gs[np.argmin(okm)] - gs[1] if not okm.all() else 1.0   # last g with SEP <= thr on the whole prefix
            if not okm[0]:
                gm = 0.0
            over = np.where(lb > C_ACC + 2 * lst)[0]
            gp = gs[over[0]] if len(over) else float("inf")
            Tlo = max(1, math.ceil(math.log2(1 + 1 / gp))) if gp > 0 else None
            Thi = math.ceil(math.log2(1 + 1 / gm)) if gm > 0 else None
            Gn = math.log(n) / (2 * r * math.log(p))
            pred = 1 if 2 * A * r < 1 else 2
            valid = 2 * lst < C_ACC
            Tin = f"[{Tlo},{Thi}]" if valid else "n/a"
            row = f"{e:7d} {A:5.2f} {2*A*r:5.2f} {lst:9.2e} {gm:7.3f} {gp:7.3f} {Gn:6.3f} {Tin:>8} {pred:4d}"
            print(row); lines.append(row)
    with open(__file__.replace("scripts", "results").replace(".py", ".txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
