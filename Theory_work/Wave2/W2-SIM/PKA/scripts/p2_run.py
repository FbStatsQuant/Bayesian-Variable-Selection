"""PKA Priority 2 (EXPLICITLY NONPRODUCTION singleton partition): exact-Gram CS, rho = 1/2, sigma = 1, p = floor(c n).
variants: v1 s0 = 1, theta_0 = 1 (L2 / SINGLETON_TARGET hypotheses);
          v3 s0 = 2, theta = (1, 1)  (L2 two-truth hypotheses; control added after review R01);
          v2 s0 = 2, theta = (1, -.1) (requested weak-truth diagnostic; NOT within L2's hypotheses).
Start = n3.singleton_start (reference; validated against bc.start_mode on singleton blocks); path = certified_path
(start construction is the only change w.r.t. the n1 reference path; path validated move-by-move).
mode 'full'  : uncapped path to the certified mode (caps inferred from its scan prefix).
mode 'early' : path computed until BOTH a non-swap move has occurred and >= ceil(3 log n) moves were made; late-path
               fields are prefix-only; merged_miss_by_size records the deterministic size implication.
Usage: python p2_run.py variant n c rep_lo rep_hi mode OUT_JSONL RAW_JSONL_GZ"""
import sys, os, math, json, time, gzip
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pka_lib import *
from scipy.stats import norm

variant, n, c = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
lo, hi, mode = int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
out_path, raw_path = sys.argv[7], sys.argv[8]
TH = dict(v1=[1.0], v2=[1.0, -.1], v3=[1.0, 1.0])
assert variant in TH and mode in ("full", "early")
p = math.floor(round(c * n, 9))
assert p <= n - 1
th0 = TH[variant]
s0 = len(th0)
theta = np.zeros(p)
theta[:s0] = th0
rho = .5
ell = bc.ell_cap(n, p)
K = min(p, n // 2)
assert K >= s0 + 2
qn = (K - s0) / (p - s0)
t_q = float(norm.isf(qn))
mu = float(norm.pdf(t_q) / qn)
Lmax = max(math.ceil(Cw * math.log(n)) for Cw in WINDOW_C)
prov_digest = write_provenance(out_path + ".prov.json", dict(prio="P2", args=dict(variant=variant, n=n, c=c, lo=lo,
                                                                                    hi=hi, mode=mode)))
SENS_KEYS = ("first_scoring_scan", "first_arrival", "initial_swaps", "initial_null_swaps", "m_star", "final_is_S0")


def run(P, start, rule):
    if mode == "full":
        return certified_path(P, start, tie_rule=rule)
    seen = [False]

    def stop(moves):
        if moves[-1][0][0] != "s":
            seen[0] = True
        return seen[0] and len(moves) >= Lmax
    return certified_path(P, start, tie_rule=rule, stop=stop)


for rep in range(lo, hi):
    seed = seed_for(2, int(variant[1]), n, round(c * 100), rep)
    t0 = time.time()
    P = cs.CS(rho, theta, n, rng=np.random.default_rng(seed))
    start = singleton_start(P)
    t1 = time.time()
    res = run(P, start, "lex")
    t2 = time.time()
    caps = dict(a=ell + len(start), a2=ell + 2 * len(start))
    an = analyse_path(P, start, res, ell, caps)
    t3 = time.time()
    m = an["initial_swaps"]
    row = dict(prio="P2", schema=2, prov=prov_digest, variant=variant, theta_S0=th0,
               partition="SINGLETON (nonproduction diagnostic)", mode=mode, in_L2_hypotheses=variant in ("v1", "v3"),
               n=n, p=p, c=c, rho=rho, rep=rep, seed=seed, K=P.K, ell=ell, s0=s0, L0=ell + s0 + 2,
               q_n=qn, t_q=t_q, mu_theory=mu, eta=P.eta, s=P.s)
    # size implication (deterministic): |start| = K, K >= s0+2, first m >= ell+s0+2 moves size-preserving
    row["merged_miss_by_size"] = (len(start) == P.K and m is not None and m >= ell + s0 + 2)
    if row["merged_miss_by_size"] and an["caps"]["a"]["scored"] is not None:
        assert an["caps"]["a"]["scored"] is False, "size implication violated"
    row.update(start_summary(P, start))
    S0set = set(P.S0)
    nulls = np.array([j for j in range(p) if j not in S0set])
    kn = len(set(start) - S0set)
    top = set(nulls[np.argsort(P.xi[nulls])[len(nulls) - kn:]].tolist()) if kn else set()
    row["retained_nulls_are_top_xi"] = (set(start) - S0set) == top
    row["retained_mean_minus_mu"] = row["retained_null_xi_mean"] - mu
    mc = an.pop("moves_compact")
    row.update(an)
    tin = [r for r in mc if r[0] != "-N*" and r[1] in ("sTi", "+T")]
    tout = [r for r in mc if r[0] != "-N*" and r[1] in ("sTo", "-T", "sTT")]
    row["first_truth_in_move"] = tin[0][:4] if tin else None
    row["first_truth_out_move"] = tout[0][:4] if tout else None
    if res["info"]["ties"] > 0:
        res2 = run(P, start, "antilex")
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
    row["secs"] = dict(start=round(t1 - t0, 2), path=round(t2 - t1, 2), analyse=round(t3 - t2, 2),
                       antilex=round(t4 - t3, 2))
    with open(out_path, "a") as f:
        f.write(git_like_json(row) + "\n")
    with gzip.open(raw_path, "at") as f:
        f.write(git_like_json(dict(prov=prov_digest, variant=variant, n=n, p=p, c=c, rep=rep, seed=seed, mode=mode,
                                   start=list(start), termination=res["termination"], trace=res["trace"],
                                   tie_records=res["tie_records"], moves_compact=mc)) + "\n")
    print(variant, n, p, rep, "start", len(start), "init_swaps", m, "L0", ell + s0 + 2, "moves", an["moves_run"],
          "term", res["termination"], "first_score", an["first_scoring_scan"], "ties", res["info"]["ties"],
          row["secs"], flush=True)
