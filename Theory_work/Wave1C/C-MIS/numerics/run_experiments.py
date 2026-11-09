"""C-MIS falsification numerics N1-N5 (exact enumeration, p_C = 10 candidates, 20 seeds per n).

Usage: py -3.13 run_experiments.py [EXP ...]   (default: all). Writes <EXP>_results.json and <EXP>_summary.md here.
See PLAN.md (Numerics) and STATEMENT.md for what each experiment tests.
"""
import json
import math
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mis_core import exact_posterior, summarise, all_subsets  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
P = 10
NGRID = [100, 200, 400, 800, 1600, 3200, 6400]
SEEDS = range(20)


def equicorr(p, rho):
    return (1 - rho) * np.eye(p) + rho * np.ones((p, p))


def run(name, gen, targets, ngrid=NGRID, seeds=SEEDS, extra=None):
    """gen(n, rng) -> (Xr_C, yr, info). targets: dict name -> set (must contain 'S0C')."""
    rows = []
    subsets_cache = {}
    for n in ngrid:
        K = min(P, n // 2)
        if K not in subsets_cache:
            subsets_cache[K] = all_subsets(P, K)
        for s in seeds:
            rng = np.random.default_rng(100000 * n + s)
            Xr, yr, info = gen(n, rng, s)
            subs, post = exact_posterior(Xr, yr, subsets_cache[K])
            out = summarise(subs, post, P, targets)
            out.update({"n": n, "seed": s})
            out.update(info)
            rows.append(out)
    with open(os.path.join(HERE, name + "_results.json"), "w") as f:
        json.dump(rows, f)
    # summary table
    lines = [f"# {name} summary", "", "targets: " + ", ".join(f"{k}={sorted(v)}" for k, v in targets.items()), ""]
    keys = ["pi_" + k for k in targets]
    hdr = "| n | " + " | ".join(f"median {k}" for k in keys) + " | P(HPM=S0C) | " + \
        " | ".join(f"mean PIP_{j}" for j in range(P)) + " |"
    lines.append(hdr)
    lines.append("|" + "---|" * (2 + len(keys) + P))
    S0C = sorted(targets["S0C"])
    for n in ngrid:
        rs = [r for r in rows if r["n"] == n]
        med = [float(np.median([r[k] for r in rs])) for k in keys]
        phpm = np.mean([r["hpm"] == S0C for r in rs])
        pips = np.mean([r["pip"] for r in rs], axis=0)
        lines.append(f"| {n} | " + " | ".join(f"{m:.4f}" for m in med) + f" | {phpm:.2f} | " +
                     " | ".join(f"{q:.3f}" for q in pips) + " |")
    if extra:
        lines += ["", extra(rows)]
    with open(os.path.join(HERE, name + "_summary.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return rows


# ---------------- N1: jointly Gaussian rows, one omitted variable with three proxies ----------------
A_N1 = np.zeros(P); A_N1[[0, 1, 2]] = [0.6, 0.5, -0.4]


def gen_N1(n, rng, s, cancel=False, small=None):
    Xc = rng.multivariate_normal(np.zeros(P), equicorr(P, 0.3), size=n)
    a = A_N1.copy()
    if small is not None:
        a[5] = small
    xk = Xc @ a + rng.standard_normal(n)            # omitted variable; GR: x_k | x_C = linear + N(0,1)
    beta = np.zeros(P); beta[3] = 0.8; beta[4] = 0.6
    if cancel:
        beta[0] = -0.6                              # cancels gamma_0 = 0.6 * beta_k
    yr = 1.5 + Xc @ beta + 1.0 * xk + rng.standard_normal(n)
    # sample projection of omega = x_k on [1, X_C]: its support is dense
    Z = np.column_stack([np.ones(n), Xc])
    coef = np.linalg.lstsq(Z, xk, rcond=None)[0][1:]
    return Xc, yr, {"sample_proj_nnz_abs_gt_1e-8": int(np.sum(np.abs(coef) > 1e-8)),
                    "sample_proj_coef": coef.round(4).tolist()}


# ---------------- N1b: fixed candidate design, GR with random xi ----------------
_FIXED = {}


def gen_N1b(n, rng, s):
    if n not in _FIXED:
        _FIXED[n] = np.random.default_rng(999 + n).multivariate_normal(np.zeros(P), equicorr(P, 0.3), size=n)
    Xc = _FIXED[n]
    xk = Xc @ A_N1 + rng.standard_normal(n)
    beta = np.zeros(P); beta[3] = 0.8; beta[4] = 0.6
    yr = Xc @ beta + xk + rng.standard_normal(n)
    return Xc, yr, {}


# ---------------- N2: chain 0 - 1 - k in the precision graph ----------------
def chain_cov():
    # variables ordered (x_0, ..., x_9, x_k); precision: chain 0-1-k, everything else independent unit
    Th = np.eye(P + 1)
    Th[0, 1] = Th[1, 0] = -0.45
    Th[1, P] = Th[P, 1] = -0.45
    return np.linalg.inv(Th), Th


def gen_N2(n, rng, s):
    Sig, Th = chain_cov()
    W = rng.multivariate_normal(np.zeros(P + 1), Sig, size=n)
    Xc, xk = W[:, :P], W[:, P]
    beta = np.zeros(P); beta[5] = 0.7
    yr = Xc @ beta + 1.0 * xk + rng.standard_normal(n)
    return Xc, yr, {}


def n2_extra(rows):
    Sig, Th = chain_cov()
    gamma = np.linalg.solve(Sig[:P, :P], Sig[:P, P])
    corr0k = Sig[0, P] / math.sqrt(Sig[0, 0] * Sig[P, P])
    return (f"Population gamma = Sigma_CC^-1 Sigma_Ck = {gamma.round(6).tolist()}; "
            f"-Theta_Ck/Theta_kk = {(-Th[:P, P] / Th[P, P]).round(6).tolist()}; "
            f"marginal corr(x_0, x_k) = {corr0k:.4f} (nonzero, but x_0 is not a graph neighbour of k).")


# ---------------- N3: fixed design, exact projection (EP), dilution ----------------
_FIX3 = {}


def make_N3(n, Delta, c):
    key = (n, Delta, c)
    if key not in _FIX3:
        rg = np.random.default_rng(31337 + n)
        Xc = rg.multivariate_normal(np.zeros(P), equicorr(P, 0.3), size=n)
        b = np.zeros(P); b[3] = 0.8; b[4] = 0.6
        b[5] = math.sqrt(c * math.log(n) / n)       # weak signal at BM-ratio c w.r.t. sigma^2 = 1
        w = rg.standard_normal(n)
        Z = np.column_stack([np.ones(n), Xc])
        r = w - Z @ np.linalg.lstsq(Z, w, rcond=None)[0]   # r orthogonal to 1 and to every candidate column
        if Delta > 0:
            r *= math.sqrt(Delta * (n - 1) / float(r @ r))
        else:
            r[:] = 0.0
        _FIX3[key] = (Xc, Xc @ b + r, float(np.abs(Xc.T @ r).max()))
    return _FIX3[key]


def gen_N3(Delta, c):
    def g(n, rng, s):
        Xc, mu, orth = make_N3(n, Delta, c)
        yr = mu + rng.standard_normal(n)
        return Xc, yr, {"max_abs_XCt_r": orth}
    return g


# ---------------- N5: non-GR probes ----------------
def gen_N5(kind):
    def g(n, rng, s):
        Xc = rng.multivariate_normal(np.zeros(P), equicorr(P, 0.3), size=n)
        beta = np.zeros(P); beta[3] = 0.8; beta[4] = 0.6
        if kind == "square":
            om = 1.0 * (Xc[:, 0] ** 2 - 1.0)          # linear projection on x_C is 0 (Gaussian odd moments)
        else:  # product
            om = 1.0 * Xc[:, 0] * Xc[:, 1] - 0.3      # E = 0.3; linear projection on x_C is 0
        yr = Xc @ beta + om + rng.standard_normal(n)
        return Xc, yr, {}
    return g


if __name__ == "__main__":
    which = sys.argv[1:] or ["N1", "N1b", "N2", "N3", "N4", "N5"]
    S0C = {0, 1, 2, 3, 4}
    if "N1" in which:
        def n1_extra(rows):
            nn = [r["sample_proj_nnz_abs_gt_1e-8"] for r in rows]
            return f"Sample projection of x_k on [1, X_C]: number of nonzero coefficients min/max = {min(nn)}/{max(nn)} (of {P})."
        run("N1", gen_N1, {"S0C": S0C, "S0capC": {3, 4}, "S0C_minus2": {0, 1, 3, 4}}, extra=n1_extra)
    if "N1b" in which:
        run("N1b", gen_N1b, {"S0C": S0C, "S0capC": {3, 4}})
    if "N2" in which:
        run("N2", gen_N2, {"S0C": {1, 5}, "S0capC": {5}, "with0": {0, 1, 5}}, extra=n2_extra)
    if "N3" in which:
        for Delta in (0.0, 4.0):
            run(f"N3_Delta{int(Delta)}", gen_N3(Delta, 6.0), {"S0C": {3, 4, 5}, "no5": {3, 4}})
    if "N4" in which:
        run("N4_cancel", lambda n, rng, s: gen_N1(n, rng, s, cancel=True),
            {"S0C": {1, 2, 3, 4}, "with0": {0, 1, 2, 3, 4}})
        run("N4_small", lambda n, rng, s: gen_N1(n, rng, s, small=0.08),
            {"S0C": {0, 1, 2, 3, 4, 5}, "no5": {0, 1, 2, 3, 4}})
    if "N5" in which:
        run("N5_square", gen_N5("square"), {"S0C": {3, 4}, "with0": {0, 3, 4}})
        run("N5_product", gen_N5("product"), {"S0C": {3, 4}, "with01": {0, 1, 3, 4}})


# ---------------- N3b: EP with Delta = 4 and the weak signal rescaled to BM-ratio 6 w.r.t. sigma_C^2 = 5 ----------------
if __name__ == "__main__" and "N3b" in sys.argv[1:]:
    run("N3b_Delta4_c30", gen_N3(4.0, 30.0), {"S0C": {3, 4, 5}, "no5": {3, 4}})


# ---------------- N6: null projection (omitted signal independent of all candidates; no candidate truth) ----------------
def gen_N6(n, rng, s):
    Xc = rng.multivariate_normal(np.zeros(P), equicorr(P, 0.3), size=n)
    xk = rng.standard_normal(n)                      # independent of the candidates: gamma = 0
    yr = 2.0 + 1.0 * xk + rng.standard_normal(n)     # beta^C = 0, S0C = empty, sigma_C^2 = 2
    return Xc, yr, {}


# ---------------- N7: Example E1 (p_C = 3): omitted x_k = -x1 + x2 + z, y = x1 + x_k + eps ----------------
def run_N7():
    import itertools
    from mis_core import exact_posterior, summarise, all_subsets
    rows = []
    subs = all_subsets(3, 3)
    for n in NGRID:
        for s in SEEDS:
            rg = np.random.default_rng(700000 + 100 * n + s)
            X = rg.standard_normal((n, 3)); z = rg.standard_normal(n)
            xk = -X[:, 0] + X[:, 1] + z
            yr = X[:, 0] + xk + rg.standard_normal(n)
            sb, post = exact_posterior(X, yr, subs)
            out = summarise(sb, post, 3, {"S0C": {1}, "S0capC": {0}, "full": {0, 1, 2}})
            out.update({"n": n, "seed": s}); rows.append(out)
    json.dump(rows, open(os.path.join(HERE, "N7_results.json"), "w"))
    lines = ["# N7 summary (Example E1; candidate indices 0,1,2 = x1,x2,x3; S0C = {x2} = index 1)", "",
             "| n | median pi({x2}) | median pi({x1}) | median pi({x1,x2,x3}) | P(HPM={x2}) | mean PIP x1 | x2 | x3 |", "|---|---|---|---|---|---|---|---|"]
    for n in NGRID:
        rs = [r for r in rows if r["n"] == n]
        pip = np.mean([r["pip"] for r in rs], axis=0)
        lines.append(f"| {n} | {np.median([r['pi_S0C'] for r in rs]):.4f} | {np.median([r['pi_S0capC'] for r in rs]):.4f} | "
                     f"{np.median([r['pi_full'] for r in rs]):.4f} | {np.mean([r['hpm'] == [1] for r in rs]):.2f} | "
                     f"{pip[0]:.3f} | {pip[1]:.3f} | {pip[2]:.3f} |")
    open(os.path.join(HERE, "N7_summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__" and "N6" in sys.argv[1:]:
    run("N6_null", gen_N6, {"S0C": set(), "any1": {0}})
if __name__ == "__main__" and "N7" in sys.argv[1:]:
    run_N7()
