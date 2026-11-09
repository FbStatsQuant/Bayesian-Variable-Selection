"""summarize.py (v2, after X_R01) -- W2-SIM family X: per-cell summary of x_paths.py / x_paths_k.py raw JSONL.
Usage: python summarize.py OUT_PREFIX --tasks t1.tsv[,t2.tsv] [--ends e1.jsonl,...] raw1.jsonl [raw2.jsonl ...]
* Expected units are reconstructed from the task tables: (cell, seed, path_from) with path_from in {mode, full} for
  start=both (plus the data-dependent 'oracle_SstarN0' when present), {full} for start=full; both_seeds handled.
  Missing units are listed and the cell is marked INCOMPLETE (rates are then not interpretable as unbiased).
  Duplicates are an error. Task return codes (ends.jsonl) are reported.
* Per cell and prespecified binary outcome: k/m and Wilson 95% interval (both ends).
  Outcomes: pure_deletion, final_S0, S0_scored_within_cap, add_gain_pos (max addition gain > 0 at a visited set),
  numerically_ok, C1_start_eq_Sstar (mode paths only).
* Trend (FAC-X request "failure rate not decreasing in n at fixed A"): for each (item, load, rho, A_target, path_from)
  and outcome 'fail' = not (pure_deletion and final_S0): counts by n; if >= 1 failure, exact-conditional
  Cochran-Armitage test of a monotone trend in log10 n (Monte-Carlo permutation of the failure labels, 20000 draws,
  rng seed 1; one-sided p for increasing and for decreasing); with 0 failures the pooled Wilson upper bound is reported.
  These are finite-sample comparisons; they cannot establish an asymptotic rate."""
import sys, json, math, csv, collections, re
import statistics as st
import numpy as np

OUTCOMES = ["pure_deletion", "final_S0", "S0_scored_within_cap", "add_gain_pos", "numerically_ok"]


def wilson(k, m, z=1.96):
    if m == 0:
        return (float("nan"), float("nan"))
    ph = k / m
    den = 1 + z * z / m
    c = (ph + z * z / (2 * m)) / den
    h = z * math.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def parse_range(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def cellkey(r):
    return (r["item"], r["load"], r.get("mode", "iid"), r.get("coef", "std"), r.get("lseed", 0), float(r.get("rho", 0) or 0),
            int(r["n"]), int(r["p"]))


def expected_from_tasks(paths):
    exp = {}
    for tp in paths:
        for line in open(tp):
            if "\t" not in line:
                continue
            cmd = line.rstrip("\n").split("\t", 1)[1]
            if "x_paths" not in cmd:
                continue
            kv = dict(m.split("=", 1) for m in re.findall(r"(\S+=\S+)", cmd) if not m.startswith("$"))
            k = (kv.get("item", "K" if "x_paths_k" in cmd else "A") if "x_paths_k" not in cmd else
                 ("REAL" if kv["load"].startswith("real") else "K"),
                 kv.get("load", "cs"), kv.get("mode", "iid"), kv.get("coef", "std"), int(kv.get("lseed", 0)),
                 float(kv.get("rho", 0.5)) if "x_paths_k" not in cmd else 0.0, int(float(kv["n"])), int(kv["p"]))
            seeds = parse_range(kv.get("seeds", "0"))
            bs = set(parse_range(kv["both_seeds"])) if "both_seeds" in kv else None
            for s in seeds:
                sk = kv.get("start", "full" if "x_paths_k" not in cmd else "both")
                if bs is not None:
                    sk = "both" if s in bs else "full"
                pf = ["mode", "full"] if sk == "both" else [sk]
                for f in pf:
                    exp[(k, s, f)] = kv.get("A_target")
    return exp


def ca_trend(ns, fails, totals, draws=20000):
    """exact-conditional Cochran-Armitage via permutation of unit-level failure labels; score = log10 n."""
    x = np.concatenate([np.full(t, math.log10(n)) for n, t in zip(ns, totals)])
    y = np.concatenate([np.r_[np.ones(f), np.zeros(t - f)] for f, t in zip(fails, totals)])
    obs = float((x * y).sum())
    g = np.random.default_rng(1)
    sims = np.array([float((x * g.permutation(y)).sum()) for _ in range(draws)])
    return float((sims >= obs - 1e-12).mean()), float((sims <= obs + 1e-12).mean())


def main():
    pref = sys.argv[1]
    args = sys.argv[2:]
    tasks, ends, raws = [], [], []
    i = 0
    while i < len(args):
        if args[i] == "--tasks":
            tasks += args[i + 1].split(","); i += 2
        elif args[i] == "--ends":
            ends += args[i + 1].split(","); i += 2
        else:
            raws.append(args[i]); i += 1
    recs = []
    for fn in raws:
        for line in open(fn):
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    for r in recs:
        if "rho" not in r:
            r["rho"] = 0.0
    seen = set()
    for r in recs:
        key = (cellkey(r), r["seed"], r["path_from"])
        if key in seen:
            raise SystemExit(f"duplicate record {key}")
        seen.add(key)
    exp = expected_from_tasks(tasks) if tasks else {}
    missing = sorted(k for k in exp if k not in seen)
    unexpected = sorted(k for k in seen if exp and k not in exp and k[2] != "oracle_SstarN0")
    rcs = collections.Counter()
    for fn in ends:
        for line in open(fn):
            if line.strip():
                rcs[json.loads(line)["rc"]] += 1
    shas = collections.Counter(json.dumps({k: v for k, v in r["prov"].items() if k.endswith("sha256")}, sort_keys=True)
                               for r in recs)
    G = collections.OrderedDict()
    for r in sorted(recs, key=lambda r: (r["item"], r["load"], r.get("coef", "std"), r.get("lseed", 0), r["rho"],
                                         r.get("A_target") or r["A"], r["n"], r["path_from"])):
        G.setdefault((cellkey(r), r["path_from"]), []).append(r)
    miss_by_cell = collections.Counter((k[0], k[2]) for k in missing)
    rows = []
    for (ck, pf), rs in G.items():
        m = len(rs)
        row = dict(item=ck[0], load=ck[1], mode=ck[2], coef=ck[3], lseed=ck[4], rho=ck[5], n=ck[6], p=ck[7],
                   A_target=rs[0].get("A_target"), A_actual=round(rs[0].get("A_actual", rs[0]["A"]), 4),
                   p_capped=rs[0].get("p_capped_n2"), path_from=pf, units=m, missing=miss_by_cell.get((ck, pf), 0))
        row["complete"] = row["missing"] == 0
        vals = {"pure_deletion": [r["pure_deletion"] for r in rs], "final_S0": [r["final_is_S0"] for r in rs],
                "S0_scored_within_cap": [r["S0_scored_within_cap"] for r in rs],
                "add_gain_pos": [r["max_add_gain_over_logn"] > 0 for r in rs],
                "numerically_ok": [r.get("numerically_ok", True) for r in rs]}
        if pf == "mode" and "C1_start_eq_Sstar" in rs[0]:
            vals["C1_start_eq_Sstar"] = [r["C1_start_eq_Sstar"] for r in rs]
        for o, v in vals.items():
            k = int(sum(bool(x) for x in v))
            lo, hi = wilson(k, len(v))
            row[o] = k; row[o + "_lo"] = round(lo, 3); row[o + "_hi"] = round(hi, 3)
        row["fail"] = sum(not (r["pure_deletion"] and r["final_is_S0"]) for r in rs)
        def mx(key):
            v = [r.get(key) for r in rs if r.get(key) is not None]
            return round(max(v), 4) if v else None
        def md(key):
            v = [r.get(key) for r in rs if r.get(key) is not None]
            return round(st.median(v), 4) if v else None
        row.update(max_add_over_logn=mx("max_add_gain_over_logn"), med_add_over_logn=md("max_add_gain_over_logn"),
                   max_swap_minus_del=mx("max_swap_minus_del"),
                   min_del_gain=(round(min(r["min_del_gain"] for r in rs), 3)),
                   start_size_med=md("start_size"), mode_size_med=md("mode_size"), start_missing_med=md("start_missing"),
                   moves_med=md("moves"), cap_med=md("cap_mr1"),
                   xi_exc_w0_med=md("xi_exc_over_w0"), xi_exc_w0_max=mx("xi_exc_over_w0"),
                   xi_exc_varpi1_max=mx("xi_exc_over_varpi1"), xi_excess_w0_max=mx("xi_excess_over_w0"),
                   xi_defect_med=md("xi_defect_max"), cls_exc_w0_max=mx("cls_exc_over_w0"),
                   cls_excess_w0_max=mx("cls_excess_over_w0"), d_exc_w0_max=mx("d_exc_over_w0"),
                   s_rank_max=mx("s_rank_max"), cls_rank_max=mx("cls_rank_max"), common_rank_max=mx("common_rank_max"),
                   nonfinite_s=sum(r.get("nonfinite_s", 0) for r in rs),
                   delta_hat_w0_max=mx("delta_hat_over_w0"), absx_max=mx("absX_max"), floor_over_w0=md("floor_over_w0"),
                   val_max_absdiff=mx("val_max_absdiff"), min_top2_gap=(min([r["min_top2_gap_improving"] for r in rs
                                                                              if r.get("min_top2_gap_improving") is not None],
                                                                             default=None)),
                   t_path_med=md("t_path"),
                   seeds_fail=",".join(str(r["seed"]) for r in rs if not (r["pure_deletion"] and r["final_is_S0"])),
                   seeds_nondel=",".join(str(r["seed"]) for r in rs if not r["pure_deletion"]))
        rows.append(row)
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with open(pref + "_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # trend table
    T = collections.OrderedDict()
    for r in rows:
        if r["A_target"] is None:
            continue
        T.setdefault((r["item"], r["load"], r["coef"], r["lseed"], r["rho"], r["A_target"], r["path_from"]), []).append(r)
    trows = []
    for key, rs in T.items():
        rs = sorted(rs, key=lambda r: r["n"])
        ns = [r["n"] for r in rs]; fails = [r["fail"] for r in rs]; tots = [r["units"] for r in rs]
        F, M = sum(fails), sum(tots)
        if F:
            p_inc, p_dec = ca_trend(ns, fails, tots)
        else:
            p_inc = p_dec = None
        trows.append(dict(item=key[0], load=key[1], coef=key[2], lseed=key[3], rho=key[4], A_target=key[5], path_from=key[6],
                          n_list=" ".join(f"{n:.0e}" for n in ns), fails_by_n=" ".join(f"{f}/{t}" for f, t in zip(fails, tots)),
                          total=f"{F}/{M}", pooled_wilson_hi=round(wilson(F, M)[1], 3),
                          CA_p_increasing=p_inc, CA_p_decreasing=p_dec,
                          all_complete=all(r["complete"] for r in rs)))
    if trows:
        with open(pref + "_trend.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(trows[0].keys()))
            w.writeheader()
            for r in trows:
                w.writerow(r)

    def kmi(r, o):
        if o not in r:
            return ""
        return f"{r[o]}/{r['units']} [{r[o + '_lo']:.2f},{r[o + '_hi']:.2f}]"
    with open(pref + "_summary.md", "w", encoding="utf-8") as f:
        f.write(f"# Summary: {len(recs)} path records from {len(raws)} raw files\n\n")
        f.write(f"Expected units (from task tables {', '.join(tasks) or 'none'}): {len(exp)}; missing: {len(missing)}; "
                f"unexpected: {len(unexpected)}; task return codes: {dict(rcs)}; provenance sha sets: {len(shas)}\n\n")
        if missing:
            f.write("Missing units (first 50): " + "; ".join(f"{k[0]} seed {k[1]} {k[2]}" for k in missing[:50]) + "\n\n")
        cols = ["item", "load", "coef", "lseed", "rho", "A_target", "A_actual", "n", "p", "path_from", "units", "complete"]
        f.write("| " + " | ".join(cols + ["pure deletion", "final = S0", "S0 scored ≤ cap", "add gain > 0", "num ok",
                                        "C1 start = S*", "max add/log n", "start size med", "xi exc/w0 med|max",
                                        "xi excess/w0 max", "cls exc/w0 max", "s rank max", "δ̂/w0 max", "fail seeds"]) + " |\n")
        f.write("|" + "---|" * (len(cols) + 14) + "\n")
        for r in rows:
            f.write("| " + " | ".join(str(r[c]) for c in cols) + " | " + " | ".join([
                kmi(r, "pure_deletion"), kmi(r, "final_S0"), kmi(r, "S0_scored_within_cap"), kmi(r, "add_gain_pos"),
                kmi(r, "numerically_ok"), kmi(r, "C1_start_eq_Sstar"), str(r["max_add_over_logn"]),
                str(r["start_size_med"]), f"{r['xi_exc_w0_med']}|{r['xi_exc_w0_max']}", str(r["xi_excess_w0_max"]),
                str(r["cls_exc_w0_max"]), str(r["s_rank_max"]), str(r["delta_hat_w0_max"]), r["seeds_fail"] or "—"]) + " |\n")
        if trows:
            f.write("\n## Trend in n at fixed A_target (fail = not (pure deletion and final = S0))\n\n")
            tc = list(trows[0].keys())
            f.write("| " + " | ".join(tc) + " |\n|" + "---|" * len(tc) + "\n")
            for r in trows:
                f.write("| " + " | ".join(str(r[c]) for c in tc) + " |\n")
    print(f"{len(recs)} records, {len(rows)} cells, expected {len(exp)}, missing {len(missing)}, rc {dict(rcs)} -> {pref}_*")


if __name__ == "__main__":
    main()
