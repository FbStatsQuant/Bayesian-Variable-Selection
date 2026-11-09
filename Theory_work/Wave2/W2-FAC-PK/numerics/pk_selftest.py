"""pk_selftest.py -- checks of pk_core against the general exact-Gram objects copied from W2-FAC-B (bvs_core, fac_core).
(1) cs_partition == bvs_core.partition_from_corr on exactly equicorrelated matrices (several p, B);
(2) start_mode_cs == bvs_core.start_mode (general scorer, all block tables) on small exact-Gram data;
(3) reproduction of W2-FAC-B N2 (rho=0.5, n=600, p=500, seed 0): start size 300, 19 swaps then 296 deletions;
(4) path_from == fac_core.ls0_path (general Schur-complement scanner) on small data (same move sequence)."""
import math, json, sys, time
import numpy as np
import bvs_core as bc, fac_core as fc, cs_core as cc, pk_core as pk

out = []
def rep(**d):
    print(json.dumps(d), flush=True); out.append(d)

# (1) partition
for p, B in [(40, 4), (100, 10), (257, 16), (500, 16), (777, 16)]:
    rho = 0.5
    R = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
    blocks = bc.partition_from_corr(R, B)
    rep(test="partition", p=p, B=B, equal=[sorted(b) for b in blocks] == pk.cs_partition(p, B), nblocks=len(blocks))

# (2) start mode, small data, general scorer
for (n, p, seed) in [(64, 40, 1), (64, 40, 2), (100, 70, 3), (144, 100, 4), (64, 60, 5), (100, 99, 6), (144, 130, 7), (196, 190, 8)]:
    rho = 0.5
    th = np.zeros(p); th[[2, 9, 17]] = [1.0, 0.8, 1.3]
    rng = np.random.default_rng(seed)
    xi = rng.standard_normal(p); eta = float(rng.standard_normal()); chi = float(rng.chisquare(n - 1 - p)) if n - 1 - p > 0 else 0.0
    P = cc.CS(rho, th, n, xi=xi, eta=eta, chi=chi)
    Sigma = (1 - rho) * np.eye(p) + rho * np.ones((p, p))
    # general exact-Gram object with the same g, chi
    class G: pass
    E = fc.ExactGram.__new__(fc.ExactGram)
    E.n, E.p, E.K, E.Sigma = n, p, min(p, n // 2), Sigma
    g = math.sqrt(rho) * eta + math.sqrt(1 - rho) * xi
    nm1 = n - 1.0
    gSg = float(g @ np.linalg.solve(Sigma, g))
    s = math.sqrt((nm1 * th @ Sigma @ th + 2 * math.sqrt(nm1) * th @ g + gSg + chi) / nm1)
    E.Xty = (nm1 * (Sigma @ th) + math.sqrt(nm1) * g) / s; E.XtX = nm1 * Sigma; E.yty = nm1
    E.nu = 0.01 + n / 2.0; E.logw = bc.log_prior_w(p, E.K); E.logm0 = -E.nu * math.log(0.02 + E.yty)
    E.cache = {(): E.logm0}
    B = pk.block_size(n, p)
    blocks = pk.cs_partition(p, B)
    info = bc.start_mode(E, blocks)
    sm = pk.start_mode_cs(P, blocks)
    rep(test="start_mode", n=n, p=p, K=P.K, B=B, equal=tuple(info.mode) == sm["mode"], size=sm["size"],
        zdiff=float(np.max(np.abs(E.Xty - P.z))))
    # (4) path comparison
    t0 = time.time()
    r_gen = fc.ls0_path(E, sm["mode"], P.S0)
    r_pk = pk.path_from(P, sm["mode"])
    mv_gen = [st.get("move") for st in r_gen["steps"] if "move" in st]
    mv_pk = [m if not m.startswith("s") else ("swN>N" if m == "sN" else m) for m in r_pk["moves"]]
    same_final = tuple(r_gen["final"]) == r_pk["final"]
    rep(test="path", n=n, p=p, moves_gen=r_gen["moves"], moves_pk=r_pk["n_moves"], same_final=same_final,
        same_types=[m[:2] if not m.startswith("sw") else "s" for m in mv_gen] == [m[:2] if not m.startswith("s") else "s" for m in r_pk["moves"]],
        t=round(time.time() - t0, 1))

# (3) reproduce N2
n, p, seed, rho = 600, 500, 0, 0.5
th = np.zeros(p); S0 = (2, 26, 53, 75); th[list(S0)] = np.array([1.4, 1.0, 1.8, 1.2])
rng = np.random.default_rng(seed)
eta = float(rng.standard_normal(1)[0]); xi = rng.standard_normal(p); chi = float(rng.chisquare(n - 1 - p)) if n - 1 - p > 0 else 0.0
P = cc.CS(rho, th, n, xi=xi, eta=eta, chi=chi)
blocks = pk.cs_partition(p, pk.block_size(n, p))
sm = pk.start_mode_cs(P, blocks)
r = pk.path_from(P, sm["mode"])
rep(test="N2_repro", start=sm["size"], has_S0=set(S0) <= set(sm["mode"]), moves=r["n_moves"], final_is_S0=r["final_is_S0"],
    summ=pk.summarize_moves(r["moves"]), k_hit=r["k_hit"], cap_MR1=pk.ell_cap(n, p) + sm["size"])
