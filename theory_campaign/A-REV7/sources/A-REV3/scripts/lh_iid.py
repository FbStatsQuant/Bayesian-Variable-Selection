"""LH-iid: the linked-hub family with iid Gaussian rows, p >> n (W3-PXN, Theorem P).

Rows iid N(0, Sigma_LH): G groups of size g, within-group equicorrelation rho; c linked pairs (a_i, b_i) with
corr(j_a, j_b) = psi and C_a independent of C_b given the hub pair (rank-one cross covariance through the hubs);
v visible groups; all other groups null and independent.  Truth: theta_{j_a} = beta_i, theta_{j_b} = -psi beta_i,
theta_{j_h} = beta_h.  Reference S° = S0 minus the masked hubs M = {j_b}.

Usage: python3 lh_iid.py CONFIG   (CONFIG in A, B, P; see CONFIGS).  Seeds fixed per (config, n, p, rep).
Writes results/lh_<CONFIG>.jsonl (one JSON record per replicate).
"""
import json, math, sys, time
import numpy as np
from scipy.special import logsumexp
from scipy.stats import chi2
from pxn_core import *


def gen_lh(n, G, g, rho, psi, pairs, visible, rng, sigma=1.0):
    """pairs: list of (a, b, beta); visible: list of (h, beta). Hub = first member of each group."""
    p = G * g
    X = np.empty((n, p))
    linked_b = {b: (a, beta) for (a, b, beta) in pairs}
    for h in range(G):
        if h in linked_b:
            continue
        f = rng.standard_normal(n)
        X[:, h * g:(h + 1) * g] = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, g))
    for b, (a, beta) in linked_b.items():
        hub = psi * X[:, a * g] + math.sqrt(1 - psi ** 2) * rng.standard_normal(n)
        X[:, b * g] = hub
        f = rng.standard_normal(n)
        X[:, b * g + 1:(b + 1) * g] = (rho * hub[:, None] + math.sqrt(rho * (1 - rho)) * f[:, None]
                                       + math.sqrt(1 - rho) * rng.standard_normal((n, g - 1)))
    theta = np.zeros(p)
    M = []
    for (a, b, beta) in pairs:
        theta[a * g] = beta
        theta[b * g] = -psi * beta
        M.append(b * g)
    for (h, beta) in visible:
        theta[h * g] = beta
    y = X @ theta + sigma * rng.standard_normal(n)
    S0 = sorted(np.flatnonzero(theta).tolist())
    Sref = sorted(set(S0) - set(M))
    groups = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    return X, y, groups, S0, Sref, sorted(M)


CONFIGS = {
    # c = 1: one linked pair + one visible group; S3-like rho = 0.7, groups of 10
    "A": dict(g=10, rho=0.7, psi=0.5, pairs=[(0, 1, 1.0)], visible=[(2, 1.0)],
              grid=[(200, 750, 20), (400, 1790, 20), (800, 4260, 12), (1600, 10120, 6)]),
    # c = 2: two linked pairs (masked depth 2) + one visible group
    "B": dict(g=10, rho=0.7, psi=0.5, pairs=[(0, 1, 1.0), (2, 3, -1.0)], visible=[(4, 1.0)],
              grid=[(200, 750, 20), (400, 1790, 20), (800, 4260, 12), (1600, 10120, 6)]),
    # p sweep at the study size n = 200 (c = 1)
    "P": dict(g=10, rho=0.7, psi=0.5, pairs=[(0, 1, 1.0)], visible=[(2, 1.0)],
              grid=[(200, 500, 20), (200, 1000, 20), (200, 2000, 20), (200, 4000, 10)]),
}


def dvals(D, T, sets):
    lbf = log_bf_sets(D, sets)
    return lbf - np.array([T.log_r(S) for S in sets])


def run_rep(cfg, n, p, rep, name):
    g = cfg["g"]
    G = p // g
    seed = 20261102 + 1000003 * (ord(name) - 64) + 7919 * n + 31 * p + rep
    rng = np.random.default_rng(seed)
    X, y, groups, S0, Sref, M = gen_lh(n, G, g, cfg["rho"], cfg["psi"], cfg["pairs"], cfg["visible"], rng)
    D = Data(X, y)
    rec = dict(config=name, n=n, p=p, rep=rep, seed=seed, B=D.B, g=g, K=D.K, S0=S0, Sref=Sref, M=M)
    t0 = time.time()
    maxw, minc = group_margin(D, groups)
    rec["margin_maxw"], rec["margin_minc"] = maxw, minc
    rec["margin_ok"] = bool(maxw < minc and g <= D.B < 2 * g)
    if p <= 4300:
        blocks = v3_blocks(D)
        rec["blocks_eq_groups"] = sorted(map(tuple, blocks)) == sorted(map(tuple, groups))
    else:
        blocks = groups if rec["margin_ok"] else None
        rec["blocks_eq_groups"] = None  # implied by margin_ok (Lemma P1)
    if blocks is None:
        return rec
    rec["seblk_min_eig"] = float(min(np.linalg.eigvalsh(D.gram(C) / (n - 1))[0] for C in blocks))
    rec["lmin_RS0"] = float(np.linalg.eigvalsh(D.gram(S0) / (n - 1))[0])
    T = Tables(D, blocks)
    L = StartLaw(T)
    c, s = len(M), len(Sref)
    rec["log_pi0_Sref"] = L.log_pi0(Sref)
    rec["log_pi0_S0"] = L.log_pi0(S0)
    rec["Mstat"] = rec["log_pi0_S0"] + c * math.log(p) + 0.5 * c * math.log(n)
    rec["Mstat_limit_const"] = sum(math.log((s + i) / 2) for i in range(1, c + 1))
    rec["log_pi0_R0"] = L.log_mass_Rd(S0, 0)
    rec["log_pi0_R2"] = L.log_mass_Rd(S0, 2)
    mode, lmode = L.start_mode()
    rec["mode"], rec["mode_is_Sref"] = mode, mode == Sref
    q, loge = agg_q_e(T, Sref)
    rec["q"], rec["log_e"] = q, loge
    e = math.exp(loge) if loge < 50 else float("inf")
    rec["T22i_bound"] = (1 - q) ** (s + 1) / (1 + e) ** s if q < 1 else 0.0
    # start PIPs of the masked hubs and the start log-odds statistic n x / 2 at T = empty
    rec["start_pip_M"] = [L.log_mass_constrained(forced_in=[j]) for j in M]
    # LS0 from the start mode
    ell = math.ceil(math.log2(n + p + 1))
    ls = local_search(D, mode, ell, S0)
    rec["LS0_path"] = [list(x) for x in ls["path"]]
    rec["LS0_end_is_S0"] = list(ls["path"][-1]) == S0
    rec["LS0_certified"], rec["LS0_scored_S0"], rec["LS0_nscored"] = ls["certified"], ls["scored_S0"], ls["nscored"]
    # local posterior at S0: is S0 a strict local max; 1-neighbourhood mass ratio
    nb = neighbours(S0, p, D.K)
    fS0 = log_F(D, [S0])[0]
    fn = log_F(D, [list(x) for x in nb])
    rec["S0_local_max_gap"] = float(fS0 - fn.max())
    rec["log_nbr_mass_ratio_S0"] = float(logsumexp(fn - fS0))
    rec["F_S0_minus_F_Sref"] = float(fS0 - log_F(D, [Sref])[0])
    # D2 (c = 1): Dep at x° = Sref with Dset = proxies of the masked hub (rest of its group)
    if c == 1:
        jb = M[0]
        Dset = set(groups[jb // g]) - {jb}
        others = [l for l in range(p) if l not in Dset and l != jb]
        sets1 = [sorted(set(Sref) ^ {l}) for l in others]
        lg0 = np.array([log_w(len(S), p) + T.log_r(S) for S in sets1]) - (log_w(s, p) + T.log_r(Sref))
        lg1 = log_F(D, sets1) - log_F(D, [Sref])[0]
        k0 = np.exp(np.minimum(lg0, 50)); k1 = np.exp(np.minimum(lg1, 50))
        rec["Dep"] = float(np.maximum(k0, k1).sum())
        rec["Dep_kappa0"], rec["Dep_kappa1"] = float(k0.sum()), float(k1.sum())
        prox = [sorted(set(Sref) | {l}) for l in sorted(Dset)]
        rec["proxy_log_kappa1_max"] = float((log_F(D, prox) - log_F(D, [Sref])[0]).max())
        rec["kD"] = len(Dset)
    # NB of D2: initial pilot d-range over H0 exact pi0 draws
    N0 = max(2500, n, p)
    H0 = math.ceil(512 * N0 / 2500)
    draws = L.sample(H0, np.random.default_rng(seed + 1))
    uniq = {tuple(S) for S in draws}
    ul = [list(S) for S in uniq]
    dv = dict(zip(uniq, dvals(D, T, ul)))
    dd = np.array([dv[tuple(S)] for S in draws])
    rec["H0"] = H0
    rec["frac_draws_Sref"] = float(np.mean([S == Sref for S in draws]))
    rec["S0_drawn"] = any(S == S0 for S in draws)
    rec["d_range"] = float(dd.max() - dd.min())
    T0 = max(1000, ell ** 2)
    rec["NB_threshold"] = T0 * math.log(1.925)
    rec["NB_holds"] = bool(rec["S0_drawn"] or rec["d_range"] <= rec["NB_threshold"])
    rec["n_draws_with_proxy_of_M"] = int(sum(any(l in S for l in M) or
                                             any((l // g) * g in M and l not in M for l in S) for S in draws))
    rec["secs"] = time.time() - t0
    return rec


def main():
    name = sys.argv[1]
    cfg = CONFIGS[name]
    only = None if len(sys.argv) < 3 else int(sys.argv[2])
    out = open(f"../results/lh_{name}.jsonl", "a")
    for (n, p, R) in cfg["grid"]:
        if only is not None and n != only:
            continue
        for rep in range(R):
            rec = run_rep(cfg, n, p, rep, name)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(name, n, p, rep, "Mstat %.3f" % rec.get("Mstat", float("nan")),
                  "pi0(S°) %.4f" % math.exp(rec.get("log_pi0_Sref", -np.inf)),
                  "LS0", rec.get("LS0_end_is_S0"), "%.0fs" % rec.get("secs", 0), flush=True)


if __name__ == "__main__":
    main()
