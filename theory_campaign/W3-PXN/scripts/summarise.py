"""Summaries of results/*.jsonl for REPORT.md. Usage: python3 summarise.py > ../results/summary.txt"""
import json, math, collections
import numpy as np
from scipy.stats import chi2

L10 = math.log(10)


def load(f):
    try:
        return [json.loads(l) for l in open(f)]
    except FileNotFoundError:
        return []


def q(a, qs=(0.05, 0.5, 0.95)):
    a = np.asarray(a, float)
    return "/".join("%.2f" % np.quantile(a, x) for x in qs)


def lh(name):
    R = load(f"../results/lh_{name}.jsonl")
    if not R:
        return
    print(f"\n=== LH-iid config {name} ===")
    by = collections.defaultdict(list)
    for r in R:
        by[(r["n"], r["p"])].append(r)
    c = len(R[0]["M"]); s = len(R[0]["Sref"])
    const = sum(math.log((s + i) / 2) for i in range(1, c + 1))
    lim = [const + 0.5 * chi2.ppf(x, c) for x in (0.05, 0.5, 0.95)]
    print(f"c={c}, s={s}; limit law of Mstat: q05/med/q95 = " + "/".join("%.2f" % v for v in lim))
    print("n p reps | blocks=groups | margin(maxw<minc) | SEblk min | med log10pi0(S0) | Mstat q05/med/q95 |"
          " sqrt(n/log n)*med(1-pi0(S°)) | med pi0(R0) | med pi0(R2) | mode=S° | med q | max log e | T22(i) bound<=pi0(S°) |"
          " LS0 ends S0 certified | med F(S0)-F(S°) | S0 local max | Dep med (c=1) | NB holds | med d_range / thr")
    for (n, p), rs in sorted(by.items()):
        bg = [r["blocks_eq_groups"] for r in rs if r["blocks_eq_groups"] is not None]
        line = [f"{n} {p} {len(rs)}",
                ("%d/%d" % (sum(bg), len(bg))) if bg else "n/a(margin)",
                "%d/%d" % (sum(r["margin_ok"] for r in rs), len(rs)),
                "%.3f" % min(r["seblk_min_eig"] for r in rs),
                "%.2f" % np.median([r["log_pi0_S0"] / L10 for r in rs]),
                q([r["Mstat"] for r in rs]),
                "%.2f" % np.median([math.sqrt(n / math.log(n)) * (1 - math.exp(r["log_pi0_Sref"])) for r in rs]),
                "%.3f" % np.median([math.exp(r["log_pi0_R0"]) for r in rs]),
                "%.3f" % np.median([math.exp(r["log_pi0_R2"]) for r in rs]),
                "%d/%d" % (sum(r["mode_is_Sref"] for r in rs), len(rs)),
                "%.3f" % np.median([r["q"] for r in rs]),
                "%.1f" % max(r["log_e"] for r in rs),
                "%d/%d" % (sum(r["T22i_bound"] <= math.exp(r["log_pi0_Sref"]) + 1e-12 for r in rs), len(rs)),
                "%d/%d" % (sum(r["LS0_end_is_S0"] and r["LS0_certified"] for r in rs), len(rs)),
                "%.1f" % np.median([r["F_S0_minus_F_Sref"] for r in rs]),
                "%d/%d" % (sum(r["S0_local_max_gap"] > 0 for r in rs), len(rs)),
                ("%.3f" % np.median([r["Dep"] for r in rs])) if "Dep" in rs[0] else "-",
                "%d/%d" % (sum(r["NB_holds"] for r in rs), len(rs)),
                "%.1f/%.0f" % (np.median([r["d_range"] for r in rs]), rs[0]["NB_threshold"])]
        print(" | ".join(line))


def tau(n, p, s0=14):
    """dilution threshold: LO0(j) ~ V0(j) - [log((2p - s0)/s0) + (1/2) log(n+1)]"""
    return math.log((2 * p - s0) / s0) + 0.5 * math.log(n + 1)


def study(fname, title):
    R = load(fname)
    if not R:
        return
    print(f"\n=== {title} ===")
    by = collections.defaultdict(list)
    for r in R:
        by[(r["scen"], r.get("n", 200), r["p"], r["cc"])].append(r)
    print("scen n p scale reps | med log10 pi0(S0) | med pi0(R2) | med pi0(R0) | mean #mode-missing truths |"
          " mean #start-masked (LO0<0) | frac start-masked with LO1>0 | masked: med V0 / med V0pop / med V1 |"
          " masked: med delta2_pop (=L^2) | med v_T | med [log10 pi0(S0)-log10 pi0(mode)] | CL(0) pred -#miss*log10(p sqrt n) |"
          " dilution-predicted #masked (V0pop < tau) | per-truth agreement pred vs LO0<0")
    for key, rs in sorted(by.items()):
        s, n, p, cc = key
        masked = [t for r in rs for t in r["per_truth"] if t["LO0"] < 0]
        line = [f"S{s} {n} {p} {cc} {len(rs)}",
                "%.1f" % np.median([r["log_pi0_S0"] / L10 for r in rs]),
                "%.2f" % np.median([math.exp(r["log_pi0_R2"]) for r in rs]),
                "%.2f" % np.median([math.exp(r["log_pi0_R0"]) for r in rs]),
                "%.1f" % np.mean([len(r["mode_missing"]) for r in rs]),
                "%.1f" % np.mean([sum(t["LO0"] < 0 for t in r["per_truth"]) for r in rs]),
                ("%.2f" % np.mean([t["LO1"] > 0 for t in masked])) if masked else "-",
                ("%.1f / %.1f / %.1f" % (np.median([t["V0"] for t in masked]), np.median([t["V0pop"] for t in masked]),
                                         np.median([t["V1"] for t in masked]))) if masked else "-",
                ("%.0f" % np.median([t["delta2"] for t in masked])) if masked else "-",
                "%.2f" % np.median([t["vT"] for r in rs for t in r["per_truth"]]),
                "%.1f" % np.median([(r["log_pi0_S0"] - r["log_pi0_mode"]) / L10 for r in rs]),
                "%.1f" % np.median([-len(r["mode_missing"]) * math.log10(p * math.sqrt(n)) for r in rs]),
                "%.1f" % np.mean([sum(t["V0pop"] < tau(n, p) for t in r["per_truth"]) for r in rs]),
                "%.2f" % np.mean([(t["V0pop"] < tau(n, p)) == (t["LO0"] < 0) for r in rs for t in r["per_truth"]])]
        print(" | ".join(line))
    allt = [t for r in R for t in r["per_truth"]]
    v0 = np.array([t["V0"] for t in allt]); vp = np.array([t["V0pop"] for t in allt])
    print("all truths: corr(V0, V0pop) = %.3f; median V0 - V0pop = %.2f; n_truths = %d" %
          (np.corrcoef(v0, vp)[0, 1], np.median(v0 - vp), len(allt)))


if __name__ == "__main__":
    for nm in ("A", "B", "P"):
        lh(nm)
    study("../results/study_n200.jsonl", "Study design, n = 200 (S1/S3/S4/S6)")
    study("../results/study_nsweep.jsonl", "Study design, n sweep at p = 1000, scale 0.5")


def ls0_study():
    R = load("../results/study_ls0.jsonl")
    if not R:
        return
    print("\n=== LS0 (local search from the exact start mode) on the study design, n = 200 ===")
    by = collections.defaultdict(list)
    for r in R:
        by[(r["scen"], r["p"], r["cc"])].append(r)
    print("scen p scale reps | ell | med |S~0 Delta S0| | frac dist <= ell+1 | LS0 ends at S0 (certified) | LS0 scores S0 |"
          " end F >= F(S0) | frac S0-reached among dist<=ell+1 | frac S0-reached among dist>ell+1")
    for key, rs in sorted(by.items()):
        s, p, cc = key
        ell = rs[0]["ell"]
        near = [r for r in rs if r["start_dist"] <= ell + 1]
        far = [r for r in rs if r["start_dist"] > ell + 1]
        f = lambda xs: ("%d/%d" % (sum(r["scored_S0"] for r in xs), len(xs))) if xs else "-"
        print(" | ".join([f"S{s} {p} {cc} {len(rs)}", str(ell), "%.0f" % np.median([r["start_dist"] for r in rs]),
                          "%.2f" % np.mean([r["start_dist"] <= ell + 1 for r in rs]),
                          "%d/%d" % (sum(r["end_is_S0"] and r["certified"] for r in rs), len(rs)),
                          "%d/%d" % (sum(r["scored_S0"] for r in rs), len(rs)),
                          "%d/%d" % (sum(r["end_minus_S0_F"] >= -1e-9 for r in rs), len(rs)), f(near), f(far)]))


ls0_study()
