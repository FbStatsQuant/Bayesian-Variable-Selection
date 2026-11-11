r"""v1_masked.py -- W3-RM sharpness probe V1: visibility (V) violated (a truth masked inside its block).
FALSIFICATION PROBE: OBSERVATIONS ONLY, NOT A PROOF; every theorem is asymptotic.  Run:  py -3.13 v1_masked.py
Imports (does not edit) the ported method objects (bvs_core via rm_common.py).  Output: v1_results.csv.  Seeds fixed:
BASE = 20261201, seeds 1..20 per cell; data rng = SeedSequence([BASE, cell, n, p, seed]); column-layout permutation rng =
SeedSequence([BASE, 99, cell, p, seed]) (n-independent).  Gaussian rows, columns standardised by the port, sigma = 1,
y via bc.make_y_std.  Pipeline = n4_r2_pseudo.py: start mode -> LS0 (complete scans) from the start mode with cap
ell_cap(n,p)+|start| (SHIPPED) and, derived from the same path, with the OLD cap ell_cap(n,p).  Definitions of every column
(start mode, move types, endpoint, certified, S0 scored, S0_is_max): see rm_common.py docstring.

DESIGN (canonical order, then columns are randomly permuted per seed)
  j (theta=1), k (theta=2), t (theta=1.5, independent of everything), W_k has Corr(W_j,W_k) = -0.5, so
  Cov(W_j, theta_j W_j + theta_k W_k) = 1 - 2*0.5 = 0 (j marginally masked).   Remaining columns iid N(0,1).
  cell V1a   : j has G=15 decoys d_i = 0.9 W_j + sqrt(1-0.81) e_i, k has G=15 decoys built from W_k the same way.
  cell V1a13 : same with G = 13 decoys per truth, p = 200 ONLY (variant added by me: B = block_size(n,200) = 14 < 16 = group
               size in V1a, so with p = 200 the 16-member groups cannot fit into one block; G=13 gives group size 14 = B).
  cell V1b   : no decoys.
  p in {200, 400}; n in {400, 1600, 6400}; 20 seeds (V1a13 only for p = 200).
PER RUN (CSV columns)
  blocks: realised block of j, k, t (index, size); same_block_jk; per type counts inside j's block and k's block
  (types: j, k, t, dJ = decoys of j, dK = decoys of k, iid).
  j_in_start / k_in_start / t_in_start / S0_in_start, n_extra, extras_by_type; start_trunc/start_nopt (tie enumeration cap).
  LS0 columns (prefix ls_ shipped cap, ls_old_ old cap): moves, final_eq_S0, certified, S0_scored, S0_is_max, move-type counts.
  j_entry := how j first appears on the shipped-cap LS0 path: in_start | add (pure addition move) | swap (swapped in) | never.
  reached_by_add := ls_final_eq_S0 AND j_entry == add (S0 reached with j entering by an addition move).
  ls_n_add_truth counts additions of any truth; ls_n_swap_add_truth counts swaps that remove a non-truth and add a truth.
  POPULATION QUANTITIES (population Sigma, permuted to column order; theta supported on S0; m = sum_{S0} theta_i W_i):
  cov_j(U) := Cov(W_j, m | W_U) = c_j - Sigma_{jU} Sigma_UU^{-1} c_U, c = Sigma theta.
  minabs_cov_j_block := min over ALL U subset of block(j) \ {j} (|U| <= 15) of |cov_j(U)|; n_masked_U_j := number of such U with
  |cov_j(U)| < 1e-9; n_U_j := number of U (2^(|block|-1)).   NB U = empty always gives exactly 0 (j is marginally masked), so
  minabs_cov_j_block ~ 0 in every cell by construction; the informative columns are
  minabs_cov_j_noK := same min restricted to U subset block(j) \ {j,k}  (U never contains k; ~0 means j stays masked inside
  its block unless k is in the block) and frac_masked_noK := fraction of those U with |cov| < 1e-9.
  same for k (minabs_cov_k_block, n_masked_U_k): cov_k(U) = Cov(W_k, m | W_U); k is visible marginally (Cov = 1.5).
"""
import os, sys, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rm_common import bc, np, HERE, start_record, ls_record, write_csv, json   # noqa: E402
from multiprocessing import Pool

BASE = 20261201
THETA = {"j": 1.0, "k": 2.0, "t": 1.5}
NSEEDS = 20
CELLS = {"V1a": 1, "V1a13": 2, "V1b": 3}


def build_sigma(p, G):
    """canonical order [j, k, t, dJ(G), dK(G), rest]; returns Sigma, labels, truth idx dict"""
    L = np.zeros((p, p))
    s34 = np.sqrt(0.75)
    L[0, 0] = 1.0                                     # W_j = z0
    L[1, 0] = -0.5; L[1, 1] = s34                     # W_k = -.5 z0 + sqrt(.75) z1
    L[2, 2] = 1.0                                     # t = z2
    c = 3
    lab = ["j", "k", "t"]
    for i in range(G):
        L[c, 0] = 0.9; L[c, c] = np.sqrt(1 - 0.81); lab.append("dJ"); c += 1
    for i in range(G):
        L[c, 0] = 0.9 * (-0.5); L[c, 1] = 0.9 * s34; L[c, c] = np.sqrt(1 - 0.81); lab.append("dK"); c += 1
    while c < p:
        L[c, c] = 1.0; lab.append("iid"); c += 1
    return L @ L.T, np.array(lab)


def cov_over_subsets(Sig, cvec, j, pool_idx):
    """for all U subset pool_idx (j not in pool_idx): cov(U) = c_j - Sig_{jU} Sig_UU^{-1} c_U.  Returns array of |cov|."""
    pool_idx = np.array(pool_idx, dtype=np.int64)
    m = len(pool_idx)
    vals = [abs(cvec[j])]                             # U = empty
    for k in range(1, m + 1):
        comb = np.array(list(itertools.combinations(range(m), k)), dtype=np.int64)
        idx = pool_idx[comb]
        chunk = max(1, int(2_000_000 // (k * k)))
        for s in range(0, len(idx), chunk):
            ii = idx[s:s + chunk]
            SS = Sig[ii[:, :, None], ii[:, None, :]]
            rhs = np.stack([Sig[j, ii], cvec[ii]], axis=2)
            sol = np.linalg.solve(SS, rhs)
            cov = cvec[j] - (Sig[j, ii] * sol[:, :, 1]).sum(1)
            vals.extend(np.abs(cov).tolist())
    return np.array(vals)


def job(args):
    cell, n, p, seed = args
    t0 = time.time()
    G = {"V1a": 15, "V1a13": 13, "V1b": 0}[cell]
    Sig0, lab0 = build_sigma(p, G)
    lrng = np.random.default_rng(np.random.SeedSequence([BASE, 99, CELLS[cell], p, seed]))
    perm = lrng.permutation(p)                        # perm[new] = canonical
    inv = np.empty(p, dtype=int); inv[perm] = np.arange(p)
    Sig = Sig0[np.ix_(perm, perm)]
    lab = lab0[perm]
    jj, kk, tt = int(inv[0]), int(inv[1]), int(inv[2])
    S0 = tuple(sorted([jj, kk, tt]))
    theta = np.zeros(p); theta[jj] = THETA["j"]; theta[kk] = THETA["k"]; theta[tt] = THETA["t"]
    rng = np.random.default_rng(np.random.SeedSequence([BASE, CELLS[cell], n, p, seed]))
    Wr = bc.iid_design_raw(Sig, n, rng)
    X = bc.standardize_X(Wr)
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    bid = bc.block_id_array(blocks, p)
    mode, info, r = start_record(prob, blocks, S0, lab)
    r.update(dict(cell=cell, n=n, p=p, seed=seed, G=G, S0=json.dumps(list(S0)), pos_j=jj, pos_k=kk, pos_t=tt))
    bj, bk, bt = int(bid[jj]), int(bid[kk]), int(bid[tt])
    r.update(dict(blk_j=bj, blk_k=bk, blk_t=bt, blk_j_size=len(blocks[bj]), blk_k_size=len(blocks[bk]),
                  same_block_jk=bj == bk, j_in_start=jj in mode, k_in_start=kk in mode, t_in_start=tt in mode))
    for nm, b in (("j", bj), ("k", bk)):
        cnts = {}
        for c in blocks[b]:
            cnts[lab[c]] = cnts.get(lab[c], 0) + 1
        r["blk_%s_composition" % nm] = json.dumps(cnts, sort_keys=True)
    # population quantities
    cvec = Sig @ theta
    for nm, idx, b in (("j", jj, bj), ("k", kk, bk)):
        pool_all = [c for c in blocks[b] if c != idx]
        a = cov_over_subsets(Sig, cvec, idx, pool_all)
        r["minabs_cov_%s_block" % nm] = float(a.min())
        r["n_masked_U_%s" % nm] = int((a < 1e-9).sum())
        r["n_U_%s" % nm] = len(a)
        if nm == "j":
            other = kk
            pool_nk = [c for c in blocks[b] if c != idx and c != other]
            a2 = cov_over_subsets(Sig, cvec, idx, pool_nk)
            r["minabs_cov_j_noK"] = float(a2.min())
            r["frac_masked_noK"] = float((a2 < 1e-9).mean())
            r["n_U_noK"] = len(a2)
            r["k_in_block_j"] = other in blocks[b]
    # LS0 from the start mode
    rec, res = ls_record(prob, mode, S0, "ls_")
    r.update(rec)
    # how j enters the path (shipped-cap path): 'in_start', 'add' (pure addition move), 'swap' (swap in), 'never'
    path = res["path"]
    entry = "in_start" if jj in path[0] else "never"
    if entry == "never":
        for i in range(len(path) - 1):
            if jj not in path[i] and jj in path[i + 1]:
                entry = "add" if len(path[i + 1]) > len(path[i]) else "swap"
                break
    r["j_entry"] = entry
    r["reached_by_add"] = bool(r["ls_final_eq_S0"] and entry == "add")
    r["secs"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    t_start = time.time()
    only_n = os.environ.get("V1_N")
    cfgs = []
    for cell in CELLS:
        for p in (200, 400):
            if cell == "V1a13" and p != 200:
                continue
            for n in (400, 1600, 6400):
                if only_n and int(only_n) != n:
                    continue
                for seed in range(1, NSEEDS + 1):
                    cfgs.append((cell, n, p, seed))
    if os.environ.get("V1_TEST"):
        cfgs = cfgs[:int(os.environ["V1_TEST"])]
    print("BASE seed", BASE, "seeds 1..%d" % NSEEDS, "runs", len(cfgs), flush=True)
    rows = []
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        for r in pool.imap_unordered(job, cfgs):
            rows.append(r)
            print(r["cell"], r["n"], r["p"], r["seed"], "mode", r["start_size"], "extras", r["n_extra"], "j_in", r["j_in_start"], "k_in", r["k_in_start"],
                  "same_blk", r["same_block_jk"], "final=S0", r["ls_final_eq_S0"], "secs", r["secs"], flush=True)
    rows.sort(key=lambda r: (r["cell"], r["p"], r["n"], r["seed"]))
    out = "v1_results_test.csv" if os.environ.get("V1_TEST") else "v1_results.csv"
    write_csv(os.path.join(HERE, out), rows)
    print("total runtime %.1f s" % (time.time() - t_start))
