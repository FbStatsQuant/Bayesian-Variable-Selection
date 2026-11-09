"""summarize.py -- W2-SIM family PK: per-cell summaries reconciled against the frozen task tables.
usage: python summarize.py OUT_PREFIX TASKS_TSV::RAW_DIR [TASKS_TSV::RAW_DIR ...]
Each task line's command writes $OUT/raw/<NAME>.jsonl; the unit <NAME> is looked up as RAW_DIR/<NAME>.jsonl.
Reconciliation (fixed rule): all records of a unit (several lines, or the same unit in several specs = reruns) are compared
on their result fields; identical -> collapsed; different -> CONFLICT, unit excluded and listed; no record -> MISSING
(listed). Every record must carry the reference module sha256 set (the first one seen); otherwise PROVENANCE flag (excluded).
Censored units (limited = True: move limit reached) are excluded from endpoint / m* / k_hit statistics and counted apart.
Writes OUT_PREFIX_summary.md, OUT_PREFIX_cells.csv, OUT_PREFIX_units.jsonl (one compact line per unit, used units only)."""
import sys
import os
import re
import json
import math
import csv
from collections import defaultdict
import numpy as np

RESULT_FIELDS = ("seed", "start_size", "m_star", "k_hit", "final_is_S0", "moves_rle", "limited", "arrival")
COMPACT = ("exp", "design", "rho", "n", "p", "frac", "layout", "rep", "seed", "K", "ell", "start_size", "saturated",
           "start_has_S0", "start_truths", "lead_swaps", "n_swaps", "n_dels", "n_adds", "swaps_after_first_del",
           "adds_after_first_del", "first_del", "m_star", "m_star_over_K", "final_is_S0", "final_size", "limited", "k_hit",
           "arrival", "cap_MR1", "cap_2", "MR1_scores", "cap2_scores", "excess_over_MR1", "scan_ties", "size_ties",
           "within_ties", "start_n_optimal", "n_near_ties", "min_margin", "min_margin_reduced", "max_direct_absdiff",
           "direct_order_ok", "F_final_direct", "F_S0_direct", "moves_rle", "t_path")


def med_rng(v):
    v = [x for x in v if x is not None]
    if not v:
        return "—"
    m = float(np.median(v))
    fm = (lambda x: f"{x:.3g}" if not float(x).is_integer() else f"{int(x)}")
    return f"{fm(m)} [{fm(min(v))}, {fm(max(v))}]"


def key(d):
    return (d["exp"], d.get("design") or "cs_exact", d.get("rho"), d["n"], d["p"], d["layout"])


def any_tie(d):
    return ((d.get("scan_ties") or 0) > 0 or (d.get("size_ties") or 1) > 1 or (d.get("within_ties") or 0) > 0
            or (d.get("start_n_optimal") or 1) > 1)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    pref = sys.argv[1]
    specs = [a.split("::") for a in sys.argv[2:]]
    units = defaultdict(list)      # name -> list of (spec_idx, record)
    planned = []
    for si, (tsv, raw) in enumerate(specs):
        for line in open(tsv):
            if not line.strip():
                continue
            m = re.search(r"\$OUT/raw/(\S+)\.jsonl", line)
            name = m.group(1)
            if name not in planned:
                planned.append(name)
            f = os.path.join(raw, name + ".jsonl")
            if os.path.exists(f):
                for ln in open(f):
                    if ln.strip():
                        units[name].append((si, json.loads(ln)))
    used, missing, conflict, prov = [], [], [], []
    ref_sha = None
    for name in planned:
        recs = [r for _, r in units.get(name, [])]
        if not recs:
            missing.append(name)
            continue
        sigs = {json.dumps([r.get(f) for f in RESULT_FIELDS]) for r in recs}
        if len(sigs) > 1:
            conflict.append((name, len(recs)))
            continue
        d = recs[0]
        if ref_sha is None:
            ref_sha = d.get("module_sha")
        if d.get("module_sha") != ref_sha:
            prov.append(name)
            continue
        d["_unit"] = name
        d["_n_records"] = len(recs)
        used.append(d)
    cells = defaultdict(list)
    for d in used:
        cells[key(d)].append(d)
    out_rows = []
    for k in sorted(cells, key=lambda t: (t[0], t[1], t[2] or 0, t[3], t[4], t[5])):
        L = cells[k]
        U = [d for d in L if not d["limited"]]        # uncensored
        r = dict(exp=k[0], design=k[1], rho=k[2], n=k[3], p=k[4], layout=k[5], p_over_n=round(k[4] / k[3], 3),
                 N=len(L), censored=len(L) - len(U), K=L[0]["K"], ell=L[0]["ell"],
                 saturated=sum(d["saturated"] for d in L), start_size=med_rng([d["start_size"] for d in L]),
                 start_has_S0=sum(d["start_has_S0"] for d in L),
                 W=med_rng([d["lead_swaps"] for d in L]), W_minus_ell_s0=med_rng([d["W_minus_ell_s0"] for d in L]),
                 m_star_over_K=med_rng([round(d["m_star_over_K"], 4) for d in U]),
                 swaps_total=med_rng([d["n_swaps"] for d in U]),
                 runs_swaps_after_del=sum(d["swaps_after_first_del"] > 0 for d in U),
                 events_swaps_after_del=sum(d["swaps_after_first_del"] for d in U),
                 runs_adds=sum(d["n_adds"] > 0 for d in U), events_adds=sum(d["n_adds"] for d in U),
                 final_is_S0=sum(d["final_is_S0"] for d in U),
                 k_hit_finite=sum(d["k_hit"] is not None for d in U),
                 MR1_scores=sum(d["MR1_scores"] for d in L),
                 MR1_scores_saturated=sum(d["MR1_scores"] and d["saturated"] for d in L),
                 cap2_scores=sum(d["cap2_scores"] for d in L),
                 excess_over_MR1=med_rng([d["excess_over_MR1"] for d in U]),
                 runs_ties=sum(any_tie(d) for d in L), events_scan_ties=sum(d.get("scan_ties") or 0 for d in L),
                 runs_near_ties=sum((d.get("n_near_ties") or 0) > 0 for d in L),
                 max_direct_absdiff=(max(d.get("max_direct_absdiff") or 0 for d in L) if L[0].get("max_direct_absdiff") is not None else None),
                 direct_order_fail=sum(d.get("direct_order_ok") is False for d in L),
                 t_path_med=round(float(np.median([d["t_path"] for d in L])), 1))
        out_rows.append(r)
    cols = list(out_rows[0].keys()) if out_rows else []
    with open(pref + "_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    with open(pref + "_units.jsonl", "w") as f:
        for d in used:
            f.write(json.dumps({c: d.get(c) for c in COMPACT}) + "\n")
    show = ["design", "rho", "n", "p", "layout", "N", "censored", "K", "saturated", "start_size", "start_has_S0", "W",
            "W_minus_ell_s0", "m_star_over_K", "runs_swaps_after_del", "events_swaps_after_del", "runs_adds",
            "final_is_S0", "k_hit_finite", "MR1_scores", "MR1_scores_saturated", "cap2_scores", "excess_over_MR1",
            "runs_ties", "runs_near_ties", "max_direct_absdiff", "direct_order_fail"]
    L = ["# Summary: " + os.path.basename(pref), "",
         "specs (tasks::raw): " + "; ".join("::".join(s) for s in specs),
         f"planned units {len(planned)}; used {len(used)}; missing {len(missing)}; conflicting {len(conflict)}; "
         f"provenance-excluded {len(prov)}; reference module sha256: {json.dumps(ref_sha)}", "",
         "Counts out of N (used units of the cell); endpoint/m*/k_hit/excess statistics over uncensored units only. "
         "Medians [min, max]. W = leading swaps; excess = k_hit − (ℓ_n + |S̃₀|) (≤ 0 ⇔ MR1 scores S₀), over the "
         "k_hit_finite units. runs_* = number of runs with ≥ 1 event; events_* = total events.", "",
         "| " + " | ".join(show) + " |", "|" + "---|" * len(show)]
    for r in out_rows:
        L.append("| " + " | ".join(str(r[c]) for c in show) + " |")
    # descriptive n-trend of median W (log-log least squares), per (exp, design, rho, p/n, layout)
    grp = defaultdict(list)
    for r in out_rows:
        grp[(r["exp"], r["design"], r["rho"], r["p_over_n"], r["layout"])].append(r)
    L += ["", "## Descriptive n-trend of the median leading-swap count W (log-log LS slope; evidence, not a limit)", "",
          "| exp | design | rho | p/n | layout | n values | median W | slope |", "|---|---|---|---|---|---|---|---|"]
    for g, rows in sorted(grp.items(), key=lambda t: tuple(str(x) for x in t[0])):
        rows = sorted(rows, key=lambda r: r["n"])
        if len(rows) < 2:
            continue
        ns = [r["n"] for r in rows]
        mw = [float(np.median([d["lead_swaps"] for d in cells[(r["exp"], r["design"], r["rho"], r["n"], r["p"], r["layout"])]])) for r in rows]
        slope = (float(np.polyfit(np.log(ns), np.log(mw), 1)[0]) if all(x > 0 for x in mw) else None)
        L.append(f"| {g[0]} | {g[1]} | {g[2]} | {g[3]} | {g[4]} | {ns} | {mw} | {('%.3f' % slope) if slope is not None else '—'} |")
    exc = []
    for d in used:
        why = []
        if d["limited"]:
            why.append("CENSORED (move limit)")
        elif not d["final_is_S0"]:
            why.append("final!=S0")
        if not d["cap2_scores"]:
            why.append("cap2 miss")
        if d["saturated"] and d["MR1_scores"] and d["n"] >= 60000:
            why.append("MR1 scores in saturated run at n>=6e4")
        if d["n_adds"] > 0:
            why.append("additions")
        if any_tie(d):
            why.append("exact ties")
        if d.get("direct_order_ok") is False:
            why.append("direct re-scoring changes the winner order")
        if (d.get("max_direct_absdiff") or 0) > 1e-6:
            why.append(f"direct |dF| {d['max_direct_absdiff']:.2e}")
        if why:
            exc.append((d, why))
    L += ["", f"## Exceptional units ({len(exc)})", ""]
    for d, why in exc:
        extra = ""
        if "F_final_direct" in d:
            extra = f", F_final_direct={d['F_final_direct']:.6f}, F_S0_direct={d['F_S0_direct']:.6f}"
        L.append(f"* {d['_unit']} seed={d['seed']}: {', '.join(why)}; start={d['start_size']}/K={d['K']}, W={d['lead_swaps']}, "
                 f"m*={d['m_star']}, final_size={d['final_size']}, k_hit={d['k_hit']}, cap_MR1={d['cap_MR1']}{extra}; "
                 f"moves: {d['moves_rle'][:160]}")
    L += ["", f"## Missing units ({len(missing)})", "", ", ".join(missing) or "none",
          "", f"## Conflicting units ({len(conflict)})", "", ", ".join(f"{a} ({b} records)" for a, b in conflict) or "none",
          "", f"## Provenance-excluded units ({len(prov)})", "", ", ".join(prov) or "none"]
    open(pref + "_summary.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:12]))
    print(f"cells {len(out_rows)}, exceptional {len(exc)}")


if __name__ == "__main__":
    main()
