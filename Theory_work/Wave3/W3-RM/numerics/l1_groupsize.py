r"""l1_groupsize.py -- W3-RM sharpness probe L1: leakage far beyond log n (count of visible nulls).
FALSIFICATION PROBE: OBSERVATIONS ONLY, NOT A PROOF; every theorem is asymptotic.  Run:  py -3.13 l1_groupsize.py
Imports (does not edit) the ported method objects (bvs_core via rm_common.py).  Output: l1_results.csv.  Seeds fixed:
BASE = 20261202, seeds 1..20 per cell; data rng = SeedSequence([BASE, g, n, seed]); layout (column permutation) rng =
SeedSequence([BASE, 99, g, seed]).  Gaussian rows, standardised by the port, sigma = 1, y via bc.make_y_std.
Pipeline = n4_r2_pseudo.py (start mode -> LS0 with complete scans; shipped cap ell_cap(n,p)+|start| and, derived from the
same path, OLD cap ell_cap(n,p)); exact definitions of start mode / move types / endpoint / certified / S0 scored /
S0_is_max in rm_common.py.

DESIGN: p = 400.  One truth j (theta = 1) inside an equicorrelated group of size g (within-group correlation 0.5; the g-1
other group members are 'visible nulls'); two more truths (theta = -0.8, 1.2) alone (independent of everything); all other
columns iid N(0,1).  g in {8, 32, 128}; n in {400, 1600, 6400}; 20 seeds.  Columns are randomly permuted per seed.
PER RUN: extras by type (gnull = null in j's group, iid = elsewhere); n_extra, log n, n_extra_le_logn := n_extra <= log n,
n_extra_le_ell := n_extra <= ell_cap(n,p);  n_gnull_in_start;  LS0 columns (ls_ shipped, ls_old_ old cap): moves,
final_eq_S0, certified, S0_scored, S0_is_max, move-type counts, all_del_extra := every move is a deletion of a non-truth.
Block of j: size and number of group nulls inside it.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rm_common import bc, np, HERE, start_record, ls_record, write_csv, json   # noqa: E402
import math
from multiprocessing import Pool

BASE = 20261202
P = 400
NSEEDS = 20
THETA_OTHER = (-0.8, 1.2)


def job(args):
    g, n, seed = args
    t0 = time.time()
    p = P
    # canonical order: [j, g-1 group nulls, truth2, truth3, iid...]; group block = 0.5 I + 0.5 11'
    lab0 = np.array(["gtruth"] + ["gnull"] * (g - 1) + ["truth", "truth"] + ["iid"] * (p - g - 2))
    Sig0 = np.eye(p)
    Sig0[:g, :g] = 0.5 * np.eye(g) + 0.5 * np.ones((g, g))
    lrng = np.random.default_rng(np.random.SeedSequence([BASE, 99, g, seed]))
    perm = lrng.permutation(p)
    inv = np.empty(p, dtype=int); inv[perm] = np.arange(p)
    Sig = Sig0[np.ix_(perm, perm)]
    lab = lab0[perm]
    jj, t2, t3 = int(inv[0]), int(inv[g]), int(inv[g + 1])
    S0 = tuple(sorted([jj, t2, t3]))
    theta = np.zeros(p); theta[jj] = 1.0; theta[t2] = THETA_OTHER[0]; theta[t3] = THETA_OTHER[1]
    rng = np.random.default_rng(np.random.SeedSequence([BASE, g, n, seed]))
    X = bc.standardize_X(bc.iid_design_raw(Sig, n, rng))
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    bid = bc.block_id_array(blocks, p)
    mode, info, r = start_record(prob, blocks, S0, lab)
    ell = bc.ell_cap(n, p)
    logn = math.log(n)
    r.update(dict(g=g, n=n, p=p, seed=seed, S0=json.dumps(list(S0)), pos_j=jj, log_n=round(logn, 3), ell_cap=ell,
                  n_extra_le_logn=r["n_extra"] <= logn, n_extra_le_ell=r["n_extra"] <= ell))
    gn = {i for i in range(p) if lab[i] == "gnull"}
    r["n_gnull_in_start"] = len(gn & set(mode))
    bj = int(bid[jj])
    r["blk_j_size"] = len(blocks[bj])
    r["blk_j_n_gnull"] = sum(1 for c in blocks[bj] if lab[c] == "gnull")
    r["j_in_start"] = jj in mode
    rec, res = ls_record(prob, mode, S0, "ls_")
    r.update(rec)
    r["secs"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    t_start = time.time()
    cfgs = [(g, n, s) for g in (8, 32, 128) for n in (400, 1600, 6400) for s in range(1, NSEEDS + 1)]
    if os.environ.get("L1_TEST"):
        cfgs = cfgs[:int(os.environ["L1_TEST"])]
    print("BASE seed", BASE, "seeds 1..%d" % NSEEDS, "runs", len(cfgs), flush=True)
    rows = []
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        for r in pool.imap_unordered(job, cfgs):
            rows.append(r)
            print("g", r["g"], "n", r["n"], "seed", r["seed"], "mode", r["start_size"], "extras", r["n_extra"], r["extras_by_type"], "final=S0", r["ls_final_eq_S0"],
                  "old", r["ls_old_final_eq_S0"], "secs", r["secs"], flush=True)
    rows.sort(key=lambda r: (r["g"], r["n"], r["seed"]))
    out = "l1_results_test.csv" if os.environ.get("L1_TEST") else "l1_results.csv"
    write_csv(os.path.join(HERE, out), rows)
    print("total runtime %.1f s" % (time.time() - t_start))
