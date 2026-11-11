r"""l2_eta.py -- W3-RM sharpness probe L2: population proxy strength n r^2 = eta log n (exploratory).
[Docstring note added by the lead after council round 1; no code changed: eta is the NOMINAL POPULATION strength with sigma^2
normalisation and a cellwise A = log p / log n; the runs do not certify violation or satisfaction of the sample condition
(L-gain) of STATEMENT v1.2.  Original title: "gain just above the threshold eta_A (assumption (L-gain))".]
FALSIFICATION PROBE: OBSERVATIONS ONLY, NOT A PROOF; every theorem is asymptotic.  Run:  py -3.13 l2_eta.py
Imports (does not edit) the ported method objects (bvs_core via rm_common.py).  Output: l2_results.csv.  Seeds fixed:
BASE = 20261203, seeds 1..20 per cell EXCEPT eta = 2.0: (p=400, n in {1600, 6400}) NOT RUN and (p=200, n >= 1600) seeds 1..10 (compute budget;
see nseeds_cell()); data rng = SeedSequence([BASE, etaidx, n, p, seed]); layout
(column permutation) rng = SeedSequence([BASE, 99, p, seed]).  Gaussian rows, port standardisation, sigma = 1, y via bc.make_y_std.
Pipeline = n4_r2_pseudo.py (start mode -> LS0 complete scans; shipped cap ell_cap(n,p)+|start|, OLD cap ell_cap(n,p)
derived from the same path).  Exact definitions of start mode / move types / endpoint / certified / S0 scored / S0_is_max:
rm_common.py.

DESIGN: one truth j (theta = 1); EVERY other column l is a weak proxy W_l = r W_j + sqrt(1-r^2) e_l (so
Corr(W_l, W_l') = r^2 between proxies) with r chosen so n r^2 = eta log n  (population gain of l given U = empty ~ eta sigma^2 log n).
eta in {0, 0.5 eta_A, 2 eta_A, 0.5, 1.0, 2.0}, eta_A = (sqrt(2A+1) - sqrt(2A))^2, A = log p / log n  (eta_A reported per cell;
A < 1 for some cells, the formula is applied as written).  p in {200, 400}; n in {400, 1600, 6400}.
PER RUN: eta label/value, eta_A, A, r, n r^2; n_proxy_in_start = |start mode \ {j}| (= n_extra; the sandwich S0 <= S~ <= Q with
Q = S0 fails iff n_extra > 0); j_in_start; LS0 columns (ls_ shipped, ls_old_ old cap): moves, final_eq_S0, certified,
S0_scored, S0_is_max, move-type counts, all_del_extra (every move is a deletion of a non-truth).
"""
import os, sys, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rm_common import bc, np, HERE, start_record, ls_record, write_csv, json   # noqa: E402
from multiprocessing import Pool

BASE = 20261203
NSEEDS = 20


def nseeds_cell(label, n, p):
    """Seeds per cell.  NOT RUN (0 seeds): eta = 2.0 with p = 400 and n in {1600, 6400}: their start modes have 69-91 elements and
    one complete LS0 run took ~1000 s each at (n=6400, p=400) (a complete scan is |S|*p swap models of size ~|S|), so even 10 seeds
    exceed the ~15-minute budget; the SPEC allows reducing p for such cells -- the p = 200 cells with the same eta and n are run
    instead.  REDUCED to 10 seeds (the minimum): eta = 2.0 with p = 200 and n >= 1600.  All other cells: 20 seeds."""
    if label == "2.0" and p == 400 and n >= 1600:
        return 0
    if label == "2.0" and p == 200 and n >= 1600:
        return 10
    return NSEEDS


ETAS = [("0", None), ("0.5etaA", None), ("2etaA", None), ("0.5", 0.5), ("1.0", 1.0), ("2.0", 2.0)]


def eta_value(label, A):
    etaA = (math.sqrt(2 * A + 1) - math.sqrt(2 * A)) ** 2
    return {"0": 0.0, "0.5etaA": 0.5 * etaA, "2etaA": 2 * etaA}.get(label), etaA


def job(args):
    ei, n, p, seed = args
    t0 = time.time()
    label = ETAS[ei][0]
    A = math.log(p) / math.log(n)
    eta, etaA = eta_value(label, A)
    if eta is None:
        eta = ETAS[ei][1]
    r_ = math.sqrt(eta * math.log(n) / n)
    v = np.full(p, r_); v[0] = 1.0
    Sig0 = np.diag(1 - v ** 2) + np.outer(v, v)
    lab0 = np.array(["truth"] + ["proxy"] * (p - 1))
    lrng = np.random.default_rng(np.random.SeedSequence([BASE, 99, p, seed]))
    perm = lrng.permutation(p)
    inv = np.empty(p, dtype=int); inv[perm] = np.arange(p)
    Sig = Sig0[np.ix_(perm, perm)]
    lab = lab0[perm]
    jj = int(inv[0])
    S0 = (jj,)
    theta = np.zeros(p); theta[jj] = 1.0
    rng = np.random.default_rng(np.random.SeedSequence([BASE, ei, n, p, seed]))
    X = bc.standardize_X(bc.iid_design_raw(Sig, n, rng))
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    mode, info, r = start_record(prob, blocks, S0, lab)
    r.update(dict(eta_label=label, eta=eta, eta_A=etaA, A=A, r=r_, n_r2=n * r_ * r_, n=n, p=p, seed=seed, pos_j=jj,
                  n_proxy_in_start=r["n_extra"], j_in_start=jj in mode, log_n=round(math.log(n), 3)))
    rec, res = ls_record(prob, mode, S0, "ls_")
    r.update(rec)
    r["secs"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    t_start = time.time()
    only_n = os.environ.get("L2_N")
    cfgs = [(ei, n, p, s) for ei in range(len(ETAS)) for p in (200, 400) for n in (400, 1600, 6400)
            for s in range(1, nseeds_cell(ETAS[ei][0], n, p) + 1) if (not only_n or int(only_n) == n)]
    cfgs.sort(key=lambda c: -(c[0] == 5) * (c[2] * c[1] ** 0.5))          # heaviest cells first (load balance); result sorted later
    if os.environ.get("L2_TEST"):
        cfgs = cfgs[:int(os.environ["L2_TEST"])]
    print("BASE seed", BASE, "seeds 1..20 (1..10 for the reduced cells)", "runs", len(cfgs), flush=True)
    rows = []
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        for r in pool.imap_unordered(job, cfgs):
            rows.append(r)
            print("eta", r["eta_label"], "n", r["n"], "p", r["p"], "seed", r["seed"], "mode", r["start_size"], "extras", r["n_extra"], "final=S0", r["ls_final_eq_S0"],
                  "moves", r["ls_moves"], "secs", r["secs"], flush=True)
    rows.sort(key=lambda r: (r["eta_label"], r["p"], r["n"], r["seed"]))
    out = os.environ.get("L2_OUT", "l2_results.csv")
    if os.environ.get("L2_TEST"):
        out = "l2_results_test.csv"
    write_csv(os.path.join(HERE, out), rows)
    print("total runtime %.1f s" % (time.time() - t_start))
