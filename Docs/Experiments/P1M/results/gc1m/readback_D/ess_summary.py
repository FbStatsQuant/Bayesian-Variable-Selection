#!/usr/bin/env python3
"""ess_summary.py -- descriptive, unregistered (GC_D read-back, HQ H-47): summarises the per-stage ESS (island section st_ess) read by ess_read.py / ess_many.py
and the low_empirical_ESS census over every eval.bin.json under records/. Reads only JSON in this directory. Usage: python3 -I ess_summary.py > ess_summary.txt
Flag rule (merge.h l.486 of F2): low_empirical_ESS = any island stage ESS < 0.5 N; ESS_t = (sum w)^2 / sum w^2, w_i = exp(dphi_t d_i) (island_run.h l.779)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
L = lambda f: json.load(open(os.path.join(H, f)))
def stats(isl, N):
    allv = [(x, f, t + 1) for f, s in isl.items() for t, x in enumerate(s["st_ess"])]
    mn = min(allv); low = [(round(x, 1), f, t) for x, f, t in allv if x < 0.5 * N]
    return len(isl), len(allv) // max(1, len(isl)), len(allv), round(mn[0], 1), mn[1], mn[2], round(mn[0] / N, 3), low
rows = []
d = L("ess_D.json"); rows.append(("GC_D 6-AR-n1000-r01 (1M, N 2500, F2)", 2500, {os.path.basename(k): v for k, v in d.items()}))
loc = L("ess_local.json"); rows.append(("GC_P 6-AR-n200-r01 (1M, N 2500, F2)", 2500, loc["GC_P"])); rows.append(("11-17 6-AR-n200-r01 (1M, N 2500, I_max 3)", 2500, loc["F1M_pilot_1117"]))
N_OF = {"VN_V0_3/4-ADJOPP-n200-r04-V-s2": 2500}
for k, v in L("ess_others.json").items():
    rows.append((k + (" (p 1e4, F2)" if k.startswith("VN_V0") else " (p 1e5, F2, N 10000)"), N_OF.get(k, 10000), v))
print("%-62s %4s %5s %6s  %9s %-12s %-6s %7s  %s" % ("fit", "isl", "T", "stages", "min ESS", "where", "stage", "min/N", "island-stages < 0.5 N"))
for name, N, isl in rows:
    n, T, tot, mn, f, t, r, low = stats(isl, N)
    print("%-62s %4d %5d %6d  %9.1f %-12s %-6d %7.3f  %d %s" % (name, n, T, tot, mn, f, t, r, len(low), low if low else ""))
print()
ev = L("eval_flags_all.json")   # [path, n, p, N, low_empirical_ESS, checks_passed_final, binary sha8]
import collections
c = collections.Counter(); 
for r in ev: c[(r[1], r[2], bool(r[4]))] += 1
print("low_empirical_ESS census over all %d eval.bin.json under records/ (all builds):" % len(ev))
for (n, p), _ in sorted({(k[0], k[1]): 0 for k in c}.items()):
    print("  n %5s p %8s : TRUE %d of %d" % (n, p, c[(n, p, True)], c[(n, p, True)] + c[(n, p, False)]))
print("TRUE fits:")
for r in ev:
    if r[4]: print("  ", r[0], "n", r[1], "p", r[2], "binary", r[6])
f2 = [r for r in ev if r[6] == "da0cf85b"]
print("F2 build (da0cf85b) only: %d fits, TRUE %d; n=200 F2: %d fits, TRUE %d" % (len(f2), sum(1 for r in f2 if r[4]), sum(1 for r in f2 if r[1] == 200), sum(1 for r in f2 if r[1] == 200 and r[4])))
