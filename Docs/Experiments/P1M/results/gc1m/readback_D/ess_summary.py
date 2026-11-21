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

# ---- added after the Opus check (F2, F4, F5): census stratified by N; early tempering steps; island-6 recovery band ----
print()
print("census stratified by N (all builds, then F2 da0cf85b only); rows = (N, n): TRUE of fits")
def strat(rows, title):
    c = collections.Counter()
    for r in rows: c[(r[3], r[1], bool(r[4]))] += 1
    print(title)
    keys = sorted({(k[0], k[1]) for k in c})
    for (N, n) in keys:
        t, f = c[(N, n, True)], c[(N, n, False)]
        print("  N %6s n %5s : TRUE %d of %d" % (N, n, t, t + f))
    byN = collections.Counter()
    for r in rows: byN[(r[3], bool(r[4]))] += 1
    for N in sorted({r[3] for r in rows}):
        print("  N %6s all n : TRUE %d of %d" % (N, byN[(N, True)], byN[(N, True)] + byN[(N, False)]))
strat(ev, "all builds, %d records" % len(ev))
strat(f2, "F2 only, %d records" % len(f2))
n200_hi = [r for r in ev if r[1] == 200 and r[2] >= 100000]
print("n 200, p >= 1e5 (all builds): %d records; N 2500: %d (TRUE %d); N 10000: %d (TRUE %d); the N 2500 ones: %s" % (
    len(n200_hi), sum(1 for r in n200_hi if r[3] == 2500), sum(1 for r in n200_hi if r[3] == 2500 and r[4]),
    sum(1 for r in n200_hi if r[3] == 10000), sum(1 for r in n200_hi if r[3] == 10000 and r[4]), [r[0] for r in n200_hi if r[3] == 2500]))
print()
print("early bridge steps (delta phi of stages 1-5) and the flagged stage, from st_phi of island 1")
def dphi(isl):
    f = sorted(isl)[0] if False else list(isl)[0]; p = isl[f]["st_phi"]
    return [round(p[i] - (p[i - 1] if i else 0), 4) for i in range(len(p))]
d = {os.path.basename(k): v for k, v in L("ess_D.json").items()}
print("  GC_D n 1000   :", dphi(d)[:5], "flagged stage 3 delta", dphi(d)[2])
print("  GC_P n 200 1M :", dphi(loc["GC_P"])[:5])
oth = L("ess_others.json")
print("  V0 ADJ-OPP n200 p1e4 N2500 :", dphi(oth["VN_V0_3/4-ADJOPP-n200-r04-V-s2"])[:5], "flagged stage 3 delta", dphi(oth["VN_V0_3/4-ADJOPP-n200-r04-V-s2"])[2])
for k in ("GB_G2a/5-ADJOPP-n200-r01-V-s1", "GB_G1a/5-AR-n200-r01-V-s1"):
    print("  %s (N 10000):" % k, dphi(oth[k])[:5])
import math
w1, N = 167.47, 2500
print("one-particle model, same ~54-unit outlier: dphi 0.095 -> w %.0f ESS/N %.3f ; dphi 0.041 -> w %.1f ESS/N %.3f" % (
    math.exp(0.0949 * 54), ((N - 1 + math.exp(0.0949 * 54)) ** 2 / (N - 1 + math.exp(0.0949 * 54) ** 2)) / N,
    math.exp(0.041 * 54), ((N - 1 + math.exp(0.041 * 54)) ** 2 / (N - 1 + math.exp(0.041 * 54) ** 2)) / N))
print()
print("island 6 (GC_D) stages 5-20 against the other 15 islands' range (min / max per stage)")
names = sorted(d, key=lambda s: int(s.split("_")[1].split(".")[0]))
e6 = d["island_6.bin"]["st_ess"]
below = []
for t in range(4, 20):
    oth15 = [d[n]["st_ess"][t] for n in names if n != "island_6.bin"]
    if e6[t] < min(oth15): below.append((t + 1, round(e6[t], 1), round(min(oth15), 1)))
    if e6[t] > max(oth15): print("  stage %d above the others' max" % (t + 1))
print("  stages where island 6 is below the other 15's minimum:", below, "(of 16 stages 5-20)")
print("  stage 4: all 16 islands in [%.1f, %.1f] (delta phi %.4f)" % (min(d[n]["st_ess"][3] for n in names), max(d[n]["st_ess"][3] for n in names), dphi(d)[3]))

# ---- added for HQ H-49: every flagged fit at N 2,500 with the island-stage events and the phi step (dphi) at each dip ----
print()
print("flagged fits (N 2500): island-stage events (island stage: ESS, ESS/N, dphi, phi); older-build islands read from NOTS (ess_oldbuild.json)")
def events(isl, N=2500):
    out = []
    for f, s in isl.items():
        ph = s["st_phi"]
        for t, x in enumerate(s["st_ess"]):
            if x < 0.5 * N: out.append((f.replace(".bin", ""), t + 1, round(x), round(x / N, 3), round(ph[t] - (ph[t - 1] if t else 0), 4), round(ph[t], 3)))
    return out
rows2 = [("GC_D n1000 p1e6 (F2)", {os.path.basename(k): v for k, v in L("ess_D.json").items()})]
rows2.append(("V0 ADJ-OPP r04 n200 p1e4 (F2)", oth["VN_V0_3/4-ADJOPP-n200-r04-V-s2"]))
for k, v in L("ess_oldbuild.json").items():
    rows2.append((k.split("/")[1] + (" n800 p1e4 (d0c30b65)" if "n800" in k else " n100 p1e4 (d0c30b65)"), v))
for name, isl in rows2:
    ev2 = events(isl); print("  %-44s %s" % (name, ev2))
