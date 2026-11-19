#!/usr/bin/env python3
"""class_costs.py <wave>... [--records DIR] -- per-fit billed core-h BY CLASS from the collected cost records (p1m_cost.py output), for a pilot re-quote
(S7 -> S8, S9 -> S10; manager 11-19). Per fit: stages (setup / calibrate / islands / merge / eval core-h and wall max, maxRSS), class (committed table), cost, ratio to the
committed E; per class: n, mean, min, max, committed E / soft / hard, mean/E, and the cost split. Read-only. Stdlib only."""
import argparse, glob, json, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("srp", os.path.join(HERE, "stop_rules_prec.py")); srp = importlib.util.module_from_spec(sp); sp.loader.exec_module(srp)
ap = argparse.ArgumentParser(); ap.add_argument("waves", nargs="+"); ap.add_argument("--records", default="/home/fb31/SMC_Engineering_Department/records/precision1e4"); a = ap.parse_args()
rows = []
for w in a.waves:
    for f in sorted(glob.glob(os.path.join(a.records, w, "_batch_PL_%s_*" % w, "cost", "cost_4-*.json"))):
        j = json.load(open(f)); rid = j["run_id"]; st = j["stages"]
        rows.append({"wave": w, "run_id": rid, "class": srp.klass(rid), "core_h": j["billed_core_h"], "stages": {k: v["billed_core_h"] for k, v in st.items()},
                     "wall": {k: v["wall_s_max"] for k, v in st.items()}, "rss": max(v["max_rss_bytes"] for v in st.values()), "states": sorted({s for v in st.values() for s in v["states"]})})
print("%-34s %-14s %8s %7s | %7s %7s %7s %6s %6s | %s" % ("run_id", "class", "core-h", "x E", "setup", "calib", "islands", "merge", "eval", "wall max s (cal/isl/merge); maxRSS MB"))
for r in rows:
    E = srp.TABLE.get(r["class"], (None,))[0]; s = r["stages"]; w = r["wall"]
    print("%-34s %-14s %8.2f %7s | %7.3f %7.3f %7.3f %6.3f %6.3f | %s/%s/%s; %.0f %s" % (r["run_id"], r["class"], r["core_h"], ("%.2f" % (r["core_h"] / E)) if E else "-", s.get("setup", 0), s.get("calibrate", 0), s.get("islands", 0),
          s.get("merge", 0), s.get("eval", 0), w.get("calibrate"), w.get("islands"), w.get("merge"), r["rss"] / 1e6, "" if r["states"] == ["COMPLETED"] else r["states"]))
print("\n%-14s %3s %8s %8s %8s | %6s %6s %6s %7s | %s" % ("class", "n", "mean", "min", "max", "E", "soft", "hard", "mean/E", "mean split (setup/calib/islands/merge/eval)"))
cl = {}
for r in rows: cl.setdefault(r["class"], []).append(r)
tot = 0.0
for k, rs in sorted(cl.items()):
    n = len(rs); m = sum(x["core_h"] for x in rs) / n; tot += sum(x["core_h"] for x in rs); t = srp.TABLE.get(k)
    sp_ = [sum(x["stages"].get(s, 0) for x in rs) / n for s in ("setup", "calibrate", "islands", "merge", "eval")]
    print("%-14s %3d %8.2f %8.2f %8.2f | %6s %6s %6s %7s | %s" % (k, n, m, min(x["core_h"] for x in rs), max(x["core_h"] for x in rs), "%.2f" % t[0] if t else "-", "%.1f" % t[1] if t else "-", "%.1f" % t[2] if t else "-",
          ("%.2f" % (m / t[0])) if t else "-", "/".join("%.2f" % v for v in sp_)))
print("\nwave(s) %s: %d fits, %.2f core-h billed" % (",".join(a.waves), len(rows), tot))
