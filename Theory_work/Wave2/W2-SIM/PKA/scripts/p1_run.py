"""PKA Priority 1: exact-Gram compound symmetry, p = floor(c n) <= n-1, truths (2,26,53,75), theta = .5*(1.4,1,1.8,1.2),
sigma = 1.  Start = actual capped block DP on the FAC-B baseline source partition (fast replacement, validated);
path = certified complete-scan LS0 path (pka_lib.certified_path, production tie rule), uncapped, computed once; caps
a = ell+|start|, a2 = ell+2|start| inferred from its scan prefix.  If the path met an exact float tie, the path is
re-run with the opposite tie rule ('antilex') and the outcomes are compared (sensitivity).  For n <= REF_MAX_N the
reference n1 run_path is also run and its move list compared with the certified path.
Usage: python p1_run.py n c rho rep_lo rep_hi OUT_JSONL RAW_JSONL_GZ"""
import sys, os, math, json, time, gzip
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pka_lib import *

REF_MAX_N = 12800
n, c, rho = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
lo, hi = int(sys.argv[4]), int(sys.argv[5])
out_path, raw_path = sys.argv[6], sys.argv[7]
p = math.floor(round(c * n, 9))
assert p <= n - 1
TRUTH = (2, 26, 53, 75)
theta = np.zeros(p)
theta[list(TRUTH)] = .5 * np.array([1.4, 1, 1.8, 1.2])
B = bc.block_size(n, p)
blocks = fast_partition_cs(p, B)
ell = bc.ell_cap(n, p)
prov_digest = write_provenance(out_path + ".prov.json", dict(prio="P1", args=dict(n=n, c=c, rho=rho, lo=lo, hi=hi)))
truth_blocks = sorted({bi for bi, C in enumerate(blocks) for j in C if j in TRUTH})
SENS_KEYS = ("first_scoring_scan", "first_arrival", "initial_swaps", "m_star", "final_is_S0")
for rep in range(lo, hi):
    seed = seed_for(1, n, round(c * 100), round(rho * 10), rep)
    t0 = time.time()
    P = cs.CS(rho, theta, n, rng=np.random.default_rng(seed))
    st = fast_start_mode(P, blocks)
    start = st["mode"]
    t1 = time.time()
    res = certified_path(P, start)
    t2 = time.time()
    caps = dict(a=ell + len(start), a2=ell + 2 * len(start))
    an = analyse_path(P, start, res, ell, caps)
    t3 = time.time()
    row = dict(prio="P1", schema=2, prov=prov_digest, n=n, p=p, c=c, rho=rho, rep=rep, seed=seed, K=P.K, ell=ell, B=B,
               s0=len(TRUTH),
               partition="FAC-B baseline source partition (population Sigma, tie tol 1e-10) = consecutive blocks of B; "
                         "NOT production tie-breaking",
               partition_digest=partition_digest(blocks), n_blocks=len(blocks), truth_blocks=truth_blocks,
               start_fallback=st["fallback"], start_size_margin=st["size_margin"],
               start_K_gap=st["best_below_K_gap"], slack=ell + len(TRUTH) + 1, eta=P.eta, s=P.s)
    row.update(start_summary(P, start, blocks))
    mc = an.pop("moves_compact")
    row.update(an)
    if res["info"]["ties"] > 0:          # tie-rule sensitivity
        res2 = certified_path(P, start, tie_rule="antilex", trace=False)
        an2 = analyse_path(P, start, res2, ell, caps)
        row["antilex"] = {k: an2[k] for k in SENS_KEYS}
        row["antilex"]["scored_a"] = an2["caps"]["a"]["scored"]
        row["antilex"]["scored_a2"] = an2["caps"]["a2"]["scored"]
        row["antilex"]["same_moves"] = res2["moves"] == res["moves"]
        row["tie_outcome_sensitive"] = any(row["antilex"][k] != v for k, v in
                                           [(k, an[k]) for k in SENS_KEYS] + [("scored_a", an["caps"]["a"]["scored"]),
                                                                             ("scored_a2", an["caps"]["a2"]["scored"])])
    else:
        row["tie_outcome_sensitive"] = False
    t4 = time.time()
    if n <= REF_MAX_N:
        ref = run_path(P, start)
        row["ref_run_path_equal"] = [tuple(m) for m in ref["moves"]] == [tuple(m) for m in res["moves"]]
        row["ref_ties"] = ref["info"]["ties"]
    t5 = time.time()
    row["secs"] = dict(start=round(t1 - t0, 2), path=round(t2 - t1, 2), analyse=round(t3 - t2, 2),
                       antilex=round(t4 - t3, 2), ref=round(t5 - t4, 2))
    with open(out_path, "a") as f:
        f.write(git_like_json(row) + "\n")
    with gzip.open(raw_path, "at") as f:
        f.write(git_like_json(dict(prov=prov_digest, n=n, p=p, c=c, rho=rho, rep=rep, seed=seed, start=list(start),
                                   termination=res["termination"], trace=res["trace"],
                                   tie_records=res["tie_records"], moves_compact=mc)) + "\n")
    print(n, p, rho, rep, "start", len(start), "K", P.K, "m*", an["m_star"], "init_swaps", an["initial_swaps"],
          "first_score", an["first_scoring_scan"], "cap", caps, "ties", res["info"]["ties"],
          "sens", row["tie_outcome_sensitive"], "ref_eq", row.get("ref_run_path_equal"), row["secs"], flush=True)
