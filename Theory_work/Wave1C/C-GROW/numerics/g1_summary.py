"""g1_summary.py -- aggregates G1_raw.csv (+ G1_raw_p4000.csv) into G1_summary.md"""
import os, json, csv, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
seen = set()
for fn in ("G1_raw.csv", "G1_raw_p800.csv", "G1_raw_p4000.csv"):
    fp = os.path.join(HERE, fn)
    if os.path.exists(fp):
        with open(fp, newline="") as f:
            for r in csv.DictReader(f):
                k = (r["rho"], r["n"], r["p"], r["seed"])
                if k in seen:
                    continue
                seen.add(k)
                r["_file"] = fn
                rows.append(r)
B = lambda s: s == "True"
F = lambda s: float(s)
groups = {}
for r in rows:
    groups.setdefault((float(r["rho"]), int(r["n"]), int(r["p"])), []).append(r)
out = []
out.append("# G1 summary: falsification test of C-GROW lemma L6 (iid-row AR(1))\n")
out.append("Source: g1_run.py -> G1_raw.csv, G1_raw_p4000.csv; aggregated by g1_summary.py. Every number below is computed from those CSVs.\n")
out.append("Truths (0-based, s0=4, evenly spaced round((k+.5)p/4)): p=800: 100,300,500,700; p=1000: 125,375,625,875; p=2000: 250,750,1250,1750; p=4000: 500,1500,2500,3500. theta=(1.4,-1.0,1.8,-1.2).\n")
out.append("## Table 1: per design row (a), (c)\n")
out.append("| rho | n | p | #runs | d_n | |Q| | K | |S~0| (min/max) | max |S~0\\S0| | (a) S0 in S~0 | (a) S~0 in Q | (c) ell_n | (c) moves=|extras| & only -N & final=S0 (ell_n) | (c) same (ell_n+|S~0|) | S0 scored (ell_n / ell+) | local_limit (ell_n) |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for key in sorted(groups, key=lambda k: (k[1], k[2], k[0])):
    g = groups[key]
    N = len(g)
    ss = [int(r["start_size"]) for r in g]
    ex = [int(r["n_extra"]) for r in g]
    ok_ell = sum(B(r["c_ell_moves_eq_extras"]) and B(r["c_ell_only_delN"]) and B(r["c_ell_final_eq_S0"]) for r in g)
    ok_ellp = sum(B(r["c_ellplus_moves_eq_extras"]) and B(r["c_ellplus_only_delN"]) and B(r["c_ellplus_final_eq_S0"]) for r in g)
    sc1 = sum(B(r["c_ell_S0_scored"]) for r in g); sc2 = sum(B(r["c_ellplus_S0_scored"]) for r in g)
    ll = sum(B(r["c_ell_local_limit"]) for r in g)
    out.append("| %.1f | %d | %d | %d | %s | %s | %s | %d/%d | %d | %d/%d | %d/%d | %s | %d/%d | %d/%d | %d/%d, %d/%d | %d |" % (
        key[0], key[1], key[2], N, g[0]["d_n"], g[0]["Q_size"], g[0]["K"], min(ss), max(ss), max(ex),
        sum(B(r["a_S0_in_start"]) for r in g), N, sum(B(r["a_start_in_Q"]) for r in g), N, g[0]["ell_n"],
        ok_ell, N, ok_ellp, N, sc1, N, sc2, N, ll))
out.append("\n## Table 2: (a) violations (runs where S0 not in S~0 or S~0 not in Q)\n")
viol = [r for r in rows if not (B(r["a_S0_in_start"]) and B(r["a_start_in_Q"]))]
if not viol:
    out.append("None.\n")
else:
    out.append("| rho | n | p | seed | |S~0| | missing truths | variables outside Q | their distance to S0 | d_n |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for r in viol:
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["rho"], r["n"], r["p"], r["seed"], r["start_size"], r["missing"], r["outQ"], r["outQ_dist"], r["d_n"]))
out.append("\n## Table 3: (b) NA, max over tested family of F(T+l)-F(T)  (<0 needed)\n")
out.append("Family: all T=S0+1 extra from Q, T=S0, T=Q, all T=Q-1, plus 100 random S0<=T<=Q (T with |T|+1>K skipped). `near` = l in Q\\T, `far` = l outside Q (all p-|Q| of them). Cross-check vs Problem.F: max abs discrepancy shown.\n")
out.append("| rho | n | p | #T tested/run | max near (max over runs) | max far (max over runs) | #runs with far>0 | #runs with near>0 | max far among |T|<=5 | among |T| 6-15 | among |T|>15 | Schur vs Problem.F max diff |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
def bsz(r, k, i):
    d = json.loads(r["na_by_size"])
    return d[k][i] if k in d else float("-inf")
for key in sorted(groups, key=lambda k: (k[1], k[2], k[0])):
    g = groups[key]
    out.append("| %.1f | %d | %d | %s | %.3f | %.3f | %d/%d | %d/%d | %.3f | %.3f | %.3f | %.1e |" % (
        key[0], key[1], key[2], "%d-%d" % (min(int(r["nT"]) for r in g), max(int(r["nT"]) for r in g)),
        max(F(r["na_max_near"]) for r in g), max(F(r["na_max_far"]) for r in g),
        sum(F(r["na_max_far"]) > 0 for r in g), len(g), sum(F(r["na_max_near"]) > 0 for r in g), len(g),
        max(bsz(r, "T<=5", 1) for r in g), max(bsz(r, "T6-15", 1) for r in g), max(bsz(r, "T>15", 1) for r in g),
        max(F(r["na_schur_vs_F_maxdiff"]) for r in g)))
out.append("\nWorst NA violations (far l > 0), arg = [T kind, |T|, l, dist(l,S0)]:\n")
bad = sorted([r for r in rows if F(r["na_max_far"]) > 0], key=lambda r: -F(r["na_max_far"]))[:12]
for r in bad:
    out.append("- rho=%s n=%s p=%s seed=%s: max far = %.3f at %s (near max %.3f at %s)" % (r["rho"], r["n"], r["p"], r["seed"], F(r["na_max_far"]), r["na_arg_far"], F(r["na_max_near"]), r["na_arg_near"]))
out.append("\n## Table 4: (d) far-null h_{U,l}, l outside Q, U in block(l)\{l}\n")
out.append("T1 = 2 log p + 0.5 log n; junk = log(n+1) + 2 log(p/|S~0|) (per run). Sources per run: empty = U empty (all far l); U1 = |U|<=1 (all far l, all u in block); rand = 2000 random (l,U); fullblock = U=block\{l} (all far l); climb = ADAPTIVE search over U (coordinate ascent maximising h, 2 restarts, 50 top + 150 random l). `non-adaptive` = max of empty/U1/rand/fullblock. Max over runs:\n")
out.append("| rho | n | p | #runs | max non-adaptive h | max climb h | T1 | #runs non-adaptive>T1 | #runs climb>T1 | #runs any>junk | pairs>T1 / total per run | max by source: empty / U1 / rand / fullblock / climb |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for key in sorted(groups, key=lambda k: (k[1], k[2], k[0])):
    g = groups[key]
    T1 = F(g[0]["thr_2logp_halflogn"])
    na_ = [max(F(r[k]) for k in ("h_empty_max", "h_U1_max", "h_rand_max", "h_fullblock_max")) for r in g]
    cl = [F(r["h_climb_max"]) for r in g]
    jr = sum(F(r["h_overall_max"]) > F(r["thr_junk"]) for r in g)
    srcs = "/".join("%.1f" % max(F(r[k]) for r in g) for k in ("h_empty_max", "h_U1_max", "h_rand_max", "h_fullblock_max", "h_climb_max"))
    out.append("| %.1f | %d | %d | %d | %.2f | %.2f | %.2f | %d/%d | %d/%d | %d/%d | %d / %s | %s |" % (
        key[0], key[1], key[2], len(g), max(na_), max(cl), T1, sum(x > T1 for x in na_), len(g), sum(x > T1 for x in cl), len(g), jr, len(g),
        sum(int(r["n_h_above_T1"]) for r in g), g[0]["n_h_total"], srcs))
out.append("\n## Per-run raw table (rho,n,p,seed | |S~0| extras | NA near / far max | h max vs T1 vs junk | LS0 moves | time s)\n")
out.append("| rho | n | p | seed | |S~0| | extras | extras dist | NA near | NA far | h max | T1 | junk | moves(ell+) | seq | t_total |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in sorted(rows, key=lambda r: (int(r["n"]), int(r["p"]), float(r["rho"]), int(r["seed"]))):
    out.append("| %s | %s | %s | %s | %s | %s | %s | %.2f | %.2f | %.2f | %.2f | %.2f | %s | %s | %s |" % (
        r["rho"], r["n"], r["p"], r["seed"], r["start_size"], r["n_extra"], r["extras_dist"], F(r["na_max_near"]), F(r["na_max_far"]),
        F(r["h_overall_max"]), F(r["thr_2logp_halflogn"]), F(r["thr_junk"]), r["c_ellplus_moves"], r["c_ellplus_seq"], r["t_total"]))
open(os.path.join(HERE, "G1_summary.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out[:60]))
