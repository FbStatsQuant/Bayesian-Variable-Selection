"""Summarise PKA per-seed JSONL rows (schema 2) into cell tables.  Usage: python summarise.py OUT_DIR file1.jsonl [...]
Writes OUT_DIR/P1_cells.csv, P1_trend.csv, P2_cells.csv, P2_windows.csv, DEDUP.json and SUMMARY.md.
Descriptive statistics only: trends are evidence, not limits.
Dedup policy (R01 finding 6): records are keyed by (prio, rho|variant, n, c, mode, rep); duplicates whose scientific
content (all fields except secs/prov/source) is identical are merged; CONFLICTING duplicates are quarantined (excluded
from every statistic) and listed in DEDUP.json.  Rows with schema != 2 are ignored (listed)."""
import sys, os, json, math, csv
import numpy as np
from scipy.stats import beta

out_dir = sys.argv[1]
os.makedirs(out_dir, exist_ok=True)
raw, ignored = [], 0
for fn in sys.argv[2:]:
    with open(fn) as f:
        for l in f:
            if l.strip():
                r = json.loads(l)
                if r.get("schema") != 2:
                    ignored += 1
                    continue
                r["_source"] = os.path.basename(fn)
                raw.append(r)


def key(r):
    return (r["prio"], r.get("variant", r["rho"]), r["n"], r["c"], r.get("mode", "full"), r["rep"])


def sci(r):
    return json.dumps({k: v for k, v in r.items() if k not in ("secs", "prov", "_source")}, sort_keys=True)


groups = {}
for r in raw:
    groups.setdefault(key(r), []).append(r)
rows, conflicts, merged = [], [], 0
for k, rs in groups.items():
    if len({sci(r) for r in rs}) > 1:
        conflicts.append(dict(key=list(k), sources=[r["_source"] for r in rs]))
        continue
    merged += len(rs) - 1
    rows.append(rs[0])
json.dump(dict(ignored_non_schema2=ignored, merged_identical=merged, conflicts=conflicts),
          open(os.path.join(out_dir, "DEDUP.json"), "w"), indent=1)


def cp(k, n, a=.05):
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def q(x, qq):
    x = [v for v in x if v is not None]
    return float(np.quantile(x, qq)) if x else float("nan")


def opt(rs, f):
    """(successes, observed, missing) for an optional boolean field."""
    vals = [f(r) for r in rs]
    obs = [v for v in vals if v is not None]
    return sum(bool(v) for v in obs), len(obs), len(vals) - len(obs)


def fmt(v, f="{:.2f}"):
    return "—" if v is None or (isinstance(v, float) and math.isnan(v)) else f.format(v)


nswaps = lambda r: sum(v for k, v in r["counts"].items() if k.startswith("s"))
md = ["# PKA summary (summarise.py; descriptive only — trends are evidence, not limits)", "",
      f"schema-2 rows: {len(raw)}; identical duplicates merged: {merged}; conflicting keys quarantined: {len(conflicts)}; "
      f"non-schema-2 rows ignored: {ignored}", ""]
# ------------------------------------------------------------------------------------------------ P1
cells = {}
for r in rows:
    if r["prio"] == "P1":
        cells.setdefault((r["rho"], r["n"], r["c"]), []).append(r)
tab = []
for kk in sorted(cells):
    rs = cells[kk]
    N = len(rs)
    r0 = rs[0]
    dec_a = [r for r in rs if r["caps"]["a"]["scored"] is not None]
    dec_a2 = [r for r in rs if r["caps"]["a2"]["scored"] is not None]
    ma = sum(not r["caps"]["a"]["scored"] for r in dec_a)
    ma2 = sum(not r["caps"]["a2"]["scored"] for r in dec_a2)
    lo, hi = cp(ma, len(dec_a)) if dec_a else (float("nan"),) * 2
    lo2, hi2 = cp(ma2, len(dec_a2)) if dec_a2 else (float("nan"),) * 2
    refeq = opt(rs, lambda r: r.get("ref_run_path_equal"))
    tab.append(dict(
        rho=kk[0], n=kk[1], c=kk[2], p=r0["p"], K=r0["K"], ell=r0["ell"], slack=r0["slack"], seeds=N,
        reps=f"{min(r['rep'] for r in rs)}-{max(r['rep'] for r in rs)}",
        noncertified=sum(r["termination"] != "certified" for r in rs),
        start_eq_K=sum(r["start_is_K"] for r in rs), truth_in_start=sum(r["truth_in_start"] for r in rs),
        init_q25=q([r["initial_swaps"] for r in rs], .25), init_med=q([r["initial_swaps"] for r in rs], .5),
        init_q75=q([r["initial_swaps"] for r in rs], .75), init_max=max(r["initial_swaps"] for r in rs),
        init_null_med=q([r["initial_null_swaps"] for r in rs], .5),
        init_over_slack_med=q([r["initial_swaps"] / r["slack"] for r in rs], .5),
        swaps_total_med=q([nswaps(r) for r in rs], .5),
        additions=sum(r["counts"].get("+N", 0) + r["counts"].get("+T", 0) for r in rs),
        truth_out_moves=sum(r["counts"].get("sTo", 0) + r["counts"].get("-T", 0) + r["counts"].get("sTT", 0) for r in rs),
        truth_in_moves=sum(r["counts"].get("sTi", 0) + r["counts"].get("+T", 0) for r in rs),
        reentries=sum(r["reentries"] for r in rs), seeds_swaps_after_del=sum(r["swaps_reappear"] for r in rs),
        miss_a=ma / len(dec_a) if dec_a else float("nan"), miss_a_lo=lo, miss_a_hi=hi,
        miss_a2=ma2 / len(dec_a2) if dec_a2 else float("nan"), miss_a2_lo=lo2, miss_a2_hi=hi2,
        arrived_a=sum(bool(r["caps"]["a"]["arrived"]) for r in rs),
        fs_minus_a_med=q([(r["first_scoring_scan"] - r["caps"]["a"]["a"]) if isinstance(r["first_scoring_scan"], int)
                          else None for r in rs], .5),
        final_is_S0=sum(bool(r["final_is_S0"]) for r in rs),
        seeds_with_ties=sum(r["ties"] > 0 for r in rs), tie_scans=sum(r["ties"] for r in rs),
        interior_ties=sum(r.get("interior_ties", 0) for r in rs),
        tie_sensitive=sum(bool(r.get("tie_outcome_sensitive")) for r in rs),
        ref_equal=f"{refeq[0]}/{refeq[1]}", fallbacks=sum(r["start_fallback"] for r in rs),
        max_abs_centre_med=q([r["max_abs_centre"] for r in rs], .5), x0_med=q([r["centre_x0"] for r in rs], .5),
        retained_xi_mean_med=q([r["retained_null_xi_mean"] for r in rs], .5),
        path_s_med=q([r["secs"]["path"] for r in rs], .5)))
if tab:
    with open(os.path.join(out_dir, "P1_cells.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, list(tab[0]))
        w.writeheader()
        w.writerows(tab)
    md += ["## P1 (exact CS; FAC-B baseline source partition = consecutive blocks of 16; NOT production tie-breaking)", "",
           "| ρ | n | c | seeds | K | ℓ+s0+1 | start=K | truth∈start | init swaps q25/med/q75/max | total swaps med | "
           "miss@a (95% CP) | miss@a2 (95% CP) | add | truth-out | reentries | swaps after 1st del | final=S0 | "
           "tie seeds / scans / sensitive | ref equal |", "|" + "---|" * 19]
    for t in tab:
        md.append(f"| {t['rho']} | {t['n']} | {t['c']} | {t['seeds']} | {t['K']} | {t['slack']} | {t['start_eq_K']} | "
                  f"{t['truth_in_start']} | {t['init_q25']:.0f}/{t['init_med']:.0f}/{t['init_q75']:.0f}/{t['init_max']} | "
                  f"{t['swaps_total_med']:.0f} | {fmt(t['miss_a'])} ({fmt(t['miss_a_lo'])}–{fmt(t['miss_a_hi'])}) | "
                  f"{fmt(t['miss_a2'])} ({fmt(t['miss_a2_lo'])}–{fmt(t['miss_a2_hi'])}) | {t['additions']} | "
                  f"{t['truth_out_moves']} | {t['reentries']} | {t['seeds_swaps_after_del']} | {t['final_is_S0']} | "
                  f"{t['seeds_with_ties']}/{t['tie_scans']}/{t['tie_sensitive']} | {t['ref_equal']} |")
    rng = np.random.default_rng(12345)
    trend = []
    for rho in sorted({k[0] for k in cells}):
        for c in sorted({k[2] for k in cells}):
            ns = sorted(k[1] for k in cells if k[0] == rho and k[2] == c)
            if len(ns) < 3:
                continue
            data = {n: np.array([r["initial_swaps"] for r in cells[(rho, n, c)]], float) for n in ns}
            ln = np.log(ns)

            def slope(meds):
                return float(np.polyfit(ln, np.log(np.maximum(meds, .5)), 1)[0])
            s_hat = slope([np.median(data[n]) for n in ns])
            boots = [slope([np.median(rng.choice(data[n], len(data[n]))) for n in ns]) for _ in range(2000)]
            trend.append(dict(rho=rho, c=c, n_values=" ".join(map(str, ns)), slope=s_hat,
                              boot_lo=float(np.quantile(boots, .025)), boot_hi=float(np.quantile(boots, .975)),
                              med_init_over_logn=" ".join(f"{np.median(data[n]) / math.log(n):.2f}" for n in ns),
                              med_init_over_slack=" ".join(f"{np.median(data[n]) / cells[(rho, n, c)][0]['slack']:.2f}"
                                                           for n in ns)))
    if trend:
        with open(os.path.join(out_dir, "P1_trend.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, list(trend[0]))
            w.writeheader()
            w.writerows(trend)
        md += ["", "### P1 n-trend of initial swaps (OLS slope of log median on log n; 2000 seed-bootstrap 95% interval)",
               "| ρ | c | n values | slope | boot 95% | median/log n per n | median/(ℓ+s0+1) per n |", "|---|---|---|---|---|---|---|"]
        for t in trend:
            md.append(f"| {t['rho']} | {t['c']} | {t['n_values']} | {t['slope']:.3f} | [{t['boot_lo']:.3f}, "
                      f"{t['boot_hi']:.3f}] | {t['med_init_over_logn']} | {t['med_init_over_slack']} |")
# ------------------------------------------------------------------------------------------------ P2
cells2 = {}
for r in rows:
    if r["prio"] == "P2":
        cells2.setdefault((r["variant"], r["n"], r["c"], r["mode"]), []).append(r)
tab2, win = [], []
for kk in sorted(cells2, key=lambda k: ({"v1": 0, "v3": 1, "v2": 2}[k[0]], k[3] == "early", k[1], k[2])):
    rs = cells2[kk]
    N = len(rs)
    r0 = rs[0]
    full = kk[3] == "full"
    top = opt(rs, lambda r: r.get("retained_nulls_are_top_xi"))
    tab2.append(dict(
        variant=kk[0], in_L2=r0["in_L2_hypotheses"], n=kk[1], c=kk[2], mode=kk[3], p=r0["p"], K=r0["K"], ell=r0["ell"],
        L0=r0["L0"], seeds=N, noncertified_full=sum(r["termination"] != "certified" for r in rs) if full else None,
        start_eq_K=sum(r["start_is_K"] for r in rs), truth_in_start=sum(r["truth_in_start"] for r in rs),
        top_xi=f"{top[0]}/{top[1]}", retained_minus_mu_med=q([r["retained_mean_minus_mu"] for r in rs], .5),
        init_min=min(r["initial_swaps"] for r in rs), init_med=q([r["initial_swaps"] for r in rs], .5),
        init_max=max(r["initial_swaps"] for r in rs),
        init_logn_med=q([r["initial_swaps_over_logn"] for r in rs], .5),
        init_logn_min=min(r["initial_swaps_over_logn"] for r in rs),
        init_null_min=min(r["initial_null_swaps"] for r in rs), init_null_med=q([r["initial_null_swaps"] for r in rs], .5),
        merged_miss_by_size=sum(r["merged_miss_by_size"] for r in rs),
        truth_in_idx_med=q([r["first_truth_in_move"][0] if r["first_truth_in_move"] else None for r in rs], .5),
        truth_out_seeds=sum(r["first_truth_out_index"] is not None for r in rs),
        miss_a=(sum(not r["caps"]["a"]["scored"] for r in rs) / N) if full else None,
        miss_a2=(sum(not r["caps"]["a2"]["scored"] for r in rs) / N) if full else None,
        final_is_S0=sum(bool(r["final_is_S0"]) for r in rs) if full else None,
        phase_drift_max=max(r["init_phase"]["centre_drift_max"] for r in rs),
        tie_seeds=sum(r["ties"] > 0 for r in rs), tie_sensitive=sum(bool(r.get("tie_outcome_sensitive")) for r in rs)))
    for Cw in sorted(r0["windows"], key=float):
        ws = [r["windows"][Cw] for r in rs]
        av = [w for w in ws if w["available"]]
        win.append(dict(variant=kk[0], n=kk[1], c=kk[2], mode=kk[3], C=float(Cw), L=ws[0]["L"], seeds=N,
                        available=len(av), all_null_null=sum(bool(w["all_null_null"]) for w in av),
                        all_truth_retained=sum(bool(w["all_truth_retained"]) for w in av),
                        drift_max=max((w["centre_drift_max"] for w in av), default=float("nan")),
                        drift_med=q([w["centre_drift_max"] for w in av], .5),
                        M_min=min((w["M_min"] for w in av), default=float("nan"))))
if tab2:
    for name, data in (("P2_cells.csv", tab2), ("P2_windows.csv", win)):
        with open(os.path.join(out_dir, name), "w", newline="") as f:
            w = csv.DictWriter(f, list(data[0]))
            w.writeheader()
            w.writerows(data)
    md += ["", "## P2 (SINGLETON partition — explicitly nonproduction; never pooled with P1). v1: s0=1 θ=1; v3: s0=2 "
           "θ=(1,1) (both within L2's hypotheses); v2: s0=2 θ=(1,−.1) (requested weak-truth diagnostic, NOT an L2 test)",
           "", "| var | n | c | mode | seeds | K | ℓ+s0+2 | start=K | truth∈start | top-ξ | retained mean−μ | "
           "init swaps min/med/max | init/log n med (min) | init null-null min/med | miss by size | truth-in idx med | "
           "truth-out seeds | miss@a | miss@a2 | final=S0 | tie seeds/sens |", "|" + "---|" * 21]
    for t in tab2:
        md.append(f"| {t['variant']} | {t['n']} | {t['c']} | {t['mode']} | {t['seeds']} | {t['K']} | {t['L0']} | "
                  f"{t['start_eq_K']} | {t['truth_in_start']} | {t['top_xi']} | {fmt(t['retained_minus_mu_med'], '{:.3f}')} | "
                  f"{t['init_min']}/{t['init_med']:.0f}/{t['init_max']} | {t['init_logn_med']:.1f} ({t['init_logn_min']:.1f}) | "
                  f"{t['init_null_min']}/{t['init_null_med']:.0f} | {t['merged_miss_by_size']} | "
                  f"{fmt(t['truth_in_idx_med'], '{:.0f}')} | {t['truth_out_seeds']} | {fmt(t['miss_a'])} | "
                  f"{fmt(t['miss_a2'])} | {fmt(t['final_is_S0'], '{}')} | {t['tie_seeds']}/{t['tie_sensitive']} |")
    md += ["", "### P2 fixed windows L = ⌈C log n⌉ (moves 0..L−1): seeds with window available / all null-null / all "
           "truths retained; max centre drift over window; min multiplier M", "",
           "| var | n | c | mode | C | L | avail | all sNN | truth kept | drift med / max | M min |",
           "|" + "---|" * 11]
    for w in win:
        md.append(f"| {w['variant']} | {w['n']} | {w['c']} | {w['mode']} | {w['C']} | {w['L']} | {w['available']}/{w['seeds']} | "
                  f"{w['all_null_null']} | {w['all_truth_retained']} | {fmt(w['drift_med'], '{:.3f}')} / "
                  f"{fmt(w['drift_max'], '{:.3f}')} | {fmt(w['M_min'], '{:.3f}')} |")
if conflicts:
    md += ["", f"**Quarantined conflicting keys:** {len(conflicts)} (see DEDUP.json)"]
open(os.path.join(out_dir, "SUMMARY.md"), "w", encoding="utf8").write("\n".join(md) + "\n")
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(md))
