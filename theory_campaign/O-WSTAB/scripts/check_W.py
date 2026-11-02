"""O-WSTAB REPORT checks (exact enumeration, p <= 16, seed 20261102).

(1) ell-form of T13 with V = Omega: log(1+chi2(q_v||q_u)) = ell(u) + ell(w) - 2 ell(v), ell(phi) = -log q_phi(S0),
    and the sandwich ell(w) - 2 ell* <= log(1+chi2) <= ell(w) + ell*  for 0 <= u < v <= 1 (Prop L).
(2) Lemma W2 exact sandwich under BO: kappa*G <= LR <= kappa*G/(1-y).
(3) Lemma SEP (ORTH, any partition, w in [0,2]): ell(w) <= sum_{j in S0} log(1 + 2 p sqrt(n) e^{-nu x_j})
    - (s0+1) log(1 - q(w)),  q(w) = p^{-1} n^{-1/2} sum_{j notin S0} exp(beta(w) nu x_j).
(4) Ideal-grid stage count vs the deterministic sandwich of Prop G.
(5) Multi-extra lower bound (Prop W-div): ell(w) >= log of the exact single term for E = top-k nulls.
"""
import math
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import wstab_core as wc  # noqa: E402

rng = np.random.default_rng(20261102)
C_ACC = math.log(10 / 9)


def ell(P, phi, iS0):
    return -P.logq(phi)[iS0]


def ideal_grid(P, tol=1e-10):
    """From u take the largest v <= 1 with rho_Omega(u, v) >= 0.9 (bisection on the accept set; we scan then bisect)."""
    u, T, grid = 0.0, 0, [0.0]
    while u < 1 - 1e-12 and T < 200:
        if P.log1pchi2(u, 1.0) <= C_ACC:
            v = 1.0
        else:
            # largest accepted v: scan fine grid from the top, then bisect
            vs = np.linspace(u, 1, 2001)[1:]
            acc = [P.log1pchi2(u, v) <= C_ACC for v in vs]
            idx = max(i for i, a in enumerate(acc) if a) if any(acc) else None
            if idx is None:
                lo, hi = u, vs[0]
            else:
                lo, hi = vs[idx], (vs[idx + 1] if idx + 1 < len(vs) else 1.0)
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if P.log1pchi2(u, mid) <= C_ACC:
                    lo = mid
                else:
                    hi = mid
            v = lo
        grid.append(v)
        u, T = v, T + 1
    return T, grid


def gpm(P, iS0, lstar):
    """g_- = sup{g: ell(1+g) <= c - lstar}, g_+ = sup{g: ell(1+g) <= c + 2 lstar} (scan on [1, 3])."""
    ws = np.linspace(1, 3, 4001)
    L = np.array([ell(P, w, iS0) for w in ws])
    def sup_le(t):
        ok = np.where(L <= t)[0]
        # first crossing after which ell stays above t (ell convex => sublevel set is an interval)
        return ws[ok.max()] - 1 if len(ok) else 0.0
    return sup_le(C_ACC - lstar), sup_le(C_ACC + 2 * lstar)


def orth_problem(p, n, theta, sigma, B):
    Sigma = np.eye(p)
    R, r, ex = wc.suff_exact_gram(Sigma, theta, n, sigma, rng)
    blocks = [list(range(i, min(p, i + B))) for i in range(0, p, B)]
    return wc.Problem(R, r, n, blocks=blocks), ex


def x_single(P):
    """Under ORTH: x_j = t_j / Qbar for singletons."""
    Q0 = 2 * wc.B0 + (P.n - 1.0)
    out = np.zeros(P.p)
    for j in range(P.p):
        _, t = wc.score_parts(np.array([[j]]), P.R, P.r, P.n)
        out[j] = t[0] / Q0
    return out


def main():
    lines = []
    out = lambda s: (print(s), lines.append(s))

    # ---------------- (1),(3),(4),(5): ORTH designs
    worst1, worst_sep, sep_n = 0.0, -np.inf, 0
    out("ORTH runs: p, n, B, s0, R2pop | ell(0) ell(1) ell(2) | SEP bound at w=2 | T_ideal [T_lo, T_hi] | multi-extra LB at w=2")
    for (p, n, B, th) in [(14, 200, 4, [1.0, 0.8]), (14, 800, 4, [1.0, 0.8]), (16, 3200, 4, [0.6, 0.6, 0.6]),
                          (16, 400, 4, [0.3, 0.3]), (16, 20000, 4, [1.0, 1.0, 1.0]), (12, 100, 3, [1.5]),
                          (16, 1000, 4, [2.0, 2.0])]:
        theta = np.zeros(p)
        S0 = list(range(len(th)))           # truths in block 0 (and 1 if s0 > B)
        theta[S0] = th
        # spread truths over blocks: put truth k at column k*B
        theta = np.zeros(p)
        S0 = [k * B for k in range(len(th))]
        theta[S0] = th
        P, ex = orth_problem(p, n, theta, 1.0, B)
        iS0 = P.space.idx(S0)
        # (1) ell identity and sandwich
        lstar = max(ell(P, 0.0, iS0), ell(P, 1.0, iS0))
        for _ in range(200):
            u, v = np.sort(rng.uniform(0, 1, 2))
            w = 2 * v - u
            lhs = P.log1pchi2(u, v)
            rhs = ell(P, u, iS0) + ell(P, w, iS0) - 2 * ell(P, v, iS0)
            worst1 = max(worst1, abs(lhs - rhs))
            assert ell(P, w, iS0) - 2 * lstar - 1e-9 <= lhs <= ell(P, w, iS0) + lstar + 1e-9
        # (3) separable bound
        x = x_single(P)
        nu = wc.A0 + n / 2.0
        s = x[S0].sum()
        N = [j for j in range(p) if j not in S0]
        ubar = x[N].sum() / (1 - s)
        for w in np.linspace(0, 2, 21):
            beta = (1 / ((1 - s) * (1 - ubar))) if w <= 1 else (w / ((1 - s) * (1 - ubar)) - (w - 1))
            q = np.sum(np.exp(beta * nu * x[N] - 0.5 * math.log(n))) / p
            if ubar < 1 and q < 1:
                bound = np.sum(np.log1p(2 * p * math.sqrt(n) * np.exp(-nu * x[S0]))) - (len(S0) + 1) * math.log1p(-q)
                gap = ell(P, w, iS0) - bound
                worst_sep = max(worst_sep, gap)
                sep_n += 1
        w = 2.0
        beta2 = 2 / ((1 - s) * (1 - ubar)) - 1
        q2 = np.sum(np.exp(beta2 * nu * x[N] - 0.5 * math.log(n))) / p
        sep2 = (np.sum(np.log1p(2 * p * math.sqrt(n) * np.exp(-nu * x[S0]))) - (len(S0) + 1) * math.log1p(-q2)) if q2 < 1 else float("inf")
        # (4) grid
        T, grid = ideal_grid(P)
        gm, gp = gpm(P, iS0, lstar)
        Tlo = math.ceil(math.log2(1 + 1 / gp)) if gp > 0 else None
        Thi = math.ceil(math.log2(1 + 1 / gm)) if gm > 0 else None
        cond = 3 * lstar < C_ACC
        # (5) multi-extra lower bound: E = top-k nulls in truth-free blocks
        sig_blocks = {j // B for j in S0}
        N0 = [j for j in N if (j // B) not in sig_blocks]
        order = sorted(N0, key=lambda j: -x[j])
        best = -np.inf
        for k in range(1, len(order) + 1):
            S = sorted(S0 + order[:k])
            if len(S) > P.K:
                break
            best = max(best, -(P.logq(2.0)[iS0] - P.logq(2.0)[P.space.idx(S)]))
        lb5 = math.log1p(math.exp(best)) if best < 700 else best
        R2 = ex["mumu"] / (ex["mumu"] + (n - 1))
        out(f"p={p} n={n} B={B} s0={len(S0)} R2={R2:.3f} | ell0={ell(P,0,iS0):.3g} ell1={ell(P,1,iS0):.3g} ell2={ell(P,2,iS0):.4g}"
            f" | SEP2={sep2:.4g} | T={T} [{Tlo},{Thi}] (3l*<c: {cond}) | LB5={lb5:.4g}")
        if cond and Tlo is not None and Thi is not None:
            assert Tlo <= T <= Thi, (T, Tlo, Thi)
        assert lb5 <= ell(P, 2, iS0) + 1e-9
    out(f"(1) max |log(1+chi2) - [ell(u)+ell(w)-2ell(v)]| = {worst1:.2e}; sandwich held in all 1400 draws")
    out(f"(3) SEP lemma: max over {sep_n} (design, w) of ell(w) - bound = {worst_sep:.3g} (must be <= 0)")

    # ---------------- (2) W2 under BO with within-block correlation
    worst2 = 0.0
    cnt = 0
    for rep in range(6):
        p, B, n = 12, 4, [150, 400, 1600][rep % 3]
        Sigma = np.eye(p)
        for b in range(3):
            A = rng.uniform(-0.5, 0.5, (B, B))
            M = A @ A.T + np.eye(B)
            d = np.sqrt(np.diag(M))
            Sigma[b * B:(b + 1) * B, b * B:(b + 1) * B] = M / np.outer(d, d)
        theta = np.zeros(p)
        theta[[0, 4]] = [0.8, -0.6]
        R, r, ex = wc.suff_exact_gram(Sigma, theta, n, 1.0, rng)
        blocks = [list(range(b * B, (b + 1) * B)) for b in range(3)]
        P = wc.Problem(R, r, n, blocks=blocks)
        Q0 = 2 * wc.B0 + (n - 1.0)
        nu = wc.A0 + n / 2.0
        g = lambda z: -math.log1p(-z)
        for Sref in [[0, 4], [0], [4, 5], [1, 9]]:
            xbar = P.t[P.space.idx(Sref)] / Q0
            for l in range(p):
                if l in Sref:
                    continue
                b = l // B
                T_ = [j for j in Sref if j // B == b]
                xT = P.t[P.space.idx(T_)] / Q0
                delta = P.t[P.space.idx(sorted(T_ + [l]))] / Q0 - xT
                kappa = (xbar - xT) / (1 - xT)
                y = delta / (1 - xbar)
                G = nu * g(y)
                LR = P.d[P.space.idx(sorted(Sref + [l]))] - P.d[P.space.idx(Sref)]
                lo, hi = kappa * G, kappa * G / (1 - y)
                assert lo - 1e-9 <= LR <= hi + 1e-9, (LR, lo, hi)
                worst2 = max(worst2, (LR - lo) / max(hi - lo, 1e-300) if hi > lo else 0)
                cnt += 1
    out(f"(2) W2 sandwich kappa*G <= LR <= kappa*G/(1-y): held in {cnt} comparisons (BO, correlated blocks)")

    with open(__file__.replace("scripts", "results").replace("check_W.py", "check_W.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
