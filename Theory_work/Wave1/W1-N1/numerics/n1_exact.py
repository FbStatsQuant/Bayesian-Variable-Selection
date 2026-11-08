"""W1-N1 exact companion: E[W_r H_r(h)] versus pi(h) on production-extracted kernels.

Input: a directory written by `cpp/n1_harness_v2.exe export <id> <dir>` (production scores, pi0 law from the production
sampler tables, a pilot-derived grid (production pilot + production build_grid on an enumerated V), and the kernel matrices
of the production elementary steps at each phi, extracted by scripted uniforms and bisection).

Exact computations (no Monte Carlo):
  * round kernel R_phi = average over all orders of the m = p + B + 2 labelled steps (the B neighbour-swap labels are
    the same kernel), by a multiset DP over (subset of distinct labels, number of N labels used);
  * the frozen island I(c) with N = 1 and N = 2 particles: exact law of the population weighted by W = Zhat/Z
    (mixture-of-products recursion for multinomial resampling), L burn-in + 4 measured rounds at phi = 1;
  * E[W H(h)], E[W], E[H(h)] (normalised, to show the bias), for a list of h; negative controls.
Usage: py -3.13 n1_exact.py <dir> [<dir> ...]   (writes <dir>/exact_results.json and prints a summary)
"""
import json
import math
import sys
from itertools import combinations

import numpy as np


def load(dirn):
    meta = {}
    for line in open(f"{dirn}/meta.txt"):
        k, *v = line.split()
        meta[k] = v
    p = int(meta["p"][0]); M = int(meta["M"][0])
    om = np.genfromtxt(f"{dirn}/omega.tsv", delimiter="\t", names=True)
    phis = [(int(a), float(b)) for a, b, *_ in (l.split() for l in open(f"{dirn}/phis.txt"))]
    K = {}
    for ip, phi in phis:
        K[phi] = np.fromfile(f"{dirn}/K_{ip}.bin", dtype=np.float64).reshape(p + 3, M, M)
    return meta, om, K


def apply_round(V, Ks, p, B):
    """V @ R_phi, R_phi = average over uniform orders of the multiset {G_0..G_{p-1}, U, I} + B copies of N.
    Exact finite sum by a DP over (subset of distinct labels used, number of N labels used); rows of V propagate
    independently, so V may be a single row vector (cheap) or the identity (full kernel)."""
    distinct = list(range(p)) + [p, p + 2]   # Gibbs j, U, I
    D = len(distinct); KN = Ks[p + 1]
    total = D + B
    narr = math.factorial(total) // math.factorial(B)   # number of distinct arrangements of the multiset
    layer = {(0, 0): np.array(V, dtype=float)}
    for _ in range(total):
        new = {}
        for (mask, c), A in layer.items():
            for t, lab in enumerate(distinct):
                if mask & (1 << t):
                    continue
                key = (mask | (1 << t), c); v = A @ Ks[lab]
                new[key] = new[key] + v if key in new else v
            if c < B:
                key = (mask, c + 1); v = A @ KN
                new[key] = new[key] + v if key in new else v
        layer = new
    return layer[((1 << D) - 1, B)] / narr


class Rounds:
    """Round kernels per phi: full matrix when |Omega| <= FULL_MAX, otherwise applied to vectors by the DP."""
    FULL_MAX = 130

    def __init__(self, K, p, B):
        self.K, self.p, self.B = K, p, B
        self.M = next(iter(K.values())).shape[1]
        self.full = {}

    def matrix(self, phi):
        if phi not in self.full:
            self.full[phi] = apply_round(np.eye(self.M), self.K[phi], self.p, self.B)
        return self.full[phi]

    def right(self, V, phi):          # V @ R_phi
        if self.M <= self.FULL_MAX:
            return V @ self.matrix(phi)
        return apply_round(V, self.K[phi], self.p, self.B)


def lse(x):
    m = np.max(x); return m + math.log(np.sum(np.exp(x - m)))


def island_exact(RD, phis, G, w0, v0, phi_term, L, Nm=4):
    """Return per measured round q: (E[W eta_q], E[eta_q]) as functions h -> value, for N = 1 and N = 2.
    R: list of stage round kernels (stages 1..T); G: list of stage potentials; Rterm: kernel for burn-in/measured."""
    out = {}
    # N = 1: rows = (weighted measure mu, unweighted law nu)
    X = np.vstack([w0 * v0, v0])
    for ph, Gt in zip(phis, G):
        X = RD.right(np.vstack([X[0] * Gt, X[1]]), ph)   # Zhat_t = Zhat_{t-1} G_t(X_{t-1}) when N = 1
    for _ in range(L):
        X = RD.right(X, phi_term)
    m1 = []
    for _ in range(Nm):
        X = RD.right(X, phi_term)
        m1.append((X[0].copy(), X[1].copy()))
    out[1] = m1
    if RD.M > RD.FULL_MAX:
        return out
    R = [RD.matrix(ph) for ph in phis]; Rterm = RD.matrix(phi_term)
    # N = 2: weighted pair measure mu2 (E[W; pair = (x1, x2)]) and unweighted pair law P2
    mu2 = w0 * np.outer(v0, v0); P2 = np.outer(v0, v0)
    for Rt, Gt in zip(R, G):
        S = Gt[:, None] + Gt[None, :]
        for which in (0, 1):
            X = mu2 if which == 0 else P2
            c = X / (2.0 * S) if which == 0 else X / (S * S)
            Bm = np.diag(Gt ** 2 * (c.sum(1) + c.sum(0))) + np.outer(Gt, Gt) * (c + c.T)
            Y = Rt.T @ Bm @ Rt
            if which == 0: mu2 = Y
            else: P2 = Y
    for _ in range(L):
        mu2 = Rterm.T @ mu2 @ Rterm; P2 = Rterm.T @ P2 @ Rterm
    m2 = []
    for _ in range(Nm):
        mu2 = Rterm.T @ mu2 @ Rterm; P2 = Rterm.T @ P2 @ Rterm
        # marginal of eta = (delta_x1 + delta_x2)/2
        m2.append((0.5 * (mu2.sum(1) + mu2.sum(0)), 0.5 * (P2.sum(1) + P2.sum(0))))
    out[2] = m2
    return out


def h_list(meta, om, p, M):
    masks = om["mask"].astype(np.int64); sizes = om["size"]; K = int(meta["K"][0])
    S0 = [int(x) for x in meta["S0"]]
    s0mask = sum(1 << j for j in S0)
    H = {}
    def inc(js): return np.array([1.0 if all((m >> j) & 1 for j in js) else 0.0 for m in masks])
    edges = [tuple(int(x) for x in e.split("-")) for e in meta.get("edges", [])]
    for e in edges[:2]:
        H[f"joint{e[0]}-{e[1]}(edge)"] = inc(e)
    H[f"joint{S0[0]}-{S0[1]}(true pair)"] = inc((S0[0], S0[1]))
    H[f"marg{S0[0]}"] = inc((S0[0],))
    H["1{S!=S0}"] = np.array([0.0 if m == s0mask else 1.0 for m in masks])
    H["size/K"] = sizes / K
    d = om["d"]; H["d_norm"] = (d - d.min()) / (d.max() - d.min()) if d.max() > d.min() else np.zeros(M)
    rng = np.random.default_rng(int(meta["id"][0]) + 12345)
    H["random_U01"] = rng.uniform(size=M)
    return H, s0mask


def basis(M):
    return {f"1{{S=s{a}}}": np.eye(M)[a] for a in range(M)}


def run(dirn):
    meta, om, K = load(dirn)
    p = int(meta["p"][0]); M = int(meta["M"][0]); B = int(meta["B"][0]); L = int(meta["L"][0])
    logm0 = float(meta["logm0"][0]); logZbar0 = float(meta["logZbar0"][0])
    F = om["F"]; d = om["d"]; lg0 = om["lg0"]
    logZ = lse(F); pi = np.exp(F - logZ)
    v0 = np.exp(om["logpi0_prod"]); v0_spec = np.exp(lg0 - logZbar0)
    w0 = math.exp(logm0 + logZbar0 - logZ)
    res = {"dir": dirn, "p": p, "n": int(meta["n"][0]), "M": M, "B": B, "L": L,
           "pi0_prod_vs_spec_maxrel": float(np.max(np.abs(v0 / v0_spec - 1))),
           "gamma1_check_maxabs": float(np.max(np.abs((lg0 + d) - (F - logm0))))}
    RD = Rounds(K, p, B)
    for phi in K:
        q = np.exp(lg0 + phi * d - lse(lg0 + phi * d))
        chk = {"invariance_err": float(np.max(np.abs(RD.right(q[None, :], phi)[0] - q))),
               # max_x |sum_y R[x,y] - 1|: R 1 = (1^T R^T)^T and R^T is the order average of the transposed kernels
               # (reversal is a bijection of the uniform order law), so the DP on transposed kernels gives every row sum.
               "row_sum_err": float(np.max(np.abs(apply_round(np.ones((1, M)), np.transpose(K[phi], (0, 2, 1)), p, B)[0] - 1)))}
        if M <= Rounds.FULL_MAX:
            R = RD.matrix(phi)
            chk["row_sum_err"] = float(np.max(np.abs(R.sum(1) - 1)))
            chk["detailed_balance_err"] = float(np.max(np.abs(q[:, None] * R - (q[:, None] * R).T)))
        res.setdefault("round_checks", {})[f"{phi:.6g}"] = chk
    H, s0mask = h_list(meta, om, p, M)
    Hb = basis(M)
    grids = {"pilot-derived": [float(x) for x in meta["grid"]], "T=1 {0,1}": [0.0, 1.0], "{0,.5,1}": [0.0, 0.5, 1.0]}
    res["grids"] = grids
    piS0 = float(pi[list(om["mask"].astype(int)).index(s0mask)]) if s0mask in set(om["mask"].astype(int)) else 0.0
    res["delta1"] = 1 - piS0
    res["cases"] = {}
    def case(name, grid, Rterm_phi=1.0, truncate=False, Lc=None):
        g = grid[:-1] if truncate else grid
        Gs = [np.exp((g[t] - g[t - 1]) * d) for t in range(1, len(g))]
        out = island_exact(RD, list(g[1:]), Gs, w0, v0, Rterm_phi, L if Lc is None else Lc)
        rec = {}
        for Np in sorted(out):
            per = out[Np]
            EW = float(per[0][0].sum())
            rows = {}
            for hn, h in H.items():
                ewh_q = [float(m @ h) for m, _ in per]
                eh_q = [float(u @ h) for _, u in per]
                rows[hn] = {"pi_h": float(pi @ h), "EWH": float(np.mean(ewh_q)), "EWH_per_q": ewh_q,
                            "abs_err": float(abs(np.mean(ewh_q) - pi @ h)),
                            "EH_normalised": float(np.mean(eh_q)), "bias_normalised": float(np.mean(eh_q) - pi @ h)}
            # every basis indicator, separately for each measured round q (N1-q coordinatewise)
            basis_res = max(float(np.max(np.abs(m - pi))) for m, _ in per)
            rec[f"N={Np}"] = {"EW": EW, "h": rows, "basis_max_abs_err_all_q": basis_res,
                              "max_abs_err_per_q": [max(abs(r["EWH_per_q"][q] - r["pi_h"]) for r in rows.values()) for q in range(4)],
                              "max_abs_err": max(r["abs_err"] for r in rows.values()),
                              "max_abs_bias_normalised": max(abs(r["bias_normalised"]) for r in rows.values())}
        res["cases"][name] = rec
    for gname, g in grids.items():
        case(f"N1 grid={gname}", g)
    # stress (L = 0 is in the locked domain L >= 0): measured rounds start right after the bridge
    case("N1 L=0 grid=T=1 {0,1} (stress: largest normalised bias)", grids["T=1 {0,1}"], Lc=0)
    case("N1 L=0 grid=pilot-derived (stress)", grids["pilot-derived"], Lc=0)
    # negative controls
    case("NC1 measured+burn-in at phi=0.5 (kernel not pi-invariant), pilot-derived grid", grids["pilot-derived"], Rterm_phi=0.5)
    if len(grids["pilot-derived"]) > 2:
        case("NC2 bridge stopped before the last reweighting (pilot-derived grid minus phi_T)", grids["pilot-derived"], truncate=True)
    else:
        case("NC2 bridge stopped before the last reweighting (d7 exception: its pilot-derived grid has one interval, so the {0,.5,1} grid minus 1 is used)", grids["{0,.5,1}"], truncate=True)
    # enforce the declared tolerances (fail loudly rather than report)
    for cn, c in res["cases"].items():
        for k, v in c.items():
            worst = max(v["max_abs_err"], v["basis_max_abs_err_all_q"], max(v["max_abs_err_per_q"]))
            if cn.startswith("NC"):
                assert worst > 1e-6, f"negative control not detected: {dirn} {cn} {k} {worst}"
            else:
                assert worst <= 1e-10 and abs(v["EW"] - 1) <= 1e-10, f"N1 residual above tolerance: {dirn} {cn} {k} {worst}"
    for ph, chk in res["round_checks"].items():
        assert chk["row_sum_err"] <= 1e-12 and chk["invariance_err"] <= 1e-12, f"round check failed {dirn} {ph}"
    with open(f"{dirn}/exact_results.json", "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    for dn in sys.argv[1:]:
        r = run(dn)
        print(f"== {dn}: n={r['n']} p={r['p']} |Omega|={r['M']} B={r['B']} L={r['L']} grid={r['grids']['pilot-derived']} delta1={r['delta1']:.4g}")
        print(f"   pi0 prod vs spec maxrel {r['pi0_prod_vs_spec_maxrel']:.2e}; round checks (max over phi): "
              f"rows {max(v['row_sum_err'] for v in r['round_checks'].values()):.1e} inv {max(v['invariance_err'] for v in r['round_checks'].values()):.1e} "
              f"DB {max(v.get('detailed_balance_err', float('nan')) for v in r['round_checks'].values()):.1e}")
        for cn, c in r["cases"].items():
            s = "; ".join(f"{k}: |E[W H]-pi(h)|max={v['max_abs_err']:.2e} basis(all q)={v['basis_max_abs_err_all_q']:.2e} E[W]-1={v['EW']-1:.1e} |normalised bias|max={v['max_abs_bias_normalised']:.2e}" for k, v in c.items())
            print(f"   {cn}: {s}")
