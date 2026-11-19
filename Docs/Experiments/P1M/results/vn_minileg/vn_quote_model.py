#!/usr/bin/env python3
"""vn_quote_model.py -- cost quote of the V-N mini-leg from MEASURED twin costs (MINILEG_PLAN section 5). Stdlib, deterministic (fixed seed).
  vn_quote_model.py --waves waves_vn.json --twins twin_costs.csv [--reps 20000] > vn_quote_output.txt
Model. Each N = 10^4 fit has an N = 2,500 TWIN with the same seed (paired seeds: same data, same calibration, same grid, same T), measured in the precision leg on F:
  setup, calibrate, merge, eval  = the twin's (N-independent: H = 512, store size and merge are not N-dependent);   islands = the twin's x f, f = the island cost ratio N = 10^4 / 2,500.
  f: SAME-MACHINE ratio 3.85 (range 3.4-4.6; VN_MINILEG_NOTE section 1: Owls, 4 threads, one grid T = 20), i.e. effectively linear in N: modelled lognormal, median 3.85, sigma 0.09
  (so +-2 sigma = 3.2-4.6), ONE draw per replicate (a systematic error, not noise), plus per-fit noise sigma 0.04 (node speed / load), calibration +-10 %.
  r04 pair (R' 16, N 2,500): the I_max = 0 seed-2 fit = the measured r04 seed-1 fit (1.54); the I_max = 3 twin = x 1.5 (the 14 VF vs I_max-3 twins: 1.35 vs 2.02 on the leg).
  XB2 = its twin (4-AR-n200-r01-P-N2500-m1-I0-c1-s1, 5.545) x lognormal(0, 0.04).    A fit is re-run with probability 0.03 (cost doubles).
"""
import argparse, csv, json, math, random, statistics as st

ap = argparse.ArgumentParser(); ap.add_argument("--waves", required=True); ap.add_argument("--twins", required=True); ap.add_argument("--reps", type=int, default=20000); a = ap.parse_args()
rng = random.Random(20261119)
tw = {r["run_id"]: {k: float(r[k]) for k in ("setup", "calibrate", "islands", "merge", "eval", "fit_total")} for r in csv.DictReader(open(a.twins))}
W = json.load(open(a.waves))


def twin_of(rid):
    return rid.replace("-N10000-", "-N2500-")


class Fit:
    def __init__(s, f, w):
        s.rid, s.wave = f["run_id"], w
        if "-P-N10000-" in s.rid:
            s.kind = "N10000"; s.twin = tw[twin_of(s.rid)]; s.I = f["params"]["I_max"]
            s.cls = "vn N10000 m1 I%d" % s.I
        elif s.rid.endswith("-XB2-s1"):
            s.kind = "XB2"; s.twin = tw["4-AR-n200-r01-P-N2500-m1-I0-c1-s1"]; s.cls = "XB2 (N2500 R'64 I0, F2 vs F)"
        elif s.rid == "4-ADJOPP-n200-r04-VI3-s1":
            s.kind = "r04I3"; s.twin = tw["4-ADJOPP-n200-r04-V-s1"]; s.cls = "r04 pair (R'16)"
        else:
            s.kind = "r04s2"; s.twin = tw["4-ADJOPP-n200-r04-V-s1"]; s.cls = "r04 pair (R'16)"


fits = [Fit(f, w) for w, v in W.items() for b in v["batches"] for f in b["fits"]]


def draw(f, F):
    t = f.twin
    if f.kind == "N10000":
        cost = t["setup"] + t["calibrate"] * math.exp(rng.gauss(0, 0.10)) + t["merge"] + t["eval"] + t["islands"] * F * math.exp(rng.gauss(0, 0.04))
    elif f.kind == "XB2":
        cost = t["fit_total"] * math.exp(rng.gauss(0, 0.04))
    else:
        cost = t["fit_total"] * (1.5 if f.kind == "r04I3" else 1.0) * math.exp(rng.gauss(0, 0.10))
    rr = rng.random() < 0.03
    return (cost * 2.0 if rr else cost), rr


def pct(xs, q):
    xs = sorted(xs); k = (len(xs) - 1) * q; lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


tot = {w: [] for w in W}; fd = {f.rid: [] for f in fits}; fn = {f.rid: [] for f in fits}
for i in range(a.reps):
    F = 3.85 * math.exp(rng.gauss(0, 0.09)); per = {w: 0.0 for w in W}
    for f in fits:
        c, rr = draw(f, F); per[f.wave] += c
        if i < 4000:
            fd[f.rid].append(c)
            if not rr:
                fn[f.rid].append(c)
    for w in W:
        tot[w].append(per[w])
print("vn_quote_model.py: %d replicates, %d fits in %d waves; island factor f median 3.85 (sigma 0.09)" % (a.reps, len(fits), len(W)))
print("\n== PER WAVE (billed core-h; wave stop > 2 x quote; quote = E rounded to 5)")
for w in W:
    xs = tot[w]; e = st.mean(xs); q = 5 * round(e / 5.0)
    print("%-3s %2d fits  E %7.1f  P10 %7.1f  P50 %7.1f  P90 %7.1f  P99 %7.1f   QUOTE %4d  WAVE STOP > %4d" % (w, sum(len(b["fits"]) for b in W[w]["batches"]), e, pct(xs, .1), pct(xs, .5), pct(xs, .9), pct(xs, .99), q, 2 * q))
allw = [sum(tot[w][i] for w in W) for i in range(a.reps)]
n10 = [sum(c for f in fits if f.kind == "N10000" for c in [0]) for _ in range(1)]
E = st.mean(allw)
print("\n== MINI-LEG TOTAL   E %.1f  P10 %.1f  P50 %.1f  P90 %.1f  P99 %.1f   (approved H-28: ~440, P90 ~510, cap 600; r04 ~4)" % (E, pct(allw, .1), pct(allw, .5), pct(allw, .9), pct(allw, .99)))
print("P(total > 444) = %.4f ; P(total > 600) = %.4f" % (sum(x > 444 for x in allw) / a.reps, sum(x > 600 for x in allw) / a.reps))
print("cumulative stop (1.6 x E, rounded up to 50): %d ; projection ceiling = the approved cap 600" % (50 * math.ceil(1.6 * E / 50)))
print("\n== PER-FIT CLASS MODEL (committed): soft = max(3.0, 1.5 E), hard = max(3.0, 2.5 E)")
byc = {}
for f in fits:
    byc.setdefault(f.cls, []).append(f.rid)
print("%-30s %4s %8s %8s %8s %8s %8s %16s" % ("class", "fits", "E/fit", "P90/fit", "soft", "hard", "min..max E", "P(>soft|no rerun)"))
et = 0.0; eh = 0.0
for c, rids in sorted(byc.items()):
    xs = [x for r in rids for x in fd[r]]; nr = [x for r in rids for x in fn[r]]
    es = [st.mean(fd[r]) for r in rids]; E1 = st.mean(xs); S = max(3.0, 1.5 * E1); H = max(3.0, 2.5 * E1)
    p1 = sum(x > S for x in nr) / len(nr); et += len(rids) * p1; eh += len(rids) * sum(x > H for x in nr) / len(nr)
    print("%-30s %4d %8.2f %8.2f %8.1f %8.1f %8.1f..%-6.1f %12.4f" % (c, len(rids), E1, pct(xs, .9), S, H, min(es), max(es), p1))
print("expected soft trips (reruns excluded) %.2f ; hard trips %.3f" % (et, eh))
