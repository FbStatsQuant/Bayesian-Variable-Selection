#!/usr/bin/env python3
"""quote_model.py -- the cost quote of the precision + 10^4-science leg (LEG_PLAN section 5), from MEASURED V costs.
Stdlib only, deterministic (fixed seed). Usage:  quote_model.py --waves waves.json --measured measured_V_costs.csv [--reps 20000] > quote_output.txt

BASIS (measured): the 20 counted V fits of the 10^4 overlap (n = 200, N = 2,500, R' = 16, m = 1, I_max = 3; mean 1.99 core-h; sacct CPUTimeRAW/3600).
  island core-h        = 0.0256 + c_step * (T + 12)       T = bridging stages of the frozen grid (9..24 for AR/AR-weak/ADJ-OPP/IND, 1 for NULL),
                                                          12 = L (8 burn-in) + Hm (4 measured); OLS fit on the 20 fits, c_step = 0.00189 core-h/step; each fit uses
                                                          its OWN measured (T, per-island cost) so the T <-> cost correlation is kept (bootstrap over the measured fits of its design)
  m = 4                -> T x 4 (CONFIRMED on the F-equivalent binary: T = 23 -> 92, LEG_PLAN section 1); island = fixed + c_step * (4 T + 12)
  calibration          = the measured calibrate cost of the sampled fit (unrefined grid: m costs nothing there); I_max = 0 -> x U(0.2, 0.5) (UNMEASURED: pilot + preliminary grid)
  R' = 64              -> islands x 64; merge x (0.3 + 0.7 R'/16) (the island-reading part of the merge scales with R'; UNMEASURED, canary A0 measures it)
ASSUMED (UNMEASURED, stated, and the reason the first wave of each n-level is a pilot):
  n-scaling of the per-step cost = the planning model nf(n) = (3 (30 + 60 n/200) + 30) / 300 (0.7, 1.0, 1.6, 2.8 for n = 100, 200, 400, 800) x lognormal(0, 0.2)
  growth of the number of stages T with n: T(n) = T(200) (n/200)^g, g ~ U(0, 0.5), one draw per n-level and replicate (shared: it is a model error, not noise)
  BLK has no measurement: the AR pool is used with an extra lognormal(0, 0.2); exact linkage (A3) setup extra ~ U(0.1, 1.0) core-h per fit
  N = 10^4 (held arms, B2): island x 4 (per-step cost proportional to N); one common step-cost factor lognormal(0, 0.1) (node speed / load) per replicate
  infrastructure rerun: each fit independently w.p. 0.03 costs twice (the overlap had none; the 4 W0 evidence reruns are the only precedent)
"""
import argparse, csv, json, math, random, statistics as st

ap = argparse.ArgumentParser(); ap.add_argument("--waves", required=True); ap.add_argument("--measured", required=True)
ap.add_argument("--reps", type=int, default=20000); a = ap.parse_args()
rng = random.Random(20261119)
FIX, C_STEP = 0.0256, 0.00189
NF = {100: (3 * (30 + 60 * 100 / 200) + 30) / 300, 200: 1.0, 400: (3 * (30 + 60 * 400 / 200) + 30) / 300, 800: (3 * (30 + 60 * 800 / 200) + 30) / 300}
pool = {}
for r in csv.DictReader(open(a.measured)):
    d = {"ADJOPP": "ADJOPP", "AR": "AR", "ARweak": "ARweak", "IND": "IND", "NULL": "NULL"}[r["design"]]
    pool.setdefault(d, []).append({k: float(r[k]) for k in ("T", "setup", "calibrate", "per_island", "merge", "eval")})
W = json.load(open(a.waves))


def design(run_id):
    return run_id.split("-")[1]


class Fit:
    def __init__(s, f, wave):
        s.rid, s.wave, s.n, s.Rp, s.N = f["run_id"], wave, f["n"], f["Rp"], f["N"]
        s.d = design(s.rid); s.m = f["params"].get("refine_m", 1); s.I = f["params"].get("I_max", 3); s.a3 = "-A3-" in s.rid
        s.proxy = s.d == "BLK"; s.cls = ("prec N%d m%d I%d" % (s.N, s.m, s.I)) if s.Rp == 64 else ("A3 n%d" % s.n if s.a3 else "sci %s n%d" % (s.d, s.n))


fits = [Fit(f, w) for w, v in W.items() for b in v["batches"] for f in b["fits"]]


def draw_fit(f, g, nfac, G):
    row = rng.choice(pool["AR" if f.proxy else f.d])
    T0 = row["T"]; c = (row["per_island"] - FIX) / (T0 + 12)
    Tn = T0 if f.n == 200 else max(1.0, T0 * (f.n / 200.0) ** g[f.n])
    steps = (f.m * Tn + 12) if Tn > 1 else 13                    # a NULL grid has T = 1: refinement x m of one interval
    if Tn <= 1 and f.m > 1:
        steps = f.m + 12
    isl = FIX + c * nfac[f.n] * G * (f.N / 2500.0) * steps
    cal = row["calibrate"] * nfac[f.n] * G * (Tn / T0) * (rng.uniform(0.2, 0.5) if f.I == 0 else 1.0)
    mer = row["merge"] * (0.3 + 0.7 * f.Rp / 16.0)
    cost = row["setup"] * (f.n / 200.0) + cal + f.Rp * isl + mer + row["eval"]
    if f.a3:
        cost += rng.uniform(0.1, 1.0)
    if f.proxy:
        cost *= math.exp(rng.gauss(0, 0.2))
    rerun = rng.random() < 0.03
    if rerun:
        cost *= 2.0
    return cost, rerun


def pct(xs, q):
    xs = sorted(xs); k = (len(xs) - 1) * q; lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


tot = {w: [] for w in W}; fit_draw = {f.rid: [] for f in fits}; fit_norerun = {f.rid: [] for f in fits}
ns = sorted({f.n for f in fits})
for _ in range(a.reps):
    g = {n: rng.uniform(0.0, 0.5) for n in ns}
    nfac = {n: NF[n] * math.exp(rng.gauss(0, 0.2)) if n != 200 else 1.0 for n in ns}
    G = math.exp(rng.gauss(0, 0.1))
    per = {w: 0.0 for w in W}
    for f in fits:
        c, rr = draw_fit(f, g, nfac, G); per[f.wave] += c
        if _ < 4000:
            fit_draw[f.rid].append(c)
            if not rr:
                fit_norerun[f.rid].append(c)
    for w in W:
        tot[w].append(per[w])

released = [w for w in W if not w.startswith("H")]
held = [w for w in W if w.startswith("H")]
def line(name, xs):
    return "%-22s E %8.1f   P10 %8.1f  P50 %8.1f  P90 %8.1f  P99 %8.1f" % (name, st.mean(xs), pct(xs, .1), pct(xs, .5), pct(xs, .9), pct(xs, .99))
print("quote_model.py: %d replicates, %d fits in %d waves; measured pool: %s" % (a.reps, len(fits), len(W), {k: len(v) for k, v in pool.items()}))
print("\n== PER WAVE (billed core-h; stop > 2 x the quote; quote = E rounded to 5)")
for w in W:
    e = st.mean(tot[w]); q = 5 * round(e / 5.0)
    nfit = sum(len(b["fits"]) for b in W[w]["batches"])
    print("%-4s %3d fits  %s   QUOTE %4d  WAVE STOP > %4d   worst-case %7.1f" % (w, nfit, line("", tot[w])[1:], q, 2 * q, sum(b["worst_case_core_h"] for b in W[w]["batches"])))
def agg(ws):
    return [sum(tot[w][i] for w in ws) for i in range(a.reps)]
print("\n== LEG TOTALS")
# block totals from wave sums (A0 holds 2 precision fits + the A3 canary; it is counted in the precision part)
print(line("released (A0,P1-P4,S1-S9)", agg(released)))
print(line("  precision part P1-P4+A0", agg([w for w in released if w[0] in "AP"])))
print(line("  science part S1-S9", agg([w for w in released if w[0] == "S"])))
print(line("held N=10^4 (H1-H3)", agg(held)))
print(line("released + held", agg(list(W))))
rel = agg(released); full = agg(list(W))
E_rel, E_full = st.mean(rel), st.mean(full)
print("\nplan figure (MANIFEST_CELLS v0.4, precision 2,117 + science 2,010): 4,127.   released scope E = %.0f (%.1f%% of 4,127), P90 = %.0f, P99 = %.0f; with the held arms E = %.0f, P90 = %.0f, P99 = %.0f"
      % (E_rel, 100 * E_rel / 4127, pct(rel, .9), pct(rel, .99), E_full, pct(full, .9), pct(full, .99)))
print("P(released total > 4,127) = %.4f;  P(with held > 4,127) = %.4f" % (sum(x > 4127 for x in rel) / a.reps, sum(x > 4127 for x in full) / a.reps))
print("cumulative stop (1.6 x E of the scope in release): released %.0f -> %d ; with held %.0f -> %d ; projection ceiling = the plan figure 4,127"
      % (E_rel, 100 * math.ceil(1.6 * E_rel / 100), E_full, 100 * math.ceil(1.6 * E_full / 100)))
print("\n== PER-FIT MODEL BY CLASS (E over the fits of the class, first 4,000 replicates) -> per-fit stop = max(3.0, 1.5 x E)")
byc = {}
for f in fits:
    byc.setdefault(f.cls, []).append(f.rid)
print("%-30s %4s %8s %8s %8s %9s %14s %12s" % ("class", "fits", "E/fit", "P90/fit", "P99/fit", "STOP/fit", "P(>STOP|no rerun)", "P(>2.5xE|no rr)"))
exp_trips = 0.0; exp_hard = 0.0
for c, rids in sorted(byc.items()):
    xs = [x for r in rids for x in fit_draw[r]]; nr = [x for r in rids for x in fit_norerun[r]]
    E = st.mean(xs); S = max(3.0, 1.5 * E); H = max(3.0, 2.5 * E)
    p1 = sum(x > S for x in nr) / len(nr); p2 = sum(x > H for x in nr) / len(nr)
    exp_trips += len(rids) * p1; exp_hard += len(rids) * p2
    print("%-30s %4d %8.2f %8.2f %8.2f %9.1f %14.4f %12.4f" % (c, len(rids), E, pct(xs, .9), pct(xs, .99), S, p1, p2))
print("expected number of per-fit trips over the leg (186 fits, reruns excluded): %.1f at 1.5 x E; %.2f at 2.5 x E" % (exp_trips, exp_hard))
