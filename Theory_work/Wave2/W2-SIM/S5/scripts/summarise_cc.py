"""E-S5CC summariser (local, on the pulled raw JSONL).  v2 after design review R01 (reviews/S5_R01_design.md).
usage: python summarise_cc.py RAW.jsonl OUT_PREFIX TASKS.tsv [TASKS2.tsv ...]
* Input integrity (R01 item 5): every row must match a task of the given tables (key (q, rb, rw, p, n, seed)), no duplicate
  keys, rng_seed == 10007*seed + p; missing tasks are listed; inference stops (exit 2) on duplicates / unknown rows.
* Incomplete deletion paths (R01 item 2): phase statistics use only runs that visited the phase (denominators shown);
  scaling slopes use complete paths only; incomplete runs listed with fail_reason and m_final.
* Admissible delta (R01 item 3): min_T delta(T), deterministic e = 0 baseline, pass rates for delta in DELTAS.
* Competing moves (R01 item 4): additions every step, candidate swaps at checkpoints, terminal state (never acted on).
* Pairing (R01 item 6): deletion-sequence digest + all unrounded e-statistics.
* Imbalance events (R01 item 7), prespecified, among runs that visited m <= 5:
    E1 (primary) excursion: |I(m)| >= 2 for some m <= 5 (one excursion suffices: the KL-attempt end-phase argument has
       |I| <= 1 absorbing after the entry phase, so any |I| >= 2 at m <= 5 contradicts it unless the entry phase lasts
       until m <= 5);
    E2 re-entry: |I(m)| >= 2 at some m <= 5 after a state m' in (m, 30] with |I(m')| <= 1;
    E3 persistence: |I(m)| >= 2 at >= 2 of the states m in {5, 4, 3, 2, 1}.
  Reported with Wilson 95% intervals; for 0 events the upper bound is the largest rate not excluded.
* Slopes (R01 item 8): log(mean statistic) on log p, OLS over p; bootstrap CI (seeds resampled within p) only when every
  contributing cell has >= 2 complete runs, else "descriptive".
Bootstrap B = 4000, rng 20261109.
"""
import sys, json, math, re
import numpy as np

raw, pre, tables = sys.argv[1], sys.argv[2], sys.argv[3:]
rng = np.random.default_rng(20261109)
B = 4000
DELTAS = (0.0, 0.1, 0.25)


def key_of(q, rb, rw, p, n, seed):
    return (int(q), round(float(rb), 6), round(float(rw), 6), int(p), float(n), int(seed))


# ---------------------------------------------------------------- integrity
expected = {}
for t in tables:
    for line in open(t):
        if not line.strip(): continue
        tid, cmd = line.rstrip("\n").split("\t", 1)
        a = re.search(r"s5cc\.py\s+(.*?)\s*>", cmd).group(1).split()
        q, rb, rw = (a[3], a[4], a[5]) if len(a) > 3 else (5, .3, .7)
        expected[key_of(q, rb, rw, a[0], a[1], a[2])] = (t, tid)
R = [json.loads(l) for l in open(raw) if l.strip()]
seen, problems = {}, []
for r in R:
    k = key_of(r["q"], r["rb"], r["rw"], r["p"], r["n"], r["seed"])
    if k in seen: problems.append("duplicate key %s" % (k,))
    if k not in expected: problems.append("row not in task tables %s" % (k,))
    if r["rng_seed"] != 10007 * r["seed"] + r["p"]: problems.append("rng_seed mismatch %s" % (k,))
    seen[k] = r
missing = sorted(set(expected) - set(seen))
L = ["# E-S5CC summary (W2-SIM family S5)", "", "source: `%s` (%d rows); task tables: %s (%d tasks)" % (raw, len(R), ", ".join(tables), len(expected)),
     "", "Integrity: %d duplicate/unknown/rng problems; %d missing tasks%s." % (
         len(problems), len(missing), (": " + "; ".join("%s task %s" % expected[k] for k in missing[:40])) if missing else "")]
if problems:
    print("\n".join(L + problems)); sys.exit(2)


def des(r):
    return "S5(5,.3,.7)" if (r["q"], r["rb"], r["rw"]) == (5, .3, .7) else "CB(%d,%g,%g)" % (r["q"], r["rb"], r["rw"])


def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    ph = k / n; den = 1 + z * z / n; c = ph + z * z / (2 * n); h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return ((c - h) / den, (c + h) / den)


def bci(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2: return (float("nan"),) * 2
    mb = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return tuple(np.quantile(mb, [.025, .975]))


def vals(rs, f):
    return np.array([f(r) for r in rs if f(r) is not None], float)


cells = {}
for r in seen.values():
    cells.setdefault((des(r), r["p"], r["n"]), []).append(r)
keys = sorted(cells, key=lambda k: (k[0], k[1], k[2]))
out = {"integrity": dict(rows=len(R), expected=len(expected), missing=[list(k) for k in missing]), "cells": [], "slopes": {}}

# ---------------------------------------------------------------- path / competing moves / delta
L += ["", "## Deletion path (Pi of s3_cc.py) and competing moves (recorded, never acted on)", "",
      "deletion_path_complete = the deletion-only path reached S0 (= original field reached_S0); it is NOT a certification",
      "of the LS0 path: additions are checked at every step, candidate swaps (bcs_core Path._swaps) only at checkpoints.", "",
      "| design | p | n | runs | complete | incomplete (seed: reason, m_final) | max (add-del)/log n bulk / mid / end | steps add>=del | steps add>0 | max (swap-del)/log n bulk / mid / end | steps swap>=del (checked steps) | terminal improvable |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for key in keys:
    rs = sorted(cells[key], key=lambda r: r["seed"])
    comp = [r for r in rs if r["deletion_path_complete"]]
    inc = [r for r in rs if not r["deletion_path_complete"]]
    f = lambda d, ph: max([r[d][ph] for r in rs if r[d][ph] is not None], default=None)
    fm = lambda v: "-" if v is None else "%.3f" % v
    term = [r["terminal"]["improvable"] for r in comp if r.get("terminal")]
    L.append("| %s | %g | %g | %d | %d | %s | %s / %s / %s | %d | %d | %s / %s / %s | %d (%d) | %d/%d |" % (
        key[0], key[1], key[2], len(rs), len(comp), "; ".join("%d: %s, %d" % (r["seed"], r["fail_reason"], r["m_final"]) for r in inc) or "-",
        fm(f("add_minus_del_max", "bulk")), fm(f("add_minus_del_max", "mid")), fm(f("add_minus_del_max", "end")),
        sum(r["add_ge_del_steps"] for r in rs), sum(r["add_positive_steps"] for r in rs),
        fm(f("swap_minus_del_max", "bulk")), fm(f("swap_minus_del_max", "mid")), fm(f("swap_minus_del_max", "end")),
        sum(r["swap_ge_del_steps"] for r in rs), sum(r["swap_checked_steps"] for r in rs), sum(term), len(term)))
    out["cells"].append(dict(design=key[0], p=key[1], n=key[2], runs=len(rs), complete=len(comp),
                             incomplete=[dict(seed=r["seed"], reason=r["fail_reason"], m_final=r["m_final"]) for r in inc]))

L += ["", "## Centre condition CC_n(delta): admissible delta = min over visited T of 1 - (H_q + kappa0 max|e|)^2 / Lambda_k", "",
      "Baseline = the same with e = 0 (deterministic). A negative baseline means CC_n(delta) fails at this finite (p, n) for",
      "every delta >= 0 whatever e is (H_q^2 > Lambda_k): such cells cannot diagnose the global error; this is a finite-n",
      "statement and does not bear on the asymptotic Lemma KL.", "",
      "| design | p | n | baseline (e=0) | delta_adm mean / min | argmin m (median) | loss to e: mean (baseline - delta_adm) | pass rate delta >= " + " / ".join("%g" % d for d in DELTAS) + " |",
      "|---|---|---|---|---|---|---|---|"]
for c, key in zip(out["cells"], keys):
    rs = cells[key]
    da = vals(rs, lambda r: r["delta_adm_min"]); db = vals(rs, lambda r: r["delta_baseline_e0"])
    at = [r["delta_adm_min_at_m"] for r in rs]
    pr = [float(np.mean(da >= d)) for d in DELTAS]
    c.update(delta_baseline=[float(db.min()), float(db.max())], delta_adm_mean=float(da.mean()), delta_adm_min=float(da.min()),
             delta_pass=dict(zip([str(d) for d in DELTAS], pr)))
    L.append("| %s | %g | %g | %.4f%s | %.4f / %.4f | %g | %.4f | %s |" % (
        key[0], key[1], key[2], db.min(), "" if db.max() - db.min() < 1e-12 else " .. %.4f" % db.max(), da.mean(), da.min(),
        np.median(at), float(np.mean(db - da)), " / ".join("%.2f" % x for x in pr)))

# ---------------------------------------------------------------- e statistics
PH = [("r_bulk", "bulk"), ("r_mid", "mid"), ("r_end", "end"), ("rT_bulk", "bulk"), ("rT_mid", "mid"), ("rT_end", "end"),
      ("r_m_ge_p10", None), ("r_m_ge_sqrtp", None)]
L += ["", "## Global error in units of H = sqrt(2 log 2p): r = kappa0 max(|e_T|, max_j |e_{T minus j}|)/H, rT = centre only",
      "(per-run maxima over the phase; mean over runs that visited the phase [95% bootstrap CI], N = # such runs)", "",
      "| design | p | n | N | r_bulk mean [CI] | r_bulk median / q90 / max | frac r_bulk >= 0.03 | argmax m <= 35 | rT_bulk mean / max | r_mid mean / max (N) | r_end mean / max (N) | rT_end mean / max |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c, key in zip(out["cells"], keys):
    rs = cells[key]
    for f, _ in PH:
        x = vals(rs, lambda r: r[f])
        if len(x):
            lo, hi = bci(x)
            c[f] = dict(N=len(x), mean=float(x.mean()), median=float(np.median(x)), q90=float(np.quantile(x, .9)), max=float(x.max()),
                        ci_mean=[lo, hi], frac_ge_0p03=float(np.mean(x >= .03)))
        else:
            c[f] = None
    at = [r["r_bulk_at_m"] for r in rs if r["r_bulk_at_m"] is not None]
    c["r_bulk_at_m_le35_frac"] = float(np.mean(np.array(at) <= 35)) if at else None
    a = c["r_bulk"]
    g = lambda f, s: "-" if c[f] is None else s % (c[f]["mean"], c[f]["max"])
    if a is None:
        L.append("| %s | %g | %g | 0 | - | - | - | - | - | %s | %s | %s |" % (key[0], key[1], key[2], g("r_mid", "%.3f / %.3f"), g("r_end", "%.3f / %.3f"), g("rT_end", "%.3f / %.3f")))
    else:
        L.append("| %s | %g | %g | %d | %.4f [%.4f, %.4f] | %.4f / %.4f / %.4f | %.2f | %.2f | %s | %s (%s) | %s (%s) | %s |" % (
            key[0], key[1], key[2], a["N"], a["mean"], *a["ci_mean"], a["median"], a["q90"], a["max"], a["frac_ge_0p03"],
            c["r_bulk_at_m_le35_frac"], g("rT_bulk", "%.4f / %.4f"), g("r_mid", "%.3f / %.3f"), c["r_mid"]["N"] if c["r_mid"] else 0,
            g("r_end", "%.3f / %.3f"), c["r_end"]["N"] if c["r_end"] else 0, g("rT_end", "%.3f / %.3f")))
L += ["", "## Bulk proper: max r over m >= p/10 and over m >= sqrt(p)", "",
      "| design | p | n | r(m>=p/10) mean [95% CI] / max (N) | r(m>=sqrt p) mean [95% CI] / max (N) |", "|---|---|---|---|---|"]
for c, key in zip(out["cells"], keys):
    h = lambda f: "-" if c[f] is None else "%.4f [%.4f, %.4f] / %.4f (%d)" % (c[f]["mean"], *c[f]["ci_mean"], c[f]["max"], c[f]["N"])
    L.append("| %s | %g | %g | %s | %s |" % (key[0], key[1], key[2], h("r_m_ge_p10"), h("r_m_ge_sqrtp")))
allm = sorted({int(m) for rs in cells.values() for r in rs for m in r["m_checkpoints"]})
L += ["", "## r at fixed m (single visited state; mean over runs that visited m: r | centre-only rT)", "",
      "| design | p | n | " + " | ".join("m=%d" % m for m in allm) + " |", "|---|---|---|" + "---|" * len(allm)]
for c, key in zip(out["cells"], keys):
    rs = cells[key]; row = []; c["mchk_mean"] = {}
    for m in allm:
        v = [r["m_checkpoints"][str(m)] for r in rs if str(m) in r["m_checkpoints"]]
        if v:
            c["mchk_mean"][str(m)] = [float(np.mean([x[0] for x in v])), float(np.mean([x[1] for x in v])), len(v)]
            row.append("%.4f / %.4f" % tuple(c["mchk_mean"][str(m)][:2]))
        else:
            row.append("-")
    L.append("| %s | %g | %g | " % key + " | ".join(row) + " |")
bl = next(iter(cells.values()))[0]["band_lo"]
hdr = ["[%g,%s)" % (bl[i], ("%g" % bl[i + 1]) if i + 1 < len(bl) else "inf") for i in range(len(bl))]
L += ["", "## Bulk r by m-band (mean over runs of the per-run band maximum; '-' = band not visited)", "",
      "| design | p | n | " + " | ".join(hdr) + " |", "|---|---|---|" + "---|" * len(hdr)]
for c, key in zip(out["cells"], keys):
    rs = cells[key]; c["band_mean"] = []
    for i in range(len(bl)):
        v = [r["band_max"][i] for r in rs if r["band_max"][i] is not None]
        c["band_mean"].append(float(np.mean(v)) if v else None)
    L.append("| %s | %g | %g | " % key + " | ".join("-" if v is None else "%.4f" % v for v in c["band_mean"]) + " |")

# ---------------------------------------------------------------- imbalance
L += ["", "## End-phase imbalance I(m) = #(tau>0) - #(tau<0) over retained nulls (tau = deletion statistic tau_{j|T\\j})", "",
      "N = runs that visited m <= 5. E1 (primary) = excursion |I| >= 2 at some m <= 5; E2 = re-entry (|I| >= 2 at m <= 5 after",
      "|I| <= 1 at some m' in (m, 30]); E3 = |I| >= 2 at >= 2 of m in {5,..,1}. Wilson 95% intervals.", "",
      "| design | p | n | N | I30 dist | I10 dist | I5 dist | #|I|>=2 at m = 30/10/5/4/3/2/1 | E1 [95%] | E2 [95%] | E3 [95%] |",
      "|---|---|---|---|---|---|---|---|---|---|---|"]
for c, key in zip(out["cells"], keys):
    rs = [r for r in cells[key] if any(t[0] <= 5 for t in r["end_trace"])]
    N = len(rs)
    tr = [{t[0]: t[1] for t in r["end_trace"]} for r in rs]
    cnt = {m: (sum(abs(d[m]) >= 2 for d in tr if m in d), sum(m in d for d in tr)) for m in (30, 10, 5, 4, 3, 2, 1)}
    E1 = sum(any(abs(d[m]) >= 2 for m in d if m <= 5) for d in tr)
    E2 = 0
    for d in tr:
        ms = sorted(d, reverse=True)
        low = False; hit = False
        for m in ms:
            if m <= 5 and low and abs(d[m]) >= 2: hit = True
            if abs(d[m]) <= 1: low = True
        E2 += hit
    E3 = sum(sum(abs(d[m]) >= 2 for m in (5, 4, 3, 2, 1) if m in d) >= 2 for d in tr)
    dist = lambda m: {str(k): int(v) for k, v in zip(*np.unique([d[m] for d in tr if m in d], return_counts=True))}
    c.update(imb_N=N, I_absge2_counts={str(m): list(v) for m, v in cnt.items()}, E1=[E1, N, wilson(E1, N)],
             E2=[E2, N, wilson(E2, N)], E3=[E3, N, wilson(E3, N)], I30_dist=dist(30), I10_dist=dist(10), I5_dist=dist(5))
    w = lambda k: "%d/%d [%.2f, %.2f]" % (k, N, *wilson(k, N))
    L.append("| %s | %g | %g | %d | %s | %s | %s | %s | %s | %s | %s |" % (
        key[0], key[1], key[2], N, c["I30_dist"], c["I10_dist"], c["I5_dist"],
        " / ".join("%d" % cnt[m][0] for m in (30, 10, 5, 4, 3, 2, 1)), w(E1), w(E2), w(E3)))

# ---------------------------------------------------------------- slopes (complete paths only)
L += ["", "## Scaling with p: slope of log(mean statistic) on log p (complete paths only; OLS over p; 95% bootstrap CI, seeds",
      "resampled within p; 'descriptive' when a contributing cell has < 2 runs)", "",
      "| design | n | statistic | p values (runs) | slope [95% CI] |", "|---|---|---|---|---|"]
STATS = [(f, (lambda f: lambda r: r[f])(f)) for f, _ in PH] + \
        [("band[%g,..)" % lo, (lambda i: lambda r: r["band_max"][i])(i)) for i, lo in enumerate(bl)] + \
        [("r@m=%d" % m, (lambda m: lambda r: (r["m_checkpoints"].get(str(m)) or [None])[0])(m)) for m in (30, 100, 1000)]
for d in sorted({k[0] for k in cells}):
    for nn in sorted({k[2] for k in cells if k[0] == d}):
        ps = sorted({k[1] for k in cells if k[0] == d and k[2] == nn})
        for name, fn in STATS:
            ys = {}
            for pp in ps:
                v = [fn(r) for r in cells[(d, pp, nn)] if r["deletion_path_complete"] and fn(r) is not None]
                if v and min(v) > 0: ys[pp] = np.array(v, float)
            pv = sorted(ys)
            if len(pv) < 2: continue
            lx = np.log(pv)
            sl = np.polyfit(lx, np.log([ys[pp].mean() for pp in pv]), 1)[0]
            if min(len(ys[pp]) for pp in pv) >= 2:
                bs = [np.polyfit(lx, np.log([ys[pp][rng.integers(0, len(ys[pp]), len(ys[pp]))].mean() for pp in pv]), 1)[0] for _ in range(B)]
                lo, hi = np.quantile(bs, [.025, .975]); ci = "[%.3f, %.3f]" % (lo, hi)
            else:
                lo = hi = None; ci = "descriptive"
            out["slopes"]["%s|%g|%s" % (d, nn, name)] = dict(p=pv, runs=[len(ys[pp]) for pp in pv], slope=sl, ci=[lo, hi])
            L.append("| %s | %g | %s | %s | %.3f %s |" % (d, nn, name, ",".join("%g(%d)" % (pp, len(ys[pp])) for pp in pv), sl, ci))

# ---------------------------------------------------------------- n pairing
EF = ["r_bulk", "r_mid", "r_end", "rT_bulk", "rT_mid", "rT_end", "r_m_ge_p10", "r_m_ge_sqrtp", "band_max", "m_checkpoints",
      "end_trace", "del_sequence_sha1"]
L += ["", "## n-pairing check (same rng stream at n = 1e12 and 1e20; e_T itself does not depend on n)", ""]
out["n_pairing"] = []
for d in sorted({k[0] for k in cells}):
    for pp in sorted({k[1] for k in cells if k[0] == d}):
        ns = sorted({k[2] for k in cells if k[0] == d and k[1] == pp})
        if len(ns) != 2: continue
        A = {r["seed"]: r for r in cells[(d, pp, ns[0])]}; Bb = {r["seed"]: r for r in cells[(d, pp, ns[1])]}
        both = sorted(set(A) & set(Bb)); unp = sorted(set(A) ^ set(Bb))
        same_path = sum(A[s]["del_sequence_sha1"] == Bb[s]["del_sequence_sha1"] for s in both)
        same_all = sum(all(A[s][f] == Bb[s][f] for f in EF) for s in both)
        diff = sorted({f for s in both for f in EF if A[s][f] != Bb[s][f]})
        L.append("* %s p=%g: identical deletion sequence %d/%d, identical all e-statistics %d/%d; unpaired seeds %s; differing fields %s." % (
            d, pp, same_path, len(both), same_all, len(both), unp or "none", diff or "none"))
        out["n_pairing"].append(dict(design=d, p=pp, same_path=same_path, same_all=same_all, paired=len(both), unpaired=unp, differing=diff))
open(pre + "_summary.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(out, open(pre + "_summary.json", "w"), indent=1, default=float)
print("\n".join(L))
