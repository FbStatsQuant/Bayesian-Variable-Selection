"""Summarise results/pilot.jsonl (goal 4) into results/pilot_summary.txt."""
import json, math
from collections import defaultdict
import numpy as np

rows = list({(r["scen"], r["p"], r["scale"], r["n"], r["rep"]): r for r in (json.loads(l) for l in open("../results/pilot.jsonl") if l.strip())}.values())  # dedupe
cells = defaultdict(list)
for r in rows:
    cells[(r["scen"], r["p"], r["scale"], r["n"])].append(r)
L = ["# Pilot simulation (M §6.6) and one-pass candidate grid (M §6.7, V from pilot-scored models): per replicate",
     "# cols: scen p scale n rep | H | T_pilot (forced) | T_grid | 1-pi0(S0) | u1 | delta1 in [lb, est] | Delta_est | "
     "(T_pilot+1)Delta | (T_grid+1)Delta | frac particles at S0 after pilot | first-stage ESS frac"]
for k in sorted(cells):
    for r in sorted(cells[k], key=lambda r: r["rep"]):
        L.append("S%d %4d %.1f %4d r%d | %4d | %3d (%d) | %3d | %.3f | %.3f | [%.3f, %.3f] | %.3f | %.2f | %.2f | %.2f | %.2f" % (
            r["scen"], r["p"], r["scale"], r["n"], r["rep"], r["H"], r["T_pilot"], r["forced"], r["T_grid"],
            r["one_minus_pi0"], r["u1"], r["delta1_lb"], r["delta1_est"], r["Delta_est"],
            (r["T_pilot"] + 1) * r["Delta_est"], (r["T_grid"] + 1) * r["Delta_est"], r["frac_S0_end"], r["ess_first"]))
L.append("")
L.append("# By n (all scenarios/p/scales pooled): median T_pilot, T_grid, Delta_est, (T_grid+1)Delta_est; fraction of runs with (T_grid+1)Delta < 1")
byn = defaultdict(list)
for r in rows:
    byn[r["n"]].append(r)
for n in sorted(byn):
    rs = byn[n]
    v = [(r["T_grid"] + 1) * r["Delta_est"] for r in rs]
    vp = [(r["T_pilot"] + 1) * r["Delta_est"] for r in rs]
    L.append("n=%5d runs=%2d | T_pilot med %.1f [%d,%d] | T_grid med %.1f [%d,%d] | Delta med %.3f | (T_pilot+1)Delta med %.2f, <1 in %d/%d | "
             "(T_grid+1)Delta med %.2f, <1 in %d/%d" % (
                 n, len(rs), np.median([r["T_pilot"] for r in rs]), min(r["T_pilot"] for r in rs), max(r["T_pilot"] for r in rs),
                 np.median([r["T_grid"] for r in rs]), min(r["T_grid"] for r in rs), max(r["T_grid"] for r in rs),
                 np.median([r["Delta_est"] for r in rs]), np.median(vp), sum(x < 1 for x in vp), len(vp),
                 np.median(v), sum(x < 1 for x in v), len(v)))
open("../results/pilot_summary.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
