"""E7: proxy flood.  truth x1 (theta=1), d proxies l_k = r x1 + sqrt(1-r^2) z_k (r=.6), remaining nulls independent, exact-Gram design,
p=120, d in {20,40}, n in {200,800,3200}, 20 seeds.  Extra (beyond spec): p=300, d=200, B=16, 5 seeds."""
import json, math, time
import numpy as np
import bvs_core as bc, exp_common as ec


def spec_flood(p, d, r=0.6):
    Sigma = np.eye(p)
    Sigma[0, 1:d + 1] = r
    Sigma[1:d + 1, 0] = r
    Sigma[1:d + 1, 1:d + 1] = r * r
    np.fill_diagonal(Sigma, 1.0)
    th = np.zeros(p)
    th[0] = 1.0
    return dict(Sigma=Sigma, theta=th, groups=None, S0=(0,), V=tuple(range(0, d + 1)), ref_Sstar=None, sigma2=1.0)


_S, _X = {}, {}


def job(j):
    p, d, n, seed = j
    if (p, d) not in _S:
        _S[(p, d)] = spec_flood(p, d)
    spec = _S[(p, d)]
    if (p, d, n) not in _X:
        _X[(p, d, n)] = bc.exact_gram_design(spec["Sigma"], n, np.random.default_rng(4242 + n + d))
    X = _X[(p, d, n)]
    y = bc.make_y_std(X, spec["theta"], 1.0, np.random.default_rng(777 * seed + n + d))
    r = ec.analyse(X, y, spec, ("flood", p, d, n), noise_ref=True)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    ls = bc.local_search(prob, info.mode, 2000)
    S0 = (0,)
    prox = set(range(1, d + 1))
    r["n_blocks_with_proxies"] = sum(1 for b in blocks if prox & set(b))
    r["x1_block_size"] = len([b for b in blocks if 0 in b][0])
    r["start_has_x1"] = 0 in info.mode
    r["start_proxies"] = len(set(info.mode) & prox)
    r["start_nulls"] = len(set(info.mode) - prox - {0})
    r["unc_moves"] = ls["moves"]
    r["unc_reach_S0"] = S0 in ls["path"]
    r["unc_tau"] = ls["path"].index(S0) if S0 in ls["path"] else -1
    r["unc_S0_scored"] = S0 in ls["scored"]
    r["unc_final_eq_S0"] = ls["final"] == S0
    r["unc_certified"] = ls["certified"]
    r.update(dict(d=d, seed=seed))
    return r


def summarise(rows, keys):
    summ = ec.agg(rows, keys)
    for s in summ:
        rs = [r for r in rows if all(r[k] == s[k] for k in keys)]
        mm = lambda k: "%d-%d" % (min(r[k] for r in rs), max(r[k] for r in rs))
        s["B"] = rs[0]["B"]
        s["blocks w/ proxies"] = mm("n_blocks_with_proxies")
        s["x1 in start"] = ec.frac(rs, "start_has_x1")
        s["|start\S0|"] = mm("start_extra_vs_S0")
        s["proxies/nulls in start (max)"] = "%d/%d" % (max(r["start_proxies"] for r in rs), max(r["start_nulls"] for r in rs))
        s["moves"] = mm("moves")
        s["local_limit"] = ec.frac(rs, "local_limit")
        s["uncapped moves to S0 (tau)"] = mm("unc_tau")
        s["uncapped reach S0"] = ec.frac(rs, "unc_reach_S0")
        s["uncapped final=S0"] = ec.frac(rs, "unc_final_eq_S0")
        s["final=S0 (capped)"] = ec.frac(rs, "final_eq_S0")
    return summ


COLS = ["p", "d", "n", "N", "B", "blocks w/ proxies", "x1 in start", "|start| (min-max)", "|start\S0|", "proxies/nulls in start (max)", "ell",
        "moves", "local_limit", "S0 scored", "certified", "final=S0 (capped)", "HPM=S0", "uncapped moves to S0 (tau)", "uncapped reach S0", "uncapped final=S0"]

if __name__ == "__main__":
    t0 = time.time()
    NS = [200, 800, 3200]
    jobs = [(120, d, n, s) for d in (20, 40) for n in NS for s in range(20)]
    rows = ec.pmap(job, jobs)
    ec.write_rows(rows, "E7")
    summ = summarise(rows, ["p", "d", "n"])
    jobs2 = [(300, 200, n, s) for n in (800, 3200) for s in range(5)]
    rows2 = ec.pmap(job, jobs2)
    ec.write_rows(rows2, "E7b")
    summ2 = summarise(rows2, ["p", "d", "n"])
    with open("E7_summary.md", "w") as f:
        f.write("## E7 proxy flood (x1 truth theta=1; d proxies with corr .6 to x1, mutual corr .36; remaining nulls independent; exact Gram) -- 20 seeds per row\n\n")
        f.write(ec.md_table(summ, COLS))
        f.write("\n### E7b (extra, beyond the spec): p=300, d=200, 5 seeds per row\n\n")
        f.write(ec.md_table(summ2, COLS))
    json.dump(dict(E7=summ, E7b=summ2), open("E7_summary.json", "w"), indent=1, default=str)
    print(open("E7_summary.md").read())
    print("secs", time.time() - t0)
